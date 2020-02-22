'''
    step1.对爬取的数据进行处理
'''

# 一、对数据进行处理，去除表情等无用的字符。
import emoji
import pymongo
import re

#字典去重：删除数据库中重复的数据
def deleteRepeatArr(arr):
    newArr = list(set([str(i) for i in arr]))
    li = [eval(i) for i in newArr]
    return li

# 从数据库中读取数据，保存到res这个数组中
class MongoDB():
    def __init__(self,formName,collection='',result=''):
        self.host = 'localhost'
        self.port = 27017
        self.databaseName = 'meituan'
        self.formName = formName
        self.result = result
        self.collection = collection

    # 连接数据库
    def collect_database(self):
        client = pymongo.MongoClient(host=self.host, port=self.port)  # 连接MongoDB
        db = client[self.databaseName]  # 选择数据库
        collection = db[self.formName]  # 指定要操作的集合,表
        print('数据库已经连接')
        return collection

    # 查询数据,将结果保存到数组中
    def selectMongoDB(self):
        res = []; #存储所保存的评论结果
        collection = self.collect_database()
        #将数据库数据保存到数组中
        for x in collection.find({"shopName":shopName},{"_id":0,"user-comment":1}):
            print(x)
            res.append(x)
        #因为数据库中有重复的数据，所以要删除重复数据
        res = deleteRepeatArr(res)
        return res


# 制定规则，进行数据预处理
def regProcessed(line):
    delete_emoji = emoji.demojize(line["user-comment"])    # 将emoji表情转换成字符串的形式以供删除
    result = re.sub(r':.*:', " ", delete_emoji)    # 删除变成字符串形式的emoji表情
    result = re.sub(r'【.*】', "", result)    # 删除评论自带的标签，如：【环境】，【服务】
    result = re.sub(r'\（.*\）|\(.*\)', "", result)    # 删除评论中的颜表情(⑅˃◡˂⑅)
    result = re.sub(r'#.*#', "", result)    # 删除评论中出现的菜名，例如：#广式炸云吞# #白灼大海虾# #盐水呛生蚝#
    result = re.sub(r'h{2,}', "", result)    # 删除评论中出现的hhhh
    result = re.sub(r'[0-9|A-Z|a-z]{2,}', "", result)    # 删除评论中出现的数字，英文字母
    result = re.sub(r'\[\.\]', "", result) #去除 [害羞] 类型的字符
    result = re.sub(r'(…|\.|\?|。|，|,|！|!|~|～){2,}', "。", result)  # 删除评论中出现的标点符号
    result = re.sub(r'\s{1,}',',',result) #匹配多个空格，替换成"，"
    result = result.strip()    # 去除两边的空格
    result = result.replace('\n','')    # 去除换行符\n
    result = result.replace('\r','')    # 去除换行符\r
    # result = re.split('[，,.。？?～ ]',result.strip())    # 将每个句子进行分割
    #开头只有1个逗号的情况
    if(result.strip()==','):
        result=''
    return result

if __name__ == '__main__':
    shopName = '老树咖啡（峡山店）'

    # 给出文档路径,用于保存处理前的数据和处理后的数据
    inputs = MongoDB("shops_comments").selectMongoDB()
    outfilename = "./outputFile/p1_processed_Data.txt"
    outfilename2 = "./outputFile/p1_initial_Data.txt"
    outfilename3 = "./outputFile/p1_small_processed_Data.txt"
    outputs = open(outfilename, 'w', encoding='UTF-8')
    outputs2 = open(outfilename2, 'w', encoding='UTF-8')
    outputs3 = open(outfilename3,'w',encoding='UTF-8')

    # 根据制定的正则表达式规则，进行数据处理
    for index, line in enumerate(inputs):
        # 得到处理过后的数据
        lineList = regProcessed(line)
        # 完整的句子->写到txt文件中,
        outputs2.write(line["user-comment"] + '\n')
        if len(lineList.strip())>0:
            outputs.write('id_' + str(index) + '.' + lineList + '\n')
        # 将句子进行切割->写到txt文件中
        lineList = re.split('[，,.。？?～ ]', lineList.strip())
        for ind,item in enumerate(lineList):
            if len(item) > 0:
                outputs3.write('id_' + str(index) +'_'+ str(ind) +'.' + item + '\n')

    #关闭txt文档
    outputs.close()
    outputs2.close()
    outputs3.close()
    print('----------------------step1:数据处理完毕-----------------------')