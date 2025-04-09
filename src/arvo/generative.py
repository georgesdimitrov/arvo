"""
Module providing functions and classes for generative musical processes.

Currently supports L-systems and Markov chain-based music generation.
"""

import copy
import random
import numbers
from typing import Optional, Union, Sequence, List, Any
from dataclasses import dataclass
from music21 import stream

from arvo import core
from arvo import tools

@dataclass
class LSystemRule:
    """
    Represents a substitution rule used in an L-system generative process.

    Attributes:
        target: The target sequence that will be replaced.
        replacement: The sequence used as a replacement when the target is matched.
    """
    target: Any | core.ArvoSequence
    replacement: Any | core.ArvoSequence

    def __init__(self, target, replacement):
        self.target = core.ArvoSequence(target)
        self.replacement = core.ArvoSequence(replacement)


@dataclass
class LSystemOptions:
    """
    Configuration options for the L-system generative process.

    Attributes:
        repetitions: Number of repetitions per iteration. Can be a single integer
        (applies to all iterations) or a sequence specifying repetitions per iteration.
        iterations_start: Starting iteration index for generating the output sequence.
        iterations_stop: Ending iteration index for generating the output sequence.
    """
    repetitions: Optional[int | Sequence[int]] = 1
    iterations_start: Optional[int] = 0
    iterations_stop: Optional[int] = 1


def create_l_system(
    sequence: Sequence | stream.Stream,
    substitution_rules: List[LSystemRule],
    options: Optional[LSystemOptions]
) -> Sequence | stream.Stream:
    """
    Generates a sequence using an L-system substitution process.

    Args:
        sequence: The initial sequence (or stream) of elements.
        substitution_rules: List of LSystemRule objects defining substitution targets
        and replacements.
        options: Configuration options for the L-system generation.

    Returns:
        A new sequence or music21 stream generated through the L-system rules.
    """

    # Create elements list
    sequence = core.ArvoSequence(sequence)

    # Check repetitions type and initialize repetitions sequence.
    if isinstance(options.repetitions, int):
        repetitions_sequence = [options.repetitions]
    else:
        repetitions_sequence = options.repetitions
    repetitions_index = 0

    # Initialize function variables.
    l_system_sequences = [sequence]
    post_sequence = []

    for iteration_index in range(1, options.iterations_stop + 1):
        current_sequence = []
        for index in range(0, len(l_system_sequences[iteration_index - 1])):
            matched = False
            for rule in substitution_rules:
                rule_len = len(rule.target)
                target = core.ArvoSequence(l_system_sequences[iteration_index - 1][
                            index:index+rule_len])
                if not matched and target == rule.target:
                    current_sequence.extend(
                        copy.deepcopy(rule.replacement)
                    )
                    index += rule_len - 1
                    matched = True
            if not matched:
                current_sequence.append(copy.deepcopy(l_system_sequences[
                                                          iteration_index - 1][index]))
        l_system_sequences.append(current_sequence)

    for iteration_index in range(options.iterations_start, options.iterations_stop + 1):
        for _ in range(repetitions_sequence[repetitions_index]):
            post_sequence.extend(l_system_sequences[iteration_index])

        # Increment step and repetition indexes, looping if the end of the sequence is reached.
        repetitions_index += 1
        if repetitions_index > len(repetitions_sequence) - 1:
            repetitions_index = 0

    if sequence.is_stream:
        return tools.notes_to_stream(post_sequence)
    else:
        return post_sequence


def create_markov_chain(
    elements: Sequence[core.ArvoElement],
    probabilities_table: List[List[numbers.Number,]],
    length: int,
    starting_element_index: Optional[int] = 0,
) -> Sequence[core.ArvoElement]:
    """ Creates a sequence using a Markov chain process

    """
    # Initialize function variables.
    if starting_element_index < 0:
        starting_element_index = 0
    if starting_element_index >= len(elements):
        starting_element_index = len(elements) - 1
    current_element_index = starting_element_index
    post_sequence = [elements[current_element_index]]

    for i in range(0, length):
        current_element_index = _get_next_markov_element(
            probabilities_table, current_element_index
        )
        post_sequence.append(elements[current_element_index])

    return post_sequence


def _get_next_markov_element(probability_table, current_element_index):
    return random.choices(range(len(probability_table[current_element_index])), weights=probability_table[current_element_index])[0]
