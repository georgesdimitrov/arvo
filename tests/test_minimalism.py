import music21
import pytest
from arvo import minimalism
from arvo import sequences
from arvo.minimalism import Direction
from arvo.minimalism import StepMode


@pytest.fixture
def example_stream():
    s = music21.converter.parse("tinyNotation: C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4")
    return s


def _getStreamNotes(stream):
    notes = []
    for n in stream.flat.notes:
        notes.append(n.pitch.unicodeNameWithOctave)
    return notes


def test_additive_process(example_stream):
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
        C4 D4 E4 F4 G4 A4 B4 c4 d4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_direction_backward(example_stream):
    stream = minimalism.additive_process(example_stream, direction=Direction.BACKWARD)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        g4
        f4 g4  
        e4 f4 g4  
        d4 e4 f4 g4  
        c4 d4 e4 f4 g4  
        B4 c4 d4 e4 f4 g4  
        A4 B4 c4 d4 e4 f4 g4  
        G4 A4 B4 c4 d4 e4 f4 g4   
        F4 G4 A4 B4 c4 d4 e4 f4 g4   
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_direction_inward(example_stream):
    stream = minimalism.additive_process(example_stream, direction=Direction.INWARD)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 g4
        C4 D4 f4 g4  
        C4 D4 E4 e4 f4 g4   
        C4 D4 E4 F4 d4 e4 f4 g4
        C4 D4 E4 F4 G4 c4 d4 e4 f4 g4 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_direction_outward(example_stream):
    stream = minimalism.additive_process(example_stream, direction=Direction.OUTWARD)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        A4 B4
        G4 A4 B4 c4
        F4 G4 A4 B4 c4 d4
        E4 F4 G4 A4 B4 c4 d4 e4
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_step_int(example_stream):
    stream = minimalism.additive_process(example_stream, step=2)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 
        C4 D4 E4 F4 
        C4 D4 E4 F4 G4 A4 
        C4 D4 E4 F4 G4 A4 B4 c4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_step_sequence(example_stream):
    stream = minimalism.additive_process(example_stream, step=[1, 2, 3])
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4
        C4 D4 E4 
        C4 D4 E4 F4 G4 A4 
        C4 D4 E4 F4 G4 A4 B4 
        C4 D4 E4 F4 G4 A4 B4 c4 d4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
        """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_step_sequence_absolute(example_stream):
    stream = minimalism.additive_process(
        example_stream, step=sequences.PRIMES, step_mode=StepMode.ABSOLUTE
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 
        C4 D4 E4 
        C4 D4 E4 F4 G4 
        C4 D4 E4 F4 G4 A4 B4 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
        """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_step_sequence_absolute_infinite_loop(example_stream):
    stream = minimalism.additive_process(
        example_stream, step=[1, 2, 3], step_mode=StepMode.ABSOLUTE
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4
        C4 D4 
        C4 D4 E4 
        """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_repetitions_int(example_stream):
    stream = minimalism.additive_process(example_stream, repetitions=2)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4
        C4
        C4 D4 
        C4 D4 
        C4 D4 E4 
        C4 D4 E4 
        C4 D4 E4 F4 
        C4 D4 E4 F4 
        C4 D4 E4 F4 G4 
        C4 D4 E4 F4 G4 
        C4 D4 E4 F4 G4 A4 
        C4 D4 E4 F4 G4 A4 
        C4 D4 E4 F4 G4 A4 B4 
        C4 D4 E4 F4 G4 A4 B4 
        C4 D4 E4 F4 G4 A4 B4 c4
        C4 D4 E4 F4 G4 A4 B4 c4
        C4 D4 E4 F4 G4 A4 B4 c4 d4
        C4 D4 E4 F4 G4 A4 B4 c4 d4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_repetitions_sequence(example_stream):
    stream = minimalism.additive_process(example_stream, repetitions=[1, 2, 3])
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4
        C4 D4 
        C4 D4 
        C4 D4 E4 
        C4 D4 E4 
        C4 D4 E4 
        C4 D4 E4 F4 
        C4 D4 E4 F4 G4 
        C4 D4 E4 F4 G4 
        C4 D4 E4 F4 G4 A4 
        C4 D4 E4 F4 G4 A4 
        C4 D4 E4 F4 G4 A4 
        C4 D4 E4 F4 G4 A4 B4 
        C4 D4 E4 F4 G4 A4 B4 c4
        C4 D4 E4 F4 G4 A4 B4 c4
        C4 D4 E4 F4 G4 A4 B4 c4 d4
        C4 D4 E4 F4 G4 A4 B4 c4 d4
        C4 D4 E4 F4 G4 A4 B4 c4 d4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_additive_process_iterations(example_stream):
    stream = minimalism.additive_process(example_stream, iterations=8)
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


def test_additive_process_nonlinear(example_stream):
    stream = minimalism.additive_process(
        example_stream,
        step=sequences.kolakoski(),
        step_mode=StepMode.ABSOLUTE,
        iterations=8,
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4
        C4 D4     
        C4 D4     
        C4
        C4
        C4 D4     
        C4
        C4 D4     
        """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process(example_stream):
    stream = minimalism.subtractive_process(example_stream)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        F4 G4 A4 B4 c4 d4 e4 f4 g4   
        G4 A4 B4 c4 d4 e4 f4 g4   
        A4 B4 c4 d4 e4 f4 g4  
        B4 c4 d4 e4 f4 g4  
        c4 d4 e4 f4 g4  
        d4 e4 f4 g4  
        e4 f4 g4  
        f4 g4  
        g4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_direction_backward(example_stream):
    stream = minimalism.subtractive_process(
        example_stream, direction=Direction.BACKWARD
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4
        C4 D4 E4 F4 G4 A4 B4 c4 d4
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


def test_subtractive_process_direction_inward(example_stream):
    stream = minimalism.subtractive_process(example_stream, direction=Direction.INWARD)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4
        E4 F4 G4 A4 B4 c4 d4 e4
        F4 G4 A4 B4 c4 d4
        G4 A4 B4 c4
        A4 B4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_direction_outward(example_stream):
    stream = minimalism.subtractive_process(example_stream, direction=Direction.OUTWARD)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        C4 D4 E4 F4 G4 c4 d4 e4 f4 g4 
        C4 D4 E4 F4 d4 e4 f4 g4
        C4 D4 E4 e4 f4 g4   
        C4 D4 f4 g4  
        C4 g4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_step_int(example_stream):
    stream = minimalism.subtractive_process(example_stream, step=2)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        G4 A4 B4 c4 d4 e4 f4 g4   
        B4 c4 d4 e4 f4 g4  
        d4 e4 f4 g4  
        f4 g4  
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_step_sequence(example_stream):
    stream = minimalism.subtractive_process(example_stream, step=[1, 2, 3])
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        F4 G4 A4 B4 c4 d4 e4 f4 g4   
        B4 c4 d4 e4 f4 g4  
        c4 d4 e4 f4 g4  
        e4 f4 g4  
        """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_step_sequence_absolute(example_stream):
    stream = minimalism.subtractive_process(
        example_stream, step=sequences.PRIMES, step_mode=StepMode.ABSOLUTE
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        F4 G4 A4 B4 c4 d4 e4 f4 g4   
        A4 B4 c4 d4 e4 f4 g4  
        c4 d4 e4 f4 g4  
        g4
        """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_step_sequence_absolute_infinite_loop(example_stream):
    stream = minimalism.subtractive_process(
        example_stream, step=[1, 2, 3], step_mode=StepMode.ABSOLUTE
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        F4 G4 A4 B4 c4 d4 e4 f4 g4   
        """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_repetitions_int(example_stream):
    stream = minimalism.subtractive_process(example_stream, repetitions=2)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        F4 G4 A4 B4 c4 d4 e4 f4 g4   
        F4 G4 A4 B4 c4 d4 e4 f4 g4   
        G4 A4 B4 c4 d4 e4 f4 g4   
        G4 A4 B4 c4 d4 e4 f4 g4   
        A4 B4 c4 d4 e4 f4 g4  
        A4 B4 c4 d4 e4 f4 g4  
        B4 c4 d4 e4 f4 g4  
        B4 c4 d4 e4 f4 g4  
        c4 d4 e4 f4 g4  
        c4 d4 e4 f4 g4  
        d4 e4 f4 g4  
        d4 e4 f4 g4  
        e4 f4 g4  
        e4 f4 g4  
        f4 g4  
        f4 g4  
        g4   
        g4
        """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_repetitions_sequence(example_stream):
    stream = minimalism.subtractive_process(example_stream, repetitions=[1, 2, 3])
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        F4 G4 A4 B4 c4 d4 e4 f4 g4   
        G4 A4 B4 c4 d4 e4 f4 g4   
        G4 A4 B4 c4 d4 e4 f4 g4   
        A4 B4 c4 d4 e4 f4 g4  
        A4 B4 c4 d4 e4 f4 g4  
        A4 B4 c4 d4 e4 f4 g4  
        B4 c4 d4 e4 f4 g4  
        c4 d4 e4 f4 g4  
        c4 d4 e4 f4 g4  
        d4 e4 f4 g4  
        d4 e4 f4 g4  
        d4 e4 f4 g4  
        e4 f4 g4  
        f4 g4  
        f4 g4  
        g4
        g4
        g4
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_iterations(example_stream):
    stream = minimalism.subtractive_process(example_stream, iterations=8)
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        F4 G4 A4 B4 c4 d4 e4 f4 g4   
        G4 A4 B4 c4 d4 e4 f4 g4   
        A4 B4 c4 d4 e4 f4 g4  
        B4 c4 d4 e4 f4 g4  
        c4 d4 e4 f4 g4  
        d4 e4 f4 g4  
    """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)


def test_subtractive_process_nonlinear(example_stream):
    stream = minimalism.subtractive_process(
        example_stream,
        step=sequences.kolakoski(),
        step_mode=StepMode.ABSOLUTE,
        iterations=8,
    )
    intended_result = music21.converter.parse(
        """tinyNotation: 
        C4 D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4      
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        D4 E4 F4 G4 A4 B4 c4 d4 e4 f4 g4  
        E4 F4 G4 A4 B4 c4 d4 e4 f4 g4   
        """
    )

    assert _getStreamNotes(stream) == _getStreamNotes(intended_result)
