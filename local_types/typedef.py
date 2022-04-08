from ida_typeinf import (
    get_ordinal_qty,
    idc_get_local_type_name,
    idc_get_local_type_raw,
    idc_print_type,
)


class types:
    #   By now GetLocalType() returns typedef without ending ; and struct name
    #   it exists only in the definition's end
    #   makeProperTypedef makes the string suitable for set_local_type()
    def makeProperTypedef(self, typedef: str) -> str | None:
        if typedef:
            splitted = typedef.split()
            name = splitted[-1]
            splitted.insert(1, name)
            splitted.pop()
            return " ".join(splitted) + ";"
        return None

    def getTypedef(self, name: str) -> str | None:
        for ordinal in range(get_ordinal_qty()):
            if idc_get_local_type_name(ordinal) == name:
                (type, fields) = idc_get_local_type_raw(ordinal)
                return idc_print_type(type, fields, name, 0)
        return None
