chords={
    frozenset(["C","E","G"]):"C Major",
    frozenset(["A","C","E"]):"A Minor",
    frozenset(["G","B","D"]):"G Major",
    frozenset(["D","F#","A"]):"D Major",
    frozenset(["E","G#","B"]):"E Major",
    frozenset(["F","A","C"]):"F Major",
    frozenset(["D","F","A"]):"D Minor",
}

def detect_chord(notes):
    detected_set=frozenset(notes)

    for chord_notes,chord_name in chords.items():
        if chord_notes.issubset(detected_set):
            return chord_name

    return "Unknown"