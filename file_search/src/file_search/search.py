import os
import re

from os import listdir
from typing import List, Set
from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections.abc import Callable
from collections import deque

@dataclass
class Result:
    files: List[str]
    folders: List[str]

class Search(ABC):

    show_folder: bool = False
    verbose: bool = False

    def __init__(self, fun_step_results: Callable[[List[str]], None]):
        super().__init__()
        self._fun_step_results = fun_step_results

    def go(self, folder: str, file_pattern: str, folder_pattern: str = "") -> Set[str]:
        """
        Search for files in a given folder
        
        :param folder: The folder to start the search
        :type folder: str
        :param pattern: The file name pattern
        :type pattern: str
        :param folder_pattern: If a folder pattern is given, then only start the file search in folders matching the given pattern
        :type folder_pattern: str
        :return: A list of file paths. Contains folder paths if a folder pattern was given without using a file pattern.
        :rtype: List[str]
        """
        files: Set[str] = set()

        result = self.step(folder, file_pattern, folder_pattern)

        folders = deque(result.folders if result.folders else []) 
        files.union(result.files) if result.files else None
        self.notify(result)        

        while len(folders) > 0:
            result = self.step(self.pick_item(folders), file_pattern, folder_pattern)

            folders.extend(result.folders)
            files.union(result.files)
            self.notify(result)

        return files

    @abstractmethod
    def pick_item(self, q: deque) -> str:
        return ""

    def step(self, folder, file_pattern, folder_pattern = "") -> Result:

        elements = self.get_files(folder)

        files = Search.get_files_matching(elements, file_pattern)

        folders = Search.get_dirs_matching(elements, folder_pattern)

        return Result(files, folders)
    
    def notify(self, result: Result):
        if callable(self._fun_step_results):
            if self.show_folder == True:
                self._fun_step_results(result.folders)

            self._fun_step_results(result.files)

    def get_files(self, folder:str) -> List[str]:
        """Returns file and directory names of all elements in the current folder"""

        if os.path.exists(folder) and os.path.isdir(folder):
            try:
                return list(map(lambda p: os.path.join(folder ,p) ,listdir(folder)))
            except:
                #for now just a simple print
                if self.verbose:
                    print(f"Cannot access folder '{folder}'")
        return []

    def get_files_matching(files: List[str], pattern: str) -> List[str]:
        """Returns only the file paths that match the given pattern"""

        return list(filter(lambda file: os.path.isfile(file) and re.match(pattern, os.path.basename(file)), files))

    def get_dirs_matching(files: List[str], pattern: str) -> List[str]:
        """Returns only the directory paths that match the given pattern"""

        return list(filter(lambda file: os.path.isdir(file) and re.match(pattern, os.path.basename(file)), files))
    
class BreadthFirstSearch(Search):
    
    def pick_item(self, q):
        return q.popleft()
        
    
class DepthFirstSearch(Search):
    
    def pick_item(self, q):
        return q.pop()