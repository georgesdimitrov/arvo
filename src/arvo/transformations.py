"""
Module for transformations such as transposition and inversion.
"""
import copy
from typing import Union

from music21 import pitch
from music21 import scale
from music21 import stream

__all__ = ["scalar_transposition", "scalar_inversion", "octave_shift"]


def scalar_transposition(
    original_stream: stream.Stream,
    steps: int,
    reference_scale: scale.ConcreteScale = scale.ChromaticScale("C"),
    in_place: bool = False,
) -> stream.Stream:
    """Performs scale-space transpotition on a stream.

    Transposes all notes in a stream by a specified amount of scale steps in a specific scale space.

    Args:
        original_stream: The stream to process.
        steps: The amount of steps to transpose. Positive values transpose up, negative values
          transpose down.
        reference_scale: Optional; The scale to use as reference. By default, the chromatic scale
          is used.
        in_place: Optional; If true, the operation is done in place on the original stream. By
          default, a new Stream object is returned.

    Returns:
        The transposed stream.
    """
    # Check if stream is to be processed in place
    post_stream = original_stream if in_place else copy.deepcopy(original_stream)

    # Transpose all individual pitches
    for pitch_ in post_stream.pitches:
        _transpose_pitch_in_scale_space(pitch_, steps, reference_scale)

    return post_stream


def scalar_inversion(
    original_stream: stream.Stream,
    inversion_axis: Union[str, pitch.Pitch],
    reference_scale: scale.ConcreteScale = scale.ChromaticScale("C"),
    in_place: bool = False,
) -> stream.Stream:
    """Performs a scale-space inversion on a stream.

    Args:
        original_stream: The stream to process.
        inversion_axis: The pitch around which to execute the inversion.
        reference_scale: Optional; The scale to use as reference. By default, the chromatic scale is
          used.
        in_place: Optional; If true, the operation is done in place on the original stream. By
          default, a new Stream object is returned.

    Returns:
        The inverted stream.
    """
    # Check if stream is to be processed in place
    post_stream = original_stream if in_place else copy.deepcopy(original_stream)

    # Check if inversion_axis is Pitch
    if isinstance(inversion_axis, str):
        inversion_axis = pitch.Pitch(inversion_axis)

    # Invert all individual pitches
    for pitch_ in post_stream.pitches:
        distance_from_axis = _get_scale_distance(
            inversion_axis, pitch_, reference_scale
        )
        _transpose_pitch_in_scale_space(
            pitch_, distance_from_axis * -2, reference_scale
        )

    return post_stream


def retrograde(
    original_stream: stream.Stream,
    in_place: bool = False,
) -> stream.Stream:
    """Performs a retrograde operation on a Stream.

    Args:
        original_stream: The Stream to process.
        in_place: Optional; If true, the operation is done in place on the original stream. By
          default, a new Stream object is returned.

    Returns:
        The reversed Stream.
    """
    # Check if stream is to be processed in place
    post_stream = original_stream if in_place else copy.deepcopy(original_stream)

    # Extract list of notes and clear stream of bars and notes
    notes = list(post_stream.flat.notes)
    post_stream.removeByClass("Barline")
    post_stream.removeByClass("Measure")
    post_stream.remove(notes, recurse=True)

    # Build new stream of notes in reverse order
    reverse_stream = stream.Stream()
    for note_ in reversed(notes):
        reverse_stream.append(note_)

    # Put back notes in the stream
    for note_ in reverse_stream.notes:
        post_stream.insert(note_.offset, note_)

    post_stream.sort()
    #post_stream.makeMeasures(inPlace=True)

    return post_stream


def octave_shift(original_stream: stream.Stream, octave_interval, in_place=False):
    """Transpooses a Stream up or down by a number of octaves

    Args:
        original_stream: Stream to process.
        octave_interval: The octave shift. Postive numbers transpose up, negative numbers transpose
          down.
        in_place: Optional; If true, the operation is done in place on the original stream. By
          default, a new Stream object is returned.

    Returns:
        The transposed Stream.
    """
    # Check if stream is to be processed in place
    post_stream = original_stream if in_place else copy.deepcopy(original_stream)

    # Transpose all individual pitches
    for pitch_ in post_stream.pitches:
        pitch_.ps += 12 * octave_interval

    return post_stream


def _transpose_pitch_in_scale_space(
    original_pitch: pitch.Pitch,
    steps: int,
    reference_scale: scale.ConcreteScale,
) -> pitch.Pitch:
    if steps == 0:
        return
    if steps > 0:
        direction = "ascending"
    else:
        direction = "descending"
        steps *= -1
    new_pitch = reference_scale.next(original_pitch, direction, steps)
    original_pitch.step = new_pitch.step
    original_pitch.octave = new_pitch.octave
    original_pitch.accidental = new_pitch.accidental


def _get_scale_distance(pitch_a, pitch_b, reference_scale):
    if isinstance(pitch_a, str):
        pitch_a = pitch.Pitch(pitch_a)
    if isinstance(pitch_b, str):
        pitch_b = pitch.Pitch(pitch_b)

    if pitch_a.ps == pitch_b.ps:
        return 0

    direction = "ascending"
    if pitch_b.ps < pitch_a.ps:
        direction = "descending"

    scale_distance = 0
    while True:
        scale_distance += 1
        next_pitch = reference_scale.next(pitch_a, direction, scale_distance)
        if next_pitch.ps == pitch_b.ps:
            break
        if scale_distance > 1000:
            return 0

    if direction == "descending":
        scale_distance *= -1

    return scale_distance
