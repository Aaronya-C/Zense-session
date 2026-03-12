TEXT_BASE = 0x00400000
DATA_BASE = 0x10010000


R_TYPE_OPCODE = {

    "add":  {"opcode":"000000","funct":"100000",
             "RegDst":1,"ALUSrc":0,"MemtoReg":0,
             "RegWrite":1,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"10"},

    "sub":  {"opcode":"000000","funct":"100010",
             "RegDst":1,"ALUSrc":0,"MemtoReg":0,
             "RegWrite":1,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"10"},

    "and":  {"opcode":"000000","funct":"100100",
             "RegDst":1,"ALUSrc":0,"MemtoReg":0,
             "RegWrite":1,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"10"},

    "or":   {"opcode":"000000","funct":"100101",
             "RegDst":1,"ALUSrc":0,"MemtoReg":0,
             "RegWrite":1,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"10"},

    "slt":  {"opcode":"000000","funct":"101010",
             "RegDst":1,"ALUSrc":0,"MemtoReg":0,
             "RegWrite":1,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"10"},

    "sll":  {"opcode":"000000","funct":"000000",
             "RegDst":1,"ALUSrc":0,"MemtoReg":0,
             "RegWrite":1,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"10"},

    "srl":  {"opcode":"000000","funct":"000010",
             "RegDst":1,"ALUSrc":0,"MemtoReg":0,
             "RegWrite":1,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"10"},
    
    "syscall": {"opcode":"000000","funct":"001100",
            "RegDst":None,"ALUSrc":None,"MemtoReg":None,
            "RegWrite":0,"MemRead":0,"MemWrite":0,
            "Branch":0,"Jump":0,"ALUOp":None}

}


OPCODE_FUNCT = {
    "addi": {"opcode":"001000","funct":None,
             "RegDst":0,"ALUSrc":1,"MemtoReg":0,
             "RegWrite":1,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"00"},

    "ori":  {"opcode":"001101","funct":None,
             "RegDst":0,"ALUSrc":1,"MemtoReg":0,
             "RegWrite":1,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"11"},
    
    "lui": {"opcode":"001111","funct":None,
        "RegDst":0,"ALUSrc":1,"MemtoReg":0,
        "RegWrite":1,"MemRead":0,"MemWrite":0,
        "Branch":0,"Jump":0,"ALUOp":"LUI"},


    "lw":   {"opcode":"100011","funct":None,
             "RegDst":0,"ALUSrc":1,"MemtoReg":1,
             "RegWrite":1,"MemRead":1,"MemWrite":0,
             "Branch":0,"Jump":0,"ALUOp":"00"},

    "sw":   {"opcode":"101011","funct":None,
             "RegDst":None,"ALUSrc":1,"MemtoReg":None,
             "RegWrite":0,"MemRead":0,"MemWrite":1,
             "Branch":0,"Jump":0,"ALUOp":"00"},


    "beq":  {"opcode":"000100","funct":None,
             "RegDst":None,"ALUSrc":0,"MemtoReg":None,
             "RegWrite":0,"MemRead":0,"MemWrite":0,
             "Branch":1,"Jump":0,"ALUOp":"01"},

    "bne":  {"opcode":"000101","funct":None,
             "RegDst":None,"ALUSrc":0,"MemtoReg":None,
             "RegWrite":0,"MemRead":0,"MemWrite":0,
             "Branch":1,"Jump":0,"ALUOp":"01"},


    "j":    {"opcode":"000010","funct":None,
             "RegDst":None,"ALUSrc":None,"MemtoReg":None,
             "RegWrite":0,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":1,"ALUOp":None}
}


 



class Register:
    def __init__(self):
        self.t = [0] * 10
        self.s = [0] * 8
        self.a = [0] * 4   

        self.pc = TEXT_BASE

        self.zero = 0
        self.at = 0
        self.ra = 0
        self.v0 = 0
        self.v1 = 0



class Memory:
    
    def __init__(self, file_instr,file_data):
        self.data_memory = file_data
        self.instr_memory = file_instr
                

    def read_data(self, addr):
        with open(self.data_memory, "r") as f:
            for i, line in enumerate(f):
                if i == addr:
                    return line.strip()
        return ""


    def read_instr(self, addr):
        with open(self.instr_memory, "r") as f:
            for i, line in enumerate(f):
                if i == addr:
                    return line.strip()
        return ""

    def write_data(self, addr, value):
        value &= ((1 << 32) - 1)

        with open(self.data_memory, "r") as f:
            lines = f.readlines()

        while len(lines) <= addr:
            lines.append("0".zfill(32) + "\n")

        lines[addr] = format(value, "032b") + "\n"

        with open(self.data_memory, "w") as f:
            f.writelines(lines)


    def write_instr(self, addr, value):
        value &= ((1 << 32) - 1)

        with open(self.instr_memory, "r") as f:
            lines = f.readlines()

        while len(lines) <= addr:
            lines.append("0".zfill(32) + "\n")

        lines[addr] = format(value, "032b") + "\n"

        with open(self.instr_memory, "w") as f:
            f.writelines(lines)



class CPU:
    def __init__(self,instr_file,data_file):
        self.mem = Memory(instr_file,data_file)
        self.reg = Register()
        self.running = True
        self.instr=""
        self.data=""
        self.opcode =""
        self.rs=""
        self.rt=""
        self.rd=""
        self.shamt=""
        self.func = ""
        self.imme = 0
        self.jaddr = 0
        self.ctrl = None
        self.current_instr = ""
        self.alu_result = 0
        self.mem_data = 0
        self.cycle=0

        
    def print_reg(self):
        print("\n==============================")
        print(f"Cycle: {self.cycle}")
        print(f"PC: {hex(self.reg.pc)}")

        print("Registers:")

        print("---- $a registers ----")
        for i in range(4):
            if self.reg.a[i]!=0:
                print(f"$a{i} = {self.reg.a[i]}")

        print("---- $t registers ----")
        for i in range(10):
            if self.reg.t[i]!=0:
                print(f"$t{i} = {self.reg.t[i]}")

        print("---- $s registers ----")
        for i in range(8):
            if self.reg.s[i]!=0:
                print(f"$s{i} = {self.reg.s[i]}")

        print("==============================\n")

    def IF_stage(self):
        self.instr = self.mem.read_instr((self.reg.pc-TEXT_BASE) // 4)
        if not self.instr: # Stop if no more instructions
            self.running = False
            return
        self.reg.pc += 4


    def ID_stage(self):
        self.ctrl = None
        self.current_instr = None

        self.opcode = self.instr[0:6]
        self.rs = int(self.instr[6:11],2)
        self.rt = int(self.instr[11:16],2)
        
        if self.opcode == "000000":
            self.rd = int(self.instr[16:21],2)
            self.shamt = int(self.instr[21:26],2)
            self.func = self.instr[26:32]
            
            
            for name,signals in R_TYPE_OPCODE.items():
                if signals["funct"] == self.func:
                    self.ctrl = signals.copy()
                    self.current_instr = name
                    break


        elif self.opcode in ["000010"] :
            self.jaddr = int(self.instr[6:32],2)
            self.current_instr = "j"

            self.ctrl = {"opcode":"000010","funct":None,
             "RegDst":None,"ALUSrc":None,"MemtoReg":None,
             "RegWrite":0,"MemRead":0,"MemWrite":0,
             "Branch":0,"Jump":1,"ALUOp":None}

        else:
            self.rd = None
            raw_imm = int(self.instr[16:32], 2)
            if raw_imm & 0x8000:
                self.imme = raw_imm - 0x10000
            else:
                self.imme = raw_imm

            for name, signals in OPCODE_FUNCT.items():
                if signals["opcode"] == self.opcode:
                    self.ctrl = signals.copy()
                    self.current_instr = name
                    break
        
        if self.ctrl is None:
            print("ERROR: Unknown instruction")
            print("Opcode:", self.opcode)
            self.running = False


    def get_register_val(self, register_idx):
        if register_idx == 0: return 0  # $zero
        if register_idx == 1: return self.reg.at
        if register_idx == 2: return self.reg.v0
        if register_idx == 3: return self.reg.v1
        if 4 <= register_idx <= 7: return self.reg.a[register_idx - 4]
        if 8 <= register_idx <= 15: return self.reg.t[register_idx - 8]
        if 16 <= register_idx <= 23: return self.reg.s[register_idx - 16]
        if 24 <= register_idx <= 25: return self.reg.t[register_idx - 16] # t8-t9
        if register_idx == 31: return self.reg.ra
        return 0

    def EX_stage(self):


        # 1. Fetch Operands
        val_at_rs = self.get_register_val(self.rs)
        val_at_rt = self.get_register_val(self.rt)

        # 2. ALU Mux: Choose between Register (0) or Immediate (1)
        operand_b = val_at_rt  # default

        if self.ctrl and self.ctrl["ALUSrc"] is not None:
            operand_b = val_at_rt if self.ctrl["ALUSrc"] == 0 else self.imme


        # 3. ALU Operations
        if self.current_instr == "add":
            self.alu_result = val_at_rs + operand_b
            
        elif self.current_instr == "sub":
            self.alu_result = val_at_rs - operand_b

        elif self.current_instr == "and":
            self.alu_result = val_at_rs & operand_b

        elif self.current_instr == "or":
            self.alu_result = val_at_rs | operand_b

        elif self.current_instr == "sll":
            # Shift rt, not rs
            self.alu_result = val_at_rt << self.shamt

        elif self.current_instr == "srl":
            # Shift rt, not rs
            self.alu_result = val_at_rt >> self.shamt
            
        elif self.current_instr == "slt":
            self.alu_result = 1 if val_at_rs < operand_b else 0

        elif self.current_instr == "addi":
            self.alu_result = val_at_rs + operand_b

        elif self.current_instr == "ori":
            self.alu_result = val_at_rs | operand_b
        
        elif self.current_instr == "lui":
            self.alu_result = self.imme << 16

        # 4. Memory Address Calculation (Base + Offset)
        elif self.current_instr in ["lw", "sw"]:
            self.alu_result = val_at_rs + self.imme

        # 5. Branch Operations
        # Target = PC + (Offset * 4). Note: PC was already +4 in IF_stage.
        elif self.current_instr == "beq":
            if val_at_rs == val_at_rt:
                self.reg.pc += (self.imme * 4)

        elif self.current_instr == "bne":
            if val_at_rs != val_at_rt:
                self.reg.pc += (self.imme * 4)


        elif self.current_instr == "j":
            pc_upper = (self.reg.pc & 0xF0000000)
            pc_upper = (self.reg.pc & 0xF0000000)
            self.reg.pc = pc_upper | (self.jaddr * 4)
    # Concatenate PC upper bits with jaddr shifted left by 2
    
        elif self.current_instr == "syscall":
            if self.reg.v0 == 10:
                self.running = False



    def MEM_stage(self):
        
        if not self.ctrl:
            return

        if self.ctrl["MemRead"] == 1 or self.ctrl["MemWrite"] == 1:
            print("ALU_RESULT:", hex(self.alu_result))
            address = (self.alu_result - DATA_BASE)//4

        if self.ctrl["MemRead"] == 1:
            raw_data = self.mem.read_data(address)
            if raw_data:
                val = int(raw_data, 2)
                # Check if the sign bit (bit 31) is 1
                self.mem_data = val - 0x100000000 if val & 0x80000000 else val
            else:
                self.mem_data = 0

        if self.ctrl["MemWrite"] == 1:
            val_at_rt = self.get_register_val(self.rt)

            self.mem.write_data(address,val_at_rt)


    def WB_stage(self):
        if not self.ctrl:
            return
        if self.ctrl["RegWrite"] == 0:
            return
        
        write_value = self.mem_data if self.ctrl["MemtoReg"] == 1 else self.alu_result
        dest_reg = self.rd if self.ctrl["RegDst"] == 1 else self.rt
        
        if dest_reg == 0: return
        
        # Mapping logic (must match get_register_val)
        if dest_reg == 2: self.reg.v0 = write_value
        elif dest_reg == 1: self.reg.at = write_value
        elif dest_reg == 3: self.reg.v1 = write_value
        elif 4 <= dest_reg <= 7:
            self.reg.a[dest_reg - 4] = write_value
        elif 8 <= dest_reg <= 15: self.reg.t[dest_reg - 8] = write_value
        elif 16 <= dest_reg <= 23: self.reg.s[dest_reg - 16] = write_value
        elif 24 <= dest_reg <= 25: self.reg.t[dest_reg - 16] = write_value
        elif dest_reg == 31: self.reg.ra = write_value


    def run(self):
        while self.running:
            self.cycle +=1
            
            
            self.IF_stage()
            if not self.running: break
            self.ID_stage()
            self.EX_stage()
            self.MEM_stage()
            self.WB_stage()
            
            if self.cycle % 10 == 0:
                self.print_reg()



def get_files():
    file_instr = input("Enter instruction filename: ")
    file_data = input("Enter data filename: ")
    return (file_instr,file_data)
    
file_list=get_files()
file_instr=file_list[0]
file_data=file_list[1]
 
 
cpu=CPU(file_instr,file_data)
cpu.run()
