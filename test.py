import copy

damier = [[0, 0, 0], [0, 0, 0]]

caribou = copy.deepcopy(damier)

caribou[0][1] = 1

print(damier)
print(caribou)