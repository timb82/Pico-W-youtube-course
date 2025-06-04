import ujson as json

cal = {
    "red": [255, 0, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "yellow": [255, 255, 0],
    "purple": [128, 0, 128],
    "cyan": [0, 255, 255],
}

with open("data.json", "w") as f:
    json.dump(cal, f)

with open("data.json", "r") as f:
    cal_data = json.load(f)

print(cal_data)
print(type(cal_data))
