# &Sigma;&Sigma;<sub>Job</sub>

[![PyPI version](https://badge.fury.io/py/SumsJob.svg)](https://badge.fury.io/py/SumsJob)
[![Downloads](https://pepy.tech/badge/sumsjob)](https://pepy.tech/project/sumsjob)
[![License](https://img.shields.io/github/license/lululxvi/sumsjob)](https://github.com/lululxvi/sumsjob/blob/master/LICENSE)

&Sigma;&Sigma;<sub>Job</sub> or Sums<sub>Job</sub> (**S**imple **U**tility for **M**ultiple-**S**ervers **Job** **Sub**mission) is a simple Linux command-line utility which submits a job to one of the multiple servers each with limited GPUs. &Sigma;&Sigma;<sub>Job</sub> provides similar key functions for multiple servers as [Slurm Workload Manager](https://slurm.schedmd.com) for supercomputers and computer clusters. It provides the following key functions:

- show the status of GPUs on all servers,
- submit a job to servers in noninteractive mode, i.e., the job will be running in the background of the server,
- submit a job to servers in interactive mode, just as the job is running in your local machine,
- display all running jobs,
- cancel running jobs.

## Motivation

Assume you have a few GPU servers: `server1`, `server2`, ... When you need to run a code from your computer, you will

1. Select one server and log in

       $ ssh LAN (You may need to first log in a local area network)
       $ ssh server1

1. Check GPU status. If no free GPU, go to step 1

   `$ nvidia-smi` or `$ gpustat`

1. Copy the code from your computer to the server

       $ scp -r codes server1:~/project/codes

1. Run the code in the server

       $ cd ~/project/codes
       $ CUDA_VISIBLE_DEVICES=0 python main.py

1. Transfer back the results

       $ scp server1:~/project/codes/results.dat .

These steps are boring. &Sigma;&Sigma;<sub>Job</sub> makes all these steps automatic.

## Features

- Simple to use
- Two modes: noninteractive mode, and interactive mode
- Noninteractive mode: the job will be running in the background of the server
    + You can turn off your local machine
- Interactive mode: just as the job is running in your local machine
    + Display the output of the program in the terminal of your local machine in real time
    + Kill the job by Ctrl-C

## Usage

### `$ gpuresource`

Show the status of GPUs on all servers. For example,

![](https://github.com/lululxvi/sumsjob/blob/master/docs/figs/gpuresource.png)

### `$ submit jobfile [jobname]`

Submit a job to GPU servers. Automatically do the following steps:

1. Find a GPU with low utilization and sufficient memory (the criterion is in the configuration file). You can also specify the server and GPU by `-s SERVER` and `--gpuid GPUID`.
1. Copy the code to the server.
1. Run the job on it in noninteractive mode (default) or interactive mode (with `-i`).
1. Save the output in a log file.
1. For interactive mode, when the code finishes, transfer back the result files and the log file.

- `jobfile` : File to be run
- `jobname` : Job name, and also the folder name of the job. If not provided, a random number will be used.

Options:

- `-h`, `--help` : Show this help message and exit
- `-i`, `--interact` : Submit as an interactive job
- `-s SERVER`, `--server SERVER` : Server host name
- `--gpuid GPUID` : GPU ID to be used; -1 to use CPU only

### `$ sacct`

Display all running jobs ordered by the start time. For example,

![](https://github.com/lululxvi/sumsjob/blob/master/docs/figs/sacct.png)

### `$ scancel jobname`

Cancel a running job.

- `jobname` : Job name.

## Installation

Install Sums<sub>Job</sub> with `pip`:

```
$ pip install sumsjob
```

You also need to do the following:

- Make sure you can `ssh` to each server, ideally without typing the password by SSH keys.
- Install [gpustat](https://github.com/wookayin/gpustat) in each server.
- Have a configuration file at `~/.sumsjob/config.py`. Use [config.py](https://github.com/lululxvi/sumsjob/blob/master/sumsjob/config.py) as a template, and modify the values to your configurations.
- Make sure `~/.local/bin` is in your `$PATH`.

Then run `gpuresource` to check if everything works.

## License

[GNU GPLv3](LICENSE)
