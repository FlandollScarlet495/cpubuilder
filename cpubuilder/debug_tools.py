from typing import Any, Dict, List, Optional, Callable
import time
import json

class DebugTools:
    def __init__(self):
        self.breakpoints: Dict[int, bool] = {}
        self.traces: List[Dict[str, Any]] = []
        self.watches: Dict[str, Callable] = {}
        self.step_count = 0
        self.start_time = None

    def add_breakpoint(self, address: int) -> None:
        """ブレークポイントを追加"""
        self.breakpoints[address] = True

    def remove_breakpoint(self, address: int) -> None:
        """ブレークポイントを削除"""
        self.breakpoints.pop(address, None)

    def check_breakpoint(self, address: int) -> bool:
        """ブレークポイントをチェック"""
        return self.breakpoints.get(address, False)

    def add_watch(self, name: str, callback: Callable) -> None:
        """ウォッチ式を追加"""
        self.watches[name] = callback

    def remove_watch(self, name: str) -> None:
        """ウォッチ式を削除"""
        self.watches.pop(name, None)

    def start_trace(self) -> None:
        """トレース記録を開始"""
        self.traces.clear()
        self.step_count = 0
        self.start_time = time.time()

    def add_trace(self, state: Dict[str, Any]) -> None:
        """状態をトレースに追加"""
        if self.start_time is not None:
            self.step_count += 1
            trace_entry = {
                'step': self.step_count,
                'time': time.time() - self.start_time,
                'state': state
            }
            self.traces.append(trace_entry)

    def stop_trace(self) -> None:
        """トレース記録を停止"""
        self.start_time = None

    def save_trace(self, filename: str) -> None:
        """トレースをJSONファイルとして保存"""
        with open(filename, 'w') as f:
            json.dump(self.traces, f, indent=2)

    def check_watches(self) -> Dict[str, Any]:
        """全てのウォッチ式を評価"""
        results = {}
        for name, callback in self.watches.items():
            try:
                results[name] = callback()
            except Exception as e:
                results[name] = f"Error: {str(e)}"
        return results

class CPUStateFormatter:
    @staticmethod
    def format_registers(registers: Dict[str, Any]) -> str:
        """レジスタの状態をフォーマット"""
        output = []
        for name, value in registers.items():
            if isinstance(value, int):
                output.append(f"{name}: 0x{value:04X} ({value})")
            else:
                output.append(f"{name}: {value}")
        return "\n".join(output)

    @staticmethod
    def format_memory_dump(memory: bytes, start_addr: int,
                          bytes_per_line: int = 16) -> str:
        """メモリダンプをフォーマット"""
        lines = []
        for i in range(0, len(memory), bytes_per_line):
            chunk = memory[i:i + bytes_per_line]
            hex_values = " ".join(f"{b:02X}" for b in chunk)
            ascii_values = "".join(chr(b) if 32 <= b <= 126 else "."
                                for b in chunk)
            addr = start_addr + i
            lines.append(f"{addr:04X}: {hex_values:<{bytes_per_line*3}} {ascii_values}")
        return "\n".join(lines)

    @staticmethod
    def format_instruction(instruction: Dict[str, Any]) -> str:
        """命令をフォーマット"""
        return (f"{instruction.get('name', 'Unknown')} "
                f"{' '.join(str(op) for op in instruction.get('operands', []))}")