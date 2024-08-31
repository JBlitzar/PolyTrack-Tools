from imagebuilder import ImageBuilder
from shapebuilder import ShapeBuilder
from titlebuilder import TitleBuilder
from trackbuilder import TrackBuilder
from voxelbuilder import VoxelBuilder
import time
from PIL import Image

from chainer import Chainer


builder = ImageBuilder("hardfish")
builder.add_image(Image.open("hardfish.png"), size=(240,240),monochrome=True)
builder.add_starting_point()
with open("out.txt", "a") as file:
    file.write(builder.export("hardfish_jblitzar"))


