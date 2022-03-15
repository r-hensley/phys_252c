import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, classification_report
from matplotlib import pyplot as plt


def import_csv() -> (list[str], list[str]):
    english: list[str] = []
    spanish: list[str] = []
    for csv_name in ['principiante.csv', 'avanzado.csv', 'beginner.csv', 'advanced.csv']:
        with open(f"./{csv_name}", newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                message_text = row[2]
                if len(message_text) < 20:
                    continue
                if csv_name in ['principiante.csv', 'avanzado.csv']:
                    if len(spanish) > 10000:
                        # continue
                        pass
                    spanish.append(message_text)
                else:
                    if len(english) > 10000:
                        # continue
                        pass
                    english.append(message_text)

    return english, spanish


english, spanish = import_csv()

# Example of word vectorizer
text = ['this is english english six six six six six six five five five',
        'this is more english', 'hello english', 'LOUD VOICES five five']
# word_vectorizer = CountVectorizer(analyzer="word")  # Identifies all unique words
# fit = word_vectorizer.fit_transform(text)
# feature_names = word_vectorizer.get_feature_names_out()
# counts_array = fit.toarray()
# sums = [(sum(j), feature_names[i]) for i, j in enumerate(np.transpose(counts_array))]
# ngram_counts = sorted(sums, key=lambda x: x[0], reverse=True)
# print(counts_array)
# print(np.shape(counts_array))
# print(np.transpose(counts_array))
# print(sums)
# counts = {}
# for row in counts_array:
#     for word_index, count in enumerate(row):
#         name = feature_names[word_index]
#         counts[name] = counts.get(name, 0) + count
# print(counts)

# Example of character vectorizer
char_vectorizer = CountVectorizer(analyzer="char", ngram_range=(2, 2))  # All unique length-2 character ngrams
char_vectorizer.fit_transform(text)
# print(char_vectorizer.get_feature_names_out())
# [' e' ' i' 'en' 'gl' 'hi' 'is' 'li' 'ng' 's ' 'sh' 'th']

# Example of character vectorizer with word boundary option
char_wb_vectorizer = CountVectorizer(analyzer="char_wb", ngram_range=(2, 2))  # All unique length-2 character ngrams
char_wb_vectorizer.fit_transform(text)
# print(char_wb_vectorizer.get_feature_names_out())
# [' e' ' i' ' t' 'en' 'gl' 'h ' 'hi' 'is' 'li' 'ng' 's ' 'sh' 'th']

# Preliminarily get number of unique words/ngrams in each English/Spanish data set
word_vectorizer_2 = CountVectorizer(analyzer="word")  # , ngram_range=(2, 2))  # Identifies all unique words
word_vectorizer_2.fit_transform(english)
feature_names_english = word_vectorizer_2.get_feature_names_out()
# print(f"{len(feature_names_english)=}")
# print(f"{feature_names_english[500:515]=}")
word_vectorizer_2.fit_transform(spanish)

feature_names_spanish = word_vectorizer_2.get_feature_names_out()
# print(f"{len(feature_names_spanish)=}")
# print(f"{feature_names_spanish[400:415]=}")

# when using word analyzer, length of feature names is 13276/17793
# when using (2, 2) char analyzer, length of feature names is 1343/1434
# when using (1, 3) char analyzer, length of feature names is 10213/11120
# when using (3, 3) char analyzer, length of feature names is 8726/9536
# when using (2, 4) char analyzer, length of feature names is 43427/46211


def plot_unique_words_per_message():
    number_of_messages = np.array([])
    number_of_unique_words = np.array([])
    # Calculate how quickly number of unique words
    for number in list(range(1, 999, 10)) + list(range(1000, len(english), 1000)):
        vectorizer = CountVectorizer(analyzer="word")
        vectorizer.fit_transform(english[:number])
        number_of_messages = np.append(number_of_messages, number)
        number_of_unique_words = np.append(number_of_unique_words, len(vectorizer.get_feature_names_out())/number)

    plot, axis = plt.subplots()
    axis.plot(number_of_messages, number_of_unique_words)
    axis.set_title("Number of unique words per message")
    axis.set_xlabel("Number of messages")
    axis.set_ylabel("Unique words per message")
    # plt.xlim(-100, 10000)
    plt.xlim(left=-100)
    plt.ylim(bottom=0)
    plt.show()
# plot_unique_words_per_message()


def make_set(_english, _spanish, pipeline=None, print_results=False):
    if pipeline:
        eng_pred = pipeline.predict(_english)
        sp_pred = pipeline.predict(_spanish)
        new_english = []
        new_spanish = []
        for i in range(len(_english)):
            if eng_pred[i] == 'en':
                new_english.append(_english[i])
            else:
                print(f"False English: {_english[i]}")
        for i in range(len(_spanish)):
            if sp_pred[i] == 'sp':
                new_spanish.append(_spanish[i])
            else:
                print(f"False Spanish: {_spanish[i]}")
        _spanish = new_spanish
        _english = new_english

    x = np.array(_english + _spanish)  # An array with all messages
    y = np.array(['en'] * len(_english) + ['sp'] * len(_spanish))  # An array identifying the language of each message
    together = np.array(
        [(x[i], y[i]) for i, _ in enumerate(x)]
    )  # Combine the arrays into a linked array like [(message_1, lang), (message_2, lang), ...]
    np.random.shuffle(together)  # Shuffle the above array
    x = np.array([i[0] for i in together])  # Split the arrays again
    y = np.array([i[1] for i in together])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

    cnt = CountVectorizer(analyzer='char', ngram_range=(2, 2))
    cnt1 = CountVectorizer(analyzer='word', token_pattern=r"\S{2}")
    cnt2 = CountVectorizer(analyzer='word', token_pattern=r"\S{2}")

    pipeline = Pipeline([
        ('vectorizer', cnt),
        ('model', MultinomialNB())
    ])

    pipeline.fit(x_train, y_train)
    y_pred = pipeline.predict(x_test)

    # Get most common ngrams
    eng = cnt1.fit_transform(_english)
    spa = cnt2.fit_transform(_spanish)
    for lang in [(eng, cnt1), (spa, cnt2)]:
        feature_names = lang[1].get_feature_names_out()
        counts_array = lang[0].toarray()
        sums = [(sum(j), feature_names[i]) for i, j in enumerate(np.transpose(counts_array))]
        most_common_ngrams = sorted(sums, key=lambda i: i[0], reverse=True)
        print(most_common_ngrams[:30])

    if print_results:
        print(f"{pipeline=}\n")
        print(f"{type(pipeline)=}\n")
        print(confusion_matrix(y_test, y_pred))
        print()
        print(classification_report(y_test, y_pred))
        print()

    return pipeline


# print(len(english))  # 39394
# print(sum([len(i) for i in english]))  # 1041876
# print(len(spanish))  # 35917
# print(sum([len(i) for i in spanish]))  # 835712

# iteration_one = make_set(english, spanish, pipeline=None)
# iteration_two = make_set(english, spanish, pipeline=iteration_one)
# langdetect = make_set(english, spanish, pipeline=iteration_two, print_results=True)
langdetect = make_set(english, spanish, pipeline=None, print_results=False)


def detect_language(text):
    probs = langdetect.predict_proba([text])[0]
    if probs[0] > 0.9:
        return 'en', probs[0]
    elif probs[0] < 0.1:
        return 'sp', probs[0]
    else:
        return '??', probs[0]


messages = ['hello this is english',
            'y ahora esto es espanol',
            "cette fois, c'est francais",
            "this time, this is french",
            "wie sieht deutsch aus",
            "and this is german",
            "forse l'italiano e simile",
            "maybe italian is similar",
            "talvez portugues seja similar",
            "maybe portuguese is similar",
            'kore ha nihongo nan dakedo',
            "now this is just japanese"]

# Word ngrams
# en (0.99) --> hello this is english
# sp (0.05) --> y ahora esto es espanol
# en (0.56) --> cette fois, c'est francais
# en (1.0) --> this time, this is french
# en (0.56) --> wie sieht deutsch aus
# en (0.99) --> and this is german
# en (0.56) --> forse l'italiano e simile
# en (0.68) --> maybe italian is similar
# en (0.56) --> talvez portugues seja similar
# en (0.68) --> maybe portuguese is similar
# en (0.56) --> kore ha nihongo nan dakedo
# en (1.0) --> now this is just japanese

# 2x2 char ngrams
# en (1.0) --> hello this is english
# sp (0.0) --> y ahora esto es espanol
# en (1.0) --> cette fois, c'est francais
# en (1.0) --> this time, this is french
# en (1.0) --> wie sieht deutsch aus
# en (1.0) --> and this is german
# sp (0.1) --> forse l'italiano e simile
# en (1.0) --> maybe italian is similar
# sp (0.0) --> talvez portugues seja similar
# en (0.11) --> maybe portuguese is similar
# en (0.94) --> kore ha nihongo nan dakedo
# en (1.0) --> now this is just japanese


for message in messages:
    lang, probs = detect_language(message)
    print(f"{lang} ({round(probs, 2)}) --> {message}")

# Most common words:
# [(5079, 'you'), (4881, 'the'), (4475, 'to'), (2936, 'it'), (2683, 'and'), (2604, 'is'), (2309, 'that'),
# (2269, 'in'), (2086, 'of'), (1725, 'but'), (1511, 'have'), (1478, 'are'), (1431, 'im'), (1397, 'my'), (1349, 'like'),
# (1327, 'its'), (1272, 'for'), (1255, 'what'), (1249, 'dont'), (1166, 'not'), (1113, 'me'), (1074, 'do'),
# (1022, 'was'), (966, 'so'), (936, 'just'), (931, 'with'), (871, 'be'), (850, 'your'), (815, 'if'), (796, 'can')]

# [(4239, 'que'), (3955, 'de'), (3232, 'no'), (2517, 'en'), (2443, 'la'), (2384, 'el'), (2358, 'es'), (2158, 'me'),
# (1507, 'un'), (1353, 'pero'), (1239, 'lo'), (1075, 'se'), (1068, 'por'), (1038, 'mi'), (1034, 'con'), (976, 'los'),
# (956, 'una'), (934, 'te'), (872, 'yo'), (854, 'si'), (846, 'para'), (685, 'como'), (629, 'las'), (515, 'tengo'),
# (491, 'qué'), (474, 'estoy'), (472, 'eso'), (450, 'español'), (442, 'más'), (427, 'ya')]

# ####################

# Most common 2x2 ngrams
# [(26997, 'e '), (20153, ' t'), (19958, 't '), (16133, 'th'), (15687, ' i'), (15140, ' a'), (14827, 's '),
# (13154, 'in'), (11712, 'he'), (11185, 'ou'), (10904, 'an'), (10851, 'd '), (10356, ' s'), (9806, 're'), (9590, 'n '),
# (9564, 'er'), (9242, 'ha'), (9169, ' w'), (9051, 'o '), (8784, 'y '), (8036, 'at'), (8027, 'ng'), (7816, 'i '),
# (7655, ' m'), (7455, 'it'), (7353, 'on'), (6934, 'yo'), (6801, 'r '), (6759, 'en'), (6537, ' b')]

# [(21234, 'o '), (20142, 'e '), (17572, 'a '), (14676, 's '), (12778, ' e'), (12619, 'es'), (11747, 'en'),
# (9230, 'n '), (9082, 'er'), (8643, ' d'), (8522, ' p'), (8432, 'ue'), (7824, 'de'), (7682, ' m'), (7629, ' c'),
# (7611, ' a'), (7145, 'qu'), (7044, ' s'), (6922, ' l'), (6225, 'ar'), (6180, 'as'), (6165, 'la'), (6073, 'te'),
# (5995, 'no'), (5991, ' t'), (5940, 'os'), (5791, 'ra'), (5723, 'r '), (5471, 'do'), (5297, 'an')]

# ###################

# Most common 2x2 ngrams (word boundaries)
# [(30576, 'e '), (22182, 't '), (21980, ' t'), (21753, ' i'), (17250,
# 's '), (16610, ' a'), (16133, 'th'), (13154, 'in'), (12391, 'd '), (11712, 'he'), (11185, 'ou'), (11158, ' s'),
# (10994, ' w'), (10939, 'n '), (10904, 'an'), (10061, 'y '), (9920, 'o '), (9806, 're'), (9564, 'er'), (9242, 'ha'),
# (8386, ' m'), (8036, 'at'), (8027, 'ng'), (7951, ' y'), (7917, 'r '), (7906, 'i '), (7552, ' b'), (7502, ' h'),
# (7455, 'it'), (7353, 'on')]

# [(24886, 'o '), (21654, 'e '), (20558, 'a '), (17603, 's '), (14797, ' e'), (12619,
# 'es'), (11747, 'en'), (10069, 'n '), (10042, ' p'), (9123, ' d'), (9082, 'er'), (8796, ' a'), (8676, ' m'), (8446,
# ' c'), (8432, 'ue'), (8373, ' s'), (7824, 'de'), (7750, ' l'), (7145, 'qu'), (6886, ' t'), (6677, 'r '), (6225,
# 'ar'), (6180, 'as'), (6165, 'la'), (6073, 'te'), (5995, 'no'), (5940, 'os'), (5834, ' q'), (5791, 'ra'), (5681,
# ' n')]

# ########################

# Most popular 2x2 ngrams with space-ignoring custom token
# [(15018, 'th'), (8516, 'in'), (6909, 'yo'), (6882, 'an'), (5950, 'to'), (5917, 'at'), (5367, 'it'), (5339, 'me'),
# (5274, 'is'), (4769, 're'), (4674, 'er'), (4339, 'st'), (4313, 'en'), (3922, 'nt'), (3812, 'ha'), (3738, 'ar'),
# (3668, 'do'), (3660, 've'), (3634, 'on'), (3243, 'wh'), (3054, 'be'), (3010, 'ng'), (2962, 'so'), (2932, 'li'),
# (2924, 'he'), (2850, 'ca'), (2833, 'al'), (2781, 'wa'), (2733, 'ke'), (2716, 'le')]

# [(9463, 'es'), (7103, 'en'), (6568, 'de'), (6078, 'qu'), (4969, 'no'), (4575, 'co'), (4553, 'la'), (4428, 'te'),
# (4127, 'me'), (3479, 'do'), (3456, 'lo'), (3347, 'to'), (3278, 'pa'), (3191, 'ta'), (3188, 'un'), (3082, 'el'),
# (3066, 'pe'), (3042, 'ra'), (3012, 'po'), (2907, 'ro'), (2841, 'se'), (2722, 're'), (2677, 'ha'), (2583, 'an'),
# (2571, 'er'), (2547, 'si'), (2534, 'ca'), (2333, 'mi'), (2311, 'as'), (2291, 'di')]

# ###################################

# words, all datasets
# [[11307   451]
#  [ 1040  9796]]
#
#               precision    recall  f1-score   support
#
#           en       0.92      0.96      0.94     11758
#           sp       0.96      0.90      0.93     10836
#
#     accuracy                           0.93     22594
#    macro avg       0.94      0.93      0.93     22594
# weighted avg       0.94      0.93      0.93     22594


# ######################

# 2x2 ngrams
# [[10800   990]
#  [ 1211  9593]]
#
#               precision    recall  f1-score   support
#
#           en       0.90      0.92      0.91     11790
#           es       0.91      0.89      0.90     10804
#
#     accuracy                           0.90     22594
#    macro avg       0.90      0.90      0.90     22594
# weighted avg       0.90      0.90      0.90     22594

# ##########################

# 3x3 ngrams
# [[11321   477]
#  [ 1146  9650]]
#
#               precision    recall  f1-score   support
#
#           en       0.91      0.96      0.93     11798
#           es       0.95      0.89      0.92     10796
#
#     accuracy                           0.93     22594
#    macro avg       0.93      0.93      0.93     22594
# weighted avg       0.93      0.93      0.93     22594

# #############################

# 4x4 ngrams
# [[11590   387]
#  [ 1303  9314]]
#
#               precision    recall  f1-score   support
#
#           en       0.90      0.97      0.93     11977
#           es       0.96      0.88      0.92     10617
#
#     accuracy                           0.93     22594
#    macro avg       0.93      0.92      0.92     22594
# weighted avg       0.93      0.93      0.92     22594

# #############################

# Limiting number of messages per language to 10,000 total (4x4)
# [[2723  321]
#  [ 127 2830]]
#
#               precision    recall  f1-score   support
#
#           en       0.96      0.89      0.92      3044
#           es       0.90      0.96      0.93      2957
#
#     accuracy                           0.93      6001
#    macro avg       0.93      0.93      0.93      6001
# weighted avg       0.93      0.93      0.93      6001

# ###########################################

# 2x2 ngrams, greater than 10 characters
# [[8698  229]
#  [ 219 7616]]
#
#               precision    recall  f1-score   support
#
#           en       0.98      0.97      0.97      8927
#           es       0.97      0.97      0.97      7835
#
#     accuracy                           0.97     16762
#    macro avg       0.97      0.97      0.97     16762
# weighted avg       0.97      0.97      0.97     16762

# ###########################################

# 3x3 ngrams, greater than 10 characters
# [[8698  229]
#  [ 219 7616]]
#
#               precision    recall  f1-score   support
#
#           en       0.98      0.97      0.97      8927
#           es       0.97      0.97      0.97      7835
#
#     accuracy                           0.97     16762
#    macro avg       0.97      0.97      0.97     16762
# weighted avg       0.97      0.97      0.97     16762

# ###########################################

# 4x4 ngrams, greater than 10 characters
# [[8777  166]
#  [ 175 7644]]
#
#               precision    recall  f1-score   support
#
#           en       0.98      0.98      0.98      8943
#           es       0.98      0.98      0.98      7819
#
#     accuracy                           0.98     16762
#    macro avg       0.98      0.98      0.98     16762
# weighted avg       0.98      0.98      0.98     16762

# ###########################################

# 2x2 ngrams, greater than 20, ITERATE THREE TIMES
# [[6037    5]
#  [   5 4779]]
#
#               precision    recall  f1-score   support
#
#           en       1.00      1.00      1.00      6042
#           es       1.00      1.00      1.00      4784
#
#     accuracy                           1.00     10826
#    macro avg       1.00      1.00      1.00     10826
# weighted avg       1.00      1.00      1.00     10826

# ##########################

# At least length 20, full words (not ngrams)
# [[6123   67]
#  [  99 4778]]
#
#               precision    recall  f1-score   support
#
#           en       0.98      0.99      0.99      6190
#           es       0.99      0.98      0.98      4877
#
#     accuracy                           0.99     11067
#    macro avg       0.99      0.98      0.98     11067
# weighted avg       0.99      0.99      0.98     11067
