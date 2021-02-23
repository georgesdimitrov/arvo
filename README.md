# arvo
A python library for procedural music composition, based on the music21 (https://github.com/cuthbertLab/music21) framework, created and maintained by Dr. Georges Dimitrov, composition professor at Concordia University (https://www.concordia.ca/finearts/music.html).

The library is currently in alpha development state.

### Modules
This library currently contains the following core modules:

* **isorhythm**: Functions for generating isorhythmic constructions from pitch and rhythm sequences.
* **minimalism**: Functions for generating Philip Glass/Steve Reich-inspired additive and substractive processes.
* **tintinnabuli**: Functions for generating Arvo Pärt-inspired tintinnabuli.
* **transformations**: Functions for doing scalar transpositions and inversions, retrogrades...

It also contains the following helper modules:
* **scales**: Extension of music21 scales system with some common/useful scales.
* **sequences**: Useful integer sequences for music composition, like primes, fibonacci, kolakoski...
* **tools**: Convenient helper functions for quickly manipulating and combining music21 elements.

### Samples
The samples directory contains sample pieces created with the music21 and arvo, including recreations of some famous pieces of the repertoire. Each subfolder contains a python file with the code, a music xml output, and a pdf of the piece as rendered in MuseScore.

It currently contains the following samples:

* **Olivier Messiaen - *Quatuor pour la fin du temps*** (isorhythm)
* **Arvo Pärt - *Fratres* (minimalism, transformations**, tintinnabuli)
* **Frederic Rzewski - *Coming Together*** (minimalism, transformations)
