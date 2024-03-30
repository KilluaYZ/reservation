from snownlp import SnowNLP
import matplotlib.pyplot as plt
from tqdm import tqdm

def evaulate_sentiment(words_list: list):
    pos_count = 0
    neg_count = 0
    neg_words_list = []
    pos_words_list = []

    for _, line_data in enumerate(tqdm(words_list)):

        comment = line_data

        s = SnowNLP(comment)
        rates = s.sentiments

        if (rates >= 0.5):
            pos_count += 1
            pos_words_list.append((line_data, rates))

        elif (rates < 0.5):
            neg_count += 1
            neg_words_list.append((line_data, rates))

    pos_words_list.sort(lambda x:x[1], reverse=True)
    neg_words_list.sort(lambda x:x[1], reverse=False)
    #
    # with open("./neg_words_list.txt", "w") as t:
    #     for word, rate in neg_words_list:
    #         t.write(f"{word}\t{rate}\n")
    #
    # with open("./pos_words_list.txt", "w") as t:
    #     for word, rate in pos_words_list:
    #         t.write(f"{word}\t{rate}\n")

    return pos_words_list, neg_words_list
    # labels = 'Positive Side\n(eg. pray,eulogize and suggestion)', 'Negative Side\n(eg. abuse,sarcasm and indignation)'
    # fracs = [pos_count, neg_count]
    # explode = [0.1, 0]  # 0.1 凸出这部分，
    # plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
    # # autopct ，show percet
    #
    # plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
    #         shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6)
    #
    # plt.savefig("emotions_pie_chart.jpg", dpi=360)
    # plt.show()

