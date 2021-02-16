from copy import deepcopy
import enum
from typing import Union, Sequence

from music21 import stream
from music21 import chord
from music21 import pitch
from music21 import note

"""
createTVoice generates a T-voice melodic stream from an M-voice melodic stream
Arguments:
	Stream m_voice: melodic stream
	Chord t_chord: resonance chord used to build the T-voice
	int position: T-voice position, usually 1 or 2
	string direction: T-Voice placement, "up", "down", "upAlternate" or "downAlternate"
"""


class Direction(enum.Enum):
    UP = 1
    DOWN = 2
    UP_ALTERNATE = 3
    DOWN_ALTERNATE = 4


class TMode(enum.Enum):
    DIATONIC = 1
    CHROMATIC = 2


def create_t_voice(
    m_voice: stream.Stream,
    t_chord: Union[Sequence[int], Sequence[str], chord.Chord],
    position: int = 1,
    direction: Direction = Direction.UP,
    t_mode: TMode = TMode.DIATONIC,
)-> stream.Stream:
    """Generates a t-voice melodic stream from a m-voice melodic stream.

    Args:
        m_voice: The stream containing the melody to use as the basis for the tintinnabuli.
        t_chord: A list of pitch-classes to use as the basis of the t-voice. Accepts letter names or numeric pitch
          classes. Can also be a music21 Chord object.
        position: Optional; The position of the t-voice. Default is 1.
        direction: Optional; The direction of the tintinnabuli process. Default is Direction.UP.
        t_mode: Optional; Determines the way the "next" note is calculated within the t-voice pitch classes for notes
          with the same note name. For example if the m-voice contains an Eb and the t-chord is C major: TMode.DIATONIC
          will consider that Eb and E are the same note, and will return G as the first "diatonic" t-note above.
          TMode.CHROMATIC ignores this and simply returns E as the first "chromatic" t-note above. Default is
          TMode.DIATONIC.

    Returns:
        A stream that contains the new t-voice.
    """
    # Create t-voice stream
    t_voice = stream.Stream()

    # Create t-voice pitch-class lists
    if isinstance(t_chord, chord.Chord):
        t_pitches = t_chord.pitches
    else:
        t_pitches = t_chord
    t_pitch_classes = []
    t_steps = []
    for p in t_pitches:
        if isinstance(p, str):
            p = pitch.Pitch(p)
        elif isinstance(p, int):
            p = pitch.Pitch(p)
        t_pitch_classes.append(p.pitchClass)
        t_steps.append(p.step)

    # Determine starting pitch direction
    if direction is Direction.DOWN or direction is Direction.DOWN_ALTERNATE:
        pitch_delta = -1
    elif direction is Direction.UP or direction is Direction.UP_ALTERNATE:
        pitch_delta = 1

    temp_pitch = pitch.Pitch()

    for m_note in m_voice.flat.notes:
        temp_pitch.ps = m_note.pitch.ps
        position_index = 0
        while position_index < position:
            temp_pitch.ps = temp_pitch.ps + pitch_delta
            if temp_pitch.pitchClass in t_pitch_classes:
                if t_mode is TMode.DIATONIC:
                    if (
                        temp_pitch.octave != m_note.pitch.octave
                        or temp_pitch.step != m_note.pitch.step
                    ):
                        position_index += 1
                else:
                    position_index += 1
        t_note = note.Note()
        t_note.pitch.ps = temp_pitch.ps
        t_note.duration = m_note.duration
        t_voice.insert(m_note.offset, t_note)
        if direction is Direction.UP_ALTERNATE or direction is Direction.DOWN_ALTERNATE:
            pitch_delta *= -1

    return t_voice
