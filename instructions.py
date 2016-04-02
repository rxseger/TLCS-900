# Constants
BYTE = 0
WORD = 1
LWORD = 2

# Class to hold registers
class Reg(object):
    def __init__(self, ext, size, reg):
        self.ext = ext
        self.size = size
        self.reg = reg
    
    def __str__(self):
        return regname(self)

# Class to hold registers used by MUL, DIV
# Wraps a normal register with a different __str__ method
class RReg(Reg):
    def __init__(self, reg):
        super(RReg, self).__init__(reg.ext, reg.size, reg.reg)
    
    def __str__(self):
        return rregname(self)

# 1) Load Instructions

#LD
def LD_R_r(insn): 
    return "LD", popR(insn, '?', insn.lastsize), insn.lastr
def LD_r_R(insn):
    return "LD", insn.lastr, popR(insn, '?', insn.lastsize)
    
def LD_r_3X(n): 
    def LD_N(insn):
        insn.pop()
        return "LD", insn.lastr, n
    return LD_N

def LD_R_n(insn):
    return "LD", popR(insn, 'zzz'), insn.pop()
def LD_RR_nn(insn):
    return "LD", popR(insn, 'zzz'), insn.popw()
def LD_XRR_nnnn(insn): 
    return "LD", popR(insn, 'zzz'), insn.popl()

def LD_r_X(insn): return
def LD_R_mem(insn): return
def LD_n_n(insn): return
def LD_nn_m(insn): return
def LDB_mem_R(insn): return
def LDW_mem_R(insn): return
def LDL_mem_R(insn): return
def LDB_m_X(insn): return
def LDW_m_X(insn): return

def LDW_n_nn(insn):
    insn.pop()
    return "LDW", wrap(insn.pop()), insn.popw()

def LDB_m_nn(insn): return
def LDW_m_nn(insn): return

#PUSH
def PUSH_F(insn): return
def PUSH_A(insn): return

def PUSH_RR(insn): 
    return "PUSH", popR(insn, 's')

def PUSH_r(insn): return
def PUSH_n(insn): return
def PUSHW_nn(insn): return
def PUSH_mem(insn): return

#POP
def POP_F(insn): return
def POP_A(insn): return
def POP_RR(insn): 
    return "POP", popR(insn, '?', WORD)

def POP_XRR(insn): 
    return "POP", popR(insn, '?', LWORD)

def POP_r(insn): return
def POPB_mem(insn): return
def POPW_mem(insn): return

#LDA
def LDAW_R_mem(insn): 
    return "LDA", popR(insn, '?', WORD), insn.lastmem
def LDAL_R_mem(insn):
    return "LDA", popR(insn, '?', LWORD), insn.lastmem
    
#LDAR
def LDAR(insn): return

# 2) Exchange

# EX
def EX_F_F1(insn): return
def EX_R_r(insn): 
    return "EX", popR(insn, '?', insn.lastsize), insn.lastr
def EX_mem_R(insn): return

#MIRR
def MIRR(insn): return

# 3) Load Increment/Decrement & Compare Increment/Decrement Size

#LDXX
def LDI(insn): return
def LDIR(insn): return
def LDD(insn): return
def LDDR(insn): return

#CPXX
def CPI(insn): 
    insn.pop()
    return "CPI", ("A" if insn.lastsize == WORD else "WA"), "(" + regname(insn.lastr) + "+)"
    
def CPIR(insn): return
def CPD(insn): return
def CPDR(insn): return

# 4) Arithmetic Operations

#ADD
def ADD_R_r(insn): 
    return "ADD", popR(insn, '?', insn.lastsize), insn.lastr

def ADD_r_X(insn):
    insn.pop()
    return "ADD", insn.lastr, insn.popn(insn.lastsize)

def ADD_R_mem(insn): 
    return "ADD", popR(insn, '?', insn.lastsize), wrap(insn.lastmem)
    
def ADD_mem_R(insn): return
def ADD_mem_X(insn): return

#ADC
def ADC_R_r(insn): 
    dst = popR(insn, '?', insn.lastsize)
    return "ADC", dst, insn.lastr
def ADC_r_X(insn): return
def ADC_R_mem(insn): return
def ADC_mem_R(insn): return
def ADC_mem_X(insn): return

#SUB
def SUB_R_r(insn):
    dst = popR(insn, '?', insn.lastsize)
    return "SUB", dst, insn.lastr

def SUB_r_X(insn):
    insn.pop()
    return "SUB", insn.lastr, insn.popn(insn.lastsize)
    
def SUB_R_mem(insn): return
def SUB_mem_R(insn): return
def SUB_mem_X(insn): return

#SBC
def SBC_R_r(insn): return
def SBC_r_X(insn): return
def SBC_R_mem(insn): return
def SBC_mem_R(insn): return
def SBC_mem_X(insn): return

#CP
def CP_R_r(insn): return

def CP_R_3X(n):
    def CP_R_N(insn):
        return
    return CP_R_N

def CP_r_X(insn): 
    insn.pop()
    return "CP", insn.lastr, insn.popn(insn.lastsize)

def CP_R_mem(insn): return
def CP_mem_R(insn): return
def CP_mem_X(insn): return

#INC
def INCF(insn): return

# TODO: INC and DEC, replace constant INC 1, REG with INC REG
def INC_X3_r(n):
    def INC_N_r(insn):
        insn.pop()
        return "INC", n, insn.lastr
    return INC_N_r

def INC_X3_mem(n):
    def INC_N_mem(insn):
        return
    return INC_N_mem
    
#DEC
def DECF(insn): insn.pop(); return "DECF"

def DEC_X3_r(n):
    def DEC_N_r(insn):
        insn.pop()
        return "DEC", n, insn.lastr
    return DEC_N_r

def DEC_X3_mem(n):
    def DEC_N_mem(insn):
        return
    return DEC_N_mem

#NEG
def NEG_r(insn): return

#EXTZ
def EXTZ(insn): return

#EXTS
def EXTS(insn): return

#DAA
def DAA(insn): return

#PAA
def PAA(insn): return

rrtable_8 = ["WA", "BC", None, "DE" , "HL"]

def rregname(register):
    ext = register.ext
    size = register.size
    reg = register.reg
    
    if not ext:
        if size == BYTE:
            return rrtable_8[reg]
        elif size == WORD:
            return Rregtable[LWORD][reg]
        else: return str(reg)
    else:
        return regname(register)

#MUL
def MUL_RR_r(insn): 
    return "MUL", RReg(popR(insn, '?', insn.lastsize)), insn.lastr
    
def MUL_rr_X(insn): return
def MUL_RR_mem(insn): return

#MULS
def MULS_RR_r(insn): return
def MULS_rr_X(insn): return
def MULS_RR_mem(insn): return

#DIV
def DIV_RR_r(insn): return
def DIV_rr_X(insn): return
def DIV_RR_mem(insn): return

#DIVS
def DIVS_RR_r(insn): return
def DIVS_rr_X(insn): return
def DIVS_RR_mem(insn): return

#MULA
def MULA(insn): return

#MINC
def MINC(n):
    def MINCN(insn):
        return
    return MINCN
    
#MDEC
def MDEC(n):
    def MDECN(insn):
        return
    return MDECN
    
# 5) Logical operations

#AND
def AND_R_r(insn): return
def AND_r_X(insn):
    insn.pop()
    return "AND", insn.lastr, insn.popn(insn.lastsize)

def AND_R_mem(insn): return
def AND_mem_R(insn): 
    reg = popR(insn, '?', insn.lastsize)
    return "AND", wrap(insn.lastmem), reg
def AND_mem_X(insn): return

#OR
def OR_R_r(insn): 
    return "OR", popR(insn, '?', insn.lastsize), insn.lastr

def OR_r_X(insn): return
def OR_R_mem(insn): return
def OR_mem_R(insn): return
def OR_mem_X(insn): return

#XOR
def XOR_R_r(insn):
    return "XOR", popR(insn, '?', insn.lastsize), insn.lastr
    
def XOR_r_X(insn): 
    insn.pop()
    return "XOR", insn.lastr, insn.popn(insn.lastsize)
    
def XOR_R_mem(insn): return
def XOR_mem_R(insn): return
def XOR_mem_X(insn): return

#CPL
def CPL_r(insn): return

# 6) Bit operations

#LDCF
def LDCF_X_r(insn): return
def LDCF_A_r(insn): return

def LDCF_X3_mem(n):
    def LDCF_N_mem(insn):
        return
    return LDCF_N_mem

def LDCF_A_mem(insn): return

#STCF
def STCF_X_r(insn): return
def STCF_A_r(insn): return

def STCF_X3_mem(n):
    def STCF_N_mem(insn):
        return
    return STCF_N_mem
    
def STCF_A_mem(insn): return

#ANDCF
def ANDCF_X_r(insn): return
def ANDCF_A_r(insn): return

def ANDCF_X3_mem(n):
    def ANDCF_N_mem(insn):
        return
    return ANDCF_N_mem
    
def ANDCF_A_mem(insn): return

#ORCF
def ORCF_X_r(insn): return
def ORCF_A_r(insn): return

def ORCF_X3_mem(n):
    def ORCF_N_mem(insn):
        return
    return ORCF_N_mem
    
def ORCF_A_mem(insn): return

#XORCF
def XORCF_X_r(insn): return
def XORCF_A_r(insn): return

def XORCF_X3_mem(n):
    def XORCF_N_mem(insn):
        return
    return XORCF_N_mem
    
def XORCF_A_mem(insn): return

#RCF, SCF, CCF, ZCF
def RCF(insn): return
def SCF(insn): return
def CCF(insn): return
def ZCF(insn): return

#BIT
def BIT_X_r(insn): 
    insn.pop()
    return "BIT", (insn.pop() & 0xF), insn.lastr

def BIT_X3_mem(n):
    def BIT_N_mem(insn):
        return
    return BIT_N_mem

#RES
def RES_X_r(insn): return
def RES_X3_mem(n):
    def RES_N_mem(insn):
        return
    return RES_N_mem
    
#SET
def SET_X_r(insn):
    insn.pop()
    return "SET", (insn.pop() & 0xF), insn.lastr
    
def SET_X3_mem(n):
    def SET_N_mem(insn):
        return
    return SET_N_mem

#CHG
def CHG_X_r(insn): return
def CHG_X3_mem(n):
    def CHG_N_mem(insn):
        return
    return CHG_N_mem

#TSET
def TSET_X_r(insn): return
def TSET_X3_mem(n):
    def TSET_N_mem(insn):
        return
    return TSET_N_mem

#BS1
def BS1F(insn): return
def BS1B(insn): return

# 7) Special operations and CPU control

#NOP
def NOP(insn): insn.pop(); return "NOP"

#NORMAL
def NORMAL(insn): return

#MAX
def MAX(insn): insn.pop(); return "MAX"

#MIN
def MIN(insn): insn.pop(); return "MIN"

#EI
def EI(insn): return

#DI
def DI(insn): return

#PUSH
def PUSH_SR(insn): return

#POP
def POP_SR(insn): return

#SWI
def SWI(insn): return

#HALT
def HALT(insn): return

#LDC
def LDC_cr_r(insn): return
def LDC_r_cr(insn): return

#LDX
def LDX(insn): return

#LINK
def LINK(insn): return

#UNLNK
def UNLNK(insn): return

#LDF
def LDF_n(insn): return

#SCC
def SCC(insn): 
    return "SCC", cctable[popcc(insn)], insn.lastr
    
# 9) Rotate and shift

#RLC
def RLC_X_r(insn):
    insn.pop()
    return "RLC", (insn.pop() & 0xF), insn.lastr
    
def RLC_A_r(insn): return
def RLC_mem(insn): return

#RRC
def RRC_X_r(insn):
    insn.pop()
    return "RRC", (insn.pop() & 0xF), insn.lastr

def RRC_A_r(insn): return
def RRC_mem(insn): return

#RL
def RL_X_r(insn): 
    insn.pop()
    return "RL", (insn.pop() & 0xF), insn.lastr
    
def RL_A_r(insn): return
def RL_mem(insn): return

#RR
def RR_X_r(insn): 
    insn.pop()
    return "RR", (insn.pop() & 0xF), insn.lastr
    
def RR_A_r(insn): return
def RR_mem(insn): return

#SLA
def SLA_X_r(insn): return
def SLA_A_r(insn): return
def SLA_mem(insn): return

#SRA
def SRA_X_r(insn): return
def SRA_A_r(insn): return
def SRA_mem(insn): return

#SLL
def SLL_X_r(insn):
    insn.pop()
    return "SLL", (insn.pop() & 0xF), insn.lastr
    
def SLL_A_r(insn): return
def SLL_mem(insn): return

#SRL
def SRL_X_r(insn):
    insn.pop()
    return "SRL", (insn.pop() & 0xF), insn.lastr
    
def SRL_A_r(insn): return
def SRL_mem(insn): return

#RLD / RRD
def RLD(insn): return
def RRD(insn): return

# 9) Jump, call and return

#JP
def JP_nn(insn): 
    insn.pop()
    return "JP", insn.popw()
def JP_nnn(insn):
    insn.pop()
    return "JP", (insn.popw() | (insn.pop() << 16))

def JP_cc_mem(insn): return

def JR_cc(insn): 
    pc = insn.pc
    cc = cctable[popcc(insn)]
    loc = insn.pop()
    
    return "JR", cc, (pc + 2 + loc)
    return

def JRL_cc(insn): 
    pc = insn.pc
    cc = cctable[popcc(insn)]
    loc = insn.popw()
    
    return "JRL", cc, (pc + 3 + loc)
def JP_mem(insn): return
    
#CALL
def CALL_nn(insn):
    insn.pop()
    return "CALL", insn.popw()
def CALL_nnn(insn):
    insn.pop()
    return "CALL", (insn.popw() | (insn.pop() << 16))

def CALL_cc_mem(insn): return
def CALR(insn): return
def CALL(insn): return

#DJNZ
def DJNZ(insn): return

#RET
def RET(insn): insn.pop(); return "RET"
def RET_cc(insn): return
    
def RETD(insn): return
def RETI(insn): return

# General utility functions:

# Converts argument x to str and wraps it in paranthesis
def wrap(x):
    return "(" + str(x) + ")"

def call_opc(insn, x, y, optable):
    opc = optable[x][y]   
    if opc is None:
        print str(insn.pc) + ":", hex(x), hex(y), "UNDEFINED"
        return ("UNDEFINED",)
    else:
        print str(insn.pc) + ":", hex(x), hex(y), opc.__name__
        asm = opc(insn)
        if type(asm) is tuple: 
            return asm
        elif asm is None:
            raise Exception("Not implemented") 
        else: return (asm,)

def src(insn):
    x, y = peekopc(insn)    
    if (x >= 0xC): 
        insn.lastsize = x - 0xC
        insn.lastmem = popmem(insn)
    else:
        insn.lastsize = x - 0x8
        insn.lastr = popR(insn, '?', LWORD)

    x, y = peekopc(insn)
    return call_opc(insn, x, y, optable_src)

def dst(insn):
    insn.lastmem = popmem(insn)
    x, y = peekopc(insn)
    return call_opc(insn, x, y, optable_dst)
    
def reg(insn):
    insn.last = insn.peek() # Not really needed but added for consistency
    x, y = peekopc(insn)
    size = x - 0xC
    if y == 0x7:
        # Can have extended registers
        insn.lastr = popr(insn, '?', size)
    else:
        insn.lastr = popR(insn, '?', size)
    insn.lastsize = size
    
    x, y = peekopc(insn)
    return call_opc(insn, x, y, optable_reg)
    
def next_insn(insn, out):
    x, y = peekopc(insn)
    opc = call_opc(insn, x, y, optable)
    asm = str(opc[0]) + " "
    for i in range(1, len(opc)):
        if i != 1: asm += ", "
        asm += str(opc[i])
            
    print ">>> " + asm + "\n"
    #out.write(asm)
    return
    
def popcc(insn):
    cc = insn.pop()
    return (cc & 0x0F)

def popmem(insn):
    mem = insn.pop()
    if (mem & 0x40) == 0:
        if (mem & 0x8) == 0:
            # XWA to XSP
            return 0xE0 + 4 * (mem & 0x7)
        else:
            # XWA to XSP + d8
            return (0xE0 + 4 * (mem & 0x7)) + insn.pop()
    elif (mem & 0x4) == 0x4:
        
        mem2 = insn.pop()
        c = (mem2 & 0x2)
        c = 1 if c == 0 else c * 2
        if (mem & 0x1) == 0:
            return (mem2 & 0xFE) * 4 - c # -r32
        else:
            return (mem2 & 0xFE) * 4 + c # r32+
    else:
        n = mem & 0x3
        if n == 0: 
            return insn.pop() # 8
        elif n == 1:
            return insn.popw() # 16
        elif n == 2:
            return insn.popw() | (insn.pop() >> 16) # 24
        else:
            mem = insn.pop()
            n = mem & 0x3
            if n == 0:
                return mem * 4 # r32
            elif n == 1:
                return (mem & 0xFE) * 4 + insn.popw() # r32 + d16
            elif mem == 0x3:
                return insn.pop() * 4 + insn.pop()
            else:
                return insn.pop() * 4 + insn.pop() * 2
                
                
    
bnames = ["A", "W", "C", "B", "E", "D", "L", "H"]
wnames = ["WA", "BC", "DE", "HL"]
lnames = ["XWA", "XBC", "XDE", "XHL"]
extnames = ["X", "Y", "Z", "P"]

# takes the returned register of popr / popR
# returns a register name or the address if its an invalid register
def regname(register):
    ext = register.ext
    size = register.size
    reg = register.reg
    
    if not ext:
        return Rregtable[size][reg]
    
    if (size == WORD and reg & 1) != 0: 
        return str(reg) # Check if divisible by 2
    elif (size == LWORD and reg & 0b11) != 0: 
        return str(reg) # Check if divisible by 4
    
    rname = ""
    if reg <= 0x7F: # Normal banks
        if size == BYTE:
            rname += "Q" if (reg & 0b0010) != 0 else "R"
            rname += bnames[((reg & 0b1100) >> 1) | (reg & 1)]
        elif size == WORD:    
            rname += "Q" if (reg & 0b0010) != 0 else "R"
            rname += wnames[(reg & 0b1100) >> 2]
        elif size == LWORD:
            rname += lnames[(reg & 0b1100) >> 2]
        rname += str((reg & 0xF0) >> 4)
    elif reg >= 0xD0 and reg <= 0xEF:
        if size == BYTE:
            if (reg & 0b0010) != 0: rname += "Q"
            rname += bnames[((reg & 0b1100) >> 1) | (reg & 1)]
        elif size == WORD:
            if (reg & 0b0010) != 0: rname += "Q"
            rname += wnames[(reg & 0b1100) >> 2]
        elif size == LWORD:
            rname += lnames[(reg & 0b1100) >> 2]
        if reg <= 0xDC:
            rname += "'"
        elif reg <= 0xE0:
            return str(reg)
    elif reg >= 0xF0 and reg <= 0xFF:
        if size == BYTE:
            if (reg & 0b0010) != 0: rname += "Q"
        elif size == LWORD:
            rname += "Z"
        if (reg & 0xFC) == 0xFC:
            rname += "S"
        else: rname += "I"
        rname += extnames[(reg & 0b1100) >> 2]
        if size == BYTE:
            rname += "H" if (reg & 0b0010) != 0 else "L"
    else:
        return str(reg)
    
    return rname
    
operand_size_table = {
    'z' : [0, 1, None],
    'zz' : [0b00, 0b01, 0b10],
    'zzz' : [0b010, 0b011, 0b100],
    's' : [None, 0, 1]
}

# Arguments [insn, type = s/z/zz/zzz/?, [size = -1], [spos = -1]]
def popr(insn, tpe, size = -1, spos = -1):
    b = insn.peek()
    # check if we are using extended addresses, flag is 0x7
    extended = ((b ^ 0x7) & 0x7) == 0
    
    reg = popR(insn, tpe, size, spos)
    
    if not extended: return reg
    
    return Reg(True, reg.size, insn.pop())

# Arguments [insn, type = s/z/zz/zzz/?, [size = -1], [spos = -1]]
def popR(insn, tpe, size = -1, spos = -1):
    b = insn.pop()
    rcode = (b & 0x7)
    
    if tpe != '?':
        opsizecode = 0
        if tpe == 's' or tpe == 'z':
            if spos < 0: spos = 3
            smask = (0x80 >> spos)
            opsizecode = (b & smask) >> (8 - spos - 1)
        elif tpe == 'zz':
            if spos < 0: spos = 2
            smask = (0xC0 >> spos)
            opsizecode = (b & smask) >> (8 - spos - 2)
        elif tpe == 'zzz':
            if spos < 0: spos = 1
            smask = (0xE0 >> spos)
            opsizecode = (b & smask) >> (8 - spos - 3)
        elif tpe != '?': raise ValueError("Type must be one of s/z/zz/zzz/?")
        
        size = operand_size_table[tpe].index(opsizecode)
        
    return Reg(False, size, rcode)

def peekopc(insn, n = 1):
    opcode = insn.peek(n)
    x = (opcode & 0xF0) >> 4
    y = (opcode & 0x0F)
    return [x, y]

# Global tables

Rregtable = [
    ["W", "A", "B", "C", "D", "E", "H", "L"],
    ["WA", "BC", "DE", "HL", "IX", "IY", "IZ", "SP"],
    ["XWA", "XBC", "XDE", "XHL", "XIX", "XIY", "XIZ", "XSP"]
]

# TODO: Actually replace T with None and have a function instead of access to cctable
cctable = ["F", "LT", "LE", "ULE", "PE/OV", "M", "Z", "C", "T", "GE", "GT", "UGT", "PO/NOV", "P", "NZ", "NC"]

optable = [
    [NOP, NORMAL, PUSH_SR, POP_SR, MAX, HALT, EI, RETI, LD_n_n, PUSH_n, LDW_n_nn, PUSHW_nn, INCF, DECF, RET, RETD],
    [RCF, SCF, CCF, ZCF, PUSH_A, POP_A, EX_F_F1, LDF_n, PUSH_F, POP_F, JP_nn, JP_nnn, CALL_nn, CALL_nnn, CALR, None],
    [LD_R_n, LD_R_n, LD_R_n, LD_R_n, LD_R_n, LD_R_n, LD_R_n, LD_R_n, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR],
    [LD_RR_nn, LD_RR_nn, LD_RR_nn, LD_RR_nn, LD_RR_nn, LD_RR_nn, LD_RR_nn, LD_RR_nn, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR, PUSH_RR],
    [LD_XRR_nnnn, LD_XRR_nnnn, LD_XRR_nnnn, LD_XRR_nnnn, LD_XRR_nnnn, LD_XRR_nnnn, LD_XRR_nnnn, LD_XRR_nnnn, POP_RR, POP_RR, POP_RR, POP_RR, POP_RR, POP_RR, POP_RR, POP_RR],
    [None, None, None, None, None, None, None, None, POP_XRR, POP_XRR, POP_XRR, POP_XRR, POP_XRR, POP_XRR, POP_XRR, POP_XRR],
    [JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc, JR_cc],
    [JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc, JRL_cc],
    [src, src, src, src, src, src, src, src, src, src, src, src, src, src, src, src],
    [src, src, src, src, src, src, src, src, src, src, src, src, src, src, src, src],
    [src, src, src, src, src, src, src, src, src, src, src, src, src, src, src, src],
    [dst, dst, dst, dst, dst, dst, dst, dst, dst, dst, dst, dst, dst, dst, dst, dst],
    [src, src, src, src, src, src, None, reg, reg, reg, reg, reg, reg, reg, reg, reg],
    [src, src, src, src, src, src, None, reg, reg, reg, reg, reg, reg, reg, reg, reg],
    [src, src, src, src, src, src, None, reg, reg, reg, reg, reg, reg, reg, reg, reg],
    [dst, dst, dst, dst, dst, dst, None, LDX, SWI(0), SWI(1), SWI(2), SWI(3), SWI(3), SWI(4), SWI(5), SWI(6), SWI(7)]
]

optable_reg = [
    [None, None, None, LD_r_X, PUSH_r, POP_r, CPL_r, NEG_r, MUL_rr_X, MULS_rr_X, DIV_rr_X, DIVS_rr_X, LINK, UNLNK, BS1F, BS1B],
    [DAA, EXTZ, EXTS, PAA, None, MIRR, None, None, MULA, None, None, DJNZ, None, None, None],
    [ANDCF_X_r, ORCF_X_r, XORCF_X_r, LDCF_X_r, STCF_X_r, None, None, None, ANDCF_A_r, ORCF_A_r, XORCF_A_r, LDCF_A_r, STCF_A_r, None, LDC_cr_r, LDC_r_cr],
    [RES_X_r, SET_X_r, CHG_X_r, BIT_X_r, TSET_X_r, None, None, None, MINC(1), MINC(2), MINC(4), None, MDEC(1), MDEC(2), MDEC(4), None],
    [MUL_RR_r, MUL_RR_r, MUL_RR_r, MUL_RR_r, MUL_RR_r, MUL_RR_r, MUL_RR_r, MUL_RR_r, MULS_RR_r, MULS_RR_r, MULS_RR_r, MULS_RR_r, MULS_RR_r, MULS_RR_r, MULS_RR_r, MULS_RR_r],
    [DIV_RR_r, DIV_RR_r, DIV_RR_r, DIV_RR_r, DIV_RR_r, DIV_RR_r, DIV_RR_r, DIV_RR_r, DIVS_RR_r, DIVS_RR_r, DIVS_RR_r, DIVS_RR_r, DIVS_RR_r, DIVS_RR_r, DIVS_RR_r, DIVS_RR_r],
    [INC_X3_r(8), INC_X3_r(1), INC_X3_r(2), INC_X3_r(3), INC_X3_r(4), INC_X3_r(5), INC_X3_r(6), INC_X3_r(7), DEC_X3_r(8), DEC_X3_r(1), DEC_X3_r(2), DEC_X3_r(3), DEC_X3_r(4), DEC_X3_r(5), DEC_X3_r(6), DEC_X3_r(7)],
    [SCC, SCC, SCC, SCC, SCC, SCC, SCC, SCC, SCC, SCC, SCC, SCC, SCC, SCC, SCC, SCC],
    [ADD_R_r, ADD_R_r, ADD_R_r, ADD_R_r, ADD_R_r, ADD_R_r, ADD_R_r, ADD_R_r, LD_R_r, LD_R_r, LD_R_r, LD_R_r, LD_R_r, LD_R_r, LD_R_r, LD_R_r],
    [ADC_R_r, ADC_R_r, ADC_R_r, ADC_R_r, ADC_R_r, ADC_R_r, ADC_R_r, ADC_R_r, LD_r_R, LD_r_R, LD_r_R, LD_r_R, LD_r_R, LD_r_R, LD_r_R, LD_r_R],
    [SUB_R_r, SUB_R_r, SUB_R_r, SUB_R_r, SUB_R_r, SUB_R_r, SUB_R_r, SUB_R_r, LD_r_3X(0), LD_r_3X(1), LD_r_3X(2), LD_r_3X(3), LD_r_3X(4), LD_r_3X(5), LD_r_3X(6), LD_r_3X(7)],
    [SBC_R_r, SBC_R_r, SBC_R_r, SBC_R_r, SBC_R_r, SBC_R_r, SBC_R_r, SBC_R_r, EX_R_r, EX_R_r, EX_R_r, EX_R_r, EX_R_r, EX_R_r, EX_R_r, EX_R_r],
    [AND_R_r, AND_R_r, AND_R_r, AND_R_r, AND_R_r, AND_R_r, AND_R_r, AND_R_r, ADD_r_X, ADC_r_X, SUB_r_X, SBC_r_X, AND_r_X, XOR_r_X, OR_r_X, CP_r_X],
    [XOR_R_r, XOR_R_r, XOR_R_r, XOR_R_r, XOR_R_r, XOR_R_r, XOR_R_r, XOR_R_r, CP_R_3X(0), CP_R_3X(1), CP_R_3X(2), CP_R_3X(3), CP_R_3X(4), CP_R_3X(5), CP_R_3X(6), CP_R_3X(7)],
    [OR_R_r, OR_R_r, OR_R_r, OR_R_r, OR_R_r, OR_R_r, OR_R_r, OR_R_r, RLC_X_r, RRC_X_r, RL_X_r, RR_X_r, SLA_X_r, SRA_X_r, SLL_X_r, SRL_X_r],
    [CP_R_r, CP_R_r, CP_R_r, CP_R_r, CP_R_r, CP_R_r, CP_R_r, CP_R_r, RLC_A_r, RRC_A_r, RL_A_r, RR_A_r, SLA_A_r, SRA_A_r, SLL_A_r, SRL_A_r],
]

optable_src = [
    [None, None, None, None, PUSH_mem, None, RLD, RRD, None, None, None, None, None, None, None, None],
    [LDI, LDIR, LDD, LDDR, CPI, CPIR, CPD, CPDR, None, LD_nn_m, None, None, None, None, None, None],
    [LD_R_mem, LD_R_mem, LD_R_mem, LD_R_mem, LD_R_mem, LD_R_mem, LD_R_mem, LD_R_mem, None, None, None, None, None, None, None, None],
    [EX_mem_R, EX_mem_R, EX_mem_R, EX_mem_R, EX_mem_R, EX_mem_R, EX_mem_R, EX_mem_R, ADD_mem_X, ADC_mem_X, SUB_mem_X, SBC_mem_X, AND_mem_X, XOR_mem_X, OR_mem_X, CP_mem_X],
    [MUL_RR_mem, MUL_RR_mem, MUL_RR_mem, MUL_RR_mem, MUL_RR_mem, MUL_RR_mem, MUL_RR_mem, MUL_RR_mem, MULS_RR_mem, MULS_RR_mem, MULS_RR_mem, MULS_RR_mem, MULS_RR_mem, MULS_RR_mem, MULS_RR_mem, MULS_RR_mem],
    [DIV_RR_mem, DIV_RR_mem, DIV_RR_mem, DIV_RR_mem, DIV_RR_mem, DIV_RR_mem, DIV_RR_mem, DIV_RR_mem, DIVS_RR_mem, DIVS_RR_mem, DIVS_RR_mem, DIVS_RR_mem, DIVS_RR_mem, DIVS_RR_mem, DIVS_RR_mem, DIVS_RR_mem],
    [INC_X3_mem(8), INC_X3_mem(1), INC_X3_mem(2), INC_X3_mem(3), INC_X3_mem(4), INC_X3_mem(5), INC_X3_mem(6), INC_X3_mem(7), INC_X3_mem(8), DEC_X3_mem(1), DEC_X3_mem(2), DEC_X3_mem(3), DEC_X3_mem(4), DEC_X3_mem(5), DEC_X3_mem(6), DEC_X3_mem(7)],
    [None, None, None, None, None, None, None, None, RLC_mem, RRC_mem, RL_mem, RR_mem, SLA_mem, SRA_mem, SLL_mem, SRL_mem],
    [ADD_R_mem, ADD_R_mem, ADD_R_mem, ADD_R_mem, ADD_R_mem, ADD_R_mem, ADD_R_mem, ADD_R_mem, ADD_mem_R, ADD_mem_R, ADD_mem_R, ADD_mem_R, ADD_mem_R, ADD_mem_R, ADD_mem_R, ADD_mem_R],
    [ADC_R_mem, ADC_R_mem, ADC_R_mem, ADC_R_mem, ADC_R_mem, ADC_R_mem, ADC_R_mem, ADC_R_mem, ADC_mem_R, ADC_mem_R, ADC_mem_R, ADC_mem_R, ADC_mem_R, ADC_mem_R, ADC_mem_R, ADC_mem_R],
    [SUB_R_mem, SUB_R_mem, SUB_R_mem, SUB_R_mem, SUB_R_mem, SUB_R_mem, SUB_R_mem, SUB_R_mem, SUB_mem_R, SUB_mem_R, SUB_mem_R, SUB_mem_R, SUB_mem_R, SUB_mem_R, SUB_mem_R, SUB_mem_R],
    [SBC_R_mem, SBC_R_mem, SBC_R_mem, SBC_R_mem, SBC_R_mem, SBC_R_mem, SBC_R_mem, SBC_R_mem, SBC_mem_R, SBC_mem_R, SBC_mem_R, SBC_mem_R, SBC_mem_R, SBC_mem_R, SBC_mem_R, SBC_mem_R],
    [AND_R_mem, AND_R_mem, AND_R_mem, AND_R_mem, AND_R_mem, AND_R_mem, AND_R_mem, AND_R_mem, AND_mem_R, AND_mem_R, AND_mem_R, AND_mem_R, AND_mem_R, AND_mem_R, AND_mem_R, AND_mem_R],
    [XOR_R_mem, XOR_R_mem, XOR_R_mem, XOR_R_mem, XOR_R_mem, XOR_R_mem, XOR_R_mem, XOR_R_mem, XOR_mem_R, XOR_mem_R, XOR_mem_R, XOR_mem_R, XOR_mem_R, XOR_mem_R, XOR_mem_R, XOR_mem_R],
    [OR_R_mem, OR_R_mem, OR_R_mem, OR_R_mem, OR_R_mem, OR_R_mem, OR_R_mem, OR_R_mem, OR_mem_R, OR_mem_R, OR_mem_R, OR_mem_R, OR_mem_R, OR_mem_R, OR_mem_R, OR_mem_R],
    [CP_R_mem, CP_R_mem, CP_R_mem, CP_R_mem, CP_R_mem, CP_R_mem, CP_R_mem, CP_R_mem, CP_mem_R, CP_mem_R, CP_mem_R, CP_mem_R, CP_mem_R, CP_mem_R, CP_mem_R, CP_mem_R]
]

optable_dst = [
    [LDB_m_X, None, LDW_m_X, None, POPB_mem, None, POPW_mem, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, LDB_m_nn, None, LDW_m_nn, None, None, None, None, None, None, None, None, None],
    [LDAW_R_mem, LDAW_R_mem, LDAW_R_mem, LDAW_R_mem, LDAW_R_mem, LDAW_R_mem, LDAW_R_mem, LDAW_R_mem, ANDCF_A_mem, ORCF_A_mem, XORCF_A_mem, LDCF_A_mem, STCF_A_mem, None, None, None],
    [LDAL_R_mem, LDAL_R_mem, LDAL_R_mem, LDAL_R_mem, LDAL_R_mem, LDAL_R_mem, LDAL_R_mem, LDAL_R_mem, None, None, None, None, None, None, None, None],
    [LDB_mem_R, LDB_mem_R, LDB_mem_R, LDB_mem_R, LDB_mem_R, LDB_mem_R, LDB_mem_R, LDB_mem_R, None, None, None, None, None, None, None, None],
    [LDW_mem_R, LDW_mem_R, LDW_mem_R, LDW_mem_R, LDW_mem_R, LDW_mem_R, LDW_mem_R, LDW_mem_R, None, None, None, None, None, None, None, None],
    [LDL_mem_R, LDL_mem_R, LDL_mem_R, LDL_mem_R, LDL_mem_R, LDL_mem_R, LDL_mem_R, LDL_mem_R, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [ANDCF_X3_mem(0), ANDCF_X3_mem(1), ANDCF_X3_mem(2), ANDCF_X3_mem(3), ANDCF_X3_mem(4), ANDCF_X3_mem(5), ANDCF_X3_mem(6), ANDCF_X3_mem(7), ORCF_X3_mem(0), ORCF_X3_mem(1), ORCF_X3_mem(2), ORCF_X3_mem(3), ORCF_X3_mem(4), ORCF_X3_mem(5), ORCF_X3_mem(6), ORCF_X3_mem(7)],
    [XORCF_X3_mem(0), XORCF_X3_mem(1), XORCF_X3_mem(2), XORCF_X3_mem(3), XORCF_X3_mem(4), XORCF_X3_mem(5), XORCF_X3_mem(6), XORCF_X3_mem(7), LDCF_X3_mem(0), LDCF_X3_mem(1), LDCF_X3_mem(2), LDCF_X3_mem(3), LDCF_X3_mem(4), LDCF_X3_mem(5), LDCF_X3_mem(6), LDCF_X3_mem(7)],
    [STCF_X3_mem(0), STCF_X3_mem(1), STCF_X3_mem(2), STCF_X3_mem(3), STCF_X3_mem(4), STCF_X3_mem(5), STCF_X3_mem(6), STCF_X3_mem(7), TSET_X3_mem(0), TSET_X3_mem(1), TSET_X3_mem(2), TSET_X3_mem(3), TSET_X3_mem(4), TSET_X3_mem(5), TSET_X3_mem(6), TSET_X3_mem(7)],
    [RES_X3_mem(0), RES_X3_mem(1), RES_X3_mem(2), RES_X3_mem(3), RES_X3_mem(4), RES_X3_mem(5), RES_X3_mem(6), RES_X3_mem(7), SET_X3_mem(0), SET_X3_mem(1), SET_X3_mem(2), SET_X3_mem(3), SET_X3_mem(4), SET_X3_mem(5), SET_X3_mem(6), SET_X3_mem(7)],
    [CHG_X3_mem(0), ANDCF_X3_mem(1), ANDCF_X3_mem(2), ANDCF_X3_mem(3), ANDCF_X3_mem(4), ANDCF_X3_mem(5), ANDCF_X3_mem(6), ANDCF_X3_mem(7), BIT_X3_mem(0), BIT_X3_mem(1), BIT_X3_mem(2), BIT_X3_mem(3), BIT_X3_mem(4), BIT_X3_mem(5), BIT_X3_mem(6), BIT_X3_mem(7)],
    [JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem, JP_cc_mem],
    [CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem, CALL_cc_mem],
    [RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc, RET_cc]
]