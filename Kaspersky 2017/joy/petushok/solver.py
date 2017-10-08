css = '.Co{background-color: #000;}'

with open('ctfcoco.html', 'r') as f:
    data = f.read()

part1 = data[:data.index('.CoCo54901')]
part2 = data[data.index('</style>'):]

with open('result.html','w') as f:
    f.write(part1 + css + part2)