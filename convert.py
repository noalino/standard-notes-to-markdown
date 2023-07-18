from datetime import datetime
import json
import os
import sys
import time


def get_args():
    """
    Check & return arguments passed to the script
    """
    # Should at least include the path to the standard notes file
    if len(sys.argv) < 2:
        raise Exception('Invalid number of required arguments.')

    # Sanity check standard notes file path
    stdnotes_file_path = sys.argv[1]
    if not os.path.isfile(stdnotes_file_path):
        raise Exception('Invalid path to standard notes file.')

    # Sanity check export path
    try:
        export_path = sys.argv[2]
    except IndexError:
        export_path = os.path.join(os.getcwd(), 'Notes')

    if os.path.exists(export_path):
        raise Exception(
            f'Exported path "{export_path}" already exists, '
            f'please remove or update the path. '
            f'We don\'t want to overwrite anything.')

    return stdnotes_file_path, export_path


def is_valid_note(note):
    """
    Filter the notes out
    Do not include trashed, archived or duplicated ones
    """
    return (
        not note.get('trashed') and
        not note.get('archived') and
        not note.get('duplicate_of')
    )


def get_note(item):
    """
    Define note with extracted info from standard notes file
    """
    return {
        'uuid':                 item.get('uuid'),
        'title':                item.get('content').get('title'),
        'text':                 item.get('content').get('text'),
        'updated_at_timestamp': item.get('updated_at_timestamp'),
        'duplicate_of':         item.get('duplicate_of', None),
        'trashed':              item.get('content').get('trashed', False),
        'archived':             item.get('content')
                                    .get('appData')
                                    .get('org.standardnotes.sn')
                                    .get('archived', False),
        'tags':                 [],
    }


def get_notes(json_file):
    """
    Get notes content from the standard notes file
    """
    notes = []
    items = json_file.get('items')
    # Sort list to append all notes before assigning them tags
    items.sort(key=lambda item: item.get('content_type'))

    for item in items:
        # Handle note content & metadata
        if item.get('content_type') == 'Note':
            note = get_note(item)
            if not is_valid_note(note):
                continue

            notes.append(note)

        # Handle tags
        refs = item.get('content').get('references')
        if item.get('content_type') == 'Tag' and len(refs) > 0:
            for ref in refs:
                # Look for valid refs only
                if (
                    not ref.get('content_type') == 'Note' or
                    not ref.get('uuid')
                ):
                    continue

                found_note = next(filter(
                    lambda note: note.get('uuid') == ref.get('uuid'),
                    notes
                ), None)
                # Link tag to note
                if found_note:
                    found_note.get('tags').append(
                        item.get('content').get('title'))

    return notes


def get_note_filename(name):
    """
    Sanitize note filename
    """
    remove_punctuation_map = dict((ord(char), None) for char in r'\/*?:"<>|')
    return name.translate(remove_punctuation_map)


def get_note_times(note):
    """
    Get note access and modified times
    Both are set to the last udpated time
    """
    updated_datetime = datetime.fromtimestamp(
        note.get('updated_at_timestamp') // 1e6)
    updated_time = time.mktime(updated_datetime.timetuple())
    return (updated_time, updated_time)


def get_note_content(note):
    """
    Create note content with yaml front matter
    """
    content = ['---']
    content.append(f'title: {note.get("title")}')
    if len(note.get('tags')) > 0:
        tags = '\n'.join([f'  - {tag}' for tag in note.get('tags')])
        content.append(f'tags:\n{tags}')
    content.append('---')
    content.append(note.get('text'))
    return '\n'.join(content)


def get_note_filepath(dir_path, note):
    """
    Handle filename conflicts by appending a uuid to duplicate ones
    """
    filename = get_note_filename(note.get("title"))
    filepath = os.path.join(dir_path, f'{filename}.md')

    if os.path.exists(filepath):
        filepath = os.path.join(
            dir_path,
            f'{filename}-{note.get("uuid").split("-")[0]}.md')

    return filepath


def write_notes(notes, export_path):
    """
    Save notes in the export path
    """
    # No need to raise error if dir exists, as we checked it earlier
    os.makedirs(export_path, exist_ok=True)

    for note in notes:
        filepath = get_note_filepath(export_path, note)

        with open(filepath, 'w') as note_file:
            note_file.write(get_note_content(note))

        times = get_note_times(note)
        # Set file access and modified times
        os.utime(filepath, times)


def main():
    stdnotes_file_path, export_path = get_args()

    with open(stdnotes_file_path) as stdnotes_file:
        stdnotes_json = json.load(stdnotes_file)
        notes = get_notes(stdnotes_json)

    write_notes(notes, export_path)

    print(f'{len(notes)} notes have been successfully exported!')


if __name__ == "__main__":
    main()
