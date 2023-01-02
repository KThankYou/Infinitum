# Contains skeleton of all classes, used to not cause an accidental circular import while type hinting
# Used only if the class is just needed for TypeHinting and should not be called
# v.5.5

from typing import Tuple, Dict, BinaryIO, List, Callable, Optional

import tempfile, pygame

class Metadata:
    def __init__(self, name: str, index: int, pointer: int, size: int = 0, 
                    app: bool = False) -> None: raise NotImplementedError

    def add_block(self, index: int, pointer: int): raise NotImplementedError
    
    def __repr__(self) -> str: raise NotImplementedError

class Block:
    def __init__(self, index: int = 0, pointer: int = 0) -> None: raise NotImplementedError

    def __str__(self) -> str: raise NotImplementedError

    def __repr__(self) -> str: raise NotImplementedError

class MasterBootTable:
    def __init__(self, config: Dict) -> None: raise NotImplementedError

    def load(cls, file: BinaryIO) -> 'MasterBootTable': raise NotImplementedError
    
    @classmethod
    def make_MBT(cls, user: str, password: str) -> 'MasterBootTable': raise NotImplementedError
    
    def flush(self, file: BinaryIO) -> None: raise NotImplementedError
    
    def installed(self) -> None: raise NotImplementedError

class MasterFileTable:
    def __init__(self, MFT: Dict, blocks: List[int]) -> None: raise NotImplementedError

    def load(cls, FileManager) -> 'MasterFileTable': raise NotImplementedError

    def make_MFT(cls) -> 'MasterFileTable': raise NotImplementedError

    def flush(self, FileManager: Callable, drive: BinaryIO, password: str) -> None: raise NotImplementedError

    def get_apps(self) -> Dict[str, Metadata]: raise NotImplementedError

    def make_dir(self, folder_name: str, folder_path: str = '') -> Optional[1]: raise NotImplementedError

    def del_dir(self, folder_name: str, folder_path: str = '') -> Optional[1]: raise NotImplementedError

    def cd(self, folder: str): raise NotImplementedError

    def set_cwd(self, directory: str) -> Optional[1]: raise NotImplementedError

    def get_cwd(self) -> str: raise NotImplementedError

    def make_file(self, file_name: str, metadata: Metadata, file_path: str) -> Optional[1]: raise NotImplementedError

    def exists(self, file_name: str, file_path: str) -> bool: raise NotImplementedError

    def get_file(self, file_name: str, file_path: str) -> Metadata: raise NotImplementedError

    def del_file(self, file_path: str) -> Optional[1]: raise NotImplementedError

    def parse_path(self, path: str) -> List[str]: raise NotImplementedError

    def join(*args): raise NotImplementedError

    def make_metadata(self, size: int, name: str) -> Metadata: raise NotImplementedError

    def del_metadata(self, metadata: Metadata) -> None: raise NotImplementedError

    def consolidate(self) -> None: raise NotImplementedError

    def update_size(self, metadata: Metadata, size: int): raise NotImplementedError

class FileManager:
    def __init__(self, drive_path: str, pwd: str) -> None:
        self.MFT: MasterFileTable = None
        self.MBT: MasterBootTable = None

    def temp(self) -> tempfile.TemporaryDirectory: raise NotImplementedError

    def check_install(drive_path: str) -> bool: raise NotImplementedError

    def get_user(drive_path: str) -> str: raise NotImplementedError

    def get_pwd(drive_path: str) -> str: raise NotImplementedError

    def get_config(drive_path: str) -> Dict: raise NotImplementedError

    def get_res(drive_path: str) -> Tuple[int, int]: raise NotImplementedError

    def initial_setup(cls, drive_path: str, username: str, password: str ) -> 'FileManager': raise NotImplementedError

    def __create_file(self, file_name: str, file_path: str) -> None: raise NotImplementedError

    def write(self, obj: object, metadata: Metadata) -> None: raise NotImplementedError

    def write_MFT(drive: BinaryIO, pwd: str, obj: object): raise NotImplementedError

    def read_MFT(self) -> MasterFileTable: raise NotImplementedError

    def write_open(self, file_name: str, file_path: str = '') -> 'WriteIO': raise NotImplementedError

    def read_open(self, file_name: str, file_path: str = '') -> 'ReadIO': raise NotImplementedError

    def read(self, metadata: Metadata) -> object: raise NotImplementedError

    def __read_bytes(self, Bytes: int, pointer: int) -> bytes: raise NotImplementedError

    def encrypt(data: bytes, pwd: str) -> bytes: raise NotImplementedError

    def __decrypt(self, data: bytes) -> bytes: raise NotImplementedError

    def flush(self) -> None: raise NotImplementedError

    def close(self) -> None: raise NotImplementedError

    def make_folder(self, folder_name: str, folder_path: str) -> str: raise NotImplementedError

    def del_folder(self, folder_name: str, folder_path: str) -> None: raise NotImplementedError

    def get_apps(self) -> Dict[str, Metadata]: raise NotImplementedError

class WriteIO:
    def __init__(self, manager: FileManager, metadata: Metadata\
                ) -> None: raise NotImplementedError

    def write(self, data: object) -> int: raise NotImplementedError

    def flush(self): raise NotImplementedError

    def close(self): raise NotImplementedError

class ReadIO:
    def __init__(self, manager: FileManager, metadata: Metadata) -> None: raise NotImplementedError

    def read(self): raise NotImplementedError
        
    def close(self):  raise NotImplementedError

class Login:
    def __init__(self) -> None: raise NotImplementedError

    def main(self) -> None: raise NotImplementedError

    def draw(self) -> pygame.Surface: raise NotImplementedError

    def check_password(self) -> bool: raise NotImplementedError

class _Process:
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError
    
    def draw(self) -> pygame.Surface:
        raise NotImplementedError

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int], keys: pygame.key.ScancodeWrapper, *args, **kwargs) -> None:
        raise NotImplementedError

class Frame:
    def __init__(self, process: _Process, border: bool = True, fullscreen: bool = False, name: str = None, 
            pos: Tuple[int, int] = (0, 0), size: Tuple[int, int] = (0, 0), max_res: Tuple[int, int] = (1600, 900), 
            working_dir: str = tempfile.TemporaryDirectory().name, *args, **kwargs) -> None: 
        self.name: str = None
        self.working_dir: str = None
        self.alive: bool = None
        self.id: int = None
        raise NotImplementedError

    def draw(self) -> pygame.Surface: raise NotImplementedError

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int], active: bool = True, *args, **kwargs) -> None: raise NotImplementedError

    def update_pos(self, x: int = None, y: int = None, w: int = None, h: int = None) -> None: raise NotImplementedError

    def get_rect(self) -> pygame.Rect: raise NotImplementedError

    def get_pos(self) -> Tuple[int, int]: raise NotImplementedError

    def get_size(self) -> Tuple[int, int]: raise NotImplementedError

    def mini(self) -> None: raise NotImplementedError

    def close(self) -> None: raise NotImplementedError

    def maxi(self) -> None: raise NotImplementedError

    def restore(self) -> None: raise NotImplementedError

    def refresh(self) -> None: raise NotImplementedError

class Icon:
    def __init__(self, process: _Process, name: str = 'name_placeholder', process_size: Tuple[int, int] = (0, 0), 
        image: str = None, rect: pygame.Rect = 'empty_rect', fullscreen: bool = False, max_res: Tuple[int, int] = (1600, 900)) -> None: 
        self.process: _Process = None
        self.name: str = None
        self.metadata: Metadata = None
        self.image: pygame.Surface = None

    def launch(self, working_dir: str) -> Frame: raise NotImplementedError

    def draw(self, surf: pygame.Surface, rect: pygame.Rect) -> pygame.Surface: raise NotImplementedError

    def set_psize(self, x: int = None, y: int = None): raise NotImplementedError

    def update_pos(self, x: int = None, y: int = None, w: int = None, h: int = None) -> None: raise NotImplementedError

class Installer:
    def __init__(self, FM: FileManager, max_res: Tuple[int, int] = (1600, 900),paths: List[str] = []) -> None: raise NotImplementedError

    def install(self): raise NotImplementedError

    def get_icon(self, metadata: Metadata) -> Icon: raise NotImplementedError

class DesktopWindowManager:
    def __init__(self, pwd: str, display: pygame.Surface, windows: List[Frame] = [], icons: List[Icon] = []) -> None: 
        self.FM: FileManager = None
        self.bg: pygame.Surface = None
        self.icons, self.windows = list(icons), list(windows)
        self.grid: pygame.Rect = None
        self.display: pygame.Surface = None
        self.active = None
        self.installer: Installer = None
        self.taskbar: Taskbar = None
        self.surf: pygame.Surface = None
        raise NotImplementedError

    def main(self) -> None: raise NotImplementedError

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]) -> None: raise NotImplementedError

    def add_icon(self, icon_gen: Icon, **kwargs) -> None: raise NotImplementedError

    def shutdown(self, code = 0) -> int: raise NotImplementedError

    def get_apps(self) -> None: raise NotImplementedError

    def refresh(self) -> None: raise NotImplementedError

class Taskbar:
    def __init__(self, display_res: Tuple[int, int] = (1600, 900), thickness: int = 60, processes: Dict[Tuple[pygame.Surface, Frame], pygame.Rect] = {},
            color: Tuple[int, int, int] = (210, 210, 210), power_image: pygame.Surface = '_default_power') -> None:
        self.process_num: int = None    
        self.processes = dict(processes)
        raise NotImplementedError

    def add_process(self, image: pygame.Surface, process: Frame) -> None: raise NotImplementedError

    def calculate_icon_position(self) -> Tuple[int, int]: raise NotImplementedError

    def refresh(self) -> None: raise NotImplementedError

    def draw(self): raise NotImplementedError

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]) -> None: raise NotImplementedError

    def set_datetime(self) -> None: raise NotImplementedError

    def get_rect(self) -> pygame.Surface: raise NotImplementedError

class TextHandler:
    def __init__(self, font: str = 'OpenSans', starting: Tuple = (0, 0)) -> None: raise NotImplementedError

    def write(self, text: str, color: tuple | pygame.Color, surface: pygame.Surface, size: int = None, width: bool = None,
        U: bool = False, B: bool = False, I: bool = False, S: bool = False, newline_width: int = 20, special_flags: List = 0) -> None: raise NotImplementedError

    def set_pos(self, x: int = 0, y: int = 0) -> None:  raise NotImplementedError

    def get_pos(self) -> Tuple[int]:  raise NotImplementedError

    def reset_pos(self) -> None:  raise NotImplementedError

    def print(self, text: str, color: tuple | pygame.Color, surface: pygame.Surface, 
            width: bool = None, modifier: str = 'Text1', newline_width: int = 20, special_flags: List = 0) -> None:raise NotImplementedError

    def get_rect(self, text: str, size: int = 20, bold: bool = False, modifier: str = None, center: pygame.Rect = None) -> pygame.Rect: raise NotImplementedError

class Button:
    def __init__(self, 
            text: str, Font: str, text_color: Tuple[int] = (255, 255, 255), box_color: Tuple[int] = (0, 0, 0),
            function: Callable = 'NOTHING', margin: Tuple[int] = (7, 7), text_size: Tuple[int] = 20, pos = (0, 0), border_size: int = 1,
            hover_color: Tuple[int] = (200, 200, 200), border: bool = False, border_color: Tuple[int, int, int] = (0, 0, 0),
            *args, **kwargs) -> None: raise NotImplementedError

    def on_click(self, generator = False): raise NotImplementedError

    def __repr__(self) -> str: raise NotImplementedError

    def draw(self) -> Tuple[pygame.Surface]: raise NotImplementedError

    def get_pos(self) -> Tuple[int]: raise NotImplementedError

    def get_rect(self) -> pygame.Rect: raise NotImplementedError

    def set_pos(self, x: int = None, y: int = None) -> None: raise NotImplementedError

class TextBox:
    def __init__(self, 
            placeholder: str, font: str, text_color: Tuple[int] = (0, 0, 0), box_color: Tuple[int] = (255, 255, 255),
            size: Tuple[int] = (100, 30), text_size: Tuple[int] = 20, pos = (0, 0), password: bool = False,
            border_size: int = 1, border: bool = False, border_color: Tuple[int, int, int] = (0, 0, 0)) -> None: raise NotImplementedError

    def draw(self) -> pygame.Surface: raise NotImplementedError

    def typing(self) -> None: raise NotImplementedError

    def set_pos(self, x: int = None, y: int = None) -> None: raise NotImplementedError

    def get_pos(self) -> Tuple[int, int]: raise NotImplementedError

    def set_size(self, w: int = None, h: int = None) -> None: raise NotImplementedError

    def get_size(self) -> Tuple[int, int]: raise NotImplementedError

    def get_rect(self) -> pygame.Rect: raise NotImplementedError

    def get_text(self) -> str: raise NotImplementedError

class _Dropdown:
    def __init__(self, width: int, height: int, buttons: List[Button],
        gap_color: Tuple[int, int, int], gap_size: int, *args, **kwargs) -> None: raise NotImplementedError
        
    def refresh(self) -> None: raise NotImplementedError

    def __get_rects(self, buttons: List[Button]) -> Dict[Button, pygame.Rect]: raise NotImplementedError

    def draw(self) -> pygame.Surface: raise NotImplementedError

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int], abs_pos: pygame.Rect, *args, **kwargs) -> None: raise NotImplementedError

class DropDownMenu:
    def __init__(self, pos: Tuple[int, int], width: int = 200, height: int = 30, dropup: bool = False, 
    buttons: List[Button] = [], gap_color: Tuple[int, int, int] = (0, 0, 0), gap_size: int = 2) -> None: raise NotImplementedError

    def draw(self) -> pygame.Surface: raise NotImplementedError

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]): raise NotImplementedError
