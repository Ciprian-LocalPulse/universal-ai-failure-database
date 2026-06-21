import sys

MEMSIZE = 59049  # 3^10

ORIGINAL    = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
TRANSLATED  = "5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB6v^=I_0/8|jsb9m<.TVac`uY*MK'X~xDl}REokN:#?G\"i@"

assert len(ORIGINAL) == 94, len(ORIGINAL)
assert len(TRANSLATED) == 94, len(TRANSLATED)

ENC = {ord(o): ord(t) for o, t in zip(ORIGINAL, TRANSLATED)}

CRAZY = {
    0: [1, 0, 0],
    1: [1, 0, 2],
    2: [2, 2, 1],
}

def trits(x):
    arr = []
    for _ in range(10):
        arr.append(x % 3)
        x //= 3
    return arr  # arr[0] = LSB

def from_trits(arr):
    x = 0
    p = 1
    for d in arr:
        x += d * p
        p *= 3
    return x

def crazy_op(a, d):
    ta = trits(a)
    td = trits(d)
    res = [CRAZY[td[i]][ta[i]] for i in range(10)]
    return from_trits(res)

def rotate_right(x):
    return (x // 3) + (x % 3) * 19683  # 3^9 = 19683

class Halt(Exception):
    pass

class MalbolgeVM:
    def __init__(self, source, input_bytes=b"", max_steps=2_000_000, eof_value=59048):
        prog = [c for c in source if not c.isspace()]
        self.mem = [0] * MEMSIZE
        n = len(prog)
        for i, ch in enumerate(prog):
            self.mem[i] = ord(ch)
        for i in range(n, MEMSIZE):
            if i < 2:
                # spec doesn't define this edge case; fall back to 0,0
                a = self.mem[i-1] if i-1 >= 0 else 0
                b = a
                self.mem[i] = crazy_op(self.mem[max(i-2,0)], self.mem[i-1])
            else:
                self.mem[i] = crazy_op(self.mem[i-2], self.mem[i-1])
        self.A = 0
        self.C = 0
        self.D = 0
        self.input_bytes = input_bytes
        self.input_pos = 0
        self.eof_value = eof_value
        self.max_steps = max_steps
        self.output = bytearray()
        self.halted = False
        self.steps = 0

    def step(self):
        instr_byte = self.mem[self.C]
        if instr_byte < 33 or instr_byte > 126:
            self.halted = True
            raise Halt("invalid instruction byte (outside 33-126)")
        op = (self.C + instr_byte) % 94
        if op == 4:      # i : C = [D]
            self.C = self.mem[self.D]
        elif op == 5:    # < : print A
            self.output.append(self.A % 256)
        elif op == 23:   # / : A = input
            if self.input_pos < len(self.input_bytes):
                self.A = self.input_bytes[self.input_pos]
                self.input_pos += 1
            else:
                self.A = self.eof_value
        elif op == 39:   # * : rotate
            val = rotate_right(self.mem[self.D])
            self.mem[self.D] = val
            self.A = val
        elif op == 40:   # j : D = [D]
            self.D = self.mem[self.D]
        elif op == 62:   # p : crazy
            val = crazy_op(self.A, self.mem[self.D])
            self.mem[self.D] = val
            self.A = val
        elif op == 68:   # o : nop
            pass
        elif op == 81:   # v : halt
            self.halted = True
            return
        else:
            pass  # nop

        # encryption step at CURRENT C (post effect)
        cur = self.mem[self.C]
        if 33 <= cur <= 126:
            self.mem[self.C] = ENC[cur]
        # else undefined per spec; leave as-is

        self.C = (self.C + 1) % MEMSIZE
        self.D = (self.D + 1) % MEMSIZE

    def run(self):
        while not self.halted and self.steps < self.max_steps:
            self.step()
            self.steps += 1
        return bytes(self.output)


if __name__ == "__main__":
    pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 05_malbolge_interpreter.py <program.mb> [max_steps]")
        print("Feeds stdin to the program as input; writes program output to stdout.")
        print("Example: cat 01_README_English.md | python3 05_malbolge_interpreter.py 04_repo_echo.mb 50000")
        sys.exit(1)
    path = sys.argv[1]
    max_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    with open(path) as f:
        source = f.read()
    stdin_bytes = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""
    vm = MalbolgeVM(source, input_bytes=stdin_bytes, max_steps=max_steps)
    try:
        out = vm.run()
    except Halt:
        out = bytes(vm.output)
    sys.stdout.buffer.write(out)
