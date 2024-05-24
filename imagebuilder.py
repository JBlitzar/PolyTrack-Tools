from trackbuilder import TrackBuilder
from PIL import Image, ImagePalette
from typing import Optional, Union, List, Dict, Type, Tuple

class ImageBuilder(TrackBuilder):
    def __init__(self, name: str = "", height:int = 2**16) -> None:
        super().__init__(name)

        self.height = height
        self.palette = {
                (77, 138, 218): 0,
                (192, 58, 51): 6, 
                (255, 255, 255): 5,
                (221, 193, 74): 52, 
                (20, 32, 79): -1 
            }
        
    def get_pil_palette(self):
        palette = list(self.palette.keys())
        
        palette = [list(i) for i in palette]

        concatenated = []

        [concatenated.extend(i) for i in palette]

        im = Image.new('P', (1,1))

        im.putpalette(concatenated)

        return im
    

    def add_image(self, image: Image, size: Union[Tuple[int, int], None] = None, monochrome: bool = False, offset: Tuple[int, int, int] = (0,0,0)):
        if size != None:
            image = image.resize(size)
        if monochrome:
            image = image.convert('1')
            width, height = image.size
            for y in range(height):
                for x in range(width):
                    pixel_color = image.getpixel((x, y))
                    #print(pixel_color)
                    pixel_id = 0 if pixel_color == 255 else -1
                    if pixel_id != -1:
                        if pixel_id == self.get_id_alias("checkpoint"):
                            self.add_piece(pixel_id, x+offset[0], self.height+offset[1], y+offset[2], 0, 0)
                        else:
                            self.add_piece(pixel_id, x+offset[0], self.height+offset[1], y+offset[2], 0, None)
        else:
            
            image = image.quantize(colors=len(list(self.palette.keys())), palette=self.get_pil_palette())
            width, height = image.size
            for y in range(height):
                for x in range(width):
                    pixel_color = image.getpixel((x, y))
                    pixel_id = self.palette[list(self.palette.keys())[pixel_color]]
                    if pixel_id != -1:
                        if pixel_id == self.get_id_alias("checkpoint"):
                            self.add_piece(pixel_id, x+offset[0], self.height+offset[1], y+offset[2], 0, 0)
                        else:
                            self.add_piece(pixel_id, x+offset[0], self.height+offset[1], y+offset[2], 0, None)
        
