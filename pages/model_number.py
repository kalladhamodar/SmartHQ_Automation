from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ModelPage(BasePage):

    edit_btn = (AppiumBy.XPATH,
                '//android.widget.ImageView[@content-desc="Search your appliance"]/android.widget.ImageView')
    done_btn    = (AppiumBy.ACCESSIBILITY_ID, "Done")
    model_input = (AppiumBy.XPATH, "//android.widget.EditText")
    model_section = (
        AppiumBy.ACCESSIBILITY_ID,
        "MODEL #\nSERIAL #\nManufacture Date\nInvalid Serial #\nDocumentation Only Mode"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 25)

    # ---------- Validations ----------

    def is_edit_button_present(self):
        """Validate Search/Edit button is present on dashboard."""
        assert self.is_element_present(self.edit_btn, timeout=15), \
            "❌ 'Search your appliance' edit button not found on dashboard"

    def is_model_input_present(self):
        """Wait until model input field is visible after clicking edit."""
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.model_input)
            )
        except Exception:
            assert False, "❌ Model number input field not found after clicking edit"

    def is_done_button_present(self):
        """Validate Done button is present after model selection."""
        assert self.is_element_present(self.done_btn, timeout=10), \
            "❌ Done button not found after model selection"

    # ---------- Actions ----------

    def click_edit_btn(self):
        """Click the edit/search button on dashboard."""
        self.is_edit_button_present()
        edit = self.wait.until(EC.element_to_be_clickable(self.edit_btn))
        edit.click()
        print("✅ Edit button clicked")

    def scroll_and_select_model(self, search_text, expected_model):
        """
        Type search text and select the expected model from suggestions.
        NOTE: call click_edit_btn() before calling this method.
        """
        # Wait for input field to be visible (screen transition after edit click)
        self.is_model_input_present()

        model_input = self.wait.until(EC.element_to_be_clickable(self.model_input))
        model_input.click()
        model_input.clear()
        model_input.send_keys(search_text)
        print(f"Typed: {search_text}")

        # Wait for suggestions to appear
        self.wait.until(
            lambda d: len(d.find_elements(AppiumBy.XPATH, "//android.widget.Button[@content-desc]")) > 0
        )

        buttons = self.driver.find_elements(AppiumBy.XPATH, "//android.widget.Button[@content-desc]")
        assert len(buttons) > 0, \
            f"❌ No suggestions appeared after typing '{search_text}'"

        for btn in buttons:
            value = btn.get_attribute("content-desc")
            if value == expected_model:
                btn.click()
                print(f"✅ Selected: {value}")
                return True

        # Scroll fallback
        try:
            safe_model = expected_model.replace('"', '\\"')
            ui_scrollable = (
                'new UiScrollable(new UiSelector().scrollable(true)).'
                f'scrollIntoView(new UiSelector().description("{safe_model}"))'
            )
            element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_scrollable)
            element.click()
            print(f"✅ Selected after scroll: {expected_model}")
            return True
        except Exception as e:
            raise Exception(f"❌ Model '{expected_model}' not found in suggestions or scroll: {e}")

    def click_done_btn(self):
        """Click the Done button after model selection."""
        self.is_done_button_present()
        done = self.wait.until(EC.element_to_be_clickable(self.done_btn))
        done.click()
        print("✅ Done clicked")

    def complete_model_flow(self, search, expected):
        """Full flow: click edit → search → select model → click done."""
        self.click_edit_btn()
        result = self.scroll_and_select_model(search, expected)
        assert result is True, f"❌ Model '{expected}' was not selected"
        self.click_done_btn()

    def enter_or_update_model(self, model):
        """
        Used by MultiModelPage — clicks edit button, enters model number,
        selects from suggestions, clicks Done, and waits until back on dashboard.
        """
        # Click edit button to open model search
        self.click_edit_btn()

        # Wait for input field after screen transition
        self.is_model_input_present()

        field = self.wait.until(EC.element_to_be_clickable(self.model_input))
        field.click()
        field.clear()
        field.send_keys(model)
        print(f"Typed: {model}")

        # Wait for suggestions to appear
        self.wait.until(
            lambda d: len(d.find_elements(AppiumBy.XPATH, "//android.widget.Button[@content-desc]")) > 0
        )

        buttons = self.driver.find_elements(AppiumBy.XPATH, "//android.widget.Button[@content-desc]")
        assert len(buttons) > 0, f"❌ No suggestions appeared for model: {model}"

        # Select matching suggestion
        matched = False
        for btn in buttons:
            value = btn.get_attribute("content-desc")
            if value == model:
                btn.click()
                print(f"✅ Selected suggestion: {value}")
                matched = True
                break

        # Scroll fallback if not matched in visible list
        if not matched:
            try:
                safe_model = model.replace('"', '\\"')
                ui_scrollable = (
                    'new UiScrollable(new UiSelector().scrollable(true)).'
                    f'scrollIntoView(new UiSelector().description("{safe_model}"))'
                )
                element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_scrollable)
                element.click()
                print(f"✅ Selected after scroll: {model}")
                matched = True
            except Exception as e:
                raise Exception(f"❌ Model '{model}' not found in suggestions or scroll: {e}")

        # Click Done
        self.is_done_button_present()
        self.wait.until(EC.element_to_be_clickable(self.done_btn)).click()
        print(f"✅ Done clicked for model: {model}")

        # Wait until back on dashboard (edit button visible again)
        self.wait.until(EC.presence_of_element_located(self.edit_btn))
        print(f"✅ Model '{model}' entered and confirmed — back on dashboard")