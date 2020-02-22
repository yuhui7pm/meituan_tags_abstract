'''
    将每个标签替换成聚类之后的标签
'''
input1 = open("./outputFile/p3_cluster_index.txt", "r", encoding='UTF-8')
input2 = open("./outputFile/p3_cluster_tags.txt", "r", encoding='UTF-8')
input3 = open("./outputFile/p2_comment_tags.txt", "r", encoding='UTF-8')
tag_id = open("./outputFile/p5_tag_id.txt", "w", encoding='UTF-8')
tag_top_10 = open("./outputFile/p5_tag_top_10.txt", "w", encoding='UTF-8')
output = open("./outputFile/p4_comment_cluster.txt", "w", encoding='UTF-8')
output2 = open("./outputFile/p4_tag3_same.txt", "w", encoding='UTF-8')
output3 = open("./outputFile/p4_ans_tags.txt", "w", encoding='UTF-8')
outputNew = open("./outputFile/p4_top_10.txt", "w", encoding='UTF-8')

#每个标签对应的聚类编号
for i in input1:
    clusterCount = eval(i.strip()) #得到一个多重数组
#每个聚类的中心聚类名字
for k in input2:
    clusterTags = eval(k.strip())[0]#也是个数组
#还没聚类前每个标签的名字
arr = []
for j in input3:
    arr.append(j.strip())
ind = 0;

# 将结果输出到txt文件中，为了便于观察
resArr = []
count = 0
zidian = sorted(clusterTags.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
for tags in clusterTags:
    for item in clusterCount[ind]:
        output.write(arr[item] + '---------------' + tags + '\n')
        output2.write(arr[item].split('.')[0]+ '.'+tags + '\n')
        # 输出至最大的前10个
        for i in range(10):
            if tags == zidian[i][0]:
                outputNew.write(arr[item].split('.')[0] + '.' +'top_'+str(i)+'_'+ zidian[i][0] + '\n')

                tag_id.write((arr[item].split('.')[0]).split('_')[1]+' ')
                tag_top_10.write(zidian[i][0]+' ')
                if count!=i:
                    tag_id.write('\n')
                    tag_top_10.write('\n')
                count = i
    ind+=1
print('标签和聚类中心匹配完毕')
output.close()
output2.close()
tag_top_10.close()
tag_id.close()
outputNew.close()