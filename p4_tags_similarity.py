'''
    文本为相似性检测，替换相似的文本
'''
from jieba import lcut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
import re

displayArr = []
# filePath = './outputFile/p4_tag3_same.txt'
# filePath = './outputFile/p2_comment_tags.txt'
with open('./outputFile/p2_comment_tags.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        line = re.split(r'id_\d+\.', line)[1]
        title = line.strip()
        displayArr.append(title)

textsOld = []
with open('./outputFile/p2_comment_tags.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        line = re.split(r'id_\d+\.', line)[1]
        title = line.strip()
        textsOld.append(title)

# 合并标签
def mergeTags(textArr):
    res = []
    for i in range(len(displayArr)):
        try:
            exampleArr = textArr
            if i==0:
                texts = textArr
            else:
                for item in res:
                    if item in exampleArr:
                        exampleArr.remove(item)
                texts = exampleArr
                res = []

            # print(exampleArr)
            # 文本集和搜索词
            # texts = ['吃鸡这里所谓的吃鸡并不是真的吃鸡，也不是谐音词刺激的意思',
            #          '而是出自策略射击游戏《绝地求生：大逃杀》里的台词',
            #          '我吃鸡翅，你吃鸡腿']
            keyword = texts[i]
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
                    res.append(exampleArr[e-1])
                    print(keyword+' 与 '+exampleArr[e-1]+' 的相似度为 ：',s)
            print('---------------------------------------------------')
        except:
            print('')
    print('合并完成！')
mergeTags(textsOld)