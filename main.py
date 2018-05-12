import prepare_extraction
import prepare_og_files_weeks
import tfidf
import tfidf_two_steps

def prepare_files():
    prepare_og_files_weeks.PrepareOriginalFiles()
    prepare_og_files_weeks.Stopwords()

"""def tfidf_posts_as_doc(forum, week, number_of_stopwords, content):
    prepared_forum = prepare_extraction.Preparation(forum, week, number_of_stopwords, content)
    my_tfidf = tfidf.Tfidf(prepared_forum)
    my_tfidf.parse_doc_data()
    my_tfidf.count_tf()
    my_tfidf.count_idf_posts_as_doc()
    my_tfidf.count_tfidf(my_tfidf.idf_posts_as_doc)
"""

def tfidf_week_as_doc(forum, week, number_of_stopwords, content):
    prepared_forum = prepare_extraction.Preparation(forum, week, number_of_stopwords, content)
    my_tfidf = tfidf.Tfidf(prepared_forum)
    my_tfidf.parse_doc_data()
    my_tfidf.count_tf()
    my_tfidf.count_idf_weeks_as_doc()
    my_tfidf.count_tfidf(my_tfidf.idf_weeks_as_doc)

"""def tfidf_two_step(forum, week, number_of_stopwords, content):
    prepared_forum = prepare_extraction.Preparation(forum, week, number_of_stopwords, content)
    my_two_step = tfidf_two_steps.Tfidf(prepared_forum)
    my_two_step.parse_doc_data()
    my_two_step.count_tf()
    my_two_step.count_idf_posts_as_doc()
    my_two_step.count_tfidf(my_two_step.idf_posts_as_doc)
    my_two_step.create_new_doc_from_sorted()
"""

    #Rake = Rake(KE)
    #Stats = Stats(KE)

# either this:
#prepare_files()
#tfidf_posts_as_doc("t", "2015-14", number_of_stopwords=200, content="both")
tfidf_week_as_doc("l", "2015-14", number_of_stopwords=200, content="both")
#tfidf_two_step("l", "2015-14", number_of_stopwords=200, content="both")
# or this:
#KE.only_tfidf()
#KE.only_rake()
#KE.only_statistics()

