import os.path
import pickle

class KeywordExtraction:
    def __init__(self, forum_nick, week_of_interest):
        self.forum_nick = forum_nick
        self.directory = forum_nick + "_weeks_pickle/"
        self.week = week_of_interest
        self.corpus = self.unpickle_corpus()
        print(self.corpus)

    def unpickle_corpus(self):
        file_name = self.forum_nick + ".pkl"
        full_path = os.path.join(self.directory + file_name)
        try:
            with open(full_path, "rb") as fin:
                corpus = pickle.load(fin)
                fin.close()
                return corpus
        except FileNotFoundError:
            print("Can't find file '%s' and/or directory '%s'" % (file_name, self.directory))

