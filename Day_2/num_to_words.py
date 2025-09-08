def nums_to_words():
    num = input("Enter a number: ")
    result = ""   
    for digit in num:
        if digit == "0":
            result += "zero "
        elif digit == "1":
            result += "one "
        elif digit == "2":
            result += "two "
        elif digit == "3":
            result += "three "
        elif digit == "4":
            result += "four "
        elif digit == "5":
            result += "five "
        elif digit == "6":
            result += "six "
        elif digit == "7":
            result += "seven "
        elif digit == "8":
            result += "eight "
        elif digit == "9":
            result += "nine "
        else:
            print("Invalid input")
    print("In words:", result)
nums_to_words()
