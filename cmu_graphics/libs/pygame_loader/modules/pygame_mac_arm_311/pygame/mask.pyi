from typing import Any, List, Optional, Sequence, Tuple, Union

from pygame.rect import Rect
from pygame.surface import Surface

from ._common import ColorValue, Coordinate, RectValue

def from_surface(surface: Surface, threshold: int = 127) -> Mask: ...
def from_threshold(
    surface: Surface,
    color: ColorValue,
    threshold: ColorValue = (0, 0, 0, 255),
    othersurface: Optional[Surface] = None,
    palette_colors: int = 1,
) -> Mask: ...

class Mask:
    def __init__(self, size: Coordinate, fill: bool = False) -> None: ...
    def __copy__(self) -> Mask: ...
    copy = __copy__
    def get_size(self) -> Tuple[int, int]: ...
    def get_rect(self, **kwargs: Any) -> Rect: ...  # Dict type needs to be completed
    def get_at(self, pos: Coordinate) -> int: ...
    def set_at(self, pos: Coordinate, value: int = 1) -> None: ...
    def overlap(self, other: Mask, offset: Coordinate) -> Optional[Tuple[int, int]]: ...
    def overlap_area(self, other: Mask, offset: Coordinate) -> int: ...
    def overlap_mask(self, other: Mask, offset: Coordinate) -> Mask: ...
    def fill(self) -> None: ...
    def clear(self) -> None: ...
    def invert(self) -> None: ...
    def scale(self, scale: Coordinate) -> Mask: ...
    def draw(self, other: Mask, offset: Coordinate) -> None: ...
    def erase(self, other: Mask, offset: Coordinate) -> None: ...
    def count(self) -> int: ...
    def centroid(self) -> Tuple[int, int]: ...
    def angle(self) -> float: ...
    def outline(self, every: int = 1) -> List[Tuple[int, int]]: ...
    def convolve(
        self,
        other: Mask,
        output: Optional[Mask] = None,
        offset: Coordinate = (0, 0),
    ) -> Mask: ...
    def connected_component(
        self, pos: Union[Sequence[int], Tuple[int, int]] = ...
    ) -> Mask: ...
    def connected_components(self, minimum: int = 0) -> List[Mask]: ...
    def get_bounding_rects(self) -> Rect: ...
    def to_surface(
        self,
        surface: Optional[Surface] = None,
        setsurface: Optional[Surface] = None,
        unsetsurface: Optional[Surface] = None,
        setcolor: Optional[ColorValue] = (255, 255, 255, 255),
        unsetcolor: Optional[ColorValue] = (0, 0, 0, 255),
        dest: Union[RectValue, Coordinate] = (0, 0),
    ) -> Surface: ...

MaskType = Mask
