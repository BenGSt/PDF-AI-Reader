"""Simple platform/hardware detector used by the MVP scaffolding."""
import platform
import subprocess


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
        info["GPU info"] = [gpu.name for gpu in psutil.gpus()] if hasattr(psutil, "gpus") else None
    except Exception:
        # psutil is optional for the scaffold
        info["cpu_count_physical"] = None
        info["cpu_count_logical"] = None
        info["total_memory_bytes"] = None
        info["GPU info"] = None

    # Add detection for Mac with M4
    if info["system"] == "Darwin":
        try:
            result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True)
            cpu_brand = result.stdout.strip()
            info["is_mac_with_m4"] = "Apple M4" in cpu_brand
        except Exception:
            info["is_mac_with_m4"] = None
    else:
        info["is_mac_with_m4"] = False

    return info

if __name__ == "__main__":
    print()  # blank line for readability in CLI
    print(detect())
