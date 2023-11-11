c = open('level1.dash', 'w')
for i in range(25):
    x = ''
    for ii in range(70):
        x+="A"
    c.write(x)
    c.write('\n')
    x = ''