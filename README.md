# data2tex
[![Build Status](https://travis-ci.org/mjirik/data2tex.svg?branch=master)](https://travis-ci.org/mjirik/data2tex)
[![Coverage Status](https://coveralls.io/repos/github/mjirik/data2tex/badge.svg?branch=master)](https://coveralls.io/github/mjirik/data2tex?branch=master)

Latex support for pushing data from python script to LaTeX.

In your python use `save` function.

```python
import data2tex as dtt
import pandas as pd
import numpy as np

dtt.set_output(".")

df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv")

dtt.save(df[["survived", "sex", "age", "class", 'fare', "embark_town", "alone"]][:10], "dataframe")
dtt.save(len(df), "nrecords")
dtt.save(np.sum(df["fare"]), "fare",  precision=2, scientific_notation=True)
dtt.save(np.mean(df["survived"]), "psurvived", precision=4)

dtt.save(df, "dataframe")
```

Add fallowing lines into your LaTeX
```latex
\usepackage{siunitx}
\usepackage{booktabs}
```

In you LaTex then just call `input`
```latex
\documentclass[12pt]{article}
\usepackage{siunitx}
\usepackage{booktabs}
\begin{document}

We have \input{nrecords} records in our titanic table. 
The total fare was $\input{fare}$  and mean survive chance is \input{psurvived}.

\input{dataframe}
\end{document}
```

![pdfoutput](https://raw.githubusercontent.com/mjirik/data2tex/master/graphics/pdfoutput.png "PDF output")
