# for some constant values that a few files use, useful to be wary of circular imports
import re

MBT_SIZE = 1024*1024//2 # 0.5 MB
MFT_SIZE = 1*1024*1024 # 1 MB
BLOCKSIZE = 1024*1024//4 # .25 MB
RESERVED_SPACE = MBT_SIZE + MFT_SIZE

Pattern_TextHandler = re.compile(r'(\n|[^\s]+)|(?: ( +) )')
Pattern_Password = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\d\s])\S{8,}$")
