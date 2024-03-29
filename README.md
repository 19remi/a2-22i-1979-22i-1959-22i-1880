# a2
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('process.csv')

# Filter the DataFrame where ARTICLE_ID equals 0, 1, or 2
filtered_df = df[df['ARTICLE_ID'].isin([0, 1])]

# Initialize an empty set to store unique words
word_set = set()

# Iterate over the SECTION_TEXT values in the filtered DataFrame
for section_text in filtered_df['SECTION_TEXT']:
    # Split the paragraph into words using whitespace as the delimiter
    section_text = str(section_text)
    words = section_text.split()
    # Add each word to the set
    for word in words:
        word_set.add(word)

# Convert the set into a sorted list
sorted_word_list = sorted(word_set)

# Create a dictionary to map each word to a unique ID
unique_id_set = {word: idx for idx, word in enumerate(sorted_word_list)}

# Create a dictionary tf0 with unique ID from unique_id_set and count as 0 initially
tf0 = {unique_id: 0 for unique_id in unique_id_set.values()}
tf1={unique_id: 0 for unique_id in unique_id_set.values()}
# Iterate over each paragraph where ARTICLE_ID equals 0
for section_text in df[df['ARTICLE_ID'] == 0]['SECTION_TEXT']:
    # Split the paragraph into words using whitespace as the delimiter
    words = str(section_text).split()
    # Increment the count for each word in tf0
    for word in words:
        unique_id = unique_id_set.get(word)
        if unique_id is not None:
            tf0[unique_id] += 1
for section_text in df[df['ARTICLE_ID'] == 1]['SECTION_TEXT']:
    # Split the paragraph into words using whitespace as the delimiter
    words = str(section_text).split()
    # Increment the count for each word in tf1
    for word in words:
        unique_id1 = unique_id_set.get(word)
        if unique_id1 is not None:
            tf1[unique_id1] += 1
# Filter out items with count 0
tf0_filtered = {unique_id: count for unique_id, count in tf0.items() if count != 0}
# Filter out items with count 0
tf1_filtered = {unique_id1: count for unique_id1, count in tf1.items() if count != 0}


# Print the filtered tf0 dictionary
print(tf0_filtered)

# Print the filtered tf0 dictionary
print(tf0_filtered)

# Print the tf0 dictionary
#print(tf0)
#print('\n \n \n')
#print(tf1)
# for understanding will do map reducer later
