from idaapi import plugin_t, PLUGIN_UNL, PLUGIN_OK, get_highlight, get_current_viewer
from ida_funcs import get_func_name
from ida_kernwin import get_screen_ea
from requests import get
from ida_typeinf import idc_set_local_type
from local_types.db import base


class getFuncOrigin(plugin_t):
    flags = PLUGIN_UNL
    comment = (
        "Plugin resolves original file name by function name using local lumen database"
    )
    help = "Standing on function name just call from configparser import ConfigParserthe plugin from menu or press hotkey mentioned below"
    wanted_name = "Get function's original file name"
    wanted_hotkey = "Alt-F8"

    def init(self):
        print("Get original file name plugin is ready\n")
        return PLUGIN_OK

    def run(self, arg):
        postg = base()
        v = get_current_viewer()
        if v is not None:
            print("Function came from file: ")
            url = "http://127.0.0.1:8082/api/origin/"
            name = get_func_name(get_screen_ea())
            url += name
            res = get(url)
            print(res.text)
            hl = get_highlight(v)
            if hl is not None:
                (type_name, _) = hl
                typedef = postg.getTypedefFromDB(type_name)
                idc_set_local_type(-1, typedef, 0)

    def term(self):
        print("Get original file name plugin is unloaded now\n")
        pass


def PLUGIN_ENTRY():
    return getFuncOrigin()
