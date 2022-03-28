from io import BytesIO
from django.core.files import File
from PIL import Image
from django.conf import settings


def add_watermark(image):
    """Resize user avatar and Add watermark"""
    if not image:
        image = settings.SAMPLE_IMAGE
        name = "sample.png"
    else:
        name = image.name

    im = Image.open(image)
    im.convert('RGB')
    im.thumbnail((settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH))
    image_io = BytesIO()

    watermark = Image.open(settings.WATERMARK_IMAGE_PATH)
    watermark.convert('RGB')
    watermark.thumbnail((100, 100))

    im.paste(watermark, (im.width - watermark.width, im.height - watermark.height))

    im.save(image_io, 'PNG', quality=100)

    avatar = File(image_io, name=name)

    return avatar
