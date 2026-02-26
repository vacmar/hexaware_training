from datetime import datetime
#import pytz - python 3.8 and below
import zoneinfo  # python 3.9 and above
 
# Define timezones
ist = zoneinfo.ZoneInfo("Asia/Kolkata") #indian standard time
utc = zoneinfo.ZoneInfo("UTC")                         #coordinated universal time utc+0
ny  = zoneinfo.ZoneInfo("America/New_York") #coordinated universal time utc-5
 
# Current time in IST
now_ist = datetime.now(ist)
print(now_ist.strftime("%Y-%m-%d %H:%M:%S %Z"))   # 2026-02-23 14:35:22 IST
 
# Convert IST to UTC
now_utc = now_ist.astimezone(utc)
print(now_utc.strftime("%Y-%m-%d %H:%M:%S %Z"))   # 2026-02-23 09:05:22 UTC
 
# Convert IST to New York
now_ny = now_ist.astimezone(ny)
print(now_ny.strftime("%Y-%m-%d %H:%M:%S %Z"))    # 2026-02-23 03:35:22 EST