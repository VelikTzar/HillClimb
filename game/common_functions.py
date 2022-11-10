import math
import pygame
import pymunk
from pymunk import Vec2d


def convert_coordinates(p, height):
    """Convert chipymunkunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+height)