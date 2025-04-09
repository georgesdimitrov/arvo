"""
Core module defining the fundamental Arvo classes and types.

Includes wrappers for music21 streams, sequences, pitches, and durations, providing
a consistent interface for Arvo-related operations.
"""

from __future__ import annotations

import enum
import numbers
from typing import Union, Sequence, Iterator

from music21 import duration
from music21 import note
from music21 import pitch
from music21 import stream
from music21 import chord


class ArvoObjectType(enum.Enum):
    """
    Enum classifying the types of objects wrapped by ArvoObject.

    Attributes:
        ELEMENT: A single note, pitch, or duration.
        STREAM: A music21 stream object.
        SEQUENCE: A sequence or iterable.
    """

    ELEMENT = 1
    STREAM = 2
    SEQUENCE = 3


class ArvoObject:
    """
    Wrapper class providing a unified interface for various objects, including music21
    streams, single musical elements (notes, pitches, durations), and general sequences.

    Automatically determines and sets the type of the wrapped object.

    Args:
        wrapped_object: A music21 stream, sequence, or single musical element to wrap.
    """

    def __new__(cls, wrapped_object):
        if isinstance(wrapped_object, ArvoObject):
            return wrapped_object
        return super().__new__(cls)

    def __init__(
        self,
        wrapped_object: Union[stream.Stream, ArvoElement, ArvoSequence],
    ):
        if not isinstance(wrapped_object, ArvoObject):
            self.wrapped_object = wrapped_object
            if isinstance(wrapped_object, stream.Stream):
                self.object_type = ArvoObjectType.STREAM
            elif isinstance(wrapped_object, Sequence):
                self.object_type = ArvoObjectType.SEQUENCE
            elif isinstance(wrapped_object, Iterator):
                self.object_type = ArvoObjectType.SEQUENCE
                self.wrapped_object = list(wrapped_object)
            else:
                self.object_type = ArvoObjectType.ELEMENT

    def __eq__(self, other: ArvoObject) -> bool:
        if self.object_type != other.object_type:
            return False
        if self.object_type == ArvoObjectType.ELEMENT:
            return self.wrapped_object == other.wrapped_object
        return self.get_elements_list() == other.get_elements_list()

    def get_elements_list(self) -> Sequence:
        """
        Returns a flat list of musical elements contained in this ArvoObject.

        If the object is a STREAM, returns all flattened notes. If a SEQUENCE,
        returns the sequence directly. If an ELEMENT, returns a single-element list
        containing the wrapped object.
        """
        match self.object_type:
            case ArvoObjectType.STREAM:
                elements_list = []
                for element in self.wrapped_object.flatten().notes:
                    elements_list.append(element)
                return elements_list
            case ArvoObjectType.SEQUENCE:
                return self.wrapped_object
        return [self.wrapped_object]

    def __repr__(self):
        return (
            f"<ArvoObject(type={self.object_type.name}, "
            f"wrapped={repr(self.wrapped_object)})>"
        )


class ArvoSequence(Sequence):
    """
    Represents an ordered sequence of elements, optionally musical elements derived
    from a music21 Stream.

    Args:
        sequence: A Sequence of elements or a music21 Stream.
    """

    def __init__(self, sequence: Sequence | stream.Stream):
        if isinstance(sequence, stream.Stream):
            self._sequence = list(sequence.flatten().notes)
            self.is_stream = True
        elif isinstance(sequence, Sequence):
            self._sequence = list(sequence)
            self.is_stream = False
        else:
            self._sequence = [sequence]
            self.is_stream = False

    def __getitem__(self, item: int):
        return self._sequence[item]

    def __len__(self) -> int:
        return len(self._sequence)

    def __eq__(self, other: ArvoSequence) -> bool:
        if isinstance(other, ArvoSequence):
            return list(self._sequence) == list(other._sequence)
        if isinstance(other, Sequence):
            return list(self._sequence) == list(other)
        return NotImplemented

    def __repr__(self):
        return f"<ArvoSequence(len={len(self)}, is_stream={self.is_stream})>"


class ArvoPitchesSequence(ArvoSequence):
    """
    Specialized sequence class for handling sequences of pitches.

    Accepts various pitch representations, including chord objects, pitch sequences,
    and streams.
    """

    def __init__(
        self,
        sequence: PitchesSequence | stream.Stream,
    ):
        if isinstance(sequence, chord.Chord):
            sequence = sequence.pitches
        super().__init__(sequence)


class ArvoDurationsSequence(ArvoSequence):
    """
    Specialized sequence class for handling sequences of durations.

    Accepts numeric durations, music21 Duration objects, or note objects.
    """

    def __init__(
        self,
        sequence: DurationsSequence | stream.Stream,
    ):
        super().__init__(sequence)


# Represents acceptable inputs for pitch sequences.
PitchesSequence = (
    Sequence[int]
    | Sequence[str]
    | Sequence[pitch.Pitch]
    | Sequence[note.GeneralNote]
    | chord.Chord
)


# Represents acceptable inputs for duration sequences.
DurationsSequence = (
    Sequence[numbers.Number] | Sequence[duration.Duration] | Sequence[note.GeneralNote]
)


# Represents any valid single-element Arvo object.
ArvoElement = Union[
    numbers.Number, str, pitch.Pitch, duration.Duration, note.GeneralNote
]
