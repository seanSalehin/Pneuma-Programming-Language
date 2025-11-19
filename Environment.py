#for typing safe
from llvmlite import ir

class Environment:
    def __init__(self, records: dict[str, tuple[ir.Value, ir.Type]]=None, parent=None, name:str = "global"):
        self.records=records if records else {}
        self.parent = parent
        self.name=name

    
    #define method
    def define(self, name, value, _type):
        self.records[name]=(value, _type)
        return value
    

    def lookup(self, name):
        return self.__resolve(name)
    

    #called internally in the environment class
    def __resolve(self, name):
        if name in self.records:
            return self.records[name]
        elif self.parent:
            return self.parent.__resolve(name)
        else:
            return None
