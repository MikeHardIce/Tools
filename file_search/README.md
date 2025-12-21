
# File Search

A little tool to search for files based on a regex pattern. Optional only search for files in folders that match a specific folder pattern.

`poetry run main ~ "^.*\.toml$"`

Currently only with BFS (Breadth First Search), DFS will follow. See

`poetry run main --help`

TODO:
* DFS
* Cancel after n results
* Folder pattern not to prevent search of child folders etc. To only restrict if to files (not folders) within a folder matching the
  folder pattern.
* read and prep for pipx git installation
* potentially running concurrently
