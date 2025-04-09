"""
Convenient helper functions for manipulating, converting, and combining music21
elements.
"""

import copy
import numbers
from typing import Union, Sequence, Optional, Type, List, Iterable, TypeVar
from music21 import duration
from music21 import note
from music21 import stream
from music21 import pitch
from music21.note import GeneralNote, Note

T = TypeVar("T")

__all__ = [
    "convert_stream",
    "notes_to_stream",
    "durations_to_stream",
    "merge_streams",
    "append_stream",
    "create_note",
    "to_note",
    "to_duration",
    "flatten_sequence",
]


def convert_stream(
    original_stream: stream.Stream,
    stream_class: Type[Union[stream.Voice, stream.Part, stream.Score]],
) -> stream.Stream:
    """Converts a stream to the specified type.

    Args:
        original_stream: The stream to convert.
        stream_class: The type of stream to convert to (`Score`, `Part`, or `Voice`).

    Returns:
        The converted stream.
    """
    if stream_class is stream.Score:
        post_stream = stream.Score()
    elif stream_class is stream.Part:
        post_stream = stream.Part()
    elif stream_class is stream.Voice:
        post_stream = stream.Voice()
    else:
        raise ValueError(f"Unsupported stream_class: {stream_class}")

    for element in original_stream.elements:
        post_stream.append(element)
    return post_stream


def notes_to_stream(
    pitches: Sequence[Union[int, str, pitch.Pitch, note.GeneralNote]],
) -> stream.Stream:
    """Creates a stream from a sequence of pitches.

    Args:
        pitches: Sequence of pitches to convert to a stream. Sequence can consist of
        pitch classes (0-11), midi note numbers (12+), note names (str), music21
        Pitch objects, music21 GeneralNote objects.

    Returns:
        Stream containing a sequence of notes with the corresponding pitches.
    """
    post_stream = stream.Stream()
    for pitch_ in pitches:
        post_stream.append(to_note(pitch_))
    return post_stream


def durations_to_stream(
    durations: Sequence[Union[numbers.Number, duration.Duration, note.GeneralNote]],
) -> stream.Stream:
    """Converts a sequence of durations to a Stream containing note objects of that
    duration.

    Args:
        durations: Sequence of durations to convert to a stream. Sequence can
        consist of numeric
          values (1 = quarter note), music21 Duration objects or music21 Note objects.

    Returns:
        Stream containing a sequence of notes with the corresponding durations.
    """
    post_stream = stream.Stream()
    for duration_ in durations:
        if isinstance(duration_, note.GeneralNote):
            post_stream.append(duration_)
        else:
            post_stream.append(note.Note(duration=to_duration(duration_)))
    return post_stream


def to_duration(
    duration_: Union[numbers.Number, duration.Duration, note.GeneralNote],
    in_place: bool = False,
):
    """
    Creates a music21 Duration object from a numeric value, Duration, or GeneralNote.

    Args:
        duration_: Number (quarterLength), Duration, or Note/GeneralNote to derive
        the duration from.
        in_place: If True and duration_ is already a Duration, returns it directly
        without copying.

    Returns:
        A music21 Duration object. Defaults to quarter note if input is invalid.
    """
    if isinstance(duration_, duration.Duration):
        return duration_ if in_place else copy.deepcopy(duration_)
    if isinstance(duration_, numbers.Number):
        return duration.Duration(duration_)
    if isinstance(duration_, note.GeneralNote):
        return duration_.duration

    return duration.Duration()


def to_note(
    note_: Union[int, str, pitch.Pitch, note.GeneralNote], in_place: bool = False
) -> GeneralNote | Note:
    """
    Creates a music21 Note from various pitch representations.

    Args:
        note_: MIDI number, note name string, Pitch object, or Note/GeneralNote.
        in_place: If True and note_ is already a Note, returns it directly without
        copying.

    Returns:
        A music21 Note object. Defaults to middle C if input is invalid.
    """

    if isinstance(note_, note.GeneralNote):
        return note_ if in_place else copy.deepcopy(note_)
    if isinstance(note_, int):
        n = note.Note(note_)
        if n.pitch.accidental is not None and n.pitch.accidental.name == "natural":
            n.pitch.accidental = None
        return n
    if isinstance(note_, str):
        return note.Note(note_)
    if isinstance(note_, pitch.Pitch):
        return note.Note(note_)

    return note.Note()


def create_note(
    note_: Union[int, str, pitch.Pitch, note.GeneralNote],
    duration_: Union[numbers.Number, duration.Duration, note.GeneralNote],
    in_place: bool = False,
) -> note.Note:
    """
    Creates a music21 Note with specified pitch and duration.

    Args:
        note_: Pitch representation (MIDI note number, name, Pitch object, or Note).
        duration_: Duration representation (number, Duration object, or Note).
        in_place: If True, existing Note or Duration objects aren't copied.

    Returns:
        A music21 Note object.
    """
    n = to_note(note_, in_place)
    n.duration = to_duration(duration_, in_place)
    return n


def merge_streams(
    *streams: stream.Stream,
    stream_class: Optional[Type[Union[stream.Voice, stream.Part, stream.Score]]] = None,
) -> stream.Stream:
    """
    Combines multiple streams vertically into a new stream.

    Args:
        *streams: Streams to merge.
        stream_class: Optional; type of the resulting stream (`Score`, `Part`,
        or `Voice`). Defaults to a generic Stream.

    Returns:
        A new combined stream containing the provided streams inserted at offset 0.
    """
    if stream_class is stream.Score:
        post_stream = stream.Score()
    elif stream_class is stream.Part:
        post_stream = stream.Part()
    elif stream_class is stream.Voice:
        post_stream = stream.Voice()
    else:
        post_stream = stream.Stream()
    for stream_ in streams:
        post_stream.insert(0, stream_)
    return post_stream


def append_stream(original_stream: stream.Stream, *streams: stream.Stream) -> None:
    """
    Appends the elements of one or more streams sequentially to the end of the
    original stream.

    Args:
        original_stream: The target stream to append elements into.
        *streams: Streams whose elements will be appended after the original stream's
        end.
    """
    for stream_ in streams:
        h_offset = original_stream.highestTime
        for element in stream_.elements:
            original_stream.insert(element.offset + h_offset, element)


def flatten_sequence(xss: Iterable[Iterable[T]]) -> List[T]:
    """
    Flattens an iterable of iterables into a single list.

    Args:
        xss: An iterable of iterables to flatten.

    Returns:
        A flat list containing all elements.
    """
    return [x for xs in xss for x in xs]
