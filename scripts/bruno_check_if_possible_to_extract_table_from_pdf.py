from tabula import read_pdf
import pandas as pd

df = read_pdf("/home/administrator/Downloads/2017_2018.pdf")

df.to_csv("/home/administrator/repos/edufuture/data/2017_2018.csv")



df = read_pdf("/home/administrator/Downloads/69_matem_rezultati.pdf")

df.to_csv("/home/administrator/repos/edufuture/data/2018_2019.csv")