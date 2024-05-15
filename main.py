import argparse
import json

import trackinfo

def main():
    parser = argparse.ArgumentParser(
        description="Command line encoding/decoding of polytrack track codes",
    )
    parser.add_argument(
        "--encode",
        dest="json_file",
        help="Read from a JSON file and encode to a track code",
        metavar="FILEPATH",
    )
    parser.add_argument(
        "--decode",
        nargs=2,
        dest="track_code",
        help="Decode a track code to JSON",
        metavar=("CODE", "FILEPATH"),
    )

    args = parser.parse_args()
    if args.json_file is None and args.track_code is None:
        parser.print_help()
        exit(0)
    if args.json_file:
        with open(args.json_file, 'r') as f:
            track_data = json.load(f)
            name = track_data["name"]
            track = track_data["track"]
            track_code = {}
            for id, data in track.items():
                track_code[int(id)] = data
            code = trackinfo.gen_track_code(name, track_code)
            print(code)
    else:
        code = args.track_code[0]
        file = args.track_code[1]

        name, track = trackinfo.decode_track_code(code)
        track_json = { "name": name, "track": track }

        with open(file, "w") as f:
            json.dump(track_json, f, indent=" " * 2)

if __name__ == "__main__":
    main()
