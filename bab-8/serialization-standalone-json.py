import json

mylist = []

mylist.append('This is a string')
mylist.append(5)
mylist.append(('localhost',5000))

#print list 
print("--- This is original list: ----\n")
print(mylist, "\n\n")

p = json.dumps(mylist)

print("---- This is json list: ----\n")
print(p,"\n\n")


u = json.loads(p)
print("---- This is unjson list: ----\n")
print(u,"\n\n")