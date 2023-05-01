
with open ('tcs_telnet.txt', 'r') as log:
    list1=log.read()



with open ('params_test.dat', 'r') as log:
    list2=log.read()

data = {}
for element in list1 + list2:
    date_time = element.split(': ', 0)[2].split(',')[0]
    if date_time not in data:
        data[date_time] = []
    data[date_time].append(element)

joinedlist = []
for date_time in sorted(data.keys()):
    joinedlist.extend(data[date_time])
print(joinedlist)