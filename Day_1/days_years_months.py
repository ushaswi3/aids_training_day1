def days_yr_months(days):
    yr=d/365
    year=round(yr,2)
    months=d/30
    m=round(months,2)
    message=f"{d} days={year}years & {d} days={m}months"
    print(message)
d=int(input("Enter the no.of days:"))
days_yr_months(d)