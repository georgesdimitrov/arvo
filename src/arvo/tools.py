"""
Convenient helper functions for quickly manipulating and combining music21 elements.
"""

import copy
import numbers
from typing import Union, Sequence, List, Optional, Type

from music21 import duration
from music21 import note
from music21 import stream
from music21 import pitch
from music21 import chord

__all__ = [
    "convert_stream",
    "stream_to_notes",
    "stream_to_pitches",
    "notes_to_stream",
    "durations_to_stream",
    "merge_streams",
]


def convert_stream(
    original_stream: stream.Stream,
    stream_class: Type[Union[stream.Voice, stream.Part, stream.Score]],
) -> stream.Stream:
    """Converts a stream to a the specified type

    Args:
        original_stream: The Stream to convert.
        stream_class: The type of stream to convert to (Score, Part or Voice).

    Returns:
        Converted stream.
    """
    if stream_class is stream.Score:
        post_stream = stream.Score()
    elif stream_class is stream.Part:
        post_stream = stream.Part()
    elif stream_class is stream.Voice:
        post_stream = stream.Voice()

    for element in original_stream.elements:
        post_stream.append(element)
    return post_stream


def stream_to_notes(
    original_stream: stream.Stream, in_place: bool = False
) -> List[note.Note]:
    """Returns a list of all notes contained in a Stream

    Args:
        original_stream: Stream to process.
        in_place: Optional; If True, returns references to Note objects in the original stream, else
          returns new copies. Default is True.

    Returns:
        The list of Note objects.

    """
    notes = []
    for note_ in original_stream.flat.notes:
        if in_place:
            notes.append(note_)
        else:
            notes.append(copy.deepcopy(note_))
    return notes


def stream_to_pitches(
    original_stream: stream.Stream, in_place: bool = False
) -> List[pitch.Pitch]:
    """Returns a list of all pitches contained in a Stream

    Args:
        original_stream: Stream to process.
        in_place: Optional; If True, returns references to Pitch objects in the original stream,
          else returns new copies. Default is True.

    Returns:
        The list of Pitch objects.

    """
    pitches = []
    for note_ in stream_to_notes(original_stream, in_place=in_place):
        if note_.isChord:
            element_pitches = note_.pitches
        else:
            element_pitches = [note_.pitch]

        for pitch_ in element_pitches:
            if in_place:
                pitches.append(pitch_)
            else:
                pitches.append(copy.deepcopy(pitch_))

    return pitches


def notes_to_stream(
    pitches: Sequence[Union[numbers.Number, str, pitch.Pitch, note.Note, chord.Chord]]
) -> stream.Stream:
    """Creates a stream from a sequence of pitches.

    Args:
        pitches: Sequence of pitches to convert to a stream. Sequence can consist of pitch classes
          (0-11), midi note numbers (12+), note names (str), music21 Pitch objects, music21
          Note objects or music21 Chord objects.

    Returns:
        Stream containing a sequence of notes with the corresponding pitches.
    """
    post_stream = stream.Stream()
    for pitch_ in pitches:
        if isinstance(pitch_, (str, pitch.Pitch)):
            post_stream.append(note.Note(pitch_))
        elif isinstance(pitch_, numbers.Number):
            note_ = note.Note(pitch_)
            if note_.pitch.accidental.name == "natural":
                note_.pitch.accidental = None
            post_stream.append(note_)
        elif isinstance(pitch_, (note.Note, chord.Chord)):
            post_stream.append(pitch_)
    return post_stream


def durations_to_stream(
    durations: Sequence[Union[numbers.Number, duration.Duration, note.Note]]
):
    """Converts a sequence of durations to a Stream containing note objects of that duration.

    Args:
        durations: Sequence of durations to convert to a stream. Sequence can consist of numeric
          values (1 = quarter note), music21 Duration objects or music21 Note objects.

    Returns:
        Stream containing a sequence of notes with the corresponding durations.
    """
    post_stream = stream.Stream()
    for duration_ in durations:
        if isinstance(duration_, numbers.Number):
            new_note = note.Note()
            new_note.duration = duration.Duration(duration_)
            post_stream.append(new_note)
        elif isinstance(duration_, duration.Duration):
            new_note = note.Note()
            new_note.duration = duration_
            post_stream.append(new_note)
        elif isinstance(duration_, note.Note):
            post_stream.append(duration_)
    return post_stream


def merge_streams(
    *streams: stream.Stream,
    stream_class: Optional[Type[Union[stream.Voice, stream.Part, stream.Score]]] = None
) -> stream.Stream:
    """

    Creates a new stream by combining streams vertically.

    Args:
        *streams: Streams to merge.
        stream_class: Optional; The type of stream to convert to (Score, Part or Voice). By
        default, a generic Stream is returned.

    Returns:

    """
    if stream_class is None:
        post_stream = stream.Stream()
    if stream_class is stream.Score:
        post_stream = stream.Score()
    elif stream_class is stream.Part:
        post_stream = stream.Part()
    elif stream_class is stream.Voice:
        post_stream = stream.Voice()
    for stream_ in streams:
        post_stream.insert(0, stream_)
    return post_stream


def append_stream(original_stream: stream.Stream, *streams: stream.Stream):
    """

    Appends all elements of one or more streams at the end of a stream.

    Args:
        original_stream: The stream to append to.
        *streams: Any number of streams to be appended to the original stream.
    """
    for stream_ in streams:
        h_offset = original_stream.highestTime
        for element in stream_.elements:
            original_stream.insert(element.offset + h_offset, element)
