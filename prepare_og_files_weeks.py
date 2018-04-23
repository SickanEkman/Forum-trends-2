import original_filenames
import json
import collections
import os.path
import datetime
import pickle
import tag_text
import csv


class PrepareOriginalFiles:
    def __init__(self):
        self.dir_with_og_files = "original_files/"
        for forum in original_filenames.forums:
            self.prepare_files(forum)

    def prepare_files(self, forum):
        language = forum[-7:-5]
        #if language == "sv":
        #    udpipe_model = #todo: continue here!!!
        path_to_file = os.path.join(self.dir_with_og_files, forum)
        forum_nick = forum[6]  # saves first letter in forum name
        data = self.extract_data_of_interest(path_to_file)
        #subdir_txt = forum_nick + "_weeks_readable"
        self.store_time_periods_csv_files(data, forum_nick)

    '''    if self.check_if_dir_exists(subdir_txt) == "Go ahead and create the files!":
            self.store_time_periods_to_txt_files(data, forum_nick)
        else:
            pass
        subdir_pkl = forum_nick + "_weeks_pickle"
        if self.check_if_dir_exists(subdir_pkl) == "Go ahead and create the files!":
            self.store_time_periods_to_pkl_file(data, forum_nick)
        else:
            pass
    '''

    def extract_data_of_interest(self, og_file):
        """
        todo: update this
        """
        data = collections.defaultdict(list)
        data_list_w_tuples = []
        with open(og_file, "r") as fin:
            og_forum = json.load(fin)
        for dialogs in og_forum["dialogs"]:
            dialog_title = self.extract_text(dialogs, "title") + "."
            dialog_text = self.extract_text(dialogs, "content_text")
            dialog_date = self.extract_date(dialogs)
            data_tuple = (dialog_date, "content_text", dialog_title, dialog_text)
            data_list_w_tuples.append(data_tuple)
            #data[dialog_date].append((dialog_title, dialog_text))
            for comments in dialogs["comments"]:
                comment_text = self.extract_text(comments, "content_text")
                comment_date = self.extract_date(comments)
                data_tuple = (comment_date, "comments", dialog_title, comment_text)
                data_list_w_tuples.append(data_tuple)
                #data[comment_date].append((dialog_title, comment_text))
        fin.close()
        #return data
        return data_list_w_tuples

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

    def check_if_dir_exists(self, subdir):
        try:
            os.mkdir(subdir)
            return "Go ahead and create the files!"
        except FileExistsError:
            print("Directory '%s' already exists." % subdir)
            overwrite = input("Do you want to overwrite it? \ny/n\n")
            if overwrite == "y" or overwrite == "Y":
                return "Go ahead and create the files!"
            else:
                return "Directory already exist, don't overwrite!"

    def store_time_periods_to_txt_files(self, data_dict, file_name):
        """
        todo: update this
        """
        subdir_txt = file_name + "_weeks_readable"
        for date, texts in data_dict.items():
            outfile_name = file_name + "_" + date + ".txt"
            with open(os.path.join(subdir_txt, outfile_name), "w") as txt_fout:
                for text in texts:
                    txt_fout.write(text[0] + " ")
                    txt_fout.write(text[1])
            txt_fout.close()

    def store_time_periods_to_pkl_file(self, data_dict, file_name):
        subdir_pkl = file_name + "_weeks_pickle"
        pkl_outfile_name = file_name + ".pkl"
        with open(os.path.join(subdir_pkl, pkl_outfile_name), "wb") as pkl_fout:
            pickle.dump(data_dict, pkl_fout)
        pkl_fout.close()

    def store_time_periods_csv_files(self, data_list, forum_nick):
        subdir_csv_files = forum_nick + "_weeks_csv"
        if self.check_if_dir_exists(subdir_csv_files) == "Go ahead and create the files!":
            csv_outfile_name = forum_nick + ".csv"
            with open(os.path.join(subdir_csv_files, csv_outfile_name), "w", newline="") as csv_fout:
                csv_writer = csv.writer(csv_fout, delimiter="\t", quotechar='"', quoting=csv.QUOTE_ALL)
                csv_writer.writerow(["Week", "text type", "title", "text"])
                csv_writer.writerows(i for i in data_list)
            csv_fout.close()



    def create_conllu_files(self):
        file_list = []
        model = tag_text.Model(training_file)
        for dirpath, dirnames, filenames in os.walk(directory_name):
            for filename in filenames:
                if filename.endswith("txt"):
                    file_list.append(os.path.join(dirpath, filename))
            for f in file_list:
                with open(f, "r") as fin:
                    forum_text = fin.read()
                    sentences = model.tokenize(forum_text)
                    for s in sentences:
                        model.tag(s)
                    conllu = model.write(sentences, "conllu")

                    print(conllu)
                    go_on = input("continue?")

                    outfile_name = f[9:18] + ".conllu"
                    with open(os.path.join(dirpath, outfile_name), "w") as fout:
                        fout.write(conllu)
                    fout.close()
                fin.close()