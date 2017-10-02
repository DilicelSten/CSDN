# coding=utf-8
"""
created on:2017.7.20
author:DilicelSten
target:获取百度百科对应兴趣的内容
finished on:2017.7.20
"""
import requests
from pyquery import PyQuery as pq

def gethtml(url):
    w = requests.get(url)
    html = w.content
    return html

def write(file_name,data):
    path='../baidu/'+file_name+'.txt'
    with open(path, 'w+') as f:
        f.write(data+'\n')

# arr = ['web开发', '并行及分布式计算', '大数据技术', '地理信息系统', '电子商务', '多媒体处理', '机器人', '机器学习', '计算机辅助工程', '计算机视觉', '企业信息化', '嵌入式开发', '人工智能', '人机交互', '人脸识别', '软件工程', '商业智能', '深度学习', '数据恢复', '数据可视化', '数据库', '数据挖掘', '算法', '图像处理', '推荐系统', '网络管理与维护', '网络与通信', '文字识别', '物联网', '系统运维', '项目管理', '信息安全', '虚拟化', '虚拟现实', '移动开发', '硬件', '游戏开发', '语音识别', '云计算', '增强现实', '桌面开发', '自然语言处理']
arr = ['桌面应用程序']
for i in arr:
    url='https://baike.baidu.com/item/'+i
    html = gethtml(url)
    doc = pq(html)
    data= doc('.para').text()
    print data
    # write(i,data)