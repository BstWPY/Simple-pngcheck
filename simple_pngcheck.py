import enum
from typing import List, Optional
import zlib

"""
Add the packages you need here.
"""

class ChunkType(enum.Enum):
    """
    Types of PNG chunks.
    You can add more types if you need.
    """
    IHDR = enum.auto()
    IDAT = enum.auto()
    IEND = enum.auto()
    iCCP = enum.auto()
    eXIf = enum.auto()
    iTXt = enum.auto()
    cHRM = enum.auto()
    bKGD = enum.auto()
    tEXt = enum.auto()

    def __str__(self):
        return self.name
    
    def FindType(chunktype: str):
        if chunktype == 'IHDR':
            return ChunkType.IHDR
        elif chunktype == 'IDAT':
            return ChunkType.IDAT
        elif chunktype == 'IEND':
            return ChunkType.IEND
        elif chunktype == 'iCCP':
            return ChunkType.iCCP
        elif chunktype == 'eXIf':
            return ChunkType.eXIf
        elif chunktype == 'iTXt':
            return ChunkType.iTXt
        elif chunktype == 'cHRM':
            return ChunkType.cHRM
        elif chunktype == 'bKGD':
            return ChunkType.bKGD
        elif chunktype == 'tEXt':
            return ChunkType.tEXt
        else:
            return None

class Chunk():
    """
    PNG chunk.

    Example:
        Chunk(0x0000c, 0x0000000D, ChunkType.IHDR)
    """
    def __init__(
            self,
            offset: int, 
            length: int, 
            chunktype: ChunkType, 
            data: Optional[bytes] = None,
            crc32: Optional[int] = None
        ):
        self.offset = offset
        self.length = length
        self.type = chunktype
        self.data = data
        self.crc32 = crc32
    
    def checkCRC(self) -> bool:
        if int(self.crc32,16)==zlib.crc32(str(self.type).encode()+self.data):#读取的校验码和正确校验码进行比较
            return True
        else:
            print('CRC32 ERROR in Chunk at offset: '+self.offset)
class PNG():
    def __init__(
            self, 
            name: str,
            chunks: List[Chunk] = []
        ):
        self.name = name
        self.chunks = chunks
    
    def getInfo(self):
        print(f"File: {self.name}")
        for chunk in self.chunks:
            print(f"chunk {chunk.type} at offset {chunk.offset}, length {chunk.length}")
    
    def addChunk(self, chunk: Chunk):
        self.chunks.append(chunk)

    def check_CRC(self) -> bool:
        return all(chunk.checkCRC() for chunk in self.chunks)

def ProcessPNG(png: PNG):
    f=open("your file",'rb')
    f.seek(8)#跳过png文件头
    roffset=12#第一个块的偏移
    k=0#定义偏移加量
    while True:
        rlength=int(f.read(4).hex(),16)#长度
        roffset=roffset+k#偏移
        rChunktype=ChunkType.FindType((f.read(4)).decode('utf-8'))#块的类型
        rdata=f.read(rlength)#数据       
        rcrc32=f.read(4).hex()#CRC32校验码 
        png.addChunk(Chunk(hex(roffset),rlength,rChunktype,rdata,rcrc32))
        if(rChunktype==ChunkType.IEND):
            break#读到文件尾就退出
        k=12+rlength#数据块4字节+校验码4字节+数据长度+下一块（如果有的话）长度4字节

if __name__ == "__main__":
    # Create a PNG object
    png = PNG("your file")

    # Process the PNG object
    ProcessPNG(png)    

    # Print the information of the PNG object
    png.getInfo()
    
    print("--------------------")

    # Check the CRC of each chunk
    if png.check_CRC():
        print("CRC check passed.")