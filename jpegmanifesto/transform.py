#!/usr/bin/env python3

import logging
import os
import random

log = logging.getLogger(__name__)

GNU_TXT = os.path.join(os.path.dirname(__file__), 'corpora', 'gnu.txt')
with open(GNU_TXT, encoding='utf-8') as gnu_txt:
    gnus = tuple(
        line.strip().encode('utf-8')
        for line in gnu_txt if line.strip()
    )


class Transformer:
    OPS = ('transpose', 'insert', 'replace')

    def __init__(self, jpeg, prob=0.005):
        self.jpeg_lines = jpeg.read().split(b'\n')
        self.prob = prob

    def mangle(self):
        jpeg_lines = self.jpeg_lines.copy()
        trials = len(jpeg_lines) - 2

        stats = {k: 0 for k in self.OPS}
        skipped = 0

        # TODO: probably need to skip the header more carefully
        for i in range(5, trials):
            r = random.random()
            if r < self.prob:
                log.debug('transpose %d', i)
                stats['transpose'] += 1
                jpeg_lines[i], jpeg_lines[i+1] = jpeg_lines[i+1], jpeg_lines[i]
            elif r < 2 * self.prob:
                log.debug('insert %d', i)
                stats['insert'] += 1
                jpeg_lines.insert(i, random.choice(gnus))
            elif r < 3 * self.prob:
                log.debug('replace %d', i)
                stats['replace'] += 1
                jpeg_lines[i] = random.choice(gnus)
            else:
                # Allow rest to pass through unmodified
                skipped += 1

        log.debug('skipped %d/%d', skipped, trials)
        stats = {k: v / trials for k, v in stats.items()}
        return b'\n'.join(jpeg_lines), stats
