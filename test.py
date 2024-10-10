# class Test:
#     def __init__(self, value):
#         self.value = value
    
  
#     def set(self, value):
#         self.value = value

#     def get(self):
#         return self.value
    

# t1 = Test(0)
# t2 = Test(0)
# t3 = Test(0)

# test = [t1, t2, t3]
# l = [1,2,3]

# for tup in zip(test, l):
#     print(tup[0].get(),tup[1])

led = 'R G B'.split()
vals = [1,2,3]
for l,z in zip(led, vals):
    print(l,z)

