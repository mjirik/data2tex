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

        self.assertEqual(text, r"\num[]{15}")

    def test_save_number(self):
        dtt.set_output(pth)
        text = dtt.save(15, "fifteen")

        self.assertTrue(op.exists(op.join(pth, "fifteen.tex")))

    def test_save_number_with_python_implementation(self):
        dtt.set_output(pth)
        text = dtt.save(16, "sixteen", scientific_notation=True, python_implementation=True)

        self.assertTrue(op.exists(op.join(pth, "sixteen.tex")))

    def test_save_pi_with_python_implementation(self):
        fn = op.join(pth, "pi.tex")
        dtt.set_output(pth)
        text = dtt.save(3.1415, "pi", scientific_notation=True, python_implementation=True)

        self.assertTrue(op.exists(fn))
        os.remove(fn)

    def test_save_pi_with_no_scientific_notation_and_siunitx_implementation(self):
        dtt.set_output(pth)
        fn = op.join(pth, "pi.tex")
        text = dtt.save(3.1415, "pi", scientific_notation=False, python_implementation=False)
        self.assertTrue(op.exists(fn))
        os.remove(fn)

    def test_save_directly_num_with_siunitx_implementation(self):
        dtt.set_output(pth)
        fn = op.join(pth, "pi.tex")
        text = dtt.save(r"\num{3.1415}", "pi", scientific_notation=False, python_implementation=False)
        self.assertTrue(op.exists(fn))
        os.remove(fn)


    def test_throw_exception_on_no_output_path(self):
        dtt.output_dir_path = None
        # dtt.set_output(None)
        self.assertRaises(ValueError, dtt._to_file, "asd", "file")


    def test_compile_latex(self):
        texfile = "test_latex.tex"
        fn, ext = op.splitext(texfile)
        pdffile = fn + ".pdf"
        pth = op.dirname(op.abspath(__file__))

        dtt.set_output(pth)
        # r = 90
        # s = np.pi * r**2
        # dtt.save(r, "radius")
        # dtt.save(np.pi, "pi", precision=3)
        # dtt.save(np.pi, "pi2", precision=7)
        # dtt.save(s, "surface", scientific_notation=True, precision=2)
        # dates = pd.date_range('20130101', periods=6)
        # df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
        df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv")
        dtt.save(df[["survived", "sex", "age", "class", 'fare', "embark_town", "alone"]][:10], "dataframe")

        dtt.save(len(df), "nrecords")
        dtt.save(np.sum(df["fare"]), "fare",  precision=2, scientific_notation=True)
        # dtt.save(np.sum(df["fare"]), "fare",  precision=2, scientific_notation="engineering")
        dtt.save(np.mean(df["survived"]), "psurvived", precision=3)
        dtt.save(df["embark_town"].value_counts().idxmax(), "embark")

        print(pth)
        if op.exists(pdffile):
            os.remove(pdffile)
        import glob
        p = subprocess.Popen(["pdflatex", texfile, "-interaction", "nonstopmode"],
                             stdout=subprocess.PIPE, shell=False, cwd=pth)
        latex_output = p.communicate()
        logger.debug(latex_output[0])
        logger.debug(latex_output[1])
        # print(glob.glob(op.join(pth, "*")))
        self.assertTrue(op.exists(op.join(pth, pdffile)))
