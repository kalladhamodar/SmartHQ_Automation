import pytest
from pages.model_number import ModelPage


class MultiModelPage:

    def __init__(self, driver):
        self.driver = driver
        self.model_page = ModelPage(driver)

    def enter_models(self, models):
        """
        Sequentially enter each model number using edit button flow.
        Returns a list of tuples:
          (model, True)          — on success
          (model, False, error)  — on failure
        """
        assert models and len(models) > 0, \
            "❌ Models list is empty — provide at least one model number"

        results = []
        for m in models:
            assert isinstance(m, str) and m.strip() != "", \
                f"❌ Invalid model number provided: '{m}'"
            try:
                self.model_page.enter_or_update_model(m)
                results.append((m, True))
                print(f"✅ Model entered successfully: {m}")
            except Exception as e:
                results.append((m, False, str(e)))
                print(f"❌ Failed to enter model: {m} — {e}")

        return results

    def enter_models_and_assert(self, models):
        """
        Enter all models and assert all succeeded.
        Fails with a clear message listing which models failed.
        """
        results = self.enter_models(models)
        failures = [r for r in results if not r[1]]

        if failures:
            fail_msgs = [f"  • {r[0]}: {r[2]}" for r in failures]
            pytest.fail(
                f"❌ {len(failures)} out of {len(models)} model(s) failed:\n" +
                "\n".join(fail_msgs)
            )

        print(f"✅ All {len(models)} models entered successfully")
        return results