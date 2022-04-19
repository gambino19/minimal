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


# # Petals
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

# for petal in [petal1, petal2, petal3, petal4, petal5]:
#     line = Line(segments=petal, div=100)
#     line.noise((0,0))
#     canvas.add(line)

# # # Stem
# stemleft = [(465, 580), (462, 556), (455, 528), (450, 503), (440, 477), (432, 450),
#   (426, 422), (421, 401), (413, 374), (404, 348), (397, 334), (384, 327)]
# stemright = [(500, 651), (495, 629), (494, 602), (489, 576), (487, 548), (484, 529), 
#               (478, 503), (476, 482), (469, 460), (462, 438), (456, 409), (449, 386), 
#               (442, 364), (435, 343), (441, 322), (449, 296)]

# for stem in [stemleft, stemright]:
#     line = Line(segments=stem, div=100)
#     line.noise((0,0))
#     canvas.add(line)

# # Leaf
# leafleft = [(463, 583), (448, 555), (433, 536), (413, 517), (394, 501), (370, 480), 
#             (351, 461), (337, 442), (323, 420), (309, 403), (301, 422), (305, 446), 
#             (306, 485), (310, 509), (317, 543), (327, 574), (343, 602), (357, 623), 
#             (372, 645), (388, 675), (412, 696), (434, 721), (448, 744), (466, 772)]
# leafleftmiddle = [(489, 688), (470, 653), (459, 613), (447, 589), (427, 559), 
#                   (410, 535), (395, 520), (380, 508), (367, 489), (349, 472), 
#                   (335, 451), (322, 427), (309, 406)]
# leafright = [(479, 502), (497, 477), (512, 451), (527, 422), (535, 402), (548, 378),
#               (556, 347), (561, 315), (566, 287), (573, 260), (573, 224), (594, 235), 
#               (608, 256), (620, 298), (627, 329), (631, 361), (633, 393), (631, 433), 
#               (628, 473), (620, 517), (608, 552), (592, 586), (579, 626), (562, 661), 
#               (545, 688), (529, 710), (519, 731), (528, 753)]
# leafrightmiddle = [(488, 687), (496, 665), (505, 639), (518, 614), (529, 590), 
#                     (539, 563), (548, 538), (560, 508), (566, 478), (573, 453), 
#                     (583, 423), (588, 387), (592, 362), (595, 334), (594, 308), 
#                     (593, 277), (585, 257), (575, 227)]

# for leaf in [leafleft, leafleftmiddle, leafright, leafrightmiddle]:
#     line = Line(segments=leaf, div=100)
#     line.noise((0,0))
#     canvas.add(line)

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


# Left Leaf

segments = []
alphas = []
line_widths = []

# Bottom

b1 = [(451, 745), (443, 736), (437, 726), (433, 719), (427, 710), (421, 700), 
      (417, 694), (409, 684), (403, 675), (397, 667), (392, 662), (387, 655), 
      (377, 648), (372, 639), (367, 634), (357, 625), (353, 614), (346, 608), 
      (339, 598), (332, 589)]
shades, alphas, line_widths = repeated_shader(b1, "[i-1.5*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=1, line_width=1)

b2 = [(336, 594), (330, 575), (327, 568), (325, 554), (323, 544), (320, 532), 
      (317, 519), (314, 508), (310, 497), (309, 487)]
shades, alphas, line_widths = repeated_shader(b2, "[i-1.5*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.8, line_width=0.8)

b3 = [(307, 482), (307, 470), (307, 454), (306, 443), (304, 429), (304, 415), (306, 410)]
shades, alphas, line_widths = repeated_shader(b3, "[i-1*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=1, line_width=1)

b4 = [(473, 736), (464, 722), (454, 710), (448, 700), (440, 689), (431, 675), 
      (422, 662), (416, 655), (410, 649)]
shades, alphas, line_widths = repeated_shader(b4, "[i-2*i,i-0.5*i]", (0, 30, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.2, line_width=1)

b5 = [(409, 649), (401, 639), (393, 629), (385, 621), (378, 612), (372, 605), 
      (366, 596), (359, 586), (348, 574)]
shades, alphas, line_widths = repeated_shader(b5, "[i-2*i,i-0.5*i]", (0, 60, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.05, line_width=1)

b6 = [(346, 567), (341, 554), (338, 543), (336, 528), (332, 518), (331, 509), 
      (327, 499), (325, 490)]
shades, alphas, line_widths = repeated_shader(b6, "[i-2*i,i-0.5*i]", (0, 30, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.05, line_width=1)
b7 = [(333, 502), (330, 496), (328, 485), (325, 477), (322, 465), (319, 457), 
      (319, 449), (316, 438), (315, 430), (315, 423)]
shades, alphas, line_widths = repeated_shader(b7, "[i-1.25*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.6, line_width=1)

b8 = [(447, 617), (441, 605), (433, 595), (427, 588), (421, 578), (417, 571), 
      (411, 563), (404, 550), (398, 542), (392, 536), (386, 528), (377, 517), 
      (374, 513), (367, 504), (361, 499), (357, 494), (354, 489), (345, 481), 
      (341, 475), (336, 470)]
shades, alphas, line_widths = repeated_shader(b8, "[i-1.25*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.4, line_width=1)

b9 = [(393, 574), (383, 561), (376, 554), (370, 545), (364, 539), (357, 531), 
      (352, 523), (346, 514)]
shades, alphas, line_widths = repeated_shader(b9, "[i-1.25*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.15, line_width=1)

b10 = [(380, 624), (375, 617), (369, 611), (363, 604), (359, 596), (353, 590), 
        (350, 584), (345, 576)]
shades, alphas, line_widths = repeated_shader(b10, "[i-1.25*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.15, line_width=1)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)


# Top

segments = []
alphas = []
line_widths = []

t1 = [(487, 688), (482, 675), (478, 667), (473, 656), (468, 643), (466, 636), 
      (463, 625), (460, 615), (456, 605), (452, 597), (448, 591)]
shades, alphas, line_widths = repeated_shader(t1, "[i-1.25*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.5, line_width=1)

t2 = [(447, 585), (442, 578), (436, 572), (431, 563), (426, 557), (422, 547), 
      (419, 543), (415, 537), (406, 529)]
shades, alphas, line_widths = repeated_shader(t2, "[i-1.25*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.25, line_width=1)

t3 = [(408, 531), (405, 527), (396, 520), (389, 514), (387, 511), (381, 505), (377, 499)]
shades, alphas, line_widths = repeated_shader(t3, "[i-1.25*i,i-0.5*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.15, line_width=1)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)

# Stem

segments = []
alphas = []
line_widths = []


s1 = [(403, 343), (409, 359), (414, 374), (418, 390), (421, 403), (426, 415), 
      (429, 429), (433, 449), (437, 461), (441, 474), (444, 488), (450, 503), 
      (453, 518), (456, 531), (460, 550), (463, 564), (464, 577), (465, 593)]
shades, alphas, line_widths = repeated_shader(s1, "[i-1.25*i,i-0.5*i]", (0, 10, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.6, line_width=1)

s2 = [(464, 572), (466, 585), (472, 595), (477, 608), (478, 617), (480, 631)]
shades, alphas, line_widths = repeated_shader(s2, "[i-1.25*i,i-0.5*i]", (0, 10, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.4, line_width=1)

s3  = [(411, 339), (414, 354), (421, 372), (422, 383), (425, 395), (433, 410), 
        (434, 423), (438, 438), (444, 455), (446, 469), (452, 485), (457, 498), 
        (461, 513), (465, 525), (469, 544), (472, 555), (474, 565), (476, 579), 
        (478, 589)]
shades, alphas, line_widths = repeated_shader(s3, "[i-1.5*i,i-0.5*i]", (0, 30, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.05, line_width=1)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)

# Petals

#Left 

segments = []
alphas = []
line_widths = []

p1 = [(306, 316), (295, 313), (286, 308), (273, 302), (259, 295), (245, 284), 
      (236, 276), (226, 263), (216, 252), (208, 240), (203, 229), (198, 221), 
      (192, 213), (186, 200), (178, 180), (175, 171), (171, 161), (168, 151), (166, 147)]
shades, alphas, line_widths = repeated_shader(p1, "[i-1.25*i,i-0.5*i]", (0, 7, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.85, line_width=1)

p2 = [(295, 302), (286, 299), (275, 296), (260, 289), (249, 281), (243, 272), 
      (233, 262), (229, 254)]
shades, alphas, line_widths = repeated_shader(p2, "[i-1.5*i,i-0.5*i]", (0, 15, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.35, line_width=1)

p3 = [(308, 296), (298, 291), (285, 284), (275, 277), (265, 271), (259, 266), 
      (251, 257), (245, 250), (235, 242), (227, 231), (220, 220), (214, 208), 
      (208, 194), (202, 177), (195, 165)]
shades, alphas, line_widths = repeated_shader(p3, "[i-1.5*i,i-0.5*i]", (0, 2, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.4, line_width=1)

p4 = [(403, 322), (391, 323), (377, 324), (368, 324), (358, 324), (343, 321), 
      (335, 321), (322, 318)]
shades, alphas, line_widths = repeated_shader(p4, "[i-0.75*i,i-0.5*i]", (0, 10, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.8, line_width=1)

p5 = [(372, 320), (360, 317), (351, 312), (341, 304), (335, 299)]
shades, alphas, line_widths = repeated_shader(p5, "[i-0.25*i,i-0.5*i]", (0, 10, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.8, line_width=1)

p6 = [(272, 243), (262, 234), (254, 225), (248, 217), (241, 210), (234, 200), 
      (229, 191), (222, 184), (218, 173), (212, 160)]
shades, alphas, line_widths = repeated_shader(p6, "[i-0.25*i,i-0.5*i]", (0, 2, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.25, line_width=1)

p7 = [(343, 300), (335, 292), (327, 285), (320, 280), (314, 276), (302, 264), (294, 253)]
shades, alphas, line_widths = repeated_shader(p7, "[i-0.25*i,i-0.5*i]", (0, 10, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.4, line_width=1)

p8 = [(286, 235), (280, 226), (272, 215), (263, 201), (259, 188), (255, 179), 
      (249, 169), (246, 160), (240, 145), (235, 128)]
shades, alphas, line_widths = repeated_shader(p8, "[i-2.5*i,i-0.5*i]", (0, 5, 1), 
                                              segments, alphas, line_widths,
                                              alpha=1, line_width=1, random_cond=(-5, 5))

pall = [(397, 327), (390, 327), (379, 327), (370, 327), (355, 327), (341, 326), 
        (328, 323), (315, 320), (296, 317), (284, 311), (267, 305), (260, 301), 
        (252, 295), (242, 288), (236, 282), (230, 276), (222, 268), (214, 256), 
        (208, 246), (202, 239), (197, 226), (188, 212), (181, 197), (178, 183), 
        (174, 172), (168, 156), (164, 145), (163, 133), (161, 120), (161, 105)]
shades, alphas, line_widths = repeated_shader(pall, "[i-2*i,i-0.5*i]", (0, 60, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.05, line_width=1)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)

# Back Left

segments = []
alphas = []
line_widths = []

p1 = [(257, 157), (253, 146), (251, 136), (247, 125), (245, 115), (243, 102), 
      (240, 91), (238, 80), (237, 76), (236, 69)]
shades, alphas, line_widths = repeated_shader(p1, "[i-0.25*i,i-0.5*i]", (0, 10, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.3, line_width=1)

p2 = [(232, 113), (230, 106), (229, 98), (228, 95), (226, 89)]
shades, alphas, line_widths = repeated_shader(p2, "[i+0.25*i,i-0.5*i]", (0, 10, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.3, line_width=1)

p3 = [(259, 137), (254, 125), (251, 115), (249, 105), (247, 97), (245, 89), (243, 83)]
shades, alphas, line_widths = repeated_shader(p3, "[i-2.5*i,2*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.3, line_width=1)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)

# Right

segments = []
alphas = []
line_widths = []

p1 = [(489, 255), (489, 243), (489, 230), (484, 215), (480, 203), (478, 194), 
      (473, 186), (467, 174), (459, 162), (456, 152), (450, 138), (445, 128), 
      (439, 114), (432, 102), (423, 91), (418, 86), (409, 76)]
shades, alphas, line_widths = repeated_shader(p1, "[i-1.25*i,2*i]", (0, 40, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.1, line_width=1)

p2 = [(462, 280), (471, 273), (478, 261), (484, 252), (489, 245), (493, 237), 
      (501, 225), (505, 219), (511, 207)]
shades, alphas, line_widths = repeated_shader(p2, "[i,i-2*i]", (0, 20, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.4, line_width=1) 

p3 = [(484, 229), (484, 221), (481, 208), (477, 197), (472, 183)]
shades, alphas, line_widths = repeated_shader(p3, "[i-1.5*i,i]", (0, 40, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.275, line_width=1) 

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)

# Back Right

segments = []
alphas = []
line_widths = []

p1 = [(316, 72), (313, 64), (308, 60), (302, 53), (293, 51)]
shades, alphas, line_widths = repeated_shader(p1, "[i-2.25*i,0.75*i]", (0, 40, 2), 
                                              segments, alphas, line_widths,
                                              alpha=0.3, line_width=1)

p2 = [(387, 61), (390, 51), (390, 41), (390, 30), (386, 20)]
shades, alphas, line_widths = repeated_shader(p2, "[i-2*i,i-2*i]", (0, 20, 2), 
                                              segments, alphas, line_widths,
                                              alpha=0.3, line_width=1)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)

# Middle

segments = []
alphas = []
line_widths = []

p1 = [(439, 305), (434, 305), (424, 305), (416, 305), (411, 305), (402, 305), 
      (393, 305), (383, 303), (372, 301), (363, 299), (350, 295), (340, 290)]
shades, alphas, line_widths = repeated_shader(p1, "[0,0.25*i]", (0, 40, 2), 
                                              segments, alphas, line_widths,
                                              alpha=0.3, line_width=1)

p2 = [(381, 285), (366, 281), (353, 275), (339, 268), (328, 259), (315, 246), 
      (304, 236), (295, 223), (283, 209), (275, 198), (268, 184)]
shades, alphas, line_widths = repeated_shader(p2, "[i-2*i,0.25*i]", (0, 40, 2), 
                                              segments, alphas, line_widths,
                                              alpha=0.2, line_width=1)

p3 = [(344, 221), (332, 211), (324, 197), (315, 180), (307, 163), (300, 152), 
      (297, 135), (294, 116)]
shades, alphas, line_widths = repeated_shader(p3, "[i-4*i,0.25*i]", (0, 20, 2), 
                                              segments, alphas, line_widths,
                                              alpha=0.2, line_width=1)

p4 = [(426, 264), (425, 245), (422, 221), (417, 204), (413, 175), (408, 155), 
      (400, 134), (387, 104)]
shades, alphas, line_widths = repeated_shader(p4, "[i-2*i,0.25*i]", (0, 30, 2), 
                                              segments, alphas, line_widths,
                                              alpha=0.3, line_width=1)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)


# Petal Outline

segments = []
alphas = []
line_widths = []

p1 = [(265, 173), (269, 152), (270, 132), (274, 117), (281, 101), (293, 86), (305, 81)]
shades, alphas, line_widths = repeated_shader(p1, "[i+1*i,0.25*i]", (0, 5, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.6, line_width=1)

p2 = [(443, 139), (433, 128), (428, 121), (421, 110), (414, 97), (407, 90), 
      (398, 80), (393, 73), (384, 69)]
shades, alphas, line_widths = repeated_shader(p2, "[i-1*i,0.25*i]", (0, 7, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.6, line_width=1)

p3 = [(416, 76), (416, 66), (419, 52), (422, 40), (428, 30), (432, 22)]
shades, alphas, line_widths = repeated_shader(p3, "[i-1*i,0.25*i]", (0, 7, 1), 
                                              segments, alphas, line_widths,
                                              alpha=0.6, line_width=1)

p4 = [(238, 141), (230, 130), (220, 126), (204, 121), (192, 119), (178, 119), (169, 119)]
shades, alphas, line_widths = repeated_shader(p4, "[i-1*i,0.25*i]", (0, 21, 3), 
                                              segments, alphas, line_widths,
                                              alpha=0.6, line_width=1)

for segment, alpha, line_width in zip(segments, alphas, line_widths):
    line = Line(segments=segment, div=30, alpha=alpha, line_width=line_width)
    line.noise((0,0))
    canvas.add(line)

# canvas.add(img, index=0)

for obj in canvas.order.items:
    if isinstance(obj, Line):
        obj.noise((10,10))
        obj.repeat(random=True)
canvas.show(inspect=True)