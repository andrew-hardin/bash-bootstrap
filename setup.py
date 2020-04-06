#!/usr/bin/env python3
#
# Welcome to your bash bootstrap module. This was written because
# you're always touching new machines and you wanted to setup
# a consistent environment.
#
# Please note that the environment is versioned, and you can upgrade
# to a newer version if modifications are made.
import os
import shutil
import subprocess

# Configure globals.
REPO_ROOT = os.path.dirname(os.path.realpath(__file__))
MODULE_PATH = os.path.join(REPO_ROOT, "modules")
DOWNLOAD_MODULE_PATH = os.path.join(REPO_ROOT, "downloads")
GIT_PATH = shutil.which("git")
assert GIT_PATH is not None, "Missing the git command"
USER_HOME = os.path.expanduser("~")
BOOTSTRAP_NAME = ".bash_bootstrap"
INSTALL_ROOT = os.path.join(USER_HOME, BOOTSTRAP_NAME)
SYMLINK_NAME = "current"
SYMLINK_PATH = os.path.join(INSTALL_ROOT, SYMLINK_NAME)
BASHRC_NAME = ".bashrc"
BASHRC_PATH = os.path.join(USER_HOME, BASHRC_NAME)
    
def version():
  """ Get the bootstrap version - just the short git hash."""
  os.chdir(REPO_ROOT)
  cmd = [GIT_PATH, "rev-parse", "--verify", "--short", "HEAD"]
  short = subprocess.check_output(cmd)
  short = short.decode("utf-8").strip()
  return short


def init():
  """ Initialize the versioned directory that contains modules. """

  # Setup root directory.
  os.makedirs(INSTALL_ROOT, exist_ok=True)

  # Remove the current symlink if it exists already.
  if os.path.exists(SYMLINK_PATH):
    os.remove(SYMLINK_PATH)

  # Setup the symlink to be relative - makes it easier to change
  # home directory locations...
  v = version()
  os.chdir(INSTALL_ROOT)
  os.symlink(v, SYMLINK_NAME)

  # Copy every module into the directory.
  versioned_path = os.path.join(INSTALL_ROOT, v)
  if os.path.exists(versioned_path):
    os.rmtree(versioned_path)
  shutil.copytree(MODULE_PATH, versioned_path)

  # Execute each of the dynamic modules. There's no prescription for
  # the module format, so we delegate to the os.system module.
  os.chdir(SYMLINK_PATH)
  for _, _, files in os.walk(DOWNLOAD_MODULE_PATH):
    for f in files:
      p = os.path.join(DOWNLOAD_MODULE_PATH, f)
      assert os.system(p) == 0, "Non-zero exit code from %s" % p

def list_modules():
  items = []
  for f in os.listdir(SYMLINK_PATH):
    p = os.path.join(SYMLINK_PATH, f)
    if os.path.isfile(p):
      relative_path = "%s/%s/%s/%s" % ("~", BOOTSTRAP_NAME, SYMLINK_NAME, f)
      priority = f[0:2]
      priority = int(priority) if priority.isdigit() else 99
      items.append((priority, relative_path))

  # Return tuples sorted based on priority.
  items.sort(key=lambda x : x[0])
  return [x[1] for x in items]

def bashrc_sources_modules():
  """ Add source [path] to the bashrc for every module. """

  with open(BASHRC_PATH, "r") as stream:
    lines = stream.readlines()
  START = "# >>> BEGIN AUTOMATIC BASH BOOTSTRAP <<<"
  STOP = "# >>>  END AUTOMATIC BASH BOOTSTRAP  <<<"

  # Check if we have a start or and end tag.
  start_idx = None
  stop_idx = None
  for i, l in enumerate(lines):
    if START in l:
      start_idx = i
    if STOP in l:
      stop_idx = i

  # Remove the sources if they exist already.
  assert (start_idx is None) == (stop_idx is None), "Expected both start/stop tags or neither of them."
  if start_idx is not None:
    lines = lines[0:start_idx] + lines[stop_idx + 1:]
  
  with open(BASHRC_PATH, "w") as stream:
    for l in lines:
      stream.write(l)
    stream.write("\n\n%s\n" % START)
    for path in list_modules():
      stream.write("source %s\n" % path)
    stream.write("%s\n" % STOP)

def does_loginmode_load_bashrc():
  """ Check if one of the login mode init files loads the bashrc. """
  # https://unix.stackexchange.com/questions/320465/new-tmux-sessions-do-not-source-bashrc-file/541352
  candidates = [".bash_profile", ".bash_login", ".profile"]
  candidates = [os.path.join(USER_HOME, x) for x in candidates]
  for p in candidates:
    if os.path.exists(p):
      with open(p) as stream:
        lines = stream.readlines()
        for l in lines:
          if BASHRC_NAME in l:
            return True
  return False


def upgrade():
  assert False, "NOT IMPLEMENTED."

def install():

  # Install fzf.
  os.chdir(SYMLINK_PATH)
  assert os.system("fzf/install --all") == 0, "Non-zero exit code while setting up fzf."

  # Modify the .bashrc file to source all the modules.
  bashrc_sources_modules()
  


if __name__ == "__main__":
  
  is_upgrade = os.path.exists(INSTALL_ROOT)
  init()
  if is_upgrade:
    upgrade()
  else:
    install()

  # Verify that our changes to bashrc will (probably) be loaded.
  if not does_loginmode_load_bashrc():
    sys.stderr.write("The init scripts for bash login mode don't seem to load the .bashrc file.\n")
    sys.stderr.write("Consider adding the following: source ~/.bashrc\n")



