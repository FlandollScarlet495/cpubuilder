import pytest
from cpubuilder import BinaryHelper, MemoryHelper, DebugTools

def test_binary_helper():
    # to_bytes のテスト
    assert BinaryHelper.to_bytes(0xFF, 2, 'little') == b'\xFF\x00'
    
    # from_bytes のテスト
    assert BinaryHelper.from_bytes(b'\xFF\x00', 'little') == 255
    
    # ビット操作のテスト
    value = 0b11110000
    assert BinaryHelper.extract_bits(value, 4, 4) == 0b1111
    
    new_value = BinaryHelper.set_bits(0, 0b1111, 4, 4)
    assert new_value == 0b11110000

def test_memory_helper():
    memory = MemoryHelper(256)
    
    # 書き込みと読み取りのテスト
    memory.write(0, 0xFF)
    assert memory.read(0) == 0xFF
    
    # 範囲外アクセスのテスト
    with pytest.raises(ValueError):
        memory.write(256, 0)
    
    with pytest.raises(ValueError):
        memory.read(256)
    
    # メモリダンプのテスト
    memory.write(0, bytes([1, 2, 3, 4]))
    dump = memory.dump(0, 4)
    assert dump == bytes([1, 2, 3, 4])

def test_debug_tools():
    debug = DebugTools()
    
    # ブレークポイントのテスト
    debug.add_breakpoint(0x1000)
    assert debug.check_breakpoint(0x1000) == True
    assert debug.check_breakpoint(0x2000) == False
    
    # ウォッチのテスト
    value = 0
    debug.add_watch("test", lambda: value)
    watch_results = debug.check_watches()
    assert watch_results["test"] == 0
    
    # トレースのテスト
    debug.start_trace()
    debug.add_trace({"pc": 0, "instruction": "NOP"})
    assert len(debug.traces) == 1
    assert debug.traces[0]["state"]["instruction"] == "NOP"