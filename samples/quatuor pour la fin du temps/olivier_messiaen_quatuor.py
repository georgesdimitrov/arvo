"""

Frederic Rzewski - Coming Together

This example showcases the following arvo modules:

minimalism for creating the additive and substractive processes
transformations for scalar transposition and inversion, as well as retrograde
scales for the PentatonicScale subclass.

Since Rzewski applied mathematical processes in a very strict way to create the piece, the generated
output is 100% identical to the original score.

"""

from music21 import chord
from music21 import clef
from music21 import duration
from music21 import key
from music21 import layout
from music21 import metadata
from music21 import meter
from music21 import note
from music21 import stream
from arvo import isorhythm
from arvo import tools


# --------------------------------------------------------------------------------------------------
# Define pitch and duration sequences for the piano
# --------------------------------------------------------------------------------------------------

piano_left_hand_chords = [
    chord.Chord(["F3", "G3", "Bb3", "C4"]),
    chord.Chord(["F3", "G3", "Bb3", "C4"]),
    chord.Chord(["F3", "Ab3", "Bb3", "Db4"]),
    chord.Chord(["F3", "Ab3", "Bb3", "Db4"]),
    chord.Chord(["F3", "G3", "Bb3", "D4"]),
    chord.Chord(["F3", "G3", "Bb3", "D4"]),
    chord.Chord(["F3", "A3", "C4", "D4"]),
    chord.Chord(["F3", "A3", "C4", "D4"]),
    chord.Chord(["F3", "Bb3", "Db4"]),
    chord.Chord(["F3", "B3", "D4"]),
    chord.Chord(["F3", "C4", "Eb4"]),
    chord.Chord(["F3", "C#4", "E4"]),
    chord.Chord(["Ab3", "Eb4", "Gb4"]),
    chord.Chord(["Ab3", "Eb4", "F4"]),
    chord.Chord(["Gb3", "Db4", "Ab4"]),
    chord.Chord(["Gb3", "Db4", "Bb4"]),
    chord.Chord(["A3", "C4", "D4", "F#4", "Bb4"]),
    chord.Chord(["Bb3", "C#4", "E4", "G#4"]),
    chord.Chord(["C4", "D4", "F4"]),
    chord.Chord(["C#4", "E4", "F#4"]),
    chord.Chord(["F4", "G#4", "Bb4"]),
    chord.Chord(["F#4", "A4", "B4"]),
    chord.Chord(["F4", "Bb4"]),
    chord.Chord(["E4", "Ab4"]),
    chord.Chord(["D4", "G4"]),
    chord.Chord(["C#4", "F4"]),
    chord.Chord(["B3", "E4"]),
    chord.Chord(["Ab3", "C#4"]),
    chord.Chord(["Gb3", "Cb4"]),
]

piano_right_hand_chords = [
    chord.Chord(["Eb4", "B4", "E5"]),
    chord.Chord(["Eb4", "B4", "D5"]),
    chord.Chord(["Eb4", "B4", "D5"]),
    chord.Chord(["Eb4", "G4", "C5"]),
    chord.Chord(["F#4", "B4", "C5"]),
    chord.Chord(["E4", "A4", "C5"]),
    chord.Chord(["G4", "C#5", "F#5"]),
    chord.Chord(["G4", "B4", "E5"]),
    chord.Chord(["Gb4", "E5"]),
    chord.Chord(["G4", "E5", "G5"]),
    chord.Chord(["Ab4", "G5"]),
    chord.Chord(["A4", "G5", "B5"]),
    chord.Chord(["Bb4", "Eb5", "Gb5", "Cb6"]),
    chord.Chord(["Bb4", "Db5", "F5", "Bb5"]),
    chord.Chord(["Eb5", "Ab5", "Cb6", "Eb6"]),
    chord.Chord(["D5", "F5", "Bb5", "D6"]),
    chord.Chord(["Db5", "Gb5", "Bb5", "Db6"]),
    chord.Chord(["C5", "D5", "G#5", "C6"]),
    chord.Chord(["A4", "C#5", "E5", "A5"]),
    chord.Chord(["Bb4", "D5", "F5"]),
    chord.Chord(["D5", "F#5", "A5"]),
    chord.Chord(["D#5", "E#5", "G#5"]),
    chord.Chord(["D5", "E5", "G5"]),
    chord.Chord(["C#5", "D5"]),
    chord.Chord(["B4", "C#5", "E5"]),
    chord.Chord(["Bb4", "B4", "F5"]),
    chord.Chord(["Ab4", "Bb4"]),
    chord.Chord(["F4", "G4"]),
    chord.Chord(["Eb4", "F4"]),
]

piano_durations = [
    1,
    1,
    1,
    0.5,
    0.75,
    0.5,
    0.5,
    0.5,
    0.5,
    0.75,
    0.75,
    0.75,
    0.25,
    0.5,
    0.75,
    1,
    2,
]

# --------------------------------------------------------------------------------------------------
# Define pitch and duration sequences for the cello
# --------------------------------------------------------------------------------------------------

cello_notes = ["C4", "E4", "D4", "F#4", "Bb3"]
cello_durations = [2, 1.5, 2, 2, 0.5, 0.5, 1.5, 0.5, 0.5, 0.5, 0.5, 1.5, 0.5, 0.5, 2]


# --------------------------------------------------------------------------------------------------
# Create isorhythms
# --------------------------------------------------------------------------------------------------

piano_right_hand = isorhythm.create_isorhythm(
    piano_right_hand_chords, piano_durations, length=167
)
piano_left_hand = isorhythm.create_isorhythm(
    piano_left_hand_chords, piano_durations, length=167
)
cello = isorhythm.create_isorhythm(cello_notes, cello_durations, length=109)

# --------------------------------------------------------------------------------------------------
# Add time signatures, rests, clefs...
# --------------------------------------------------------------------------------------------------

piano_right_hand.insertAndShift(0, note.Rest(duration=duration.Duration(2)))
piano_right_hand.insert(0, meter.TimeSignature("3/4"))
piano_right_hand.insert(key.KeySignature(-2))
piano_right_hand.notes[len(piano_right_hand.notes) - 1].duration = duration.Duration(
    1.25
)
piano_right_hand.makeMeasures(inPlace=True)

piano_left_hand.insertAndShift(0, note.Rest(duration=duration.Duration(2)))
piano_left_hand.insert(key.KeySignature(-2))
piano_left_hand.insert(0, meter.TimeSignature("3/4"))
piano_left_hand.notes[len(piano_left_hand.notes) - 1].duration = duration.Duration(1.25)
piano_left_hand.insert(0, clef.BassClef())
for n in piano_left_hand.notes:
    if n.pitches == chord.Chord(["F4", "G#4", "Bb4"]).pitches:
        piano_left_hand.insert(n.offset, clef.TrebleClef())
    if n.pitches == chord.Chord(["Ab3", "C#4"]).pitches:
        piano_left_hand.insert(n.offset, clef.BassClef())
piano_left_hand.makeMeasures(inPlace=True)

cello.insertAndShift(0, note.Rest(duration=duration.Duration(5.5)))
cello.insert(0, meter.TimeSignature("3/4"))
cello.insert(key.KeySignature(-2))
cello.insert(0, clef.TenorClef())
cello.notes[len(cello.notes) - 1].duration = duration.Duration(2.5)  # Extend final note
for n in cello.notes:
    harmonicNote = note.Note()
    harmonicNote.pitch.ps = n.pitch.ps + 5
    harmonicNote.notehead = "diamond"
    harmonicNote.noteheadFill = "no"
    c = chord.Chord(notes=[n, harmonicNote], duration=n.duration)
    cello.insert(n.offset, c)
    cello.remove(n)
cello.makeMeasures(inPlace=True)

# --------------------------------------------------------------------------------------------------
# Build final score
# --------------------------------------------------------------------------------------------------

piano_right_hand = tools.convert_stream(piano_right_hand, stream.Part)
piano_left_hand = tools.convert_stream(piano_left_hand, stream.Part)
cello = tools.convert_stream(cello, stream.Part)
cello.partName = "Vc."
score = tools.merge_streams(
    cello, piano_right_hand, piano_left_hand, stream_class=stream.Score
)
piano_staff_group = layout.StaffGroup(
    [piano_right_hand, piano_left_hand],
    name="Piano",
    abbreviation="Pno.",
    symbol="brace",
)
score.insert(0, piano_staff_group)
score.metadata = metadata.Metadata()
score.metadata.title = "Liturgie de Cristal"
score.metadata.composer = "Olivier Messiaen"

# --------------------------------------------------------------------------------------------------
# Output xml file and show score in MuseScore
# --------------------------------------------------------------------------------------------------
score.write(fp="olivier_messiaen_quatuor.xml")
score.show()
