from datetime import datetime

now = datetime.now()

print("Current date and time:", now)
print("Year:", now.year)
print("Month:", now.month)
print("Day:", now.day)
print("Hour:", now.hour)
print("Minute:", now.minute)
print("Second:", now.second)

print('Date Fomatting')
print("Formatted date:", now.strftime("%Y-%m-%d"))
print("Formatted time:", now.strftime("%H:%M:%S"))