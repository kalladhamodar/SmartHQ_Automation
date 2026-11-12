import pytest
from pages.product_features import ProductFeaturesPage


@pytest.mark.order(8)
def test_product_features(model_selected_driver):
    """Verify Product Features on the dashboard after selecting an appliance."""
    pf = ProductFeaturesPage(model_selected_driver)



    # Validate Product Features screen is loaded
    pf.is_product_features_screen_loaded()

    # Manual & Bulletins
    pf.is_manuals_bulletins_displayed()
    print("✅ Manual & Bulletins opened")
    pf.click_back_button()
    print("✅ Returned from Manual & Bulletins")

    # Training Manual
    pf.is_training_manuals_displayed()
    print("✅ Training Manual opened")
    pf.click_back_button()
    print("✅ Returned from Training Manual")

    # Product Overview
    pf.is_product_overview_displayed()
    print("✅ Product Overview opened")
    pf.click_back_button()
    print("✅ Returned from Product Overview")

    # Ethernet Port → Kitchen Appliances
    pf.is_ethernet_port_displayed()
    print("✅ Ethernet Port opened")
    pf.is_kitchen_appliances_displayed()
    print("✅ Kitchen Appliances found and clicked")

    # Dismiss popup
    pf.is_close_button()
    print("✅ Popup closed via Close button")
    pf.is_outside_popup()
    print("✅ Popup dismissed by tapping outside (Scrim)")