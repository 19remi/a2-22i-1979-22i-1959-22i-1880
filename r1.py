import pandas as pd
import nltk
import contractions
import string

# Download necessary resources
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Function to preprocess text
def preprocess_text(text):
    text = contractions.fix(text)
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(lemmatized_words)

# Read the CSV file
df = pd.read_csv('process.csv')

# Ask user for the number of articles to check
num_articles = int(input("Enter the number of articles to check: "))

# Initialize a set for all unique words and a list to hold the tf dictionaries
word_set = set()
tf_dicts = []

# Initialize a data structure for IDF
idf = {}

# Stop words and lemmatizer initialization
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Process each article
for i in range(num_articles):
    # Filter the DataFrame for the current article
    filtered_df = df[df['ARTICLE_ID'] == i]
    
    # Initialize term frequency dictionary for the current article
    tf_dicts.append({})
    
    # Iterate over each section of the article
    for section_text in filtered_df['SECTION_TEXT']:
        # Preprocess the text
        processed_text = preprocess_text(str(section_text))
        
        # Tokenize the processed text
        words = processed_text.split()
        
        # Update word_set and term frequency dictionary
        for word in words:
            word_set.add(word)
            tf_dicts[i][word] = tf_dicts[i].get(word, 0) + 1
            
            # For IDF, we just mark if the word has appeared in the document
            if word in idf:
                idf[word].add(i)
            else:
                idf[word] = {i}

# Calculate IDF for each word
idf = {word: len(idf[word]) for word in idf}

# Calculate TF-IDF for each document
tf_idf_dicts = []
for i in range(num_articles):
    tf_idf = {}
    for word in tf_dicts[i]:
        tf = tf_dicts[i][word]
        # Perform IDF smoothing to avoid division by zero
        idf_value = idf[word] if idf[word] != 0 else 1
        tf_idf[word] = tf / idf_value
    tf_idf_dicts.append(tf_idf)

# Get a search query from the user
query = input("Enter your search query: ")
processed_query = preprocess_text(query)
query_words = processed_query.split()

# Compute TF-IDF for the query
query_tf_idf = {}
for word in query_words:
    # Perform IDF smoothing to avoid division by zero
    idf_value = idf.get(word, 0) if idf.get(word, 0) != 0 else 1
    query_tf_idf[word] = query_words.count(word) / idf_value

# Compute similarity scores (inner product) between the query and each document
similarity_scores = []
for i in range(num_articles):
    score = sum(query_tf_idf.get(word, 0) * tf_idf_dicts[i].get(word, 0) for word in query_words)
    similarity_scores.append((i, score))

# Sort the scores and print the results
sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
print("Similarity scores:")
for score in sorted_scores:
    print(f"Article {score[0]}: {score[1]}")
