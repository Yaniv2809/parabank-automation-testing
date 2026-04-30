import sys
import os

# Fix Windows cp1255 encoding — FixtureForge prints Unicode characters during
# permission evaluation which crashes on non-UTF-8 Windows terminals.
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from fixtureforge import Forge
from pydantic import BaseModel


class RegistrationData(BaseModel):
    first_name: str
    last_name:  str
    address:    str
    city:       str
    state:      str
    zip_code:   str
    phone:      str
    username:   str


def create_forge(seed: int = 42) -> Forge:
    return Forge(use_ai=False, seed=seed, interactive=False)


def generate_users(count: int = 3, seed: int = 42) -> list[RegistrationData]:
    forge = create_forge(seed=seed)
    return forge.create_batch(RegistrationData, count=count)
