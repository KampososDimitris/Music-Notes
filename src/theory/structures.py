import re

natural_notes = [
    'C',
    'D',
    'E',
    'F',
    'G',
    'A',
    'B',
]


roots = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']


chord_variants = {
    'Major': {
        'notation': '',
        'formula': [0, 4, 7],
        'labels': ['1', '3', '5']
    },
    'Minor': {
        'notation': 'm',
        'formula': [0, 3, 7],
        'labels': ['1', 'b3', '5']
    },
    'Diminished': {
        'notation': 'dim',
        'formula': [0, 3, 6],
        'labels': ['1', 'b3', 'b5']
    },
    'Augmented': {
        'notation': 'aug',
        'formula': [0, 4, 8],
        'labels': ['1', '3', '#5']
    },
    'Suspended 2nd': {
        'notation': 'sus2',
        'formula': [0, 2, 7],
        'labels': ['1', '2', '5']
    },
    'Suspended 4th': {
        'notation': 'sus4/sus',
        'formula': [0, 5, 7],
        'labels': ['1', '4', '5']
    },
    'Dominant 7th': {
        'notation': '7',
        'formula': [0, 4, 7, 10],
        'labels': ['1', '3', '5', 'b7']
    },
    'Major 7th': {
        'notation': 'maj7',
        'formula': [0, 4, 7, 11],
        'labels': ['1', '3', '5', '7']
    },
    'Minor 7th': {
        'notation': 'm7',
        'formula': [0, 3, 7, 10],
        'labels': ['1', 'b3', '5', 'b7']
    },
    'Half-Diminished 7th': {
        'notation': 'm7b5',
        'formula': [0, 3, 6, 10],
        'labels': ['1', 'b3', 'b5', 'b7']
    },
    'Diminished 7th': {
        'notation': 'dim7',
        'formula': [0, 3, 6, 9],
        'labels': ['1', 'b3', 'b5', 'bb7']
    },
    'Major 6th': {
        'notation': '6',
        'formula': [0, 4, 7, 9],
        'labels': ['1', '3', '5', '6']
    },
    'Minor 6th': {
        'notation': 'm6',
        'formula': [0, 3, 7, 9],
        'labels': ['1', 'b3', '5', '6']
    },
}


scales = {
    'Major': {
        'notation': 'Ionian',
        'formula': [0, 2, 4, 5, 7, 9, 11],
        'labels': ['1', '2', '3', '4', '5', '6', '7']
    },
    'Natural Minor': {
        'notation': 'Minor/Aeolian',
        'formula': [0, 2, 3, 5, 7, 8, 10],
        'labels': ['1', '2', 'b3', '4', '5', 'b6', 'b7']
    },
    'Harmonic Minor': {
        'notation': '',
        'formula': [0, 2, 3, 5, 7, 8, 11],
        'labels': ['1', '2', 'b3', '4', '5', 'b6', '7']
    },
    'Melodic Minor': {
        'notation': '',
        'formula': [0, 2, 3, 5, 7, 9, 11],
        'labels': ['1', '2', 'b3', '4', '5', '6', '7']
    },
    'Major Pentatonic': {
        'notation': '',
        'formula': [0, 2, 4, 7, 9],
        'labels': ['1', '2', '3', '5', '6']
    },
    'Minor Pentatonic': {
        'notation': '',
        'formula': [0, 3, 5, 7, 10],
        'labels': ['1', 'b3', '4', '5', 'b7']
    },
    'Blues': {
        'notation': 'Minor Blues',
        'formula': [0, 3, 5, 6, 7, 10],
        'labels': ['1', 'b3', '4', 'b5', '5', 'b7']
    },
    'Dorian': {
        'notation': '',
        'formula': [0, 2, 3, 5, 7, 9, 10],
        'labels': ['1', '2', 'b3', '4', '5', '6', 'b7']
    },
    'Phrygian': {
        'notation': '',
        'formula': [0, 1, 3, 5, 7, 8, 10],
        'labels': ['1', 'b2', 'b3', '4', '5', 'b6', 'b7']
    },
    'Lydian': {
        'notation': '',
        'formula': [0, 2, 4, 6, 7, 9, 11],
        'labels': ['1', '2', '3', '#4', '5', '6', '7']
    },
    'Mixolydian': {
        'notation': '',
        'formula': [0, 2, 4, 5, 7, 9, 10],
        'labels': ['1', '2', '3', '4', '5', '6', 'b7']
    },
    'Locrian': {
        'notation': '',
        'formula': [0, 1, 3, 5, 6, 8, 10],
        'labels': ['1', 'b2', 'b3', '4', 'b5', 'b6', 'b7']
    },
}


N_OF_NATURAL_NOTES = 7


def calculate_structure_notes(root, structure):
    if structure in list(chord_variants.keys()):
        structure = chord_variants[structure]
    elif structure in list(scales.keys()):
        structure = scales[structure]
    else:
        raise Exception(f'Invalid structure: {structure}')

    if not check_valid(root):
        raise Exception(f'Invalid note: {root}')

    degrees = calculate_degrees(root, structure)
    notes_list = []
    
    for idx, semitones in enumerate(structure['formula']):
        notes_list.append(next_note(root, degrees[idx], semitones))

    return notes_list


def next_note(root, degree, semitones):
    note = root

    for _ in range(semitones):
        note = increment_interval(note)

    if not corresponds_to_degree(note, degree):
        note = adjust_note(note, degree)

    return note


# Move to the next note, adding one interval.
def increment_interval(note):
    incremented = note

    if is_e_or_b(incremented):
        if is_flat(incremented):
            return remove_flat(incremented)
        else:
            return move_to_next_natural(incremented)
    elif is_flat(incremented):
        return remove_flat(incremented)
    elif is_natural(incremented):
        return add_sharp(incremented)
    else:
        return move_to_next_natural(incremented)


def is_e_or_b(note):
    if re.fullmatch(r"(?:E|B)?", note):
        return True
    return False


def is_flat(note):
    if re.fullmatch(r"[A-G]b", note):
        return True
    return False


def is_natural(note):
    if re.fullmatch(r"[A-G]", note):
        return True
    return False


def add_sharp(note):
    return f'{note}#'


def remove_flat(note):
    return note[0]


def move_to_next_natural(note):
    natural_note_idx = natural_notes.index(note[0])
    return natural_notes[(natural_note_idx + 1) % N_OF_NATURAL_NOTES]


def corresponds_to_degree(note, degree):
    return note[0] == degree


# Adjust the note to be in the degree it needs to be, to match the scale.
def adjust_note(note, degree):
    notes_natural_idx = natural_notes.index(note[0])
    next_two_naturals = [natural_notes[(notes_natural_idx + i) % N_OF_NATURAL_NOTES] for i in range(1,3)]

    if degree not in next_two_naturals:
        accidental = '#'
        incremented = degree
        intervals = 0
        
        while incremented != note:
            incremented = increment_interval(incremented)
            intervals += 1
    else:
        accidental = 'b'
        incremented = note
        intervals = 0

        while incremented != degree:
            incremented = increment_interval(incremented)
            intervals += 1

    return f'{degree}{intervals*accidental}'


def is_seven_note_structure(structure):
    return not (len(structure['labels']) < 7)


def calculate_degrees(root, structure):
    root_idx = natural_notes.index(root[0])
    
    if is_seven_note_structure(structure):
        degrees = [
            natural_notes[(root_idx + i) % N_OF_NATURAL_NOTES] for i in range(7)
        ]
    else:
        degrees = []

        for label in structure['labels']:
            degree = int(label) if len(label) == 1 else int(label[-1])
            degree_note_idx = (root_idx + (degree - 1)) % N_OF_NATURAL_NOTES
            degrees.append(natural_notes[degree_note_idx])

    return degrees


def check_valid(note):
    if re.fullmatch(r"[A-G](?:#|b)?", note):
        return True
    return False


# def write_output():
#     s = ''
#     for root in roots:
#         for chord_name in chord_variants.keys():
#             if not is_seven_note_structure(chord_variants[chord_name]):
#                 s += f'Root: {root}\n'
#                 s += f'Chord: {chord_name}\n'
#                 s += f'Notes: {' '.join(calculate_structure_notes(root, chord_name))}\n'
#                 s += f"{'-'*50}\n"
#     return s

# import os
# filepath = os.path.join(os.getcwd(), 'results.txt')

# with open(filepath, 'w') as f:
#     f.write(write_output())

print(list(chord_variants.keys()))