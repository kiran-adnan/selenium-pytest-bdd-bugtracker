Feature: Bug Tracker

  @smoke
  Scenario: Create bug from UI
    Given the bug tracker app is open
    When I add a bug with title "Button misaligned" and severity "High"
    Then I should see a bug titled "Button misaligned" in the list

  @smoke
  Scenario: Update bug status and delete
    Given the bug tracker app is open
    And I add a bug with title "Save crashes" and severity "Critical"
    When I set status of bug titled "Save crashes" to "Closed"
    Then the status of bug titled "Save crashes" should be "Closed" 
    #Then the status of bug titled "Save crashes" should be "Open"
    When I delete bug titled "Save crashes"
    Then I should not see a bug titled "Save crashes" in the list