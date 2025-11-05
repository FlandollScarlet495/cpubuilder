from cpubuilder import (
    InstructionBase,
    instruction,
    MemoryHelper,
    DebugTools,
    CPUStateFormatter,
    BinaryHelper
)

# 命令セットの定義例
class MyInstructionSet(InstructionBase):
    def __init__(self):
        super().__init__()
        self.registers = [0] * 8
        self.memory = MemoryHelper(65536)
        self.pc = 0
        self.debug = DebugTools()

    @instruction(opcode=0x00, cycles=1, description="No operation")
    def nop(self):
        self.pc += 1

    @instruction(opcode=0x10, cycles=2, description="Load immediate value to register")
    def load_immediate(self, reg: int, value: int):
        self.registers[reg] = value
        self.pc += 3

    @instruction(opcode=0x20, cycles=3, description="Add registers")
    def add(self, dest: int, src: int):
        self.registers[dest] += self.registers[src]
        self.pc += 3

def main():
    # CPUの作成
    cpu = MyInstructionSet()
    
    # デバッグツールのセットアップ
    cpu.debug.add_watch("R0", lambda: cpu.registers[0])
    cpu.debug.add_watch("R1", lambda: cpu.registers[1])
    cpu.debug.start_trace()
    
    # プログラムの作成と実行
    program = [
        0x10, 0x00, 0x05,  # LOAD R0, 5
        0x10, 0x01, 0x03,  # LOAD R1, 3
        0x20, 0x00, 0x01,  # ADD R0, R1
    ]
    
    # プログラムをメモリにロード
    cpu.memory.write(0, bytes(program))
    
    # プログラムの実行
    while cpu.pc < len(program):
        opcode = cpu.memory.read(cpu.pc)
        instruction_name = None
        
        # 命令を探して実行
        for name, info in cpu.instructions.items():
            if info['opcode'] == opcode:
                instruction_name = name
                method = getattr(cpu, name)
                if 'parameters' in info:
                    params = []
                    for i in range(1, len(info['parameters'])):
                        params.append(cpu.memory.read(cpu.pc + i))
                    method(*params)
                else:
                    method()
                break
        
        # デバッグ情報の記録
        cpu.debug.add_trace({
            'pc': cpu.pc,
            'instruction': instruction_name,
            'registers': cpu.registers.copy()
        })
    
    # 結果の表示
    print("実行結果:")
    print(f"R0: {cpu.registers[0]}")  # 8が表示されるはず
    print(f"R1: {cpu.registers[1]}")  # 3が表示されるはず
    
    # ウォッチの結果を表示
    watch_results = cpu.debug.check_watches()
    print("\nウォッチの結果:")
    for name, value in watch_results.items():
        print(f"{name}: {value}")
    
    # トレースを保存
    cpu.debug.save_trace("execution_trace.json")

if __name__ == "__main__":
    main()