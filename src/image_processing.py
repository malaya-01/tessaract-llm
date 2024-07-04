import io
from PIL import Image, ImageFont, ImageDraw
import pytesseract
from config import TESSERACT_CMD

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def text_to_image_and_extract(combined_text):
    lines = combined_text.split('\n')
    width, height = 1000, 20 * (len(lines) + 1)
    im = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(im)
    font = ImageFont.load_default()
    y = 10
    for line in lines:
        d.text((10, y), line, font=font, fill=(0, 0, 0))
        y += 20
    del d
    buffer = io.BytesIO()
    im.save(buffer, format="JPEG")
    buffer.seek(0)
    return pytesseract.image_to_string(Image.open(buffer)), buffer
