
import click
import os

from typing import List

from file_search.search import Search, BreadthFirstSearch, DepthFirstSearch

def print_partial_results(elements: List[str]):
    if elements is not None:
        for element in elements:
            print(element)

@click.command()
@click.option("--algo", default="bfs", help="bfs (breadth first search), dfs (depth first search)")
@click.option("--folder-pattern", default=".*", help="regex pattern for folders")
@click.option("--show-folders", is_flag = True, default=False, help="True - show folders in output, False to disable")
@click.option("-v","--verbose", is_flag = True, default=False)
@click.option("--limit", default="-1", help="Limit the results and stop after reaching the limit")
@click.argument("folder")
@click.argument("pattern")
def main(algo: str, folder_pattern: str, show_folders: bool, verbose: bool
         , limit: int, folder: str, pattern: str):
    
    limit = int(limit)

    if folder.strip() == "." or folder.strip() == "":
        folder = os.getcwd()

    if len(pattern.strip(" ")) == 0:
        pattern = ".*"

    search: Search = None

    match algo:
        case "dfs":
            search = DepthFirstSearch(print_partial_results)
        case _:
            search = BreadthFirstSearch(print_partial_results)

    search.show_folder = show_folders
    search.verbose = verbose
    search.go(folder, pattern, folder_pattern, limit)

if __name__ == "__main__":
    main()