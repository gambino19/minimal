# -*- coding: utf-8 -*-
"""
Minimal Objects
"""

from datetime import datetime

import cairo
from colour import Color
import cv2
import imageio
import numpy as np

from . import noise

#TODO: Can we do 3d rotations via cv2.warpPerspective

#FIXME: WORK IN PROGRESS 

class Line():
    
    def __init__(self, start=None, stop=None, segments=None,
                 div=2, color=Color(rgb=(0, 0, 0)),
                 alpha = 1.0,
                 csystem="cartesian",
                 offset=(0, 0),
                 line_width=2,
                 dimension=2
                 ):
        """ 
        Minimal Generative Line
        
        Notes:
            - Divisions divide line start to endpoint by equal values to allow
            for movements across the shape method. Having div=2 signifies
            two divisions - the start and end point. Divisions can never be less
            than two.
            - csystem (Coordinate system) allows for defining points by either
            cartesian point system or polar point system. Currently only
            cartesian is allowed
        
        Keyword Arguments:
            start (tuple, int): Starting x, y coordinates for the line
            end (tuple, int): Ending x, y coordinates for the line
            segments (Iterable): n x 2 Iterable container where 0th index is start, 1st indes is end
            div (int): Divisions of the line. Default is set to 2
            color (colour.Color): Color of Line
            alpha (float): Alpha transparency of Line
            csystem (str): Coordinate system for line. Accepts 'cartesian' and 'polar'
            offset (tuple, int): x, y offset of center, useful in polar coordinate system
            line_width (float): Line Width
            dimension (float): Specify whether object is plotted in 2d or 3d
        
        """
        
        if div < 2:
            raise ValueError("Divisions cannot be set to a value less than two")
        self.div = div
        
        self.colors = [color]
        self.alphas = [alpha]
        self.colorranges = [(0, self.div)]
        
        self.csystem = csystem
        self.offset = offset
        
        self.line_width = line_width
        
        if start and stop:
            self.start = start
            self.stop = stop
            self.pts = np.array((np.linspace(start[0], stop[0], div),
                                np.linspace(start[1], stop[1], div))).T
        elif segments:
            self.start, self.stop = segments[0], segments[1]
            self.pts = np.empty((0, 2))
            for seg1, seg2 in zip(segments[:], segments[1:]):
                self.pts = np.vstack((self.pts, np.array((np.linspace(seg1[0], seg2[0], div//(len(segments)-1)),
                                                          np.linspace(seg1[1], seg2[1], div//(len(segments)-1)))).T))
                
        self._repeat = False
        self._lead = div
        self._follow = 0

    def ranges(self, colorrange):
        """ 
        Get different colors across ranges of divs in line
        
        Keyword Arguments:
            colorrange (Iterable): 2-D container where 0th index is starting point and 1st index is ending point (in range) 
        """
        
        _follow, _lead = colorrange[0], colorrange[1] + 1 # Addition of 1 on upperbound is to add connection in range
        if self._lead < colorrange[0] or self._follow > colorrange[1]:               
            _follow, _lead = None, None
        if self._lead <= colorrange[1] and self._lead >= colorrange[0]:
            _lead = self._lead
        if self._follow >= colorrange[0] and self._follow <= colorrange[1]:
            _follow = self._follow
        return _follow, _lead

    def _draw(self, canvas):
        """ Generative Object Drawing Method """
        
        canvas.set_line_width(self.line_width)
        
        for colorrange, color in zip(self.colorranges, zip(self.colors, self.alphas)):
            follow, lead = self.ranges(colorrange)
            if not follow and not lead:
                continue
            for i, f in zip(self.pts[follow:lead], self.pts[follow+1:lead]):
                canvas.set_source_rgba(*color[0].get_rgb(), color[1])
                if self.csystem == "cartesian":
                    #TODO: Some gap between lines thats visible, how can we connect this so it doesnt look disjointed?
                    # See https://stackoverflow.com/questions/38143037/cairo-gtk-draw-a-line-with-transparency-like-a-highlighter-pen
                    canvas.move_to(i[0], i[1])
                    canvas.line_to(f[0], f[1])
                elif self.csystem== "polar":
                    canvas.move_to(i[0]*np.cos(i[1])+self.offset[0], i[0]*np.sin(i[1])+self.offset[1])
                    canvas.line_to(f[0]*np.cos(f[1])+self.offset[0], f[0]*np.sin(f[1])+self.offset[1])
                canvas.stroke()
        canvas.set_line_join(cairo.LINE_JOIN_ROUND)
            
        if self._repeat:
            if self._lead < self.div:
                self._lead += 1
            elif self._lead >= self.div and self._follow < self.div:
                self._follow += 1
            elif self._follow == self._lead:
                self._follow, self._lead = 0, 0
    
    def shape(self, f, axis="x"):
        """ 
        EXPERIMENTAL: How can we better define polar functions?
        """
        # TODO: Good potential, but is not part of MVP
        
        raise NotImplementedError
        
        if self.csystem == "cartesian":
            i, j = (0, 1) if axis == "x" else (1, 0)
            f = f.replace("x", "self.pts[:, 0]").replace("y", "self.pts[:, 1]")
        elif self.csystem == "polar":
            i, j = (0, 1) if axis == "r" else (1, 0)
            f = f.replace("r", "self.pts[:, 0]").replace("theta", "self.pts[:, 1]")
        
        if isinstance(f, str):
            self.pts[:, i] = eval(f) + self.pts[:, j]
        else:
            self.pts[:, i] = f(self.pts[:, i]) + self.pts[:, j]
        
        
    def gradient(self, color, step, alpha = (1, 1)):
        """ 
        Gradient to color by step for line
        
        Notes:
            Gradient is handled by colour.Color object but will modify for colorranges
            when called by ranges
            
        Keyword Arguments:
            color (colour.Color): Color to gradient to
            step (int): Number of steps in gradient from base color to argument color
            alpha (Iterable, int): Alpha transparency for gradient
        """
        
        self.colorranges = []
        self.colors = [self.colors[-1]]
        self.alphas = [self.alphas[-1]]
        
        ranges = np.linspace(0, self.div, step)
        alphas = np.linspace(alpha[0], alpha[1], step)
        for c, p in zip(zip(self.colors[-1].range_to(color, step), alphas), zip(ranges[:], ranges[1:])):
            self.colorranges.append(tuple([int(i) for i in p]))
            self.colors.append(c[0])
            self.alphas.append(c[1])
        
    def repeat(self, random=False):
        """ 
        Repeat Line
        
        Notes:
            Repeated line causes lines to be constantly recreated upon each
            frame. Gives illusion that line is being drawn and erased
            
        Keyword Arguments: 
            random (bool): Start repeat at random part in range
        """
        
        self._repeat = True
        if random:
            self._lead = np.random.choice(self.div)
        else:
            self._lead = 0
        
    def couple(self, line):
        """ 
        Couple two lines; make two line objects into one
        
        Keyword Arguments:
            line (objects.Line): Line to couple
        """
        
        self.stop = line.stop
        self.div += line.div
        
        self.colorranges.append((self.colorranges[-1][-1], self.colorranges[-1][-1] + line.div))
        self.colors.append(line.colors[0]) # TOOO: This doesnt seem like the best thing to do
        
        self._lead += line.div
        self.pts = np.vstack((self.pts[:-1], line.pts[:]))

    def noise(self, scale=1, z=datetime.now().microsecond, **kwargs):
        """
        Using simplex or perlin noise methods to add noise in constructed line.pts
        
        Keyword Arguments:
            scale (int, float, tuple): Define scaling factors to induced noise. If int or float is provided
                                       will apply to axis 0, 1. If tuple is provided, will apply index 0, 1
                                       to axis 0, 1
            method (str): Determine which noise method to apply to lines
            z (int, float): Variable parameter to ensure random generation of noise in each run
            ** kwargs as defined by noise.SimplexNoise
        
        """

        snoise = noise.SimplexNoise()

        if isinstance(scale, int) or isinstance(scale, float):
            scalex, scaley = scale, scale
        elif isinstance(scale, tuple):
            scalex, scaley = scale[0], scale[1]
        else:
            raise NotImplementedError("Noise scale only accepts int for uniform axis definition or tuple with length 2 for singular axis definition")

        for pt in range(len(self.pts)):
            self.pts[pt, 0] += scalex*snoise.noise3(x=self.pts[pt, 0]/self.div, 
                                                    y=self.pts[pt, 1]/self.div,
                                                    z=z)
            self.pts[pt, 1] += scaley*snoise.noise3(x=self.pts[pt, 0]/self.div, 
                                                    y=self.pts[pt, 1]/self.div,
                                                    z=z)
    
    #TODO: Bezier Curve in Line: https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy

class Image:
    
    def __init__(self, data, position=(0, 0), channels=4):
        """ 
        Minimal handler for adding Images to canvas
        
        Keyword Arguments:
            data (str, ndarray, imageio.core.utils.array): Data representative for Image. 
                  Data as str is a filepath to image, array (imageio or numpy) is array representation of image
            position (tuple: int, optional): x, y location for top-left corner of Image
            channels (int): Number of color channels
        """
          
        if isinstance(data, str):
            self.image = cv2.imread(data, flags=cv2.IMREAD_UNCHANGED)
        elif isinstance(data, imageio.core.util.Array) or isinstance(data, np.ndarray):
            self.image = data
        else:
            raise NotImplementedError(f"Datatype {type(data)} is not supported.")    
        
        if channels == 4 and self.image.shape[-1] != 4:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2RGBA)
        
        self.position = position
        
    def _draw(self, canvas):
        """ Image Drawing Method """
        
        # Canvas-coordinats coordinates for cropping
        cx1, cx2 = max(0, self.position[0]), min(canvas.shape[1], self.position[0] + self.image.shape[1])
        cy1, cy2 = max(0, self.position[1]), min(canvas.shape[0], self.position[1] + self.image.shape[0])
    
        # Image-based coordinates for cropping
        ix1, ix2 = max(0, -self.position[0]), min(self.image.shape[1], canvas.shape[1] - self.position[0])
        iy1, iy2 = max(0, -self.position[1]), min(self.image.shape[0], canvas.shape[0] - self.position[1])
    
        if not (cy1 >= cy2 or cx1 >= cx2 or iy1 >= iy2 or ix1 >= ix2):
        
            image = self.image[iy1:iy2, ix1:ix2]
            alpha_mask = self.image[:, :, 3] / 255.0
            image_alpha = alpha_mask[iy1:iy2, ix1:ix2, np.newaxis]

            canvas_crop = canvas[cy1:cy2, cx1:cx2]
            canvas_alpha = 1.0 - image_alpha
        
            canvas_crop[:] = image_alpha * image + canvas_alpha * canvas_crop
            
    def mirror(self, axis):
        """ Mirror Image. Follows np.flip axis argument """
        
        self.image = np.flip(self.image, axis)
    
    def resize(self, size, interpolation=cv2.INTER_LINEAR):
        """ 
        Resize Image. 
        
        Notes:
            Handled by CV2. Defaultly uses interpolation=cv2.INTER_LINEAR
            
        Keyword Arguments:
            size (Iterable: int): Resize shape
            interpolation (cv2 method): cv2 Interpolation method
        """
        self.image = cv2.resize(self.image, size, interpolation=interpolation)    
    
    def rotate(self, angle):
        """ Rotate Image. Rotation angle in degrees  """
        
        center = tuple(np.array(self.image.shape[1::-1]) / 2)
        rotation = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.image = cv2.warpAffine(self.image, rotation, self.image.shape[1::-1], flags=cv2.INTER_LINEAR)
    
class Video:
    
    def __init__(self, path, position):
        """
        EXPERIMENTAL
        """
        
        self.video = imageio.get_reader(path)
        self.position = position
        self.frame = 0
        
        self._mirror_axis = None
        
    def _draw(self, data):
        
        img = Image(self.video.get_data(self.frame), self.position)
        if isinstance(self._mirror_axis, int):
            img.mirror(self._mirror_axis)
        img._draw(data)
        if self.frame == len(self.video)-1:
            self.frame = 0
        else:
            self.frame += 1

    def mirror(self, axis):
        
        self._mirror_axis = axis