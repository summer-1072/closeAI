data1 = ['它对这个世界的规律有了一个', '比较更为完整的了解', '他对这个世界的规律有了一个比较更为完整的了解']
data2 = ['最神奇的是他把这些事物之间的相互关系', '这些物理规律好像都能学习', '这个物理规律好像都能学习进去。']


def merge_sentences(sentences, num=3, similar=0.8):
    indices = []
    size = len(sentences)
    for i in range(size):
        sen_i = sentences[i]
        for j in range(i + 1, min(i + num, size)):
            sen_j = sentences[j]
            if len(set(sen_i) & set(sen_j)) / min(len(set(sen_i)), len(set(sen_j))) > similar:
                index = [i, j].index()

            # sen2 = sentences[j]
            # ratio = len(''.join(set(sen1) & set(sen2))) / min(len(sen1), len(sen2))
            #
            # print(i, j, ratio)


merge_sentences(data2)
