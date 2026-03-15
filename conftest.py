import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import allure
from allure_commons.types import AttachmentType
from config.logger import get_logger
logger = get_logger("conftest")

# Always load .env from the project root (same folder as this conftest.py)
PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=False)


def pytest_addoption(parser):
    parser.addoption("--headless", action="store", default=None, help="true/false")
    parser.addoption("--base-url", action="store", default=None, help="Base URL override")
    parser.addoption("--api-base-url", action="store", default=None, help="API base URL override")


@pytest.fixture(scope="session")
def base_url(request):
    # UI base url: CLI overrides .env, which overrides default
    return (
        request.config.getoption("--base-url")
        or os.getenv("BASE_URL")
        or "https://duckduckgo.com/"
    )


@pytest.fixture(scope="session")
def api_base_url(request):
    # API base url: used in API tests
    return (
        request.config.getoption("--api-base-url")
        or os.getenv("API_BASE_URL")
        or "http://127.0.0.1:5000"
    )


@pytest.fixture
def driver(request):
    headless_opt = request.config.getoption("--headless")
    if headless_opt is None:
        headless = os.getenv("HEADLESS", "false").lower() == "true"
    else:
        headless = str(headless_opt).lower() == "true"

    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1400,900")
    logger.info("Launching Chrome | headless=%s", headless)

    # Helpful for local HTML file + calling localhost APIs
    options.add_argument("--allow-file-access-from-files")
    options.add_argument("--disable-web-security")

    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)

    yield drv
    logger.info("Closing browser")
    drv.quit()

#Screenshot code for failed tests
import datetime
from pathlib import Path


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # only act after the test call (not setup/teardown)
    if rep.when != "call" or not rep.failed:
        return

    # Get driver reliably (pytest-bdd sometimes doesn't keep it in item.funcargs)
    driver = None
    try:
        driver = item.funcargs.get("driver")
    except Exception:
        driver = None

    if driver is None:
        try:
            driver = item._request.getfixturevalue("driver")
        except Exception:
            return  # no UI driver in this test, so no screenshot

    screenshots_dir = Path("reports") / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = screenshots_dir / f"{item.name}_{ts}.png"

    try:
        # 1) save screenshot to disk
        driver.save_screenshot(str(file_path))

        # 2) attach to Allure
        allure.attach.file(
            str(file_path),
            name=f"screenshot_{item.name}",
            attachment_type=AttachmentType.PNG
        )
    except Exception:
        pass