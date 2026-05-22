from appium.options.android import UiAutomator2Options
from appium import webdriver

def get_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "12"
    options.device_name = "RZ8N921LQRB"
    options.automation_name = "UiAutomator2"
    options.app_package = "com.smarthqpro.service.field"
    options.app_activity = "com.smarthqpro.service.MainActivity"

    return webdriver.Remote("http://localhost:4723", options=options)