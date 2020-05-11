'''
    step2.将分割好的句子，进行分词
'''
from pyhanlp import *
from jpype import *
import re

# 提取候选标签
def splitTag(ind,arr,i):
    nounce = ''
    adj = ''
    n_ind = 0
    adj_ind = 0
    adjNew = ''
    deny_word_count = 0
    deny_word_arr = []

    comment_id= str(re.split(r'_\d+\.',i.strip())[0])+'.'

    for index,item in enumerate(arr):
        # 获得名词，形容词的索引
        if re.compile('/n').findall(str(item)):
            nounce = str(item).split('/n')[0]
            n_ind = index
        elif re.compile('/vn').findall(str(item)):
            nounce = str(item).split('/vn')[0]
            n_ind = index

        if re.compile('/a').findall(str(item)):
            adj = str(item).split('/a')[0]
            adj_ind = index

        if re.compile('不\|没').findall(str(item)):
            #在名词和形容词之间
            if index>nounce and index<adj_ind:
                deny_word_count +=1
                deny_word_arr.append(item.split('/')[0])
        # 名词必须在形容词之前
        if len(nounce)*len(adj)>0 and n_ind<adj_ind:
            # 规定两个词之间的距离
            if n_ind-adj_ind<3 and n_ind-adj_ind>-3:
                # 如果是消极情绪就加 不
                if nounce=="态度":
                    nounce = "服务态度"
                if deny_word_count%2==1:
                    print(str(ind), '.', arr, comment_id, nounce + deny_word_arr[0] +adj)
                    output3.write(comment_id+nounce+deny_word_arr[0]+adj+adjNew+'\n')
                else:
                    print(str(ind), '.', arr, comment_id, nounce +adj)
                    output3.write(comment_id+nounce+adj+adjNew+'\n')
                nounce = ''
                adj = ''
                deny_word_count = 0
                deny_word_arr = []
        # 遍历一次数组就清空数据一次
        if index>=len(arr)-1:
            nounce = ''
            adj = ''
            deny_word_count = 0
            deny_word_arr = []

if __name__ == '__main__':
    # 读取经过处理之后的txt数据
    input = open("./outputFile/p1_small_processed_Data.txt", "r", encoding='UTF-8')
    # 将分词之后的结果保存到txt文件中
    outfilename = "./outputFile/p2_data_seperated.txt"
    output = open(outfilename, 'w', encoding='UTF-8')
    # 将经依存句法解析之后的结果保存到txt文件中
    outfilename2 = "./outputFile/p2_parse_data_seperated.txt"
    output2 = open(outfilename2, 'w', encoding='UTF-8')
    # 生成的标签结果保存到txt文件中
    outfilename3 = "./outputFile/p2_comment_tags.txt"
    output3 = open(outfilename3, 'w', encoding='UTF-8')

    index = 0 #用于计数
    for i in input:
        # if index<100:
            result = re.sub(r'id_\d+\_\d+\.', "", i.strip())

            # HANLP标准分词
            CustomDictionary = JClass('com.hankcs.hanlp.dictionary.CustomDictionary')
            HanLP = JClass('com.hankcs.hanlp.HanLP')
            # HanLP.Config.ShowTermNature = False
            test1 = HanLP.segment(result)
            # NLP分词
            # NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
            # test1 = NLPTokenizer.segment(result)
            #自定义词典
            # HanLP = JClass('com.hankcs.hanlp.HanLP')
            # CustomDictionary = JClass('com.hankcs.hanlp.dictionary.CustomDictionary')
            # test = HanLP.parseDependency(result)
            # 依存关系解析
            sentence = HanLP.parseDependency(result)
            output2.write(str(index) +': '+str(test1) +'\n' + str(sentence) + '\n\n')
            # 根据一定的规则生成标签
            splitTag(index,test1,i)

            # 写到txt文件中
            output.write(str(index) + '.' + str(test1) + '\n')
            index += 1

    input.close()
    output.close()
    output2.close()
    output3.close()
    print('----------------------step2:分词&&依存句法分析结束-----------------------')
