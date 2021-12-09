# &Sigma;&Sigma;<sub>Job</sub>

[![PyPI version](https://badge.fury.io/py/SumsJob.svg)](https://badge.fury.io/py/SumsJob)
[![License](https://img.shields.io/github/license/lululxvi/sumsjob)](https://github.com/lululxvi/sumsjob/blob/master/LICENSE)

&Sigma;&Sigma;<sub>Job</sub> or Sums<sub>Job</sub> (**S**imple **U**tility for **M**ultiple-**S**ervers **Job** **Sub**mission) is a simple Linux command-line utility which submits a job to one of the multiple servers each with limited resources. It will first look for servers with available resources, such as GPUs, and then run the job in that server interactively just as the job is running in your local machine.

**Tutorial**: [Slides](https://github.com/lululxvi/sumsjob/blob/master/tutorials/sumsjob.pdf)

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

These steps are boring. &Sigma;&Sigma;<sub>Job</sub> makes these steps automatic.

## Features

- Simple to use: commands `gpuresource` and `submit` are all your need
- Automatically choose available GPUs among all the servers
- interactively: just as the job is running in your local machine
    + Display the output of the job in real time
    + Kill the job by Ctrl-C
    + Save the output in a log file
    + Transfer back the files you specified

## Usage

### `$ gpuresource`

Show the status of GPUs on all servers. For example,

![](https://github.com/lululxvi/sumsjob/blob/master/tutorials/figs/gpuresource.png)

### `$ submit jobfile jobname`

Automatically do the following:

1. Find a server with free GPU
1. Copy the code to the server
1. Run the job on it
1. When the code finishes, transfer back the results

- `jobfile` : File to be run
- `jobname` : Job name, and also the folder name of the job. If not provided, a random number will be used.

Options:

- `-h`, `--help` : Show this help message and exit
- `-s SERVER`, `--server SERVER` : Server host name
- `--gpuid GPUID` : GPU ID to be used; -1 to use CPU only

## Installation

You can install Sums<sub>Job</sub> with `pip`:

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
