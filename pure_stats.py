from conllu import parse
from collections import defaultdict
import statistics
import math


class PureStatistics(object):
    def __init__(self, prepared_forum, threshold_for_tokens=2):
        self.rare_threshold = threshold_for_tokens
        self.forum = prepared_forum
        self.week_frequency_dict = {}
        self.corpus_frequency_dict = {}
        self.corpus_mean = {}
        self.corpus_median = {}
        self.corpus_sd = {}

        self.get_week_word_frequencies()
        self.get_corpus_word_frequencies()
        self.get_corpus_stats()


    '''def __init__(self, document, list_with_files):
        self.compare_doc_and_corpus()'''

    def get_week_word_frequencies(self):
        """
        todo: This needs to be updated!
        Gets frequency ((occurences/number words)*1000) of all words in doc and saves to self.doc_frequency_dict
        :param document: name/path to conllu file
        :param rare_threshold: minimum number of occurences in file for word to be included in analysis
        :return: self.corpus_frequency_dict with k:word-in-file, v:[] (to be modified later)
        """
        frequency_d = defaultdict(int)
        for text in self.forum.week_data:
            text_as_list = text.split(" ")
            for lemma in text_as_list:
                frequency_d[lemma] += 1
        for k, v in frequency_d.items():
            if v >= self.rare_threshold:
                # Multiply with 1000 to avoid small numbers:
                self.week_frequency_dict[k] = (v / self.forum.number_tokens_in_week) * 1000
            else:
                pass

    def get_corpus_word_frequencies(self):
        """
        todo: This needs to be updated!
        Gets frequency in each file, for all words in doc above threshold
        :param words_in_corpus: dict with k:word-in-file, v:[]
        :param files_in_corpus: list of file names/paths
        :return: dict with k:word, v:[(frequency in doc x), (frequency in doc y), ...]
        """
        self.corpus_frequency_dict = dict.fromkeys([k for k, v in self.week_frequency_dict.items()], [])
        for week, list_w_texts in self.forum.corpus_data.items():
            word_count = 0
            dict_count_occurences = defaultdict(int)
            for text in list_w_texts:
                list_w_words = text.split(" ")
                for word in list_w_words:
                    word_count += 1
                    if word in self.corpus_frequency_dict:  # Otherwise - why bother?
                        dict_count_occurences[word] += 1
            for k, v in self.corpus_frequency_dict.items():
                if k in dict_count_occurences:
                    self.corpus_frequency_dict[k] = \
                        self.corpus_frequency_dict[k] + [(dict_count_occurences[k] / word_count) * 1000]
                else:
                    self.corpus_frequency_dict[k] = \
                        self.corpus_frequency_dict[k] + [0]


    def get_corpus_stats(self):
        """
        get mean, median and (population)standard deviation for all words
        :return: modifies attributes dictionaries corpus_mean, corpus_median, corpus_sd, corpus_sd_median
        """
        for word, frequency in self.corpus_frequency_dict.items():
            self.corpus_mean[word] = statistics.mean(frequency)
            self.corpus_median[word] = statistics.median(frequency)
            self.corpus_sd[word] = statistics.pstdev(frequency)  # pstdev = population standard deviation

    def compare_doc_and_corpus(self, mean_or_median):
        """
        prints the words with frequency > (mean + sd * 2)
        :param median: default=False. Otherwise prints words with frequency > median+sd*2
        """
        list_big_deviations = []
        for word, frequency in self.week_frequency_dict.items():
            if mean_or_median == "mean":
                # todo: instead or deciding on a cut off - save to dictionary with diff as value \
                # and then create a sorted list as I did in TFIDF.
                # So save all and then print in reverse order.

                if frequency > self.corpus_mean[word] + (self.corpus_sd[word] * 3):
                    list_big_deviations.append((word, frequency))
                    print("MEAN: ", word, frequency)  # todo:save this somehow
            elif mean_or_median == "median":
                if frequency > self.corpus_median[word] + (self.corpus_sd[word] * 3):
                    print("MEDIAN:", word, frequency)  # todo:save this somehow
        print(list_big_deviations)
        #sorted_list = sorted(list_biggest_tfidf, key=lambda t: t[1], reverse=True)
        #for i in sorted_list:
        #    print(i)
        #print("\n\n")
        # todo: check create median sorted list too!
