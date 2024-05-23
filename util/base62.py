t = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
i = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]

def n(e: list[int] | bytes, t: int) -> int:
    if t >= 8 * len(e):
        raise ValueError("Out of range")
    i = t // 8
    n = e[i]
    r = t - 8 * i
    if r <= 2 or i >= len(e) - 1:
        return (n & (63 << r)) >> r
    return ((n & (63 << r)) >> r) | ((e[i + 1] & (63 >> (8 - r))) << (8 - r))

def r(e: list[int], t: int, i: int, n: int, r: bool):
    s = t // 8
    while s >= len(e):
        e.append(0)
    a = t - 8 * s
    e[s] |= n << a & 0xFF
    if a > 8 - i and not r:
        t = s + 1
        if t >= len(e):
            e.append(0)
        e[t] |= n >> 8 - a

def encode(e: list[int] | bytes) -> str:
    i = 0
    r = ""
    while i < 8 * len(e):
        s = n(e, i)
        if 30 == (30 & s):
            a = 31 & s
            i += 5
        else:
            a = s
            i += 6
        r += t[a]
    return r

def decode(e: str) -> list[int] | None:
    t = 0
    n: list[int] = []
    s = len(e)
    for a in range(s):
        o = ord(e[a])
        if o >= len(i):
            print("yes")
            return None
        l = i[o]
        if l == -1:
            print(o)
            return None
        if 30 == (30 & l):
            r(n, t, 5, l, a == s - 1)
            t += 5
        else:
            r(n, t, 6, l, a == s - 1)
            t += 6

    return n
