# coding=utf-8
"""
created on:2017.7.20
author:DilicelSten
target:预测用户兴趣
finished on:2017.7.20
"""
from gensim import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from interestPredict import *
import random
import jieba

documents = []
interest = ['web开发', '并行及分布式计算', '大数据技术', '地理信息系统', '电子商务', '多媒体处理', '机器人', '机器学习', '计算机辅助工程', '计算机视觉', '企业信息化',
            '嵌入式开发', '人工智能', '人机交互', '人脸识别', '软件工程', '商业智能', '深度学习', '数据恢复', '数据可视化', '数据库', '数据挖掘', '算法', '图像处理',
            '推荐系统', '网络管理与维护', '网络与通信', '文字识别', '物联网', '系统运维', '项目管理', '信息安全', '虚拟化', '虚拟现实', '移动开发', '硬件', '游戏开发',
            '语音识别', '云计算', '增强现实', '桌面开发', '自然语言处理']

stopwords = {}.fromkeys([ line.rstrip().decode() for line in open('Stopword.txt') ])
in_dic = {}

def get_document(id):
    """
    根据id获取文档内容
    :param id: 文档编号
    :return:文档内容
    """
    result = ''
    path = '../training_user/' + id + '.txt'
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            result = result + line
    return result

def get_class():
    """
    获取类别的文档
    :return: 文档列表
    """
    data_path = '../tag/'
    num = 0
    for i in range(len(interest)):
        each_path = os.path.join(data_path, interest[i]+'/')
        filename = os.listdir(each_path)
        for name in filename:
            title_class = ''
            f_path = os.path.join(each_path, name)
            lines = linecache.getlines(f_path)
            line = jieba.cut(lines[2])
            for word in line:
                print word
                if word not in stopwords:
                    title_class = title_class + word + ' '
                else:
                    continue
            documents.append(title_class)
            in_dic[num] = interest[i]
            num = num + 1
    return documents

def build_model():
    to_id = get_user_id()
    precision = 0
    documents = get_class()
    texts = [[word for word in document.lower().split()] for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=350)
    index = similarities.MatrixSimilarity(lsi[corpus])
    n = 1000
    t_id = random.sample(to_id,n)
    for j in range(n):
        three_interest = []
        count = 0
        query = get_document(t_id[j])
        print t_id[j]
        query_bow = dictionary.doc2bow(query.lower().split())
        query_lsi = lsi[query_bow]
        sims = index[query_lsi]
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # print sort_sims
        for m in range(len(sort_sims)):
            if in_dic[sort_sims[m][0]] not in three_interest:
                three_interest.append(in_dic[sort_sims[m][0]])
            else:
                continue
            if len(three_interest) == 3:
                break
        for k in range(3):
            print three_interest[k]
            if three_interest[k] in get_interest(t_id[j]):
                count = count + 1
            else:
                continue
        result = count/3.0
        print result
        precision = precision + result
    print precision
    precision = precision/n
    print precision

if __name__ == '__main__':

    # build_model()
    print get_class()[0]
    # print get_document('U0000210')
    # print len(get_user_id())
    # print stopwords
    print in_dic[1],in_dic[17],in_dic[37],in_dic[77]