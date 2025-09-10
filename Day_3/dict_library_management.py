'''You are building a Library Management System in Python. The system should store books
    in a dictionary where:

Key → Book ID
Value → Book Title

Write a Python program to perform the following operations using Dictionaries:
Add a book to the library (Book ID, Title).
Remove a book using Book ID.
Search for a book by Book ID and display the title.
Update the title of a book (e.g., correction in title).
Display all books in the library.
Count the total number of books in the library.
Check if a book title exists in the library (reverse lookup).
 '''

def library_management():
    library={}

    def add_book():
        book_id=input("Enter Book ID: ")
        title=input("Enter Book Title: ")
        library[book_id]=title
        print(title , ":", book_id)

    def remove_book():
        book_id=input("Enter Book ID to remove: ")
        if book_id in library:
            rem=library.pop(book_id)
            print("Book", rem, "removed.")
        else:
            print("Book ID not found.")

    def search_book():
        book_id=input("Enter Book ID to search: ")
        if book_id in library:
            print("Book found title: ",library[book_id])
        else:
            print("Book ID not found.")

    def update_book():
        book_id=input("Enter Book ID to update: ")
        if book_id in library:
            new_title=input("Enter new title: ")
            library[book_id]=new_title
            print("Book title updated.")
        else:
            print("Book ID not found.")

    def display_books():
        if not library:
            print("Library is empty.")
        else:
            print("Books in Library:")
            for b, t in library.items():
                print(b, "→" ,t)

    def count_books():
        print("Total no.of books:", len(library))

    def check_title():
        title = input("Enter Book Title to check: ")
        if title in library.values():
            print("Yes,",title," exists in the library.")
        else:
            print(title," not found in the library.")

    while True:
        print("Library Management:")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book by ID")
        print("4. Update Book Title")
        print("5. Display All Books")
        print("6. Count Books")
        print("7. Check Book")
        print("8. Exit")

        choice = int(input("Enter choice: "))
        if choice == 1:
            add_book()
        elif choice == 2:
            remove_book()
        elif choice == 3:
            search_book()
        elif choice == 4:
            update_book()
        elif choice == 5:
            display_books()
        elif choice == 6:
            count_books()
        elif choice == 7:
            check_title()
        elif choice == 8:
            print("Exiting Library System.")
            break
        else:
            print("Invalid choice, try again.")
            
library_management()




