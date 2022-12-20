from typing import BinaryIO, Dict, List, Tuple, Optional
import pickle, os, shutil, tempfile

from Infinitum.Core.Storage.MBT import MasterBootTable as MBT, MBT_size
from Infinitum.Core.Storage.MFT import MasterFileTable as MFT, MFT_size
from Infinitum.Core.Storage.Metadata import Metadata

RESERVED_SPACE = MBT_size + MFT_size

class FileManager:
    def __init__(self, drive_path: str) -> None:
        self.drive, self.working_dir = open(drive_path, 'rb'), tempfile.TemporaryDirectory()
        self.MBT, self.MFT = MBT.load(self.drive), MFT.load(self.drive)



    def _(): pass
    
    @staticmethod
    def del_folder(folder_path: str): shutil.rmtree(folder_path)
    
    @staticmethod
    def del_file(file_path: str): shutil.rmtree(file_path)

    
