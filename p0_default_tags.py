'''
    step0.获取默认标签
'''
import pymongo

# 删除数组中重复的数据
def deleteRepeatArr(arr):
  newArr = list(set([str(i) for i in arr]))
  # print('newArr：',newArr)
  # li = [eval(i) for i in newArr]
  return newArr

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
        for x in collection.find({},{"_id":0,"tag":1}):
            print(x)
            res.append(x)
        #因为数据库中有重复的数据，所以要删除重复数据
        res = deleteRepeatArr(res)
        return res

if __name__ == '__main__':
    # 给出文档路径,用于保存处理前的数据和处理后的数据
    inputs = MongoDB("shops_tags").selectMongoDB()
    outfilename = "./outputFile/p0_default_tags.txt"
    outputs = open(outfilename, 'w', encoding='UTF-8')

    tmpArr = []
    # 根据制定的正则表达式规则，进行数据处理
    for index, line in enumerate(inputs):
        tmpArr.append(eval(line)['tag'])
    print(tmpArr)
    Arr = deleteRepeatArr(tmpArr)
    for index in range(len(Arr)):
        outputs.write(Arr[index] + '\n')

    #关闭txt文档
    outputs.close()
    tmpArr = []
    print('----------------------step0:获取了默认标签-----------------------')