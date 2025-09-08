def currentbill_units():
    cnum = input("Consumer number: ")
    cname = input("Consumer name: ")
    pmr = int(input("Enter present month readings: "))
    lmr = int(input("Enter last month readings: "))
    tu = pmr - lmr
    print("Total units:", tu)
    
    if tu <= 50:
        bill = tu * 3.80
    elif tu <= 100:
        bill = (50 * 3.80) + (tu - 50) * 4.20
    elif tu <= 200:
        bill = (50 * 3.80) + (50 * 4.20) + (tu - 100) * 5.10
    elif tu <= 300:
        bill = (50 * 3.80) + (50 * 4.20) + (100 * 5.10) + (tu - 200) * 6.30
    else:  
        bill = (50 * 3.80) + (50 * 4.20) + (100 * 5.10) + (100 * 6.30) + (tu - 300) * 7.50

    print("Current bill:", bill)

    message = f"Customer number: {cnum}, Customer name: {cname}! Your current bill is ₹{bill:.2f}"
    print(message)

currentbill_units()
