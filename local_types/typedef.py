from idc import get_ordinal_qty, GetLocalType
from ida_typeinf import idc_get_local_type_name

class types():    
#   By now GetLocalType() returns typedef without ending ; and struct name - it exists only in the definition's end
#   makeProperTypedef makes the string suitable for set_local_type()
    def makeProperTypedef(self, typedef: str) -> str:
        splitted = typedef.split()
        name = splitted[-1]
        splitted.insert(1, name)
        splitted.pop()  
        return(" ".join(splitted) + ";")

    def getTypedef(self, name: str) -> str:
        for i in range(get_ordinal_qty()):
            if (idc_get_local_type_name(i) == name):
                return(GetLocalType(i, 0))
        return(None)