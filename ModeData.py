class ModeData:
    def __init__(self, parent, key, display):
        self.parent = parent
        self.key = key
        self.display = display
        
    def getParentEnumType(self):
        return self.parent