#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plik z funkcjami pomocniczymi, szerokiego, ogolnego zastosowania.

Created on Tue Jun 18 14:17:54 2019
@author: marek

(C) MK & AM

C: 2019.06.18
M: 2019.06.26
"""
import os

all = []

def textWrap(fname = ''):
    """
    C: 2019.06.18
    M: 2019.06.22
    """
    if not len(fname):
        fname=os.path.basename(__file__)
    print()
    p = len(fname) + 8
    print(p * '#')
    print("### %s ###" % fname)
    print(p * '#')
all.append('textWrap')

def imgInfo(img, name='obrazek'):
    print('info o {}: nmin={:.2f}, aver={:.2f},  max={:.2f}, \
shape={},dtype={}'.format(name.upper(), img.min(), img.mean(), img.max(), img.shape, img.dtype))
all.append('imgInfo')


if __name__ == '__main__':
    a = 'ala ma kota'
    textWrap(a)

