
  @headerAndNavbar
  Feature: Header and NavBar actions

    @TCID-1
    Scenario: User should be redirected to home page when click on page name

      Given I go to 'home' page
      When I click on the page name
      Then I should be redirected to 'home' page

    @TCID-2
    Scenario: User should be redirected to home page when click on Home option in the nav bar

      Given I go to 'home' page
      When I click on 'Home' option on the navbar
      Then I should be redirected to 'home' page

    @TCID-3
    Scenario: Search product should list products base on any text coincidence in the name

      Given I go to 'home' page
      When I type in the search text box
      And Press enter
      Then it should list all the products base on what I type in