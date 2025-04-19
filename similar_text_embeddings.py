from sentence_transformers import SentenceTransformer
import numpy as np
from itertools import combinations

# Load the Sentence Transformer model
model = SentenceTransformer('BAAI/bge-base-en-v1.5')

# Paths to input and output files
input_file_path = r"data/comments.txt"
output_file_path = r"data/comments-similar.txt"

# Function to compute cosine similarity
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Read the comments from file
with open(input_file_path, "r", encoding="utf-8") as file:
    comments = [line.strip() for line in file.readlines() if line.strip()]

# Ensure there are at least two comments to compare
if len(comments) < 2:
    print("Not enough comments to compare.")
    exit()

# Generate embeddings for all comments
embeddings = model.encode(comments)

# Find the most similar pair
max_similarity = -1
most_similar_pair = None

for (i, j) in combinations(range(len(comments)), 2):
    similarity = cosine_similarity(embeddings[i], embeddings[j])
    if similarity > max_similarity:
        max_similarity = similarity
        most_similar_pair = (comments[i], comments[j])

# Write the most similar pair to the output file
if most_similar_pair:
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(most_similar_pair[0] + "\n")
        file.write(most_similar_pair[1] + "\n")

    print(f"Most similar comments saved to {output_file_path}")
else:
    print("No similar comments found.")
