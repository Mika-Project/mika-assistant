import os
import subprocess

######################################
# Install requirements automatically #
######################################

def install_dependencies():
    if os.path.exists("installed-dependencies.txt"):
        with open("installed-dependencies.txt", "r") as file:
            content = file.read().strip()
            print(content)
            if content == "true":
                print("Dependencies are already installed.")
                return

    if os.name == 'posix':
        dependencies_script = 'install-requirements.sh'
        try:
            subprocess.run(['sh', dependencies_script], check=True)
            with open("installed-dependencies.txt", "w") as file:
                file.write("true")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script: {e}")
    elif os.name == 'nt':
        dependencies_script = '.\\install-requirements.bat'
        try:
            subprocess.run([dependencies_script], check=True)
            with open("installed-dependencies.txt", "w") as file:
                file.write("true")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script: {e}")
    else:
        print("Your OS is not found")