#!/usr/bin/env bash
#
# Run this script to clone and run the bash setup.
set -e

# Check prerequisite programs.
which git
which curl
which python3

# Make a temp directory, clone repo, then run the setup.
d=$(mktemp -d)
pushd $d
git clone "git@github.com:andrew-hardin/bash-bootstrap.git" .
./setup.py
popd
rm -rf $d
