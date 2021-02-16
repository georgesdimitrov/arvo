import pytest
from arvo import transformations
from arvo import scales
from music21 import converter


@pytest.fixture
def major_scale():
    s = converter.parse("tinyNotation: C D E F G A B c")
    return s


@pytest.fixture
def pentatonic_scale():
    s = converter.parse("tinyNotation: C D E G A c")
    return s


def _getStreamNotes(original_stream):
    notes = []
    for n in original_stream.flat.notes:
        notes.append(n.pitch.nameWithOctave)
    return notes


def test_scalar_transposition(major_scale):
    result = transformations.scalar_transposition(major_scale, 1)
    intended_result = converter.parse("tinyNotation: C# E- F F# A- B- c c#")
    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_transposition_reference_scale(pentatonic_scale):
    result = transformations.scalar_transposition(
        pentatonic_scale, 2, reference_scale=scales.PentatonicScale("C")
    )
    intended_result = converter.parse("tinyNotation: E G A c d e")
    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_transposition_different_scales(major_scale):
    result = transformations.scalar_transposition(
        major_scale, 1, reference_scale=scales.PentatonicScale("C")
    )
    intended_result = converter.parse("tinyNotation: D E G G A c c d")
    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_transposition_in_place(major_scale):
    transformations.scalar_transposition(major_scale, 1, in_place=True)
    intended_result = converter.parse("tinyNotation: C# E- F F# A- B- c c#")
    assert _getStreamNotes(major_scale) == _getStreamNotes(intended_result)


def test_scalar_inversion(major_scale):
    result = transformations.scalar_inversion(major_scale, "C3")
    intended_result = converter.parse("tinyNotation: C BB- GG# GG FF EE- CC# CC")
    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_inversion_reference_scale(pentatonic_scale):
    result = transformations.scalar_inversion(
        pentatonic_scale, "C3", reference_scale=scales.PentatonicScale("C")
    )
    intended_result = converter.parse("tinyNotation: C AA GG EE DD CC")
    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_octave_shift(pentatonic_scale):
    result = transformations.octave_shift(pentatonic_scale, 1)
    intended_result = converter.parse("tinyNotation: c d e g a c'")
    assert _getStreamNotes(result) == _getStreamNotes(intended_result)


def test_scalar_inversion_in_place(major_scale):
    transformations.scalar_inversion(major_scale, "C3", in_place=True)
    intended_result = converter.parse("tinyNotation: C BB- GG# GG FF EE- CC# CC")
    assert _getStreamNotes(major_scale) == _getStreamNotes(intended_result)
