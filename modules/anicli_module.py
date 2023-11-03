import os
import subprocess

######################
# ANIME PLAY COMMAND #
######################

def run_ani_cli(anime):
    # get if the user is using windows or linux
    # if windows, use cmd
    # if linux, use terminal
    platform = os.sys.platform
    try:
        if platform == 'win32':
            command = ['ani-cli', anime]
            subprocess.Popen(['cmd', '/k'] + command)
        else:
            command = ['ani-cli', anime]
            terminal_emulator = os.popen("echo $TERM").read().strip()
            subprocess.Popen([terminal_emulator, '-e'] + command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except print(0):
        print("Error executing the script: {e}")
        return

    return 