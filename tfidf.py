import collections
import math


class Tfidf:
    def __init__(self, prepared_forum):
        self.forum = prepared_forum
        self.corpus_dict = self.parse_corpus_data()
        self.list_of_week_words = self.parse_doc_data()
        self.tf = {}
        self.idf = {}
        self.sorted_tfidf = []

    def parse_corpus_data(self):
        """
        Create a set with types for each week in forum
        :return: add to self.corpus_dict, k=week and v=set w types
        """
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
        """
        Append all tokens from Week In Question (doc) to list
        :return: append to self.list_of_week_words
        """
        list_of_week_words = []
        for text in self.forum.week_data:
            text_as_list = text.split(" ")
            for word in text_as_list:
                list_of_week_words.append(word)
        return list_of_week_words

    def count_tf(self):
        """
        Count Term Frequency for types in doc (Week Of Interest)
        TF equation: (frequency of type)/(maximum frequency of any type)
        :return: adds to self.tf where k=type and v=TF
        """
        list_with_words = self.list_of_week_words
        counted = collections.Counter(list_with_words)
        max_occurencies = max(counted.values())
        self.tf = {k: (v / max_occurencies) for (k, v) in counted.items()}

    def count_idf(self):
        """
        Count Inverse Document Frequency for every type in Week Of Interest
        IDF equation: log2(number of documents in my corpus/number doc in corpus containing the word)
        :return: adds to self.idf where k=type and v=IDF
        """
        num_docs = len(self.corpus_dict) + 1
        # + 1 because I start my doc_occurences with 1 instead of 0, and if I
        # divide a doc_occurences with a bigger value the log of the quotient would be negative. Not good, right?
        for word, frequency in self.tf.items():
            doc_occurences = 1  # to avoid division by zero issues
            for week, word_set in self.corpus_dict.items():
                if word in word_set:
                    doc_occurences += 1
            self.idf[word] = math.log2(num_docs/doc_occurences)
        return self.idf

    def count_tfidf(self):
        """
        Multiply every type's tf with it's idf and get tf*idf. Create tuples (type, tfidf-value).
        :return: append tuples to self.sorted_tfidf, sorted after size of tfidf-value in falling order.
        """
        if len(self.tf) == 0:
            self.count_tf()
        if len(self.idf) == 0:
            self.count_idf()
        tfidf = {}
        for word, value in self.tf.items():
            tfidf[word] = value * self.idf[word]
        # Get k-v-tuples from dictionary, sort by tuple[1] in falling order. Save in order to list with tuples:
        self.sorted_tfidf = sorted(tfidf.items(), key=lambda t: t[1], reverse=True)
        return self.sorted_tfidf
