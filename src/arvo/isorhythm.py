"""
Functions for generating isorhythmic constructions from pitch and rhythm sequences.
"""

import copy
import numbers
from typing import Optional, Union, Sequence

from music21 import stream
from music21 import duration
from music21 import pitch
from music21 import note
from music21 import chord

from arvo import tools


__all__ = ["create_isorhythm"]


def create_isorhythm(
    pitches: Union[
        stream.Stream, Sequence[Union[numbers.Number, str, pitch.Pitch, note.Note, chord.Chord]]
    ],
    durations: Union[
        stream.Stream, Sequence[Union[numbers.Number, duration.Duration, note.Note, chord.Chord]]
    ],
    length: Optional[int] = None,
) -> stream.Stream:

    """Creates an isorhythmic construction from pitches and durations sequences.

    Args:
        pitches: The stream or Sequence containing pitch information. Sequence can consist of
          pitch classes (0-11), midi note numbers (12+), note names (str), music21 Pitch objects
          or music21 Note objects.
        durations: The stream or Sequence containing duration information. Sequence can consist
          of numeric values (1 = quarter note), music21 Duration objects or music21 Note objects.
        length: Optional; The length of the resulting stream, expressed in isorhythmic elements.
          By default, the process continues until the cycle is completed. For example, provided a
          color of 5 pitches and a talea of 7 rhythms, this function will, by default, return an
          isorhythm of 35 elements.

    Returns:
        The stream created by the isorhythmic process.
    """

    # Create pitches list
    if not isinstance(pitches, stream.Stream):
        pitches = tools.notes_to_stream(pitches)
    color_list = []
    for element in pitches.flat.notes:
        color_list.append(element)

    # Create durations list
    if not isinstance(durations, stream.Stream):
        durations = tools.durations_to_stream(durations)
    talea_list = []
    for element in durations.flat.notes:
        talea_list.append(element.duration)

    # Initialize function variables
    color_index = 0
    talea_index = 0
    current_length = 0
    post_stream = stream.Stream()

    # Loop
    while True:
        current_element = copy.deepcopy(color_list[color_index])
        current_element.duration = talea_list[talea_index]
        post_stream.append(current_element)
        color_index += 1
        if color_index == len(color_list):
            color_index = 0
        talea_index += 1
        if talea_index == len(talea_list):
            talea_index = 0
        current_length += 1
        if length is None and color_index == 0 and talea_index == 0:
            break
        if length is not None and current_length == length:
            break

    return post_stream
