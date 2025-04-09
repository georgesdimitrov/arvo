import random

import pytest
from music21 import converter
from music21 import note
from arvo import generative


@pytest.fixture
def l_system_note_rules():
    return [
        generative.LSystemRule(note.Note("C3"), [note.Note("C3"), note.Note("D3")]),
        generative.LSystemRule(note.Note("D3"), [note.Note("E3"), note.Note("D3")]),
    ]


@pytest.fixture
def l_system_starting_sequence():
    return converter.parse("tinyNotation: C")

@pytest.fixture
def convert_table_to_probabilities():
    def convert(table):
        result_table = []
        for index_1 in range(len(table[0])):
            result_table.append([])
            for index_2 in range(len(table[0])):
                result_table[index_1].append(table[index_1][index_2] / sum(table[index_1]))

        return result_table

    return convert

@pytest.fixture
def flatten_table():
    def flatten(xss):
        return [x for xs in xss for x in xs]

    return flatten

def test_l_system(l_system_starting_sequence, l_system_note_rules):
    result = generative.create_l_system(l_system_starting_sequence,
                                        l_system_note_rules, generative.LSystemOptions(
                                        iterations_stop=3))
    intended_result = converter.parse(
        """
        tinyNotation: 
        C 
        C D
        C D E D
        C D E D E E D
        """
    )

    assert list(result.flatten().notes) == list(intended_result.flatten().notes)

@pytest.fixture
def markov_chain_probabilities_table():
    return [[0, 50, 50], [75, 0, 25], [75, 25, 0]]


def test_markov_chain_notes(markov_chain_probabilities_table, convert_table_to_probabilities, flatten_table):
    notes = [note.Note("C3"), note.Note("D3"), note.Note("E3")]
    random.seed(0)

    result = generative.create_markov_chain(notes, markov_chain_probabilities_table, 10000)
    result_count = []

    for index1 in range(len(notes)):
        note1 = notes[index1]
        result_count.append([])
        for index2 in range(len(notes)):
            note2 = notes[index2]
            count = 0
            # Iterate through the list until the second last element
            for i in range(len(result) - 1):
                # Check if the current element is x and the next one is y
                if result[i] == note1 and result[i + 1] == note2:
                    count += 1

            result_count[index1].append(count)

    expected_probabilities = flatten_table(convert_table_to_probabilities(markov_chain_probabilities_table))
    result_probabilities = flatten_table(convert_table_to_probabilities(result_count))

    assert result_probabilities == pytest.approx(expected_probabilities, rel=0.02)
