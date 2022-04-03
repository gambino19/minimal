# -*- coding: utf-8 -*-
"""
Tulip Case Study
"""

from os.path import abspath, dirname
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from colour import Color
import numpy as np

from minimal.display import Canvas
from minimal.objects import Line, Image


canvas = Canvas(800, 800, fps=60, bg=Color(hex="#FFFFFF"))

img = Image("./tulip.jpg", position=(150,0))
img.resize((500,800))
# canvas.add(img)

# Petals
petal1 = [(394, 323), (366, 329), (336, 325), (303, 318), (269, 304), (251, 288),
  (232, 273), (217, 252), (203, 233), (191, 209), (182, 187), (173, 163), (166, 137),
  (164, 107), (171, 98), (185, 107), (195, 102), (215, 104), (232, 115), (243, 131),
  (256, 165), (266, 191), (276, 221), (297, 242)]
petal2 = [(194, 105), (192, 91), (201, 83), (213, 76), (221, 65), (232, 49),
  (258, 44), (271, 44), (293, 49), (305, 60), (313, 76)]
petal3=[(257, 167), (260, 133), (263, 108), (278, 86), (293, 75), (311, 69),
  (335, 65), (347, 60), (365, 58), (384, 60), (401, 66), (416, 81), (426, 98),
  (443, 122), (450, 140), (459, 159), (473, 183), (480, 206), (486, 226), (487, 254)]
petal4 = [(296, 49), (302, 30), (315, 26), (327, 17), (344, 11), (367, 9),
  (383, 19), (402, 16), (415, 25)]
petal5 = [(443, 302), (462, 283), (477, 266), (496, 241), (509, 209), (512, 183),
  (509, 151), (502, 121), (489, 98), (474, 71), (455, 48), (438, 24), (423, 16),
  (415, 28), (409, 47), (409, 73)]

for petal in [petal1, petal2, petal3, petal4, petal5]:
    line = Line(segments=petal, div=100)
    line.noise((0,0))
    canvas.add(line)

# Stem
stemleft = [(465, 580), (462, 556), (455, 528), (450, 503), (440, 477), (432, 450),
  (426, 422), (421, 401), (413, 374), (404, 348), (397, 334), (384, 327)]
stemright = [(500, 651), (495, 629), (494, 602), (489, 576), (487, 548), (484, 529), 
              (478, 503), (476, 482), (469, 460), (462, 438), (456, 409), (449, 386), 
              (442, 364), (435, 343), (441, 322), (449, 296)]

for stem in [stemleft, stemright]:
    line = Line(segments=stem, div=100)
    line.noise((0,0))
    canvas.add(line)

# Leaf
leafleft = [(463, 583), (448, 555), (433, 536), (413, 517), (394, 501), (370, 480), 
            (351, 461), (337, 442), (323, 420), (309, 403), (301, 422), (305, 446), 
            (306, 485), (310, 509), (317, 543), (327, 574), (343, 602), (357, 623), 
            (372, 645), (388, 675), (412, 696), (434, 721), (448, 744), (466, 772)]
leafleftmiddle = [(489, 688), (470, 653), (459, 613), (447, 589), (427, 559), 
                  (410, 535), (395, 520), (380, 508), (367, 489), (349, 472), 
                  (335, 451), (322, 427), (309, 406)]
leafright = [(479, 502), (497, 477), (512, 451), (527, 422), (535, 402), (548, 378),
              (556, 347), (561, 315), (566, 287), (573, 260), (573, 224), (594, 235), 
              (608, 256), (620, 298), (627, 329), (631, 361), (633, 393), (631, 433), 
              (628, 473), (620, 517), (608, 552), (592, 586), (579, 626), (562, 661), 
              (545, 688), (529, 710), (519, 731), (528, 753)]
leafrightmiddle = [(488, 687), (496, 665), (505, 639), (518, 614), (529, 590), 
                    (539, 563), (548, 538), (560, 508), (566, 478), (573, 453), 
                    (583, 423), (588, 387), (592, 362), (595, 334), (594, 308), 
                    (593, 277), (585, 257), (575, 227)]

for leaf in [leafleft, leafleftmiddle, leafright, leafrightmiddle]:
    line = Line(segments=leaf, div=100)
    line.noise((0,0))
    canvas.add(line)

# Shading Leaf Right
segments = []
alphas = []
line_widths = []

def repeated_shader(base, repeat_cond, range_args, 
                    segments, alphas, line_widths,
                    alpha=1, line_width=1, random_cond=(-10, 10)):
    """ DOCSTRING """
    
    base = np.array(base)
    
    for i in range(*range_args):
        _base = base.copy()
        placement = np.array(eval(repeat_cond))
        random = np.random.randint(*random_cond, size=2)
        
        _base = _base - placement + random
    
        segments.append(_base.tolist())
        alphas.append(alpha)
        line_widths.append(line_width)
    
    return segments, alphas, line_widths

#TODO: Lets functionalize this!

# Top Right

l1 = [(501, 651), (503, 641), (507, 635), (511, 629), (512, 626), (515, 617), (518, 612)]

shades, alphas, line_widths = repeated_shader(l1, "[i-0.7*i,i+i]", (0, 66, 2), 
                                              segments, alphas, line_widths,
                                              alpha=1, line_width=1.5)

l2 = [(503, 646), (505, 641), (510, 635), (513, 626), (517, 617), (519, 609), 
        (523, 602), (526, 596), (528, 588), (533, 578)]

shades, alphas, line_widths = repeated_shader(l2, "[i-0.7*i,i+i]", (0, 70, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.75, line_width=1)
    
l3 = [(535, 573), (537, 563), (539, 557), (542, 549), (545, 541), (548, 535), 
          (551, 528), (555, 521), (559, 512)]

shades, alphas, line_widths = repeated_shader(l3, "[i-0.7*i,i+i]", (0, 60, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.65, line_width=0.8)
    
l4 = [(562, 492), (566, 480), (569, 470), (573, 460), (576, 449), (580, 438), (583, 427)]
shades, alphas, line_widths = repeated_shader(l4, "[i-0.7*i,i+i]", (0, 53, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.55, line_width=0.65)

l5 = [(587, 399), (588, 384), (590, 368), (593, 354), (596, 341)]
shades, alphas, line_widths = repeated_shader(l5, "[i-0.7*i,i+i]", (0, 53, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.45, line_width=0.5)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)

# Bottom Right

segments = []
alphas = []
line_widths = []

b1 = [(520, 722), (527, 713), (533, 702), (539, 693), (547, 681), (553, 669), 
      (561, 656), (566, 643), (571, 633), (575, 625), (578, 611), (582, 603), (587, 590)]

shades, alphas, line_widths = repeated_shader(b1, "[i-0.4*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=1, line_width=1)

b2 = [(509, 711), (518, 698), (521, 690), (526, 681), (532, 670), (538, 661), 
      (543, 652), (548, 641), (552, 633), (556, 624), (560, 611), (564, 604), 
      (568, 593), (571, 586), (576, 576)]
shades, alphas, line_widths = repeated_shader(b2, "[i-0.4*i,i-0.5*i]", (0, 40, 2), 
                                              segments, alphas, line_widths,
                                              alpha=0.4, line_width=0.4)

b3 = [(592, 585), (601, 572), (607, 556), (609, 536), (614, 519), (622, 499), 
      (626, 477), (630, 463)]
shades, alphas, line_widths = repeated_shader(b3, "[i-0.4*i,i-0.5*i]", (0, 30, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.7, line_width=0.7)

b4 = [(571, 573), (576, 560), (583, 546), (587, 535), (591, 519), (595, 505), 
      (601, 488), (604, 475), (607, 464), (610, 453)]
shades, alphas, line_widths = repeated_shader(b4, "[i-0.4*i,i-0.5*i]", (0, 40, 2), 
                                              segments, alphas, line_widths,
                                              alpha=0.4, line_width=0.4)

b5 = [(630, 450), (630, 438), (630, 421), (630, 407), (631, 392), (630, 371), (629, 344)]
shades, alphas, line_widths = repeated_shader(b5, "[i-0.4*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.6, line_width=0.6)

b6 = [(611, 452), (611, 434), (612, 416), (613, 398), (614, 385), (615, 372), 
      (615, 362), (615, 348)]
shades, alphas, line_widths = repeated_shader(b6, "[i-0.4*i,i-0.5*i]", (0, 40, 2), 
                                              segments, alphas, line_widths,
                                              alpha=0.3, line_width=0.3)

b7 = [(630, 345), (625, 330), (622, 313), (618, 297), (614, 283), (610, 260)]
shades, alphas, line_widths = repeated_shader(b7, "[i-0.4*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.6, line_width=0.6)

b8 = [(607, 259), (599, 248), (590, 238), (583, 231), (575, 225)]
shades, alphas, line_widths = repeated_shader(b8, "[i-1.5*i,i-1.5*i]", (0, 10, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.6, line_width=0.6)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)

for obj in canvas.order.items:
    if isinstance(obj, Line):
        obj.noise((20,20))
        # obj.repeat(random=True)
canvas.show(inspect=True)