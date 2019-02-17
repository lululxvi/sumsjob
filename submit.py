#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import subprocess

import config
from gpuresource import gpu_available


def submit(machine, gpuid, jobpy, jobname, interact):
    runpath = os.path.join(config.path_prefix, jobname)

    if config.LAN is not None:
        cmd = "rsync -avhP {} ./ {}:{}".format(config.files_push, config.LAN, runpath)
    else:
        cmd = "rsync -avhP {} ./ {}:{}".format(config.files_push, machine, runpath)
    print(cmd)
    subprocess.check_call(cmd, shell=True)

    if interact:
        cmd = "ssh -tX {} 'cd {} && CUDA_VISIBLE_DEVICES={} {} {} |& tee {}.log'".format(
            machine, runpath, gpuid, config.cmd, jobpy, jobname
        )
        if config.LAN is not None:
            cmd = '''ssh -tX {} "{}"'''.format(config.LAN, cmd)
        print(cmd)
        subprocess.check_call(cmd, shell=True)

        if config.LAN is not None:
            cmd = "rsync -avhP {} {}:{}/ .".format(
                config.files_pull, config.LAN, runpath
            )
        else:
            cmd = "rsync -avhP {} {}:{}/ .".format(config.files_pull, machine, runpath)
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    else:
        print("Does not support non-interactive job yet.")


def main():
    parser = argparse.ArgumentParser(description="Submit a job to (GPU) servers.")
    parser.add_argument("jobfile", help="File to be run")
    parser.add_argument("jobname", help="Job name, and also the folder name of the job")
    parser.add_argument(
        "-i", "--interact", action="store_true", help="Submit as an interactive job"
    )
    parser.add_argument("-s", "--server", help="Server host name")
    parser.add_argument("--gpuid", help="GPU ID to be used; -1 to use CPU only")
    args = parser.parse_args()

    machine, gpuid = args.server, args.gpuid
    if machine is None:
        machine, gpuid = gpu_available()
    else:
        if gpuid == "-1":
            print("Server: %s, CPU" % machine)
            gpuid = ""
        else:
            print("Server: %s, gpuid: %s" % (machine, gpuid))
    if machine is None:
        return
    submit(machine, gpuid, args.jobfile, args.jobname, args.interact)


if __name__ == "__main__":
    main()
