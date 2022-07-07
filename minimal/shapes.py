"""
Minimal wrapper of Pycairo shapes
"""

from __future__ import annotations

from copy import deepcopy
from functools import partial
from itertools import cycle, chain
from typing import Dict, List, Optional, Type, Union

import cairo
from cairo import Gradient, LinearGradient, RadialGradient
from colour import Color
import numpy as np

from . import display

class CairoMinimalObject:

    """
    Cairo Minimal Object
    Provides shared methods uniform across all Cairo Minimal Objects

    Attributes:
        fill_color (colour.Color, None): Shape Fill Color. If None, will not
            fill shape
        fill_alpha (float): Shape Fill alpha composite
        outline_color (colour.Color): Shape Outline Color
        outline_alpha (float): Shape Outline Alpha Composite
        outline_width (float): Shape Outline Width
        scalex (float): X-Axis Scaler
        scaley (float): Y-Axis Scaler
        rotate_angle (float): Rotation of Shape (in Radians)
            #TODO: I think it wants it in degrees
        preserve_pattern (bool): Preserve pattern upon location transformation
        metadata (dict): Set shape metadata
        pattern (cairo.Pattern): Cairo Pattern object
        preserve_pattern (bool): Allows pattern to transform along with shape
            if transformation methods are applied

    Keyword Arguments:
        fill_color (Color, optional): Shape Fill Color. If None, will not
            fill shape
        fill_alpha (float, optional): Shape Fill alpha composite
        outline_color (Color, optional): Shape Outline Color
        outline_alpha (float, optional): Shape Outline Alpha Composite
        outline_width (float, optional): Shape Outline Width
        scalex (float, optional): X-Axis Scaler
        scaley (float, optional): Y-Axis Scaler
        rotate_angle (float, optional): Rotation of Shape (in Radians)
            #TODO: I think it wants it in degrees
        preserve_pattern (bool, optional): Preserve pattern upon location
            transformation
        metadata (dict, optional): Set shape metadata
    """

    # Transformable Variables are variables able to be transformed by the
    # self.transform method. Each Object has their own specific transformable
    # variables but will always have the inherited transformable variables from
    # CairoMinimalObject. Having this be a class attribute instead of a instance
    # attribute allows users to extend certain shape classes with more
    # transformable variables to then be present on every instance of said shape.
    # Class attribute extensions on base CairoMinimal object however will not
    # be present on all inherited shapes
    _TRANSFORMABLE_VARIABLES = ['x', 'y', 'fill_color', 'fill_alpha',
                                'outline_color', 'outline_alpha', 'outline_width',
                                'scalex', 'scaley']
    #TODO: Scale X, Scale Y Transforms not working

    def __init__(self,
                 fill_color: Optional[Type[Color]] = Color(rgb=(0, 0, 0)),
                 fill_alpha: Optional[float] = 1.0,
                 outline_color: Optional[Type[Color]] = Color(rgb=(1, 1, 1)),
                 outline_alpha: Optional[float] = 1.0,
                 outline_width: Optional[float] = 1.0,
                 scalex: Optional[float] = 1.0,
                 scaley: Optional[float] = 1.0,
                 rotate_angle: Optional[float] = 0.0,
                 preserve_pattern: Optional[bool] = True,
                 metadata: Optional[Dict] = None) -> None:

        self.fill_color, self.fill_alpha = fill_color, fill_alpha
        self.outline_color, self.outline_alpha = outline_color, outline_alpha
        self.outline_width = outline_width
        self.scalex, self.scaley = scalex, scaley
        self.rotate_angle = rotate_angle
        self.metadata = {} if not metadata else metadata

        self.pattern = None
        self.preserve_pattern = None

    def linear_gradient(self,
                        color: Type[Color],
                        xy1: Optional[List[float, float]] = None,
                        xy2: Optional[List[float, float]] = None,
                        alpha: Optional[float] = 1.0,
                        offset: Optional[float] = 1.0) -> None:
        """
        Creates a linear gradient fill from provided coordinates and color

        Notes:
            Gradient can be called multiple times, with only the first needing
            linear space coordinate definitions
            First gradient color will be CairoMinimalObject defined fill_color

        Keyword Arguments:
            color (colour.Color): Color for gradient space
            xy1 (list: float, optional): Beginning coordinates for linear
                gradient colorspace, defined as (x1, y1)
            xy2 (list: float, optional): Ending coordinates for linear gradient
                colorspace, defined as (x2, y2)
            alpha (float, optional): Gradient Color alpha composite
            offset (float, optional): Range value 0-1 where defined color is
                sole color in gradient colorspace
        """

        if not self.pattern:
            self.pattern = LinearGradient(*xy1, *xy2)
            self.pattern.add_color_stop_rgba(0,
                                             *self.fill_color.get_rgb(),
                                             self.fill_alpha)
            self.pattern.add_color_stop_rgba(offset,
                                             *color.get_rgb(),
                                             alpha)
        else:
            self.pattern.add_color_stop_rgba(offset, *color.get_rgb(), alpha)

    def radial_gradient(self,
                        color: Type[Color],
                        cr1: Optional[List[float, float]] = None,
                        cr2: Optional[List[float, float]] = None,
                        alpha: Optional[float] = 1.0,
                        offset: Optional[float] = 1.0) -> None:
        """
        Creates a radial gradient fill from provided radial coordinates and color

        Notes:
            Gradient can be called multiple times, with only the first needing
            radial space coordinate definitions
            First gradient color will be CairoMinimalObject defined fill_color

        Keyword Arguments:
            color (colour.Color): Color for gradient space
            cr1 (list: float, optional): Beginning coordinates for radial
                gradient colorspace, defined as (cx1, cy1, r1)
            cr2 (list: float, optional): Ending coordinates for radial gradient
                colorspace, defined as (cx1, cy2, r2)
            alpha (float, optional): Gradient Color alpha composite
            offset (float, optional): Range value 0-1 where defined color is
                sole color in gradient colorspace
        """

        if not self.pattern:
            self.pattern = RadialGradient(*cr1, *cr2)
            self.pattern.add_color_stop_rgba(0,
                                             *self.fill_color.get_rgb(),
                                             self.fill_alpha)
            self.pattern.add_color_stop_rgba(offset,
                                             *color.get_rgb(),
                                             alpha)
        else:
            self.pattern.add_color_stop_rgba(offset, *color.get_rgb(), alpha)

        return None

    def _draw(self, canvas: Type[cairo.Canvas]):
        """
        Base Cairo Minimal Object Drawing Method
        What makes an object compatible with the minimal framework is the _draw
        method attached and called in the display object. Each object will run
        there own draw method and also the base draw method (Dependent on the
        object, the base draw can be before or after the specific object)
        """

        if self.fill_color: # self.fill_color can be None for outlined objects
            if self.pattern:
                canvas.set_source(self.pattern)
            else:
                canvas.set_source_rgba(*self.fill_color.get_rgb(),
                                       self.fill_alpha)

        if not isinstance(self, Text):
            if self.fill_color:
                canvas.fill_preserve()
            canvas.set_source_rgba(*self.outline_color.get_rgb(),
                                   self.outline_alpha)
            canvas.set_line_width(self.outline_width)

        canvas.stroke()

        self.transform()
        if self.preserve_pattern and issubclass(type(self.pattern), Gradient):
            self._preserve_pattern()

    def copy(self) -> CairoMinimalObject:
        """
        Return a deepcopy of Shape Object

        Notes:
            Gradient Objects not pickleable so we will just temporarily store
            it and reassign
        """

        pattern = self.pattern
        self.pattern = None

        copy = deepcopy(self)

        copy.pattern = pattern
        self.pattern = pattern

        return copy

    def translate(self, shift: List[float, float]) -> None:
        """
        Translates Shape by Some Shift

        Notes:
            Shift can take its argument as either a float or a tuple of floats.
            If float, value specified will apply uniformly to x and y.
            If tuple, values specified will take dx as the first item, dy as the
            second item. Polygons apply translate shift to all points automatically

        Keyword Arguments:
            shift (list: float): Value to shift
        """

        if isinstance(shift, tuple):
            dx, dy = shift
        else:
            dx, dy = shift, shift

        self._dx = dx
        self._dy = dy

        self.x += dx
        self.y += dy

        if isinstance(self, Polygon):
            self.lpts += np.array([dx, dy, dx, dy, dx, dy])

        if self.preserve_pattern:
            self._preserve_pattern()

    def _preserve_pattern(self) -> None:
        """
        Preserves pattern by after calling a method that changes the position
        of the shape
        """

        if isinstance(self.pattern, RadialGradient):
            cx1, cy1, r1, cx2, cy2, r2 = self.pattern.get_radial_circles()
            dx, dy = cx2-cx1, cy2-cy1
            fn = partial(self.radial_gradient,
                         cr1=(self.x, self.y, r1),
                         cr2=(self.x+dx, self.y+dy, r2))
        elif isinstance(self.pattern, LinearGradient):
            x1, y1, x2, y2 = self.pattern.get_linear_points()
            dx, dy = x2-x1, y2-y1
            fn = partial(self.linear_gradient,
                         xy1=(self.x-dx/2, self.y-dy/2),
                         xy2=(self.x+dx/2, self.y+dy/2))

        color_stops = self.pattern.get_color_stops_rgba()
        self.pattern = None

        for color_stop in color_stops[1:]:
            fn(color=Color(rgb=color_stop[1:4]),
               alpha=color_stop[-1],
               offset = color_stop[0]
               )

    def transform(self, at_end: str = "restart", **kwargs) -> None:
        """
        Transform Attributes of Objects

        Notes:
            Transformations are iterative states assigned through keyword arguments.
            If transform is called without transformable variables, will just
            iterative to the next state of assigned tranformations

            at_end supports the following movement endings:
                restart: At end of path, will restart from original cx, cy and
                    run through same path
                reverse: At end of path, will reverse course and follow path
                    in opposite direction
                stop: At end of path, will stay at last coordinate in path

        Keyword Arguments:
            at_end (str): Specifies what happens to movement at end of path
            **kwargs: Transformation variable with respective tranformation
        """

        if kwargs:
            for kwarg, t in kwargs.items():
                if kwarg in self._TRANSFORMABLE_VARIABLES:
                    if at_end == "restart":
                        _iter = cycle(t)
                    elif at_end == "reverse":
                        _iter = cycle(t + t[::-1][1:])
                    elif at_end == "stop":
                        _iter = chain(t, cycle([t[-1]]))
                    else:
                        raise KeyError("at_end specification not recognized",
                                       "select a supported method")

                    setattr(self, f"_{kwarg}", _iter)

                else:
                    raise AttributeError("Variable provided is not transformable: ",
                                         f"{kwarg}")

        else:
            for transformable_variable in self._TRANSFORMABLE_VARIABLES:
                if hasattr(self, f"_{transformable_variable}"):
                    prev = getattr(self, transformable_variable)
                    if transformable_variable == "x":
                        _dx = self._dx if hasattr(self, "_dx") else 0
                        setattr(self, transformable_variable, next(getattr(self, "_x"))+_dx)
                        if isinstance(self, Polygon):
                            dx = self.x - prev + _dx
                            self.lpts += np.array([dx, 0, dx, 0, dx, 0])
                    elif transformable_variable == "y" and isinstance(self, Polygon):
                        _dy = self._dy if hasattr(self, "_dy") else 0
                        setattr(self, transformable_variable, next(getattr(self, "_y"))+_dy)
                        if isinstance(self, Polygon):
                            dy = self.y - prev + _dy
                            self.lpts += np.array([0, dy, 0, dy, 0, dy])
                    else:
                        setattr(self, transformable_variable, next(getattr(self, f"_{transformable_variable}")))

    def transform_axis(self,
                       canvas: Union[Type[display.Canvas], Type[display.Frame]],
                       method: str) -> None:
        """
        Scales Cairo + Canvas objects

        Notes:
            Two potential scaling options - 'up' and 'down'
            'up' scale: Apply scale as-is
            'down' scale Return scale to base 1.0, 1.0

        Keyword Arguments:
            canvas (display.Canvas, display.Frame): Minimal Display object
            method (str): Scaler method
        """
        if method == 'up':
            canvas.scale(self.scalex, self.scaley)
            if self.rotate_angle:
                #TODO: rotate_angle works, but doesnt rotate around center/point
                # canvas.translate(self.x, self.y)
                canvas.rotate(self.rotate_angle)

        if method == 'down':
            canvas.scale(1.0/self.scalex, 1.0/self.scaley)
            if self.rotate_angle:
                canvas.rotate(-self.rotate_angle)
                # canvas.translate(-self.x, -self.y)


class Circle(CairoMinimalObject):

    # Circle extension of transformable variables
    _TRANSFORMABLE_VARIABLES = ['radius', 'angle1', 'angle2',
                                *CairoMinimalObject._TRANSFORMABLE_VARIABLES]

    def __init__(self, x, y, radius,
                 angle1=0.0, angle2=2*np.pi,
                 **kwargs):
        """
        Minimal Circle

        Notes:
            The beginning angle starts right of the center at 3 o'clock
            and rotates from that point clockwise

        Keyword Arguments:
            x (float): X-coordinate for center of circle
            y (float): Y-coordinate for center of circle
            radius (float): Radius of circle
            angle1 (float): Optional: Beginning angle. Default: 0
            angle2 (float): Optional: Ending angle. Default: 2*np.pi
            **kwargs: CairoMinimalObject Keyword Arguments
        """

        super().__init__(**kwargs)

        self.x, self.y = x, y
        self.radius = radius
        self.angle1, self.angle2 = angle1, angle2

    def _draw(self, canvas):
        """ Circle Object Drawing Method """

        self.transform_axis(canvas, 'up')
        canvas.arc(self.x, self.y, self.radius, self.angle1, self.angle2)
        super()._draw(canvas)
        self.transform_axis(canvas, 'down')

class Rectangle(CairoMinimalObject):

    # Square extension of transformable variables
    _TRANSFORMABLE_VARIABLES = ['width', 'height',
                                *CairoMinimalObject._TRANSFORMABLE_VARIABLES]

    def __init__(self, x, y, width, height, **kwargs):
        """
        Minimal Rectangle

        Notes:
            X, Y describe the upper left corner of the rectangle

        Keyword Arguments:
            x (float): X-coordinate for upper left corner
            y (float): Y-coordinate for upper left corner
            width (float): Width of the rectangle
            height (float): Height of the rectangle
            **kwargs: CairoMinimalObject Keyword Arguments
        """

        super().__init__(**kwargs)

        self.x, self.y = x, y
        self.width, self.height = width, height

    def _draw(self, canvas):
        """ Rectangle Object Drawing Method """

        self.transform_axis(canvas, 'up')
        canvas.rectangle(self.x, self.y, self.width, self.height)
        super()._draw(canvas)
        self.transform_axis(canvas, 'down')

class Triangle(CairoMinimalObject):

    def __init__(self, vertices, **kwargs):
        """ DOCSTRING """

        assert len(vertices) == 3, "Only three vertices allowed in triangle class"

        self.vertices = np.array(vertices)

        super().__init__(**kwargs)

    def _draw(self, canvas):
        """ DOCSTRING """

        self.transform_axis(canvas, "up")
        canvas.move_to(*self.vertices[0])
        for vertex in self.vertices[1:]:
            canvas.line_to(*vertex)
        canvas.line_to(*self.vertices[0])
        canvas.close_path()
        super()._draw(canvas)
        self.transform_axis(canvas, 'down')


class Polygon(CairoMinimalObject):

    def __init__(self, x, y, **kwargs):
        """
        Minimal Polygon

        Keyword Arguments:
            x (float): X-coordinate for starting polygon vertex
            y (float): Y-coordinate for starting polygon vertex
            **kwargs: CairoMinimalObject Keyword Arguments
        """

        super().__init__(**kwargs)

        self.x, self.y = x, y

        self.ltypes = []
        self.lpts = np.empty((0, 6)) #Default: cx1, cy1, cx2, cy2, x, y. If line_to, cxy1, cxy2 do not matter

    def line_to(self, x=None, y=None, segments=None):
        """
        Create line from previous vertex to current defined vertex

        Notes:
            Previous vertex will be the last vertex in self.order attribute.

        Keyword Arguments:
            x (float): X-coordinate for next polygon vertex
            y (float): Y-coordinate for next polygon vertex
            segments (list: float): X,Y coordinates for next n-polygon vertices
        """

        if x and y:
            self.ltypes.append('line_to')
            self.lpts = np.append(self.lpts, np.array([[0, 0, 0, 0, x, y]]), axis=0)
        elif segments:
            for segment in segments:
                self.ltypes.append('line_to')
                self.lpts = np.append(self.lpts, np.array([[0, 0, 0, 0, *segments]]), axis=0)
        else:
            raise ValueError("Missing value for either x and y or segments of x and y")

    def curve_to(self, x=None, y=None, cxy1=None, cxy2=None, segments=None):
        """
        Create cubic bezier curve from previous vertex to current defined vertex

        Notes:
            Previous vertex will be the last vertex in self.order attribute.

        Keyword Arguments:
            x (float): X-coordinate for next polygon vertex
            y (float): Y-coordinate for next polygon vertex
            cxy1 (list: float): Control point 1 X + Y Coordinates
            cxy2 (list: float): Control point 2 X + Y Coordinates
            segments (list: float): X,Y coordinates + curve control points for next n-polygon vertices
        """

        if cxy1 and cxy2 and x and y:
            cx1, cy1 = cxy1
            cx2, cy2 = cxy2
            self.ltypes.append('curve_to')
            self.lpts = np.append(self.lpts, np.array([[cx1, cy1, cx2, cy2, x, y]]), axis=0)
        elif segments:
            for segment in segments:
                self.ltypes.append('curve_to')
                self.lpts = np.append(self.lpts, np.array([[*cxy1, *cxy2, x, y]]), axis=0)
        else:
            raise ValueError("Missing value for either curve parameters or segments of curve parameters")

    def _draw(self, canvas):
        """ Polygon Object Drawing Method """

        self.transform_axis(canvas, 'up')
        canvas.move_to(self.x, self.y)
        for ltype, lpt in zip(self.ltypes, self.lpts):
            if ltype == 'line_to':
                canvas.line_to(*lpt[-2:])
            elif ltype == 'curve_to':
                canvas.curve_to(*lpt)

        canvas.close_path()
        super()._draw(canvas)
        self.transform_axis(canvas, 'down')

class Text(CairoMinimalObject):

    # Text extension of transformable variables
    _TRANSFORMABLE_VARIABLES = ["text", "font_size", "font",
                                "font_slant", "font_weight",
                                *CairoMinimalObject._TRANSFORMABLE_VARIABLES]

    def __init__(self, x, y, text, font_size=10,
                 font=None, font_slant="NORMAL", font_weight="NORMAL",
                 **kwargs):
        """
        Minimal Text

        Notes:
            Origin of text provided by x, y will be lower-left corner of first character
            Spacing between text characters handled solely by font selection


        Keyword Arguments:
            x (float): X-coordinate for text
            y (float): Y-coordinate for text
            text (str): Text to display
            font_size (float): Font Size
            font (str): Font family. Default if None will be system Default.
                        Limited selection possible as explained by cairo toy text API
            font_slant (str): Font Slant. Options: NORMAL, ITALIC, OBLIQUE
            font_weight (str): Font Weight. Options: NORMAL, BOLD
            **kwargs: CairoMinimalObject Keyword Arguments
        """

        super().__init__(**kwargs)

        self.x, self.y = x, y

        self.text = text
        self.font_size = font_size

        self.font = font if font else cairo.ToyFontFace("").get_family()
        self.font_slant = getattr(cairo.FontSlant, font_slant)
        self.font_weight = getattr(cairo.FontWeight, font_weight)

    def _draw(self, canvas):
        """ Text Object Drawing Method """

        super()._draw(canvas)
        canvas.select_font_face(self.font, self.font_slant, self.font_weight)
        canvas.set_font_size(self.font_size)

        canvas.move_to(self.x, self.y)
        self.transform_axis(canvas, 'up')
        canvas.show_text(self.text)
        canvas.stroke()
        self.transform_axis(canvas, 'down')