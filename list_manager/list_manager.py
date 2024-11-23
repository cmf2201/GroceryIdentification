class ListManager:
    def __init__(self, shopping_list_amounts: list[int]):
        """
        Initializes the List_Manager with the given shopping list amounts.

        Args:
            shopping_list_amounts (list[int]): A list of integers representing the amounts of each item in the shopping list.
                The list should contain exactly 5 elements in the following order:
                [apples, bananas, carrots, onions, oranges]

        Attributes:
            shopping_list (dict): A dictionary with the initial amounts of each item in the shopping list.
            cart_items (dict): A dictionary initialized with zero amounts for each item in the cart.
        """
        self.shopping_list = {'apples' : shopping_list_amounts[0],
                              'bananas' : shopping_list_amounts[1],
                              'carrots' : shopping_list_amounts[2],
                              'onions' : shopping_list_amounts[3],
                              'oranges' : shopping_list_amounts[4]}
        self.cart_items = {'apples' : 0,
                              'bananas' : 0,
                              'carrots' : 0,
                              'onions' : 0,
                              'oranges': 0}
    
    def check_item_name(self, item_name: str):
        item_name = item_name.lower()
        if item_name not in self.shopping_list:
            print("invalid item name")
            return False
        return True

    def add_item_to_list(self, item_name: str, quantity: int):
        if not self.check_item_name(item_name):
            return
        self.shopping_list[item_name] += quantity
        print(f"{quantity} {item_name} added to the list.")

    def remove_item_from_list(self, item_name: str, quantity: int):
        if not self.check_item_name(item_name):
            return
        if self.shopping_list[item_name] >= quantity:
            self.shopping_list[item_name] -= quantity
            print("removed", quantity, "of", item_name, "from shopping list")
        else: print("Cannot remove item from list that is not there")
        
    def add_item_to_cart(self, item_name: str):
        if not self.check_item_name(item_name):
            return
        self.cart_items[item_name] += 1
        print("added", item_name, "to cart")
    
    def remove_item_from_cart(self, item_name: str):
        if not self.check_item_name(item_name):
            return
        if self.cart_items[item_name] >= 1:
            self.cart_items[item_name] -= 1
            print("removed", item_name, "from cart")
        else: print("Cannot remove item from cart that is not there")

    def modify_quantity_of_list(self, item_name, new_quantity):
        if not self.check_item_name(item_name):
            return
        if new_quantity >= 0:
            self.shopping_list[item_name] = new_quantity
            print("modified", item_name, "to have", new_quantity)

    def list_status(self):        
        return self.cart_items, self.shopping_list

### OLD EXAMPLE USAGE ###
# list_manager = ListManager()


# while True:
#     print("\nShopping List Menu:")
#     print("1. Add Item")
#     print("2. Modify Quantity")
#     print("3. Remove Item")
#     print("4. List Status")
#     print("5. Check Cart with ByteTrack")
#     print("6. Exit")

#     choice = input("Enter your choice: ").lower()

#     if choice == '1':
#         item_name = input("Enter item name: ").lower()
#         quantity = int(input("Enter quantity: "))
#         list_manager.add_item(item_name, quantity)
#     elif choice == '2':
#         item_name = input("Enter item name to modify: ").lower()
#         new_quantity = int(input("Enter new quantity: "))
#         list_manager.modify_quantity(item_name, new_quantity)
#     elif choice == '3':
#         item_name = input("Enter item name to remove: ").lower()
#         list_manager.remove_item(item_name)
#     elif choice == '4':
#         list_manager.list_status()
#     elif choice == '5':
#         detected_items = ["milk", "eggs"]  
#         list_manager.check_cart_with_bytetrack(detected_items)
#     elif choice == '6':
#         print("Thanks for using our application!")
#         break
#     else:
#         print("Invalid choice. Please try again.")
