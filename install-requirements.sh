#!/bin/bash

# Set some colors
CNT=$(tput setaf 7)$(tput bold)"["$(tput sgr0)$(tput setaf 6)$(tput bold)NOTE$(tput sgr0)$(tput setaf 7)$(tput bold)"]"$(tput sgr0)
COK=$(tput setaf 7)$(tput bold)"["$(tput sgr0)$(tput setaf 2)$(tput bold)OK$(tput sgr0)$(tput setaf 7)$(tput bold)"]"$(tput sgr0)
CER=$(tput setaf 7)$(tput bold)"["$(tput sgr0)$(tput setaf 1)$(tput bold)ERROR$(tput sgr0)$(tput setaf 7)$(tput bold)"]"$(tput sgr0)
CAT=$(tput setaf 7)$(tput bold)"["$(tput sgr0)$(tput setaf 7)$(tput bold)ATTENTION$(tput sgr0)$(tput setaf 7)$(tput bold)"]"$(tput sgr0)
CWR=$(tput setaf 7)$(tput bold)"["$(tput sgr0)$(tput setaf 5)$(tput bold)WARNING$(tput sgr0)$(tput setaf 7)$(tput bold)"]"$(tput sgr0)
CAC=$(tput setaf 7)$(tput bold)"["$(tput sgr0)$(tput setaf 3)$(tput bold)ACTION$(tput sgr0)$(tput setaf 7)$(tput bold)"]"$(tput sgr0)
CIN=$(tput setaf 7)$(tput bold)"["$(tput sgr0)$(tput setaf 4)$(tput bold)INPUT$(tput sgr0)$(tput setaf 7)$(tput bold)"]"$(tput sgr0)
CDE=$(tput setaf 7)$(tput bold)"["$(tput sgr0)$(tput setaf 7)$(tput bold)DEBUG$(tput sgr0)$(tput setaf 7)$(tput bold)"]"$(tput sgr0)
CPR=$(tput setaf 7)$(tput bold)"["$(tput sgr0)$(tput setaf 7)$(tput bold)PROGRESS$(tput sgr0)$(tput setaf 7)$(tput bold)"]"$(tput sgr0)


echo "##########################################################"
echo "###         SCRIPT TO INSTALL ALL REQUIREMENTS         ###"
echo "###                   LINUX VERSION                    ###"
echo "###                                                    ###"
echo "###           MADE WITH LOVE BY 'Luciousdev'           ###"
echo "###                    luciousdev.nl                   ###"
echo "##########################################################"

log_file="pip-install.log"

# Function to log output to the log file
log() {
    echo -e "$1" | tee -a "$log_file"
}

# Function to handle errors
handle_error() {
    local argument=$1

    if [ $argument == "pip" ]; then
        log "$CER - An error occurred during the pip installation. Try running the script again with the break-system-packages enabled. Exiting..."
        exit 1
    else
        log "$CER - An error occurred. Exiting..."
        exit 1
    fi
}



if [ -f /etc/os-release ]; then
  . /etc/os-release

    # Check the value of the ID variable for Arch-based distributions
    if [[ "$ID" == "arch" || "$ID_LIKE" == *"arch"* ]]; then
        log "$CNT - Detected Arch-based Linux distribution"

        if ! command -v yay &> /dev/null; then
            log "$CAT - yay is not installed. Installing..."
        
            # Install yay using yay's official installation command
            sudo pacman -S --noconfirm yay || handle_error
            log "$COK - successfully installed yay. Continuing with the script."
        fi
        log "$CNT - yay is already installed"

        # Check if Python is installed
        if ! command -v python &> /dev/null; then
            log "$CWR - Python is not installed. Installing Python..."
            yay -S --noconfirm python3 || handle_error
            log "$COK - Python is successfully installed."
        fi

        # Check if Pip is installed
        if ! command -v pip &> /dev/null; then
            log "$CWR - pip is not installed. Installing Pip..."
            yay -S --noconfirm python-pip || handle_error
            log "$COK - pip is successfully installed."
        fi

        # Install packages from requirements.txt using Pip
        if command -v pip &> /dev/null; then
            log "$CWR - Installing Python packages from requirements.txt..."   

            # Ask the user if they want to use the '--break-system-packages' argument
            read -p "Would you like to use the argument '--break-system-packages'? Note: this can cause major issues. [y/n]" arguments

            if [[ $arguments =~ ^[Yy]$ ]]; then
                # Install Python dependencies
                pip install --break-system-packages -r requirements.txt || handle_error
            else 
                # Install Python dependencies
                pip install -r requirements.txt || handle_error "pip"
            fi
        else
            log "$CER - pip installation failed. Please install Pip manually and run 'pip install -r requirements.txt'."
        fi
    elif [[ "$ID" == "debian" || "$ID_LIKE" == *"debian"* ]]; then
        log "$CNT - Detected Debian-based Linux distribution"
        sudo apt-get update
        sudo apt-get install -y python3-pip python3
    fi 
fi

log "$COK - Installation of python, pip and or the needed packages were successfull."
exit 0