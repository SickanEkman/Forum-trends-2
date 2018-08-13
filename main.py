import prepare_extraction
import prepare_og_files_weeks
import tfidf
import pure_stats


forum_nick = "l"
week = "2015-25"


def prepare_files():
    """
    Extract relevant info from all json-files and store to csv-files. Create stopword-txt for each forum.
    :return: saves csv-files to folder csv_files, and txt-files to folder stopword_files
    """
    prepare_og_files_weeks.PrepareOriginalFiles()
    prepare_og_files_weeks.Stopwords()


def prepare_forum(forum,
                  week,
                  number_of_stopwords,
                  title_or_post,
                  token_or_type,
                  ):
    """
    Create an object containing all info needed for different KE methods stored in attributes
    :param forum: The forum nick, ex: "k" or "l"
    :param week: The Week Of Interest, ex "2015-14"
    :param number_of_stopwords: defaults to 20
    :param title_or_post: defaults to "both". Can also be "title" or "post"
        If title, only lemmatized titles is stored in week_data & corpus_data (once for each post/comment in thread)
        If post, only lemmatizes posts/comments are stored in week_data & corpus_data
    :param token_or_type: defaults to "token".
        If token, every occurence of a lemma is counted.
        If type, each lemma is counted only once per post/comment/title.
    :return: An object with attributes:
        self.forum_file_name, ex "k.csv"
        self.path_to_csv_file, ex "csv_files/k.csv"
        self.stopword_file, ex "k_stopwords.txt"
        self.path_to_stopword_file, ex "stopword_files/k_stopwords.txt"
        self.week, ex "2015-14"
        self.content_type, either "title", "post", or "both"
        self.stopwords, ex ("the", "and", "or", ...) whith len == number of stopwords
        self.week_data, list w posts and/or headings from the week in question as items
        self.corpus_data, dictionary with week as key, and list with posts and/or headings as value
    """
    print("Creating a Forum Object")
    return prepare_extraction.Preparation(forum,
                                          week,
                                          number_of_stopwords,
                                          title_or_post,
                                          token_or_type,
                                          )


def do_tfidf(my_forum):
    """
    Count TF*IDF for types in Week In Question.
    :param my_forum: forum object prepared for KE
    :return: print list with the final n keywords, in order.
    """
    print("Counting TF*IDF...")
    my_tfidf = tfidf.Tfidf(my_forum)
    my_tfidf.count_tfidf()

    number_of_keywords = 20
    list_of_keywords_tfidf = []
    for t in my_tfidf.sorted_tfidf[:number_of_keywords]:
        list_of_keywords_tfidf.append((t[0], t[1]))
    return list_of_keywords_tfidf


def do_stats(my_forum, mean_or_median, subtract_sd, rare_threshold):
    print("Counting stats...")
    my_stats_model = pure_stats.PureStatistics(my_forum, mean_or_median, subtract_sd, rare_threshold)

    number_of_keywords = 20
    list_of_keywords_stats = []
    for t in my_stats_model.sorted_stats[:number_of_keywords]:
        list_of_keywords_stats.append((t[0], t[1]))
    return list_of_keywords_stats

def write_results_to_file(list_of_keywords, method_specs):
    full_path_to_file = "results/" + forum_nick + "_" + week + ".txt"
    with open(full_path_to_file, "a") as fout:
        fout.write("\n\n" + method_specs + "\n")
        for i in list_of_keywords:
            fout.write(i[0]+"\t")
    fout.close()

def write_method_version_to_file(info):
    full_path_to_file = "results/" + forum_nick + "_" + week + ".txt"
    with open(full_path_to_file, "a") as fout:
        fout.write("\n\n" + info)
    fout.close()

stopwords = 10

rare_threshold_for_stats = 2

#prepare_files()

info = "\n*** Basic version, title only:"
write_method_version_to_file(info)
my_forum = prepare_forum(forum_nick, week, stopwords, "title", "token")
my_list = do_tfidf(my_forum)
write_results_to_file(my_list, "tfidf:")
my_list = do_stats(my_forum, "mean", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, NOT substracting SD")
my_list = do_stats(my_forum, "mean", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, substracting SD")
my_list = do_stats(my_forum, "median", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, NOT substracting SD")
my_list = do_stats(my_forum, "median", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, substracting SD")

info = "*** Basic version, post only:"
write_method_version_to_file(info)
my_forum = prepare_forum(forum_nick, week, stopwords, "post", "token")
my_list = do_tfidf(my_forum)
write_results_to_file(my_list, "tfidf:")
my_list = do_stats(my_forum, "mean", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, NOT substracting SD")
my_list = do_stats(my_forum, "mean", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, substracting SD")
my_list = do_stats(my_forum, "median", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, NOT substracting SD")
my_list = do_stats(my_forum, "median", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, substracting SD")

info = "*** Basic version, both title and post:"
write_method_version_to_file(info)
my_forum = prepare_forum(forum_nick, week, stopwords, "both", "token")
my_list = do_tfidf(my_forum)
write_results_to_file(my_list, "tfidf:")
my_list = do_stats(my_forum, "mean", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, NOT substracting SD")
my_list = do_stats(my_forum, "mean", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, substracting SD")
my_list = do_stats(my_forum, "median", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, NOT substracting SD")
my_list = do_stats(my_forum, "median", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, substracting SD")

info = "*** Token only counted once per title, post or comment, only title:"
write_method_version_to_file(info)
my_forum = prepare_forum(forum_nick, week, stopwords, "title", "type")
my_list = do_tfidf(my_forum)
write_results_to_file(my_list, "tfidf:")
my_list = do_stats(my_forum, "mean", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, NOT substracting SD")
my_list = do_stats(my_forum, "mean", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, substracting SD")
my_list = do_stats(my_forum, "median", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, NOT substracting SD")
my_list = do_stats(my_forum, "median", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, substracting SD")

info = "*** Token only counted once per title, post or comment, only post:"
write_method_version_to_file(info)
my_forum = prepare_forum(forum_nick, week, stopwords, "post", "type")
my_list = do_tfidf(my_forum)
write_results_to_file(my_list, "tfidf:")
my_list = do_stats(my_forum, "mean", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, NOT substracting SD")
my_list = do_stats(my_forum, "mean", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, substracting SD")
my_list = do_stats(my_forum, "median", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, NOT substracting SD")
my_list = do_stats(my_forum, "median", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, substracting SD")

info = "*** Token only counted once per title, post or comment, both title and post:"
write_method_version_to_file(info)
my_forum = prepare_forum(forum_nick, week, stopwords, "both", "type")
my_list = do_tfidf(my_forum)
write_results_to_file(my_list, "tfidf:")
my_list = do_stats(my_forum, "mean", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, NOT substracting SD")
my_list = do_stats(my_forum, "mean", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with mean, substracting SD")
my_list = do_stats(my_forum, "median", False, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, NOT substracting SD")
my_list = do_stats(my_forum, "median", True, rare_threshold_for_stats)
write_results_to_file(my_list, "Stats with median, substracting SD")

