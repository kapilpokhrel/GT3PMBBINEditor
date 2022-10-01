
class Editor:
    def __read4Bytes(self, file):
        return int.from_bytes(file.read(4), "little")

    def __extract(self):
        file = self.file
        file.seek(8) #Skip the 1st 8 magic bytes
        self.texture_count = self.__read4Bytes(file)
        self.textureinfo_offset = self.__read4Bytes(file)

        TexInfo = []
        TexData = {}
        
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
            
            TexInfo.append({
                'name': textureName,
                'type': textureType,
                'data_size': textureData_size,
                'uncompressed_size': uncompressed_size
            })
            TexData[textureName] = textureData

            pointer += 8 #Each texture information occupy 8 bytes
        
        self.TexInfo = TexInfo
        self.TexData = TexData
        
    def __init__(self, filepath) -> None:
        try:
            self.file = open(filepath, "rb")
        except Exception as e:
            raise Exception(e)
        if(self.__read4Bytes(self.file) != 0x4e494250):
            raise Exception("Unsupported File Format")
        self.__extract()

    def assemble_and_save(self, filename):
        with open(filename, "wb") as file:
            file.write(bytearray([0x50, 0x42, 0x49, 0x4E, 0x00, 0x00, 0x00, 0x00])) #Magic Bytes
            file.write(self.texture_count.to_bytes(4, byteorder="little")) #No of textures
            file.write(bytearray([0x10, 0x00, 0x00, 0x00])) #Beginning of pointers list which is always 0x10 after 16 byte header

            texture_data_offset = 16 + 8*self.texture_count #16 byte header + 8 bytes info for each texture
            for texture in self.TexInfo:
                file.write(texture['uncompressed_size'].to_bytes(4, byteorder="little"))
                file.write(texture_data_offset.to_bytes(4, byteorder="little"))
                texture_data_offset += texture['data_size']

            for texture in self.TexInfo:
                file.write(self.TexData[texture['name']])
    
    def extract_texture(self, index):
        name = self.TexInfo[index]['name']
        filename = ""
        if(self.TexInfo[index]['type'] == 'G-Zipped'):
            filename = name.split('-', 1)[1]+'.gz'
        else:
            filename = name.split('-', 1)[1]+'.img'
        
        with open(filename, "wb") as texfile:
            texfile.write(self.TexData[name])