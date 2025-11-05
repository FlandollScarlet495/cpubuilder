from typing import Union, List, Dict, Any
import struct

class BinaryHelper:
    @staticmethod
    def to_bytes(value: int, size: int, endian: str = 'little') -> bytes:
        """整数値をバイト列に変換"""
        return value.to_bytes(size, endian)

    @staticmethod
    def from_bytes(data: bytes, endian: str = 'little') -> int:
        """バイト列を整数値に変換"""
        return int.from_bytes(data, endian)

    @staticmethod
    def pack_struct(format_str: str, *values: Any) -> bytes:
        """構造体としてパック"""
        return struct.pack(format_str, *values)

    @staticmethod
    def unpack_struct(format_str: str, data: bytes) -> tuple:
        """構造体としてアンパック"""
        return struct.unpack(format_str, data)

    @staticmethod
    def create_bit_mask(start_bit: int, length: int) -> int:
        """ビットマスクを作成"""
        mask = ((1 << length) - 1) << start_bit
        return mask

    @staticmethod
    def extract_bits(value: int, start_bit: int, length: int) -> int:
        """特定のビット範囲を抽出"""
        mask = BinaryHelper.create_bit_mask(start_bit, length)
        return (value & mask) >> start_bit

    @staticmethod
    def set_bits(value: int, new_bits: int, start_bit: int, length: int) -> int:
        """特定のビット範囲を設定"""
        mask = BinaryHelper.create_bit_mask(start_bit, length)
        return (value & ~mask) | ((new_bits << start_bit) & mask)