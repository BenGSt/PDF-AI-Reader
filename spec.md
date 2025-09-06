# Cross-Platform Local LLM Document Chat App - Specifications

## Overview
A portable document assistant that automatically optimizes for available hardware across macOS, Linux, and Windows. Features RAG (Retrieval-Augmented Generation) capabilities with offline LLM processing, starting with Apple Silicon optimization and expanding to CUDA, ROCm, and CPU-only systems.
 
## MVP Scope

- Goal: Minimal, offline-first document chat that reliably runs on macOS (Apple Silicon) with a CPU fallback for other platforms.
- Minimum features:
       - PDF ingestion plus Markdown and plain-text support
       - Semantic chunking with configurable overlap
       - Local embeddings (sentence-transformers) stored in ChromaDB
       - Simple Top-K retrieval and context assembly for prompts
       - Ollama backend support on macOS with llama.cpp (CPU) fallback
       - Basic CLI: add, list, remove, ask, start
       - Source citation included in responses
- Success criteria:
       - Index a 100-page PDF within a single run
       - Return a relevant answer with sources within 10s on Apple M-series hardware
       - End-to-end offline flow: add -> index -> ask -> answer with sources

## Core Features

### 1. Multi-Platform Document Processing
- **Supported Formats**: PDFs, Word docs, Markdown, plain text
- **Cross-Platform Extraction**: Platform-agnostic document loading
- **Universal File Handling**: Consistent behavior across operating systems

### 2. Local RAG Pipeline
- **Document Ingestion**: Multiple PDFs, Word docs, markdown files
- **Text Chunking**: Semantic chunking with overlap for context preservation
- **Vector Embeddings**: Local sentence-transformers model
- **Vector Storage**: ChromaDB for similarity search
- **Context Retrieval**: Top-K similarity search with re-ranking

### 3. Adaptive LLM Integration
- **Hardware Detection**: Automatic platform and GPU detection
- **Model Selection**: Hardware-optimized model recommendations
- **Multiple Backends**: Ollama (primary), llama.cpp (fallback), cloud APIs (future)
- **Performance Scaling**: 3-30+ tokens/second depending on hardware
- **Context Windows**: 4K-128K tokens based on model capabilities
- **Offline First**: No internet required for core functionality

### 4. Platform-Aware Chat Interface
- **Multi-Document Chat**: Ask questions across multiple documents
- **Hardware-Optimized Performance**: Platform-specific optimizations
- **Source Citations**: Reference specific documents and sections
- **Context Awareness**: Maintain conversation history
- **Document Management**: Add/remove documents from knowledge base
- **Cross-Platform Search**: Find specific content across collection

### 5. Universal CLI Commands
```bash
# Basic usage (works on Mac/Linux/Windows)
doc-chat --add document.pdf another-doc.docx
doc-chat --start  # Start interactive session

# Interactive commands:
/add <file>           # Add document to knowledge base
/list                 # List all indexed documents
/remove <doc>         # Remove document from knowledge base
/search <term>        # Semantic search across all documents
/ask <question>       # Chat with your documents
/sources             # Show sources for last response
/clear               # Clear conversation history
/status              # Show system status (platform, model, memory, docs)
/models              # List available models for your hardware
/switch <model>      # Switch between models
/hardware            # Show hardware capabilities and recommendations
```

## Cross-Platform Technical Architecture

### Hardware Abstraction Layer (HAL)
```
Application Layer (Universal)
       ↓
   HAL Interface
       ↓
Platform Backends (Mac/Linux/Windows)
       ↓
Hardware Optimizations (Metal/CUDA/ROCm/CPU)
```

### Platform Detection System
- **Automatic Hardware Detection**: CPU architecture, memory, GPU capabilities
- **Model Recommendations**: Hardware-appropriate model suggestions
- **Performance Optimization**: Platform-specific acceleration (Metal/CUDA/ROCm)
- **Graceful Degradation**: Fallback to CPU processing when GPU unavailable

### LLM Backend Abstraction
- **Primary**: Ollama HTTP API (all platforms)
- **Fallback**: llama.cpp binaries (platform-specific)
- **Future**: Cloud APIs for low-end hardware
- **Interface**: Unified async API regardless of backend

### Platform-Specific Optimizations

**macOS (Apple Silicon)**:
- Metal GPU acceleration via Ollama
- Unified memory optimization
- Homebrew integration
- .app bundle distribution

**macOS (Intel)**:
- CPU-only processing with AVX optimizations
- Reduced model recommendations
- Same interface, different performance profile

**Linux**:
- NVIDIA CUDA acceleration detection and setup
- AMD ROCm support
- CPU fallback with OpenMP
- AppImage/Snap/Flatpak distribution

**Windows**:
- NVIDIA CUDA support
- DirectML acceleration (Intel/AMD GPUs)
- CPU processing with OpenMP
- MSI installer, Windows Store package

### Core Components (Cross-Platform)
- **Document Loaders**: PyMuPDF (PDF), python-docx (Word), markdown parsers
- **Text Chunking**: Semantic chunking with configurable overlap
- **Embeddings**: sentence-transformers (CPU) or platform-optimized alternatives
- **Vector Database**: ChromaDB with platform-specific storage paths
- **RAG Engine**: Hardware-adaptive retrieval pipeline
- **CLI Interface**: Rich CLI with platform-appropriate styling
- **Configuration**: YAML-based with platform-specific defaults

### Technology Stack (Platform-Agnostic)
- **Runtime**: Python 3.11+ (universal)
- **LLM Interface**: Ollama Python client, llama.cpp Python bindings
- **Document Processing**: PyMuPDF, python-docx, beautifulsoup4
- **Embeddings**: sentence-transformers, torch (with platform-specific acceleration)
- **Vector DB**: ChromaDB (cross-platform SQLite)
- **CLI Framework**: Click, Rich (cross-platform terminal UI)
- **Async**: asyncio for concurrent operations
- **Platform Detection**: psutil, platform modules
- **GPU Detection**: Platform-specific libraries (Metal/CUDA/ROCm/DirectML)

## Cross-Platform File Structure

## Testing & QA (short note)

Automated tests (unit, integration, and smoke) live in `tests/` and are run with `pytest`. The spec documents the repository layout; detailed TDD and test-first policies  are in `TESTING.md` for developer workflow.

```
doc-chat/
├── src/
│   ├── __init__.py
│   ├── cli.py                    # Main CLI interface
│   ├── platform_detector.py     # Hardware/platform detection
│   ├── hardware_profiles.py     # Hardware capability definitions
│   ├── model_selector.py        # Hardware-based model selection
│   ├── backends/                 # LLM backend implementations
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract backend interface
│   │   ├── ollama_backend.py    # Ollama implementation
│   │   ├── llamacpp_backend.py  # llama.cpp implementation
│   │   └── cloud_backend.py     # Future cloud API support
│   ├── platforms/               # Platform-specific optimizations
│   │   ├── __init__.py
│   │   ├── macos.py            # macOS optimizations
│   │   ├── linux.py            # Linux optimizations
│   │   └── windows.py          # Windows optimizations
│   ├── document_processor.py   # Cross-platform document loading
│   ├── embeddings.py          # Platform-adaptive embeddings
│   ├── vector_store.py        # ChromaDB interface
│   ├── rag_pipeline.py        # RAG orchestration
│   ├── installer.py           # Universal installer
│   └── utils.py               # Helper functions
├── config/
│   ├── default.yaml           # Base configuration
│   ├── macos.yaml            # macOS-specific settings
│   ├── linux.yaml            # Linux-specific settings
│   └── windows.yaml          # Windows-specific settings
├── data/
│   ├── documents/            # Uploaded documents (user data)
│   ├── vectordb/            # ChromaDB storage
│   ├── models/              # Downloaded model cache
│   └── cache/               # Embedding cache
├── installers/              # Platform-specific installers
│   ├── macos/              # .app bundle, Homebrew formula
│   ├── linux/              # AppImage, .deb, .rpm
│   └── windows/            # MSI, exe installer
├── requirements/            # Platform-specific dependencies
│   ├── base.txt           # Core dependencies
│   ├── macos.txt          # macOS-specific packages
│   ├── linux.txt          # Linux-specific packages
│   └── windows.txt        # Windows-specific packages
├── tests/
│   ├── test_platforms.py  # Platform detection tests
│   ├── test_backends.py   # Backend implementation tests
│   └── test_integration.py # Cross-platform integration tests
├── docs/
│   ├── installation/      # Platform-specific install guides
│   ├── hardware-guide.md  # Hardware recommendations
│   └── troubleshooting.md # Platform-specific troubleshooting
├── setup.py               # Universal Python package
├── pyproject.toml         # Modern Python packaging
└── README.md              # Cross-platform documentation
```

## Cross-Platform Installation & Usage

### Hardware Requirements

**Minimum Requirements**:
- 8GB RAM, 10GB storage
- Any 64-bit CPU (x86_64 or ARM64)
- Python 3.11+

**Recommended by Platform**:

**macOS**:
- Apple Silicon (M1/M2/M3/M4): 16GB+ unified memory
- Intel Mac: 16GB RAM, dedicated GPU helpful

**Linux**:
- NVIDIA GPU: RTX 3060+ (8GB VRAM), 16GB system RAM
- AMD GPU: RX 6600+ with ROCm, 16GB system RAM  
- CPU-only: 32GB+ RAM, modern CPU (Ryzen 5/Intel i5+)

**Windows**:
- NVIDIA GPU: RTX 3060+ (8GB VRAM), 16GB system RAM
- Intel/AMD GPU: 16GB+ RAM, DirectML support
- CPU-only: 32GB+ RAM, modern CPU

### Universal Setup

**One-Line Install (All Platforms)**:
```bash
curl -fsSL https://install.doc-chat.com | bash
```

**Or Manual Install**:
```bash
# Install Python package
pip install doc-chat

# Auto-detect hardware and setup optimal configuration
doc-chat --setup
```

**Platform-Specific Installation**:

**macOS**:
```bash
# Homebrew (recommended)
brew install doc-chat

# Or download .app bundle
# Download from GitHub releases, drag to Applications
```

**Linux**:
```bash
# AppImage (universal)
wget https://github.com/your-repo/doc-chat/releases/latest/download/doc-chat.AppImage
chmod +x doc-chat.AppImage
./doc-chat.AppImage

# Or package manager
sudo snap install doc-chat         # Snap
flatpak install doc-chat          # Flatpak
sudo apt install doc-chat         # Ubuntu/Debian (future)
```

**Windows**:
```bash
# Windows installer
# Download .msi from GitHub releases

# Or package manager
winget install doc-chat           # Winget
choco install doc-chat           # Chocolatey
```

### Quick Start (Universal)
```bash
# First time setup (detects hardware, downloads optimal model)
doc-chat --setup

# Add documents to knowledge base
doc-chat --add research.pdf notes.md report.docx

# Start interactive chat
doc-chat --start

# Check what your hardware can run
doc-chat --hardware

# One-shot query
doc-chat --query "What are the main findings in the research?"
```

### Platform-Specific Performance Expectations

**macOS Apple Silicon (M4)**:
- Memory Usage: 12-15GB during operation
- Storage: ~8GB for models + documents
- Performance: 20-35 tokens/second
- Models: Llama 3.1 70B (32GB+), 8B, Mistral 7B, Phi-3

**Linux NVIDIA RTX 4090**:
- Memory Usage: 16GB system + 24GB VRAM
- Storage: ~10GB for models + documents  
- Performance: 30-50 tokens/second
- Models: Llama 3.1 70B, 8B, Mistral 7B, specialized models

**Linux/Windows CPU-only**:
- Memory Usage: 20-32GB system RAM
- Storage: ~6GB for models + documents
- Performance: 3-8 tokens/second
- Models: Phi-3 3.8B, Mistral 7B (quantized), Llama 8B (Q4)

**Windows DirectML (Intel/AMD GPU)**:
- Memory Usage: 16GB system + shared GPU memory
- Storage: ~8GB for models + documents
- Performance: 8-15 tokens/second
- Models: Phi-3 14B, Mistral 7B, Llama 8B
