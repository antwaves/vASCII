with open("log.txt") as f:
    a = f.readlines()

with open("base.txt") as f:
    c = f.readlines()

c.pop(0)
b = []
for line in c:
    if line != "\\\n":
        b.append(line)

print(len(a), len(b))

diffs = []
for i in range(len(a)):
    al = a[i]
    bl = b[i]

    if al != bl:
        diffs.append([al, bl])

with open("blah.txt", 'a') as f:
    for things in diffs:
        f.write(things[0])
        f.write(things[1])