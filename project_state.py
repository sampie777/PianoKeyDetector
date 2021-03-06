from typing import List, Optional

import numpy as np

from config import Config
from models import Key

fps: int = 0
frame_shape: tuple = (-1, -1)
is_image: bool = False
zone_bounds: Optional[np.ndarray] = Config.zone_bounds
mask_area: Optional[np.ndarray] = Config.mask_area

keys = [    # generated by profile 3
    # Key("C0", is_calibrated=True, color=(255, 54, 201), line=[(339, 397), (344, 410)]),
    Key("C#0", is_calibrated=True, color=(255, 54, 201), line=[(339, 397), (344, 410)]),
    Key("D0", is_calibrated=True, color=(255, 107, 148), line=[(352, 397), (357, 412)]),
    Key("D#0", is_calibrated=True, color=(255, 161, 94), line=[(364, 396), (369, 409)]),
    Key("E0", is_calibrated=True, color=(255, 214, 41), line=[(377, 395), (382, 411)]),
    Key("F0", is_calibrated=True, color=(255, 13, 242), line=[(388, 392), (394, 411)]),
    Key("F#0", is_calibrated=True, color=(255, 66, 189), line=[(399, 391), (405, 408)]),
    Key("G0", is_calibrated=True, color=(255, 120, 135), line=[(410, 392), (415, 406)]),
    Key("G#0", is_calibrated=True, color=(255, 173, 82), line=[(421, 393), (426, 407)]),
    Key("A0", is_calibrated=True, color=(255, 227, 28), line=[(432, 393), (438, 409)]),
    Key("A#0", is_calibrated=True, color=(255, 25, 230), line=[(444, 394), (450, 411)]),
    Key("B0", is_calibrated=True, color=(255, 79, 176), line=[(456, 394), (460, 407)]),
    Key("C1", is_calibrated=True, color=(255, 133, 122), line=[(467, 391), (473, 409)]),
    Key("C#1", is_calibrated=True, color=(255, 186, 69), line=[(479, 391), (486, 412)]),
    Key("D1", is_calibrated=True, color=(255, 240, 15), line=[(491, 391), (497, 408)]),
    Key("D#1", is_calibrated=True, color=(255, 38, 217), line=[(503, 390), (509, 407)]),
    Key("E1", is_calibrated=True, color=(255, 92, 163), line=[(515, 388), (523, 412)]),
    Key("F1", is_calibrated=True, color=(255, 145, 110), line=[(528, 389), (535, 410)]),
    Key("F#1", is_calibrated=True, color=(255, 199, 56), line=[(540, 387), (546, 407)]),
    Key("G1", is_calibrated=True, color=(255, 252, 3), line=[(553, 387), (561, 410)]),
    Key("G#1", is_calibrated=True, color=(255, 51, 204), line=[(567, 387), (574, 409)]),
    Key("A1", is_calibrated=True, color=(255, 105, 150), line=[(581, 387), (590, 414)]),
    Key("A#1", is_calibrated=True, color=(255, 158, 97), line=[(595, 387), (603, 413)]),
    Key("B1", is_calibrated=True, color=(255, 212, 43), line=[(608, 384), (616, 409)]),
    Key("C2", is_calibrated=True, color=(255, 10, 245), line=[(623, 384), (630, 409)]),
    Key("C#2", is_calibrated=True, color=(255, 64, 191), line=[(637, 381), (643, 401)]),
    Key("D2", is_calibrated=True, color=(255, 117, 138), line=[(653, 381), (661, 405)]),
    Key("D#2", is_calibrated=True, color=(255, 171, 84), line=[(667, 379), (675, 405)]),
    Key("E2", is_calibrated=True, color=(255, 224, 31), line=[(683, 386), (705, 391)]),
    Key("F2", is_calibrated=True, color=(255, 23, 232), line=[(707, 380), (734, 405)]),
]
