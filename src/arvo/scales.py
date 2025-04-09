"""Extends the music21 scale system with support for standard pentatonic scales.

Includes abstract and concrete representations of the common 5-note
pentatonic scale (Set 5-35), supporting different modes and integration
with music21.
"""

__all__ = ["AbstractPentatonicScale", "PentatonicScale"]

import music21
from music21.scale import intervalNetwork


class AbstractPentatonicScale(music21.scale.AbstractScale):
    """An abstract representation of the standard pentatonic scale (Set 5-35),
    supporting modal rotation.
    """

    def __init__(self, mode: int | str | None = None):
        super().__init__()
        self.type = "Abstract Pentatonic"
        # all pentatonic scales are octave duplicating
        self.octaveDuplicating = True
        # here, accept None
        self.buildNetwork(mode=mode)

    def buildNetwork(self, mode: int | str | None = None) -> None:
        src_list = ("M2", "M2", "m3", "M2", "m3")
        if mode in (None, 1, "major", "Major"):
            interval_list = src_list
        elif mode == 2:
            interval_list = src_list[1:] + src_list[:1]
        elif mode == 3:
            interval_list = src_list[2:] + src_list[:2]
        elif mode == 4:
            interval_list = src_list[3:] + src_list[:3]
        elif mode in (5, "minor", "Minor"):
            interval_list = src_list[4:] + src_list[:4]
        else:
            raise music21.scale.ScaleException(
                f"Cannot create a scale with the specified mode: {mode}"
            )
        self.tonicDegree = 1
        self._net = intervalNetwork.IntervalNetwork(
            interval_list,
            octaveDuplicating=self.octaveDuplicating,
            pitchSimplification="none",
        )
        # might also set weights for tonic and dominant here


class PentatonicScale(music21.scale.ConcreteScale):
    """A concrete pentatonic scale in one of five modes."""

    usePitchDegreeCache = True

    def __init__(
        self,
        tonic: music21.pitch.Pitch | str | None = None,
        mode: int | str | None = None,
    ):
        super().__init__(tonic=tonic)
        self._abstract = AbstractPentatonicScale(mode=mode)
        self.type = "Pentatonic"
