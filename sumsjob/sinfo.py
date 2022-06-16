__all__ = ["gpu_available"]

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".sumsjob"))
import config
from .utils import local_cmdline


def exclude_gpus(lines):
    if config.gpus_exclude:
        lines = [
            l for l in lines if all(map(lambda gpu: gpu not in l, config.gpus_exclude))
        ]
    return lines


def exclude_process(lines):
    for process in config.sinfo_process_exclude:
        prog = re.compile(" \S+:" + process + "/\S+")
        lines = [prog.sub("", l) for l in lines]
    return lines


def gpustat(machine, stat):
    # Example of stat:
    # chitu                       Fri Dec 31 01:33:24 2021  470.74
    # [0] NVIDIA GeForce RTX 3080 | 70'C,  67 % |  3637 / 10018 MB | shuaim:python3/3589(689M)
    # [1] NVIDIA GeForce RTX 3080 | 66'C,  37 % |  6412 / 10014 MB | shuaim:python3/3589(361M)
    lines = stat.strip().split("\n")
    lines = exclude_gpus(lines)
    lines = exclude_process(lines)
    avail = None
    for l in lines[1:]:
        contents = l.split("|")
        utilization = int(contents[1].split(",", 1)[1].split("%")[0]) / 100
        memory = contents[2].split("/", 1)
        memory_used = int(memory[0])
        memory_total = int(memory[1].split("MB")[0])
        if (
            1 - utilization >= config.gpu_utilization
            and memory_total - memory_used >= config.gpu_memory * 1024
        ):
            avail = int(l[1])
            break
    return machine, "\n".join(lines), avail


def gpuresource():
    for m in config.servers:
        cmd = "gpustat -cup"
        cmd = local_cmdline(m, cmd, verbose=0)
        try:
            stat = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            print("Failed to get the GPU status on {}\n".format(m))
            continue
        if sys.version_info >= (3, 0):
            stat = stat.decode("utf-8")
        yield gpustat(m, stat)


def gpu_available(first_only=False, verbose=0):
    gm, gavail = None, None
    for m, stat, avail in gpuresource():
        if verbose == 2:
            print(stat)
            print("")
        if gavail is None and avail is not None:
            gm, gavail = m, avail
            if first_only:
                break
    if gm is None:
        if verbose > 0:
            print("No available GPU.")
        return None, None
    else:
        if verbose > 0:
            print("Available GPU: {} [{}]\n".format(gm, gavail))
        return gm, gavail


def main():
    gpu_available(verbose=2)


if __name__ == "__main__":
    main()
