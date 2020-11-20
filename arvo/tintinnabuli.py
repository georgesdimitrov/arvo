from copy import deepcopy

import music21

"""
createTVoice generates a T-voice melodic stream from an M-voice melodic stream
Arguments:
	Stream m_voice: melodic stream
	Chord t_chord: resonance chord used to build the T-voice
	int position: T-voice position, usually 1 or 2
	string direction: T-Voice placement, "up", "down", "upAlternate" or "downAlternate"
"""


def createT_Voice(m_voice, t_chordOrChordPitches, position, direction, ignoreSameDiatonicPitch=True):
    t_voice = music21.stream.Stream()
    if isinstance(t_chordOrChordPitches, music21.chord.Chord):
        t_pitches = t_chordOrChordPitches.pitches
    else:
        t_pitches = t_chordOrChordPitches
    t_pitchClasses = []
    t_steps = []
    for p in t_pitches:
        t_pitchClasses.append(p.pitchClass)
        t_steps.append(p.step)

    if direction == "down" or direction == "downAlternate":
        pitchDelta = -1
    elif direction == "up" or direction == "upAlternate":
        pitchDelta = 1

    tempPitch = music21.pitch.Pitch()

    for m_note in m_voice.flat.notes:
        tempPitch.ps = m_note.pitch.ps
        positionIndex = 0
        while positionIndex < position:
            tempPitch.ps = tempPitch.ps + pitchDelta
            if tempPitch.pitchClass in t_pitchClasses:
                if ignoreSameDiatonicPitch:
                    if tempPitch.octave != m_note.pitch.octave or tempPitch.step != m_note.pitch.step:
                        positionIndex += 1
                else:
                    positionIndex += 1
        t_note = music21.note.Note()
        t_note.pitch.ps = tempPitch.ps
        t_note.duration = m_note.duration
        t_voice.insert(m_note.offset, t_note)
        if direction == "downAlternate" or direction == "upAlternate":
            pitchDelta *= -1

    return t_voice


"""
def createParallelVoice(m_voice, transpositionInterval, keySignature=None):
    parallelVoice = deepcopy(m_voice)
    if keySignature is None:
        parallelVoice.transpose(transpositionInterval, True)
    else:
        parallelVoice.insert(0, keySignature)
        parallelVoice.transpose(
            music21.interval.GenericInterval(transpositionInterval), True
        )
    return parallelVoice
"""
