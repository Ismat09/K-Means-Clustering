# -*- coding: utf-8 -*-
"""Copy of Lab 5 - k-means.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15DkQxv7-x-PmVNVhZTtaqDCwSPt_QVyf
"""

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

from sklearn.cluster import KMeans

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import silhouette_score

from sklearn.decomposition import PCA



"""Loading of Airpoll dataset"""

from google.colab import files
uploaded = files.upload()

data = pd.read_csv('/content/airpoll spreadsheet.csv', sep=";")

# Data Exploration

print(data.info())

data.describe()

# Handling missing values

for column in data.columns:
  try:
    data[column] = pd.to_numeric(data[column].str.replace(',', ''),  errors='coerce')
  except ValueError:
    pass

data.fillna(data.mean(), inplace=True)

# Describe variables

print("Dataset variables (column names):")
print(data.columns)

"""Correlation Matrix"""

correlation_matrix = data.corr()

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")

# Show distribution of each Pollutant

for column in data.columns:
    sns.histplot(data[column], kde=True, bins=30)
    plt.title(f"Distribution of {column}")
    plt.show()

# Normalize the dataset

scaler = StandardScaler()

data_scaled = scaler.fit_transform(data)

# determine the number of clusters using Elbow method

inertia = []
K = range(1, 11)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K, inertia, 'bo-')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.show()

# Silhouette Analysis

silhouette_scores = []
K = range(2, 11)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(data_scaled)
    silhouette_avg = silhouette_score(data_scaled, cluster_labels)
    silhouette_scores.append(silhouette_avg) # append the calculated scores

# show silhoute distribution

plt.figure(figsize=(8, 5))
plt.plot(range(2, 11), silhouette_scores, 'bo-')
plt.title("Silhouette Scores")
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.show()

# Optimal clusters selection

optimal_clusters = 2  # number that corresponds with the hpeak of silhouette score

kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)

data['Cluster'] = kmeans.fit_predict(data_scaled)

# export results onto excel

data.to_excel('kmeans_results.xlsx', index=False)
print("Clustered dataset to 'kmeans_results.xlsx")

# Visualies clusters ( PCA for dimensionality Reduction)

pca = PCA(n_components=2)

data_pca = pca.fit_transform(data_scaled)

plt.figure(figsize=(8, 6))
sns.scatterplot(x=data_pca[:, 0], y=data_pca[:, 1], hue=data['Cluster'], palette="Set2", s=100)
plt.title("Clusters Visualization (PCA Reduced)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend(title="Cluster")
plt.show()