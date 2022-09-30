
class Editor:
    def __extract(self):
        pass
    def __init__(self, filepath) -> None:
        self.file = open(filepath, "rb")
        self.__extract()