import pytest
from pages.model_number import ModelPage


@pytest.mark.order(5)
def test_model_flow(dashboard_driver):
    """Verify model search, selection and confirmation works correctly."""
    model = ModelPage(dashboard_driver)

    search_text    = "PFW950"
    expected_model = "PFW950SPTDS"

    # Validate edit button is present before clicking
    edit_btn_present = model.is_element_present(model.edit_btn, timeout=15)
    assert edit_btn_present, "❌ Edit (Search your appliance) button not found on dashboard"

    # Run the full model flow
    result = model.scroll_and_select_model(search_text, expected_model)
    assert result is True, \
        f"❌ Model '{expected_model}' was not found or selected from search results"

    # Validate Done button appears after selection
    done_present = model.is_element_present(model.done_btn, timeout=10)
    assert done_present, "❌ Done button not found after model selection"

    model.click_done_btn()
    print(f"✅ Model flow complete — '{expected_model}' selected and confirmed")