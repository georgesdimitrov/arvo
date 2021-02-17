from arvo import isorhythm
from arvo import minimalism
from arvo import tintinnabuli
from arvo import tools
from arvo import transformations
from music21 import meter
from music21 import scale
from music21 import metadata

# Set reference scale (A Major Phrygian) for inversion/transposition operations
# ----------------------------------------------------------------------------------------------------------------------
reference_scale = scale.ConcreteScale(
    pitches=["A4", "B-4", "C#5", "D5", "E5", "F5", "G5"]
)

# Build core scale pattern
# ----------------------------------------------------------------------------------------------------------------------
basic_scale = isorhythm.create_isorhythm(
    reference_scale.getPitches("C#6", "G5") + reference_scale.getPitches("F6", "C#6"),
    [2, 1, 1, 1, 1, 1, 1, 3],
)

# Build the complete m-voice
# ----------------------------------------------------------------------------------------------------------------------
m_voice = minimalism.additive_process(
    basic_scale, direction=minimalism.Direction.INWARD, starting_iteration=2
)
m_voice.append(transformations.scalar_inversion(m_voice, "C#6", reference_scale))

# Create the t-voice and the second m-voice
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
