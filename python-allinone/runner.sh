#!/bin/bash
# Program: runner.sh
# Purpose: Start Jupyter notebook
# Syntax:  runner.sh jupyter
# Author:  Ray Lai
# Updated: Aug 10, 2017
# License: MIT
#
set -e

case "$1" in
  "")
    bash
    ;;
  jupyter)
    jupyter notebook --no-browser --ip='*' --allow-root
    ;;
  *)
    $@
    ;;
esac

exit 0
