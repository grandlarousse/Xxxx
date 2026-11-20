"""Parça tabloları tek CSV'de birleştirir. Kullanım: python3 -I birlestir.py <çıktı csv>"""
import os
import sys
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.concat([pd.read_csv(os.path.join(HERE, 'out', f)) for f in ['s3.csv', 'tk.csv']], ignore_index=True)
df.to_csv(sys.argv[1], index=False)
print('satir:', len(df), '->', sys.argv[1])
