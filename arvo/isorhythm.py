import music21
import tools
from copy import deepcopy


def createIsorhythm(color_stream, talea_stream, sequence_length=0):
    color_list = []
    for element in color_stream.flat.notes:
        color_list.append(element)

    talea_list = []
    for element in talea_stream.flat.notes:
        talea_list.append(element.duration)

    color_counter = 0
    talea_counter = 0
    new_stream = music21.stream.Stream()
    autoStop = False

    if sequence_length == 0:
        autoStop = True
        sequence_length = 10000

    # Loop
    for _ in range(sequence_length):
        current_element = deepcopy(color_list[color_counter])
        current_element.duration = talea_list[talea_counter]
        new_stream.append(current_element)
        color_counter += 1
        if color_counter == len(color_list):
            color_counter = 0
        talea_counter += 1
        if talea_counter == len(talea_list):
            talea_counter = 0
        if autoStop == True and color_counter == 0 and talea_counter == 0:
            break

    return new_stream
