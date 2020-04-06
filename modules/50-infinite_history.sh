#!/usr/bin/env bash

# Copied from this StackOverflow QA:
# https://stackoverflow.com/questions/9457233/unlimited-bash-history


# Eternal bash history.
# ---------------------
# Undocumented feature which sets the size to "unlimited".
# http://stackoverflow.com/questions/9457233/unlimited-bash-history
export HISTFILESIZE=
export HISTSIZE=
export HISTTIMEFORMAT="[%F %T] "

# Change the file location because certain bash sessions truncate .bash_history file upon close.
# http://superuser.com/questions/575479/bash-history-truncated-to-500-lines-on-each-login
old_hist=$HISTFILE
export HISTFILE=~/.bash_eternal_history

# Migrate the old history into the eternal history file.
# There's no timestamp for the original file, so just insert zeros on every other line.
if [ ! -f "$HISTFILE" ]; then
  if [ -f "$old_hist" ]; then
    mv $old_hist $HISTFILE
    sed -i 's/^/#0\n/' $HISTFILE
  fi
fi

# Force prompt to write history after every command.
# http://superuser.com/questions/20900/bash-history-loss
PROMPT_COMMAND="history -a; $PROMPT_COMMAND"

