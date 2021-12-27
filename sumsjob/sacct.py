import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".sumsjob"))
import config
from .utils import local_cmdline


def sacct():
    jobs = []
    for m in config.servers:
        cmd = "screen -list"
        cmd = local_cmdline(m, cmd, verbose=0)
        process = subprocess.run(cmd, capture_output=True, shell=True, text=True)

        # Example:
        # There is a screen on:
        #         47065.1640588557_8760   (12/27/2021 02:02:41 AM)        (Detached)
        # 1 Sockets in /run/screen/S-lu.
        # Or
        # No Sockets found in /run/screen/S-lu.
        lines = process.stdout.strip().split("\n")
        lines = filter(lambda l: "Detached" in l, lines)
        if not lines:
            continue

        lines = map(lambda l: l.strip(), lines)
        for l in lines:
            session_name, creation_time = l.split("\t")[:2]
            session_name = session_name.split(".", 1)[1]
            creation_time = creation_time[1:-1]
            jobs.append([m, session_name, creation_time])

    print("Server   JobName          StartTime")
    print("-------- ---------------- ----------------------")
    for m, session_name, creation_time in jobs:
        if len(session_name) > 16:
            session_name = session_name[:15] + "+"
        print(f"{m:<8} {session_name:<16} {creation_time}")
    return jobs


def main():
    sacct()


if __name__ == "__main__":
    main()
