from arvo import isorhythm
from arvo import minimalism
from arvo import tintinnabuli
from arvo import tools
from arvo import transformations
from music21 import meter
from music21 import scale
from music21 import metadata

# Build core melody
# ----------------------------------------------------------------------------------------------------------------------
m_voice = isorhythm.create_isorhythm(
    ["C#6", "B-5", "A5", "G5", "F6", "E6", "D6", "C#6"], [2, 1, 1, 1, 1, 1, 1, 3]
)

# Set reference scale (A Major Phrygian) for inversion/transposition operations
# ----------------------------------------------------------------------------------------------------------------------
reference_scale = scale.ConcreteScale(
    pitches=["A4", "B-4", "C#5", "D5", "E5", "F5", "G5"]
)

# Create the complete M-voice using an additive process, and an inversion for the second half
# ----------------------------------------------------------------------------------------------------------------------
m_voice = minimalism.additive_process(
    m_voice, direction=minimalism.Direction.INWARD, step=[2, 1, 1]
)
m_voice_inversion = transformations.scalar_inversion(m_voice, "C#6", reference_scale)
m_voice.append(m_voice_inversion)

# Create the T-voice and the second M-voice
# ----------------------------------------------------------------------------------------------------------------------
t_chord = ["A", "C", "E"]
t_voice = tintinnabuli.create_t_voice(
    m_voice, t_chord, position=2, direction=tintinnabuli.Direction.DOWN
)
m_voice2 = transformations.scalar_transposition(m_voice, -9, reference_scale)

# Merge streams and add time signatures and titles
# ----------------------------------------------------------------------------------------------------------------------
score = tools.merge_streams(m_voice, t_voice, m_voice2)
score.insert(0, meter.TimeSignature("7/4"))
score.insert(7, meter.TimeSignature("9/4"))
score.insert(16, meter.TimeSignature("11/4"))
score.insert(27, meter.TimeSignature("7/4"))
score.insert(34, meter.TimeSignature("9/4"))
score.insert(43, meter.TimeSignature("11/4"))
score = score.flat.chordify()
score.insert(0, metadata.Metadata())
score.metadata.title = "Fratres"
score.metadata.composer = "Arvo Pärt"

# Output xml file and show score in MuseScore
# ----------------------------------------------------------------------------------------------------------------------
score.write(fp="arvo_part_fratres.xml")
score.show()
