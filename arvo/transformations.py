import music21
from copy import deepcopy


def scaleSpaceTransposition(
    originalStream,
    scaleInterval,
    referenceScale=music21.scale.ChromaticScale,
    inPlace=False,
):
    if inPlace:
        newStream = originalStream
    else:
        newStream = deepcopy(originalStream)

    for streamPitch in newStream.pitches:
        _transposePitchInScaleSpace(streamPitch, scaleInterval, referenceScale)

    return newStream


def scaleSpaceInversion(
    originalStream,
    inversionAxis,
    referenceScale=music21.scale.ChromaticScale,
    inPlace=False,
):

    if inPlace:
        newStream = originalStream
    else:
        newStream = deepcopy(originalStream)

    for streamPitch in newStream.pitches:
        distanceFromAxis = _getScaleDistance(inversionAxis, streamPitch, referenceScale)
        _transposePitchInScaleSpace(streamPitch, distanceFromAxis * -2, referenceScale)

    return newStream


def octaveShift(originalStream, octaveInterval, inPlace=False):
    if inPlace:
        newStream = originalStream
    else:
        newStream = deepcopy(originalStream)

    for streamPitch in newStream.pitches:
        streamPitch.ps += 12 * octaveInterval

    return newStream


def _transposePitchInScaleSpace(originalPitch, scaleInterval, referenceScale):
    if scaleInterval == 0:
        return
    if isinstance(originalPitch, str):
        originalPitch = music21.pitch.Pitch(originalPitch)
    if scaleInterval > 0:
        direction = "ascending"
    else:
        direction = "descending"
        scaleInterval *= -1
    newPitch = referenceScale.next(originalPitch, direction, scaleInterval)
    originalPitch.ps = newPitch.ps


def _getScaleDistance(pitchA, pitchB, referenceScale):
    if isinstance(pitchA, str):
        pitchA = music21.pitch.Pitch(pitchA)
    if isinstance(pitchB, str):
        pitchB = music21.pitch.Pitch(pitchB)

    if pitchA.ps == pitchB.ps:
        return 0

    direction = "ascending"
    if pitchB.ps < pitchA.ps:
        direction = "descending"

    scaleDistance = 0
    while True:
        scaleDistance += 1
        nextPitch = referenceScale.next(pitchA, direction, scaleDistance)
        if nextPitch.ps == pitchB.ps:
            break
        if scaleDistance > 1000:
            return 0

    if direction == "descending":
        scaleDistance *= -1

    return scaleDistance
