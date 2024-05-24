from imagebuilder import ImageBuilder
from shapebuilder import ShapeBuilder
from titlebuilder import TitleBuilder
from trackbuilder import TrackBuilder
from voxelbuilder import VoxelBuilder


from chainer import Chainer



chainer = Chainer("Hand")




chainer.chain(TrackBuilder(), "add_starting_point", {})

#chainer.chain(TitleBuilder(), "create_cover_image", {"title":"Trefoil", "subtitle":"", "offset":(100,0,0)})

chainer.chain(VoxelBuilder(), "add_file", {"file_path":"hand.obj"})

with open("out.txt", "w+") as file: 
     file.write(chainer.export())