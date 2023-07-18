# Export Standard Notes to Markdown

This script allows [Standard Notes](https://standardnotes.com/) users to export their notes in markdown format.

I personally used it to make them compatible with [Obsidian](https://obsidian.md/).

<u>Features</u>

- Export notes to markdown with YAML front matter metadata
- Keep tags
- Handle file last modified time
- Remove trashed, archived and duplicated notes

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Python 3 installed on your system
- You have downloaded and unzipped the decrypted backup zip file from Standard Notes (please visit the [official Standard Notes website](https://standardnotes.com/help/14/how-do-i-create-and-import-backups-of-my-standard-notes-data) if you don't know how to do so)

## Usage

When you unzip the backup file, you'll find may files, but we are only interested in the first one, i.e. _Standard Notes Backup and Import File.txt_.

From the command line, you can run:

```
$ python3 convert.py <path-to-std-notes-file> <path-to-exported-dir>
```

where _\<path-to-std-notes-file>_ is the path to the file mentioned above, and _\<path-to-exported-dir>_ is the path into which the notes are exported (if the argument is not passed, it defaults to _./Notes_). **Make sure the directory does not exist.**

Example:

```
$ python3 convert.py Standard\ Notes\ Backup\ and\ Import\ File.txt ~/Exported_Standard_Notes
```

## Disclaimers

- The _Standard Notes Backup and Import File.txt_ file includes a version key. At the time of this writing, it is set to version 4. The script may work for earlier or future versions.
- I used Python 3.10 to write the script.
- I used no external libraries, so the front matter YAML formatting is done manually.
- I used the free version of Standard Notes, so the script may not run as you expect with some installed plugins.

Feel free to fork the project to adapt it to your use case.

## Thanks

This script is inspired by [this project](https://github.com/hozza/standardnotes-to-markdown-yaml-export) written in PHP.
