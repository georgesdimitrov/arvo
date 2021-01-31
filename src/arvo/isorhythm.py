import music21
import tools
from copy import deepcopy
from typing import Optional


def create_isorhythm(
    color_stream: music21.stream.Stream,
    talea_stream: music21.stream.Stream,
    length: Optional[int] = None,
) -> music21.stream.Stream:

    """Creates an isorythmic construction from color and talea streams.

    Args:
        color_stream: The stream containing pitch information.
        talea_stream: The stream containing rhythm information.
        length: Optional; The length of the resulting stream, expressed in isorhythmic elements. By default, the process
          continues until the cycle is completed. For example, provided a color of 5 pitches and a talea of 7 rhythms,
          this function will, by default, return an isorhythm of 35 elements.

    Returns:
        The new stream created by the isorhythmic process.
    """
    color_list = []
    for element in color_stream.flat.notes:
        color_list.append(element)

    talea_list = []
    for element in talea_stream.flat.notes:
        talea_list.append(element.duration)

    color_counter = 0
    talea_counter = 0
    new_stream = music21.stream.Stream()
    auto_stop = False

    if length == 0:
        auto_stop = True
        length = 10000

    # Loop
    for _ in range(length):
        current_element = deepcopy(color_list[color_counter])
        current_element.duration = talea_list[talea_counter]
        new_stream.append(current_element)
        color_counter += 1
        if color_counter == len(color_list):
            color_counter = 0
        talea_counter += 1
        if talea_counter == len(talea_list):
            talea_counter = 0
        if auto_stop is True and color_counter == 0 and talea_counter == 0:
            break

    return new_stream
