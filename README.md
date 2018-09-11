# data2tex
Latex support for trasport data from python script to LaTeX


In your python

```python
import data2tex as dtt

dtt.set_output(pth)
dtt.save(10, "ten")
dtt.save(np.pi, "pi")
dtt.save(np.pi, "pi2", precision=7)
dtt.save(3412516584, "big", scientific_notation=True)
dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
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

Ten \input{ten.tex},
Pi \input{pi},
Pi2 \input{pi2},
Big $\input{big}$,

Table

\input{dataframe}
\end{document}
```
