import os
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".sumsjob"))
import config


def local_cmdline(machine, cmd_server, interact=False, verbose=0):
    if interact:
        cmd = f"ssh -tX {machine} '{cmd_server}'"
    else:
        cmd = f"ssh {machine} '{cmd_server}'"
    if config.LAN is not None:
        if interact:
            cmd = 'ssh -tX {} "{}"'.format(config.LAN, cmd)
        else:
            cmd = 'ssh {} "{}"'.format(config.LAN, cmd)
    if verbose == 2:
        print(cmd)
    return cmd
