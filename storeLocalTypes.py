from idaapi import *
from idautils import *
from ida_nalt import get_input_file_path
from local_types.typedef import types
from local_types.db import base

class storeLocalTypes(plugin_t):
    flags = PLUGIN_UNL
    comment = "Plugin stores custom local types in Postgres database"
    help = "Standing on localtype's name just call the plugin from menu or press hotkey mentioned below"
    wanted_name = "Save typedefs to restore them in another .idbs"
    wanted_hotkey = "Alt-F1"       
 
    def init(self):
        print("Store local type plugin is ready\n")
        return PLUGIN_OK

#   By now GetLocalType() returns typedef without ending ; and struct name - it exists only in the definition's end
#   makeProperTypedef makes the string suitable for set_local_type()
    def makeProperTypedef(self, typedef: str) -> str:
        splitted = typedef.split()
        name = splitted[-1]
        splitted.insert(1, name)
        splitted.pop()  
        return(" ".join(splitted) + ";")

    def run(self, arg) -> None:
        print('Saving the local type')
        postgr = base()  
        type = types()      
        try:
            v = get_current_viewer()
            if v is not None: 
                hl = get_highlight(v)
                if hl is not None:
                    (type_name, _) = hl                    
                    typedef = type.getTypedef(type_name)
                    if typedef is not None:
                        file_path = get_input_file_path()                        
                        conn = postgr.insertIntoDB(type_name, type.makeProperTypedef(typedef), file_path)
        except (Exception, Error) as error:
            print(error)
 
    def term(self):
        print("Get original file name plugin is unloaded now\n")
        pass

def PLUGIN_ENTRY():
    return storeLocalTypes()
