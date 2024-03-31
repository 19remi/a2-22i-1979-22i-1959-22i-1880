from mrjob.job import MRJob
from mrjob.step import MRStep
import nltk
import string
import contractions
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd

# Download necessary NLTK resources
nltk.download('wordnet')
nltk.download('stopwords')

class MRWordSimilarity(MRJob):

    def configure_args(self):
        super(MRWordSimilarity, self).configure_args()
        self.add_passthru_arg('--num-articles', type=int, help="Number of articles to check")
        self.add_passthru_arg('--query', type=str, help="Search query")

    def mapper_preprocess_text(self, _, line):
        article_id, _, _, section_text = line.strip().split(',', 3)
        article_id = int(article_id)

        # Preprocess the text
        section_text = contractions.fix(section_text)
        section_text = section_text.lower()
        section_text = section_text.translate(str.maketrans('', '', string.punctuation))
        words = section_text.split()

        # Emit word and article_id pairs
        for word in words:
            yield word, (article_id, 1)

    def reducer_count_words(self, word, article_counts):
        # Count occurrences of each word in each article
        tf_dict = {}
        for article_id, count in article_counts:
            tf_dict[article_id] = tf_dict.get(article_id, 0) + count
        for article_id, count in tf_dict.items():
            yield (word, article_id), (count, 1)

    def reducer_calculate_tf(self, word_article_id, counts):
        # Calculate Term Frequency (TF)
        total_count = sum(count for count, _ in counts)
        tf = total_count / sum(1 for _, _ in counts)
        yield word_article_id[0], (word_article_id[1], tf)

    def reducer_calculate_idf(self, word, tf_values):
        # Calculate Inverse Document Frequency (IDF)
        num_articles = len(set(article_id for _, article_id in tf_values))
        idf = 1 / num_articles
        yield word, (idf, 1)

    def reducer_calculate_tf_idf(self, word_article_id, tf_idf_values):
        # Calculate TF-IDF
        tf, idf = 0, 0
        for val, _ in tf_idf_values:
            if val == 0:
                idf += 1
            else:
                tf = val
        tf_idf = tf * idf
        yield word_article_id, tf_idf

    def mapper_query(self, _, line):
        query_words = line.strip().split()
        for word in query_words:
            yield word, 1

    def reducer_calculate_query_tf_idf(self, word, _):
        # Calculate TF-IDF for query words
        yield word, 1

    def reducer_calculate_similarity(self, word, query_counts):
        # Calculate similarity scores
        query_count = sum(query_counts)
        yield word, query_count

    def steps(self):
        return [
            MRStep(mapper=self.mapper_preprocess_text,
                   reducer=self.reducer_count_words),
            MRStep(reducer=self.reducer_calculate_tf),
            MRStep(reducer=self.reducer_calculate_idf),
            MRStep(reducer=self.reducer_calculate_tf_idf),
            MRStep(mapper=self.mapper_query,
                   reducer=self.reducer_calculate_query_tf_idf),
            MRStep(reducer=self.reducer_calculate_similarity)
        ]

if __name__ == '__main__':
    MRWordSimilarity.run()

