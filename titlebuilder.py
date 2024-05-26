from imagebuilder import ImageBuilder
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps

class TitleBuilder(ImageBuilder):
    def __init__(self, name: str = "", height: int = 2 ** 16, image_size: int = 60, background_color: str = "#ffffff") -> None:
        super().__init__(name, height)

        self.image_size = image_size
        self.background_color = background_color


    def _create_title_image(self, title, subtitle):

        # Create a blank image with the specified background color
        image = Image.new("RGB", (self.image_size, self.image_size), "white")

        # Create a drawing context
        draw = ImageDraw.Draw(image)

        # Define font sizes and styles
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

        # Calculate text widths
        title_width = title_font.getlength(title)
        subtitle_width = subtitle_font.getlength(subtitle)

        # Calculate text heights
        title_height = 10
        subtitle_height = 10

        # Calculate text positions
        title_position = ((self.image_size - title_width) // 2,
                        (self.image_size - (title_height + subtitle_height)) // 2)
        subtitle_position = ((self.image_size - subtitle_width) // 2,
                            title_position[1] + title_height)

        # Draw text on the image
        draw.text(title_position, title, fill="black", font=title_font)
        draw.text(subtitle_position, subtitle, fill="black", font=subtitle_font)
        image.save("out.png")
        return image
    
    def create_cover_image(self, title, subtitle, offset = (0,0,0), negate=False):
        image = self._create_title_image(title, subtitle)
        if negate:
            image = PIL.ImageOps.invert(image)
        self.add_image(image, monochrome=True, offset=offset)
