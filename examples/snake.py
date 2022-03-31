# -*- coding: utf-8 -*-
"""
Snake Plants Case Study
"""

from os.path import abspath, dirname
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from colour import Color
import numpy as np
from tqdm import tqdm

from minimal.display import Canvas, Frame
from minimal.objects import Line, Image

template = Image("./snake.png")
template.resize((500, 700))
template.rotate(0)
template.position = (100, 100)

canvas = Canvas(700, 900, bg=Color(hex="#000000"))

n = 75

def generate_pairs(leaf, n=100):
    pairs = []
    for _ in range(n):
        pairs.append((leaf[np.random.randint(0, len(leaf))], leaf[np.random.randint(0, len(leaf))]))
    return pairs

def add_leaf(pairs, colors, surface, n=100, scale=10, repeat=True, random=True, div=50):
    for pair in pairs:
        line = Line(pair[0], pair[1], div=div, color=Color(hex=colors[0]))
        line.noise(scale=scale, method="simplex")
        line.gradient(colors[1], div, (1, 0))
        if repeat:
            line.repeat(random=random)
        surface.add(line)

colors1 = ["#B7E4C7", "#D8F3DC"]
leaf1 = [(363, 799),
 (366, 770),
 (376, 741),
 (386, 716),
 (401, 688),
 (405, 655),
 (405, 627),
 (405, 600),
 (409, 571),
 (421, 543),
 (427, 503),
 (426, 475),
 (422, 437),
 (414, 464),
 (406, 487),
 (394, 513),
 (383, 539),
 (378, 569),
 (376, 605),
 (367, 642),
 (361, 681),
 (361, 715),
 (357, 737),
 (347, 770),
 (339, 801)]
pairs1 = generate_pairs(leaf1, n)

colors2 = ["#40916C", "#2D6A4F"]
leaf2 = [(323, 799),
 (321, 769),
 (322, 739),
 (321, 706),
 (319, 680),
 (315, 644),
 (322, 620),
 (328, 590),
 (339, 566),
 (351, 538),
 (351, 579),
 (357, 609),
 (362, 644),
 (362, 671),
 (361, 702),
 (356, 733),
 (350, 764),
 (341, 798)]
pairs2 = generate_pairs(leaf2, n)

colors3 = ["#52B788", "#74C69D"]
leaf3 = [(365, 647),
 (373, 617),
 (375, 588),
 (378, 550),
 (391, 517),
 (395, 481),
 (395, 436),
 (385, 403),
 (382, 356),
 (371, 386),
 (359, 427),
 (353, 464),
 (346, 491),
 (340, 528),
 (339, 559)]
pairs3 = generate_pairs(leaf3, n)

colors4 = ["#1B4332", "#081C15"]
leaf4 = [(299, 801),
 (302, 773),
 (310, 735),
 (314, 702),
 (319, 668),
 (321, 638),
 (323, 609),
 (332, 583),
 (330, 553),
 (332, 529),
 (334, 488),
 (340, 459),
 (331, 440),
 (326, 469),
 (315, 499),
 (312, 531),
 (303, 554),
 (290, 586),
 (284, 624),
 (281, 656),
 (275, 685),
 (272, 715),
 (276, 743),
 (280, 769),
 (283, 797)]
pairs4 = generate_pairs(leaf4, n)

colors5 = colors2
leaf5 = [(252, 800),
 (257, 775),
 (264, 742),
 (272, 712),
 (277, 688),
 (281, 653),
 (284, 624),
 (289, 599),
 (297, 571),
 (305, 549),
 (310, 511),
 (320, 480),
 (322, 450),
 (322, 423),
 (322, 387),
 (309, 413),
 (289, 443),
 (272, 473),
 (270, 509),
 (259, 541),
 (251, 568),
 (247, 599),
 (239, 627),
 (234, 656),
 (234, 686),
 (235, 713),
 (237, 740),
 (232, 767),
 (235, 797)]
pairs5 = generate_pairs(leaf5, n)

colors6 = colors1
leaf6 = [(322, 459),
 (327, 442),
 (332, 419),
 (336, 399),
 (339, 376),
 (338, 351),
 (333, 326),
 (329, 300),
 (328, 275),
 (320, 248),
 (308, 229),
 (297, 212),
 (291, 199),
 (292, 229),
 (290, 253),
 (285, 280),
 (281, 318),
 (288, 353),
 (288, 379),
 (283, 410),
 (281, 449)]
pairs6 = generate_pairs(leaf6, n)

colors7 = colors3
leaf7 = [(236, 626),
 (242, 598),
 (247, 567),
 (253, 541),
 (264, 516),
 (263, 485),
 (260, 457),
 (263, 433),
 (267, 403),
 (268, 374),
 (263, 349),
 (255, 326),
 (249, 307),
 (248, 288),
 (246, 261),
 (236, 278),
 (228, 299),
 (221, 319),
 (212, 345),
 (207, 372),
 (206, 398),
 (209, 422),
 (212, 449),
 (216, 477),
 (217, 512),
 (214, 538),
 (225, 559),
 (230, 585),
 (231, 609)]
pairs7 = generate_pairs(leaf7, n)

colors8 = colors4
leaf8 = [(234, 800),
 (237, 780),
 (240, 755),
 (242, 730),
 (234, 707),
 (232, 681),
 (234, 650),
 (237, 631),
 (233, 610),
 (227, 571),
 (217, 543),
 (203, 512),
 (192, 479),
 (181, 505),
 (174, 529),
 (167, 556),
 (167, 594),
 (173, 632),
 (177, 660),
 (179, 696),
 (184, 728),
 (190, 749),
 (191, 767),
 (195, 795)]
pairs8 = generate_pairs(leaf8, n)

colors9 = colors5
leaf9 = [(212, 529),
 (212, 510),
 (206, 492),
 (202, 473),
 (193, 453),
 (183, 432),
 (172, 416),
 (169, 394),
 (160, 375),
 (152, 356),
 (153, 378),
 (151, 400),
 (149, 420),
 (148, 441),
 (151, 471),
 (153, 493),
 (158, 524),
 (161, 549),
 (161, 573),
 (165, 597),
 (166, 617),
 (161, 645),
 (165, 675),
 (171, 699),
 (175, 727),
 (179, 750),
 (184, 774),
 (189, 797)]
pairs9 = generate_pairs(leaf9, n)

white = Color(hex="#FFFFFF")
bg_colors = [col for col in white.range_to("#000000", 501)]

for i, j in tqdm(enumerate(np.linspace(1, 50, 501)), total=len(bg_colors)):
    frame = Frame(700, 900, bg=bg_colors[i])
    add_leaf(pairs1, colors1, frame, n=100, scale=j, div=50, repeat=False)
    add_leaf(pairs3, colors3, frame, n=100, scale=j, div=50, repeat=False)
    add_leaf(pairs2, colors2, frame, n=100, scale=j, div=50, repeat=False)
    add_leaf(pairs4, colors4, frame, n=100, scale=j, div=50, repeat=False)
    add_leaf(pairs6, colors6, frame, n=100, scale=j, div=50, repeat=False)
    add_leaf(pairs5, colors5, frame, n=100, scale=j, div=50, repeat=False)
    add_leaf(pairs7, colors7, frame, n=100, scale=j, div=50, repeat=False)
    add_leaf(pairs9, colors9, frame, n=100, scale=j, div=50, repeat=False)
    add_leaf(pairs8, colors8, frame, n=100, scale=j, div=50, repeat=False)
    canvas.add(frame)

canvas.show(inspect=False)