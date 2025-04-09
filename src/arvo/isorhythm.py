"""Module for generating isorhythmic constructions from pitch and rhythm sequences.

An isorhythm combines a repeating sequence of pitches (color) with a repeating
sequence of durations (talea). This module builds a music21 Stream by cycling
through both sequences.
"""

from typing import Optional
from dataclasses import dataclass

from music21 import stream

from arvo import core
from arvo import tools

__all__ = ["create_isorhythm"]


@dataclass
class Options:
    """Configuration options for the isorhythmic process.

    Attributes:
        length: Optional number of elements in the resulting stream. If not specified,
            the process continues until the combined pitch and rhythm cycles
            complete a full loop (i.e., least common multiple of their lengths).
            For example, a color of 5 pitches and a talea of 7 durations would
            produce 35 elements by default.
    """

    length: Optional[int] = None


def create_isorhythm(
    pitches: core.PitchesSequence | stream.Stream,
    durations: core.DurationsSequence | stream.Stream,
    options: Optional[Options] = None,
) -> stream.Stream:
    """Creates an isorhythmic construction from pitch and duration sequences.

    The function cycles through the pitch and rhythm inputs independently, combining
    them element by element. If no length is specified, the process stops after
    both sequences align (i.e., complete one full shared cycle).

    Args:
        pitches: A pitch sequence or music21 Stream. Acceptable inputs include:
            - Pitch classes (0–11)
            - MIDI numbers (12+)
            - Note names (e.g., "C4")
            - music21 Pitch or GeneralNote objects
            If a Stream is given, it is flattened and its note, chord and rest
            elements are extracted.
        durations: A duration sequence or music21 Stream. Acceptable inputs include:
            - Numeric values (1 = quarter note)
            - music21 Duration or GeneralNote objects
            Like pitches, a Stream will be flattened and the duration of its note,
            chord and rest elements will be extracted.
        options: Optional configuration for the isorhythmic process.

    Returns:
        A music21 Stream containing the resulting isorhythmic structure.
    """
    options = options or Options()
    pitches = core.ArvoPitchesSequence(pitches)
    durations = core.ArvoDurationsSequence(durations)

    # Initialize function variables
    pitch_index = 0
    rhythm_index = 0
    element_count = 0
    post_stream = stream.Stream()

    # Loop
    while True:
        current_element = tools.create_note(
            pitches[pitch_index], durations[rhythm_index]
        )
        post_stream.append(current_element)
        pitch_index += 1
        if pitch_index == len(pitches):
            pitch_index = 0
        rhythm_index += 1
        if rhythm_index == len(durations):
            rhythm_index = 0
        element_count += 1
        if options.length is None and pitch_index == rhythm_index == 0:
            break
        if options.length is not None and element_count == options.length:
            break

    return post_stream
