import os
import csv
import collections
import sys


class Preparation:
    def __init__(self, forum_nick, week_of_interest, number_of_stopwords=50, title_or_post="both"):
        """
        initialize the preparation object, give it attributes
        :param forum_nick: a letter ID:ing the forum, ex "k"
        :param week_of_interest: yyyy-ww
        :param number_of_stopwords: defults to 50
        """
        self.forum_file_name = forum_nick + ".csv"  # string
        self.path_to_csv_file = os.path.join("csv_files", self.forum_file_name)  # string
        self.stopword_file = forum_nick + "_stopwords.txt"  # string
        self.path_to_stopword_file = os.path.join("stopword_files", self.stopword_file)  # string
        self.week = week_of_interest  # string
        self.content_type = title_or_post  # string. Just "title", just "post", or "both"

        self.stopwords = self.create_stopwords(number_of_stopwords)  # set
        self.week_data = []
        self.corpus_data = collections.defaultdict(list)
        self.number_tokens_in_week = 0
        self.collect_data()

    def create_stopwords(self, number_of_stopwords):
        """
        Collect the most frequent words from the stopword file
        :return: A set containing the n most frequent stopwords from the forum
        """
        set_of_stopwords = set()
        all_stopwords = self.open_file(self.path_to_stopword_file)
        list_w_stopwords = all_stopwords.split("\n")
        for word in list_w_stopwords[:number_of_stopwords]:
            set_of_stopwords.add(word)
        return set_of_stopwords

    def open_file(self, path):
        try:
            with open(path, "r") as fin:
                data = fin.read()
                return data
        except FileNotFoundError:
            print("Can't find file '%s'" % self.path_to_stopword_file)

    def collect_data(self):
        """
        Call method to query database that collects text, either the titles or texts or both
        Call method to count the total number of tokens in Week of Interest
        """
        if self.content_type == "title" or self.content_type == "both":
            self.query_database("title_lemmatized")
        if self.content_type == "post" or self.content_type == "both":
            self.query_database("text_lemmatized")
        self.count_number_tokens_in_week()

    def query_database(self, header):
        """
        Collect posts from csv files and saves them to forum object
        :param header: Either 'title_lemmatized' or 'text_lemmatized'
        :return: add posts to:
            self.week_data (list w all text from the week in question)
            self.corpus_data (dict w k=week, v=list w texts) NOT INCLUDING WEEK IN QUESTION
        """
        try:
            with open(self.path_to_csv_file, "r") as fin:
                data = csv.DictReader(fin, delimiter="\t")
                for row in data:
                    if row["week"] == self.week:
                        self.week_data.append(row[header])
                    else:
                        self.corpus_data[row["week"]].append(row[header])
            if len(self.week_data) == 0:
                print("No posts for the specified week in file '%s'\nProgram closed" % self.path_to_csv_file)
                sys.exit()
            fin.close()
            return self.week_data, self.corpus_data
        except FileNotFoundError:
            print("Can't find file '%s'" % self.path_to_csv_file)

    def count_number_tokens_in_week(self):
        for item in self.week_data:
            self.number_tokens_in_week += len(item.split(" "))
