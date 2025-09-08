def count_notes():
    a = int(input("Enter the amount: "))
    notes = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
    print("Note Count:")
    for note in notes:
        if a>=note:
            count=a//note   
            a=a % note        
            print(note,":",count)
count_notes()
