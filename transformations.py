from constants import Width, Height
from primatives.vector import Vector3


def to_pygame_space(vector:Vector3):
    vector = vector * Vector3(1, -1, 1) + Vector3(1, 1, 0)
    vector = vector * Vector3(Width, Height, 1) * 0.5
    return vector

def from_pygame_to_clip_space(tuple):
    assert len(tuple) == 2
    x = ((tuple[0] / 0.5 / Width) - 1) / 1
    y = ((tuple[1] / 0.5 / Height) - 1) / (-1)
    return (x,y)