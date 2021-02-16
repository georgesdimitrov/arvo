import pytest
from arvo import transformations
from arvo import scales
from music21 import converter


@pytest.fixture
def major_scale():
    s = converter.parse("tinyNotation: C4 D4 E4 F4 G4 A4 B4 c4")
    return s


@pytest.fixture
def pentatonic_scale():
    s = converter.parse("tinyNotation: C4 D4 E4 G4 A4 c4")
    return s


def _getStreamNotes(original_stream):
    notes = []
    for n in original_stream.flat.notes:
        notes.append(n.pitch.nameWithOctave)
    return notes


def test_scalar_transposition(major_scale):
    result = transformations.scalar_transposition(major_scale, 1)
    intended_result = converter.parse(
        """tinyNotation: 
        C#4 E-4 F4 F#4 A-4 B-4 c4 c#4
    """
    )

    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_transposition_reference_scale(pentatonic_scale):
    result = transformations.scalar_transposition(
        pentatonic_scale, 2, reference_scale=scales.PentatonicScale("C")
    )
    intended_result = converter.parse(
        """tinyNotation: 
        E4 G4 A4 c4 d4 e4
    """
    )

    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_transposition_different_scales(major_scale):
    result = transformations.scalar_transposition(
        major_scale, 1, reference_scale=scales.PentatonicScale("C")
    )
    intended_result = converter.parse(
        """tinyNotation: 
            D4 E4 G4 G4 A4 c4 c4 d4
        """
    )

    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_transposition_in_place(major_scale):
    transformations.scalar_transposition(major_scale, 1, in_place=True)
    intended_result = converter.parse(
        """tinyNotation: 
        C#4 E-4 F4 F#4 A-4 B-4 c4 c#4
    """
    )

    assert _getStreamNotes(major_scale) == _getStreamNotes(intended_result)


def test_scalar_inversion(major_scale):
    result = transformations.scalar_inversion(major_scale, "C3")
    intended_result = converter.parse(
        """tinyNotation: 
       C4 BB-4 GG#4 GG4 FF4 EE-4 CC#4 CC4
    """
    )

    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_inversion_reference_scale(pentatonic_scale):
    result = transformations.scalar_inversion(
        pentatonic_scale, "C3", reference_scale=scales.PentatonicScale("C")
    )
    intended_result = converter.parse(
        """tinyNotation: 
        C4 AA4 GG4 EE4 DD4 CC4
    """
    )

    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_octave_shift(pentatonic_scale):
    result = transformations.octave_shift(pentatonic_scale, 1)
    intended_result = converter.parse(
        """tinyNotation: 
        c4 d4 e4 g4 a4 c'4
    """
    )

    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_inversion_in_place(major_scale):
    transformations.scalar_inversion(major_scale, "C3", in_place=True)
    intended_result = converter.parse(
        """tinyNotation: 
       C4 BB-4 GG#4 GG4 FF4 EE-4 CC#4 CC4
    """
    )

    assert _getStreamNotes(major_scale) == _getStreamNotes(intended_result)



