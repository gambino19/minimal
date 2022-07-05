# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 22:18:25 2022

@author: micha
"""


from os.path import abspath, dirname
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from colour import Color
import numpy as np

from minimal.display import Canvas
from minimal.objects import Line, Image

# canvas = Canvas(800, 800, fps=60, bg=Color(hex="#FFFFFF"))

img = Image('jasmine.jpg')