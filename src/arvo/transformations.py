"""
Module providing transformations, such as transposition, inversion, retrograde,
and octave shifts.
"""

import copy
from typing import Union

from music21 import pitch
from music21 import scale
from music21 import stream

__all__ = ["scalar_transposition", "scalar_inversion", "retrograde", "octave_shift"]


def scalar_transposition(
    original_stream: stream.Stream,
    steps: int,
    reference_scale: scale.ConcreteScale = scale.ChromaticScale("C"),
    in_place: bool = False,
) -> stream.Stream:
    """
    Performs scale-space transposition on a stream.

    Transposes all notes in a stream by a specified number of scale steps within a
    given reference scale.

    Args:
        original_stream: The stream to process.
        steps: The number of scale steps to transpose. Positive values transpose
        upward; negative values downward.
        reference_scale: The scale used as reference. Defaults to the chromatic scale.
        in_place: If True, modifies the original stream; otherwise returns a new stream.

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
    """
    Performs a scale-space inversion around a given pitch axis.

    Each pitch in the stream is inverted symmetrically around the inversion axis
    within the provided reference scale.

    Args:
        original_stream: The stream to invert.
        inversion_axis: The central pitch (as string or Pitch object) around which to
        invert.
        reference_scale: The scale used as reference. Defaults to the chromatic scale.
        in_place: If True, modifies the original stream; otherwise returns a new stream.

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
    """
    Reverses the order of notes within the stream (retrograde transformation).

    Args:
        original_stream: The stream to reverse.
        in_place: If True, modifies the original stream; otherwise returns a new stream.

    Returns:
        The reversed stream.
    """
    # Check if stream is to be processed in place
    post_stream = original_stream if in_place else copy.deepcopy(original_stream)

    # Flatten to simplify handling offsets
    flattened_notes = list(post_stream.flatten().notesAndRests)

    post_stream.remove(flattened_notes, recurse=True)

    # Reinsert notes in reversed order, recalculating offsets correctly
    current_offset = 0.0
    for element in reversed(flattened_notes):
        post_stream.insert(current_offset, element)
        current_offset += element.duration.quarterLength

    return post_stream


def octave_shift(
    original_stream: stream.Stream, octave_interval: int, in_place: bool = False
) -> stream.Stream:
    """
    Shifts all notes in the stream up or down by the specified number of octaves.

    Args:
        original_stream: Stream to transpose.
        octave_interval: Number of octaves to shift. Positive for upward, negative
        for downward shifts.
        in_place: If True, modifies the original stream; otherwise returns a new stream.

    Returns:
        The octave-shifted stream.
    """
    # Check if stream is to be processed in place
    post_stream = original_stream if in_place else copy.deepcopy(original_stream)

    # Transpose all individual pitches
    for pitch_ in post_stream.pitches:
        pitch_.octave += octave_interval

    return post_stream


def _transpose_pitch_in_scale_space(
    original_pitch: pitch.Pitch,
    steps: int,
    reference_scale: scale.ConcreteScale,
) -> None:
    if steps == 0:
        return
    if steps > 0:
        direction = scale.intervalNetwork.Direction.ASCENDING
    else:
        direction = scale.intervalNetwork.Direction.DESCENDING
        steps *= -1
    new_pitch = reference_scale.nextPitch(original_pitch, direction, steps)
    original_pitch.step = new_pitch.step
    original_pitch.octave = new_pitch.octave
    original_pitch.accidental = new_pitch.accidental


def _get_scale_distance(
    pitch_a: Union[str, pitch.Pitch],
    pitch_b: Union[str, pitch.Pitch],
    reference_scale: scale.ConcreteScale,
) -> int:
    if isinstance(pitch_a, str):
        pitch_a = pitch.Pitch(pitch_a)
    if isinstance(pitch_b, str):
        pitch_b = pitch.Pitch(pitch_b)

    if pitch_a.ps == pitch_b.ps:
        return 0

    ascending_distance = 0
    test_pitch = pitch_a
    # Try ascending
    while ascending_distance <= 1000:
        test_pitch = reference_scale.nextPitch(
            test_pitch, scale.intervalNetwork.Direction.ASCENDING, 1
        )
        ascending_distance += 1
        if test_pitch.ps == pitch_b.ps:
            return ascending_distance

    descending_distance = 0
    test_pitch = pitch_a
    # Try descending
    while descending_distance <= 1000:
        test_pitch = reference_scale.nextPitch(
            test_pitch, scale.intervalNetwork.Direction.DESCENDING, 1
        )
        descending_distance += 1
        if test_pitch.ps == pitch_b.ps:
            return -descending_distance

    # If not found, raise an error or handle gracefully
    raise ValueError(
        f"Scale distance between {pitch_a} and {pitch_b} exceeds 1000 steps."
    )


# octave shift preserves enharmonics
