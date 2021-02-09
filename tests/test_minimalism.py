import pytest
import music21
from arvo import minimalism


@pytest.fixture
def example_stream():
    s = music21.converter.parse("tinyNotation: C4 D4 E4 F4 G4 A4 B4 c4")
    return s


def _getStreamNotes(stream):
    notes = []
    for n in stream.flat.notes:
        notes.append(n.pitch.unicodeNameWithOctave)
    return notes


def test_additive_process_default(example_stream):
    stream = minimalism.additive_process(example_stream)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4
        C4 D4 
        C4 D4 E4 
        C4 D4 E4 F4 
        C4 D4 E4 F4 G4 
        C4 D4 E4 F4 G4 A4 
        C4 D4 E4 F4 G4 A4 B4 
        C4 D4 E4 F4 G4 A4 B4 c4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_backward(example_stream):
    stream = minimalism.additive_process(
        example_stream, direction=minimalism.Direction.BACKWARD
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        c4  
        B4 c4
        A4 B4 c4
        G4 A4 B4 c4 
        F4 G4 A4 B4 c4 
        E4 F4 G4 A4 B4 c4 
        D4 E4 F4 G4 A4 B4 c4
        C4 D4 E4 F4 G4 A4 B4 c4      
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_inward(example_stream):
    stream = minimalism.additive_process(
        example_stream, direction=minimalism.Direction.INWARD
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 c4  
        C4 D4 B4 c4   
        C4 D4 E4 A4 B4 c4 
        C4 D4 E4 F4 G4 A4 B4 c4   
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_outward(example_stream):
    stream = minimalism.additive_process(
        example_stream, direction=minimalism.Direction.OUTWARD
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        F4 G4
        E4 F4 G4 A4
        D4 E4 F4 G4 A4 B4
        C4 D4 E4 F4 G4 A4 B4 c4  
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_substractive_process_default(example_stream):
    stream = minimalism.subtractive_process(example_stream)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4   
        D4 E4 F4 G4 A4 B4 c4
        E4 F4 G4 A4 B4 c4 
        F4 G4 A4 B4 c4 
        G4 A4 B4 c4 
        A4 B4 c4
        B4 c4
        c4  
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_backward(example_stream):
    stream = minimalism.subtractive_process(
        example_stream, direction=minimalism.Direction.BACKWARD
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4
        C4 D4 E4 F4 G4 A4 B4 
        C4 D4 E4 F4 G4 A4 
        C4 D4 E4 F4 G4 
        C4 D4 E4 F4 
        C4 D4 E4 
        C4 D4 
        C4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_inward(example_stream):
    stream = minimalism.subtractive_process(
        example_stream, direction=minimalism.Direction.INWARD
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4  
        D4 E4 F4 G4 A4 B4
        E4 F4 G4 A4
        F4 G4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_outward(example_stream):
    stream = minimalism.subtractive_process(
        example_stream, direction=minimalism.Direction.OUTWARD
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4   
        C4 D4 E4 A4 B4 c4 
        C4 D4 B4 c4   
        C4 c4  
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)
