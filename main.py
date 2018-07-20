import prepare_extraction
import prepare_og_files_weeks
import tfidf
import pure_stats


def prepare_files():
    """
    Extract relevant info from all json-files and store to csv-files. Create stopword-txt for each forum.
    :return: saves csv-files to folder csv_files, and txt-files to folder stopword_files
    """
    prepare_og_files_weeks.PrepareOriginalFiles()
    prepare_og_files_weeks.Stopwords()


def prepare_forum(forum, week, number_of_stopwords, title_or_post, token_or_type):
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
    print("Number of stopwords =", number_of_stopwords)
    return prepare_extraction.Preparation(forum,
                                          week,
                                          number_of_stopwords,
                                          title_or_post,
                                          token_or_type,)


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
        list_of_keywords_tfidf.append(t[0])
    print("Keywords from TFIDF: ", list_of_keywords_tfidf)


def do_stats(my_forum, rare_threshold):
    my_stats_model = pure_stats.PureStatistics(my_forum, rare_threshold)
    #my_stats_model.count_stats()

    #Rake = Rake(KE)
    #Stats = Stats(KE)


#prepare_files()

print("*** Basic version:")
my_forum = prepare_forum("l", "2015-45", 10, "both", "token")
do_tfidf(my_forum)

print("\n*** Token only counted once per title, post or comment (I.e. 'a a b b c' = 'a b c', 'x x y' = 'x y'):")
my_forum = prepare_forum("l", "2015-45", 10, "both", "type")
do_tfidf(my_forum)


print("\n*** Word must appear in at least 4 titles/posts/comments to count. Every token counted (I.e. Basic version):")
my_forum = prepare_forum("l", "2015-45", 10, "both", "token")

print("\n*** Word must appear in at least 4 titles/posts/comments to count. Tokens counted once per title/post/c...:")
my_forum = prepare_forum("l", "2015-45", 10, "both", "token")

# do_stats(my_forum, rare_threshold=2)

