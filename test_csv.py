import os
import csv
import numpy as np

data = []
with open('forice.csv', 'r') as csv_file:
    csv_input = csv.reader(csv_file, delimiter=',')
    data = list(csv_input)
    
data.append("test forica")

with open('forice.csv', 'a') as f:
    f.write("\n" + "test forica")

print(data)
print(data)