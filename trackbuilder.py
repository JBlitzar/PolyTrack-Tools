from util.trackinfo import gen_track_code, decode_track_code
from typing import Optional, Union, List, Dict, Type, Tuple

class TrackBuilder:
    def __init__(self, name: str="") -> None:
        self.track_json = {}
        self.name = name

    def load_from_code(self, code: str) -> None:
        self.name, self.track_json = decode_track_code(code)

    def inherit_state(self, other:Type["TrackBuilder"]) -> None:
        self.name = other.name
        for key in other.track_json.keys():
            for piece in other.track_json[key]:
                newpiece = piece
                newpiece["id"] = key
                self.add_piece(**newpiece)
    @staticmethod
    def _remove_duplicates(points) -> list[dict[str, int | float]]:
        unique_points = set((point['x'], point['y'], point['z'], point['rot'], point['ckpt']) for point in points)
        return [{'x': x, 'y': y, 'z': z, 'rot': rot, 'ckpt': ckpt} for x, y, z, rot, ckpt in unique_points]
    


    def export(self, name: str="") -> str:
        print(self.track_json)
        if name != "":
            self.name = name
        #self.track_json = self._remove_duplicates(self.track_json)
        return gen_track_code(self.name, self.track_json)
    
    def set_name(self, name: str) -> None:
        self.name = name
    
    def add_starting_point(self, pos: Tuple[int] = (0, 0, 0), r: int = 0 ):
        self.add_piece(self.get_id_alias("start"), pos[0], pos[1], pos[2], r, None)

    @staticmethod
    def get_id_alias(id: str) -> int:
        match id: 
            case "checkpoint":
                id = 52
            case "start":
                id = 5
            case "straight":
                id = 0
            case "finish":
                id = 6
            case "block":
                id = 29
        return id

    def add_piece(self, id: int, x:int, y:int, z:int, r: int=0, ckpt: Union[int, None]=0) -> None:
        #print(id, x, y, z, r, ckpt)
        # If you want another piece, use
        # v2MAFZXZylHUpV2YllER4pdTHnkDCCAAADEEBU2UEVWV2eR9pbNxDtHmkGEEG8rPfboeh4B9HwI9R4R9HxY9xYieJYqep4J9nwz6PjZ6zwc95YheFYpelYleV4F9Xwr6vi16rxb6vhN6bw76vjP0fBepePxW9tYnedYve94geD4oej4keT4L9vw36fGn1PjL6XwV9r4meb4ue74X49qTJC
        for key in self.track_json.keys():
            if (x, y, z) in [(point['x'], point['y'], point['z']) for point in self.track_json[key]]:
                #print("repeat")
                return

        try:
            self.track_json[id].append({
                "x":x,
                "y":y,
                "z":z,
                "r":r,
                "ckpt":ckpt   
            })
        except KeyError:
            self.track_json[id] = [{
                "x":x,
                "y":y,
                "z":z,
                "r":r,
                "ckpt":ckpt   
            }]
        
    def add_pieces(self, pieces: List[Dict[str, int]]) -> None:
        for piece in pieces:
            self.add_piece(**piece)

        