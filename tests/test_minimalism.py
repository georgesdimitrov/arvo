import pytest
from music21 import converter
from arvo import minimalism
from arvo import sequences


@pytest.fixture
def example_stream_even():
    s = converter.parse("tinyNotation: C D E F G A B c d e f g")
    return s


@pytest.fixture
def example_stream_odd():
    s = converter.parse("tinyNotation: C D E F G A B c d e f")
    return s


# Additive Process Tests


def test_additive_process_even(example_stream_even):
    result = minimalism.additive_process(example_stream_even)
    intended_result = converter.parse(
        """tinyNotation: 
        C
        C D 
        C D E 
        C D E F 
        C D E F G 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c
        C D E F G A B c d
        C D E F G A B c d e
        C D E F G A B c d e f
        C D E F G A B c d e f g
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_odd(example_stream_odd):
    result = minimalism.additive_process(example_stream_odd)
    intended_result = converter.parse(
        """tinyNotation: 
        C
        C D 
        C D E 
        C D E F 
        C D E F G 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c
        C D E F G A B c d
        C D E F G A B c d e
        C D E F G A B c d e f
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


@pytest.mark.parametrize(
    "direction,intended_result",
    [
        (
            minimalism.Direction.BACKWARD,
            converter.parse(
                """tinyNotation: 
        g
        f g  
        e f g  
        d e f g  
        c d e f g  
        B c d e f g  
        A B c d e f g  
        G A B c d e f g   
        F G A B c d e f g   
        E F G A B c d e f g   
        D E F G A B c d e f g  
        C D E F G A B c d e f g      
    """
            ),
        ),
        (
            minimalism.Direction.INWARD,
            converter.parse(
                """tinyNotation: 
        C g
        C D f g  
        C D E e f g   
        C D E F d e f g
        C D E F G c d e f g 
        C D E F G A B c d e f g   
    """
            ),
        ),
        (
            minimalism.Direction.OUTWARD,
            converter.parse(
                """tinyNotation: 
        A B
        G A B c
        F G A B c d
        E F G A B c d e
        D E F G A B c d e f
        C D E F G A B c d e f g
    """
            ),
        ),
    ],
)
def test_additive_process_direction_even(
    example_stream_even, direction, intended_result
):
    result = minimalism.additive_process(example_stream_even, direction=direction)
    assert list(result.flat.notes) == list(intended_result.flat.notes)


@pytest.mark.parametrize(
    "direction,intended_result",
    [
        (
            minimalism.Direction.BACKWARD,
            converter.parse(
                """tinyNotation: 
        f   
        e f   
        d e f   
        c d e f   
        B c d e f   
        A B c d e f   
        G A B c d e f    
        F G A B c d e f    
        E F G A B c d e f    
        D E F G A B c d e f   
        C D E F G A B c d e f       
    """
            ),
        ),
        (
            minimalism.Direction.INWARD,
            converter.parse(
                """tinyNotation: 
        C f
        C D e f  
        C D E d e f   
        C D E F c d e f 
        C D E F G B c d e f 
        C D E F G A B c d e f   
    """
            ),
        ),
        (
            minimalism.Direction.OUTWARD,
            converter.parse(
                """tinyNotation: 
        A
        G A B
        F G A B c
        E F G A B c d
        D E F G A B c d e
        C D E F G A B c d e f
    """
            ),
        ),
    ],
)
def test_additive_process_direction_odd(example_stream_odd, direction, intended_result):
    result = minimalism.additive_process(example_stream_odd, direction=direction)
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_step_value_int(example_stream_even):
    result = minimalism.additive_process(example_stream_even, step_value=2)
    intended_result = converter.parse(
        """tinyNotation: 
        C D 
        C D E F 
        C D E F G A 
        C D E F G A B c
        C D E F G A B c d e
        C D E F G A B c d e f g
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_step_value_sequence(example_stream_even):
    result = minimalism.additive_process(example_stream_even, step_value=[1, 2, 3])
    intended_result = converter.parse(
        """tinyNotation: 
        C
        C D E 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c d
        C D E F G A B c d e f g
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_step_value_sequence_absolute(example_stream_even):
    result = minimalism.additive_process(
        example_stream_even,
        step_value=sequences.PRIMES,
        step_mode=minimalism.StepMode.ABSOLUTE,
    )
    intended_result = converter.parse(
        """tinyNotation: 
        C D 
        C D E 
        C D E F G 
        C D E F G A B 
        C D E F G A B c d e f
        C D E F G A B c d e f g
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_step_value_sequence_absolute_infinite_loop(
    example_stream_even,
):
    result = minimalism.additive_process(
        example_stream_even,
        step_value=[1, 2, 3],
        step_mode=minimalism.StepMode.ABSOLUTE,
    )
    intended_result = converter.parse(
        """tinyNotation: 
        C
        C D 
        C D E 
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_repetitions_int(example_stream_even):
    result = minimalism.additive_process(example_stream_even, repetitions=2)
    intended_result = converter.parse(
        """tinyNotation: 
        C
        C
        C D 
        C D 
        C D E 
        C D E 
        C D E F 
        C D E F 
        C D E F G 
        C D E F G 
        C D E F G A 
        C D E F G A 
        C D E F G A B 
        C D E F G A B 
        C D E F G A B c
        C D E F G A B c
        C D E F G A B c d
        C D E F G A B c d
        C D E F G A B c d e
        C D E F G A B c d e
        C D E F G A B c d e f
        C D E F G A B c d e f
        C D E F G A B c d e f g
        C D E F G A B c d e f g
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_repetitions_sequence(example_stream_even):
    result = minimalism.additive_process(example_stream_even, repetitions=[1, 2, 3])
    intended_result = converter.parse(
        """tinyNotation: 
        C
        C D 
        C D 
        C D E 
        C D E 
        C D E 
        C D E F 
        C D E F G 
        C D E F G 
        C D E F G A 
        C D E F G A 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c
        C D E F G A B c
        C D E F G A B c d
        C D E F G A B c d
        C D E F G A B c d
        C D E F G A B c d e
        C D E F G A B c d e f
        C D E F G A B c d e f
        C D E F G A B c d e f g
        C D E F G A B c d e f g
        C D E F G A B c d e f g
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_iterations_start(example_stream_even):
    result = minimalism.additive_process(example_stream_even, iterations_start=3)
    intended_result = converter.parse(
        """tinyNotation: 
        C D E 
        C D E F 
        C D E F G 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c
        C D E F G A B c d
        C D E F G A B c d e
        C D E F G A B c d e f
        C D E F G A B c d e f g
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_iterations_end(example_stream_even):
    result = minimalism.additive_process(example_stream_even, iterations_stop=8)
    intended_result = converter.parse(
        """tinyNotation: 
        C
        C D 
        C D E 
        C D E F 
        C D E F G 
        C D E F G A 
        C D E F G A B 
        C D E F G A B c
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_additive_process_nonlinear(example_stream_even):
    result = minimalism.additive_process(
        example_stream_even,
        step_value=sequences.kolakoski(),
        step_mode=minimalism.StepMode.ABSOLUTE,
        iterations_stop=8,
    )
    intended_result = converter.parse(
        """tinyNotation: 
        C
        C D     
        C D     
        C
        C
        C D     
        C
        C D     
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


# Subtractive Process Tests


def test_subtractive_process_even(example_stream_even):
    result = minimalism.subtractive_process(example_stream_even)
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        E F G A B c d e f g   
        F G A B c d e f g   
        G A B c d e f g   
        A B c d e f g  
        B c d e f g  
        c d e f g  
        d e f g  
        e f g  
        f g  
        g
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_odd(example_stream_odd):
    result = minimalism.subtractive_process(example_stream_odd)
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f      
        D E F G A B c d e f  
        E F G A B c d e f   
        F G A B c d e f   
        G A B c d e f   
        A B c d e f  
        B c d e f  
        c d e f  
        d e f  
        e f  
        f  
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


@pytest.mark.parametrize(
    "direction,intended_result",
    [
        (
            minimalism.Direction.BACKWARD,
            converter.parse(
                """tinyNotation: 
        C D E F G A B c d e f g
        C D E F G A B c d e f
        C D E F G A B c d e
        C D E F G A B c d
        C D E F G A B c
        C D E F G A B 
        C D E F G A 
        C D E F G 
        C D E F 
        C D E 
        C D 
        C   
    """
            ),
        ),
        (
            minimalism.Direction.INWARD,
            converter.parse(
                """tinyNotation: 
        C D E F G A B c d e f g
        D E F G A B c d e f
        E F G A B c d e
        F G A B c d
        G A B c
        A B
        """
            ),
        ),
        (
            minimalism.Direction.OUTWARD,
            converter.parse(
                """tinyNotation: 
        C D E F G A B c d e f g   
        C D E F G c d e f g 
        C D E F d e f g
        C D E e f g   
        C D f g  
        C g
    """
            ),
        ),
    ],
)
def test_subtractive_process_direction_even(
    example_stream_even, direction, intended_result
):
    result = minimalism.subtractive_process(example_stream_even, direction=direction)
    assert list(result.flat.notes) == list(intended_result.flat.notes)


@pytest.mark.parametrize(
    "direction,intended_result",
    [
        (
            minimalism.Direction.BACKWARD,
            converter.parse(
                """tinyNotation: 
        C D E F G A B c d e f
        C D E F G A B c d e
        C D E F G A B c d
        C D E F G A B c
        C D E F G A B 
        C D E F G A 
        C D E F G 
        C D E F 
        C D E 
        C D 
        C   
    """
            ),
        ),
        (
            minimalism.Direction.INWARD,
            converter.parse(
                """tinyNotation: 
        C D E F G A B c d e f
        D E F G A B c d e
        E F G A B c d
        F G A B c
        G A B
        A
        """
            ),
        ),
        (
            minimalism.Direction.OUTWARD,
            converter.parse(
                """tinyNotation: 
        C D E F G A B c d e f    
        C D E F G B c d e f
        C D E F c d e f
        C D E d e f 
        C D e f 
        C f
    """
            ),
        ),
    ],
)
def test_subtractive_process_direction_odd(
    example_stream_odd, direction, intended_result
):
    result = minimalism.subtractive_process(example_stream_odd, direction=direction)
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_step_value_int(example_stream_even):
    result = minimalism.subtractive_process(example_stream_even, step_value=2)
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        E F G A B c d e f g   
        G A B c d e f g   
        B c d e f g  
        d e f g  
        f g  
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_step_value_sequence(example_stream_even):
    result = minimalism.subtractive_process(example_stream_even, step_value=[1, 2, 3])
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        F G A B c d e f g   
        B c d e f g  
        c d e f g  
        e f g  
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_step_value_sequence_absolute(example_stream_even):
    result = minimalism.subtractive_process(
        example_stream_even,
        step_value=sequences.PRIMES,
        step_mode=minimalism.StepMode.ABSOLUTE,
    )
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        E F G A B c d e f g   
        F G A B c d e f g   
        A B c d e f g  
        c d e f g  
        g
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_step_value_sequence_absolute_infinite_loop(
    example_stream_even,
):
    result = minimalism.subtractive_process(
        example_stream_even,
        step_value=[1, 2, 3],
        step_mode=minimalism.StepMode.ABSOLUTE,
    )
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        E F G A B c d e f g   
        F G A B c d e f g   
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_repetitions_int(example_stream_even):
    result = minimalism.subtractive_process(example_stream_even, repetitions=2)
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        D E F G A B c d e f g  
        E F G A B c d e f g   
        E F G A B c d e f g   
        F G A B c d e f g   
        F G A B c d e f g   
        G A B c d e f g   
        G A B c d e f g   
        A B c d e f g  
        A B c d e f g  
        B c d e f g  
        B c d e f g  
        c d e f g  
        c d e f g  
        d e f g  
        d e f g  
        e f g  
        e f g  
        f g  
        f g  
        g   
        g
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_repetitions_sequence(example_stream_even):
    result = minimalism.subtractive_process(example_stream_even, repetitions=[1, 2, 3])
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        D E F G A B c d e f g  
        E F G A B c d e f g   
        E F G A B c d e f g   
        E F G A B c d e f g   
        F G A B c d e f g   
        G A B c d e f g   
        G A B c d e f g   
        A B c d e f g  
        A B c d e f g  
        A B c d e f g  
        B c d e f g  
        c d e f g  
        c d e f g  
        d e f g  
        d e f g  
        d e f g  
        e f g  
        f g  
        f g  
        g
        g
        g
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_iterations_start(example_stream_even):
    result = minimalism.subtractive_process(example_stream_even, iterations_start=3)
    intended_result = converter.parse(
        """tinyNotation: 
        F G A B c d e f g   
        G A B c d e f g   
        A B c d e f g  
        B c d e f g  
        c d e f g  
        d e f g  
        e f g  
        f g  
        g
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_iterations_end(example_stream_even):
    result = minimalism.subtractive_process(example_stream_even, iterations_stop=8)
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        E F G A B c d e f g   
        F G A B c d e f g   
        G A B c d e f g   
        A B c d e f g  
        B c d e f g  
        c d e f g  
        d e f g  
    """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)


def test_subtractive_process_nonlinear(example_stream_even):
    result = minimalism.subtractive_process(
        example_stream_even,
        step_value=sequences.kolakoski(),
        step_mode=minimalism.StepMode.ABSOLUTE,
        iterations_stop=8,
    )
    intended_result = converter.parse(
        """tinyNotation: 
        C D E F G A B c d e f g      
        D E F G A B c d e f g  
        E F G A B c d e f g   
        E F G A B c d e f g   
        D E F G A B c d e f g  
        D E F G A B c d e f g  
        E F G A B c d e f g   
        D E F G A B c d e f g  
        E F G A B c d e f g   
        """
    )
    assert list(result.flat.notes) == list(intended_result.flat.notes)
