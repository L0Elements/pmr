#!/bin/bash

dr="test"


if [ ! -d "$dr" ]; then
    mkdir "$dr"
fi

cd "$dr"

py_args=($(realpath "../pmr.py") "${@}")
python3 -m pdb "${py_args[@]}"
