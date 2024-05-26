from imagebuilder import ImageBuilder
from shapebuilder import ShapeBuilder
from titlebuilder import TitleBuilder
from trackbuilder import TrackBuilder
from voxelbuilder import VoxelBuilder


from chainer import Chainer



chainer = Chainer("Teapot --JBlitzar")




chainer.chain(TrackBuilder(), "add_starting_point", {"pos":(0, 31, 50)})

chainer.chain(TitleBuilder(), "create_cover_image", {"title":"Teapot", "subtitle":"JBlitzar", "offset":(0,0,0)})

chainer.chain(VoxelBuilder(), "add_file", {"file_path":"teapot.obj", "rotate":False, "scale_factor":5})

with open("out.txt", "w+") as file: 
     file.write(chainer.export())