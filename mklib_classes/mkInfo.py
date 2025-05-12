#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class to set info structures about a project working directory.

Created on Mon Aug 26 15:51:40 2019
@author: marek

(C) MK & AM

C: 2019.08.26
M: 2019.08.26

v: 0.01
"""
import os


class mkInfo(object):
    """
    C: 2019.08.26
    M: 2019.08.26
    """

    def __init__(self, name='Info about a project', sh=False):
        self.name = name
        self.textWrap(name)
        self.sh = sh
        print()

    # ### DROPBOX
    @property
    def dropboxPth(self):
        return self._dropboxPth

    @dropboxPth.setter
    def dropboxPth(self, folderList):
        self._dropboxPth = os.path.join(*folderList)
        if os.path.exists(self._dropboxPth):
            if self.sh:
                print("dropboxPth ---> Exists")

    # ### WORKINGDIR
    @property
    def MAINDIR(self):
        return self._MAINDIR

    @MAINDIR.setter
    def MAINDIR(self, folderList):
        self._MAINDIR = os.path.join(self.dropboxPth, *folderList)
        if os.path.exists(self._MAINDIR):
            if self.sh:
                print("MAINDIR ---> Exists")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    # ### MODELS
    @property
    def MODELS(self):
        return self._MODELS

    @MODELS.setter
    def MODELS(self, check):
        if check:
            self._MODELS = os.path.join(self.MAINDIR, 'MODELS')
            if os.path.exists(self._MODELS):
                if self.sh:
                    print("MODELS ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'MODELS'))
                print("MODELS ---> CREATED")

    # ### MAT
    @property
    def MAT(self):
        return self._MAT

    @MAT.setter
    def MAT(self, check):
        if check:
            self._MAT = os.path.join(self.MAINDIR, 'MODELS', 'MAT')
            if os.path.exists(self._MAT):
                if self.sh:
                    print("MAT ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'MODELS', 'MAT'))
                print("MAT ---> CREATED")

    # ### PROFILES-FIT
    @property
    def PROFILES_FIT(self):
        return self._PROFILES_FIT

    @PROFILES_FIT.setter
    def PROFILES_FIT(self, check):
        if check:
            self._PROFILES_FIT = os.path.join(self.MAINDIR, 'MODELS', 'PROFILES-FIT')
            if os.path.exists(self._PROFILES_FIT):
                if self.sh:
                    print("PROFILES-FIT ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'MODELS', 'PROFILES-FIT'))
                print("PROFILES-FIT ---> CREATED")

    # ### PROFILES-R
    @property
    def PROFILES_R(self):
        return self._PROFILES_R

    @PROFILES_R.setter
    def PROFILES_R(self, check):
        if check:
            self._PROFILES_R = os.path.join(self.MAINDIR, 'MODELS', 'PROFILES-R')
            if os.path.exists(self._PROFILES_R):
                if self.sh:
                    print("PROFILES-R ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'MODELS', 'PROFILES-R'))
                print("PROFILES-R ---> CREATED")

    # ### RDIST
    @property
    def RDIST(self):
        return self._RDIST

    @RDIST.setter
    def RDIST(self, check):
        if check:
            self._RDIST = os.path.join(self.MAINDIR, 'MODELS', 'RDIST')
            if os.path.exists(self._RDIST):
                if self.sh:
                    print("RDIST ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'MODELS', 'RDIST'))
                print("RDIST ---> CREATED")

    # ### SECTIONS
    @property
    def SECTIONS(self):
        return self._SECTIONS

    @SECTIONS.setter
    def SECTIONS(self, check):
        if check:
            self._SECTIONS = os.path.join(self.MAINDIR, 'MODELS', 'SECTIONS')
            if os.path.exists(self._SECTIONS):
                if self.sh:
                    print("SECTIONS ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'MODELS', 'SECTIONS'))
                print("SECTIONS ---> CREATED")

    # ### STL
    @property
    def STL(self):
        return self._STL

    @STL.setter
    def STL(self, check):
        if check:
            self._STL = os.path.join(self.MAINDIR, 'MODELS', 'STL')
            if os.path.exists(self._STL):
                if self.sh:
                    print("STL ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'MODELS', 'STL'))
                print("STL ---> CREATED")

    # ### CENTERLINES
    @property
    def CENTERLINES(self):
        return self._CENTERLINES

    @CENTERLINES.setter
    def CENTERLINES(self, check):
        if check:
            self._CENTERLINES = os.path.join(self.MAINDIR, 'MODELS', 'CENTERLINES')
            if os.path.exists(self._CENTERLINES):
                if self.sh:
                    print("CENTERLINES ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'MODELS', 'CENTERLINES'))
                print("CENTERLINES ---> CREATED")

    # ### IMG
    @property
    def IMG(self):
        return self._IMG

    @IMG.setter
    def IMG(self, check):
        if check:
            self._IMG = os.path.join(self.MAINDIR, 'IMG')
            if os.path.exists(self._IMG):
                if self.sh:
                    print("IMG ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'IMG'))
                print("IMG ---> CREATED")


    # ### VEF
    @property
    def VEF(self):
        return self._VEF

    @VEF.setter
    def VEF(self, check):
        if check:
            self._VEF = os.path.join(self.MAINDIR, 'VEF')
            if os.path.exists(self._VEF):
                if self.sh:
                    print("VEF ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'VEF'))
                print("VEF ---> CREATED")

    # ### TH
    @property
    def TH(self):
        return self._TH

    @TH.setter
    def TH(self, check):
        if check:
            self._TH = os.path.join(self.MAINDIR, 'TH')
            if os.path.exists(self._TH):
                if self.sh:
                    print("TH ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'TH'))
                print("TH ---> CREATED")

    # ### SKEL
    @property
    def SKEL(self):
        return self._SKEL

    @SKEL.setter
    def SKEL(self, check):
        if check:
            self._SKEL = os.path.join(self.MAINDIR, 'SKEL')
            if os.path.exists(self._SKEL):
                if self.sh:
                    print("SKEL ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'SKEL'))
                print("SKEL ---> CREATED")

    # ### SKELGRAPH
    @property
    def SKELGRAPH(self):
        return self._SKELGRAPH

    @SKELGRAPH.setter
    def SKELGRAPH(self, check):
        if check:
            self._SKELGRAPH = os.path.join(self.MAINDIR, 'SKELGRAPH')
            if os.path.exists(self._SKELGRAPH):
                if self.sh:
                    print("SKELGRAPH ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'SKELGRAPH'))
                print("SKELGRAPH ---> CREATED")

    # ### LABELLED
    @property
    def LABELLED(self):
        return self._LABELLED

    @LABELLED.setter
    def LABELLED(self, check):
        if check:
            self._LABELLED = os.path.join(self.MAINDIR, 'LABELLED')
            if os.path.exists(self._LABELLED):
                if self.sh:
                    print("LABELLED ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'LABELLED'))
                print("LABELLED ---> CREATED")

    # ### LATEX
    @property
    def LATEX(self):
        return self._LATEX

    @LATEX.setter
    def LATEX(self, check):
        if check:
            self._LATEX = os.path.join(self.MAINDIR, 'LATEX')
            if os.path.exists(self._LATEX):
                if self.sh:
                    print("LATEX ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'LATEX'))
                print("LATEX ---> CREATED")

    # ### LATEX / FIGS
    @property
    def LATEX_figs(self):
        return self._LATEX_figs

    @LATEX_figs.setter
    def LATEX_figs(self, check):
        if check:
            self._LATEX_figs = os.path.join(self.MAINDIR, 'LATEX', 'figs')
            if os.path.exists(self.LATEX_figs):
                if self.sh:
                    print("LATEX_figs ---> Exists")
            else:
                os.mkdir(os.path.join(self.MAINDIR, 'LATEX', 'figs'))
                print("LATEX_figs ---> CREATED")

    def setAllWorkingFolders(self):
        if not hasattr(self, 'dropboxPth'):
            print('SET PATH TO DROPBOX AND WORKING DIRECTORY FIRST!!!')
            return
        self.MODELS = True
        self.MAT = True
        self.PROFILES_FIT = True
        self.PROFILES_R = True
        self.RDIST = True
        self.SECTIONS = True
        self.STL = True
        self.CENTERLINES = True
        self.IMG = True
        self.VEF = True
        self.TH = True
        self.SKEL = True
        self.SKELGRAPH = True
        self.LABELLED = True
        self.LATEX = True
        self.LATEX_figs = True




    @staticmethod
    def textWrap(fname = ''):
        """
        C: 2019.06.18
        M: 2019.08.26
        """
        if not len(fname):
            fname=os.path.basename(__file__)
        print()
        p = len(fname) + 8
        print(p * '#')
        print("### %s ###" % fname)
        print(p * '#')

if __name__ == '__main__':
    info = mkInfo("Obraz bg01")
    info.dropboxPth = [ '/', 'media', 'mk', 'p1ext4']
    info.MAINDIR = ['work', '19', 'nitrc_2019', 'bg01_x1_analiza_20190517']
    info.setAllWorkingFolders()