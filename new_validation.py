# coding=utf-8
"""
created on:2017.7.22
author:DilecelSten
target:用新的方法构建lsi模型并预测用户兴趣
finished on:2017.7.22
"""
from gensim import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
import os
import linecache


interest = ['web开发', '并行及分布式计算', '大数据技术', '地理信息系统', '电子商务', '多媒体处理', '机器人', '机器学习', '计算机辅助工程', '计算机视觉', '企业信息化',
            '嵌入式开发', '人工智能', '人机交互', '人脸识别', '软件工程', '商业智能', '深度学习', '数据恢复', '数据可视化', '数据库', '数据挖掘', '算法', '图像处理',
            '推荐系统', '网络管理与维护', '网络与通信', '文字识别', '物联网', '系统运维', '项目管理', '信息安全', '虚拟化', '虚拟现实', '移动开发', '硬件', '游戏开发',
            '语音识别', '云计算', '增强现实', '桌面开发', '自然语言处理']

stopwords = {}.fromkeys([line.rstrip().decode() for line in open('Stopword.txt') ])
in_dic = {}

def get_id():
    """
    获取验证集用户id
    :return: 用户id列表
    """
    total_id = []
    path = 'SMPCUP2017_ValidationSet_Task2.txt'
    with open(path,'r') as fr:
        lines = fr.readlines()
        for each in lines:
            each = each.strip('\n').strip('\r')
            total_id.append(each)
    return total_id

def get_document(id):
    """
    根据id获取文档内容
    :param id: 文档编号
    :return:文档内容
    """
    result = ''
    path = '../验证集title/' + id + '.txt'
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n').strip('\r')
            word_line = jieba.cut(line)
            for word in word_line:
                if word not in stopwords:
                    result = result + word + ' '
    return result

def get_class():
    """
    获取类别的文档
    :return: 文档列表
    """
    documents = []
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

def build_lsi():
    title_interest = {}
    id = get_id()
    documents = get_class()
    texts = [[word for word in document.lower().split()] for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=33)
    index = similarities.MatrixSimilarity(lsi[corpus])
    for i in range(len(id)):
        three_interest = []
        query = get_document(id[i])
        query_bow = dictionary.doc2bow(query.lower().split())
        query_lsi = lsi[query_bow]
        sims = index[query_lsi]
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        for m in range(len(sort_sims)):
            if in_dic[sort_sims[m][0]] not in three_interest:
                three_interest.append(in_dic[sort_sims[m][0]])
            else:
                continue
            if len(three_interest) == 3:
                break
        with open('temp.txt','a') as fw:
            print id[i]
            fw.write(id[i]+',')
        for k in range(3):
            print three_interest[k]
            with open('temp.txt', 'a') as fw:
                if k == 2:
                    fw.write(three_interest[k]+'\n')
                else:
                    fw.write(three_interest[k] + ',')
    #     title_interest[id[i]] = three_interest
    # return title_interest

if __name__ == '__main__':
    # id = get_id()
    # print id[0]
    # print get_document('U0109327')
    build_lsi()