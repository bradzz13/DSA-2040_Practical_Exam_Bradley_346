import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt


#load iris data
iris=load_iris()
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)


# Handle missing values 
iris_df = iris_df.dropna()


# Normalize the data using min-max scaling
scaler = MinMaxScaler()
iris_df = pd.DataFrame(scaler.fit_transform(iris_df), columns=iris.feature_names)


#One hot encode the class labels 
iris_df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
iris_df = pd.get_dummies(iris_df, columns=['species'], prefix='', prefix_sep='')



# Exploratory data analysis (EDA)

## summary statistics
summary_stats = iris_df.describe()
print(summary_stats)


#Visualise the data

# Pairplots to visualize relationships between features
sns.pairplot(iris_df, hue='setosa', diag_kind='kde')
plt.title('Pairplot of Iris Dataset - Setosa')
plt.show()

sns.pairplot(iris_df, hue='versicolor', diag_kind='kde')
plt.title('Pairplot of Iris Dataset - Versicolor')
plt.show()

sns.pairplot(iris_df, hue='virginica', diag_kind='kde')
plt.title('Pairplot of Iris Dataset - Virginica')
plt.show()


# Correlation matrix heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(iris_df.corr(), annot=True, fmt='.2f', cmap='coolwarm', square=True)
plt.title('Correlation Matrix Heatmap')
plt.show()


# Identify and outliers using boxplots
# Boxplot for each feature
for feature in iris.feature_names:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=iris_df[feature])
    plt.title(f'Boxplot of {feature}')
    plt.show()



# function to split data into train/test (80/20)
def load_and_split_iris_data(test_size=0.2, random_state=42):
    # Load the iris dataset
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='species')

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test

#call the function to load and split the data
X_train, X_test, y_train, y_test = load_and_split_iris_data()

#export the preprocessed dataset 
iris_df.to_csv('preprocessed_iris.csv', index=False)
print("Preprocessed iris dataset saved to 'preprocessed_iris.csv'")
