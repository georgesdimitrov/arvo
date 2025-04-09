"""
Functions for generating Arvo Pärt-inspired tintinnabuli voices.

Tintinnabuli is a compositional technique characterized by pairing melodic lines
(M-voices) with notes drawn exclusively from a tonic chord (T-chord), creating
bell-like textures. This module implements processes to create tintinnabuli voices
according to specified directions and modes.
"""

import enum
from typing import Optional, Sequence
from dataclasses import dataclass

from music21 import stream
from music21 import pitch
from music21 import note


__all__ = ["Direction", "TMode", "create_t_voice"]

from arvo import core
from arvo import tools


class Direction(enum.Enum):
    """
    Specifies the direction in which the tintinnabuli voice searches for chord tones
    relative to the M-voice pitches.
    """

    UP = 1
    DOWN = 2
    UP_ALTERNATE = 3
    DOWN_ALTERNATE = 4


class TMode(enum.Enum):
    """
    Specifies how the next t-voice note is determined when encountering notes
    enharmonic to the T-chord.

    For instance, given an M-voice note "Eb" and a T-chord of C major:
    - DIATONIC mode treats "Eb" and "E" as equivalent, returning the next diatonic
    T-note above (G).
    - CHROMATIC mode distinguishes "Eb" from "E," returning the chromatically
    nearest T-note (E).
    """

    DIATONIC = 1
    CHROMATIC = 2


@dataclass
class Options:
    """
    Configuration options for generating a tintinnabuli voice.

    Attributes:
        position: The chord interval at which t-note will be generated relative to
        each melodic note (1 indicates the closest chord tone, 2 the second closest,
        etc.). Default is 1.
        direction: Direction in which to search for chord tones. Default is
        Direction.UP.
        mode: Method used for calculating the next note when encountering
        enharmonic notes.
            See TMode documentation for details. Default is TMode.DIATONIC.
    """

    position: int = 1
    direction: Direction = Direction.UP
    mode: TMode = TMode.DIATONIC


@dataclass
class _TChord:
    """Class containing data for t-chord pitches."""

    def __init__(self, t_chord):
        self.pitch_classes = []
        self.steps = []
        self.pitch_names = []
        for pitch_ in t_chord:
            if isinstance(pitch_, str):
                pitch_ = pitch.Pitch(pitch_)
            elif isinstance(pitch_, int):
                pitch_ = pitch.Pitch(pitch_)
            elif isinstance(pitch_, note.Note):
                pitch_ = pitch_.pitch
            self.pitch_classes.append(pitch_.pitchClass)
            self.steps.append(pitch_.step)
            self.pitch_names.append(pitch_.name)


class _Tintinnabuli:
    """
    Internal class implementing the tintinnabuli voice-generation process given an
    M-voice and a T-chord.
    """

    def __init__(self, m_voice, t_chord, options):
        self._options = options or Options()
        self._m_voice = core.ArvoPitchesSequence(m_voice)
        self._t_chord = _TChord(t_chord)
        self._t_notes = []
        match self._options.direction:
            case Direction.UP | Direction.UP_ALTERNATE:
                self._pitch_delta = 1
            case Direction.DOWN | Direction.DOWN_ALTERNATE:
                self._pitch_delta = -1

    def apply_process(self):
        temp_pitch = pitch.Pitch()

        for m_element in self._m_voice:
            m_note = tools.to_note(m_element, True)
            temp_pitch.ps = m_note.pitch.ps
            position_index = 0
            while position_index < self._options.position:
                temp_pitch.ps = temp_pitch.ps + self._pitch_delta
                if temp_pitch.pitchClass in self._t_chord.pitch_classes:
                    if temp_pitch.name not in self._t_chord.pitch_names:
                        temp_pitch = temp_pitch.getEnharmonic()
                    if self._options.mode is TMode.DIATONIC:
                        if (
                            temp_pitch.octave != m_note.pitch.octave
                            or temp_pitch.step != m_note.pitch.step
                        ):
                            position_index += 1
                    else:
                        position_index += 1
            t_note = note.Note()
            t_note.name = temp_pitch.name
            t_note.octave = temp_pitch.octave
            t_note.duration = m_note.duration
            t_note.offset = m_note.offset
            self._t_notes.append(t_note)
            if (
                self._options.direction is Direction.UP_ALTERNATE
                or self._options.direction is Direction.DOWN_ALTERNATE
            ):
                self._pitch_delta *= -1

    @property
    def result(self):
        if self._m_voice.is_stream:
            t_stream = stream.Stream()
            for t_note in self._t_notes:
                t_stream.insert(t_note.offset, t_note)
            return t_stream
        return [t_note.pitch for t_note in self._t_notes]


def create_t_voice(
    m_voice: core.PitchesSequence | stream.Stream,
    t_chord: core.PitchesSequence | stream.Stream,
    options: Optional[Options] = None,
) -> Sequence[pitch.Pitch] | stream.Stream:
    """
    Generates a tintinnabuli (T-voice) melody from a given melodic (M-voice) melody
    and T-chord.

    Accepts either a sequence of pitches or a music21 Stream as input:
    - If provided a pitch sequence, returns a corresponding sequence of T pitches.
    - If provided a music21 Stream, returns a new Stream of T notes matching the
    durations and offsets of the original M-voice notes.

    Args:
        m_voice: Sequence or Stream of melodic pitches or notes serving as the M-voice.
        t_chord: Sequence of pitch-classes or a music21 Chord object defining the
        T-chord.
        options: Optional tintinnabuli settings controlling voice generation.

    Returns:
        A Sequence of pitches or a Stream of notes representing the generated T-voice.
    """
    tintinnabuli = _Tintinnabuli(m_voice, t_chord, options)
    tintinnabuli.apply_process()
    return tintinnabuli.result
