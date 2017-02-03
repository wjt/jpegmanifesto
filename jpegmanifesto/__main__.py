#!/usr/bin/env python3

import argparse
import logging
import os
import tempfile
import uuid

from .transform import Transformer

log = logging.getLogger(__name__)


def transform(jpeg, count, target_dir, prob):
    with open(jpeg, 'rb') as jpeg_f:
        t = Transformer(jpeg_f, prob)

    base, ext = os.path.splitext(os.path.basename(jpeg))
    for _ in range(count):
        target = os.path.join(target_dir,
                              '{}-{}{}'.format(base, uuid.uuid4(), ext))
        log.info('%s → %s', jpeg, target)
        mangled, stats = t.mangle()
        for k, v in stats.items():
            log.info(' %s: %0.2f%%', k, v * 100)
        with open(target, 'wb') as mangled_f:
            mangled_f.write(mangled)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('jpeg', metavar='JPEG')
    parser.add_argument('--count', type=int, default=100)
    parser.add_argument('--target-dir', type=str)
    parser.add_argument('--prob', type=float, default=0.005)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level='DEBUG' if args.debug else 'INFO')

    target_dir = args.target_dir
    if target_dir:
        os.makedirs(target_dir, exist_ok=True)
    else:
        target_dir = tempfile.mkdtemp(prefix='jpegmanifesto-')

    transform(args.jpeg, args.count, target_dir, args.prob)


if __name__ == '__main__':
    main()
