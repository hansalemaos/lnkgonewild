# -*- coding: utf-8 -*-

import argparse
import subprocess
import sys
import os


def touch(path: str) -> bool:
    def _fullpath(path):
        return os.path.abspath(os.path.expanduser(path))

    def _mkdir(path):
        path = path.replace("\\", "/")
        if path.find("/") > 0 and not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    def _utime(path):
        try:
            os.utime(path, None)
        except Exception:
            open(path, "a").close()

    def touch_(path):
        if path:
            path = _fullpath(path)
            _mkdir(path)
            _utime(path)

    try:
        touch_(path)
        return True
    except Exception as Fe:
        print(Fe)
        return False


def parse_all_args():
    try:
        argsindex = sys.argv.index("--args")
        args_ = sys.argv[argsindex + 1 :].copy()
        sys.argv = sys.argv[:argsindex]

    except Exception:
        args_ = []

    args = parser.parse_args()
    log = os.path.normpath(str(args.log))

    exe_ = str(args.exe)
    return exe_, args_, log


def start_process(exe_, args_, log):
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    CREATE_NO_WINDOW = 0x08000000
    if "\\" in exe_:
        exe_ = f'"{exe_}"'
    cmdline = f'{exe_} {" ".join(args_)}'
    print(cmdline)
    p = subprocess.Popen(
        cmdline,
        shell=False,
        startupinfo=si,
        creationflags=CREATE_NO_WINDOW,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(log)
    if log != "None":
        touch(log)
        with open(log, mode="ab") as f:
            for line in iter(p.stdout.readline, b""):
                f.write(line)
    try:
        p.communicate()
    except Exception:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=28)
    )
    parser.add_argument(
        "--log",
        default="None",
        help="Captures STDOUT, if None, nothing will be captured",
    )
    parser.add_argument(
        "--exe",
        help="Path to the executable",
    )
    parser.add_argument(
        "--args",
        default="noargs",
        help=R"""Arguments to be passed to the exe file
        Needs to be the last argument in the command line, like: "... --exe C:\cygwin\bin\ls.exe --log c:\LOGFILE.txt --args -la". If "noargs", nothing will be passed to the executable """,
    )

    exe_, args_, log = parse_all_args()
    start_process(exe_, args_, log)
