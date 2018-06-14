import prepare_extraction
import prepare_og_files_weeks
import tfidf
import tfidf_two_steps

def prepare_files():
    prepare_og_files_weeks.PrepareOriginalFiles()
    prepare_og_files_weeks.Stopwords()

def do_tfidf(forum, week, number_of_stopwords, title_or_post):
    prepared_forum = prepare_extraction.Preparation(forum, week, number_of_stopwords, title_or_post)
    my_tfidf = tfidf.Tfidf(prepared_forum)
    #my_tfidf.count_tf()
    #my_tfidf.count_idf()
    my_tfidf.count_tfidf()

def do_stats(forum, week, number_of_stopwords, title_or_post):
    prepared_forum = prepare_extraction.Preparation(forum, week, number_of_stopwords, title_or_post)


    #Rake = Rake(KE)
    #Stats = Stats(KE)

# either this:
#prepare_files()
#tfidf_posts_as_doc("t", "2015-14", number_of_stopwords=200, content="both")
do_tfidf("l", "2015-14", number_of_stopwords=10, title_or_post="both")
#tfidf_two_step("l", "2015-14", number_of_stopwords=200, content="both")
# or this:
#KE.only_tfidf()
#KE.only_rake()
#KE.only_statistics()

