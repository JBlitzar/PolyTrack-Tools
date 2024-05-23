from imagebuilder import ImageBuilder
from shapebuilder import ShapeBuilder
from titlebuilder import TitleBuilder
from trackbuilder import TrackBuilder
from chainer import Chainer



chainer = Chainer("Chaining")

chainer.chain(TrackBuilder(), "load_from_code", {"code": "v2CAlpH4p9YlBGZAEoB4kI4ffff1zAbIxffBkPAAuR5BIA"})

chainer.chain(TitleBuilder(), "create_cover_image", {"title":"Test", "subtitle":"", "offset":(100,0,0)})

with open("out.txt", "w+") as file: 
     file.write(chainer.export())