
import csv
import random


with open("forice\\MedakUTD.csv", "r", encoding="utf8") as f:
    reader = csv.reader(f,delimiter='-')
    forice = list(reader)
    message = forice[random.randint(0,len(forice) - 1)][0]
    print(message)