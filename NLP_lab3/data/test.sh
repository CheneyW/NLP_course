# 对测试集test.txt进行测试

# 默认不重新训练模型
#crf_learn -c 4.0 template train.txt model -t

crf_test -m model test.txt > output.txt

perl evalIOB2.pl output.txt Genia4EReval1.iob2
