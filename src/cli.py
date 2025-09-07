"""Enhanced CLI for document chat with LLM integration."""
import argparse
import asyncio
import subprocess
import uuid
from pathlib import Path

from . import __version__
from .document_processor import load_text
from .embeddings import Embeddings
from .vector_store import get_default_store
from .backends.ollama_backend import OllamaBackend
from .tts import speak


EMB = Embeddings()
STORE = get_default_store()
BACKEND = OllamaBackend()

# Store the last response for --read command
_last_response = None
_last_added_docs = []


def cmd_add(paths):
    """Add documents to the knowledge base."""
    added = []
    for p in paths:
        p = Path(p)
        if not p.exists():
            print(f"❌ File not found: {p}")
            continue
        try:
            text = load_text(str(p))
            if not text.strip():
                print(f"⚠️  Empty or unreadable file: {p}")
                continue
        except Exception as e:
            print(f"❌ Error loading {p}: {e}")
            continue
        vec = EMB.embed([text])[0]
        doc_id = str(uuid.uuid4())
        STORE.add(doc_id, text, vec, metadata={"source": str(p)})
        print(f"✅ Indexed: {p} -> id={doc_id}")
        added.append(doc_id)

    # record last added documents for immediate read
    global _last_added_docs
    if added:
        _last_added_docs = added
    return added


def cmd_read(text_or_doc_id=None):
    """Read text out loud using TTS."""
    global _last_response

    if text_or_doc_id is None:
        # Read the last response if no argument provided
        if _last_response:
            text_to_read = _last_response
            print("🔊 Reading last response...")
        else:
            print("❌ No text to read. Use --ask first or provide a document ID.")
            return
    else:
        # Try to find document by ID
        docs = STORE.list_documents()
        doc = next((d for d in docs if d["id"] == text_or_doc_id), None)

        if doc:
            # Read the document content
            try:
                text_to_read = load_text(doc["source"])
                print(f"🔊 Reading document: {Path(doc['source']).name}")
            except Exception as e:
                print(f"❌ Error loading document: {e}")
                return
        else:
            # Check if it's a valid document ID format (UUID)
            import re
            if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', text_or_doc_id):
                print(f"❌ Document with ID '{text_or_doc_id}' not found")
                return
            else:
                # Treat as direct text input
                text_to_read = text_or_doc_id
                print("🔊 Reading provided text...")

    # Use the TTS helper
    ok = speak(text_to_read)
    if ok:
        print("✅ Text reading completed")
    else:
        print("❌ TTS not available or failed. Install 'pyttsx3' or use macOS 'say'.")


def cmd_list():
    """List all indexed documents."""
    docs = STORE.list_documents()
    if not docs:
        print("📭 No documents indexed yet. Use --add to add some documents.")
        return

    print(f"📚 Indexed Documents ({len(docs)} total):")
    print("-" * 60)
    for doc in docs:
        source = Path(doc["source"]).name if doc["source"] != "unknown" else "unknown"
        print(f"ID: {doc['id']}")
        print(f"Source: {source}")
        print(f"Length: {doc['text_length']} characters")
        print("-" * 60)


def cmd_remove(doc_ids):
    """Remove documents by ID."""
    for doc_id in doc_ids:
        if STORE.remove_document(doc_id):
            print(f"✅ Removed document: {doc_id}")
        else:
            print(f"❌ Document not found: {doc_id}")


def cmd_query(q, k=3):
    """Search documents without LLM chat."""
    vec = EMB.embed([q])[0]
    results = STORE.search(vec, top_k=k)
    if not results:
        print("🔍 No relevant documents found.")
        return

    print(f"🔍 Search results for: '{q}'")
    print("-" * 60)
    for score, item in results:
        source = Path(item.get('metadata', {}).get('source', 'unknown')).name
        print(f"📄 Source: {source} (score: {score:.4f})")
        print(f"ID: {item.get('id')}")
        snippet = item.get("text", "")[:400].replace("\n", " ")
        print(f"📖 Snippet: {snippet}")
        print("-" * 60)


async def cmd_ask(question, k=3):
    """Ask a question with LLM-powered response."""
    # First, search for relevant context
    vec = EMB.embed([question])[0]
    results = STORE.search(vec, top_k=k)

    if not results:
        print("🔍 No relevant documents found to answer your question.")
        return

    # Build context from top results
    context_parts = []
    sources = []
    for score, item in results:
        if score > 0.05:  # Lower threshold for LLM context
            context_parts.append(item.get("text", ""))
            source = Path(item.get('metadata', {}).get('source', 'unknown')).name
            sources.append(f"{source} (relevance: {score:.2f})")

    if not context_parts:
        print("🔍 No sufficiently relevant documents found.")
        return

    context = "\n\n".join(context_parts)

    # Build prompt for LLM
    prompt = f"""You are a helpful assistant that answers questions based on the provided documents.

Context from documents:
{context}

Question: {question}

Please provide a clear, concise answer based on the context above. If the context doesn't contain enough information to fully answer the question, say so."""

    print(f"🤔 Question: {question}")
    print(f"📚 Found {len(sources)} relevant sources:")
    for source in sources:
        print(f"   • {source}")
    print("\n💭 Thinking...")

    try:
        response = await BACKEND.generate(prompt)
        print(f"\n🤖 Answer: {response}")
        # Store the response for potential TTS reading
        global _last_response
        _last_response = response
    except Exception as e:
        print(f"\n❌ Error generating response: {e}")
        print("💡 Make sure Ollama is running with: ollama serve")


async def cmd_chat():
    """Start interactive chat mode."""
    print("🚀 Starting interactive chat mode!")
    print("💡 Type 'quit' or 'exit' to end the session.")
    print("💡 Type 'help' for available commands.")
    print("-" * 60)

    while True:
        try:
            question = input("You: ").strip()
            if not question:
                continue
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            if question.lower() == 'help':
                print("Available commands:")
                print("  • Type your question to chat with documents")
                print("  • 'quit' or 'exit' to end session")
                print("  • 'help' to show this message")
                continue

            await cmd_ask(question)
            print("-" * 60)

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break


def main():
    parser = argparse.ArgumentParser(
        prog="doc-chat",
        description="AI-powered document chat and search tool"
    )
    parser.add_argument("--version", action="store_true", help="show version")
    parser.add_argument("--add", nargs="+", help="add documents to knowledge base")
    parser.add_argument("--list", action="store_true", help="list all indexed documents")
    parser.add_argument("--remove", nargs="+", help="remove documents by ID")
    parser.add_argument("--query", help="search documents (no LLM)")
    parser.add_argument("--ask", help="ask question with LLM response")
    parser.add_argument("--chat", action="store_true", help="start interactive chat mode")
    parser.add_argument("--read", nargs="?", const="", default=None, help="read text out loud (last response if no arg, or document ID/text)")

    args = parser.parse_args()

    if args.version:
        print(f"doc-chat v{__version__}")
        return

    # Process commands in a logical order
    added_ids = None
    if args.add:
        added_ids = cmd_add(args.add)

    if args.list:
        cmd_list()

    if args.remove:
        cmd_remove(args.remove)

    if args.query:
        cmd_query(args.query)

    if args.ask:
        asyncio.run(cmd_ask(args.ask))

    if args.chat:
        asyncio.run(cmd_chat())

    # Handle --read: three modes
    # 1) --read (no value) -> read the last document added in this invocation, or last-added overall
    # 2) --read <doc_id> -> read document by id (or text if not an id)
    # 3) --read not provided -> nothing
    if args.read is not None:
        # args.read == "" -> option was present without a value
        if args.read == "":
            # no-arg: prefer the doc most-recently added in this run
            target_id = None
            if added_ids:
                target_id = added_ids[-1]
            elif _last_added_docs:
                target_id = _last_added_docs[-1]

            if target_id:
                cmd_read(target_id)
            else:
                # fallback to reading last LLM response
                cmd_read(None)
        else:
            # explicit value passed (doc id or text)
            cmd_read(args.read)

    # If no commands were specified, show help
    if not any([args.add, args.list, args.remove, args.query, args.ask, args.chat, args.read, args.version]):
        parser.print_help()


if __name__ == "__main__":
    main()
