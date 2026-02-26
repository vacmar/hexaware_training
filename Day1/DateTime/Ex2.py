#String to datetime conversion
from datetime import datetime
 
date_str = "2024-06-15"
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
print("String to datetime:", date_obj)
 
dt2 = datetime.strptime("23/02/2026", "%d/%m/%Y")
print("String to datetime:", dt2)
dt3 = datetime.strptime("February 23, 2026 14:30", "%B %d, %Y %H:%M")
print("String to datetime:", dt3)
 