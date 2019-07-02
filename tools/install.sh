#!/usr/bin/env bash

# Install conda if needed
if ! [[ -x "$(command -v conda)" ]]; then
    echo 'conda is not installed.' >&2

    read -p "Proceed to download and install conda?" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        # Download Anaconda if not present
        if [[ ! -f ~/miniconda.sh ]]; then
            echo "Downloading conda"
            wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
        fi

        bash ~/miniconda.sh
    else
        echo 'Cannot continue without conda installed.'
        exit 1
    fi
fi

# Remove existing environment
conda env remove --yes -n walletexplorer || echo 'Creating new environment'

# Install environment from file
conda env create --force -f environment.yml

# Setting the last git commit hash into the .revision file
git rev-parse HEAD > .revision
