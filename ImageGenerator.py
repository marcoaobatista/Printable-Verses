from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

OUTPUT_FOLDER_NAME = "output-images"

# Image specifications
IMAGE_WIDTH = 1200  # Image width in pixels
IMAGE_HEIGHT = 600  # Image height in pixels
IMAGE_PADDING = (32, 64)  # Padding (left/right, top/bottom)
TEXT_GAP = 56 # Gap between title and body

# Title font specifications
TITLE_FONT_NAME = "Inter-Bold.ttf"
TITLE_FONT_SIZE = 46

# Body font specifications
BODY_FONT_NAME = "Inter-Regular.ttf"
BODY_FONT_SIZE = 38

# Text and background colors
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

BODY_LINE_HEIGHT = 1.5

class ImageGenerator:

    def generate_image(self, verse_ref: str, verse_text: str):

        # Load title font and body font
        try:
            title_font = ImageFont.truetype("fonts/"+TITLE_FONT_NAME, TITLE_FONT_SIZE)
        except IOError:
            title_font = ImageFont.load_default()
            print("Title font not found. Using default font.")

        try:
            body_font = ImageFont.truetype("fonts/"+BODY_FONT_NAME, BODY_FONT_SIZE)
        except IOError:
            body_font = ImageFont.load_default()
            print("Body font not found. Using default font.")

        # Calculate the height of the title text
        title_bbox = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), verse_ref, font=title_font)
        title_height = title_bbox[3] - title_bbox[1]

        # Wrap the body text and calculate the total height
        max_body_width = IMAGE_WIDTH - 2 * IMAGE_PADDING[0]
        wrapped_text = textwrap.fill(verse_text, width=65)
        body_lines = wrapped_text.split('\n')
        line_height = int(1.5 * body_font.size)
        body_height = line_height * len(body_lines)

        # Calculate the required image height
        total_height = 2 * IMAGE_PADDING[1] + title_height + TEXT_GAP + body_height

        # Create the image with the calculated height
        image = Image.new("RGB", (IMAGE_WIDTH, total_height), color=BACKGROUND_COLOR)
        draw = ImageDraw.Draw(image)

        # Center the title text and draw it
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (IMAGE_WIDTH - title_width) // 2
        title_y = IMAGE_PADDING[1]
        draw.text((title_x, title_y), verse_ref, font=title_font, fill=TEXT_COLOR)

        # Draw each line of the body text
        body_y = title_y + title_height + TEXT_GAP
        for line in body_lines:
            line_width = draw.textbbox((0, 0), line, font=body_font)[2]
            line_x = (IMAGE_WIDTH - line_width) // 2
            draw.text((line_x, body_y), line, font=body_font, fill=TEXT_COLOR)
            body_y += line_height

        # Create the directory
        os.makedirs(OUTPUT_FOLDER_NAME, exist_ok=True)

        # Save the image
        image.save(OUTPUT_FOLDER_NAME+"/"+verse_ref+".png", format="PNG", quality=100)
        print(f"Image saved as {verse_ref}.png")