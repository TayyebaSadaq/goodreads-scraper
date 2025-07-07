import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the CSV
df = pd.read_csv("romance_books.csv")

# 2. Quick Data Checks
print(df.head())
print(df.info())

# Convert average_rating and num_ratings to float/int
df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')
df['num_ratings'] = pd.to_numeric(df['num_ratings'], errors='coerce')

# 3. Plots

# Histogram of average ratings
plt.figure(figsize=(8, 5))
df['average_rating'].hist(bins=20, color='skyblue', edgecolor='black')
plt.title("Histogram of Average Ratings")
plt.xlabel("Average Rating")
plt.ylabel("Number of Books")
plt.show()

# Top 10 books by number of ratings
top10 = df.sort_values('num_ratings', ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.barh(top10['title'][::-1], top10['num_ratings'][::-1], color='salmon')
plt.title("Top 10 Books by Number of Ratings")
plt.xlabel("Number of Ratings")
plt.tight_layout()
plt.show()

# Scatter plot: rating vs number of ratings
plt.figure(figsize=(8, 5))
plt.scatter(df['num_ratings'], df['average_rating'], alpha=0.6)
plt.title("Average Rating vs Number of Ratings")
plt.xlabel("Number of Ratings")
plt.ylabel("Average Rating")
plt.xscale('log')
plt.tight_layout()
plt.show()