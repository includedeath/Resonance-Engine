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
    detected_set=set(notes)

    best_match="Unknown"
    best_score=0

    for chord_notes,chord_name in chords.items():
        match_count=len(chord_notes.intersection(detected_set))
        score=match_count/len(chord_notes)
        if score>best_score:
            best_score=score
            best_match=chord_name

    if best_score>=0.6:
        return best_match,round(best_score,2)
    else:
        return "Unknown",round(best_score,2)