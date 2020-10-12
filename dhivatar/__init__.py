#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Code modified from maethor's avatar-generator 
# Github: https://github.com/maethor/avatar-generator


import os
from random import randint, seed
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np

__all__ = ['Avatar']

class Avatar(object):
    MIN_RENDER_SIZE = 512

    @classmethod
    def generate(cls, string, size=150, bg_color=None, font_color = (255, 255, 255), font_name="Mv_Eamaan_XP.otf", filetype="PNG", circular=False):
        render_size = max(size, Avatar.MIN_RENDER_SIZE)
        if not bg_color:
            bg_color = cls._background_color(string)
        image = Image.new('RGB', (render_size, render_size), bg_color)
        draw = ImageDraw.Draw(image)
        font = cls._font(render_size, font_name)
        text = cls._text(string)
        draw.text(cls._text_position(render_size, text, font),
                  text,
                  fill=font_color,
                  font=font)
        stream = BytesIO()
        image = image.resize((size, size), Image.ANTIALIAS)
        image.save(stream, format=filetype, optimize=True)
        path = os.path.join(os.path.dirname(__file__), 'generated',f"{string}.png")
        image.save(path, optimize=True)
        if circular:
            cls._to_circle(path, string)
        return stream.getvalue()

    @staticmethod
    def _background_color(s):
        seed(s)
        r = g = b = 255
        while r + g + b > 255*2:
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
        return (r, g, b)

    @staticmethod
    def _font(size, font_name):
        path = os.path.join(os.path.dirname(__file__), 'data', font_name)
        return ImageFont.truetype(path, size=int(0.8 * size))

    @staticmethod
    def _text(string):
        if len(string) == 0:
            return "#"
        elif " " in string:
            return string.split()[1][0]
        else:
            return string[0]

    @staticmethod
    def _text_position(size, text, font):
        width, _ = font.getsize(text)
        left = (size - width) / 2.0
        top = -50 #Don't ask me about this. I don't know why.
        return left, top

    @staticmethod
    def _to_circle(img_path, string):
        #Code from: https://stackoverflow.com/questions/51486297/cropping-an-image-in-a-circular-way-using-python
        img=Image.open(img_path).convert("RGB")
        npImage=np.array(img)
        h,w=img.size

        # Create same size alpha layer with circle
        alpha = Image.new('L', img.size,0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0,0,h,w],0,360,fill=255)

        # Convert alpha Image to numpy array
        npAlpha=np.array(alpha)

        # Add alpha layer to RGB
        npImage=np.dstack((npImage,npAlpha))

        # Save with alpha
        path = os.path.join(os.path.dirname(__file__), 'generated',f"circular_{string}.png")
        Image.fromarray(npImage).save(path)
