# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:41:18 2022

@author: micha
"""

import os
import sys

from colour import Color
import numpy as np
import pywavefront

minimal_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, minimal_dir)
from minimal import objects, display

# TODO: Can we use something with np.atleast_nd?

fNear = 0.1
fFar = 1000.0
fFov = 90.0
Width = 800
Height = 800
fAspectRatio = Height /  Width
fFovRad = 1.0 / np.tan(fFov * 0.5 / 180.0 * np.pi)
fTheta = 10.0

matProj = np.array([[fAspectRatio*fFovRad, 0      , 0                               , 0],
                    [0                   , fFovRad, 0                               , 0],
                    [0                   , 0      , fFar / (fFar - fNear)           , 1],
                    [0                   , 0      , (-fFar * fNear) / (fFar - fNear), 0]])

CANVAS = display.Canvas(Width, Height)
CANVAS.mat_project = matProj # TODO: Add this to canvas class

class geometry:

    @staticmethod
    def get_rotation_matrix(axis, theta=0.0):
        """DOCSTRING"""
        if axis == 'x':
            rot_mat = np.array([[1.0, 0.0,            0.0,            0.0],
                                [0.0, np.cos(theta),  np.sin(theta),  0.0],
                                [0.0, -np.sin(theta), np.cos(theta),  0.0],
                                [0.0, 0.0,            0.0,            1.0]])
        elif axis == 'y':
            rot_mat = np.array([[np.cos(theta),  0.0, np.sin(theta), 1.0],
                                [0.0,            1.0, 0.0,           0.0],
                                [-np.sin(theta), 0.0, np.cos(theta), 0.0],
                                [0.0,            0.0, 0.0,           1.0]])

        elif axis == 'z':
            rot_mat = np.array([[np.cos(theta),  np.sin(theta), 0.0, 0.0],
                                [-np.sin(theta), np.cos(theta), 0.0, 0.0],
                                [0.0,             0.0,          1.0, 0.0],
                                [0.0,             0.0,          0.0, 1.0]])

        return rot_mat

    def normal(arr, normalize=True):
        """ DOCSTRING """

        norm_vec = np.cross(arr[:,1,:]-arr[:,0,:],arr[:,2,:]-arr[:,0,:])
        if normalize:
            norm_vec /= np.sqrt(np.sum(norm_vec**2, axis=1, keepdims=True))

        return norm_vec


class vec3d:
    """ DOCSTRING """
    def __init__(self, x, y, z=0):

        self.x = x
        self.y = y
        self.z = z

        self.xyz = np.array([[x, y, z]])

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, z={self.z})'

class Triangle:
    """ DOCSTRING """
    def __init__(self, p1, p2, p3, color=Color(luminance=0)):

        self.p1 = p1 if isinstance(p1, vec3d) else vec3d(*p1)
        self.p2 = p2 if isinstance(p2, vec3d) else vec3d(*p2)
        self.p3 = p3 if isinstance(p3, vec3d) else vec3d(*p3)

        self.p = np.array([*self.p1.xyz, *self.p2.xyz, *self.p3.xyz])
        self.color = color

    def get_lengths(self):
        """ DOCSTRING """
        # Same thing as np.linalg.norm(arr - np.roll(arr, -1, axis=0), axis=1)
        # but is about 3x more efficient

        len12 = np.sqrt((self.p1.x-self.p2.x)**2 + (self.p1.y-self.p2.y)**2)
        len23 = np.sqrt((self.p2.x-self.p3.x)**2 + (self.p2.y-self.p3.y)**2)
        len31 = np.sqrt((self.p3.x-self.p1.x)**2 + (self.p3.y-self.p1.y)**2)

        return len12, len23, len31

    def fill(self, color):
        """ DOCSTRING """
        # https://stackoverflow.com/questions/63674527/filling-in-a-triangle-by-drawing-lines-in-pygame @ Rabbid76
        len12, len23, len31 = self.get_lengths()
        lens = {len12: (self.p1, self.p3, self.p2),
                len23: (self.p2, self.p1, self.p3),
                len31: (self.p3, self.p2, self.p1)}
        p1, p2, p3 = lens[max(lens)]

        fill_lines = []
        if abs(p3.x-p1.x) > abs(p3.y-p1.y):
            for x in range(int(min(p1.x, p3.x)), int(max(p1.x, p3.x)+1)):
                m = ((p1.y - p3.y)/ (p1.x - p3.x))
                y = m*(x - p3.x) + p3.y
                fill_lines.append(objects.Line((x, y), (p2.x, p2.y), div=100, color=color))
        else:
            for y in range(int(min(p1.y, p3.y)), int(max(p1.y, p3.y)+1)):
                m = ((p1.x - p3.x)/ (p1.y - p3.y))
                x = m*(y - p3.y) + p3.x
                fill_lines.append(objects.Line((x, y), (p2.x, p2.y), div=100, color=color))

        return fill_lines

    def __repr__(self):
        return repr(self.p)

class Mesh:
    """ DOCSTRING """
    def __init__(self, *args, wireframe=True):

        if not len(args):
            self.vertices = np.array([])
        else:
            self.vertices = np.array([arg.p for arg in args])

        self._tris = self.vertices.copy()

        self.normals = None
        self.visible_mask = None
        self.fill_color = None
        self.textures = {}

        self.wireframe = wireframe

        self.order = display.Order()

    def from_obj(self, fp):
        """ DOCSTRING """

        tris = []

        obj = pywavefront.Wavefront(fp, collect_faces=True, create_materials=False)
        for face in obj.mesh_list[0].faces:
            tris.append(Triangle(obj.vertices[face[0]], obj.vertices[face[1]], obj.vertices[face[2]]))
        self.vertices = np.array([tri.p for tri in tris])

    def rotate(self, axis, theta):
        """ DOCSTRING """

        rot_mat = geometry.get_rotation_matrix(axis, theta)
        self.vertices = w_matmul(self.vertices, rot_mat)

    def translate(self, x=0.0, y=0.0, z=0.0, method="add"):
        """ DOCSTRING """

        if method == "add":
            self.vertices += np.repeat(np.array([[x, y, z]]), 3, axis=0)
        elif method == "sub":
            self.vertices -= np.repeat(np.array([[x, y, z]]), 3, axis=0)
        elif method == "mul":
            self.vertices *= np.repeat(np.array([[x, y, z]]), 3, axis=0)
        elif method == "div":
            self.vertices /= np.repeat(np.array([[x, y, z]]), 3, axis=0)
        else:
            raise KeyError(f"Method not recognized; provided {method}. "
                           "Accepts: 'add', 'sub', 'mul', 'div'")

    def visible(self, camera=vec3d(x=0, y=0, z=0)):
        """ DOCSTRING """

        self.textures['visible'] = {"func": self._visible, "params": (camera,)}

    def _visible(self, camera):
        """ DOCSTRING """

        self.normals = geometry.normal(self.vertices)
        self.visible_mask = np.sum(self.normals * (self.vertices[:,0,:] - camera.xyz), axis=1) < 0.0
        self.vertices = self.vertices[self.visible_mask]

    def illuminate(self, light_direction=vec3d(0.0, 0.0, -1.0)):
        """ DOCSTRING """

        self.textures['illuminate'] = {"func": self._illuminate, "params": (light_direction,)}
        self.textures['shaded'] = {"func": self._shaded, "params": ()}

    def _illuminate(self, light_direction=vec3d(0.0, 0.0, -1.0)): #TODO: Seems like this is broken
        """ DOCSTRING """
        # TODO: Techincally, illuminate will produce an illumination for all faces and not just ones that are left
        normals = self.normals[self.visible_mask] if 'visible' in self.textures else self.normal
        light_direction.xyz = light_direction.xyz / np.sqrt(np.sum(light_direction.xyz**2, axis=1))
        dp = normals @ light_direction.xyz.T
        # dp = np.where(dp < 0.0, 0.0, dp)
        print(dp)
        self.fill_color = [Color(luminance=0.6) for i in dp] # TODO: Work on better illumination color code

    def project(self, canvas):
        """ DOCSTRING """

        self.vertices = w_matmul(self.vertices, canvas.mat_project)

    def sort(self):
        """ DOCSTRING """

        self.vertices = self.vertices[(np.sum(self.vertices[:,:,-1], axis=1) / 3).argsort()]

    def _wireframe(self):
        """ DOCSTRING """

        for tri in self.vertices:
            self.order.append(objects.Line((tri[0,0], tri[0,1]), (tri[1,0], tri[1,1]), div=100))
            self.order.append(objects.Line((tri[1,0], tri[1,1]), (tri[2,0], tri[2,1]), div=100))
            self.order.append(objects.Line((tri[2,0], tri[2,1]), (tri[0,0], tri[0,1]), div=100))

    def triangles(self):
        """ DOCSTRING """

        return [Triangle(vertex[0,:], vertex[1,:], vertex[2,:]) for vertex in self.vertices]

    def _shaded(self):
        """ DOCSTRING """

        for triangle, color in zip(self.triangles(), self.fill_color):
            self.order.extend(triangle.fill(color))

    def _draw(self, canvas):
        """ DOCSTRING """


        self.project(canvas)

        # Scale into view
        self.translate(x=1.0, y=1.0)# [-1, 1] -> [0,2]
        self.translate(x=0.5*canvas.width, y=0.5*canvas.height, z=1.0, method="mul")

        self.sort()

        for texture in self.textures:
            self.textures[texture]['func'](*self.textures[texture]['params'])

        if self.wireframe:
            self._wireframe()


        for line in self.order:
            line._draw(canvas.canvas)

def w_pad(point):
    """ DOCSTRING """
    if len(point.shape) == 2: # Single point
        point = point.reshape((1, 3, 1))
    c, r, _ = point.shape
    return np.append(point, np.ones((c, r, 1)), axis=-1)

def w_matmul(i, j, pad=True):
    """ DOCSTRING """
    if pad:
        i = w_pad(i)
    o = i @ j
    i, w = o[:,:,:3], o[:,:,-1].reshape((-1, 3, 1))
    w = np.where(w==0, 1, w)
    return i / w

for i in range(10):
    canvas = display.Frame(Width, Height)
    canvas.mat_project = matProj

    vCamera = vec3d(0.0, 0.0, 0.0)
    meshCube = Mesh(
        # South
        Triangle(vec3d(0.0, 0.0, 0.0), vec3d(0.0, 1.0, 0.0), vec3d(1.0, 1.0, 0.0)),
        Triangle(vec3d(0.0, 0.0, 0.0), vec3d(1.0, 1.0, 0.0), vec3d(1.0, 0.0, 0.0)),

        # East
        Triangle(vec3d(1.0, 0.0, 0.0), vec3d(1.0, 1.0, 0.0), vec3d(1.0, 1.0, 1.0)),
        Triangle(vec3d(1.0, 0.0, 0.0), vec3d(1.0, 1.0, 1.0), vec3d(1.0, 0.0, 1.0)),

        # North
        Triangle(vec3d(1.0, 0.0, 1.0), vec3d(1.0, 1.0, 1.0), vec3d(0.0, 1.0, 1.0)),
        Triangle(vec3d(1.0, 0.0, 1.0), vec3d(0.0, 1.0, 1.0), vec3d(0.0, 0.0, 1.0)),

        # West
        Triangle(vec3d(0.0, 0.0, 1.0), vec3d(0.0, 1.0, 1.0), vec3d(0.0, 1.0, 0.0)),
        Triangle(vec3d(0.0, 0.0, 1.0), vec3d(0.0, 1.0, 0.0), vec3d(0.0, 0.0, 0.0)),

        # Top
        Triangle(vec3d(0.0, 1.0, 0.0), vec3d(0.0, 1.0, 1.0), vec3d(1.0, 1.0, 1.0)),
        Triangle(vec3d(0.0, 1.0, 0.0), vec3d(1.0, 1.0, 1.0), vec3d(1.0, 1.0, 0.0)),

        # Bottom
        Triangle(vec3d(1.0, 0.0, 1.0), vec3d(0.0, 0.0, 1.0), vec3d(0.0, 0.0, 0.0)),
        Triangle(vec3d(1.0, 0.0, 1.0), vec3d(0.0, 0.0, 0.0), vec3d(1.0, 0.0, 0.0)),
        )

    # meshCube = Mesh()
    # meshCube.from_obj("./tulip.obj")

    meshCube.rotate('z', fTheta+i*0.1)
    # meshCube.rotate('y', fTheta+i*0.1)
    meshCube.rotate('x', fTheta*0.5+i*0.1)
    meshCube.translate(z=8.0)

    meshCube.visible()
    meshCube.illuminate()

    # meshCube.fill()
    canvas.add(meshCube)
    CANVAS.add(canvas)
    # for tri, col in zip(meshCube.tris, meshCube.fill_color):
    #     DrawTriangle(*tri[:, :-1].reshape(-1), canvas)
        # canvas.add(Triangle(tri[0, :], tri[1, :], tri[2, :]).fill(col))
    # CANVAS.add(canvas)
CANVAS.fps = 1
CANVAS.show()

# Testing condition for Unit Mesh Cube: %timeit -n 100 with 100 internal frame it
# 7/18/22 Linear Algebra (Unoptimized): 2.48 s ± 21.2 ms per loop
# 7/18/22 Base Video: 2.8 s ± 70.8 ms per loop