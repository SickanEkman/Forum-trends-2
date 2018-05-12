import collections
import math


class Tfidf:
    def __init__(self, prepared_forum):
        self.forum = prepared_forum
        self.corpus_dict = self.parse_corpus_data_weeks()
        #self.corpus_detailed_dict = self.parse_corpus_data_posts()
        self.list_of_words = self.parse_doc_data()
        self.tf = {}
        self.idf_posts_as_doc = {}
        self.idf_weeks_as_doc = {}
        self.sorted_tfidf = []

    """def parse_corpus_data_posts(self):
        self.corpus_detailed_dict = collections.defaultdict(list)
        for week, list_w_texts in self.forum.corpus_data.items():
            for text in list_w_texts:
                set_words = set()
                text_as_list = text.split(" ")
                for word in text_as_list:
                    set_words.add(word)
                self.corpus_detailed_dict[week].append(set_words)
        return self.corpus_detailed_dict
    """

    def parse_corpus_data_weeks(self):
        self.corpus_dict = {}
        for week, list_w_posts in self.forum.corpus_data.items():
            set_words = set()
            for text in list_w_posts:
                text_as_list = text.split(" ")
                for word in text_as_list:
                    set_words.add(word)
            self.corpus_dict[week] = set_words
        return self.corpus_dict

    def parse_doc_data(self):
        self.list_of_words = []
        for text in self.forum.week_data:
            text_as_list = text.split(" ")
            for word in text_as_list:
                self.list_of_words.append(word)
        return self.list_of_words

    def count_tf(self, list_with_words=None):
        if not list_with_words:
            list_with_words = self.list_of_words
        counted = collections.Counter(list_with_words)
        max_occurencies = max(counted.values())
        self.tf = {k: (v / max_occurencies) for (k, v) in counted.items()}

    """def count_idf_posts_as_doc(self):
        num_docs = 1
        for word, frequency in self.tf.items():
            doc_occurences = 1  # to avoid zero division error
            for week, set_list in self.corpus_detailed_dict.items():
                for text_set in set_list:
                    if word in text_set:
                        doc_occurences += 1
                    num_docs += 1
            self.idf_posts_as_doc[word] = math.log2(num_docs/doc_occurences)
        return self.idf_posts_as_doc
    """

    def count_idf_weeks_as_doc(self):
        num_docs = len(self.corpus_dict) + 1
        for word, frequency in self.tf.items():
            doc_occurences = 1
            for week, word_set in self.corpus_dict.items():
                if word in word_set:
                    doc_occurences += 1
                self.idf_weeks_as_doc[word] = math.log2(num_docs/doc_occurences)
        return self.idf_weeks_as_doc

    def count_tfidf(self, idf):
        tfidf = {}
        for word, value in self.tf.items():
            tfidf[word] = value * idf[word]
        self.sorted_tfidf = sorted(tfidf.items(), key=lambda t: t[1], reverse=True)
        print("Sorted TFIDF", self.sorted_tfidf)
        return self.sorted_tfidf
