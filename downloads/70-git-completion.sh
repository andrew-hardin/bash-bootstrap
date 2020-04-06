#!/usr/bin/env bash
OUT=70-git-completion.bash
curl -L https://github.com/git/git/raw/master/contrib/completion/git-completion.bash -o $OUT
chmod +x $OUT