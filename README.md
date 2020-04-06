# Bash Bootstrap

This repository contains scripts for bootstrapping my bash
environment. I've never committed to an environment that I push
out across machines, but I'm slightly irritated when I lose
my bash history. The goal here is to setup a bare-bones
bash environment with everything I really want on a new machine.

```bash
bash -c  "$(curl -sLo- https://github.com/andrew-hardin/bash-bootstrap/raw/master/bootstrap.sh)"
```

**Missing Features**
- [ ] Offline install
- [ ] Upgrade path environment revisions