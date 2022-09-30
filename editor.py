
class Editor:
    def __read4Bytes(file):
        return int.from_bytes(file.read(4), "little")

    def __extract(self):
        file = self.file
        file.seek(8) #Skip the 1st 8 magic bytes
        self.texture_count = self.__read4Bytes(file)
        self.textureinfo_offset = self.__read4Bytes(file)

        TexInfo_list = []
        TexData_list = {}
        
        pointer = self.textureinfo_offset
        for i in range(self.texture_count):
            file.seek(pointer)

            uncompressed_size = self.__read4Bytes(file)
            current_textureData_pointer = self.__read4Bytes(file)
            
            textureData_size = 0
            if( i < self.texture_count-1):
                file.seek(4, 1) #Skip 4 bytes form current pos to get the pointer of next textureData
                next_textureData_pointer = self.__read4Bytes(file)
                textureData_size = next_textureData_pointer - current_textureData_pointer
            else:
                # If current texture is the last one in file, subtract from the filesize
                file.seek(0, 2)
                textureData_size = file.tell() - current_textureData_pointer
            
            file.seek(current_textureData_pointer)
            textureData = file.read(textureData_size)
            textureType = ""
            textureName = ""
            if( textureData[:2] == bytearray([0x1f, 0x8b]) ):
                textureType = "G-Zipped"
                textureName = "%d-%s" % ( i, textureData[10:].split(bytearray([0x00]))[0].decode() )
            else:
                textureType = "Uncompressed"
                textureName = "%d-TEX1" % (i)
            
            TexInfo_list.append({
                'name': textureName,
                'type': textureType,
                'data_size': textureData_size,
                'uncompressed_size': uncompressed_size
            })
            TexData_list[textureName] = textureData

            pointer += 8 #Each texture information occupy 8 bytes
        
        self.TexInfo_list = TexInfo_list
        self.TexData_list = TexData_list
        
    def __init__(self, filepath) -> None:
        self.file = open(filepath, "rb")
        if(self.__read4Bytes(self.file) != 0x4e494250):
            raise Exception("Unsupported File Format")
        self.__extract()