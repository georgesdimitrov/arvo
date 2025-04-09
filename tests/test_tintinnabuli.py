import pytest
from music21 import converter
from music21 import chord
from music21 import stream
from music21 import note
from music21 import duration
from arvo import tintinnabuli
from arvo import tools


@pytest.fixture
def major_scale():
    s = converter.parse("tinyNotation: C D E F G A B c")
    return s


@pytest.fixture
def c_major_chord():
    c = chord.Chord(["C", "E", "G"])
    return c


def test_create_t_voice(major_scale, c_major_chord):
    result = tintinnabuli.create_t_voice(major_scale, c_major_chord)
    intended_result = converter.parse("tinyNotation: E E G G c c c e")
    assert list(result.flat.notes) == list(intended_result.flat.notes)


@pytest.mark.parametrize(
    "position,intended_result",
    [
        (2, converter.parse("tinyNotation: G G c c e e e g")),
        (3, converter.parse("tinyNotation: c c e e g g g c'")),
    ],
)
def test_create_t_voice_position(major_scale, c_major_chord, position, intended_result):
    options = tintinnabuli.Options(position=position)
    result = tintinnabuli.create_t_voice(major_scale, c_major_chord, options)
    assert list(result.flat.notes) == list(intended_result.flat.notes)


@pytest.mark.parametrize(
    "direction,intended_result",
    [
        (
            tintinnabuli.Direction.DOWN,
            converter.parse("tinyNotation: GG C C E E G G G"),
        ),
        (
            tintinnabuli.Direction.UP_ALTERNATE,
            converter.parse("tinyNotation: E C G E c G c G"),
        ),
        (
            tintinnabuli.Direction.DOWN_ALTERNATE,
            converter.parse("tinyNotation: GG E C G E c G e"),
        ),
    ],
)
def test_create_t_voice_direction(
    major_scale, c_major_chord, direction, intended_result
):
    options = tintinnabuli.Options(direction=direction)
    result = tintinnabuli.create_t_voice(major_scale, c_major_chord, options)
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_create_t_voice_pitch_list(major_scale):
    result = tintinnabuli.create_t_voice(major_scale, ("C", "D", "A"))
    intended_result = converter.parse("tinyNotation: D A A A A c c d")
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_create_t_voice_pitch_list_numeric(major_scale):
    result = tintinnabuli.create_t_voice(major_scale, (0, 2, 9))
    intended_result = converter.parse("tinyNotation: D A A A A c c d")
    assert list(result.flat.notes) == list(intended_result.flat.notes)


@pytest.mark.parametrize(
    "t_mode,intended_result",
    [
        (
            tintinnabuli.TMode.DIATONIC,
            converter.parse("tinyNotation: E E A A A c# c# e"),
        ),
        (
            tintinnabuli.TMode.CHROMATIC,
            converter.parse("tinyNotation: C# E A A A c# c# c#"),
        ),
    ],
)
def test_create_t_voice_tmode(major_scale, t_mode, intended_result):
    options = tintinnabuli.Options(mode=t_mode)
    result = tintinnabuli.create_t_voice(major_scale, ("C#", "E", "A"), options)
    assert list(result.flatten().notes) == list(intended_result.flatten().notes)

def test_create_t_voice_stream(c_major_chord):
    m_voice = stream.Stream()
    m_voice.append(note.Note(pitch="C4", duration=duration.Duration(2)))
    m_voice.append(note.Note(pitch="D4",  duration=duration.Duration(1)))
    m_voice.append(note.Note(pitch="E4", duration=duration.Duration(3)))

    intended_result = stream.Stream()
    intended_result.append(note.Note(pitch="E4", duration=duration.Duration(2)))
    intended_result.append(note.Note(pitch="E4", duration=duration.Duration(1)))
    intended_result.append(note.Note(pitch="G4", duration=duration.Duration(3)))
    result = tintinnabuli.create_t_voice(m_voice, c_major_chord)

    score = tools.merge_streams(m_voice, result)
    assert list(result.flatten().notes) == list(intended_result.flatten().notes)
