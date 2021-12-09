import argparse
import os
import pickle
import random
import time
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".sumsjob"))
import config
from .gpuresource import gpu_available


def get_machine(machine, gpuid, verbose=0):
    if machine is None:
        machine, gpuid = gpu_available(first_only=True, verbose=verbose)
    else:
        if gpuid == "-1":
            if verbose == 1:
                print("Server: %s, CPU" % machine)
            gpuid = ""
        else:
            if verbose == 1:
                print("Server: %s, gpuid: %s" % (machine, gpuid))
    return machine, gpuid


def push_files(src, machine, dest, options="", verbose=0):
    if verbose == 2:
        options = "-avhP " + options
    else:
        options = "-a " + options
    if config.LAN is not None:
        cmd = "rsync {} {} {}:{}".format(options, src, config.LAN, dest)
    else:
        cmd = "rsync {} {} {}:{}".format(options, src, machine, dest)
    if verbose == 2:
        print(cmd)
    subprocess.check_call(cmd, shell=True)


def pull_files(machine, runpath, verbose=0):
    if verbose == 2:
        options = "-avhP " + config.files_pull
    else:
        options = "-a " + config.files_pull
    if config.LAN is not None:
        cmd = "rsync {} {}:{}/ .".format(options, config.LAN, runpath)
    else:
        cmd = "rsync {} {}:{}/ .".format(options, machine, runpath)
    if verbose == 2:
        print(cmd)
    subprocess.check_call(cmd, shell=True)


def submit_one(
    jobpy,
    jobname=None,
    machine=None,
    gpuid=None,
    interact=True,
    inobj=None,
    infile="in.pickle",
    verbose=0,
):
    machine, gpuid = get_machine(machine, gpuid, verbose=verbose)
    if machine is None:
        return

    if jobname is None:
        jobname = "%d_%04x" % (time.time(), random.randint(0, int("ffff", 16)))
    runpath = os.path.join(config.path_prefix, jobname)

    push_files("./", machine, runpath, options=config.files_push, verbose=verbose)

    if inobj is not None:
        tmpfile = "/tmp/sumsjob." + jobname
        with open(tmpfile, "wb") as f:
            pickle.dump(inobj, f)
        push_files(tmpfile, machine, os.path.join(runpath, infile), verbose=verbose)
        subprocess.check_call(["rm", "-f", tmpfile])
    sys.stdout.flush()

    if interact:
        cmd = "ssh -tX {} 'cd {} && CUDA_VISIBLE_DEVICES={} {} {} 2>&1 | tee {}.log'".format(
            machine, runpath, gpuid, config.cmd, jobpy, jobname
        )
        if config.LAN is not None:
            cmd = '''ssh -tX {} "{}"'''.format(config.LAN, cmd)
        if verbose == 2:
            print(cmd)
        subprocess.check_call(cmd, shell=True)
        pull_files(machine, runpath, verbose=verbose)
    else:
        raise NotImplementedError("Does not support non-interactive job yet.")
    return runpath


def submit(
    jobpy,
    jobname=None,
    machine=None,
    gpuid=None,
    interact=True,
    inobj=None,
    infile="in.pickle",
    retry_num=1,
    retry_period=0,
    verbose=0,
):
    for _ in range(retry_num - 1):
        try:
            return submit_one(
                jobpy,
                jobname=jobname,
                machine=machine,
                gpuid=gpuid,
                interact=interact,
                inobj=inobj,
                infile=infile,
                verbose=verbose,
            )
        except subprocess.CalledProcessError:
            if verbose > 0:
                print("Failed to submit. Wait for %d s..." % retry_period)
                sys.stdout.flush()
            time.sleep(retry_period)
    return submit_one(
        jobpy,
        jobname=jobname,
        machine=machine,
        gpuid=gpuid,
        interact=interact,
        inobj=inobj,
        infile=infile,
        verbose=verbose,
    )


def main():
    parser = argparse.ArgumentParser(description="Submit a job to (GPU) servers.")
    parser.add_argument("jobfile", help="File to be run")
    parser.add_argument(
        "jobname",
        nargs="?",
        help="Job name, and also the folder name of the job. If not provided, a random number will be used.",
    )
    # parser.add_argument(
    #     "-i", "--interact", action="store_true", help="Submit as an interactive job"
    # )
    parser.add_argument("-s", "--server", help="Server host name")
    parser.add_argument("--gpuid", help="GPU ID to be used; -1 to use CPU only")
    args = parser.parse_args()

    submit(
        args.jobfile,
        jobname=args.jobname,
        machine=args.server,
        gpuid=args.gpuid,
        interact=True,  # args.interact,
        verbose=2,
    )


if __name__ == "__main__":
    main()
