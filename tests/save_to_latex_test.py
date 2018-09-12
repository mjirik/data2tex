#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 mjirik <mjirik@mjirik-Latitude-E6520>
#
# Distributed under terms of the MIT license.

"""
Module for testing format rawiv
"""
import logging
logger = logging.getLogger(__name__)
import unittest
import subprocess
import os.path as op
import pandas as pd
import shutil
import os
import sys
import numpy as np
import data2tex as dtt


from nose.plugins.attrib import attr

pth = op.dirname(op.abspath(__file__))

class DataToTexTest(unittest.TestCase):

    # @attr('actual')
    # @attr('interactive')
    def test_write_number(self):
        text = dtt.num2latex(15)

        self.assertEqual(text, r"\num{15}")

    def test_save_number(self):
        dtt.set_output(pth)
        text = dtt.save(15, "fifteen")

        self.assertTrue(op.exists(op.join(pth, "fifteen.tex")))

    def test_compile_latex(self):
        texfile = "test_latex.tex"
        fn, ext = op.splitext(texfile)
        pdffile = fn + ".pdf"
        pth = op.dirname(op.abspath(__file__))

        dtt.set_output(pth)
        r = 90
        s = np.pi * r**2
        dtt.save(r, "radius")
        dtt.save(np.pi, "pi", precision=3)
        # dtt.save(np.pi, "pi2", precision=7)
        dtt.save(s, "surface", scientific_notation=True, precision=2)
        df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv")
        # dates = pd.date_range('20130101', periods=6)
        # df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
        dtt.save(df[
                     ["survived", "sex", "age", "class", 'fare', "embark_town", "alone"]][:10], "dataframe")

        print(pth)
        if op.exists(pdffile):
            os.remove(pdffile)
        import glob
        p = subprocess.Popen(["pdflatex", texfile, "-interaction", "nonstopmode"],
                             stdout=subprocess.PIPE, shell=False, cwd=pth)
        print("first ", glob.glob(op.join(pth, "*")))
        latex_output = p.communicate()
        logger.debug(latex_output[0])
        logger.debug(latex_output[1])
        # print(latex_output[0])
        # print(latex_output[1])
        # subprocess.Popen("pdflatex test_latex.tex -interaction nonstopmode", shell=True, cwd=pth)
        # subprocess.check_call("pdflatex test_latex.tex -interaction nonstopmode", shell=True, cwd=pth, timeout=30)
        # subprocess.run("dir", shell=True)
        from time import sleep
        sleep(10)
        print(glob.glob(op.join(pth, "*")))
        self.assertTrue(op.exists(op.join(pth, pdffile)))
