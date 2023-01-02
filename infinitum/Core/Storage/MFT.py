from Infinitum.Core.Storage.Metadata import Metadata
from Infinitum.Core.Misc.TYPEHINTS import FileManager
from Infinitum.Core.Misc.CONSTANTS import BLOCKSIZE

from typing import BinaryIO, Dict, List, Optional, Callable
from math import ceil

def modified(function):
    def helper(*args, **kwargs):
        res = function(*args, **kwargs)
        args[0].modified = True
        return res
    return helper

class MasterFileTable:
    def __init__(self, MFT: Dict[str, Dict], blocks: List[int]) -> None:
        self.table = MFT
        self.cwd = ('root', MFT['root'])
        self.path = ['.']
        self.modified = False
        self.blocks = blocks # 0 = empty, 1 = filled, each block is of size BLOCKSIZE

    @classmethod
    def load(cls, FM: FileManager) -> 'MasterFileTable':
        return FM.read_MFT(FM.drive, FM.key)
    
    @classmethod
    def make_MFT(cls) -> 'MasterFileTable':
        table = {'root': 
            {'Apps': {'__files': {}}, 
            'User': {'__files': {}}, 
            '__files': {}}}
        obj = cls(table, [])
        obj.modified = True
        return obj
    
    def flush(self, FileManager: Callable, drive: BinaryIO, password: str) -> None:
        if self.modified:
            FileManager.write_MFT(drive, password, self)
            self.modified = False
        else: return 1

    def get_apps(self) -> Dict[str, Metadata]: # {name: metadata}
        return {i: j['__files'][i] for i, j in \
        self.table['root']['Apps'].items() if i != '__files'}

    #Return None if successful, 1 if fail
    @modified
    def make_dir(self, folder_name: str, folder_path: str = '') -> Optional[1]:
        c_dir, c_path, self.cwd, self.path = self.cwd, self.path, ('root', self.table['root']), ['.']
        if folder_path: self.set_cwd(folder_path)
        if folder_name in self.cwd[1]: return 1
        self.cwd[1][folder_name] = {'__files':{}}
        path = self.join(*self.path, folder_name)
        self.cwd, self.path = c_dir, c_path
        return path

    @modified
    def del_dir(self, folder_name: str, folder_path: str = '') -> Optional[1]:
        c_dir, c_path, self.cwd, self.path = self.cwd, self.path, ('root', self.table['root']), ['.']
        if folder_path: self.set_cwd(folder_path)
        if folder_name not in self.cwd[1]: return 1
        self.recursive_delete(self.cwd[1][folder_name])
        del self.cwd[1][folder_name]
        self.cwd, self.path = c_dir, c_path

    def recursive_delete(self, folder: Dict):
        for _, file in folder['__files'].items(): 
            self.del_metadata(file)
        del folder['__files']
        for part in folder:
            self.recursive_delete(part)
        del folder

    def cd(self, folder: str):
        if folder not in self.cwd[1]: return 1
        self.cwd = folder, self.cwd[1][folder]
        self.path.append(folder)

    def set_cwd(self, directory: str) -> Optional[1]:
        c_dir, c_path, self.cwd, self.path = self.cwd, self.path, ('root', self.table['root']), ['.'] # c_ means current path
        directory = self.parse_path(directory)
        for i in directory:
            if self.cd(i): 
                self.cwd, self.path = c_dir, c_path
                return 1
        
    @property
    def get_cwd(self) -> str: return '\\'.join(self.path)

    @modified
    def make_file(self, file_name: str, metadata: Metadata, file_path: str) -> Optional[1]:
        c_dir, c_path, self.cwd, self.path = self.cwd, self.path, ('root', self.table['root']), ['.']
        if file_path: self.set_cwd(file_path)
        folder = self.cwd[1]['__files']
        self.cwd, self.path = c_dir, c_path
        if file_name in folder: return 1
        folder[file_name] = metadata
    
    def exists(self, file_name: str, file_path: str) -> bool:
        c_dir, c_path, self.cwd, self.path = self.cwd, self.path, ('root', self.table['root']), ['.']
        if self.set_cwd(file_path or ''): return False
        if file_name in self.cwd[1]['__files']: 
            self.cwd, self.path = c_dir, c_path
            return True
        self.cwd, self.path = c_dir, c_path
    
    def get_file(self, file_name: str, file_path: str) -> Metadata:
        c_dir, c_path, self.cwd, self.path = self.cwd, self.path, ('root', self.table['root']), ['.']
        if not file_path: raise Exception('Invalid file path')
        self.set_cwd(file_path)
        folder = self.cwd[1]['__files']
        self.cwd, self.path = c_dir, c_path
        return folder[file_name]

    @modified
    def del_file(self, file_path: str) -> Optional[1]:
        c_dir, c_path, self.cwd, self.path = self.cwd, self.path, ('root', self.table['root']), ['.']
        *path, file = MasterFileTable.parse_path(file_path)
        self.set_cwd(path[:-1])
        folder, self.cwd, self.path = self.cwd[1]['__files'], c_dir, c_path
        if file not in folder: return 1
        self.del_metadata(folder[file])
        del folder[file]

    def parse_path(self, path: str) -> List[str]:
        raw = path.split('\\')
        if raw[0] == '.': raw = self.path[1:] + [i for i in raw[1:] if i]
        return raw
        
    @staticmethod
    def join(*args):
        args: List[str] = args
        return '\\'.join((i.rstrip('\\') for i in args))

    @modified
    def make_metadata(self, size: int, name: str) -> Metadata:
        self.blocks.append(0)
        if size == 0: 
            i = self.blocks.index(0)
            meta = Metadata(name, i, i*BLOCKSIZE)
            self.blocks[i] = meta
            return meta
        zcount = ceil(size/BLOCKSIZE) - self.blocks.count(0)
        if zcount > 0:
            self.blocks += [0]*zcount
        block_count = ceil(size/BLOCKSIZE)
        head = None
        for k, block in enumerate(self.blocks):
            if block == 0:
                head = Metadata(name, k, i*BLOCKSIZE, size)
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

    @modified
    def del_metadata(self, metadata: Metadata) -> None:
        node = metadata.head
        while node:
            self.blocks[node.index] = 0
            node = node.next

    @modified
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

    @modified
    def update_size(self, metadata: Metadata, size: int):
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
