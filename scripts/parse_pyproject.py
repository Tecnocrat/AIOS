import tomllib
import sys

try:
    with open('pyproject.toml','rb') as f:
        tomllib.load(f)
    print('OK')
except Exception as e:
    print('ERROR', e)
    sys.exit(2)
