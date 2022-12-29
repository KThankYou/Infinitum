from typing import List
from Infinitum.Core.Storage.FileManager import FileManager

import re


"""
# <comment>
command -> result | None
[optional] # otherwise implies if optional is not given
-flags

All commands throw an error if failed, otherwise returns None or result

Commands:
    echo "<string>" -> string # Must include \n at the end of string for newline
    cd "<directory>" -> Changes cwd to directory, 
    cwd -> "<cwd>"
    mkfile "<file name> [path] -o" -> creates file at path otherwise cwd, -o => overwrite if exists # throws error if file exists without -o
    rmfile "<file name> [path] " -> deletes file at path otherwise cwd
    mkdir "<directory name>" -> make directory in cwd
    rmdir "<directory name>" -> remove directory in cwd
    exists "<file name> [path]" -> returns True if file exists at path otherwise cwd
    flush [-mbt|-mft] -> Flush depending on flag # If nothing is given do nothing, mft flushes data too
    shutdown -> Shut down device, flushes all to drive

"""

pattern = r'\s*([^\s]+|"[^"]+"|\'[^\']+\')'
valid_commands = ('echo', 'cd', 'cwd',
                'mkfile', 'rmfile', 'mkdir', 'rmdir', 
                'exists', 'flush', 'shutdown')

P = re.compile(pattern)

class OS:
    def __init__(self, FM: FileManager) -> None:
        self.FM = FM

        fns = ( self.__echo, self.__cd, self.__cwd,
                self.__mkfile, self.__rmfile, self.__mkdir, self.__rmdir, 
                self.__exists, self.__flush, self.__shutdown)

        self.commands = dict(zip(valid_commands, fns))

    def system(self, command: str) -> None:
        tokens = P.findall(command)
        if tokens[0] not in valid_commands: raise Exception('Invalid Command')
        return self.commands[tokens[0]](*tokens[1:])

    def __echo(self, string: str) -> str:
        return string

    def __cd(self, directory: List[str]) -> None:
        if self.FM.MFT.set_cwd(directory): raise Exception('Invalid path')

    def __cwd(self) -> List[str]:
        return self.FM.MFT.get_cwd()

    def __mkfile(self, file_name: str, file_path: str = None, overwrite: bool = False) -> None:
        if self.FM.MFT.exists(file_name, file_path) and not overwrite: raise Exception('File already exists')
        self.FM.write_open(file_name, file_path, overwrite = True)
    
    def __rmfile(self, file_name: str, file_path: str):
        pass

    def __mkdir(self, file_name: str, file_path: str):
        pass

    def __exists(self, file_name: str, file_path: str):
        pass

    def __flush(self, file_name: str, file_path: str):
        pass

    def __shutdown(self, file_name: str, file_path: str):
        pass

