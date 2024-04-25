#!/bin/bash

dr="test"


if [ ! -d "$dr" ]; then
    mkdir "$dr"
fi

cd "$dr"

py_args=("-i" $(realpath "../project.py") "${@}")
python3 "${py_args[@]}"
