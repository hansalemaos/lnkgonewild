import argparse
import ast
import sys
import tempfile
import os
import pathlib

import subprocess
from time import sleep
from typing import Union

from nutikacompile import compile_with_nuitka


def escape_windows_path(filepath):
    return os.path.normpath(
        r"\\".join(
            [
                f'"{x}"' if i != 0 else x
                for i, x in enumerate(
                    pathlib.Path(os.path.normpath(os.path.abspath(filepath))).parts
                )
            ]
        )
    )


def escapepa(p):
    return os.path.normpath(p).replace("\\", "\\\\")


def escapeargu(p):
    if not p:
        return []
    if not isinstance(p, list):
        p = [p]
    allali = []
    for pp in p:
        allali.append(pp.replace("\\", "\\\\").replace('"', '\\"'))
    return allali


def create_shortcut(
    shortcut_path: str,
    target: str,
    arguments: list,
    hotkey="",
    working_dir: Union[str, None] = None,
    minimized_maximized_normal_invisible: str = "minimized",
    silentlog: Union[str, None] = None,
    asadmin: bool = False,
):
    r"""
    Creates a Windows shortcut (.lnk) file at the specified path with the specified target, arguments, and working directory.

    Args:
        shortcut_path (str): The path where the shortcut file will be created.
        target (str): The path to the target file or application that the shortcut will launch.
        arguments (list): A list of arguments to be passed to the target file or application.
        hotkey (str): Hotkey for opening the lnk file. Defaults to ''.
        working_dir (Union[str, None], optional): The working directory for the target file or application. Defaults to None (Working dict of shortcut_path).
        minimized_maximized_normal_invisible (str, optional): The window state of the target application when launched. Can be "minimized", "maximized", or "invisible". Defaults to "minimized".
        silentlog (Union[str, None], optional): The path to a log file for the target application when minimized_maximized_normal_invisible == "invisible". Defaults to None.
        asadmin (bool, optional): Whether to run the shortcut as an administrator. Defaults to False.

    Returns:
        str: The JavaScript content used to create the shortcut.

    Raises:
        OSError: If the secretsubprocess.exe file is not found and minimized_maximized_normal_invisible == "invisible".

    """
    wco = 4

    secadir = os.path.normpath(os.path.dirname(__file__))
    seca = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "secretsubprocess.exe")
    )

    if minimized_maximized_normal_invisible == "minimized":
        wco = 7
    elif minimized_maximized_normal_invisible == "maximized":
        wco = 0
    elif minimized_maximized_normal_invisible == "invisible":
        wco = 4

        if not os.path.exists(seca):
            inp=input("Secretsubprocess.exe not found! Do you want to compile the code now? [Y/n]")
            if inp.strip().lower() == 'y':
                folderp = os.path.dirname(__file__)
                secpa = os.path.join(folderp, r"secretsubprocess.py")
                wholecommand = compile_with_nuitka(
                    pyfile=secpa,
                    icon=None,
                    disable_console=True,
                    file_version="0.1",
                    onefile=True,
                    outputdir=None,
                    addfiles=[],
                    delete_onefile_temp=True,  # creates a permanent cache folder
                    needs_admin=True,
                    relativefolderinapps=None
                )

            else:
                sys.exit(1)
            while not os.path.exists(seca):
                sleep(.1)

    shortcut_path2 = pathlib.Path(shortcut_path)
    shortcut_path2.parent.mkdir(parents=True, exist_ok=True)
    if working_dir == "None":
        working_dir = None
    if not working_dir:
        working_dir = os.path.normpath(os.path.dirname(target))
    working_dir = escapepa(working_dir)
    shortcut_path = escapepa(shortcut_path)
    target = escapepa(target)

    if not minimized_maximized_normal_invisible == "invisible":
        arguments = " ".join(escapeargu(arguments))
        js_content = f"""
            var sh = WScript.CreateObject("WScript.Shell");
            var shortcut = sh.CreateShortcut("{shortcut_path}");
            shortcut.WindowStyle = {wco};
            shortcut.TargetPath = "{target}";
            shortcut.Hotkey = "{hotkey}";
            shortcut.Arguments = "{arguments}";
            shortcut.WorkingDirectory = "{working_dir}";
            shortcut.IconLocation = "{target}";
            shortcut.Save();"""
    else:
        if silentlog == "None":
            silentlog = None
        if silentlog:
            silentlog = os.path.normpath(silentlog)
            addsi = ["--log", escapepa(silentlog)]
        else:
            addsi = []

        if not arguments:
            arguments = ''
        if isinstance(arguments,list):
            arguments =  ' '.join(arguments)

        argulist = subprocess.list2cmdline(
            ["--exe", escapepa(os.path.normpath(target)), *addsi]
        )
        if isinstance(arguments,list):
            arguments=' '.join(arguments)

        argulist = argulist +" --args "+ arguments
        secaesc = escapeargu(seca)[0]
        js_content = f"""
            var sh = WScript.CreateObject("WScript.Shell");
            var shortcut = sh.CreateShortcut("{shortcut_path}");
            shortcut.WindowStyle = {wco};
            shortcut.Hotkey = "{hotkey}" ;
            shortcut.TargetPath = "{secaesc}";
            shortcut.Arguments = "{argulist}";
            shortcut.WorkingDirectory = "{working_dir.rstrip(os.sep)}";
            shortcut.IconLocation = "{secaesc}";
            shortcut.Save();"""
    print(js_content)
    fd, path = tempfile.mkstemp(".js")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(js_content)

        p = subprocess.Popen(
            [r"wscript.exe", path],
            shell=False,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        p.wait(5)

    finally:
        try:
            os.unlink(path)
        except Exception as fe:
            pass

    if asadmin:
        with open(shortcut_path, "rb") as f:
            ba = bytearray(f.read())
        ba[0x15] = ba[0x15] | 0x20
        with open(shortcut_path, "wb") as f:
            f.write(ba)
    return js_content


def asteval(x):
    try:
        return ast.literal_eval(str(x))
    except Exception:
        return x


def npath(x):
    try:
        return os.path.normpath(str(x))
    except Exception:
        return x


if __name__ == "__main__":
    print(sys.argv)
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=65)
    )
    parser.add_argument(
        "--shortcut_path",
        help=r"""The path where the shortcut file will be created.""",
    )
    parser.add_argument(
        "--target",
        default="",
        help=r"""The path to the target file or application that the shortcut will launch.""",
    )

    parser.add_argument(
        "--hotkey",
        default="",
        help=r"""Hotkey for opening the lnk file. Defaults to ''.""",
    )
    parser.add_argument(
        "--working_dir",
        default="None",
        help=r"""The working directory for the target file or application.  (Working dict of shortcut_path).""",
    )
    parser.add_argument(
        "--mode",
        default="minimized",
        help=r"""The window state of the target application when launched. Can be "normal", "minimized", "maximized", or "invisible".""",
    )
    parser.add_argument(
        "--silentlog",
        default="None",
        help=r"""The path to a log file for the target application when minimized_maximized_normal_invisible == "invisible". """,
    )
    parser.add_argument(
        "--asadmin",
        default="False",
        help=r"""Whether to run the shortcut as an administrator. Defaults to False.""",
    )
    parser.add_argument(
        r"--args",
        default="",
        help=r"""Arguments to be passed to the target file or application as they would receive them. Example: 
        lnkgonewild.exe --shortcut_path C:\Users\hansc\Desktop\testlink.lnk --target C:\cygwin\bin\lsattr.exe --hotkey Ctrl+Alt+q --working_dir None --mode minimized --silentlog None --asadmin False --arguments -a -d""",
    )
    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit(1)
    try:
        argsindex = sys.argv.index("--args")
        args_ = sys.argv[argsindex + 1 :].copy()
        sys.argv = sys.argv[:argsindex]
        args_ = " ".join(args_).strip()
        print(args_)
    except Exception:
        args_ = "[]"

    args = parser.parse_args()
    shortcut_path = npath(asteval(args.shortcut_path))
    target = npath(asteval(args.target))
    arguments = asteval(args_)
    hotkey = asteval(args.hotkey)
    working_dir = npath(asteval(args.working_dir))
    minimized_maximized_normal_invisible = asteval(args.mode)
    silentlog = npath(asteval(args.silentlog))
    asadmin = asteval(args.asadmin)
    create_shortcut(
        shortcut_path=shortcut_path,
        target=target,
        arguments=arguments,
        minimized_maximized_normal_invisible=minimized_maximized_normal_invisible,  #
        silentlog=silentlog,  # stdout can be written to file if the process is invisible
        asadmin=asadmin,  # enables the admin check box
        hotkey=hotkey,
        working_dir=working_dir,
    )


