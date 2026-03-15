from pytest_bdd import scenarios, given, when, then, parsers
from pages.bug_tracker_page import BugTrackerPage

scenarios("../features/bug_tracker.feature")

@given("the bug tracker app is open")
def open_app(driver, base_url):
    BugTrackerPage(driver, base_url).open()

@when(parsers.parse('I add a bug with title "{title}" and severity "{severity}"'))
def add_bug(driver, base_url, title, severity):
    BugTrackerPage(driver, base_url).add_bug(title=title, severity=severity)

@then(parsers.parse('I should see a bug titled "{title}" in the list'))
def should_see_bug(driver, base_url, title):
    page = BugTrackerPage(driver, base_url)
    page.refresh()
    assert page.find_row_by_title(title) is not None

@given(parsers.parse('I add a bug with title "{title}" and severity "{severity}"'))
def given_add_bug(driver, base_url, title, severity):
    BugTrackerPage(driver, base_url).add_bug(title=title, severity=severity)

@when(parsers.parse('I set status of bug titled "{title}" to "{status}"'))
def set_status(driver, base_url, title, status):
    BugTrackerPage(driver, base_url).set_status_by_title(title, status)

@then(parsers.parse('the status of bug titled "{title}" should be "{status}"'))
def verify_status(driver, base_url, title, status):
    assert BugTrackerPage(driver, base_url).get_status_by_title(title) == status

@when(parsers.parse('I delete bug titled "{title}"'))
def delete_bug(driver, base_url, title):
    BugTrackerPage(driver, base_url).delete_by_title(title)

@then(parsers.parse('I should not see a bug titled "{title}" in the list'))
def should_not_see_bug(driver, base_url, title):
    BugTrackerPage(driver, base_url).refresh()
    assert BugTrackerPage(driver, base_url).find_row_by_title(title) is None