"""Simple platform/hardware detector used by the MVP scaffolding."""
import platform


def detect():
    info = {
        "system": platform.system(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
    }
    try:
        import psutil

        info["cpu_count_physical"] = psutil.cpu_count(logical=False)
        info["cpu_count_logical"] = psutil.cpu_count(logical=True)
        info["total_memory_bytes"] = psutil.virtual_memory().total
    except Exception:
        # psutil is optional for the scaffold
        info["cpu_count_physical"] = None
        info["cpu_count_logical"] = None
        info["total_memory_bytes"] = None

    return info
