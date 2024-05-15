# trackgen code by @cwcinc

import zlib

def generateTrackCode(trackName, trackPieces):
    # Track data -> binary -> zlib (compression level 9) -> base62 encoding

    trackBytes = b''

    for partID, parts in trackPieces.items():
        trackBytes += partID.to_bytes(2, byteorder='little', signed=False)
        trackBytes += len(parts).to_bytes(4, byteorder='little', signed=False)

        for part in parts:
            for key in ['x', 'y', 'z']:
                val = part[key]
                if key in ['x', 'z']:
                    val += 2**23

                trackBytes += val.to_bytes(3, byteorder='little', signed=False)

            val = part['r']
            trackBytes += val.to_bytes(1, byteorder='little', signed=False)

    #print(finalBytes.hex())
    compressedTrack = zlib.compress(trackBytes, level=9)
    #print(compressed.hex())


    t = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    i = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]

    def n(e, t):
        if t >= 8 * len(e):
            raise ValueError("Out of range")
        i = t // 8
        n = e[i]
        r = t - 8 * i
        if r <= 2 or i >= len(e) - 1:
            return (n & (63 << r)) >> r
        return ((n & (63 << r)) >> r) | ((e[i + 1] & (63 >> (8 - r))) << (8 - r))

    def encode(e):
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

    p1 = encode([len(trackName)])
    p2 = encode([ord(char) for char in trackName])
    p3 = encode(compressedTrack)

    # v2 + length of name encoded + track name encoded + track data encoded
    encodedFinal = "v2" + p1 + p2 + p3

    return encodedFinal


"""
<track id byte 1> <track id byte 2>
<no. parts byte 1> <no. parts byte 2> <no. parts byte 3> <no. parts byte 4>
<x pos byte 1> <x pos byte 2> <x pos byte 3>
<y pos byte 1> <y pos byte 2> <y pos byte 3>
<z pos byte 1> <z pos byte 2> <z pos byte 3>
<1 byte rotation>
[optional bytes <checkpoint order byte 1> <checkpoint order byte 2>]

<id> <id count>
<xyz rot>
<xyz rot>
<xyz rot>
...
"""
