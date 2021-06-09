import os
from pathlib import Path
print(os.path.realpath(__file__))
print(os.path.dirname(os.path.realpath(__file__)))
print(Path(os.path.dirname(os.path.realpath(__file__))).joinpath("docs/normalizations"))
FIXTURE_DIR = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("docs/normalizations")
print(Path(FIXTURE_DIR).joinpath("xyz.csv"))
