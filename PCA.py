import pandas as pd
from tkinter.filedialog import askopenfile
import csv

path = "/Users/justinemajor/Documents/gph.doc/stage1/documents/spectres/"

données=pd.read_csv(path + "0001_01.txt", sep = r"\n")[14:]
print(données)