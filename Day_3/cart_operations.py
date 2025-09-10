'''You are building a simple E-commerce application in Python. The system should maintain a list of products available in the cart. Write a Python program to perform the following operations using Lists:
1.Add a product to the cart.
2.Remove a product from the cart 
3.Search for a product in the cart 
4.Display all products in the cart
5.Show the total number of products in the cart
 
Cart Operations:
1. Add Product
2. Remove Product
3. Search Product
4. Display Cart
5. Count Products
6. sort items in cart alphabetically
7.clear cart
8.exit
 
Enter choice: 1
Enter product to add: Laptop
Product 'Laptop' added to cart.
 
Enter choice: 1
Enter product to add: Phone
Product 'Phone' added to cart.
 
Enter choice: 4
Cart: ['Laptop', 'Phone']
 
Enter choice: 3
Enter product to search: Phone
Yes, 'Phone' is in the cart.
 
Enter choice: 5
Total products in cart: 2'''


def add_product(cart):
    product=input("Enter product to add: ")
    cart.append(product)
    print("Product ",product," added to cart")

def remove_product(cart):
    product=input("Enter product to remove: ")
    if product in cart:
        cart.remove(product)
        print("Product ",product," removed from cart")
    else:
        print("Product ",product," not found in the cart")

def search_product(cart):
    product=input("Enter product to search: ")
    if product in cart:
        print("Yes ",product," is in the cart")
    else:
        print("Product ",product," not found in the cart")

def display_cart(cart):
    print("Cart: ",cart)

def count_products(cart):
    count=len(cart)
    print("Total products in cart: ",count)

def sort_products(cart):
    cart.sort()
    print("Cart in sorted alphabetically: ",cart)

def clear_cart(cart):
    cart.clear()
    print("Cart cleared")

def cart_operations():
    cart=[]
    while True:
        print("\nCart Operations:")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Search Product")
        print("4. Display Cart")
        print("5. Count Products")
        print("6. Sort Items")
        print("7. Clear Cart")
        print("8. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            add_product(cart)
        elif choice == 2:
            remove_product(cart)
        elif choice == 3:
            search_product(cart)
        elif choice == 4:
            display_cart(cart)
        elif choice == 5:
            count_products(cart)
        elif choice == 6:
            sort_products(cart)
        elif choice == 7:
            clear_cart(cart)
        elif choice == 8:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
cart_operations()







    

    

