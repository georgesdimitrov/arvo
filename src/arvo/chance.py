"""Module for creating indeterminate processes."""

import copy
import enum
import random
import statistics
from typing import Optional, Union, Sequence
from dataclasses import dataclass

from music21 import stream

from arvo import tools
from arvo import core

__all__ = [
    "Weighting",
    "randomize",
]


class Weighting(enum.Enum):
    """
    Specifies how the random selection is weighted.

    Attributes:
        AVERAGE: Weights selection toward middle elements by averaging multiple rolls.
        MINIMUM: Weights selection toward starting elements by taking the lowest
        result from multiple rolls.
        MAXIMUM: Weights selection toward ending elements by taking the highest
        result from multiple rolls.
    """

    AVERAGE = 1
    MINIMUM = 2
    MAXIMUM = 3


@dataclass
class Options:
    """
    Configuration for the randomization process.

    Attributes:
        length: Length of the generated sequence. Defaults to the input sequence's
        length if not specified.
        weighting: Weighting mode applied to random selection. Defaults to uniform
        distribution if None.
        rolls: Number of rolls to perform per selection for weighted distributions.
        Higher numbers produce stronger weighting effects.
    """

    length: Optional[int] = None
    weighting: Optional[Weighting] = None
    rolls: int = 1


def randomize(
    sequence: Sequence | stream.Stream,
    options: Optional[Options] = None,
) -> Sequence | stream.Stream:
    """
        Generates a randomized sequence based on the provided sequence and options.

        If a music21 Stream is provided, it is flattened and its note, chord,
        and rest elements are randomized.

        Args:
            sequence: Input sequence or music21 Stream to randomize.
            options: Optional settings controlling sequence length and weighting.

        Returns:
            A randomized sequence or Stream, matching the type of the input.
        """
    # Initialize function variables.
    sequence = core.ArvoSequence(sequence)
    options = options or Options()

    length = options.length or len(sequence)
    rolls = max(options.rolls, 1)  # Ensure at least one roll
    post_sequence = []

    for _ in range(length):
        if options.weighting == Weighting.AVERAGE:
            indexes = [random.randrange(len(sequence)) for _ in range(rolls)]
            random_index = round(statistics.mean(indexes))
        elif options.weighting == Weighting.MINIMUM:
            indexes = [random.randrange(len(sequence)) for _ in range(rolls)]
            random_index = min(indexes)
        elif options.weighting == Weighting.MAXIMUM:
            indexes = [random.randrange(len(sequence)) for _ in range(rolls)]
            random_index = max(indexes)
        else:  # Uniform random choice
            random_index = random.randrange(len(sequence))

        post_sequence.append(copy.deepcopy(sequence[random_index]))

    if sequence.is_stream:
        return tools.notes_to_stream(post_sequence)

    return post_sequence
