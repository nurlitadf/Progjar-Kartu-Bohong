a = [1, 2, 1, 1, 2, 2, 3, 4, 3, 3, 3]
temp = {}

for num in a:
    if num not in temp:
        temp[num] = 0
    temp[num] += 1

print(list(temp.items()))
excess = list(filter(lambda x: x[1] == 4, list(temp.items())))
print(excess)
exc = list(map(lambda x: x[0], excess))
print(exc)

cleaned = list(filter(lambda x: x not in exc, a))
print(cleaned)

counter = [0] * 15
for card in a:
    counter[card] += 1
quad = [i for i, val in enumerate(counter) if val == 4]
print(quad)