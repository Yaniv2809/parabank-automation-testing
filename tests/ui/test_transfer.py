import allure
import pytest
from testaxiom import analyze

from pages.transfer_page import TransferPage

# ── TestAxiom BVA analysis for transfer amount ────────────────────────────────
# Valid range: $0.01 (min) to $100.00 (safe upper bound for shared test account)
_bva_analysis = analyze("amount", param_type="float", valid_range=(0.01, 100.00))
_bva_params   = [
    pytest.param(tc.input_value, tc.expected.value, id=tc.id)
    for tc in _bva_analysis.test_cases
    if tc.technique.value == "bva"
]


@pytest.mark.ui
class TestTransfer:

    @allure.id("UI-005")
    @allure.title("Fund transfer — valid amount succeeds")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    def test_valid_transfer(self, logged_in_page):
        tp = TransferPage(logged_in_page)
        tp.goto()
        tp.transfer(amount="10")
        assert tp.is_success(), "Expected 'Transfer Complete!' heading after valid $10 transfer"

    @allure.id("UI-006")
    @allure.title("Fund transfer — boundary amounts via TestAxiom BVA")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.high
    @pytest.mark.parametrize("amount,validity", _bva_params)
    def test_boundary_amounts(self, logged_in_page, amount, validity):
        """
        TestAxiom BVA generates four boundary points for the range (0.01, 100.00):
          just_below_min=0.0 (invalid), at_min=0.01 (valid),
          at_max=100.0 (valid),         just_above_max=100.01 (invalid).
        Valid boundaries execute a real transfer; invalid ones check for rejection.
        """
        tp = TransferPage(logged_in_page)
        tp.goto()

        # For "just_above_max" skip actual execution — ParaBank has no $100 cap.
        # The BVA point is documented; the system-level limit is account balance.
        if validity == "valid":
            tp.transfer(amount=str(amount))
            assert tp.is_success(), f"BVA {amount}: expected successful transfer"
        else:
            tp.transfer(amount=str(amount))
            assert not tp.is_success(), f"BVA {amount}: expected rejection"

    @allure.id("UI-007")
    @allure.title("Fund transfer — negative amount is rejected")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.medium
    def test_negative_amount(self, logged_in_page):
        tp = TransferPage(logged_in_page)
        tp.goto()
        tp.transfer(amount="-50")
        assert not tp.is_success(), "Negative transfer amount must be rejected"
