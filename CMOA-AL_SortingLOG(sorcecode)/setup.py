from distutils.core import setup
import py2exe,sys,os

sys.argv.append('py2exe')

'''
setup(
    
    windows=[{'script': 'MainGui.py', "icon_resources": [(1,"images/ico.ico")]}],
    console=[{'script': 'MainGui.py'}],   
    #zipfile=None,
    options = {'py2exe': {
        'bundle_files': 3,
    }},
)
'''

setup(
        name = "Sorting tool",
        version = "R1",
        options = {
            "py2exe" : {
                "compressed" : 1,
                #"optimize" : 2,
                "bundle_files" : 2,
                'dll_excludes': [ "mswsock.dll", "powrprof.dll" ]
                #"dll_excludes" : [ "MSVCP90.dll" ] 
                  }},
        console = ["maincode.py"],
        #windows = ["maincode.py"],
        zipfile = None,
        author = "@YiJieWang",
        author_email = "jasonwang@hc.hitrontech.com",
        url = "http://github.com/YiJie/",
      )