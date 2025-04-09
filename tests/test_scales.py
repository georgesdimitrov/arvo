import random

import pytest
from music21 import converter
from music21 import note
from music21 import scale
from music21 import pitch
from arvo import scales

def test_pentatonic_scale_strings():
    pentatonic_scale = scales.PentatonicScale("C")
    result = pentatonic_scale.getPitches("c4", "c5")
    expected_result = [
        pitch.Pitch("c4"),
        pitch.Pitch("d4"),
        pitch.Pitch("e4"),
        pitch.Pitch("g4"),
        pitch.Pitch("a4"),
        pitch.Pitch("c5"),
    ]

    assert result == expected_result

def test_pentatonic_scale_pitches():
    pentatonic_scale = scales.PentatonicScale(pitch.Pitch(50), mode=3)
    result = pentatonic_scale.getPitches(pitch.Pitch(50), pitch.Pitch(61))
    expected_result = [
        pitch.Pitch(50),
        pitch.Pitch(53),
        pitch.Pitch(55),
        pitch.Pitch(58),
        pitch.Pitch(60),
    ]

    assert [p.ps for p in result] == [p.ps for p in expected_result]
