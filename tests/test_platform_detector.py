import pytest
from unittest.mock import patch, MagicMock
from src.platform_detector import detect


mock_psutil_basic = MagicMock()
mock_psutil_basic.cpu_count.side_effect = [4, 8]
mock_psutil_basic.virtual_memory.return_value.total = 16 * 1024**3
mock_gpu = MagicMock()
mock_gpu.name = "NVIDIA GTX 1080"
mock_psutil_basic.gpus.return_value = [mock_gpu]

@patch.dict('sys.modules', {'psutil': mock_psutil_basic})
@patch('src.platform_detector.platform')
def test_detect_basic_info(mock_platform):
    # Mock platform info
    mock_platform.system.return_value = "Linux"
    mock_platform.machine.return_value = "x86_64"
    mock_platform.python_version.return_value = "3.9.0"
    
    result = detect()
    
    assert result["system"] == "Linux"
    assert result["machine"] == "x86_64"
    assert result["python_version"] == "3.9.0"
    assert result["cpu_count_physical"] == 4
    assert result["cpu_count_logical"] == 8
    assert result["total_memory_bytes"] == 16 * 1024**3
    assert result["GPU info"] == ["NVIDIA GTX 1080"]
    assert result["is_mac_with_m4"] is False  # Not Darwin


@patch.dict('sys.modules', {'psutil': None})
@patch('src.platform_detector.platform')
def test_detect_without_psutil(mock_platform):
    mock_platform.system.return_value = "Windows"
    mock_platform.machine.return_value = "AMD64"
    mock_platform.python_version.return_value = "3.10.0"
    
    result = detect()
    
    assert result["system"] == "Windows"
    assert result["cpu_count_physical"] is None
    assert result["cpu_count_logical"] is None
    assert result["total_memory_bytes"] is None
    assert result["GPU info"] is None


mock_psutil_mac = MagicMock()
mock_psutil_mac.cpu_count.side_effect = [10, 10]
mock_psutil_mac.virtual_memory.return_value.total = 32 * 1024**3
mock_psutil_mac.gpus.return_value = []

@patch.dict('sys.modules', {'psutil': mock_psutil_mac})
@patch('src.platform_detector.subprocess')
@patch('src.platform_detector.platform')
def test_detect_mac_with_m4(mock_platform, mock_subprocess):
    mock_platform.system.return_value = "Darwin"
    mock_platform.machine.return_value = "arm64"
    mock_platform.python_version.return_value = "3.11.0"
    
    # Mock subprocess for M4 detection
    mock_subprocess.run.return_value.stdout = "Apple M4"
    
    result = detect()
    
    assert result["system"] == "Darwin"
    assert result["is_mac_with_m4"] is True


@patch.dict('sys.modules', {'psutil': mock_psutil_mac})
@patch('src.platform_detector.subprocess')
@patch('src.platform_detector.platform')
def test_detect_mac_without_m4_subprocess_failure(mock_platform, mock_subprocess):
    mock_platform.system.return_value = "Darwin"
    mock_platform.machine.return_value = "arm64"
    mock_platform.python_version.return_value = "3.11.0"
    
    # Mock subprocess failure
    mock_subprocess.run.side_effect = Exception("Command failed")
    
    result = detect()
    
    assert result["is_mac_with_m4"] is None


@patch.dict('sys.modules', {'psutil': MagicMock()})
@patch('src.platform_detector.platform')
def test_detect_non_darwin_no_m4_check(mock_platform):
    mock_platform.system.return_value = "Linux"
    
    result = detect()
    
    assert result["is_mac_with_m4"] is False
