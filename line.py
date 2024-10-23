y1 = 0
x1 = 500_000
y2 = 180
x2 = 2_500_000
# x1 = float(input("x1= "))
# y1 = float(input("y1= "))
# x2 = float(input("x2= "))
# y2 = float(input("y2= "))

a = (y2 - y1) / (x2 - x1)
b = y1 - x1 * a
print(f"y = {a:.32f} x + {b:.32f}")
print(f"dy/dx = {y2-y1:,f}/{x2-x1:,f}")
