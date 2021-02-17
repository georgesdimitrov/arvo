"""
Convenient helper functions for quickly manipulating and combining music21 elements.
"""

import math
import copy
import numbers
from typing import Union, Sequence, List

from music21 import duration
from music21 import note
from music21 import stream
from music21 import pitch


__all__ = [
    "stream_to_part",
    "stream_to_notes",
    "stream_to_pitches",
    "pitches_to_stream",
    "durations_to_stream",
    "merge_streams",
    "copy_key_signature",
]


def stream_to_part(
    original_stream: stream.Stream, in_place: bool = False
) -> stream.Stream:
    """Flattens all notes in a Stream to a Part.

    Args:
        original_stream: stream to flatten.

    Returns:
        Flattened part.
    """
    new_part = stream.Part()
    for n in original_stream.flat.notes:
        if in_place:
            new_part.insert(n.offset, n)
        else:
            new_part.insert(n.offset, copy.deepcopy(n))
    return new_part


def stream_to_notes(
    original_stream: stream.Stream, in_place: bool = False
) -> List[note.Note]:
    """Returns a list of all notes contained in a Stream

    Args:
        original_stream: Stream to process.
        in_place: Optional; If True, returns references to Note objects in the original stream, else returns new
          copies. Default is True.

    Returns:
        The list of Note objects.

    """
    notes = []
    for n in original_stream.flat.notes:
        if in_place:
            notes.append(n)
        else:
            notes.append(copy.deepcopy(n))
    return notes


def stream_to_pitches(
    original_stream: stream.Stream, in_place: bool = False
) -> List[pitch.Pitch]:
    """Returns a list of all pitches contained in a Stream

    Args:
        original_stream: Stream to process.
        in_place: Optional; If True, returns references to Pitch objects in the original stream, else returns new
          copies. Default is True.

    Returns:
        The list of Pitch objects.

    """
    pitches = []
    for n in stream_to_notes(original_stream, in_place=in_place):
        if n.isChord:
            element_pitches = n.pitches
        else:
            element_pitches = [n.pitch]

        for p in element_pitches:
            if in_place:
                pitches.append(p)
            else:
                pitches.append(copy.deepcopy(p))

    return pitches


def pitches_to_stream(
    pitches: Sequence[Union[numbers.Number, str, pitch.Pitch, note.Note]]
) -> stream.Stream:
    """Creates a stream from a sequence of pitches.

    Args:
        pitches: Sequence of pitches to convert to a stream. Sequence can consist of pitch classes (0-11),
          midi note numbers (12+), note names (str), music21 Pitch objects or music21 Note objects.

    Returns:
        Stream containing a sequence of notes with the corresponding pitches.
    """
    post_stream = stream.Stream()
    for p in pitches:
        if isinstance(p, str) or isinstance(p, pitch.Pitch):
            post_stream.append(note.Note(p))
        elif isinstance(p, numbers.Number):
            n = note.Note(p)
            if n.pitch.accidental.name == "natural":
                n.pitch.accidental = None
            post_stream.append(n)
        elif isinstance(p, note.Note):
            post_stream.append(p)
    return post_stream


def durations_to_stream(
    durations: Sequence[Union[numbers.Number, duration.Duration, note.Note]]
):
    """Converts a sequence of durations to a Stream containing note objects of that duration.

    Args:
        durations: Sequence of durations to convert to a stream. Sequence can consist of numeric values
          (1 = quarter note), music21 Duration objects or music21 Note objects.

    Returns:
        Stream containing a sequence of notes with the corresponding durations.
    """
    post_stream = stream.Stream()
    for d in durations:
        if isinstance(d, numbers.Number):
            new_note = note.Note()
            new_note.duration = duration.Duration(d)
            post_stream.append(new_note)
        elif isinstance(d, duration.Duration):
            new_note = note.Note()
            new_note.duration = d
            post_stream.append(new_note)
        elif isinstance(d, note.Note):
            post_stream.append(d)
    return post_stream


def merge_streams(*streams):
    post_stream = stream.Stream()
    for s in streams:
        post_stream.insert(0, stream_to_part(s))
    return post_stream


def copy_key_signature(original_stream, new_stream):
    for key_signature in original_stream.getElementsByClass("KeySignature"):
        new_stream.insert(0, key_signature)
    new_stream.sort()
