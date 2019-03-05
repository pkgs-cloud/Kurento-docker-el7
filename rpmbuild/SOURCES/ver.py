import platform
import sys

sys.stdout.write (".".join (platform.python_version_tuple ()[:2]))
sys.stdout.write ("\n")
