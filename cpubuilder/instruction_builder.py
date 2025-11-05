from typing import Callable, Dict, Any, Optional
from functools import wraps
import inspect

class InstructionBase:
    def __init__(self):
        self.instructions: Dict[str, Dict[str, Any]] = {}
        self._register_decorated_methods()

    def _register_decorated_methods(self):
        """デコレートされたメソッドを登録"""
        for name, method in inspect.getmembers(self):
            if hasattr(method, '_instruction_info'):
                self.instructions[name] = method._instruction_info

def instruction(opcode: int, cycles: int = 1, description: str = ""):
    """命令を定義するデコレータ"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        
        # 命令の情報を保存
        wrapper._instruction_info = {
            'opcode': opcode,
            'cycles': cycles,
            'description': description,
            'parameters': inspect.signature(func).parameters
        }
        return wrapper
    return decorator

class InstructionSetBuilder:
    """命令セットを構築するためのビルダー"""
    def __init__(self):
        self.instructions: Dict[str, Dict[str, Any]] = {}
        self.current_opcode = 0

    def add_instruction(self, name: str, handler: Callable,
                       cycles: int = 1, description: str = "",
                       opcode: Optional[int] = None) -> 'InstructionSetBuilder':
        """新しい命令を追加"""
        if opcode is None:
            opcode = self.current_opcode
            self.current_opcode += 1

        self.instructions[name] = {
            'handler': handler,
            'opcode': opcode,
            'cycles': cycles,
            'description': description
        }
        return self

    def build(self) -> Dict[str, Dict[str, Any]]:
        """命令セットを構築"""
        return self.instructions.copy()

# 使用例：
class ExampleInstructionSet(InstructionBase):
    @instruction(opcode=0x00, cycles=1, description="No operation")
    def nop(self):
        pass

    @instruction(opcode=0x01, cycles=2, description="Move value between registers")
    def mov(self, dest: int, src: int):
        pass