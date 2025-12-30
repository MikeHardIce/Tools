
# File Search

A little tool to search for files based on a regex pattern. Optional only search for files in folders that match a specific folder pattern.

`poetry run main ~ "^.*\.toml$"`

Currently only with BFS (Breadth First Search) and DFS (Depth First Search). See

`poetry run main --help`

TODO:
* tests
* read and prep for pipx git installation or similar easy execution
* potentially running concurrently
