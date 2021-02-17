"""
Module that extends music 21 scales system.
"""

__all__ = ["AbstractPentatonicScale", "PentatonicScale"]

import music21
from music21.scale import intervalNetwork


class AbstractPentatonicScale(music21.scale.AbstractScale):
    def __init__(self, mode=None):
        super().__init__()
        self.type = "Abstract Pentatonic"
        # all pentatonic scales are octave duplicating
        self.octaveDuplicating = True
        # here, accept None
        self.buildNetwork(mode=mode)

    def buildNetwork(self, mode=None):
        src_list = ("M2", "M2", "m3", "M2", "m3")
        if mode in (None, 1, "major", "Major"):
            interval_list = src_list
            self.tonicDegree = 1
        elif mode in (2):
            interval_list = src_list[1:] + src_list[:1]
            self.tonicDegree = 1
        elif mode in (3):
            interval_list = src_list[2:] + src_list[:2]
            self.tonicDegree = 1
        elif mode in (4):
            interval_list = src_list[3:] + src_list[:3]
            self.tonicDegree = 1
        elif mode in (5, "minor", "Minor"):
            interval_list = src_list[4:] + src_list[:4]
            self.tonicDegree = 1
        else:
            raise music21.scale.ScaleException(
                f"cannot create a scale of the following mode: {mode}"
            )
        self._net = intervalNetwork.IntervalNetwork(
            interval_list,
            octaveDuplicating=self.octaveDuplicating,
            pitchSimplification="none",
        )
        # might also set weights for tonic and dominant here


class PentatonicScale(music21.scale.ConcreteScale):
    usePitchDegreeCache = True

    def __init__(self, tonic=None, mode=None):
        super().__init__(tonic=tonic)
        self._abstract = AbstractPentatonicScale(mode=mode)
        self.type = "Pentatonic"
