from conllu import parse
from collections import defaultdict
import statistics
import math


class PureStatistics(object):
    def __init__(self, prepared_forum, threshold_for_tokens=2):
        self.rare_threshold = threshold_for_tokens
        self.forum = prepared_forum
        self.doc_frequency_dict = {}
        self.corpus_mean = {}
        self.corpus_median = {}
        self.corpus_sd = {}
        self.corpus_sd_mean = {}
        self.corpus_sd_median = {}

    '''def __init__(self, document, list_with_files):
        self.corpus_frequency_dict = self.get_doc_word_frequencies(document, rare_threshold=2)
        self.get_corpus_word_frequencies(self.corpus_frequency_dict, list_with_files,)
        self.get_corpus_stats(self.corpus_frequency_dict)
        self.compare_doc_and_corpus()'''

    def get_doc_word_frequencies(self, document):
        """
        Gets frequency ((occurences/number words)*1000) of all words in doc and saves to self.doc_frequency_dict
        :param document: name/path to conllu file
        :param rare_threshold: minimum number of occurences in file for word to be included in analysis
        :return: self.corpus_frequency_dict with k:word-in-file, v:[] (to be modified later)
        """
        word_count = 0
        frequency_d = defaultdict(int)

        with open(document, "r") as fin:
            data = fin.read()
            for sentence in parse(data):
                for word in sentence:
                    word_count += 1
                    if word["upostag"] != "PUNCT":
                        lemma = word["lemma"].lower()

                        frequency_d[lemma] += 1
        fin.close()
        for k, v in frequency_d.items():
            if v >= self.rare_threshold:
                # Multiply with 1000 to avoid small numbers:
                self.doc_frequency_dict[k] = (v / word_count) * 1000
            else:
                pass
                #self.doc_frequency_dict[k] = 0
        self.corpus_frequency_dict = dict.fromkeys([k for k, v in self.doc_frequency_dict.items()], [])
        return self.corpus_frequency_dict

    def get_corpus_word_frequencies(self, words_in_corpus, files_in_corpus, ):
        """
        Gets frequency in each file, for all words in doc above threshold
        :param words_in_corpus: dict with k:word-in-file, v:[]
        :param files_in_corpus: list of file names/paths
        :return: dict with k:word, v:[(frequency in doc x), (frequency in doc y), ...]
        """
        for file_name in files_in_corpus:
            word_count = 0
            d_corpus_freq = defaultdict(int)
            with open(file_name, "r") as fin:
                data = fin.read()
                for sentence in parse(data):
                    for word in sentence:
                        word_count += 1
                        lemma = word["lemma"].lower()
                        if lemma in words_in_corpus:
                            d_corpus_freq[lemma] += 1
            for k, v in words_in_corpus.items():
                if k in d_corpus_freq:
                    words_in_corpus[k] = words_in_corpus[k] + [(d_corpus_freq[k] / word_count) * 1000]
#                    words_in_corpus[k] = words_in_corpus[k] + [math.log10(d_corpus_freq[k] / word_count)]
                else:
                    words_in_corpus[k] = words_in_corpus[k] + [0]
            #print(words_in_corpus)

    def get_corpus_stats(self, corpus_occurences):
        """
        get mean, median and (population)standard deviation for all words
        :param corpus_occurences: dict with k:word, v:[(frequency in doc x), (frequency in doc y), ...]
        :return: modifies attributes dictionaries corpus_mean, corpus_median, corpus_sd
        """
        for k, v in corpus_occurences.items():
            #import pdb; pdb.set_trace()
            self.corpus_mean[k] = statistics.mean(v)
            self.corpus_median[k] = statistics.median(v)
            self.corpus_sd[k] = statistics.pstdev(v, 2) #, self.corpus_mean[k])  # pstdev = population standard deviation
            self.corpus_sd_median[k] = statistics.pstdev(v, 7) #, self.corpus_median[k])  # pstdev = population standard deviation
        print(self.corpus_mean)
        print(self.corpus_sd_mean)
        print(self.corpus_sd_median)
        print(self.corpus_median)
        # todo: use sd and median even though sd for median doesn't work!


    def compare_doc_and_corpus(self, median=True):
        """
        prints the words with frequency > mean+sd*2
        :param median: default=False. Otherwise prints words with frequency > median+sd*2
        """
        #print("SD and MEAN: ")
        list_biggest_tfidf = []
        for k, v in self.doc_frequency_dict.items():
            #print("\t\t", k, v, "\n", "\t\t", self.corpus_mean[k], "&", self.corpus_sd[k])
            if v > self.corpus_mean[k] + (self.corpus_sd[k] * 2):
                # print("\t\t", k, v, "\n", "\t\t", self.corpus_mean[k], "&", self.corpus_sd[k])
                list_biggest_tfidf.append((k, v))
                #print("MEAN: ", k, v)  # todo:save this somehow
            if median:
                if v > self.corpus_median[k] + (self.corpus_sd[k] * 3):
                    print("MEDIAN:", k, v)  # todo:save this somehow
        print(list_biggest_tfidf)
        #sorted_list = sorted(list_biggest_tfidf, key=lambda t: t[1], reverse=True)
        #for i in sorted_list:
        #    print(i)
        #print("\n\n")
        # todo: check create median sorted list too!
