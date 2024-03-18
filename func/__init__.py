data1 = ['它对这个世界的规律有了一个', '比较更为完整的了解', '他对这个世界的规律有了一个比较更为完整的了解']
data2 = ['最神奇的是他把这些事物之间的相互关系', '这些物理规律好像都能学习', '这个物理规律好像都能学习进去。']


def merge_sentences(sentences, num=3, ratio_t=0.8):

    remove_indices = []
    for i in range(len(sentences)):
        sen1 = sentences[i]
        for j in range(i + 1, min(i + num, len(sentences))):
            sen2 = sentences[j]
            ratio = len(''.join(set(sen1) & set(sen2))) / min(len(sen1), len(sen2))



            print(i, j, ratio)


merge_sentences(data1)
