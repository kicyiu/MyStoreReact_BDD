
  @home
  Feature: Home Pages actions

    @TCID-4
    Scenario: User add an item to the cart

      Given I go to 'home' page
      When I press on Add to cart from a random item
      Then the number of items should increase by one in the cart header
