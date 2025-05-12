#!/usr/bin/kate
# -*- coding: utf-8 -*-
"""
====================================
=== Angio 3D - Add default paths ===
====================================

(C) MKocinski

Kopia na podstawie pliku:
					 mk_add_path_dropbox.py

Created: 23.01.2017
Modified: 2025.04.25

"""
#print(__doc__)

import os
import sys
import platform


if platform.system() == 'Linux':
    if platform.node() == 'mk-prec-7540':
        user = 'marek'
        MK_DROPBOX = os.path.join(os.sep, 'home', user, 'Dropbox')
    MK_ANGIO = os.path.join(os.sep, 'media', user , 'angio')
    MK_ENDO = os.path.join(os.sep, 'media', user, 'endo1')


#MK_DROPBOX_WORK = os.path.join(MK_DROPBOX, 'To_synchro', 'work')
MK_DROPBOX_DANE = os.path.join(MK_DROPBOX_WORK, 'all_data')
#MK_DROPBOX_KODY= os.path.join( MK_DROPBOX, 'To_synchr', 'work', 'all_python')
sys.path.append(MK_DROPBOX_KODY)

MK_ANGIO_DANE = os.path.join(MK_ANGIO, 'dane')

folders = [MK_DROPBOX, MK_DROPBOX_WORK, MK_DROPBOX_DANE, MK_DROPBOX_KODY,
           MK_ANGIO, MK_ENDO, MK_ANGIO_DANE]

paths = []
for p in folders:
    if os.path.exists(p):
        paths.append(p)


if False:
    print("Following paths are added:")
    print("\t%s = %s" % ('MK_DROPBOX', MK_DROPBOX))
    print("\t%s = %s" % ('MK_DROPBOX_WORK', MK_DROPBOX_WORK))
    print("\t%s = %s" % ('MK_DROPBOX_DANE', MK_DROPBOX_DANE))
    print("\t%s = %s" % ('MK_DROPBOX_KODY', MK_DROPBOX_KODY))

    print("\t%s = %s" % ('MK_ANGIO', MK_ANGIO))
    print("\t%s = %s" % ('MK_ENDO', MK_ENDO))
    print("\t%s = %s" % ('MK_ANGIO_DANE', MK_ANGIO_DANE))

__all__ = paths
