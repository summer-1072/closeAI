sentences = ['有一个问题一直让我百思不得其解', '我感觉sora不是表面上看起来那么简单', '就是一个文生视频的编辑器',
             '一个生产的工具', '也不是说就简单的比pika比runway好很多', '这些都是表象',
             '这个背后一定意味着什么big thing happen', '就一定有什么重大的事情发生',
             '应该是人工智能又到了一个新的突破点', '而且表面上看起来是一个文生视频的工具',
             '实际上现在很多人也都同意我的观点', '实际上现在很多人也都同意我的观点', '它是一个现实世界模拟器',
             '但它也不仅仅是用来模拟现实世界', '它意味着通用人工智能对这个世界的理解能力', '又一次得到了突破',
             'gvt相当于是人工智能对人类语言和知识的理解', '达到了一个突破点',
             '而除了人类的语言和这个世界的人类之间做交互用的知识之外', '这个世界还有很多规律',
             '比如说水倒在桌子上会形成一滩水', '波涛荡起来就波涛', '比如说水倒在桌子上会形成一滩水',
             '波涛档起来的时候波涛是什么样子', '波涛会拍在船上或者泼在海岸上', '无人机在空中飞的时候视角是如何的变化',
             '然后狗把鼻子扎到血里', '血会流在狗鼻子上', '如果没有掌握这种规律', '实际上这个机器人工智能是不完整的',
             '是残缺的', '它就不可能真正的变成通用人工智能', '为什么通用机器人很难做', '真正的全无人价值也很难做',
             '就因为原来', '真正的全无人价值也很难做', '就是因为原来的人工智能', '对这个世界的规律物理定律的理解太少了',
             '所以我一直在想这个问题', '我觉得soro只是露了一小手展现了说', '我能够做出真实的视频', '这个视频之所以真实',
             '不是画面有多么优美', '是因为让我们人类看起来', '它的画面所有的动作', '是符合这个世界的运行规律的',
             '它对这个世界的规律有了一个', '比较更为完整的了解', '他对这个世界的规律有了一个比较更为完整的了解',
             '这就说明人工智能的能力又上了一个台阶', '这个训练过程意味着什么', '我这两天一直在想这个问题',
             '所以为什么我一激动说', 'agi不需要十年', '可能需要两三年', '我感觉从gpd4到gpd3到sora也就一年吧',
             '我觉得这个突推猛进是远远超过我们所有人能想象的', '我觉得sora和pika', 'roundway他们最大的差别呢',
             'roundway和pika是工作在像素', 'ranway和pika是工作在像素层面', '他们是怎么对画面来进行操作',
             '他们可能知道自己在画什么', '仅此而已', '但是他们并不知道画面上对应的我们物理世界的这种规律',
             '所以你看到的就是一些比较简单的动画', '那么sora让我最惊叹的就是说', '他不仅能画出很多虚与如真的对象',
             '各种各样的事物', '最神奇的是他把这些事物之间的相互关系', '这些物理规律好像都能学习',
             '这个物理规律好像都能学习进去', 'sora不仅仅是在操作像素', '就像当年gbd出来的时候呢', '总有一些人批评gbd说',
             '认为他虽然能写文章', '能造句子', '但他不能理解啥意思', '我对这种言论一直赤字以鼻',
             '因为他们老是希望把今天大模型的突破', '把它轻描淡写的', '说成是一种伪人工智能',
             '而我是认为真正的人工智能时代其实来临了']

idxs = []
size = len(sentences)
i = 0
while i < size:
    sen_i = sentences[i]
    for j in range(i + 1, min(i + 10, size)):
        sen_j = sentences[j]

        num = 0
        for k in range(min(len(sen_i), len(sen_j))):
            if sen_i[k] == sen_j[k]:
                num += 1

        if num / min(len(sen_i), len(sen_j)) > 0.8:
            if len(sen_i) > len(sen_j):
                idxs.extend([n for n in range(i + 1, j + 1)])

            else:
                idxs.extend([n for n in range(i, j)])

            i = j + 1

        else:
            i += 1

    print(i, size)

print(idxs)
#         if len(set(sen_i) & set(sen_j)) / min(len(set(sen_i)), len(set(sen_j))) > 0.8:
#             idx = [i, j][[len(sen_i), len(sen_j)].index(min([len(sen_i), len(sen_j)]))]
#             idxs.append(idx)
#
# for idx in sorted(idxs, reverse=True):
#     sentences.pop(idx)
