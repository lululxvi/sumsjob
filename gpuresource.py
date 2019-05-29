#!/usr/bin/env python

from __future__ import print_function

import subprocess
import sys

import config


def exclude_gpus(lines):
    if config.gpus_exclude:
        lines = [
            l for l in lines if all(map(lambda gpu: gpu not in l, config.gpus_exclude))
        ]
    return lines


def gpustat(machine, stat):
    lines = stat.split("\n")
    lines = exclude_gpus(lines)
    avail = None
    for l in lines:
        if l != "" and l.split("|")[-1] == "":
            avail = int(l[1])
    return machine, "\n".join(lines), avail


def gpuresource():
    for m in config.servers:
        cmd = "ssh {} 'gpustat -cup'".format(m)
        if config.LAN is not None:
            cmd = '''ssh {} "{}"'''.format(config.LAN, cmd)
        stat = subprocess.check_output(cmd, shell=True)
        if sys.version_info >= (3, 0):
            stat = stat.decode("utf-8")
        yield gpustat(m, stat)


def gpu_available(first_only=False):
    gm, gavail = None, None
    for m, stat, avail in gpuresource():
        print(stat)
        if gavail is None and avail is not None:
            gm, gavail = m, avail
            if first_only:
                break
    if gm is None:
        print("No available GPU.")
        return None, None
    else:
        print("Available GPU: {} [{}]\n".format(gm, gavail))
        return gm, gavail


def main():
    gpu_available()


if __name__ == "__main__":
    main()
