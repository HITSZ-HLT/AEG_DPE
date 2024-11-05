import json

file = json.load(open("/data/heyuhang/DPE/data/zh_News/sample_test.json"))

rm_file = []

for data in file:
    del data['meta']
    rm_file.append(
        data
    )

json.dump(rm_file,open("/data/heyuhang/DPE/data/zh_News/sample_test.json",'w'),ensure_ascii=False,indent='\t')
print(rm_file[:1])
