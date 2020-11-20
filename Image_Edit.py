from PIL import Image, ImageDraw
import os


def welcome_image(image, member_id):
    im1 = Image.open('assets/welcome.jpg')
    im2 = Image.open(image)

    back_im = im1.copy()
    scale = 1

    for i in range(100, 0, -5):
        scale = i / 100
        print(scale)
        if int(im2.size[0] * scale) <= 153:
            scale = (i + 5) / 100
            break

    width = int(im2.size[0] * scale)
    height = int(im2.size[1] * scale)
    dimension = (width, height)

    resized = im2.resize(dimension)
    resized.convert('RGB')
    resized_name = image[:-11] + 'resized.jpg'
    resized.save(resized_name)

    im3 = Image.open(resized_name)

    mask_im = Image.new("L", im3.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((12, 11, 148, 147), fill=255)
    mask_file = (image[:-11] + '-mask.jpg')
    mask_im.save(mask_file, quality=95)
    back_im.paste(im3, (105, 12), mask_im)
    final_image = (image[:-11] + '-final.jpg')
    back_im.save(final_image, quality=95)
    os.remove(resized_name)
    os.remove(mask_file)
    return final_image
