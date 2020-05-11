## 任务：实现美团美食评论的标签提取

### 代码文件说明
p1_data_processed.py: 对评论进行数据预处理\
p2_separate_words: 将分成小片段的评论数据进行中文分词，词性标注，依存关系分析\
p5_tags_similarity_detect.py： 生成评论随营的标签，并生成统一化标签然后排序取出top10

### outputfile文件说明
p0_default_tags.txt: 自定义的统一化标签字典
p1_initial_Data.txt: 从数据库读取出来的评论数据\
p1_processed_Data.txt: 数据预处理之后的评论数据\
p1_small_processed_Data.txt: 将与处理的评论数据切分成小片段
p2_comment_tags.txt: 小片段评论生成的评论标签\
p2_data_seperated.txt: 小片段评论中文分词与词性标注的结果\
p2_parse_data_seperated.txt: 小片段评论依存关系分析
p2_tags_summarize.txt: 生成的小片段的评论标签
final_ans.txt: 执行标签统一化操作，排序。

### 其他文件说明
stopword.txt: 哈工大停用词表
custom_dictionary.txt: 自定义的美食字典，用于hanlp的中文分词，词性标注
