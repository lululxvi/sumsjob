import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".sumsjob"))
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
