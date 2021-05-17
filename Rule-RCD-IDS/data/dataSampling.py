"""
1. fuzzify data
2. compute rule
"""

import csv
import pyodbc
import time

import pandas as pd
import random


if __name__ == '__main__':
    p = 0.002
    df = pd.read_csv("5class.csv", header=None, skiprows=lambda i: i>0 and random.random() > p)
    df.to_csv("5class_1k.csv",header = 0, index = 0)
