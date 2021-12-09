# Host names of servers
servers = ["server1", "server2"]

# In some situations, you may need to first log in a local area network (LAN) to access
# the servers. In this case, provide the host name of LAN.
# None if LAN is not required.
LAN = None

# GPUs to be excluded
# e.g., gpus_exclude = ["Quadro"] to exclude all GPUs whose name contains "Quadro"
# Emply list if no GPUs to be excluded
gpus_exclude = []

# Root folder of the files
# A new folder will be created in this root folder to store your codes.
# For example, if the jobname is "myjob", then the folder is "~/scratch/myjob".
path_prefix = "~/scratch"

# Command to run your job file, i.e., the python path
cmd = "python"

# Options for [rsync](https://linux.die.net/man/1/rsync) to control what files will be
# copied from your computer to the server, and what files will be transferred back from
# the server to your computer.
# Files copied from your computer to the server, i.e., files required to run the job
# By default, all .py files in the current folder, including .py files in the subfolders.
files_push = "--include='[^.]*/' --include='*.py' --exclude='*'"
# Files transferred back from the server to your computer, i.e., new files you need
# By default, all .dat and .log files
files_pull = "--include='*.dat' --include='*.log' --exclude='*'"
