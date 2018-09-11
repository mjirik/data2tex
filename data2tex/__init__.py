#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Module is used to export data from python script to LaTeX document.
"""

import logging
logger = logging.getLogger(__name__)
import os.path as op
from numbers import Number

output_dir_path = "."

def set_output(dir_path):
    global output_dir_path
    odp = op.expanduser(dir_path)
    output_dir_path = odp


def save(data, filename, precision=4, scientific_notation=False):
    tp = type(data)

    if type(data) is str:
        text = data
        pass
    elif isinstance(data, Number):
        if scientific_notation:
            text = _latex_float(data, precision=precision)
        else:
            text = num2latex(data, precision=precision)


    else:
        try:
            import pandas as pd
            if type(data) == pd.DataFrame:
                text = data.to_latex()
                pass
        except ImportError as e:
            logger.debug("pandas is not installed")
            pass

    _to_file(text, filename)


def _latex_float(f, precision=4):
    """
    Format implementation done in python.
    :param f:
    :param precision:
    :return:
    """
    float_str = "{0:." + str(int(precision)) + "g}"
    float_str = float_str.format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
    else:
        return float_str


# def float_to_latex_file(fl, fn, precision=4):
#     string = latex_float(fl, precision=precision)
#     with open(fn, "w") as f:
#         f.write(string)


def num2latex(num, filename=None, precision=4):
    """
    Use package \\usepackage{siunitx}
    :param num:
    :param filename:
    :param precision:
    :return:
    """
    precision = precision + 1
    if type(num) is str:
        float_str = num
    else:
        float_str = "{0:." + str(int(precision)) + "g}"
        float_str = float_str.format(num)

    if float_str[:4] == r"\num":
        pass
    else:
        float_str = "\\num{" + float_str + "}"
    if filename is not None:
        _to_file(float_str, filename)
    return float_str


def _to_file(text, filename, check_extension=True):
    """
    Check extension and output path and write to latex file.

    :param text:
    :param filename:
    :param check_extension:
    :return:
    """
    basename, ext = op.splitext(filename)
    if check_extension and ext is not ".tex":
        logger.info("Extension '.tex' added.")
        filename = filename + ".tex"

    if not op.isabs(filename):
        if output_dir_path is None:
            logger.error("Set output dir with set_output() function")
            raise ValueError("The output path is not set.")
        filename = op.join(output_dir_path, filename)

    with open(filename, "w") as f:
        f.write(text)
