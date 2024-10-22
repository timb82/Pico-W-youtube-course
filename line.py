x1 = 0
y1 = 5 000 000
x2 = 180
y2 = 25 000 000
# x1 = float(input("x1= "))
# y1 = float(input("y1= "))
# x2 = float(input("x2= "))
# y2 = float(input("y2= "))

a = (y2 - y1) / (x2 - x1)
b = y1 - x1 * a
print(f"y = {a:.32f} x + {b:.32f}")
