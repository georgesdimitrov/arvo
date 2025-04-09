"""Module for generative minimalist processes, such as additive or subtractive."""

import copy
import math
import enum
from typing import Optional, Sequence
from abc import abstractmethod

from arvo import core
from arvo import tools
from music21 import stream
from dataclasses import dataclass


__all__ = [
    "Direction",
    "StepMode",
    "Options",
    "additive_process",
    "subtractive_process",
]


class Direction(enum.Enum):
    """Specifies the traversal direction for the minimalist process.

    - FORWARD: from the beginning to the end of the sequence or stream.
    - BACKWARD: from the end to the beginning.
    - INWARD: from the outermost elements toward the center.
    - OUTWARD: from the center outward to the edges.
    """

    FORWARD = 1
    BACKWARD = 2
    INWARD = 3
    OUTWARD = 4


class StepMode(enum.Enum):
    """Specifies how step values are interpreted during the process.

    - RELATIVE: step_value is added to the iteration length.
      A step of 1 yields lengths 1, 2, 3... A step sequence [1, 2] gives 1, 3, 4, 6...
    - ABSOLUTE: step_value directly sets the iteration length.
      Must be a sequence, e.g., sequences.PRIMES.
    """

    RELATIVE = 1
    ABSOLUTE = 2


@dataclass
class Options:
    """Configuration options for additive and subtractive processes.

    Attributes:
        direction: Direction in which elements are processed. Default is FORWARD.
        step_value: Number or sequence of numbers controlling iteration size.
            If a sequence (e.g., sequences.PRIMES), it cycles through the values.
            Default is 1.
        step_mode: How step_value is applied. RELATIVE adds to the current length;
            ABSOLUTE sets it directly. Default is RELATIVE.
        repetitions: Number or sequence of times each segment is repeated before
            advancing to the next iteration. Default is 1.
        iterations_start: Starting iteration index (1-based). Defaults to 1.
        iterations_stop: Ending iteration index. By default, the process continues
            until the sequence is exhausted or an infinite loop is detected.
    """

    direction: Direction = Direction.FORWARD
    step_value: int | Sequence[int] = 1
    step_mode: StepMode = StepMode.RELATIVE
    repetitions: int | Sequence[int] = 1
    iterations_start: Optional[int] = None
    iterations_stop: Optional[int] = None


@dataclass
class _ProcessState:
    iteration: int
    iteration_length: int
    completed: bool


class _IndexedSequence:
    """Wrapper for indexed sequences."""

    def __init__(self, sequence, index):
        if isinstance(sequence, int):
            self.sequence = [sequence]
        elif isinstance(sequence, Sequence):
            self.sequence = sequence
        self.index = index

    def increment(self):
        self.index += 1
        if self.index > len(self.sequence) - 1:
            self.index = 0

    @property
    def current(self):
        return self.sequence[self.index]


class _Process:
    """Base class for minimalism processes."""

    def __init__(self, sequence, options):
        self._sequence = core.ArvoSequence(sequence)
        self._options = options or Options()
        self._state = _ProcessState(
            iteration=0,
            iteration_length=0,
            completed=False,
        )
        self._steps = _IndexedSequence(self._options.step_value, 0)
        self._repetitions = _IndexedSequence(self._options.repetitions, 0)
        self._post_sequence = []

    def apply_process(self):
        while not self._state.completed:
            position1, position2 = self._get_iteration_positions()
            if (
                self._options.iterations_start is None
                or self._state.iteration + 1 >= self._options.iterations_start
            ):
                segment = self._get_interation_segment(position1, position2)
                self._post_sequence.extend(segment)

            # Increment step and repetition indexes,
            # looping if the end of the sequence is reached.
            self._steps.increment()
            self._repetitions.increment()
            # Infinite loop check
            if (
                self._steps.index == 0
                and self._state.iteration > 0
                and self._options.iterations_stop is None
                and self._options.step_mode == StepMode.ABSOLUTE
            ):
                self._state.completed = True

            # Increment iteration index, stopping
            # if iterations parameter has been set and reached.
            self._state.iteration += 1
            if (
                self._options.iterations_stop is not None
                and self._state.iteration == self._options.iterations_stop
            ):
                self._state.completed = True

            # Update segment length
            if self._options.step_mode == StepMode.RELATIVE:
                self._state.iteration_length += self._steps.current
            elif self._options.step_mode == StepMode.ABSOLUTE:
                self._state.iteration_length = self._steps.current

    @abstractmethod
    def _get_iteration_positions(self):
        pass

    @abstractmethod
    def _get_interation_segment(self, position1, position2):
        pass

    @property
    def result(self):
        if self._sequence.is_stream:
            return tools.notes_to_stream(self._post_sequence)

        return self._post_sequence


class _AdditiveProcess(_Process):
    """Internal class implementing the additive version of a generative process."""

    def __init__(self, sequence, options):
        super().__init__(sequence, options)
        self._state.iteration_length = self._steps.sequence[0]

    def _get_iteration_positions(self):
        position1 = 0
        position2 = 0
        match self._options.direction:
            case Direction.FORWARD:
                position1 = 0
                position2 = self._state.iteration_length
                position2 = min(position2, len(self._sequence))
                if self._options.iterations_stop is None and position2 == len(
                    self._sequence
                ):
                    self._state.completed = True
            case Direction.BACKWARD:
                position1 = len(self._sequence) - self._state.iteration_length
                position2 = len(self._sequence)
                position1 = max(position1, 0)
                if self._options.iterations_stop is None and position1 == 0:
                    self._state.completed = True
            case Direction.INWARD:
                position1 = self._state.iteration_length
                position2 = len(self._sequence) - self._state.iteration_length
                position1 = min(position1, position2)
                if self._options.iterations_stop is None and position1 == position2:
                    self._state.completed = True
            case Direction.OUTWARD:
                position1 = math.ceil(
                    len(self._sequence) / 2.0 - self._state.iteration_length
                )
                position2 = math.floor(
                    len(self._sequence) / 2.0 + self._state.iteration_length
                )
                position1 = max(position1, 0)
                position2 = min(position2, len(self._sequence))
                if (
                    self._options.iterations_stop is None
                    and position1 == 0
                    and position2 == len(self._sequence)
                ):
                    self._state.completed = True

        return position1, position2

    def _get_interation_segment(self, position1, position2):
        segment = []

        for _ in range(self._repetitions.current):
            match self._options.direction:
                case Direction.INWARD:
                    for i in range(0, position1):
                        segment.append(copy.deepcopy(self._sequence[i]))
                    for i in range(position2, len(self._sequence)):
                        segment.append(copy.deepcopy(self._sequence[i]))
                case _:
                    for i in range(position1, position2):
                        segment.append(copy.deepcopy(self._sequence[i]))

        return segment


class _SubtractiveProcess(_Process):
    """Internal class implementing the subtractive version of a generative process."""

    def __init__(self, sequence, options):
        super().__init__(sequence, options)
        self._state.iteration = -1
        self._steps.index = -1

    def _get_iteration_positions(self):
        position1 = 0
        position2 = 0
        match self._options.direction:
            case Direction.FORWARD:
                position1 = self._state.iteration_length
                position2 = len(self._sequence)
                position1 = min(position1, len(self._sequence))
                if self._options.iterations_stop is None and position1 == len(
                    self._sequence
                ):
                    self._state.completed = True
            case Direction.BACKWARD:
                position1 = 0
                position2 = len(self._sequence) - self._state.iteration_length
                position2 = max(position2, 0)
                if self._options.iterations_stop is None and position2 == 0:
                    self._state.completed = True
            case Direction.INWARD:
                position1 = self._state.iteration_length
                position2 = len(self._sequence) - self._state.iteration_length
                position2 = max(position2, 0)
                position1 = min(position1, position2)
                if self._options.iterations_stop is None and position1 == position2:
                    self._state.completed = True
            case Direction.OUTWARD:
                position1 = math.ceil(
                    len(self._sequence) / 2.0 - self._state.iteration_length
                )
                position2 = math.floor(
                    len(self._sequence) / 2.0 + self._state.iteration_length
                )
                position2 = max(position2, position1)
                position1 = max(position1, 0)
                position2 = min(position2, len(self._sequence))
                if (
                    self._options.iterations_stop is None
                    and position1 == 0
                    and position2 == len(self._sequence)
                ):
                    self._state.completed = True

        return position1, position2

    def _get_interation_segment(self, position1, position2):
        segment = []

        for _ in range(self._repetitions.current):
            match self._options.direction:
                case Direction.OUTWARD:
                    for i in range(0, position1):
                        segment.append(copy.deepcopy(self._sequence[i]))
                    for i in range(position2, len(self._sequence)):
                        segment.append(copy.deepcopy(self._sequence[i]))
                case _:
                    for i in range(position1, position2):
                        segment.append(copy.deepcopy(self._sequence[i]))

        return segment


def additive_process(
    sequence: Sequence | stream.Stream, options: Optional[Options] = None
) -> Sequence | stream.Stream:
    """Applies an additive process to a sequence or music21 Stream.

    If a music21 Stream is provided, it will be flattened and its note, chord,
    and rest elements extracted.

    Args:
        sequence: The input sequence or Stream to process.
        options: Optional configuration settings for the process.

    Returns:
        A new object of the same type (Sequence or Stream) generated by the process.
    """
    process = _AdditiveProcess(sequence, options)
    process.apply_process()
    return process.result


def subtractive_process(
    sequence: Sequence | stream.Stream, options: Optional[Options] = None
) -> Sequence | stream.Stream:
    """Applies a subtractive process to a sequence or music21 Stream.

    If a music21 Stream is provided, it will be flattened and its note, chord,
    and rest elements extracted.

    Args:
        sequence: The input sequence or Stream to process.
        options: Optional configuration settings for the process.

    Returns:
        A new object of the same type (Sequence or Stream) generated by the process.
    """
    process = _SubtractiveProcess(sequence, options)
    process.apply_process()
    return process.result
