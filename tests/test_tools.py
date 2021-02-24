import pytest
from music21 import converter
from music21 import pitch
from music21 import note
from music21 import duration
from arvo import tools


@pytest.fixture
def pitches_stream():
    return converter.parse("tinyNotation: C D E F# G")


@pytest.fixture()
def durations_stream():
    return converter.parse("tinyNotation: c2 c1 c4 c8")


@pytest.mark.parametrize(
    "sequence",
    [
        ["C3", "D3", "E3", "F#3", "G3"],
        [48, 50, 52, 54, 55],
        [
            pitch.Pitch("C3"),
            pitch.Pitch("D3"),
            pitch.Pitch("E3"),
            pitch.Pitch("F#3"),
            pitch.Pitch("G3"),
        ],
        [
            note.Note("C3"),
            note.Note("D3"),
            note.Note("E3"),
            note.Note("F#3"),
            note.Note("G3"),
        ],
    ],
)
def test_pitches_to_stream(pitches_stream, sequence):
    result = tools.notes_to_stream(sequence)
    assert list(result.flat.notes) == list(pitches_stream.flat.notes)


@pytest.mark.parametrize(
    "sequence",
    [
        [2, 4, 1, 0.5],
        [
            duration.Duration(2),
            duration.Duration(4),
            duration.Duration(1),
            duration.Duration(0.5),
        ],
        [
            note.Note(duration=duration.Duration(2)),
            note.Note(duration=duration.Duration(4)),
            note.Note(duration=duration.Duration(1)),
            note.Note(duration=duration.Duration(0.5)),
        ],
    ],
)
def test_durations_to_stream(durations_stream, sequence):
    result = tools.durations_to_stream(sequence)
    assert list(result.flat.notes) == list(durations_stream.flat.notes)
