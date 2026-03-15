from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


class BugTrackerPage:
    TITLE_INPUT = (By.CSS_SELECTOR, '[data-testid="bug-title-input"]')
    SEVERITY_SELECT = (By.CSS_SELECTOR, '[data-testid="severity-select"]')
    STATUS_SELECT = (By.CSS_SELECTOR, '[data-testid="status-select"]')
    ADD_BTN = (By.CSS_SELECTOR, '[data-testid="add-bug"]')
    REFRESH_BTN = (By.CSS_SELECTOR, '[data-testid="refresh"]')
    BUG_ROWS = (By.CSS_SELECTOR, '[data-testid="bug-row"]')

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.REFRESH_BTN)
        )

    def refresh(self):
        self.driver.find_element(*self.REFRESH_BTN).click()

    def add_bug(self, title: str, severity: str, status: str = "Open"):
        title_el = self.driver.find_element(*self.TITLE_INPUT)
        title_el.clear()
        title_el.send_keys(title)

        Select(self.driver.find_element(*self.SEVERITY_SELECT)).select_by_visible_text(severity)
        Select(self.driver.find_element(*self.STATUS_SELECT)).select_by_visible_text(status)

        self.driver.find_element(*self.ADD_BTN).click()

        # Wait until the new row appears (UI refresh happens after POST)
        WebDriverWait(self.driver, 10).until(lambda d: self.find_row_by_title(title) is not None)

    def _all_rows(self):
        # Always fetch fresh elements from DOM
        return self.driver.find_elements(*self.BUG_ROWS)

    def find_row_by_title(self, title: str, timeout: int = 10):
        """
        Find a row by title, with retry to handle DOM refresh (stale elements).
        Returns a WebElement row, or None if not found within timeout.
        """
        def _finder(_driver):
            for row in self._all_rows():
                try:
                    t = row.find_element(By.CSS_SELECTOR, '[data-testid="bug-title"]').text.strip()
                    if t == title:
                        return row
                except StaleElementReferenceException:
                    # DOM changed mid-iteration; retry by returning None (WebDriverWait will try again)
                    return None
            return None

        try:
            return WebDriverWait(self.driver, timeout).until(_finder)
        except TimeoutException:
            return None

    def set_status_by_title(self, title: str, status: str):
        row = self.find_row_by_title(title)
        assert row is not None, f"Bug with title '{title}' not found"

        sel = Select(row.find_element(By.CSS_SELECTOR, '[data-testid="bug-status"]'))
        sel.select_by_visible_text(status)

        # Wait until selection is reflected (protects against re-render)
        WebDriverWait(self.driver, 10).until(lambda d: self.get_status_by_title(title) == status)

    def get_status_by_title(self, title: str) -> str:
        row = self.find_row_by_title(title)
        assert row is not None, f"Bug with title '{title}' not found"

        sel = Select(row.find_element(By.CSS_SELECTOR, '[data-testid="bug-status"]'))
        return sel.first_selected_option.text.strip()

    def delete_by_title(self, title: str):
        row = self.find_row_by_title(title)
        assert row is not None, f"Bug with title '{title}' not found"

        row.find_element(By.CSS_SELECTOR, '[data-testid="delete-bug"]').click()
        WebDriverWait(self.driver, 10).until(lambda d: self.find_row_by_title(title) is None)