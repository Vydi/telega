import time
import datetime
print('go')

# time.sleep(2)

print("lol", datetime.datetime.today().time())

print(type(str(datetime.datetime.today().time())))


while True:
    date = str(datetime.datetime.today().time())
    if date[:-7] == "22:20:00":
        print("lol")
        time.sleep(60)
        continue
    elif date[:-7] == "22:21:00":
        print("lol")
        time.sleep(60)
        continue

