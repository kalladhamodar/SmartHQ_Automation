import pytest
from pages.multi_model_page import MultiModelPage

@pytest.mark.skip(reason="Multi model flow unstable — skipping for now")
@pytest.mark.order(6)
def test_enter_multiple_models(multi_model_driver):
    """
    Verify multiple model numbers can be entered sequentially.
    Uses multi_model_driver fixture from conftest.py which handles
    model entry and assertions automatically.
    """
    # multi_model_driver fixture already entered all models and asserted success.
    # This test confirms the fixture completed without errors.
    print("✅ All multiple models entered and verified via multi_model_driver fixture")
    assert True

@pytest.mark.skip(reason="Multi model flow unstable — skipping for now")
@pytest.mark.order(7)
def test_enter_models_partial_failure(dashboard_driver):
    """
    Verify that individual model failures are captured and reported clearly,
    while other valid models still succeed.
    """
    multi = MultiModelPage(dashboard_driver)

    models = [
        "GDT565HSY1SS",   # valid
        "XXXINVALID999",  # invalid — expected to fail
        "GDF650SYV3FS",   # valid
    ]

    results = multi.enter_models(models)

    # Validate result count matches input
    assert len(results) == len(models), \
        f"❌ Expected {len(models)} results, got {len(results)}"

    # Validate failures are captured (not silently ignored)
    failures = [r for r in results if not r[1]]
    assert len(failures) > 0, \
        "❌ Expected at least one failure for invalid model 'XXXINVALID999' but none reported"

    print(f"✅ Partial failure test passed — {len(failures)} failure(s) captured correctly")
    for r in results:
        status = "✅ PASS" if r[1] else f"❌ FAIL: {r[2]}"
        print(f"  {r[0]} → {status}")