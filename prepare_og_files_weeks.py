import original_filenames
import json
import os
import datetime
import tag_text
import csv
import conllu
import sys
from collections import Counter
import re


class PrepareOriginalFiles:
    def __init__(self):
        self.dir_with_og_files = "original_files/"
        for forum in original_filenames.forums:
            self.counter = 0
            self.prepare_file(forum)

    def prepare_file(self, forum):
        """
        Call the methods to extract different information from original file and save info to csv files
        :param forum: path (string) to specific forum file in json format
        :return: calls function that store information to csv files
        """
        print("Preparing forum", forum)
        udpipe_model = self.identify_language(forum)
        path_to_og_file = os.path.join(self.dir_with_og_files, forum)
        forum_nick = forum[6]  # saves first letter in forum name
        list_w_data_from_og_file = self.extract_data_from_og_file(path_to_og_file)
        list_w_data_tuples = self.add_lemmas(list_w_data_from_og_file, udpipe_model)
        self.store_time_periods_csv_files(list_w_data_tuples, forum_nick)

    def identify_language(self, forum):
        """
        Identify language from forum file name and pick right udpipe-model
        (Check if char -7 to -5 is "sv" or "en")
        :param forum: path (string) to specific forum file in json format
        :return: path to correct UDPipe language model
        """
        language = forum[-7:-5]
        try:
            if language == "sv":
                return os.path.join("udpipe_models", "swedish-ud-2.0-170801.udpipe")
            if language == "en":
                return os.path.join("udpipe_models", "english-ud-2.0-170801.udpipe")
        except:  # Totally unnecessary since UDPipe raises it's own Exception. But, still.
            sys.exit("File name doesn't follow expected pattern and no language could be identified. Program exited.")

    def extract_data_from_og_file(self, og_file):
        """
        Extract info from forum file (json) and call functions that modifies it before saving.
        :param og_file: path (string) to specific forum file in json format
        :return: nested list. Sub lists = posting on forum, containing [week, type, title text, and posted text]
        """
        data_list = []
        with open(og_file, "r") as fin:
            og_forum = json.load(fin)
        for dialogs in og_forum["dialogs"]:
            self.counter += 1
            print(self.counter)
            dialog_title = self.extract_text(dialogs, "title") + "."
            dialog_text = self.extract_text(dialogs, "content_text")
            dialog_date = self.extract_date(dialogs)
            data_entry = [dialog_date, "op", dialog_title, dialog_text]
            data_list.append(data_entry)
            for comments in dialogs["comments"]:
                comment_text = self.extract_text(comments, "content_text")
                comment_date = self.extract_date(comments)
                data_entry = [comment_date, "comments", dialog_title, comment_text]
                data_list.append(data_entry)
        fin.close()
        return data_list

    def extract_text(self, text_field, part_to_extract):
        """
        Make text more readable
        :param text_field: dialog or comment from the forum
        :param part_to_extract: may be either "title" or "content_text"
        :return: same text, without new lines and double spaces
        """
        og_text = text_field[part_to_extract]
        text_no_new_line = og_text.replace("\n", " ")
        text_no_double_quotation = text_no_new_line.replace('"', " ")
        text_no_single_quotation = text_no_double_quotation.replace("'", " ")
        text_no_open_parentheses = text_no_single_quotation.replace("(", " ")
        text_no_closing_parentheses = text_no_open_parentheses.replace(")", " ")
        text_no_double_spaces = text_no_closing_parentheses.replace("  ", " ")
        og_text_list = text_no_double_spaces.split(" ")
        og_regex_text_list = []
        for i in og_text_list:
            # not sure about this regex, do I miss something _important_?
            if re.match(r'^(\w+[-/:]?\w*)([.,!?:;]*)?$', i):
                og_regex_text_list.append(i)
            elif re.match(r'^(\w+-\w*)*$', i):  # this allows words with two or more hyphens, ex "tycka-till-knapp"
                og_regex_text_list.append(i)
            elif re.match(r'^(\w+/\w*)*$', i):  # this allows words with two or more hyphens, ex "ett/två/tre"
                og_regex_text_list.append(i)
            else:
                pass
        og_new_text = " ".join(og_regex_text_list)
        final_text = og_new_text.replace("  ", " ")
        return final_text

    def extract_date(self, text_field):
        """
        Create date format with years and weeks
        (Change "yyyy-mm-dd hh:mm:ss" to "yyyy-ww")
        :param text_field: string "yyyy-mm-dd hh:mm:ss"
        :return: string "yyyy-ww" where ww == week number (with leading 0)
        """
        og_date = text_field["meta"]["published"]
        date_yyyy_int = int(og_date[:4])
        date_mm_int = int(og_date[5:7])
        date_dd_int = int(og_date[8:10])
        date_isocalendar = datetime.date(date_yyyy_int, date_mm_int, date_dd_int).isocalendar()
        date_yyyy = str(format(date_isocalendar[0], "04d"))
        date_ww = str(format(date_isocalendar[1], "02d"))
        the_date = date_yyyy + "-" + date_ww
        return the_date

    def add_lemmas(self, list_w_data_entries, udpipe_model):
        """
        Send text chunks to method for lemmatization and compile all info to list with tuples
        :param list_w_data_entries: nested list. Sub lists = [week, type, title text, and posted text]
        :param udpipe_model: path to UDPipe language model
        :return: list w tuples, (week, type, og title text, lemmatized title text, og posting, lemmatized posting)
        """
        list_w_tuples = []
        model = tag_text.Model(udpipe_model)
        for entry in list_w_data_entries:
            title_tokenized = model.tokenize(entry[2])
            title_lemmatized = self.tag_the_text(title_tokenized, model)
            text_tokenized = model.tokenize(entry[3])
            text_lemmatized = self.tag_the_text(text_tokenized, model)
            tuple_w_data = (entry[0],  # week
                            entry[1],  # type (either 'op' or 'comments')
                            entry[2],  # original title text
                            title_lemmatized,  # lemmatized title text
                            entry[3],  # original posted text
                            text_lemmatized,  # lemamtized posted text
                            )
            list_w_tuples.append(tuple_w_data)
        return list_w_tuples

    def tag_the_text(self, text_chunk, model):
        """
        Send string to UDPipe for lemmatization (and POS-tagging but only lemmatized text saved)
        :param text_chunk: string
        :param model: Loaded UDPipe model
        :return: lemmatized text chunk (string)
        """
        words_as_lemma = []
        for sentence in text_chunk:
            model.tag(sentence)
        conllu_format = model.write(text_chunk, "conllu")
        for sentence in conllu.parse(conllu_format):
            for word in sentence:
                if word["upostag"] != "PUNCT":
                    lower_word = word["lemma"].lower()
                    words_as_lemma.append(lower_word)
        sentence_as_lemma = " ".join(words_as_lemma)
        return sentence_as_lemma

    def store_time_periods_csv_files(self, data_list, forum_nick):
        """
        Write content of a list to csv file named [forum ID].csv in subdirectory "csv_files"
        :param data_list: list w tuples, (week, type, og title, lemmatized title, og posting, lemmatized posting)
        :param forum_nick: forum ID (first letter of forum name)
        :return: save content of data_list to csv file
        """
        subdir_csv_files = "csv_files"
        csv_outfile_name = forum_nick + ".csv"
        full_path_to_file = os.path.join(subdir_csv_files, csv_outfile_name)
        if check_if_file_exist_already(full_path_to_file) == "Go ahead and create the files!":
            with open(full_path_to_file, "w", newline="") as csv_fout:
                csv_writer = csv.writer(csv_fout, delimiter="\t", quotechar='"', quoting=csv.QUOTE_ALL)
                csv_writer.writerow(["week",
                                     "text type",
                                     "title",
                                     "title_lemmatized",
                                     "text",
                                     "text_lemmatized",
                                     ])
                csv_writer.writerows(i for i in data_list)
            csv_fout.close()
        else:
            pass


class Stopwords:
    def __init__(self):
        for dirpath, dirname, filenames in os.walk("csv_files"):
            for f in filenames:
                forum_nick = f[0]
                print("Creating stopwords for", forum_nick)
                file_path = os.path.join(dirpath, f)
                list_all_words = self.collect_words(file_path)
                frequencies = self.count_frequencies(list_all_words)
                self.save_to_file(frequencies, forum_nick)

    def collect_words(self, filename):
        """
        Look through all "text_lemmatized" in csv file and save tokens to big list
        IMPORTANT! Not looking through "title_lemmatized"
        :param filename: string with subdir and filename, ex: "csv_files/l.csv"
        :return: list with all tokens in forum appearing in either OP or comments
        """
        list_of_words = []
        with open(filename, "r") as fin:
            data = csv.DictReader(fin, delimiter="\t")
            for row in data:
                mini_list = row['text_lemmatized'].split(" ")
                for i in mini_list:
                    list_of_words.append(i)
        fin.close()
        return list_of_words

    def count_frequencies(self, list_w_words):
        """
        Count every type in list with words, save to new list sorted by frequency, falling order
        :param list_w_words: list with all tokens
        :return: list with types, sorted by frequency in falling order
        """
        counted = Counter(list_w_words)
        frequency_list = sorted(
            counted,
            key=counted.__getitem__,
            reverse=True,
        )
        return frequency_list

    def save_to_file(self, frequencies, forum_nick):
        """
        If a stopword file doesn't already exist, save all types in forum to a file, sorted by frequency
        :param frequencies: list with types, sorted by frequency in falling order
        :param forum_nick: name of forum, ex "k" or "t"
        :return: write file w all types in forum. Path ex: "stopword_files/k_stopwords.txt"
        """
        subdir_stopword_files = "stopword_files"
        stopword_file_name = forum_nick + "_stopwords.txt"
        full_path_to_file = os.path.join(subdir_stopword_files, stopword_file_name)
        if check_if_file_exist_already(full_path_to_file) == "Go ahead and create the files!":
            with open(full_path_to_file, "w", newline="") as fout:
                for word in frequencies:
                    fout.write("%s\n" % word)
            fout.close()
        else:
            pass


def check_if_file_exist_already(full_path_to_file):
    """
    Check if file already exist. If it does, gives you option to overwrite it.
    :param full_path_to_file: path to csv file in subdirectory
    :return: string telling you to either save to file or not
    """
    if not os.path.isfile(full_path_to_file):
        return "Go ahead and create the files!"
    else:
        print("File '%s' already exists." % full_path_to_file)
    overwrite = input("Do you want to overwrite it? \ny/n\n")
    if overwrite == "y" or overwrite == "Y":
        return "Go ahead and create the files!"
    else:
        return "File already exist, don't overwrite!"
