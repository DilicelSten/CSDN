# coding=utf-8
"""
created on:2017.7.10
author:Dilicelsten
target:构建RBA路径实现从读者——>“博客+作者”的查询
finished on:2017.7.11
"""

"""
思路：
分别读取两个文件构建相应的字典
通过字典的遍历实现相应的搜索
"""

# 获取博客发表记录并整理成字典
def getPost():
    post = {}
    with open('../data/2_Post.txt','r') as p_file:
        for line in p_file.readlines():
            line = line.strip('\n').strip("\r")
            tokens = line.split('')
            poster = tokens[0]
            blog = tokens[1]
            # if documentid == blog:
            post[blog] = poster
        return post

# 获取用户浏览记录并实现搜索
def getBrowse(userid):
    browse = {}
    browse[userid] = []
    with open('../data/3_Browse.txt', 'r') as b_file:
        for line in b_file.readlines():
            line = line.strip('\n').strip("\r")
            tokens = line.split('')
            user = tokens[0]
            blog = tokens[1]
            if user == userid:
                browse[userid].append(blog)
        return browse[userid]

# 构建RBA路径实现读者——>博主的搜索
def RBA(UID):
    post = getPost()
    uid = []
    BA = {}
    count = 0
    DID = getBrowse(UID)
    for each in DID:
        if post[each] == UID:
            continue
        else:
            uid.append(post[each])
            if post[each] in uid:
                BA[post[each]] = count+1
    print BA
    return BA


if __name__ == '__main__':
    UID = raw_input("请输入读者id号：")
    print '该读者看过的博客的博主如下：'
    RBA(UID)







