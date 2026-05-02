import time
import uuid
import allure
import pytest

from pages.registration_page import RegistrationPage
from utils.fixture_forge_engine import generate_users


# ── FixtureForge DDT data ─────────────────────────────────────────────────────
# Generated once at collection time; seed=42 → deterministic across runs.
_ff_users = generate_users(count=2, seed=42)

_ddt_params = [
    pytest.param(u, id=f"ff-user-{i+1}")
    for i, u in enumerate(_ff_users)
]


@pytest.mark.ui
@pytest.mark.high
class TestRegistration:

    @allure.id("UI-008")
    @allure.title("New user registration — valid data (DDT via FixtureForge)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("user", _ddt_params)
    def test_register_valid_user(self, page, user):
        """
        FixtureForge (use_ai=False, seed=42) generates realistic registration
        fixtures deterministically.  A timestamp suffix is appended to the
        username to avoid conflicts on the shared public ParaBank instance.
        """
        # Combine a timestamp (seconds) with 12 hex UUID chars to get ~80 bits of
        # uniqueness.  The public ParaBank server retains all registrations across
        # CI runs, so short UUIDs (8 chars / 32 bits) eventually collide.
        unique_username = f"{user.username[:8]}_{int(time.time())}_{uuid.uuid4().hex[:8]}"

        rp = RegistrationPage(page)
        rp.goto()
        rp.register(
            first_name=user.first_name,
            last_name=user.last_name,
            address=user.address,
            city=user.city,
            state=user.state,
            zip_code=user.zip_code,
            phone=user.phone,
            ssn="555-11-9999",
            username=unique_username,
            password="Test1234!",
        )

        assert rp.is_registered(), (
            f"Expected 'Welcome' page after registering '{unique_username}'. "
            f"Error: {rp.get_error()}"
        )
