# Creates .lnk files (with admin rights if desired), can execute any file in hidden mode (no more bothersome popups when executing .bat/.cmd files)

## 1. Installing 

This tool creates .lnk files either from python or your shell (cmd.exe) 
It is possible to create .lnk files with "Run as Administrator" checked.

You can also execute every executable file in hidden mode (no window, no icon in the taskbar), no bothersome popup when opening bat files.
However, it is still possible to capture the stdout.

```python
pip install lnkgonewild
```

```python
# install nuitka! https://github.com/Nuitka/Nuitka


from lnkgonewild import lnkcompile # import to compile

# The command line that was created and executed to compile secretsubprocess.exe
# output:
# start "" "C:\ProgramData\anaconda3\envs\adda\python.exe" -m nuitka C:/ProgramData/anaconda3/envs/adda/lib/site-packages/lnkgonewild/secretsubprocess.py --standalone --assume-yes-for-downloads --windows-disable-console --onefile --windows-uac-admin --file-version=0.1 --clean-cache=all

# When you see this messsage, please wait until the first compilation has finished. 
Wait until the subprocess is done! Press enter to continue>? 

# The command line that was created and executed to compile lnkgonewild.exe
# output:
# start "" "C:\ProgramData\anaconda3\envs\adda\python.exe" -m nuitka C:/ProgramData/anaconda3/envs/adda/lib/site-packages/lnkgonewild/lnkgonewild.py --standalone --assume-yes-for-downloads --onefile --include-data-files=C:/Users/hansc/AppData/Local/Temp/tmpaz6c5xsy=.//=**/*.* --windows-uac-admin --file-version=0.1 --onefile-tempdir-spec=%CACHE_DIR%/lnkgonewild/0.1 --clean-cache=all --jobs=4
# https://github.com/hansalemaos/lnkgonewild/raw/main/1.png
```

![](https://github.com/hansalemaos/lnkgonewild/blob/main/1.png?raw=true)

The compiled files can also be downloaded (Python is not needed):
https://github.com/hansalemaos/lnkgonewild/raw/main/lnkgonewild.exe
https://github.com/hansalemaos/lnkgonewild/raw/main/secretsubprocess.exe

## Warnings

#### Due to the app's suspicious behavior (changing bytes in .lnk files, executing other processes as subprocesses, hiding windows, capturing output, containing exe in exe files (secretsubprocess.exe is in lnkgonewild.exe, writing scripts to the HDD and executing them), you might have to add those files as exceptions to your antivirus.

![](https://github.com/hansalemaos/lnkgonewild/blob/main/5.png?raw=true)

![](https://github.com/hansalemaos/lnkgonewild/blob/main/6.png?raw=true)


## 3. Creating “common” shortcuts 


![](https://github.com/hansalemaos/lnkgonewild/blob/main/2.png?raw=true)

```python
from lnkgonewild.lnkgonewild import create_shortcut

# stdout can't be captured when minimized_maximized_normal_invisible!='invisible'


create_shortcut(
    shortcut_path=r"C:\Users\hansc\Desktop\testlnk2.lnk",
    target=r"C:\cygwin\bin\ls.exe",
    arguments=[r"-la"],
    working_dir="c:\\Windows\\Fonts",
    minimized_maximized_normal_invisible="normal",  #
    silentlog=None,  # stdout can be written to file if the process is invisible
    asadmin=False,  # enables the admin check box
    hotkey="Ctrl+Alt+q",
)

# The JS that created the link 
var sh = WScript.CreateObject("WScript.Shell");
var shortcut = sh.CreateShortcut("C:\\Users\\hansc\\Desktop\\testlnk2.lnk");
shortcut.WindowStyle = 4;
shortcut.TargetPath = "C:\\cygwin\\bin\\ls.exe";
shortcut.Hotkey = "Ctrl+Alt+q";
shortcut.Arguments = "-la";
shortcut.WorkingDirectory = "c:\\Windows\\Fonts";
shortcut.IconLocation = "C:\\cygwin\\bin\\ls.exe";
shortcut.Save();
```

![](https://github.com/hansalemaos/lnkgonewild/blob/main/3.png?raw=true)


![](https://github.com/hansalemaos/lnkgonewild/blob/main/4.png?raw=true)


## 4. Creating “special” shortcuts (hidden execution)


```python
# If you pass minimized_maximized_normal_invisible="invisible"
# the window/console will be hidden, but stdout can be captured
# if secretsubprocess.exe is missing, the function will ask to compile it.
# You need https://github.com/Nuitka/Nuitka for the compilation
# If a hidden process gets stuck, you can kill it using the task manager

create_shortcut(
    shortcut_path=r"C:\Users\hansc\Desktop\testlnk3.lnk",
    target=r"C:\cygwin\bin\ls.exe",
    arguments=[r"-la" ,"-R"],
    working_dir="c:\\Windows\\System32",
    minimized_maximized_normal_invisible="invisible",  # secretsubprocess.exe is necessary
    silentlog="c:\\logfilels22.txt",  # stdout can be written to file if the process is invisible
    asadmin=True,  # enables the admin check box by changing some bytes in the .lnk file
    hotkey="Ctrl+Alt+e",
)

# The JS that created the link secretsubprocess.exe takes care of the process and hides everything
var sh = WScript.CreateObject("WScript.Shell");
var shortcut = sh.CreateShortcut("C:\\Users\\hansc\\Desktop\\testlnk3.lnk");
shortcut.WindowStyle = 4;
shortcut.Hotkey = "Ctrl+Alt+e" ;
shortcut.TargetPath = "C:\\ProgramData\\anaconda3\\envs\\adda\\lib\\site-packages\\lnkgonewild\\secretsubprocess.exe";
shortcut.Arguments = "--exe C:\\cygwin\\bin\\ls.exe --log c:\\logfilels22.txt --args -la -R";
shortcut.WorkingDirectory = "c:\\Windows\\System32";
shortcut.IconLocation = "C:\\ProgramData\\anaconda3\\envs\\adda\\lib\\site-packages\\lnkgonewild\\secretsubprocess.exe";
shortcut.Save();
            
# lnkgonewild can also be used as a command line tool to create links

# usage: lnkgonewild.exe [-h] [--shortcut_path SHORTCUT_PATH] [--target TARGET] [--hotkey HOTKEY] [--working_dir WORKING_DIR] [--mode MODE] [--silentlog SILENTLOG] [--asadmin ASADMIN] [--args ARGS]
#
# options:
#   -h, --help                     show this help message and exit
#   --shortcut_path SHORTCUT_PATH  The path where the shortcut file will be created.
#   --target TARGET                The path to the target file or application that the shortcut will launch.
#   --hotkey HOTKEY                Hotkey for opening the lnk file. Defaults to ''.
#   --working_dir WORKING_DIR      The working directory for the target file or application. (Working dict of shortcut_path).
#   --mode MODE                    The window state of the target application when launched. Can be "normal", "minimized", "maximized", or "invisible".
#   --silentlog SILENTLOG          The path to a log file for the target application when minimized_maximized_normal_invisible == "invisible".
#   --asadmin ASADMIN              Whether to run the shortcut as an administrator. Defaults to False.
#   --args ARGS                    Arguments to be passed to the target file or application as they would receive them. Example: lnkgonewild.exe --shortcut_path C:\Users\hansc\Desktop\testlink.lnk --target C:\cygwin\bin\lsattr.exe
#                                  --hotkey Ctrl+Alt+q --working_dir None --mode minimized --silentlog None --asadmin False --arguments -a -d


# --mode invisible -> window is hidden, stdout can be captured
# lnkgonewild --shortcut_path C:\Users\hansc\Desktop\dirlist.lnk --target C:\cygwin\bin\ls.exe --hotkey Ctrl+Alt+e --working_dir C:\Windows\Branding --mode invisible --silentlog c:\diroutputcap3.txt --asadmin True --args -la
# --mode normal ->  windows is shown, stdout can't be captured
# lnkgonewild --shortcut_path C:\Users\hansc\Desktop\dirlist.lnk --target C:\cygwin\bin\ls.exe --hotkey Ctrl+Alt+e --working_dir C:\Windows\Branding --mode normal --silentlog c:\diroutputcap3.txt --asadmin True --args -la -R

# If you want to capture the stdout without secretsubprocess.exe, you can do something like that:
# Create a bat file:
# cd c:\Windows\System32
# dir /b/s > c:\dirlistoutput.txt

# lnkgonewild.exe --shortcut_path C:\Users\hansc\Desktop\testbat.lnk --target C:\Users\hansc\Desktop\listdir.bat --hotkey Ctrl+Alt+i --working_dir None --mode minimized --silentlog None --asadmin False
```

