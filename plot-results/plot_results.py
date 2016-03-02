# Plots SUMSARIZER results.

# Input: CSV output file
# Outputs: directory of pngs of this file plotted

import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import datetime
import time

def parse_timestamp(date_string):
  return datetime.datetime.fromtimestamp(time.mktime(time.strptime(date_string, '%Y-%m-%d %H:%M:%S')))

# setname = 'alfashir1_B12.csv'
email = 'ajaypillarisetti@gmail.com'
filename = 'sumsarized.csv'
outdir = 'data/out'

datasets = {}

with open(filename) as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    dataset = datasets.get(row['filename'], [])
    dataset.append(row)
    datasets[row['filename']] = dataset

for filename, dataset in datasets.items():

  outpath = os.path.join('out2', filename + email + '.png')

  # Filter to a single user
  dataset = [row for row in dataset if row['email'] == email]

  ids = np.array([parse_timestamp(row['timestamp']) for row in dataset])
  temps = np.array([float(row['value']) for row in dataset])
  labels = np.array([row['cooking_label'] == 't' for row in dataset])

  cooking = np.ma.masked_where(labels, temps)

  # Stack in plots of 200 points at a time
  N = len(ids)
  M = int(N / 200)
  time_split = np.array_split(ids, M)
  temp_split = np.array_split(temps, M)
  cooking_split = np.array_split(cooking, M)

  plt.figure(figsize=(30, 5*M))

  for i in range(M):
    plt.subplot(M, 1, i+1)
    plt.plot(time_split[i], temp_split[i], 'bo-', time_split[i], cooking_split[i], 'ro-')
    axes = plt.gca()
    axes.set_ylim([15, 140])
  plt.savefig(outpath)
  plt.close()
  print outpath