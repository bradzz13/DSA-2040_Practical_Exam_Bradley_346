import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from sklearn.metrics import adjusted_rand_score


#load saved iris dataset from preprocessing step(task 1)
iris_df = pd.read_csv('C:\\Users\\Bradl\\Downloads\\DSA-2040_Practical_Exam_Bradley_346\\Data Mining\\preprocess iris\\preprocessed_iris.csv')


# KMeans Clustering
knn = KMeans(n_clusters=3, random_state=42)

# Fit the model on the features only
features = iris_df.drop(columns=['setosa', 'versicolor', 'virginica'])
knn.fit(features)


# Predict clusters and compare with actual species using adjusted rand index(ARI)
predicted_clusters = knn.predict(features)
true_labels = iris_df[['setosa', 'versicolor', 'virginica']].idxmax(axis=1)
true_labels = true_labels.map({'setosa': 0, 'versicolor': 1, 'virginica': 2})
ari = adjusted_rand_score(true_labels, predicted_clusters)
print(f'Adjusted Rand Index (ARI) for KMeans clustering on Iris dataset: {ari}')


# Experiment
# try k=2,4 ;plot elbow rule to determine optimal k
sse = []
k_values = range(1, 11)
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features)
    sse.append(kmeans.inertia_)
# Plot the elbow graph
plt.figure(figsize=(8, 5))
plt.plot(k_values, sse, marker='o')
plt.title('Elbow Method for Optimal k in KMeans')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Sum of Squared Errors (SSE)')
plt.xticks(k_values)
plt.grid()
plt.show()



# Visualize clusters for k=3 using first two features
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(features.iloc[:, :2])  # Using only the first two features for visualization
predicted_clusters_2d = kmeans.predict(features.iloc[:, :2])   
plt.figure(figsize=(8, 5))
plt.scatter(features.iloc[:, 0], features.iloc[:, 1], c=predicted_clusters_2d, cmap='viridis', marker='o', edgecolor='k', s=100)
plt.title('KMeans Clustering of Iris Dataset (k=3)')
plt.xlabel(iris_df.columns[0])
plt.ylabel(iris_df.columns[1])
plt.grid()
plt.show()

#Analysis

# The KMeans clustering on the Iris dataset yielded an Adjusted Rand Index (ARI) that indicates a good level of agreement between the predicted clusters and the actual species labels. The ARI value suggests that the clustering algorithm was able to effectively separate the different species based on their features. However, some misclassifications were observed, particularly between the Versicolor and Virginica species, which share similar feature characteristics. This overlap in feature space can lead to challenges in accurately distinguishing between these two species.

# The elbow method plot indicated that k=3 is an optimal choice for the number of clusters, as there is a noticeable bend in the SSE curve at this point. This aligns with the known number of species in the dataset, further validating the choice of k. Visualizing the clusters using the first two features revealed distinct groupings, although some points were misclassified, highlighting the limitations of using only two dimensions for clustering.

# In real-world applications, KMeans clustering can be utilized for customer segmentation, where businesses can group customers based on purchasing behavior, demographics, or preferences. This segmentation allows for targeted marketing strategies, personalized recommendations, and improved customer retention. Additionally, clustering can be applied in image segmentation, anomaly detection, and market research to identify patterns and insights within large datasets. Overall, while KMeans is a powerful tool for unsupervised learning, careful consideration of feature selection and cluster validation is essential to ensure meaningful results.# Analyze cluster quality, misclassifications, and real-world applications

