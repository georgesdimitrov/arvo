import pytest
from music21 import converter, pitch, duration, chord, stream
from arvo import isorhythm
from arvo import tools
from arvo import core


@pytest.fixture
def example_pitches_stream():
    return converter.parse("tinyNotation: C D E F G")


@pytest.fixture
def example_chords_sequence():
    return [
        chord.Chord(["C4", "E4", "G4"]),
        chord.Chord(["C4", "F4", "A4"]),
    ]


@pytest.fixture
def example_durations_sequence():
    return [1, 1, 2]


@pytest.mark.parametrize(
    "pitches",
    [
        # Stream
        converter.parse("tinyNotation: C D E F G"),
        # List of numbers
        [48, 50, 52, 53, 55],
        # List of strings
        ["C3", "D3", "E3", "F3", "G3"],
        # List of notes
        list(converter.parse("tinyNotation: C D E F G").flat.notes),
        # Iterator of notes
        converter.parse("tinyNotation: C D E F G").flat.notes,
        # List of pitches
        [
            pitch.Pitch("C3"),
            pitch.Pitch("D3"),
            pitch.Pitch("E3"),
            pitch.Pitch("F3"),
            pitch.Pitch("G3"),
        ],
    ],
)
@pytest.mark.parametrize(
    "rhythms",
    [
        # Stream
        converter.parse("tinyNotation: C4 C4 C2"),
        # List of numbers
        [1, 1, 2],
        # List of durations
        [
            duration.Duration(1),
            duration.Duration(1),
            duration.Duration(2),
        ],
        # List of notes
        list(converter.parse("tinyNotation: C4 C4 C2").flat.notes),
        # Iterator of notes
        converter.parse("tinyNotation: C4 C4 C2").flat.notes,
    ],
)
def test_create_isorhythm(pitches, rhythms):
    result = isorhythm.create_isorhythm(pitches, rhythms)
    intended_result = converter.parse(
        """
        tinyNotation: C4 D4 E2 F4 G4 C2 D4 E4 F2 G4 C4 D2 E4 F4 G2 
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_create_isorhythm_length(
    example_pitches_stream, example_durations_sequence
):
    options = isorhythm.Options(length=18)
    result = isorhythm.create_isorhythm(
        example_pitches_stream, example_durations_sequence, options
    )
    intended_result = converter.parse(
        """
        tinyNotation: C4 D4 E2 F4 G4 C2 D4 E4 F2 G4 C4 D2 E4 F4 G2 C4 D4 E2
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_create_isorhythm_chords(
            example_chords_sequence, example_durations_sequence
    ):
    result = isorhythm.create_isorhythm(
        example_chords_sequence, example_durations_sequence)

    c1 = chord.Chord(["C4", "E4", "G4"])
    c2 = chord.Chord(["C4", "F4", "A4"])
    intended_result = stream.Stream()
    intended_result.append(tools.create_note(c1, 1))
    intended_result.append(tools.create_note(c2, 1))
    intended_result.append(tools.create_note(c1, 2))
    intended_result.append(tools.create_note(c2, 1))
    intended_result.append(tools.create_note(c1, 1))
    intended_result.append(tools.create_note(c2, 2))

    assert list(result.flat.notes) == list(intended_result.flat.notes)
