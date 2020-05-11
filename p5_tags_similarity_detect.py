'''
    文本为相似性检测，替换相似的文本，并输出最终的结果
'''
from jieba import lcut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from collections import Counter
import re

#定义一个方法，用于合并同义词
def mergeSimilarity(str):
    newStr = ''
    #注意：如果匹配到近义词，则返回第一个/前的词语
    sililarity = [
        '环境优雅/环境不错',
        '服务态度好/服务态度不错/服务好/服务热情/服务态度很赞/服务态度很好/服务不错/服务态度可以/服务周到',
        '性价比低/贵/价格高/性价比差/价格贵/东西贵',
        '价格实惠/划算/物美价廉/便宜/性价比高/便宜实惠/套餐实惠/价格便宜/价格不贵/东西不贵'
        '人多/人太多/排队久',
        '好吃/味道很好/美味/味道鲜美/味道不错/东西好吃/东西不错',
        '上菜慢/上菜不快/菜慢/补给慢',
        '上菜很快/上菜快',
        '服务态度差/服务差/服务态度不好/服务态度很差/服务欠缺/服务不周到',
        '交通不便/停车不便',
        '交通便利/停车方便',
        '分量足/肉多/肉足/份量足/份量多/料足/量足',
        '分量少/量少/份量少',
        '菜品丰富/种类繁多/菜品多',
        '菜品少/菜少',
        '菜新鲜/食品新鲜/现做现卖/菜品新鲜/东西新鲜/菜鲜',
        '菜不新鲜/肉类臭/肉不新鲜/东西不新鲜',
        '孩子高兴/孩子开心',
        '孩子不高兴/孩子不开心',
        '味道一般/口味一般',
    ]
    for st in sililarity:
        words = st.split('/')
        if str in words:
            newStr = words[0]
            break
        else:
            newStr = str
    return newStr

displayArr = []
textsOld = []
# filePath = './outputFile/p4_tag3_same.txt'
# filePath = './outputFile/p2_comment_tags.txt'
with open('./outputFile/p2_comment_tags.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        textsOld.append(line.strip())
        line = re.split(r'id_\d+\.', line)[1]
        title = line.strip()
        displayArr.append(title)

#保存的默认标签
default_tags = []
with open('./p0_default_tags.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        title = line.strip()
        default_tags.append(title)

# 合并标签
def mergeTags():
    res = {}  # 创建一个空字典
    for i in range(len(displayArr)):
        texts = default_tags
        keyword = displayArr[i]
        # 1、将【文本集】生成【分词列表】
        texts = [lcut(text) for text in texts]
        # 2、基于文本集建立【词典】，并获得词典特征数
        dictionary = Dictionary(texts)
        num_features = len(dictionary.token2id)
        # 3.1、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
        corpus = [dictionary.doc2bow(text) for text in texts]
        # 3.2、同理，用【词典】把【搜索词】也转换为【稀疏向量】
        kw_vector = dictionary.doc2bow(lcut(keyword))
        # 4、创建【TF-IDF模型】，传入【语料库】来训练
        tfidf = TfidfModel(corpus)
        # 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
        tf_texts = tfidf[corpus]  # 此处将【语料库】用作【被检索文本】
        tf_kw = tfidf[kw_vector]
        # 6、相似度计算
        sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)
        similarities = sparse_matrix.get_similarities(tf_kw)
        for e, s in enumerate(similarities, 1):
            if s>0.5:
                # print(keyword, ' 与 ', ''.join(texts[e - 1]), ' 的相似度为： ', s)
                key = ''.join(texts[e-1]).strip()
                res[key]=s
        arrSorted = sorted(res.items(), key=lambda item: item[1], reverse=True)
        for ind, (k, v) in enumerate(arrSorted):
            if ind==0:
                ids = textsOld[i].strip().split('.')[0]
                textsOld[i] = textsOld[i]+'----------'+k
                # textsOld[i] = ids+'.'+k
        res = {}#字典置空
    return textsOld


#标签对比：文本向量化后与向量化前
def tagsConstrat(newArr):
    # 如果没有标签，并且以好吃结尾的，都改成 东西好吃
    for ind, itemOne in enumerate(newArr):
        if len(itemOne.split('.')[1].split('----------')) == 1:
            if itemOne.strip().split('.')[1].endswith('好吃'):
                newArr[ind] = itemOne + '----------东西好吃'
            elif itemOne.strip().split('.')[1].endswith('不好吃'):
                newArr[ind] = itemOne + '----------东西不好吃'

    initial_comment = open('./outputFile/p1_processed_Data.txt', 'r', encoding='UTF-8')
    for comment_item in initial_comment:
        initialCommentArr.append(comment_item.strip())

#将标签分类的结果输出到文件中
def dealTags(newArr):
    resOutput = {}
    res = []
    index = 0
    con = ''

    for item in newArr:
        filter1 = item.split('.')[1]
        filter2 = filter1.split('----------')
        if len(filter2) == 2:
            oldnew = filter2[1]
        else:
            oldnew = filter1
        new = mergeSimilarity(oldnew)  # 合并近义词
        tagsSummary.append(new)

        # 键值不能一样
        if con == item.split('.')[0]:
            index+=1
        else:
            index = 0
        resOutput[item.split('.')[0]+'-'+str(index)] = new
        con = item.split('.')[0]

    # 标签top10
    counterSorted = Counter(tagsSummary).most_common(10)
    res.append(counterSorted)
    print('counterSorted:',counterSorted,'\n')
    print('--------tagsSummary',len(tagsSummary),'↓------------\n',tagsSummary,'\n','-----------resOutput↓',len(resOutput),'--------------\n',resOutput)
    # 对结果进行排序
    resOutputSorted = sorted(resOutput.items(), key=lambda item: item[1])
    res.append(resOutputSorted)
    for item in resOutputSorted:
        comment_id = item[0]
        comment_tag = item[1]
        output.write(comment_id + '.' + comment_tag + '\n')
    print('-------resOutputSorted↓',len(resOutputSorted),'-----------\n',resOutputSorted)
    return res

#标签与评论对应起来
def tagToComment(res):
    obj = {}
    # print('counterSorted', res[0])
    for sorted in res[0]:  # 排好序的前十个标签
        for item in res[1]:
            comment_id = item[0]
            comment_tag = item[1]
            sortedTag = sorted[0]
            if comment_tag == sortedTag:
                obj[comment_id] = comment_tag

    for key, val in obj.items():
        for itemInitial in initialCommentArr:
            li = itemInitial.strip()
            if li.split('.')[0] == key.split('-')[0]:
                output2.write(val + ':' + li + '\n')

if __name__ == '__main__':
    output = open('./outputFile/p2_tags_summarize.txt', 'w', encoding='UTF-8')
    output2 = open('./outputFile/final_ans.txt', 'w', encoding='UTF-8')

    # 读取预处理之后的评论数据
    initialCommentArr = []
    tagsSummary = []
    resOutputSorted  =[]
    counterSorted = []

    newArr = mergeTags()
    Response = dealTags(newArr)
    tagsConstrat(newArr)
    tagToComment(Response)

    output.close()
    output2.close()

