import music21
import tools
import math
from copy import deepcopy


def additiveProcess(
        originalStream, direction, progressionType="linear", numberOfRepetitions=1, numberOfIterations=0
):
    """

    Builds a new stream by applying an additive process to the original stream. Only note and
    chord objects are included.

    Parameters
    ----------
    originalStream : Stream
        The original stream to process
    direction : str
        Determines the direction of the additive process:
            "forward" starts building from the beginning of the stream
            "backward" starts building from the end of the stream
            "inward" starts building from the extremities of the stream inward
            "outward" starts building from the middle of the stream outward
    progressionType : str
        Determines the type of mathematical progression:
            "linear", "primes" or "fibonacci". Default is "linear".
    numberOfRepetitions : int
        Determines the number of times each segment is repeated before the next addition. Default is 1.
    numberOfIterations : int
        Overrides the number of iterations of the additive process. By default, it runs until
        the original stream is complete.

    Returns
    -------
    newStream : Stream
        The stream created by the additive process.

    """
    newStream = music21.stream.Stream()
    originalNotes = originalStream.flat.notes
    originalLength = len(originalNotes)
    progressionList = _getProgressionList(progressionType)
    progressionIndex = 0
    position1 = 0
    position2 = 0
    currentLength = progressionList[progressionIndex]
    completed = False

    while not completed:
        currentStream = music21.stream.Stream()
        if direction == "forward":
            position1 = 0
            position2 = currentLength
        elif direction == "backward":
            position1 = originalLength - currentLength
            position2 = originalLength
        elif direction == "inward":
            position1 = currentLength
            position2 = originalLength - currentLength
            if position1 >= position2:
                position1 = position2
                completed = True
        elif direction == "outward":
            position1 = math.floor(originalLength / 2.0 - currentLength)
            position2 = math.floor(originalLength / 2.0 + currentLength)
        if position1 < 0:
            position1 = 0
            completed = True
        if position2 >= originalLength:
            position2 = originalLength
            completed = True
        for _ in range(numberOfRepetitions):
            if direction == "inward":
                for i in range(0, position1):
                    currentStream.append(deepcopy(originalNotes[i]))
                for i in range(position2, originalLength):
                    currentStream.append(deepcopy(originalNotes[i]))
            else:
                for i in range(position1, position2):
                    currentStream.append(deepcopy(originalNotes[i]))
        newStream.append(currentStream)
        progressionIndex += 1
        if progressionIndex == numberOfIterations:
            completed = True
        currentLength = progressionList[progressionIndex]

    return newStream.flat


def substractiveProcess(originalStream, direction, progressionType="linear", numberOfRepetitions=1,
                        numberOfIterations=0):
    """

    Builds a new stream by applying an substractive process to the original stream. Only note and
    chord objects are included.

    ----------
    originalStream : Stream
        The original stream to process
    direction : str
        Determines the direction of the substractive process:
            "forward" starts substracting from the beginning of the stream
            "backward" starts substracting from the end of the stream
            "inward" starts substracting from the extremities of the stream inward
            "outward" starts substracting from the middle of the stream outward
    progressionType : str
        Determines the type of mathematical progression:
            "linear", "primes" or "fibonacci"
    numberOfRepetitions : int
        Determines the number of times each segment is repeated before the next substraction.
    numberOfIterations : int
        Overrides the number of iterations of the substractive process. By default, it runs until
        nothing is left of the original stream.

    Returns
    -------
    newStream : Stream
        The stream created by the additive process.

    """
    newStream = music21.stream.Stream()
    originalNotes = originalStream.flat.notes
    originalLength = len(originalNotes)
    progressionList = _getProgressionList(progressionType)
    progressionList.insert(0, 0)
    progressionIndex = 0

    position1 = 0
    position2 = 0
    currentLength = progressionList[progressionIndex]
    completed = False

    while not completed:
        currentStream = music21.stream.Stream()

        if direction == "forward":
            position1 = currentLength
            position2 = originalLength
            if position1 >= originalLength:
                position1 = originalLength
                completed = True
        elif direction == "backward":
            position1 = originalLength - currentLength
            position2 = 0
            if position1 < 0:
                position1 = 0
                completed = True
        elif direction == "inward":
            position1 = currentLength
            position2 = originalLength - currentLength
            if position2 < 0:
                position2 = 0
            if position1 >= position2:
                position1 = position2
                completed = True
        elif direction == "outward":
            position1 = math.floor(originalLength / 2.0 - currentLength)
            position2 = math.floor(originalLength / 2.0 + currentLength)
            if position1 < 0 and position2 >= originalLength:
                completed = True
            if position1 < 0:
                position1 = 0
            if position2 >= originalLength:
                position2 = originalLength

        for _ in range(numberOfRepetitions):
            if direction == "outward":
                for i in range(0, position1):
                    currentStream.append(deepcopy(originalNotes[i]))
                for i in range(position2, originalLength):
                    currentStream.append(deepcopy(originalNotes[i]))
            else:
                for i in range(position1, position2):
                    currentStream.append(deepcopy(originalNotes[i]))

        newStream.append(currentStream)
        progressionIndex += 1
        if progressionIndex == numberOfIterations:
            completed = True
        currentLength = progressionList[progressionIndex]

    return newStream.flat


def scanningProcess(originalStream, direction, progressionType, windowSize):
    """

    Builds a new stream by applying an scanning process to the original stream. Only note and
    chord objects are included.
    TODO: include inward/outward directions, numberOfRepetitions and numberOfIterations options from additive and substractive processes.

    ----------
    originalStream : Stream
        The original stream to process
    direction : str
        Determines the direction of the substractive process:
            "forward" starts scanning from the beginning of the stream
            "backward" starts scanning from the end of the stream
    progressionType : str
        Determines the type of mathematical progression:
            "linear", "primes" or "fibonacci"
    windowSize : int
        Determines the size of the "window" that is scanning the original stream.

    Returns
    -------
    newStream : Stream
        The stream created by the additive process.

    """

    newStream = music21.stream.Stream()
    originalNotes = originalStream.flat.notes
    originalLength = len(originalNotes)
    progressionList = _getProgressionList(progressionType)
    progressionIndex = 0
    startPosition = 0
    endPosition = 0
    currentPosition = 0

    while currentPosition + windowSize < originalLength:
        currentStream = music21.stream.Stream()
        if direction == "forward":
            startPosition = currentPosition
            endPosition = currentPosition + windowSize
        elif direction == "backward":
            startPosition = originalLength - (currentPosition + windowSize)
            endPosition = originalLength - currentPosition
        if startPosition < 0:
            startPosition = 0
        if endPosition > originalLength:
            endPosition = originalLength
        for i in range(startPosition, endPosition):
            currentStream.append(deepcopy(originalNotes[i]))
        newStream.append(currentStream)
        progressionIndex += 1
        currentPosition = progressionList(progressionIndex)

    return newStream


def _getProgressionList(progressionType):
    linearList = []
    for i in range(1, 200):
        linearList.append(i)

    primesList = [
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
        101,
        103,
        107,
        109,
        113,
        127,
        131,
        137,
        139,
        149,
        151,
        157,
        163,
        167,
        173,
        179,
        181,
        191,
        193,
        197,
        199,
    ]

    fibonacciList = [
        1,
        1,
        2,
        3,
        5,
        8,
        13,
        21,
        34,
        55,
        89,
        144,
        233,
        377,
        610,
        987,
        1597,
        2584,
        4181,
        6765,
        10946,
        17711,
        28657,
        46368,
        75025,
        121393,
        196418,
        317811,
    ]

    progressionList = []
    if progressionType == "linear":
        progressionList = linearList
    elif progressionType == "primes":
        progressionList = primesList
    elif progressionType == "fibonacci":
        progressionList = fibonacciList

    return progressionList
