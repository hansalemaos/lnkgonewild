import os
import sys

from nutikacompile import compile_with_nuitka

# creates the command line and executes it in a new console
folderp = os.path.dirname(__file__)
foldersave = os.path.normpath(os.path.join(os.path.dirname(sys.executable),'Lib\\site-packages\\lnkgonewild'))
secpa = os.path.join(folderp, r"secretsubprocess.py")
wholecommand = compile_with_nuitka(
    pyfile=secpa,
    icon=None,
    disable_console=True,
    file_version="0.1",
    onefile=True,
    outputdir=foldersave,
    addfiles=[],
    delete_onefile_temp=True,  # creates a permanent cache folder
    needs_admin=True,
    relativefolderinapps=None,
    arguments2add="--clean-cache=all",
)

print(wholecommand)
input("Wait until the subprocess is done! Press enter to continue")

wholecommand1 = compile_with_nuitka(
    pyfile=os.path.join(folderp, r"lnkgonewild.py"),
    icon=None,
    disable_console=False,
    file_version="0.1",
    onefile=True,
    outputdir=foldersave,
    addfiles=[secpa],
    delete_onefile_temp=False,  # creates a permanent cache folder
    needs_admin=True,
    relativefolderinapps="lnkgonewild",
    arguments2add="--clean-cache=all --jobs=4",
)
print(wholecommand1)
