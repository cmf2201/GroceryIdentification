# Existing shopping list and essential items
shopping_list = {
    "milk": 1,
    "bread": 2
}

essential_items = ["milk", "eggs", "bread"]

# Core shopping list functions
def add_item(item_name, quantity):
    item_name = item_name.lower()
    if item_name in shopping_list:
        shopping_list[item_name] += quantity
        print(f"{quantity} {item_name} added to the list.")
    else:
        shopping_list[item_name] = quantity
        print(f"{item_name} added to the list with quantity {quantity}.")

def modify_quantity(item_name, new_quantity):
    item_name = item_name.lower()
    if item_name in shopping_list:
        shopping_list[item_name] = new_quantity
        print(f"Quantity of {item_name} updated to {new_quantity}.")
    else:
        print(f"{item_name} not found in the list.")

def remove_item(item_name):
    item_name = item_name.lower()
    if item_name in shopping_list:
        del shopping_list[item_name]
        print(f"{item_name} removed from the list.")
    else:
        print(f"{item_name} not found in the list.")

def list_status():
    print("Your shopping list:")
    for item, quantity in shopping_list.items():
        print(f"- {quantity} {item}")

# New function to check detected items
def check_cart_with_bytetrack(detected_items):
    detected_set = set(item.lower() for item in detected_items)
    
    # Check if essential items are missing from the shopping list
    for item in essential_items:
        if item.lower() not in shopping_list:
            print(f"Warning: You haven't added {item} to your list.")
            if item.lower() in detected_set:
                add_choice = input(f"{item} is detected in your cart but missing from the list. Do you want to add it? (yes/no): ").lower()
                if add_choice == 'yes':
                    add_item(item, 1)  # Default quantity of 1 if not specified

    # Check if items in shopping list are missing from detected items
    for item in shopping_list:
        if item.lower() not in detected_set:
            print(f"Alert: {item} is in your shopping list but not detected in your cart.")

# Example usage within the menu
while True:
    print("\nShopping List Menu:")
    print("1. Add Item")
    print("2. Modify Quantity")
    print("3. Remove Item")
    print("4. List Status")
    print("5. Check Cart with ByteTrack")
    print("6. Exit")

    choice = input("Enter your choice: ").lower()

    if choice == '1':
        item_name = input("Enter item name: ").lower()
        quantity = int(input("Enter quantity: "))
        add_item(item_name, quantity)
    elif choice == '2':
        item_name = input("Enter item name to modify: ").lower()
        new_quantity = int(input("Enter new quantity: "))
        modify_quantity(item_name, new_quantity)
    elif choice == '3':
        item_name = input("Enter item name to remove: ").lower()
        remove_item(item_name)
    elif choice == '4':
        list_status()
    elif choice == '5':
        # Simulate ByteTrack detection
        detected_items = ["milk", "eggs"]  # Replace with ByteTrack output
        check_cart_with_bytetrack(detected_items)
    elif choice == '6':
        print("Thanks for using our application!")
        break
    else:
        print("Invalid choice. Please try again.")
