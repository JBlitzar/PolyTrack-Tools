# trackgen code by @cwcinc

import zlib
import base62

def gen_track_code(track_name: str, track_pieces: dict[int, list[dict[str, int]]]) -> str:
    # Track data -> binary -> zlib (compression level 9) -> base62 encoding

    track_bytes = b''

    for part_id, parts in track_pieces.items():
        track_bytes += part_id.to_bytes(2, byteorder='little', signed=False)
        track_bytes += len(parts).to_bytes(4, byteorder='little', signed=False)

        for part in parts:
            for key in ['x', 'y', 'z']:
                val = part[key]
                if key in ['x', 'z']:
                    val += 2**23

                track_bytes += val.to_bytes(3, byteorder='little', signed=False)

            val = part['r']
            track_bytes += val.to_bytes(1, byteorder='little', signed=False)
            
            if part_id["ckpt"]:
                val = part_id["ckpt"]
                track_bytes += val.to_bytes(2, byteorder="little", signed=False)

    #print(finalBytes.hex())
    compressed_track = zlib.compress(track_bytes, level=9)
    #print(compressed.hex())

    p1 = base62.encode([len(track_name)])
    p2 = base62.encode([ord(char) for char in track_name])
    p3 = base62.encode(compressed_track)

    # v2 + length of name encoded + track name encoded + track data encoded
    encoded_track = "v2" + p1 + p2 + p3

    return encoded_track

def decode_track_code(track_code: str) -> tuple[str, dict[int, list[dict[str, int]]]]:
    # Exclude "v2"
    track_code = track_code[2:]

    # zlib header 0x78DA is always encoded to "4p" and then other stuff
    # if it is not present then track code bork
    td_start = track_code.find("4p")
    if td_start == -1:
        raise ValueError("Invalid track code")
    
    name_data = track_code[:td_start]
    track_data = track_code[td_start:]
    
    name_len = base62.decode(name_data[:2])
    name = base62.decode(name_data[2:])
    if name is None or name_len is None:
        raise ValueError("Bad name data encoding")
    if name_len[0] != len(name):
        raise ValueError("Encoded name length is invalid")
    name_str = str(bytes(name), encoding='utf-8')

    td_decoded = base62.decode(track_data)
    if td_decoded is None:
        raise ValueError("Bad track data encoding")
    td_bin = zlib.decompress(bytes(td_decoded))
    track: dict[int, list[dict[str, int]]] = {}

    pos = 0
    while pos < len(td_bin):
        part_id = int.from_bytes(td_bin[pos:pos+2],   byteorder='little')
        part_n  = int.from_bytes(td_bin[pos+2:pos+6], byteorder='little')
        pos += 6
        track[part_id] = []
        for i in range(part_n):
            x = int.from_bytes(td_bin[pos:pos+3],   byteorder='little') - 2**23
            y = int.from_bytes(td_bin[pos+3:pos+6], byteorder='little')
            z = int.from_bytes(td_bin[pos+6:pos+9], byteorder='little') - 2**23
            r = int(td_bin[pos+9])
            pos += 10

            track[part_id].append({'x': x, 'y': y, 'z': z, 'r': r})

    return name_str, track


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
