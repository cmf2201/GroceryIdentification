#!/usr/bin/env python
# coding: utf-8

# In[2]:


shopping_list = {
    "Apples": 0,
    "Bananas": 0,
    "Chicken": 0,
    "Milk": 0,
    "Eggs": 0,
    "Bread": 0,
    "Carrots": 0
}


# In[ ]:


def add_item():
    item_name = input("Enter item name: ").lower()  
    valid_items = list(shopping_list.keys())
    for valid_item in valid_items:
        if item_name in valid_item.lower() or valid_item.lower() in item_name:
            quantity = int(input("Enter quantity: "))
            shopping_list[valid_item] += quantity
            print(f"{quantity} {valid_item} added to the list.")
            return
    print("Item not found in the list.")

def modify_quantity():
    item_name = input("Enter item name to modify: ")
    if item_name in shopping_list:
        new_quantity = int(input("Enter new quantity: "))
        shopping_list[item_name] = new_quantity
        print(f"Quantity of {item_name} updated to {new_quantity}.")
    else:
        print(f"{item_name} not found in the list.")

def remove_item():
    item_name = input("Enter item name to remove: ")
    if item_name in shopping_list:
        del shopping_list[item_name]
        print(f"{item_name} removed from the list.")
    else:
        print(f"{item_name} not found in the list.")

def list_status():
    print("Your shopping list:")
    for item, quantity in shopping_list.items():
        print(f"- {quantity} {item}")

essential_items = ["Milk", "Eggs", "Bread"]

def check_for_alerts():
    for item in essential_items:
        if item not in shopping_list:
            print(f"Warning: You haven't added {item} to your list.")

while True:
    print("\nShopping List Menu:")
    print("1. Add Item")
    print("2. Modify Quantity")
    print("3. Remove Item")
    print("4. List Status")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_item()
    elif choice == '2':
        modify_quantity()
    elif choice == '3':
        remove_item()
    elif choice == '4':
        list_status()
    elif choice == '5':
        print("Thanks for using our application!")
        break
    else:
        print("Invalid choice. Please try again.")


# In[ ]:


def add_item(item_name, quantity):
    item_name = item_name.lower()
    if item_name in shopping_list:
        shopping_list[item_name] += quantity
        print(f"{quantity} {item_name} added to the list.")
    else:
        print(f"Item not found in the list.")

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

def check_for_alerts():
    for item in essential_items:
        if item not in shopping_list:
            print(f"Warning: You haven't added {item} to your list.")

essential_items = ["milk", "eggs", "bread"]

while True:
    shopping_list = {
        "Apples": 0,
        "Bananas": 0,
        "Chicken": 0,
        "Milk": 0,
        "Eggs": 0,
        "Bread": 0,
        "Carrots": 0
    }

    print("\nShopping List Menu:")
    print("1. Add Item")
    print("2. Modify Quantity")
    print("3. Remove Item")
    print("4. List Status")
    print("5. Exit")

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
        check_for_alerts()
    elif choice == '5':
        print("Thanks for using our application!")
        break
    else:
        print("Invalid choice. Please try again.")


# In[1]:


shopping_list = {
    "Apples": 0,
    "Bananas": 0,
    "Chicken": 0,
    "Milk": 0,
    "Eggs": 0,
    "Bread": 0,
    "Carrots": 0
}


# In[2]:


def add_item(item_name, quantity):
    item_name = item_name.lower()
    if item_name in shopping_list:
        shopping_list[item_name] += quantity
        print(f"{quantity} {item_name} added to the list.")
    else:
        print(f"Item not found in the list.")

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

def check_for_alerts():
    for item in essential_items:
        if item.lower() not in shopping_list:
            print(f"Warning: You haven't added {item} to your list.")

essential_items = ["milk", "eggs", "bread"]

# Initialize shopping list outside of the loop
shopping_list = {
    "apples": 0,
    "bananas": 0,
    "chicken": 0,
    "milk": 0,
    "eggs": 0,
    "bread": 0,
    "carrots": 0
}

while True:
    print("\nShopping List Menu:")
    print("1. Add Item")
    print("2. Modify Quantity")
    print("3. Remove Item")
    print("4. List Status")
    print("5. Exit")

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
        check_for_alerts()
    elif choice == '5':
        print("Thanks for using our application!")
        break
    else:
        print("Invalid choice. Please try again.")


# In[ ]:




