import original_filenames
import json
import os
import datetime
import tag_text
import csv
import conllu

class PrepareOriginalFiles:
    def __init__(self):
        self.dir_with_og_files = "original_files/"
        for forum in original_filenames.forums:
            self.prepare_file(forum)

    def prepare_file(self, forum):
        udpipe_model = ""
        language = forum[-7:-5]
        if language == "sv":
            udpipe_model = os.path.join("udpipe_models", "swedish-ud-2.0-170801.udpipe")
        if language == "en":
            udpipe_model = os.path.join("udpipe_models", "english-ud-2.0-170801.udpipe")
        path_to_og_file = os.path.join(self.dir_with_og_files, forum)
        forum_nick = forum[6]  # saves first letter in forum name
        list_w_data_from_og_file = self.extract_data_from_og_file(path_to_og_file)
        list_w_data_tuples = self.add_lemmas(list_w_data_from_og_file, udpipe_model)
        self.store_time_periods_csv_files(list_w_data_tuples, forum_nick)

    def extract_data_from_og_file(self, og_file):
        """
        todo: update this
        """
        data_list = []
        with open(og_file, "r") as fin:
            og_forum = json.load(fin)
        for dialogs in og_forum["dialogs"]:
            dialog_title = self.extract_text(dialogs, "title") + "."
            dialog_text = self.extract_text(dialogs, "content_text")
            dialog_date = self.extract_date(dialogs)
            data_entry = [dialog_date, "content_text", dialog_title, dialog_text]
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
        the_text = text_no_new_line.replace("  ", " ")
        return the_text

    def extract_date(self, text_field):
        """
        Create date format with years and weeks
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
        list_w_tuples = []
        model = tag_text.Model(udpipe_model)
        for entry in list_w_data_entries:
            title_tokenized = model.tokenize(entry[2])
            title_lemmatized = self.tag_the_text(title_tokenized, model)
            text_tokenized = model.tokenize(entry[3])
            text_lemmatized = self.tag_the_text(text_tokenized, model)
            tuple_w_data = (entry[0],
                            entry[1],
                            entry[2],
                            title_lemmatized,
                            entry[3],
                            text_lemmatized,
                            )
            list_w_tuples.append(tuple_w_data)
        return list_w_tuples

    def tag_the_text(self, text_chunk, model):
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
        subdir_csv_files = "csv_files"
        csv_outfile_name = forum_nick + ".csv"
        full_path_to_file = os.path.join(subdir_csv_files, csv_outfile_name)
        if self.check_if_file_exist_already(full_path_to_file) == "Go ahead and create the files!":
            with open(full_path_to_file, "w", newline="") as csv_fout:
                csv_writer = csv.writer(csv_fout, delimiter="\t", quotechar='"', quoting=csv.QUOTE_ALL)
                csv_writer.writerow(["Week",
                                     "text type",
                                     "title",
                                     "title_lemmatized",
                                     "text",
                                     "text_lemmatized",
                                     ])
                csv_writer.writerows(i for i in data_list)
            csv_fout.close()

    def check_if_file_exist_already(self, full_path_to_file):
        if os.path.isfile(full_path_to_file) == False:
            return "Go ahead and create the files!"
        else:
            print("File '%s' already exists." % full_path_to_file)
        overwrite = input("Do you want to overwrite it? \ny/n\n")
        if overwrite == "y" or overwrite == "Y":
            return "Go ahead and create the files!"
        else:
            return "File already exist, don't overwrite!"