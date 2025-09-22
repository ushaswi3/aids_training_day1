'''Online Library Management System (with Supabase/Postgres + Python):
Build a command-line application in Python that connects to a Supabase Postgres database and performs all 
database operations as they happen in real life:
Register students/members.
Add/update/remove books.
Borrow/return books (transaction).
Generate reports (like overdue, most borrowed books).
🗄️ Database Schema (create in Supabase → SQL Editor)
-- Students / Members
CREATE TABLE members (
    member_id serial PRIMARY KEY,
    name text NOT NULL,
    email text UNIQUE NOT NULL,
    join_date timestamptz DEFAULT NOW()
);
 
-- Books
CREATE TABLE books (
    book_id serial PRIMARY KEY,
    title text NOT NULL,
    author text NOT NULL,
    category text,
    stock int NOT NULL DEFAULT 1
);
 
-- Transactions (Borrow/Return)
CREATE TABLE borrow_records (
    record_id serial PRIMARY KEY,
    member_id int REFERENCES members(member_id),
    book_id int REFERENCES books(book_id),
    borrow_date timestamptz DEFAULT NOW(),
    return_date timestamptz
); 
 
1. Create (Insert)
Register new members (add_member(name, email)).
Add new books (add_book(title, author, category, stock)).
2. Read (Select)
List all books with availability.
Search books by title/author/category.
Show member details and their borrowed books.
3. Update
Update book stock (e.g., when more copies are purchased).
Update member info (e.g., change email).
4. Delete
Delete a member (only if no borrowed books).
Delete a book (only if not borrowed).
 
'''



import os
from supabase import create_client, Client #pip install supabase
from dotenv import load_dotenv # pip install python-dotenv
 
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

class Create:
    def add_member(self,n,e):
        mem={"name":n,"email":e}
        resp=sb.table("members").insert(mem).execute()
        return resp.data

    def add_book(self,t,a,c,s):
        book={"title":t,"author":a,"category":c,"stock":s}
        resp=sb.table("books").insert(book).execute()
        return resp.data

class Select:
    def allbook_ava(self):
        resp=sb.table("books").select("*").execute()
        return resp.data

    def search_book(self, ref, name):
        if ref == 'T':
            resp = sb.table("books").select("*").eq("title", name).execute()
        elif ref == 'A':
            resp = sb.table("books").select("*").eq("author", name).execute()
        elif ref == 'C':
            resp = sb.table("books").select("*").eq("category", name).execute()
        else:
            return {"error": "Invalid reference"}
        return resp.data


    def mem_details_b(self,mem_id):
        bresp=sb.table("borrow_records").select("*").eq("member_id",mem_id).execute()
        mresp=sb.table("members").select("*").eq("member_id",mem_id).execute()
        return bresp.data,mresp.data

class Update:
    def book_stock(self,book_id,new_stock):
        resp=sb.table("books").update({"stock":new_stock}).eq("book_id",book_id).execute()
        return resp

    def mem_email(self,mem_id,new_email):
        resp=sb.table("members").update({"email":new_email}).eq("member_id",mem_id).execute()
        return resp

class Borrowing():
    def check(self):
        resp=sb.table("borrow_records").select("*").execute()
        return resp.data

class Delete:
    def del_mem(self, mem_id):
        sb.table("borrow_records").delete().eq("member_id", mem_id).execute()
        resp = sb.table("members").delete().eq("member_id", mem_id).execute()
        return resp.data

    def del_book(self, book_id):
        sb.table("borrow_records").delete().eq("book_id", book_id).execute()
        resp = sb.table("books").delete().eq("book_id", book_id).execute()
        return resp.data

if __name__ == "__main__":
    bow=Borrowing()
    while(True):
        print("1.Create or Add\n2.Select or Read\n3.Update or Modify\n4.Delete or Remove\n5.Exit")
        ch=int(input("Enter choice = "))

        if(ch==1):
            cre=Create()
            print("1.Add member\n2.Add book")
            ch1=int(input("Enter choice = "))
            if(ch1==1):
                name=input("enter name of member = ").strip()
                email=input("enter email of member = ").strip()
                res=cre.add_member(name,email)
                print(res)
            elif(ch1==2):
                title=input("enter the name of book = ").strip()
                author=input("enter the author name = ").strip()
                category=input("enter the category = ").strip()
                stock=int(input("enter the stock = ").strip())
                res=cre.add_book(title,author,category,stock)
                print(res)
                

        elif(ch==2):
            sel=Select()
            print("1.List all books with availability\n2.Search books by title/author/category\n3.Show member details and their borrowed books.")
            ch1=int(input("Enter choice = "))
            if(ch1==1):
                res=sel.allbook_ava()
                print(res)
            elif(ch1==2):
                ref=input("enter title (T)/ author (A)/ category (C) : ")
                name=input("enter name of reference : ")
                res=sel.search_book(ref,name)
                print(res)
            elif(ch1==3):
                mem_id = int(input("enter member id : "))
                resb, resm = sel.mem_details_b(mem_id)
                if not resm:
                    print("No member found with ID", mem_id)
                else:
                    member = resm[0]  # one record
                    print("\nMember Details:")
                    print("ID:", member['member_id'])
                    print("Name:", member['name'])
                    print("Email:", member['email'])
                if resb:
                    print("\n Borrowed Books:")
                    for b in resb:
                        print("Record ID:", b['record_id'],"Book ID:", b['book_id'],"Borrow Date:", b['borrow_date'],"Return Date:", b['return_date'])
                else:
                    print("\n This member has no borrowed books.")

        elif(ch==3):
            up=Update()
            print("1.update member email\n2.update book stock")
            ch1=int(input("Enter choice = "))
            if(ch1==1):
                mem_id=int(input("enter id of member = ").strip())
                email=input("enter new email of member = ").strip()
                res=up.mem_email(mem_id,email)
                print(res)
            elif(ch1==2):
                book_id=int(input("enter the id of book = ").strip())
                stock=int(input("enter the new stock = ").strip())
                res=up.book_stock(book_id,stock)
                print(res)
            
        elif(ch==4):
            dele = Delete()
            print("1.delete member\n2.delete book (only if no borrowing are there)")
            ch1 = int(input("Enter choice = "))
            if ch1 == 1:
                mem_id = int(input("enter id of member = ").strip())
                found = False
                for i in bow.check():
                    check_idl, check_returndate = i['member_id'],i['return_date']
                    if mem_id == check_idl and check_returndate is None:
                        found = True
                        break
                if not found:
                    res = dele.del_mem(mem_id)
                    print(res)
                else:
                    print("Cannot delete member, they still have borrowed books.")
    
            elif ch1==2:
                book_id = int(input("enter the id of book = ").strip())
                found = False
                for i in bow.check():
                    check_idl, check_returndate = i['book_id'],i['return_date']
                    if book_id == check_idl and check_returndate is None:
                        found = True
                        break
                if not found:
                    res = dele.del_book(book_id)
                    print(res)
                else:
                    print("Cannot delete book, they still have borrowed books.")
            
        else:
            print("Exitting program")
            break