#!/usr/bin/env bash
OUT=70-git-prompt.bash
curl -L https://github.com/git/git/raw/master/contrib/completion/git-prompt.sh -o $OUT
chmod +x $OUT