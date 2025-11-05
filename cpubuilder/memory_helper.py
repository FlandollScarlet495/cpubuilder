from typing import Optional, Union, List
from .binary_helper import BinaryHelper

class MemoryHelper:
    def __init__(self, size: int = 65536):
        """メモリヘルパーの初期化"""
        self.size = size
        self.memory = bytearray(size)
        self.watches: List[tuple] = []  # (address, callback)のリスト

    def read(self, address: int, size: int = 1) -> Union[int, bytes]:
        """メモリから読み取り"""
        if not (0 <= address < self.size):
            raise ValueError(f"Invalid memory address: {address}")
        
        if size == 1:
            return self.memory[address]
        return bytes(self.memory[address:address + size])

    def write(self, address: int, value: Union[int, bytes], size: Optional[int] = None):
        """メモリに書き込み"""
        if isinstance(value, int):
            if size is None:
                size = 1
            value = BinaryHelper.to_bytes(value, size, 'little')
        
        if not (0 <= address < self.size) or address + len(value) > self.size:
            raise ValueError(f"Invalid memory range: {address} to {address + len(value)}")
        
        # ウォッチポイントのチェック
        for watch_addr, callback in self.watches:
            if address <= watch_addr < address + len(value):
                callback(watch_addr, value[watch_addr - address])
        
        self.memory[address:address + len(value)] = value

    def add_watch(self, address: int, callback) -> None:
        """メモリウォッチポイントを追加"""
        if not (0 <= address < self.size):
            raise ValueError(f"Invalid memory address: {address}")
        self.watches.append((address, callback))

    def remove_watch(self, address: int) -> None:
        """メモリウォッチポイントを削除"""
        self.watches = [(addr, cb) for addr, cb in self.watches if addr != address]

    def dump(self, start: int, size: int) -> bytes:
        """メモリ範囲をダンプ"""
        if not (0 <= start < self.size) or start + size > self.size:
            raise ValueError(f"Invalid memory range: {start} to {start + size}")
        return bytes(self.memory[start:start + size])

    def fill(self, start: int, size: int, value: int) -> None:
        """メモリ範囲を特定の値で埋める"""
        if not (0 <= start < self.size) or start + size > self.size:
            raise ValueError(f"Invalid memory range: {start} to {start + size}")
        self.memory[start:start + size] = [value] * size

    def copy(self, src: int, dest: int, size: int) -> None:
        """メモリ範囲をコピー"""
        if not (0 <= src < self.size and 0 <= dest < self.size):
            raise ValueError("Invalid source or destination address")
        if src + size > self.size or dest + size > self.size:
            raise ValueError("Copy operation exceeds memory bounds")
        self.memory[dest:dest + size] = self.memory[src:src + size]