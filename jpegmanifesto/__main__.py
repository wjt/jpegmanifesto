#!/usr/bin/env python3

import argparse
import os
import random
import tempfile
import uuid

def load_gnu():
    path = os.path.join(os.path.dirname(__file__), 'corpora', 'gnu.txt')
    with open(path, encoding='utf-8') as gnu_txt:
        return list(line.strip().encode('utf-8') for line in gnu_txt if line.strip())

def mangle(jpeg_lines, gnus, prob):
    jpeg_lines = jpeg_lines.copy()
    trials = len(jpeg_lines) - 2
    skipped = 0
    # TODO: probably need to skip the header more carefully
    for i in range(5, trials):
        r = random.random()
        if r < prob:
            print('transpose', i)
            jpeg_lines[i], jpeg_lines[i+1] = jpeg_lines[i+1], jpeg_lines[i]
        elif r < 2 * prob:
            print('insert', i)
            jpeg_lines.insert(i, random.choice(gnus))
        elif r < 3 * prob:
            print('replace', i)
            jpeg_lines[i] = random.choice(gnus)
        else:
            # Allow rest to pass through unmodified
            skipped += 1

    print('skipped', skipped, '/', trials)
    return jpeg_lines


def transform(jpeg, count, target_dir, prob):
    gnus = load_gnu()
    with open(jpeg, 'rb') as jpeg_f:
        jpeg_lines = jpeg_f.read().split(b'\n')

    base, ext = os.path.splitext(os.path.basename(jpeg))
    for _ in range(count):
        target = os.path.join(target_dir, '{}-{}{}'.format(base, uuid.uuid4(), ext))
        print(jpeg, '->', target)
        mangled = mangle(jpeg_lines, gnus, prob)        
        with open(target, 'wb') as mangled_f:
            mangled_f.write(b'\n'.join(mangled))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('jpeg', metavar='JPEG')
    parser.add_argument('--count', type=int, default=100)
    parser.add_argument('--target-dir', type=str)
    parser.add_argument('--prob', type=float, default=0.005)
    args = parser.parse_args()
    target_dir = args.target_dir
    if target_dir:
        os.makedirs(target_dir, exist_ok=True)
    else:
        target_dir = tempfile.mkdtemp(prefix='jpegmanifesto-')

    transform(args.jpeg, args.count, target_dir, args.prob)

if __name__ == '__main__':
    main()
