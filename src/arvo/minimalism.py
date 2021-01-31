import math
from copy import deepcopy
from enum import Enum

import music21

from src.arvo import sequences


class Direction(Enum):
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


def additive_process(
    stream: music21.stream.Stream,
    direction: Direction = Direction.FORWARD,
    sequence: list[int] = sequences.LINEAR,
    repetitions: int = 1,
    steps: int = 0,
) -> music21.stream.Stream:
    """Applies an additive process to a stream.

    Builds a new stream by applying an additive process to the original stream. Only note and
    chord objects are included.

    Args:
        stream: The original stream to process.
        direction: Optional; The direction of the additive process. Default is Direction.FORWARD.
        sequence: Optional; Determines the number sequence governing the additive process. Default is
          sequences.LINEAR ([1,2,3,4,5,6,7...]).
        repetitions: Optional; Determines the number of times each segment is repeated before moving to
          the next step in the sequence. Default is 1.
        steps: Optional; Stops the additive process after n steps in the sequence. By default,
          it runs until the original stream is completed.

    Returns:
        The new stream created by the additive process.
    """

    new_stream = music21.stream.Stream()
    original_notes = stream.flat.notes
    original_length = len(original_notes)
    progression_index = 0
    position1 = 0
    position2 = 0
    current_length = sequence[progression_index]
    completed = False

    while not completed:
        current_stream = music21.stream.Stream()
        if direction is Direction.FORWARD:
            position1 = 0
            position2 = current_length
        elif direction is Direction.BACKWARD:
            position1 = original_length - current_length
            position2 = original_length
        elif direction is Direction.INWARD:
            position1 = current_length
            position2 = original_length - current_length
            if position1 >= position2:
                position1 = position2
                completed = True
        elif direction is Direction.OUTWARD:
            position1 = math.floor(original_length / 2.0 - current_length)
            position2 = math.floor(original_length / 2.0 + current_length)
        if position1 < 0:
            position1 = 0
            completed = True
        if position2 >= original_length:
            position2 = original_length
            completed = True
        for _ in range(repetitions):
            if direction == "inward":
                for i in range(0, position1):
                    current_stream.append(deepcopy(original_notes[i]))
                for i in range(position2, original_length):
                    current_stream.append(deepcopy(original_notes[i]))
            else:
                for i in range(position1, position2):
                    current_stream.append(deepcopy(original_notes[i]))
        new_stream.append(current_stream)
        progression_index += 1
        if progression_index == steps:
            completed = True
        current_length = sequence[progression_index]

    return new_stream.flat


def substractive_process(
    stream: music21.stream.Stream,
    direction: Direction = Direction.FORWARD,
    sequence: list[int] = sequences.LINEAR,
    repetitions: int = 1,
    steps: int = 0,
) -> music21.stream.Stream:
    """Applies an substractive process to a stream.

    Builds a new stream by applying a substractive process to the original stream. Only note and
    chord objects are included.

    Args:
        stream: The original stream to process.
        direction: Optional; The direction of the substractive process. Default is Direction.FORWARD.
        sequence: Optional; Determines the number sequence governing the substractive process. Default is
          sequences.LINEAR ([1,2,3,4,5,6,7...]).
        repetitions: Optional; Determines the number of times each segment is repeated before moving to
          the next step in the sequence. Default is 1.
        steps: Optional; Stops the substractive process after n steps in the sequence. By default,
          it runs until the original stream is empty.

    Returns:
        The new stream created by the substractive process.

    """
    new_stream = music21.stream.Stream()
    original_notes = stream.flat.notes
    original_length = len(original_notes)
    sequence.insert(0, 0)
    progression_index = 0

    position1 = 0
    position2 = 0
    current_length = sequence[progression_index]
    completed = False

    while not completed:
        current_stream = music21.stream.Stream()

        if direction is Direction.FORWARD:
            position1 = current_length
            position2 = original_length
            if position1 >= original_length:
                position1 = original_length
                completed = True
        elif direction is Direction.BACKWARD:
            position1 = original_length - current_length
            position2 = 0
            if position1 < 0:
                position1 = 0
                completed = True
        elif direction is Direction.INWARD:
            position1 = current_length
            position2 = original_length - current_length
            if position2 < 0:
                position2 = 0
            if position1 >= position2:
                position1 = position2
                completed = True
        elif direction is Direction.OUTWARD:
            position1 = math.floor(original_length / 2.0 - current_length)
            position2 = math.floor(original_length / 2.0 + current_length)
            if position1 < 0 and position2 >= original_length:
                completed = True
            if position1 < 0:
                position1 = 0
            if position2 >= original_length:
                position2 = original_length

        for _ in range(repetitions):
            if direction is Direction.OUTWARD:
                for i in range(0, position1):
                    current_stream.append(deepcopy(original_notes[i]))
                for i in range(position2, original_length):
                    current_stream.append(deepcopy(original_notes[i]))
            else:
                for i in range(position1, position2):
                    current_stream.append(deepcopy(original_notes[i]))

        new_stream.append(current_stream)
        progression_index += 1
        if progression_index == steps:
            completed = True
        current_length = sequence[progression_index]

    return new_stream.flat


def scanning_process(
    stream: music21.stream.Stream,
    direction: Direction = Direction.FORWARD,
    sequence: list[int] = sequences.LINEAR,
    window_size: int = 1,
    repetitions: int = 1,
    steps: int = 0,
) -> music21.stream.Stream:
    """Applies a scanning process to a stream.

    Builds a new stream by applying an scanning process to the original stream. Only note and
    chord objects are included.
    TODO: include inward/outward directions, numberOfRepetitions and numberOfIterations options from additive and substractive processes.

    Args:
        stream: The original stream to process.
        direction: Optional; The direction of the scanning process. Default is Direction.FORWARD.
        sequence: Optional; Determines the number sequence governing the scanning process. Default is
          sequences.LINEAR ([1,2,3,4,5,6,7...]).
        window_size: Options; Determines the size of the "window" that is scanning the original stream.
        repetitions: Optional; Determines the number of times each segment is repeated before moving to
          the next step in the sequence. Default is 1.
        steps: Optional; Stops the additive process after n steps in the sequence. By default,
          it runs until the original stream is completed.


    Returns:
        The new stream created by the substractive process.
    """

    new_stream = music21.stream.Stream()
    original_notes = stream.flat.notes
    original_length = len(original_notes)
    progression_index = 0
    start_position = 0
    end_position = 0
    current_position = 0

    while current_position + window_size < original_length:
        current_stream = music21.stream.Stream()
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
            current_stream.append(deepcopy(original_notes[i]))
        new_stream.append(current_stream)
        progression_index += 1
        current_position = sequence(progression_index)

    return new_stream
