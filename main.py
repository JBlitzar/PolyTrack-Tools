from imagebuilder import ImageBuilder
from shapebuilder import ShapeBuilder
from titlebuilder import TitleBuilder
from trackbuilder import TrackBuilder
from voxelbuilder import VoxelBuilder


from chainer import Chainer



chainer = Chainer("Skibidi toilet")



chainer.chain(TrackBuilder(), "add_starting_point", {"pos":(0, 31, 50)})

chainer.chain(TitleBuilder(), "create_cover_image", {"title":"JBlitzar", "subtitle":"", "offset":(100,0,0), "negate":True})

chainer.chain(VoxelBuilder(), "add_file", {"file_path":"toilet.obj", "scale_factor":5})

with open("out.txt", "w+") as file: 
     file.write(chainer.export())