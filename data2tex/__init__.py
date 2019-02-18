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
use_pure_latex = False


def set_output(dir_path):
    global output_dir_path
    odp = op.expanduser(dir_path)
    output_dir_path = odp


def set_pure_latex(pure_tex):
    global use_pure_latex
    use_pure_latex = pure_tex


def save(data, filename, precision=4, scientific_notation=None, pure_latex=None, index=False):
    """

    :param data:
    :param filename:
    :param precision: round precision
    :param scientific_notation: None or False (13141), True (1.3141*10^4) or "engineering" (13.141 *10^3)
    Format is done in LaTeX macro from siunitx package.
    :param pure_latex:
    The python implementation of scientific formating is used if this parameter is set True. Obsolete.
    :return:
    """
    tp = type(data)

    if pure_latex is None:
        pure_latex = use_pure_latex

    if type(data) is str:
        text = data
        pass
    elif isinstance(data, Number):
        if pure_latex:
            text = num2latex_pure_tex(data, precision=precision, scientific_notation=scientific_notation)
            # text = _latex_float_pure(data, precision=precision)
        else:
            text = num2latex_with_siunintx(
                data,
                precision=precision,
                scientific_notation=scientific_notation
            )


    else:
        try:
            import pandas as pd
            if type(data) == pd.DataFrame:
                text = data.to_latex(index=index)
                pass
        except ImportError as e:
            logger.debug("pandas is not installed")

    _to_file(text, filename)
    return text


def _latex_float_pure(f, precision=4):
    """
    Format implementation done in python.
    :param f:
    :param precision:
    :return:
    """
    precision = precision + 1
    float_str = "{0:." + str(int(precision)) + "g}"
    float_str = float_str.format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
    else:
        return float_str


def num2latex_pure_tex(num, precision=4, scientific_notation=None):
    nstr = str(num)
    if "e" in nstr:
        scientific_notation = True

    if scientific_notation:
        nstr = _latex_float_pure(num, precision=precision)

    return nstr


# def float_to_latex_file(fl, fn, precision=4):
#     string = latex_float(fl, precision=precision)
#     with open(fn, "w") as f:
#         f.write(string)


def num2latex_with_siunintx(num, precision=4, scientific_notation=None):
    """
    Use package \\usepackage{siunitx}
    :param num:
    :param filename:
    :param precision:
    :param scientific_notation: None or True, False or "engeneering"
    :return:
    """
    # precision = precision + 1
    formated_float_str = None
    if type(num) is str:
        float_str = num
        if float_str[:4] == r"\num":
            formated_float_str = float_str
    else:
        float_str = "{0:." + str(int(precision)) + "g}"
        float_str = float_str.format(num)

    if formated_float_str is None:
        formated_float_str = r"\num["
        if scientific_notation is not None:
            if scientific_notation is True:
                scientific_notation = "true"
            elif scientific_notation is False:
                scientific_notation = "false"
            formated_float_str += "scientific-notation=" + scientific_notation

        formated_float_str += "]{" + float_str + "}"
    return formated_float_str


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
