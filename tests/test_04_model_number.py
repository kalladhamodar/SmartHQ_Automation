import pytest
from pages.model_number import ModelPage


@pytest.mark.order(5)
def test_model_flow(dashboard_driver):
    """Verify model search, selection and confirmation works correctly."""
    model = ModelPage(dashboard_driver)

    search_text    = "PFW950"
    expected_model = "PFW950SPTDS"

    model.complete_model_flow(search_text, expected_model)
    print(f"✅ Model flow complete — '{expected_model}' selected and confirmed")