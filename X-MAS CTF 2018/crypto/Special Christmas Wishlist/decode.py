#!/usr/bin/python3

from PIL import Image
from string import ascii_lowercase


def search(img, start_x, start_y, need_color, fix_x = False, fix_y = False):
    found = False
    for y in range(start_y, img.height) if not fix_y else [start_y]:
        for x in range(start_x, img.width) if not fix_x else [start_x]:
            color = img.getpixel((x, y)) == 0
            if color and need_color or (not color and not need_color):
                found = True
                break
        if found:
            break
    return (x, y) if found else None


def bfs(img, start_x, start_y):
    queue = [(start_x, start_y)]
    visited = set(queue)
    for x, y in queue:
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            xx, yy = x + dx, y + dy
            if img.getpixel((xx, yy)) > 0:
                continue
            if (xx, yy) not in visited:
                queue.append((xx, yy))
                visited.add((xx, yy))
    return visited


def bounds(letter):
    x, y = zip(*list(letter))
    min_x, min_y = min(x), min(y)
    max_x, max_y = max(x), max(y)
    return (min_x, min_y), (max_x, max_y)


def normalize(letter):
    (min_x, min_y), (max_x, max_y) = bounds(letter)
    normal = set()
    for x, y in letter:
        xx, yy = x - min_x, y - min_y
        normal.add((xx, yy))
    return frozenset(normal)


def draw_letter(letter):
    (min_x, min_y), (max_x, max_y) = bounds(letter)
    img = Image.new('1', (max_x + 1, max_y + 1), 255)
    for x, y in letter:
        img.putpixel((x, y), 0)
    img.show()


def scan(img):
    lines = []
    line_x, line_y = 30, 0
    while True:
        xy = search(img, line_x, line_y, True, fix_x=True)
        if not xy: break
        line = []
        while True:
            xy = search(img, *xy, True, fix_y=True)
            if not xy: break
            letter = bfs(img, *xy)
            line.append(normalize(letter))
            (min_x, min_y), (max_x, max_y) = bounds(letter)
            xy = max_x + 1, min_y + (max_y - min_y) // 2
        lines.append(line)
        line_y = max_y + 30
        print('line {0:2}, length = {1:2}'.format(len(lines) - 1, len(line)))
    return lines


def translate(lines):
    alpha = dict()
    index = 0
    text = ''
    for line in lines:
        for letter in line:
            if letter not in alpha:
                alpha[letter] = ascii_lowercase[index]
                index += 1
            text += alpha[letter]
        text += '\n'
    return text 


def main():
    img = Image.open('wishlist.png').convert('1', dither=False)
    lines = scan(img)
    print('lines count = {}'.format(len(lines)))
    print(translate(lines))


if __name__ == '__main__':
    main()
