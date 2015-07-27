#!/bin/bash

if [[ $(grep -q "download_series" ~/.bashrc; echo $?) -eq 1 ]]; then
    echo "updating path"
    echo "export PATH=$PATH:$(pwd)" >> ~/.bashrc
else
    echo "path already updated"
fi
