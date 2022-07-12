# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:41:18 2022

@author: micha
"""

import os
import sys

import numpy as np

minimal_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, minimal_dir)
from minimal import objects, display

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

canvas = display.Canvas(Width, Height)

class vec3d:
    """ DOCSTRING """
    def __init__(self, x, y, z=0):

        self.x = x
        self.y = y
        self.z = z

        self.xyz = np.array([[x, y, z]])

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, z={self.z})'

class triangle:
    """ DOCSTRING """
    def __init__(self, p1, p2, p3):

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.p = np.array([*p1.xyz, *p2.xyz, *p3.xyz])

    def __repr__(self):
        return repr(self.p)

class mesh:
    """ DOCSTRING """
    def __init__(self, *args):

        self.tris = np.array([arg.p for arg in args])

    def w_matmul(self, other):
        """ DOCSTRING """
        tris = np.append(self.tris, np.ones((len(self.tris), 3, 1)), axis=-1)
        o = tris @ other
        tris, w = o[:,:,:3], o[:,:,-1].reshape((-1, 3, 1))
        w = np.where(w==0, 1, w)
        return tris / w

    def __repr__(self):
        return repr(self.tris.reshape((1,-1,9)))

def MultiplyMatrixVector(point, matrix):
    """ DOCSTRING """
    o = point @ matrix
    if o[-1] != 0.0:
        o /= o[-1]
    return o

def DrawTriangle(x1, y1, x2, y2, x3, y3, canvas):
    canvas.add(objects.Line((x1, y1), (x2, y2), div=2))
    canvas.add(objects.Line((x2, y2), (x3, y3), div=2))
    canvas.add(objects.Line((x3, y3), (x1, y1), div=2))

matRotZ = np.zeros((4,4))
matRotZ[0,0] = np.cos(fTheta)
matRotZ[0,1] = np.sin(fTheta)
matRotZ[1,0] = -np.sin(fTheta)
matRotZ[1,1] = np.cos(fTheta)
matRotZ[2,2] = 1.0
matRotZ[3,3] = 1.0

matRotX = np.zeros((4,4))
matRotX[0,0] = 1.0
matRotX[1,1] = np.cos(fTheta * 0.5)
matRotX[1,2] = np.sin(fTheta * 0.5)
matRotX[2,1] = -np.sin(fTheta * 0.5)
matRotX[2,2] = np.cos(fTheta * 0.5)
matRotX[3,3] = 1.0

meshCube = mesh(
    # South
    triangle(vec3d(0.0, 0.0, 0.0), vec3d(0.0, 1.0, 0.0), vec3d(1.0, 1.0, 1.0)),
    triangle(vec3d(0.0, 0.0, 0.0), vec3d(1.0, 1.0, 0.0), vec3d(1.0, 0.0, 0.0)),

    # East
    triangle(vec3d(1.0, 0.0, 0.0), vec3d(1.0, 1.0, 0.0), vec3d(1.0, 1.0, 1.0)),
    triangle(vec3d(1.0, 0.0, 0.0), vec3d(1.0, 1.0, 1.0), vec3d(1.0, 0.0, 1.0)),

    # North
    triangle(vec3d(1.0, 0.0, 1.0), vec3d(1.0, 1.0, 1.0), vec3d(0.0, 1.0, 1.0)),
    triangle(vec3d(1.0, 0.0, 1.0), vec3d(0.0, 1.0, 1.0), vec3d(0.0, 0.0, 1.0)),

    # West
    triangle(vec3d(0.0, 0.0, 1.0), vec3d(0.0, 1.0, 1.0), vec3d(0.0, 1.0, 0.0)),
    triangle(vec3d(0.0, 0.0, 1.0), vec3d(0.0, 1.0, 0.0), vec3d(0.0, 0.0, 0.0)),

    # Top
    triangle(vec3d(0.0, 1.0, 0.0), vec3d(0.0, 1.0, 1.0), vec3d(1.0, 1.0, 1.0)),
    triangle(vec3d(0.0, 1.0, 0.0), vec3d(1.0, 1.0, 1.0), vec3d(1.0, 1.0, 0.0)),

    # Bottom
    triangle(vec3d(1.0, 0.0, 1.0), vec3d(0.0, 0.0, 1.0), vec3d(0.0, 0.0, 0.0)),
    triangle(vec3d(1.0, 0.0, 1.0), vec3d(0.0, 0.0, 0.0), vec3d(1.0, 0.0, 0.0)),
    )

meshCube.tris = meshCube.w_matmul(matRotZ)
meshCube.tris = meshCube.w_matmul(matRotX)
meshCube.tris = meshCube.tris + np.repeat(np.array([[0.0, 0.0, 3.0]]), 3, axis=0) # Just need for Z
meshCube.tris = meshCube.w_matmul(matProj)
meshCube.tris = meshCube.tris + np.repeat(np.array([[1.0, 1.0, 0.0]]), 3, axis=0) # Just need for X and Y
meshCube.tris = meshCube.tris * np.repeat(np.array([[0.5 * Width, 0.5 * Height, 1.0]]), 3, axis=0)
for tri in meshCube.tris:
    DrawTriangle(*tri[:, :-1].reshape(-1), canvas)
canvas.show()