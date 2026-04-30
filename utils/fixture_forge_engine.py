import re
import sys
import os

# Fix Windows cp1255 encoding — FixtureForge prints Unicode characters during
# permission evaluation which crashes on non-UTF-8 Windows terminals.
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from fixtureforge import Forge
from pydantic import BaseModel, field_validator


class RegistrationData(BaseModel):
    first_name: str
    last_name:  str
    address:    str
    city:       str
    state:      str
    zip_code:   str
    phone:      str
    username:   str

    @field_validator("zip_code")
    @classmethod
    def clean_zip(cls, v: str) -> str:
        """ParaBank requires a numeric ZIP — strip any non-digit characters."""
        digits = re.sub(r"\D", "", v)
        return digits[:5] if digits else "10001"

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, v: str) -> str:
        """Normalise phone to digits-only so ParaBank accepts it."""
        digits = re.sub(r"\D", "", v)
        return digits[:10] if digits else "5550001234"

    @field_validator("state")
    @classmethod
    def clean_state(cls, v: str) -> str:
        """Ensure state fits in ParaBank's 20-char field."""
        return (v or "NY")[:20]


def create_forge(seed: int = 42) -> Forge:
    return Forge(use_ai=False, seed=seed, interactive=False)


def generate_users(count: int = 3, seed: int = 42) -> list[RegistrationData]:
    forge = create_forge(seed=seed)
    return forge.create_batch(RegistrationData, count=count)
