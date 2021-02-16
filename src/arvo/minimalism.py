"""
Module for generative mathematical processes, such addition or subtraction.
"""

import math
import copy
import enum
from typing import Optional, Union, Sequence

from music21 import stream

from src.arvo import sequences


__all__ = ["Direction", "StepMode", "additive_process", "subtractive_process", "scanning_process"]


class Direction(enum.Enum):
    """
    Determines the direction of minimalist processes.

    FORWARD starts the process from the beginning of the stream;
    BACKWARD starts the process from the end of the stream;
    INWARD starts the process from the extremities of the stream inward;
    OUTWARD starts the process from the middle of the stream outward.
    """

    FORWARD = 1
    BACKWARD = 2
    INWARD = 3
    OUTWARD = 4


class StepMode(enum.Enum):
    RELATIVE = 1
    ABSOLUTE = 2


def additive_process(
    stream: stream.Stream,
    direction: Direction = Direction.FORWARD,
    step: Union[int, Sequence[int]] = 1,
    step_mode: StepMode = StepMode.RELATIVE,
    repetitions: Union[int, Sequence[int]] = 1,
    iterations: Optional[int] = None,
) -> stream.Stream:
    """Applies an additive process to a stream.

    Builds a new stream by applying an additive process to the original stream. Only note and
    chord objects are included.

    Args:
        stream: The original stream to process.
        direction: Optional; Determines the direction of the additive process. Default is FORWARD.
        step: Optional; Determines the number of elements added each iteration. Default is 1. If provided a sequence of
          numbers (for example, sequences.PRIMES), the step parameter will cycle through the sequence each iteration,
          looping if it reaches the end of the sequence.
        step_mode: Optional; Determines the step mode. In RELATIVE mode, step determines the amount of elements
          added each iteration relative to the previous iteration. In ABSOLUTE mode, step determines the amount
          of elements added each iteration relative to the starting point.
        repetitions: Optional; Determines the number of times each segment is repeated before moving to
          the next iteration. Default is 1. If provided a sequence of numbers (for example, sequences.PRIMES), the
          repetitions parameter will cycle through the sequence each iteration, looping if it reaches the end of the
          sequence.
        iterations: Optional; Determines the number of iterations to do before the process stops. By default, the
          process runs until the original stream is completed or an infinite loop is detected.
    Returns:
        The new stream created by the additive process.
    """

    # Check step type and initialize step sequence.
    if isinstance(step, int):
        step_sequence = [step]
    elif isinstance(step, Sequence):
        step_sequence = step
    step_index = 0

    # Check repetitions type and initialize repetitions sequence.
    if isinstance(repetitions, int):
        repetitions_sequence = [repetitions]
    elif isinstance(repetitions, Sequence):
        repetitions_sequence = repetitions
    repetitions_index = 0

    # Initialize function variables.
    new_stream = stream.Stream()
    original_notes = stream.flat.notes
    original_length = len(original_notes)
    iteration_index = 0
    position1 = 0
    position2 = 0
    current_length = step_sequence[0]
    completed = False

    while not completed:
        current_stream = stream.Stream()

        # Determine boundaries of segment to use for the current iteration, depending on direction.
        if direction is Direction.FORWARD:
            position1 = 0
            position2 = current_length
            if position2 > original_length:
                position2 = original_length
            if iterations is None and position2 == original_length:
                completed = True
        elif direction is Direction.BACKWARD:
            position1 = original_length - current_length
            position2 = original_length
            if position1 < 0:
                position1 = 0
            if iterations is None and position1 == 0:
                completed = True
        elif direction is Direction.INWARD:
            position1 = current_length
            position2 = original_length - current_length
            if position1 >= position2:
                position1 = position2
            if iterations is None and position1 == position2:
                completed = True
        elif direction is Direction.OUTWARD:
            position1 = math.floor(original_length / 2.0 - current_length)
            position2 = math.floor(original_length / 2.0 + current_length)
            if position1 < 0:
                position1 = 0
            if position2 > original_length:
                position2 = original_length
            if iterations is None and position1 == 0 and position2 == original_length:
                completed = True

        # Build the current iteration, repeating the segment the amount of times defined by the repetitions sequence.
        for _ in range(repetitions_sequence[repetitions_index]):
            if direction == Direction.INWARD:
                for i in range(0, position1):
                    current_stream.append(copy.deepcopy(original_notes[i]))
                for i in range(position2, original_length):
                    current_stream.append(copy.deepcopy(original_notes[i]))
            else:
                for i in range(position1, position2):
                    current_stream.append(copy.deepcopy(original_notes[i]))

        # Add iteration to final sequence.
        new_stream.append(current_stream)

        # Increment iteration index, stopping if iterations parameter has been set and reached.
        iteration_index += 1
        if iterations is not None and iteration_index == iterations:
            completed = True

        # Increment step and repetition indexes, looping if the end of the sequence is reached.
        step_index += 1
        if step_index > len(step_sequence) - 1:
            step_index = 0
            # Infinite loop check
            if iterations is None and step_mode == StepMode.ABSOLUTE:
                completed = True
        repetitions_index += 1
        if repetitions_index > len(repetitions_sequence) - 1:
            repetitions_index = 0

        # Update segment length
        if step_mode == StepMode.RELATIVE:
            current_length += step_sequence[step_index]
        elif step_mode == StepMode.ABSOLUTE:
            current_length = step_sequence[step_index]

    return new_stream.flat


def subtractive_process(
    stream: stream.Stream,
    direction: Direction = Direction.FORWARD,
    step: Union[int, Sequence[int]] = 1,
    step_mode: StepMode = StepMode.RELATIVE,
    repetitions: Union[int, Sequence[int]] = 1,
    iterations: Optional[int] = None,
) -> stream.Stream:
    """Applies an subtractive process to a stream.

    Builds a new stream by applying a subtractive process to the original stream. Only note and
    chord objects are included.

    Args:
        stream: The original stream to process.
        direction: Optional; The direction of the subtractive process. Default is Direction.FORWARD.
        step: Optional; Determines the number of elements subtracted each iteration. Default is 1. If provided a
         sequence of numbers (for example, sequences.PRIMES), the step parameter will cycle through the sequence each
         iteration, looping if it reaches the end of the sequence.
        step_mode: Optional; Determines the step mode. In RELATIVE mode, step determines the amount of elements
          subtracted each iteration relative to the previous iteration. In ABSOLUTE mode, step determines the amount
          of elements subtracted each iteration relative to the starting point.
        repetitions: Optional; Determines the number of times each segment is repeated before moving to
          the next iteration. Default is 1. If provided a sequence of numbers (for example, sequences.PRIMES), the
          repetitions parameter will cycle through the sequence each iteration, looping if it reaches the end of the
          sequence.
        iterations: Optional; Determines the number of iterations to do before the process stops. By default, the
          process runs until the original stream disappears. Note that the subtractive process starts with the complete
          stream, so the first iteration results in the second segment.

    Returns:
        The new stream created by the subtractive process.

    """

    # Check step type and initialize step sequence.
    if isinstance(step, int):
        step_sequence = [step]
    elif isinstance(step, Sequence):
        step_sequence = step
    step_index = -1

    # Check repetitions type and initialize repetitions sequence.
    if isinstance(repetitions, int):
        repetitions_sequence = [repetitions]
    elif isinstance(repetitions, Sequence):
        repetitions_sequence = repetitions
    repetitions_index = 0

    # Initialize function variables.
    new_stream = stream.Stream()
    original_notes = stream.flat.notes
    original_length = len(original_notes)
    iteration_index = -1
    position1 = 0
    position2 = 0
    current_length = 0
    completed = False

    while not completed:
        current_stream = stream.Stream()

        # Determine boundaries of segment to use for the current iteration, depending on direction.
        if direction is Direction.FORWARD:
            position1 = current_length
            position2 = original_length
            if position1 >= original_length:
                position1 = original_length
            if iterations is None and position1 == original_length:
                completed = True
        elif direction is Direction.BACKWARD:
            position1 = 0
            position2 = original_length - current_length
            if position2 <= 0:
                position2 = 0
            if iterations is None and position2 == 0:
                completed = True
        elif direction is Direction.INWARD:
            position1 = current_length
            position2 = original_length - current_length
            if position2 < 0:
                position2 = 0
            if position1 >= position2:
                position1 = position2
            if iterations is None and position1 == position2:
                completed = True
        elif direction is Direction.OUTWARD:
            position1 = math.floor(original_length / 2.0 - current_length)
            position2 = math.floor(original_length / 2.0 + current_length)
            if position1 < 0:
                position1 = 0
            if position2 >= original_length:
                position2 = original_length
            if iterations is None and position1 == 0 and position2 == original_length:
                completed = True

        # Build the current iteration, repeating the segment the amount of times defined by the repetitions sequence.
        for _ in range(repetitions_sequence[repetitions_index]):
            if direction is Direction.OUTWARD:
                for i in range(0, position1):
                    current_stream.append(copy.deepcopy(original_notes[i]))
                for i in range(position2, original_length):
                    current_stream.append(copy.deepcopy(original_notes[i]))
            else:
                for i in range(position1, position2):
                    current_stream.append(copy.deepcopy(original_notes[i]))

        # Add iteration to final sequence.
        new_stream.append(current_stream)

        # Increment iteration index, stopping if iterations parameter has been set and reached.
        iteration_index += 1
        if iterations is not None and iteration_index == iterations:
            completed = True

        # Increment step and repetition indexes, looping if the end of the sequence is reached.
        step_index += 1
        if step_index > len(step_sequence) - 1:
            step_index = 0
            # Infinite loop check
            if iterations is None and step_mode == StepMode.ABSOLUTE:
                completed = True
        repetitions_index += 1
        if repetitions_index > len(repetitions_sequence) - 1:
            repetitions_index = 0

        # Update segment length
        if step_mode == StepMode.RELATIVE:
            current_length += step_sequence[step_index]
        elif step_mode == StepMode.ABSOLUTE:
            current_length = step_sequence[step_index]

    return new_stream.flat


def scanning_process(
    stream: stream.Stream,
    direction: Direction = Direction.FORWARD,
    step: Union[int, Sequence[int]] = 1,
    step_mode: StepMode = StepMode.RELATIVE,
    window_size: Union[int, Sequence[int]] = 2,
    repetitions: Union[int, Sequence[int]] = 1,
    iterations: Optional[int] = None,
) -> stream.Stream:
    """Applies a scanning process to a stream.

    Builds a new stream by applying an scanning process to the original stream. Only note and
    chord objects are included. Provided a stream of 6 elements, with a LINEAR sequence in FORWARD direction, with
    a window_size of 2, this function will return a stream composed of: 12|23|34|45|56|6. With a PRIMES
    sequence, the result would be 12|34|6 (sequence = [0, 2, 3, 5, 7...]).
    TODO: include inward/outward directions, numberOfRepetitions and numberOfIterations options from additive and subtractive processes.
    TODO: include list[int] option for window_size

    Args:
        stream: The original stream to process.
        direction: Optional; The direction of the scanning process. Default is Direction.FORWARD.
        sequence: Optional; Determines the number sequence governing the starting position of the window for each
          step of the scanning process. Default is sequences.LINEAR ([1,2,3,4,5,6,7...]).
        window_size: Options; Determines the size of the "window" that is scanning the original stream.
        repetitions: Optional; Determines the number of times each segment is repeated before moving to
          the next step in the sequence. Default is 1.
        steps: Optional; Stops the additive process after n steps in the sequence. By default,
          it runs until the original stream is completed.


    Returns:
        The new stream created by the subtractive process.
    """

    new_stream = stream.Stream()
    original_notes = stream.flat.notes
    original_length = len(original_notes)
    progression_index = 0
    start_position = 0
    end_position = 0
    current_position = 0

    while current_position < original_length:
        current_stream = stream.Stream()
        if direction is Direction.FORWARD:
            start_position = current_position
            end_position = current_position + window_size
        elif direction is Direction.BACKWARD:
            start_position = original_length - (current_position + window_size)
            end_position = original_length - current_position
        if start_position < 0:
            start_position = 0
        if end_position > original_length:
            end_position = original_length
        for i in range(start_position, end_position):
            current_stream.append(copy.deepcopy(original_notes[i]))
        new_stream.append(current_stream)
        progression_index += 1
        if isinstance(interval, int):
            current_position = progression_index * interval

        current_position = sequence(progression_index)

    return new_stream
