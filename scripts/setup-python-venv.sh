#!/usr/bin/env bash

set -e
# download miniconda.sh
if [[ `uname -s` == "Darwin" ]]; then
    wget "https://repo.continuum.io/miniconda/Miniconda3-4.7.10-MacOSX-x86_64.sh" -O "miniconda.sh"
else
    wget "https://repo.continuum.io/miniconda/Miniconda3-4.7.10-Linux-x86_64.sh" -O "miniconda.sh"
fi

# add the execution permission
chmod +x miniconda.sh

# create python virtual environment
./miniconda.sh -b -p venv

# activate the conda python virtual environment
source venv/bin/activate