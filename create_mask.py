
from __future__ import print_function

import argparse
from PIL import ImageFont, ImageDraw, Image


def create_mask(text, font_type, font_size=84):
    '''
    Creates an image with the given text in it.
    '''
    # initialize fond with given size
    font = ImageFont.truetype(font_type, font_size)
    dx, dy = font.getsize(text)

    # draw the text to the image
    mask = Image.new('RGB', (dx, max(dy, font_size)))
    draw = ImageDraw.Draw(mask)
    draw.text((0,-int(0.15*font_size)), text, font=font) 
    
    return mask


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a mask for char repeat')
    parser.add_argument('text', help='the text to print on the image')
    parser.add_argument('font', help='select a font (e.g. SourceCodePro-Black.ttf)')
    parser.add_argument('-s', dest='font_size', default=84, type=int,
                        help='size of the font')
    parser.add_argument('-p', action='store_true', dest='plot', help='show image')
    param = parser.parse_args()
    
    mask = create_mask(param.text, param.font, param.font_size)
    mask.save('mask_%s.png' % param.text)

    if param.plot:
        dx, dy = mask.size
        import matplotlib.pyplot as plt
        plt.figure()
        plt.imshow(mask)
        plt.title('text: %s (mask size = %i x %i)' % (param.text, dx, dy))
        plt.show()
    

