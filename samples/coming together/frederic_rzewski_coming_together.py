from arvo import isorhythm
from arvo import minimalism
from arvo import scales
from arvo import transformations
from music21 import metadata
from music21 import stream
from music21 import expressions

# Set reference scale (G minor pentatonic) for inversion/transposition operations
# ----------------------------------------------------------------------------------------------------------------------
reference_scale = scales.PentatonicScale(tonic="G2", mode=5)

# Build core scale pattern
# ----------------------------------------------------------------------------------------------------------------------
basic_scale = isorhythm.create_isorhythm(
    reference_scale.getPitches("G2", "B-3"), [0.25]
)

# Build A section
# ----------------------------------------------------------------------------------------------------------------------
pattern_a = minimalism.additive_process(basic_scale)
section_a = minimalism.additive_process(pattern_a)
section_a.append(minimalism.subtractive_process(pattern_a, iterations_start=1))

# Build B section
# ----------------------------------------------------------------------------------------------------------------------
pattern_b = minimalism.subtractive_process(
    basic_scale, direction=minimalism.Direction.BACKWARD
)
section_b = minimalism.additive_process(pattern_b)
section_b.append(minimalism.subtractive_process(pattern_b, iterations_start=1))

# Build remaining sections
# ----------------------------------------------------------------------------------------------------------------------
section_c = transformations.retrograde(section_b)
section_d = transformations.scalar_inversion(section_b, "D3", reference_scale)
section_e = transformations.scalar_inversion(section_c, "D3", reference_scale)
section_h = transformations.retrograde(section_a)
section_g = transformations.scalar_inversion(section_a, "D3", reference_scale)
section_f = transformations.scalar_inversion(section_h, "D3", reference_scale)

# Combine streams and add titles and rehearsal marks
# ----------------------------------------------------------------------------------------------------------------------
score = stream.Stream()
score.append(
    [
        expressions.RehearsalMark("A"),
        section_a,
        expressions.RehearsalMark("B"),
        section_b,
        expressions.RehearsalMark("C"),
        section_c,
        expressions.RehearsalMark("D"),
        section_d,
        expressions.RehearsalMark("E"),
        section_e,
        expressions.RehearsalMark("F"),
        section_f,
        expressions.RehearsalMark("G"),
        section_g,
        expressions.RehearsalMark("H"),
        section_h,
    ]
)
score.insert(0, metadata.Metadata())
score.metadata.title = "Coming Together"
score.metadata.composer = "Frederic Rzewski"

# Output xml file and show score in MuseScore
# ----------------------------------------------------------------------------------------------------------------------
score.write(fp="frederic_rzewski_coming_together.xml")
score.show()
