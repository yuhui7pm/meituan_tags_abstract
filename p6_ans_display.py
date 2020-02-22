input_tag = open("./outputFile/p5_tag_top_10.txt", "r", encoding='UTF-8')
input_id = open("./outputFile/p5_tag_id.txt", "r", encoding='UTF-8')
input_initial_data = open("./outputFile/p1_processed_Data.txt", "r", encoding='UTF-8')
output = open("./outputFile/p6_ans.txt", "w", encoding='UTF-8')

#top10的标签
tags = []
index = 0
for line in input_tag:
    if index>0:
        tags.append(line.strip().split(' ')[0])
    index+=1
print(tags)

#数据预处理之后的评论
processed_data = []
for line in input_initial_data:
    processed_data.append(line.strip())

#top10标签对应的评论id号,输出结果到txt文件中
line_index = 0
tga_ids = []
for id in input_id:
    if line_index>0:
        tga_ids.append(id.strip().split(' '))
        for index in tga_ids[0]:
            for item in processed_data:
                if ('id_'+index)==item.split('.')[0]:
                    print(tags[line_index-1]+': '+item)
                    output.write(tags[line_index-1]+': '+item+'\n')
    line_index+=1

output.close()
