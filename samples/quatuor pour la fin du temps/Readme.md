# Olivier Messiaen - Quatuor pour la fin du temps (Liturgie de Cristal)

This example showcases the following **arvo** modules:

* **isorhythm** for creating the isorhythmic process

The piano and cello parts are included, since they are the ones that are built using an isorhythmic construction. The generated score is identical to Messiaen's manuscript until bar 24. After this, the generation does not concord, because Messiaen did not follow the mathematical process strictly at two points:

* In the piano part, in the 4th repetition of the 29 chords sequence, Messiaen omits the chord #3. The 17 durations cycle is however followed perfectly.
* In the cello part, in the 6th repetition of the 15 durations sequence, Messiaen used a quarter note for value #5 instead of an 8th note. The 5 pitches sequence is however followed perfectly.

It's an interesting question if these inconsistencies were simply mistakes or follow a hidden compositional intent.
