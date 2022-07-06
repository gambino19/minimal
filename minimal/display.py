# -*- coding: utf-8 -*-
"""
Minimal Display Elements
"""

from __future__ import annotations

from functools import singledispatchmethod
import time
from typing import Any, Dict, Iterable, Optional, Type, Tuple, Union
import warnings

import cairo
from colour import Color
import cv2
import h5py
import numpy as np
from PIL import Image

from . import shapes
from . import objects

class ABDisplay:

    """
    Abstract Base class for display objects such as Canvas and Frames

    Attributes:
        width (float): Display Width
        height (float): Display Height
        color (Color): Display background color. Default: Color(rgb=(1,1,1))
        inspections (list): Coordinates of left-click event on display window
        data (np.array): Pixel data for cairo.ImageSurface; can be directly
            modified for rendering. #TODO: Find a better description
        surface (cairo.ImageSurface): Cairo surface object for rendering memory
            buffers
        canvas (cairo.Context): Cairo context object for drawing instructions

    Keyword Arguments:
        width (float): Display Width
        height (float): Display Height
        color (Color, optional): Display background Color.
            Default: Color(rgb=(1,1,1))
    """

    def __init__(self,
                 width: float,
                 height: float,
                 color: Optional[Type[Color]] = Color(rgb=(1,1,1))) -> None:

        self.width = width
        self.height = height
        self.color = color

        self.inspections = []

        self.data = np.zeros((height, width, 4), dtype=np.uint8)

        self.surface = cairo.ImageSurface.create_for_data(self.data,
                                                          cairo.FORMAT_ARGB32,
                                                          width,
                                                          height)
        self.canvas = cairo.Context(self.surface)
        self.canvas.set_source_rgba(*self.color.get_rgb(), 1.0)
        self.canvas.paint()

    def _inspect(self,
                 event: int,
                 x: int, y: int,
                 flags: int,
                 param: Union[Dict, None]) -> None:
        """
        Inspecting positions on ABDisplay objects via callbacks left mouse click
        (right click to clear)Handled by cv2 during cv2.imshow operation, should
        not be called otherwise
        """

        if event == cv2.EVENT_LBUTTONDOWN:
            circle = shapes.Circle(x, y, 3,
                                   fill_color=Color(rgb=(1, 0, 0)),
                                   metadata={"label": "inspection"})
            self.add(circle)
            self.inspections.append((x, y))

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.order.items = [obj for obj in self.order.items
                                if obj.metadata.get("label") != "inspection"]
            self.inspections = []
            #TODO: Clear inspections from Canvas

    def to_image(self, fp: str) -> None:
        """
        Save Display to Image

        Keyword Arguments:
            fp (str): File path for output image
        """

        img = cv2.cvtColor(self.data, cv2.COLOR_RGB2BGRA)
        Image.fromarray(img).save(fp)

    @property
    def shape(self) -> Tuple[int, int, int]:
        """ Returns shape of display object """
        return (self.width, self.height, 4)

class Frame(ABDisplay):
    """
    Static Frame Display

    Notes:
        Frames can be used to represent single static display or can
        be successively added into the Canvas object to represent a single frame

    Attributes:
        width (float): Display Width
        height (float): Display Height
        color (Color): Display background color. Default: Color(rgb=(1,1,1))
        inspections (list): Coordinates of left-click event on display window
        data (np.array): Pixel data for cairo.ImageSurface; can be directly
            modified for rendering. #TODO: Find a better description
        surface (cairo.ImageSurface): Cairo surface object for rendering memory
            buffers
        canvas (cairo.Context): Cairo context object for drawing instructions

    Keyword Arguments:
        width (float): Display Width
        height (float): Display Height
        color (Color, optional): Display background Color.
            Default: Color(rgb=(1,1,1))

    Examples:
        >>> frame = minimal.display.Frame(800, 800)
        >>> circle = mininmal.shapes.Circle(400, 400, 100)
        >>> frame.add(circle)
        >>> frame.show()
    """

    def __init__(self,
                 width: float,
                 height: float,
                 color: Optional[Type[Color]] = Color(rgb=(1,1,1))) -> None:

        super().__init__(width=width, height=height, color=color)

    @singledispatchmethod
    def add(self, obj: Any, _index: Optional[Union[int, None]] = None) -> None:
        """
        Draws drawing objects in frame

        Notes:
            Unlike Canvas, Frames are drawn upon addition and not placed in any
            order attribute. Therefore, passing an index to a frame add method
            will not do anything

        Keyword Arguments:
            obj (object): Drawing object to add to canvas
            _index (int, optional): Adds object at particular index in order.
                Has no use in Frame Object (added from ABDisplay inheritance)
        """

        if _index:
            warnings.warn("""Frames are drawn upon addition and not placed in
                          any orderattribute. Therefore, passing an index will
                          not change order in whichdrawing objects are drawn""",
                          SyntaxWarning)
        obj._draw(self.canvas)

    @add.register(tuple)
    @add.register(list)
    def _(self,
          objs: Union[Tuple, list],
          indicies: Iterable[int] = None) -> None:
        """ Iterative add method with lists and tuples """

        if indicies:
            for obj, index in zip(objs, indicies):
                self.add(obj, index)
        else:
            for obj in objs:
                self.add(obj)

    def _draw(self, canvas: Type[cairo.Context]) -> None:
        """ Frame Drawing Method when added to Canvas"""

        canvas.data = self.data

    def show(self, exit_key: str = "q", inspect: bool = False) -> None:
        """
        Visualizes current Frame in seperate Window

        Keyword Arguments:
            exit_key (str, optional): Key to exit out of Frame Window.
                Default: 'q'
            inspect (bool, optional): Allows mouse clicks callback on window to
                inspect and mark points of interests
        """

        cv2.imshow("Frame", self.data)
        if inspect:
            cv2.setMouseCallback("Frame", self._inspect)

        while True:
            cv2.imshow("Frame", self.data)
            if cv2.waitKey(0) & 0xFF == ord(exit_key):
                break

        cv2.destroyAllWindows()

    def to_hdf5(self, fp: str, name: str, root: Optional[str] = "/") -> None:
        """
        Save Frame to HDF5

        Notes:
            If HDF5 at 'fp' already exists, will append on to it

        Keyword Arguments:
            fp (str): Filename or pathlib.Path object for Image
            name (str): Name of dataset to save Frame to
            root (str, optional): Hierarchical root for dataset
        """

        with h5py.File(fp, 'a') as f:
            f[root].create_dataset(name, data=self.data)

    def from_hdf5(self, fp: str, name: str, root: Optional[str] = "/") -> None:
        """
        Load Frame from HDF5

        Keyword Arguments:
            fp (str): Filename or pathlib.Path object for Image
            name (str): Name of dataset to save Frame to
            root (str, optional): Hierarchical root for dataset
        """

        with h5py.File(fp, 'r') as f:
            self.data = f[f"{root}/{name}"][:]

class Canvas(ABDisplay):

    """
    Canvas Display

    Notes:
        Canvas can be used in itself to be a single frame, collection of frames,
        or window of nonstatic objects

    Attributes:
        width (float): Display Width
        height (float): Display Height
        color (Color): Display background color. Default: Color(rgb=(1,1,1))
        inspections (list): Coordinates of left-click event on display window
        data (np.array): Pixel data for cairo.ImageSurface; can be directly
            modified for rendering. #TODO: Find a better description
        surface (cairo.ImageSurface): Cairo surface object for rendering memory
            buffers
        canvas (cairo.Context): Cairo context object for drawing instructions
        fps (int): Frames per second for Frame or Drawing Objects when displayed
            in Canvas

    Keyword Arguments:
        width (float): Display Width
        height (float): Display Height
        color (Color, optional): Display background Color.
            Default: Color(rgb=(1,1,1))
        fps (int): Frames per second for Frame or Drawing Objects when displayed
            in Canvas. Default: 60

    Examples:
        >>> Canvas = minimal.display.Canvas(800, 800)
        >>> circle = mininmal.shapes.Circle(400, 400, 100)
        >>> circle.transform(radius=[i for i in range(100)])
        >>> canvas.add(circle)
        >>> canvas.show()
    """

    def __init__(self,
                 width: float,
                 height: float,
                 color: Optional[Type[Color]] = Color(rgb=(1,1,1)),
                 fps: Optional[int] = 60) -> None:

        super().__init__(width=width, height=height, color=color)

        self.fps = fps
        self.refresh = True
        self.order = Order()

    @property
    def _framerate(self) -> int:
        """
        For drawing Frames on Canvas, we define frame rate to be the
        millisecond delay between frame displays. Use of @property on _framerate
        to allow users to adjust fps without needing to calculate millisecond
        delay for cv2.waitKey
        """
        return int((1 / self.fps) * 1000)

    @_framerate.setter
    def _framerate(self, value: int) -> None:
        self._fps = value

    @singledispatchmethod
    def add(self, obj: Any, index: Optional[Union[int, None]] = None) -> None:
        """
        Handles inserting drawing objects into display order

        Notes:
            Single object entry handled in base add method, lists and tuples
            are handled in an iterative manner managed by singledispatchmethod
            register

        Keyword Arguments:
            obj (object): Drawing object to add to canvas
            index (int, optional): Adds object at particular index in order.
                Default: None
        """

        if isinstance(obj, Frame):
            self.refresh = False

        if isinstance(index, int):
            self.order.insert(index, obj)
        else:
            self.order.append(obj)

    @add.register(tuple)
    @add.register(list)
    def _(self,
          objs: Union [Tuple, list],
          indicies: Iterable[int] = None) -> None:
        """ Iterative add method with lists and tuples """

        if indicies:
            for obj, index in zip(objs, indicies):
                self.add(obj, index)
        else:
            for obj in objs:
                self.add(obj)


    def _draw_nonframed(self) -> None:
        """
        Drawing framed and non-framed are handled differently, as frames
        are always static Non-framed allows objects to be modified under
        _TRANSFORMABLE_VARIABLES or other mutable properties
        """

        if self.refresh:
            self.canvas.set_source_rgba(*self.color.get_rgb(), 1.0)
            self.canvas.paint()
        for obj in self.order:
            if isinstance(obj, (objects.Image, objects.Video)):
                #TODO: Will have to rework these methods
                obj._draw(self.data)
            else:
                obj._draw(self.canvas)

    def show(self,
             exit_key: str = "q",
             inspect: Optional[bool] = False,
             restart_frames: Optional[bool] = True) -> None:
        """
        Launches external window showing Canvas illustration through
        drawing all drawing objects in Canvas order object

        Notes:
            The show method is a good way to see progress of illustration but
            shouldnt be used for final output (see Frame.to_image,
            Canvas.to_image,or Canvas.to_video), especially when using many
            computationally heavy drawing objects not in Frames

        Keyword Arguments:
            exit_key (str): Key to close out of launched window for Canvas
                preview. Default: 'q'
            inspect (bool): Enable mouse clicks to inspect positions on canvas.
                Left click to mark position, right click to clear all inspections.
                Use self.inspections once closing window to see all selected
                inpections
            restart_frames (bool): If only frames in order, will start from
                beginning if show method is called twice without re-initializing
                the Canvas object
        """

        run = True

        cv2.imshow("Canvas", self.data)
        if inspect:
            cv2.setMouseCallback("Canvas", self._inspect)

        if (all(isinstance(frame, Frame) for frame in self.order.items)
                and self.order.items):

            self.order.stopiter = False
            while run:
                frame = next(self.order)
                frame._draw(self)
                cv2.imshow("Canvas", self.data)
                if cv2.waitKey(self._framerate) & 0xFF == ord(exit_key):
                    run = False
            self.order.stopiter = True
            if restart_frames:
                self.order.i = 0

        else:
            while run:
                self._draw_nonframed()
                cv2.imshow("Canvas", self.data)
                if cv2.waitKey(self._framerate) & 0xFF == ord(exit_key):
                    run = False

        cv2.destroyAllWindows()


    def to_image(self, fp: str) -> None:
        """
        Save Display to Image

        Notes:
            to_image in Canvas does not except frame objects, as that can
            be handled by Frame.to_image. As well, multiple frames cannot be
            saved into a single image

        Keyword Arguments:
            fp (str): Filename or pathlib.Path object for Image
        """

        if any(isinstance(frame, Frame) for frame in self.order):
            raise TypeError("Cannot save multiple frames to single image ",
                             "Recommended to use Frame.to_image")
        self._draw_nonframed()
        super().to_image(fp)

    def to_video(self,
                 fp: str,
                 fourcc: Optional[str] = "DIVX",
                 duration: Optional[Union[int, None]] = None) -> None:
        """
        EXPERIMENTAL: How can we get canvas objects to write to some video file
        compatible across different environments?
        """

        _fourcc = cv2.VideoWriter_fourcc(*fourcc)
        video = cv2.VideoWriter(fp, _fourcc,
                                self.fps,
                                (self.shape[0], self.shape[1]))

        if all(isinstance(frame, Frame) for frame in self.order):
            for frame in self.order:
                frame._draw(self)
                video.write(cv2.cvtColor(self.data, cv2.COLOR_RGBA2BGR))
        else:
            end = time.time() + duration
            while time.time() < end:
                self._draw_nonframed()
                video.write(cv2.cvtColor(self.data, cv2.COLOR_RGBA2RGB))

        video.release()

class Order:

    """
    Object to handle drawing objects for Canvas Objects

    Notes:
        The order object can be iterated through normally with no change,
        however the order object can as well be iterated through infinitely
        through the use of the self.stopiter = False. Iteration options needed
        for use of show or save methods on Canvas to have responsive callbacks

    Attributes:
        items (list): Items added through either Canvas.add or Frame.add
        i (int): Beginning index of items
        j (int): Ending index of items
        stopiter (bool): Toggle iteration through order. If True, will
            stop the iteration once it reaches j. If False, will repeat from i.
    """

    def __init__(self) -> None:

        self.items = []
        self.i, self.j = 0, len(self.items)
        self.stopiter = True

    def append(self, obj: Any) -> None:
        """
        Append Objects into Order items

        Keyword Arguments:
            obj (object): Drawing Object to append to order
        """

        self.items.append(obj)
        self.j = len(self.items)

    def insert(self, index: int, obj: object) -> None:
        """
        Insert Objects by index into Order items

        Keyword Arguments:
            index (int): Index to insert object into order items
            obj (object): Drawing Object to append to order
        """

        self.items.insert(index, obj)
        self.j = len(self.items)

    def __next__(self) -> Any:

        if self.i < self.j:
            pass
        else:
            if not self.stopiter:
                self.i = 0
            else:
                self.i = 0
                raise StopIteration

        obj = self.items[self.i]
        self.i += 1
        return obj

    def __iter__(self) -> Order:
        return self
