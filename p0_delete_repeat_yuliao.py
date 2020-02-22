'''
    删除自定义美食字典中重复的数据
'''

#coding:utf-8
import shutil
readDir = "/python/bishe_new/venv/Lib/site-packages/pyhanlp/static/data/dictionary/custom/yuhui_dictionary.txt"
writeDir = "./outputFile/yuhui_dictionary.txt"
lines_seen = set()
outfile=open(writeDir,"w",encoding='UTF-8')
f = open(readDir,"r",encoding='UTF-8')
for line in f:
  if line not in lines_seen:
    print('line:',line)
    outfile.write(line)
    lines_seen.add(line)
outfile.close()
print("success")