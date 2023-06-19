import os
from numpy import vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Retrieve a list of text files in the current directory
sample_files = [doc for doc in os.listdir() if doc.endswith('.txt')]

# Read the contents of each text file and store them in a list
sample_contents = [open(File).read() for File in sample_files]

# Define a lambda function to vectorize the text data using TF-IDF
vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()

# Define a lambda function to calculate the cosine similarity between document vectors
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])

# Vectorize the text data using the defined lambda function
vectors = vectorize(sample_contents)

# Pair each sample file with its corresponding vectorized representation
s_vectors = list(zip(sample_files, vectors))

# Function to check plagiarism
def check_plagiarism():
    results = set()
    global s_vectors

    # Iterate over each sample document and its vector
    for sample_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()

        # Find the index of the current document vector
        current_index = new_vectors.index((sample_a, text_vector_a))

        # Remove the current document vector from the new list
        del new_vectors[current_index]

        # Compare the current document vector with all other vectors
        for sample_b, text_vector_b in new_vectors:
            # Calculate the similarity score between the document vectors
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]

            # Sort the document names to maintain consistent ordering
            sample_pair = sorted((sample_a, sample_b))

            # Create a tuple with document pair and similarity score
            score = sample_pair[0], sample_pair[1], sim_score

            # Add the score tuple to the results set
            results.add(score)

    return results

# Iterate over the plagiarism check results and print them
for data in check_plagiarism():
    print(data)
  