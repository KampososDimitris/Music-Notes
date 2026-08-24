notes = [
    'A',
    'A#',
    'B',
    'C',
    'C#',
    'D',
    'D#',
    'E',
    'F',
    'F#',
    'G',
    'G#',
]

chord_variants = {
    'Major': {
        'notation': '',
        'formula': [0, 4, 7],
        'labels': ['1', '3', '5'],
        'notes': []
    },
    'Minor': {
        'notation': 'm',
        'formula': [0, 3, 7],
        'labels': ['1', 'b3', '5'],
        'notes': []
    },
    'Diminished': {
        'notation': 'dim',
        'formula': [0, 3, 6],
        'labels': ['1', 'b3', 'b5'],
        'notes': []
    },
    'Augmented': {
        'notation': 'aug',
        'formula': [0, 4, 8],
        'labels': ['1', '3', '#5'],
        'notes': []
    },
    'Suspended 2nd': {
        'notation': 'sus2',
        'formula': [0, 2, 7],
        'labels': ['1', '2', '5'],
        'notes': []
    },
    'Suspended 4th': {
        'notation': 'sus4/sus',
        'formula': [0, 5, 7],
        'labels': ['1', '4', '5'],
        'notes': []
    },
    'Dominant 7th': {
        'notation': '7',
        'formula': [0, 4, 7, 10],
        'labels': ['1', '3', '5', 'b7'],
        'notes': []
    },
    'Major 7th': {
        'notation': 'maj7',
        'formula': [0, 4, 7, 11],
        'labels': ['1', '3', '5', '7'],
        'notes': []
    },
    'Minor 7th': {
        'notation': 'm7',
        'formula': [0, 3, 7, 10],
        'labels': ['1', 'b3', '5', 'b7'],
        'notes': []
    },
    'Half-Diminished 7th': {
        'notation': 'm7b5',
        'formula': [0, 3, 6, 10],
        'labels': ['1', 'b3', 'b5', 'b7'],
        'notes': []
    },
    'Diminished 7th': {
        'notation': 'dim7',
        'formula': [0, 3, 6, 9],
        'labels': ['1', 'b3', 'b5', 'bb7'],
        'notes': []
    },
    'Major 6th': {
        'notation': '6',
        'formula': [0, 4, 7, 9],
        'labels': ['1', '3', '5', '6'],
        'notes': []
    },
    'Minor 6th': {
        'notation': 'm6',
        'formula': [0, 3, 7, 9],
        'labels': ['1', 'b3', '5', '6'],
        'notes': []
    },
}

N_OF_INTERVALS = 12

def calculate_chord_notes(root, formula):
    if root not in notes:
        return []

    chord_notes = []
    root_idx = notes.index(root)
    
    for intervals in formula:
        note_idx = (root_idx + intervals) % N_OF_INTERVALS
        chord_notes.append(notes[note_idx])

    return chord_notes
