colors = [[10, 10, 10], [20, 20, 20], [30, 30, 30]]


def dim(colors, brightness):
    new_colors = []
    for i in range(len(colors)):
        new_colors.append(
            [int(colors[i][j] * brightness) for j in range(len(colors[i]))]
        )
    return new_colors


cols = dim(colors, 0.1)
print(cols)
# print[colors]
