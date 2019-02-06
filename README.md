# Sums<sub>Job</sub>

Sums<sub>Job</sub> (**S**imple **U**tility for **M**ultiple-**S**ervers **Job** **Sub**mission) is a simple Linux command-line utility which submits a job to one of the multiple servers each with limited resources. It will first look for servers with available resources, such as GPUs, and then run the job in that server interactively just as the job is running in your local machine.

## Features

- Simple to use: one single `submit` command is all your need
- Automatically choose available GPUs among all the servers
- Display the output of the job in real time
- Kill the job by Ctrl-C
- Save the output in a log file
- Transfer back the files you specified

## Usage

### Configuration

Read the comments in [config.py](config.py), and modify the values to your configurations.

### `$ gpuresource`

Show the status of GPUs on all servers.

### `$ submit jobfile jobname`

- `jobfile` : File to be run
- `jobname` : Job name, and also the folder name of the job

Options:

- `-h`, `--help` : Show this help message and exit
- `-i`, `--interact` : Submit as an interactive job
- `-s SERVER`, `--server SERVER` : Server host name
- `--gpuid GPUID` : GPU ID to be used

## Installation

- Install [gpustat](https://github.com/wookayin/gpustat) in each server
- Clone or download this package to the location you like, e.g., `/opt/sumsjob`
- [Configuration](#Configuration)
- Run the following commands to make it executable(use `sudo` if needed)

```
chmod +x /opt/sumsjob/gpuresource.py
chmod +x /opt/sumsjob/submit.py
```

- Add Sums<sub>Job</sub> to your `$PATH`

```
echo 'PATH="/opt/sumsjob:$PATH"' >> ~/.profile
source ~/.profile
```


## License

[GNU GPLv3](LICENSE)