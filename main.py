import prepare_extraction
import prepare_og_files_weeks
import tfidf
import pure_stats


def prepare_files():
    """
    Extract relevant info from all json-files and store to csv-files. Create stopword-txt for each forum.
    :return: saves csv-files to folder csv_files, and txt-files to stopword_files
    """
    prepare_og_files_weeks.PrepareOriginalFiles()
    prepare_og_files_weeks.Stopwords()


def prepare_forum(forum, week, number_of_stopwords, title_or_post, token_or_type):
    """
    Create an object containing all info needed for different KE methods stored in attributes
    :param forum: The forum nick, ex: "k" or "l"
    :param week: The Week Of Interest, ex "2015-14"
    :param number_of_stopwords: defaults to 100
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
                                          token_or_type,)


def do_tfidf_max_occurences(my_forum):
    """
    Count TF*IDF for types in Week In Question. Term frequency algorithm = token count/max_occurences
    :param my_forum: forum object prepared for KE
    :return: TF*IDF-value stored in my_tfidf.sorted_tfidf, ex [("word1", 0.789), ("word2", 0.6514), ("word3", 0.2), ...]
    """
    print("Counting TF*IDF with token count divided by maximum occurences")
    my_tfidf = tfidf.Tfidf(my_forum)
    my_tfidf.count_tfidf(tf_equation="maximum occurencies")
    print("Sorted TFIDF(tf equation = max occurences)", my_tfidf.sorted_tfidf)


def do_tfidf_tokens_in_doc(my_forum):
    """
    Count TF*IDF for types in Week In Question. Term frequency algorithm = token count/number_tokens_in_document
    :param my_forum: forum object prepared for KE
    :return: TF*IDF-value stored in my_tfidf.sorted_tfidf, ex [("word1", 0.078), ("word2", 0.065), ("word3", 0.02), ...]
    """
    print("Counting TF*IDF with token count divided by total number of tokens in document")
    my_tfidf = tfidf.Tfidf(my_forum)
    my_tfidf.count_tfidf(tf_equation="number tokens in doc")
    print("Sorted TFIDF(tf equation = tokens in doc)", my_tfidf.sorted_tfidf)


def do_stats(my_forum, rare_threshold):
    my_stats_model = pure_stats.PureStatistics(my_forum, rare_threshold)
    #my_stats_model.count_stats()

    #Rake = Rake(KE)
    #Stats = Stats(KE)


# either this:
#prepare_files()
#tfidf_posts_as_doc("t", "2015-14", number_of_stopwords=200, content="both")
print("*** Every token in title/post/comment is counted:")
my_forum = prepare_forum("l", "2015-52", number_of_stopwords=10, title_or_post="both", token_or_type="token")
do_tfidf_max_occurences(my_forum)
do_tfidf_tokens_in_doc(my_forum)
print("\n*** Every type only counted once per title/post/comment:")
my_forum = prepare_forum("l", "2015-52", number_of_stopwords=10, title_or_post="both", token_or_type="type")
do_tfidf_max_occurences(my_forum)
do_tfidf_tokens_in_doc(my_forum)
# do_stats(my_forum, rare_threshold=2)
# tfidf_two_step("l", "2015-14", number_of_stopwords=200, content="both")
# or this:
# KE.only_tfidf()
# KE.only_rake()
# KE.only_statistics()

