from Infinitum.Core.Storage.Metadata import Metadata
from typing import BinaryIO, Dict, List, Optional
from Infinitum.Core.Storage.MBT import MBT_size
from math import ceil
import pickle

MFT_size = 1*1024*1024 # 1 MB
BLOCKSIZE = 1024*1024//4 # .25 MB

def modified(function):
    def helper(*args, **kwargs):
        res = function(*args, **kwargs)
        args[0].modified = True
        return res
    return helper

class MasterFileTable:
    def __init__(self, MFT: Dict, blocks: List[int]) -> None:
        self.__table = MFT
        self.__cwd = ('root', MFT['root'])
        self.__path = ['.']
        self.modified = False
        self.blocks = blocks # 0 = empty, 1 = filled, each block is of size BLOCKSIZE

    @classmethod
    def load(cls, file: BinaryIO) -> 'MasterFileTable':
        file.seek(MBT_size, 0)
        data = file.read(MFT_size)
        try: return pickle.loads(data.lstrip(b'0'))
        except: return cls({'root':{}}, {})
    
    @classmethod
    def make_MFT(cls) -> 'MasterFileTable':
        table = {'root': 
            {'Apps': {'__files': {}}, 
            'User': {'__files': {}}, 
            '__files': {}}}
        obj = cls(table,[])
        obj.modified = True
        return obj
    
    def flush(self, file: BinaryIO) -> None:
        if self.modified:
            file.seek(MFT_size, 0)
            file.write(pickle.dumps(self).zfill(MFT_size))
            self.modified = False
        else: return 1

    #Return None if successful, 1 if fail
    @modified
    def make_dir(self, folder_name: str) -> Optional[1]:
        if folder_name in self.__cwd[1]: return 1
        self.__cwd[1][folder_name] = {'__files':{}}

    @modified
    def del_dir(self, folder_name: str) -> Optional[1]:
        if folder_name not in self.__cwd[1]: return 1
        del self.__cwd[1][folder_name]

    def cd(self, folder: str):
        if folder not in self.__cwd[1]: return 1
        self.__cwd = folder, self.__cwd[1][folder]
        self.__path.append(folder)

    def set_cwd(self, directory: str) -> Optional[1]:
        c_dir, c_path, self.__cwd = self.__cwd, self.__path, self.__table['root'] # c_ means current path
        directory = MasterFileTable.parse_path(directory)
        for i in directory:
            if self.cd(i): 
                self.__cwd, self.__path = c_dir, c_path
                return 1
        
    @property
    def get_cwd(self) -> str: return '\\'.join(self.__path)

    @modified
    def make_file(self, file_name: str, metadata: Metadata, file_path: str) -> Optional[1]:
        c_dir, c_path = self.__cwd, self.__path
        if file_path: self.set_cwd(file_path)
        folder = self.__cwd[1]['__files']
        self.__cwd, self.__path = c_dir, c_path
        if file_name in folder: return 1
        folder['__files'][file_name] = metadata
    
    def exists(self, file_name: str, file_path: str | None) -> bool:
        c_dir, c_path = self.__cwd, self.__path
        if self.set_cwd(file_path): return False
        if file_name in self.__cwd['__files']: self.__cwd, self.__path = c_dir, c_path; return True
    
    def get_file(self, file_name: str, file_path: str) -> Metadata:
        c_dir, c_path = self.__cwd, self.__path
        if self.set_cwd(file_path) or file_name not in self.__cwd[1]['__files']: 
            self.__cwd, self.__path
            raise ValueError('File/Directory does not exist')
        metadata, self.__cwd, self.__path = self.__cwd[1]['__files'][file_name], c_dir, c_path
        return metadata

    @modified
    def del_file(self, file_path: str) -> Optional[1]:
        c_dir, c_path = self.__cwd, self.__path
        *path, file = MasterFileTable.parse_path(file_path)
        self.set_cwd(path[:-1])
        folder, self.__cwd, self.__path = self.__cwd[1]['__files'], c_dir, c_path
        if file not in folder: return 1
        self.del_metadata(folder[file])
        del folder[file]

    def parse_path(self, path: str) -> List[str]:
        raw = path.split('\\')
        if raw[0] == '.': raw = self.__path[1:] + raw[1:]
        return raw

    @staticmethod
    def join(*args):
        return '\\'.join((i.rstrip('\\') for i in args))

    def make_metadata(self, size: int, name: str, binary: bool) -> Metadata:
        if size == 0: 
            i = self.blocks.index(0)
            meta = Metadata(name, i, binary, i*BLOCKSIZE)
            self.blocks[i] = meta
            return meta
        zcount = ceil(size/BLOCKSIZE) - self.blocks.count(0)
        if zcount > 0:
            self.blocks += [0]*zcount
        block_count = ceil(size/BLOCKSIZE)
        head = None
        for k, block in enumerate(self.blocks):
            if block == 0:
                head = Metadata(name, k, binary, i*BLOCKSIZE, size)
                self.blocks[k] = head
                block_count -= 1
                break
        
        node, k = head, k+1
        while block_count > 0:
            if self.blocks[k] == 0:
                self.blocks[k] = 1
                node.add_block(k, k*BLOCKSIZE)
                block_count -= 1 
                k += 1

        return head

    def del_metadata(self, metadata: Metadata) -> None:
        node = metadata.head
        while node:
            self.blocks[node.index] = 0
            node = node.next

    def consolidate(self) -> None:
        blocks, node = [], None
        for block in self.blocks:
            if isinstance(block, Metadata):
                node = block.head
                pointer = len(blocks)*BLOCKSIZE
                yield (node.pointer, pointer)
                node.index, node.pointer = len(blocks), pointer
                blocks.append(node)
                node = node.next
            if node:
                while node:
                    pointer = len(blocks)*BLOCKSIZE
                    yield (node.pointer, pointer)
                    node.index, node.pointer = len(blocks), pointer
                    blocks.append(1)
                    node = node.next
                node = None
        self.blocks = blocks 

    def update_size(self, size: int, metadata: Metadata):
        self.del_metadata(metadata)
        if size == 0: 
            i = self.blocks.index(0)
            metadata.head.index = i
            metadata.head.pointer = i*BLOCKSIZE
            self.blocks[i] = metadata
            return metadata

        zcount = ceil(size/BLOCKSIZE) - self.blocks.count(0)
        if zcount > 0:
            self.blocks += [0]*zcount
        block_count = ceil(size/BLOCKSIZE)
        head = None
        for k, block in enumerate(self.blocks):
            if block == 0:
                head = metadata.head
                head.index, head.pointer = k, k*BLOCKSIZE
                self.blocks[k] = metadata
                block_count -= 1
                k += 1
                break
    
        while block_count > 0:
            if self.blocks[k] == 0:
                self.blocks[k] = 1
                metadata.add_block(k, k*BLOCKSIZE)
                block_count -= 1 
                k += 1

        metadata.size = size

        return metadata

