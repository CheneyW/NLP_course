# 生物医学命名实体识别


实验环境：ubuntu 16.04 LTS

实验结果：f-score = 70.39%  
/data> sh test.sh  可查看评价结果

采用的语料为 JNLBA2004

使用前需进入crf/ 文件夹下安装crf++

## 运行步骤

**python task1.py**  
提取出训练文件的特征文件 data/train.txt，并将一系列训练得到的全局特征存储在 data/feature\_model.txt

**/data> crf_learn -c 4.0 template train.txt model -t**  
其中 template 是模板文件，model 是训练出的模型文件，参数-t 要求生成模型文件 model.txt

**python task3_getFeature.py**  
程序读取训练出的全局特征 feature\_model.txt，从而提取出测试文件的特征文件 data/test.txt

**/data> crf_test -m model test.txt > output.txt**  
生成测试结果 output.txt

**python task3_getResult.py**  
更改测试结果output.txt的格式，只保留词和命名实体标记，生成result.txt。

**/data> perl evalIOB2.pl result.txt Genia4EReval1.iob2 >> evaluation_result.txt**  
调用评价程序，保存评价结果文件evaluation\_result.txt




## 特征含义
![](https://i.imgur.com/YVflkrA.jpg)



## 文件目录
		NLP_lab3
		│	
		│  analyse.py			分析标注错误原因
		│  MyClass.py 
		│  README.md
		│  task1.py			提取训练集特征文件
		│  task3_getFeature.py		提取测试集特征文件
		│  task3_getResult.py		更改测试结果的格式，只保留词以及命名实体标记
		│
		├─crf++
		│      CRF++-0.58.tar.gz
		│      README.txt
		│
		├─data
		│  │  evalIOB2.pl 			评价程序
		│  │  evaluation_result.txt		评价结果
		│  │  Genia4EReval1.iob2		测试集标准答案
		│  │  global_feature.txt		训练集提取的全局特征存储文件
		│  │  model				模型文件
		│  │  output.txt			crf_test生成结果
		│  │  result.txt			只保留词和实体标记的结果
		│  │  template				crf++模板
		│  │  test.sh				使用当前model文件对test.txt进行测试
		│  │  test.txt				测试集提取的特征文件
		│  │  train.txt				训练集提取的特征文件
		│  │
		│  ├─CommonUsedWords		通用词
		│  │      list.txt
		│  │      README.txt
		│  │
		│  ├─Genia4ERtest
		│  │
		│  ├─Genia4ERtraining
		│  │
		│  ├─JNLPBA2004_eval
		│  │
		│  └─StopWordList		停用词
		│          README.txt
		│          swl1.txt
		│          swl2.txt
		│
		└─...




		
