
from __future__ import print_function

import os
import numpy as np
import argparse

from PIL import ImageFont, ImageDraw, Image, ImageColor
from create_mask import create_mask


def draw_text(draw, mask, txt, font, ignore=None):
    cc = 0
    for i in range(mask.size[1]):
        for j in range(mask.size[0]):
            r,g,b = mask.getpixel((j,i))
            if ignore is not None and (r,g,b) == ignore:
                continue
            draw.text((dx*j, dy*i), txt[cc], font=font, fill=(r,g,b,255))
            cc += 1
    return cc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='char repeat')
    parser.add_argument('mask', help='mask text or path to a mask image')
    parser.add_argument('font', help='path to a font file (e.g. SourceCodePro-Black.ttf)')
    parser.add_argument('-t', dest='text', default='', help='the text to fill the mask')
    parser.add_argument('-s', dest='font_size', default=16, type=int,
                        help='size of the font')
    parser.add_argument('-i', dest='ignore', default='black', help='no fill color')
    parser.add_argument('-c', dest='bg_color', default='black', help='background color')
    parser.add_argument('-a', dest='alpha', default=255, type=int,
                              help='alpha value of background')
    parser.add_argument('-p', action='store_true', dest='plot', help='show image')
    param = parser.parse_args()

    # initialize font
    font = ImageFont.truetype(param.font, param.font_size)
    dx, dy = font.getsize('A')

    # create mask    
    if os.path.isfile(param.mask):
        mask = Image.open(param.mask)
    else:
        mask = create_mask(param.mask, param.font, param.font_size*5)
    
    mask = mask.resize((mask.size[0], int(float(dx)/dy*mask.size[1]+0.5)))

    # prepare fill text
    sz = mask.size[0]*mask.size[1]
    if len(param.text) == 0:
        np.random.seed(42)
        txt = ''.join([str(np.random.randint(10)) for j in range(sz)])
    elif os.path.isfile(param.text):
        with open(param.text, 'r') as fp:
            txt = ''.join(fp.readlines()).replace('\n', '')
    else:
        txt = param.text
    
    # make sure the text is long enough
    while len(txt) < sz:
        txt += txt

    # get the background color
    try:
        bg_color = ImageColor.getrgb(param.bg_color)
    except ValueError:
        print('Warning: Wrong format or not a valid background color!')
        bg_color = ImageColor.getrgb('black')
        
    ignore = None
    if len(param.ignore) > 0:
        try:
            ignore = ImageColor.getrgb(param.ignore)
        except ValueError:
            print('Warning: Wrong format or not a valid no fill color!')
        
    # create image
    img = Image.new('RGBA', (mask.size[0]*dx, mask.size[1]*dy))
    img.putalpha(param.alpha)

    draw = ImageDraw.Draw(img)
    draw.rectangle((0,0,img.size[0],img.size[1]), fill=bg_color)

    draw_text(draw, mask, txt, font, ignore)
    img.save('image.png')
    
    if param.plot:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.imshow(img)
        plt.title('%s (%i x %i)' % (param.mask, img.size[0], img.size[1]))
        plt.show()

