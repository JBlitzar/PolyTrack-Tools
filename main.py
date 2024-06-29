from imagebuilder import ImageBuilder
from shapebuilder import ShapeBuilder
from titlebuilder import TitleBuilder
from trackbuilder import TrackBuilder
from voxelbuilder import VoxelBuilder
import time

from chainer import Chainer


for i in range(100):
     chainer = Chainer("skibidi")



     chainer.chain(TrackBuilder(), "add_starting_point", {"pos":(0, 1, 0)})

     pieces = []



     for j in range(i):
          pieces.append({"id":52,"x":1,"y":1,"z":j+1})
     
     pieces.append({"id":6,"x":1,"y":1,"z":i+2})
     print(pieces)
     time.sleep(1)
     chainer.chain(TrackBuilder(), "add_pieces", {"pieces":pieces})

     #chainer.chain(TitleBuilder(), "create_cover_image", {"title":"JBlitzar", "subtitle":"", "offset":(100,0,0), "negate":True})

     #chainer.chain(VoxelBuilder(), "add_file", {"file_path":"toilet.obj", "scale_factor":5})

     with open("out.txt", "a") as file:
          file.write(f"\nStraightaway: {i+1} "+chainer.export())