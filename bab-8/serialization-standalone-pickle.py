import pickle

mylist = []

mylist.append('This is a string')
mylist.append(5)
mylist.append(('localhost',5000))

#print list 
print("--- This is original list: ----\n")
print(mylist, "\n\n")

p = pickle.dumps(mylist)

print("---- This is pickled list: ----\n")
print(p,"\n\n")


u = pickle.loads(p)
print("---- This is unpickled list: ----\n")
print(u,"\n\n")