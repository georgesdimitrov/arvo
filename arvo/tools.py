import music21
import math
from copy import deepcopy

# streamToPart converts a Stream to a Part
# Arguments:
# 	Stream original_stream: Stream to convert
def streamToPart(originalStream):
    newPart = music21.stream.Part()
    for element in originalStream.flat.notes:
        newPart.insert(element.offset, element)
    return newPart


def pitchesToStream(pitches):
    new_stream = music21.stream.Stream()
    for p in pitches:
        if isinstance(p, str):
            new_stream.append(music21.note.Note(p))
        elif isinstance(p, music21.pitch.Pitch):
            new_stream.append(music21.note.Note(p.nameWithOctave))
    return new_stream


def durationsToStream(durations):
    new_stream = music21.stream.Stream()
    for d in durations:
        new_note = music21.note.Note()
        new_note.duration = music21.duration.Duration(d)
        new_stream.append(new_note)
    return new_stream


def mapRhythmsToStream(original_stream, *durations):
    for i in range(len(durations)):
        original_stream.flat.notes[i].duration = music21.duration.Duration(durations[i])


def mergeStreams(*streamsToMerge):
    newStream = music21.stream.Stream()
    for s in streamsToMerge:
        newStream.insert(0, streamToPart(s))
    return newStream


def copyKeySignature(original_stream, new_stream):
    for key_signature in original_stream.getElementsByClass("KeySignature"):
        new_stream.insert(0, key_signature)
    return new_stream
