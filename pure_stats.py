from collections import defaultdict
import statistics


class PureStatistics(object):
    def __init__(self, prepared_forum, mean_or_median, subtract_sd, threshold_for_tokens=2):
        self.forum = prepared_forum
        self.mean_or_median = mean_or_median
        self.subtract_sd = subtract_sd
        self.rare_threshold = threshold_for_tokens
        self.week_frequency_dict = {}
        self.corpus_frequency_dict = {}
        self.corpus_mean = {}
        self.corpus_median = {}
        self.corpus_sd = {}
        self.sorted_stats = []

        self.get_week_word_frequencies()
        self.get_corpus_word_frequencies()
        self.get_corpus_stats()
        self.compare_week_and_corpus()

    def get_week_word_frequencies(self):
        """
        Counts frequencies ((occurences/number words in Week)*1000) for all words in Week Of Interest
        :return: Saves frequencies to self.week_frequency_dict
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
        Get word's frequencies in corpus, for all words in Week Of Interest

        :return: save to dict with k:word, v:[(frequency in doc x), (frequency in doc y), ...]
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
        get mean, median and (population)standard deviation for all words in Week Of Interest
        :return: saves to dictionaries corpus_mean, corpus_median, corpus_sd, corpus_sd_median
        """
        for word, frequency in self.corpus_frequency_dict.items():
            self.corpus_mean[word] = statistics.mean(frequency)
            self.corpus_median[word] = statistics.median(frequency)
            self.corpus_sd[word] = statistics.pstdev(frequency)  # pstdev = population standard deviation

    def compare_week_and_corpus(self):
        """
        Compares each word's frequency to either it's mean or median, ex: (frequency - mean).
        If self.subtract_sd == True, also subtract standard deviation, ex: (frequency - mean - sd)
        Creates tuples (word, diff-value) and save to self.sorted_stats, sorted after size of diff in falling order.
        """
        dict_w_scores = {}
        for word, frequency in self.week_frequency_dict.items():
            if self.mean_or_median == "mean":
                if not self.subtract_sd:
                    dict_w_scores[word] = frequency - self.corpus_mean[word]
                elif self.subtract_sd:
                    dict_w_scores[word] = frequency - self.corpus_mean[word] - self.corpus_sd[word]
            elif self.mean_or_median == "median":
                if not self.subtract_sd:
                    dict_w_scores[word] = frequency - self.corpus_median[word]
                elif self.subtract_sd:
                    dict_w_scores[word] = frequency - self.corpus_median[word] - self.corpus_sd[word]
        # Get k-v-tuples from dictionary, sort by tuple[1] in falling order. Save in order to list with tuples:
        self.sorted_stats = sorted(dict_w_scores.items(), key=lambda t: t[1], reverse=True)
        return self.sorted_stats
