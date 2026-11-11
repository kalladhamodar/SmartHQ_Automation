import os

from appium.options.android import UiAutomator2Options
from appium import webdriver

def get_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = os.getenv("ANDROID_PLATFORM_VERSION", "12")
    options.device_name = os.getenv("ANDROID_DEVICE_NAME", "RZ8N921LQRB")
    options.automation_name = "UiAutomator2"
    options.app_package = "com.smarthqpro.service.field"
    options.app_activity = "com.smarthqpro.service.MainActivity"
    app_path = os.getenv("ANDROID_APP_PATH")
    if app_path:
        options.app = app_path

    return webdriver.Remote("http://localhost:4723", options=options)