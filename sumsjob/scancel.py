__al__ = ["scancel"]

import argparse
import subprocess

from .sacct import sacct
from .utils import local_cmdline


def scancel(jobname):
    jobs = sacct()
    for job in jobs:
        if job["JobName"] == jobname:
            cmd = f"screen -S sumsjob-{jobname} -X quit"
            cmd = local_cmdline(job["Server"], cmd, verbose=0)
            subprocess.run(cmd, shell=True, check=True)
            print(f"Job {jobname} on {job['Server']} cancelled.")
            return
    print(f"Job {jobname} not found.")


def main():
    parser = argparse.ArgumentParser(description="Cancel a running job.")
    parser.add_argument("jobname", help="Job name")
    args = parser.parse_args()

    scancel(args.jobname)


if __name__ == "__main__":
    main()
