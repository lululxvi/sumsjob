import datetime
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".sumsjob"))
import config
from .utils import local_cmdline


def order_by_start(jobs):
    for job in jobs:
        job["Start datetime"] = datetime.datetime.strptime(
            job["Start"], "%m/%d/%Y %I:%M:%S %p"
        )
    return sorted(jobs, key=lambda e: e["Start datetime"])


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
            jobs.append({"Server": m, "JobName": session_name, "Start": creation_time})

    jobs = order_by_start(jobs)
    print("Server   JobName          Start")
    print("-------- ---------------- ----------------------")
    for job in jobs:
        session_name = job["JobName"]
        if len(session_name) > 16:
            session_name = session_name[:15] + "+"
        print(f"{job['Server']:<8} {session_name:<16} {job['Start']}")
    return jobs


def main():
    sacct()


if __name__ == "__main__":
    main()
