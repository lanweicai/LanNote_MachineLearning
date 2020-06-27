# 项目课week01

## 一、项目导论

项目一：问答摘要与推理

数据集：<https://aistudio.baidu.com/aistudio/competition/detail/3> 

NLP主要解决的三类问题：

+ 分类问题
  + 比如文本分类、情感分析、多标签的文本分类
+ 序列标注问题
  + 命名体识别、词性分析、语法分析
+ **序列到序列问题（Seq2seq问题）**
  + 文本摘要（输入一篇原文生成一篇摘要）
  + 机器翻译（输入英文翻译成中文）
  + 问答
  + 对话
  + 其他

Seq2seq也能解决序列标注问题

该项目8周的安排，详情看课表



## 二、语言模型到Word Embedding 

——(词向量方法的引入)

### 概念

Word Embedding：

Embedding：嵌入，用一个嵌入空间来表达该语言（把一个词嵌入到空间里），让计算机理解它

语言模型：表达一句话，其合理性的模型。让概率最大化就是最好的语言模型 



### 历程

语言模型

到03年出现神经网络语言模型（NNLM）

![1592932221527](C:\Users\LANWEI~1\AppData\Local\Temp\1592932221527.png)



### 语言的表达形式

#### discrete symbols

离散型表示——one-hot 

比如：我爱你   

建立一个字典，['我','爱','你']

通过one-hot 来表征这个词，比如"我"  [1,0,0]，爱[0,1,0]，你[0,0,1]

缺点：每一个词都是单独的，相似度很难体现， 

所以引出下一个语言的表达形式来解决这个问题

#### by their context

通过周围词的表现特征来表现这个词

比如 我爱你，我喜欢你，通过周围特征得出 爱=喜欢



## 

词嵌入 word embedding

解决这个问题的方法是 Word2vec (谷歌2013)

词向量：维度的矩阵，多维空间的一个点 

条件：

- 有一个很大的词表库
- 在词表中的每一个词都可以通过向量表征
- 有一个中心词c，有一个输出词o
- 用词c和o的相似度来计算他们之间同时出现的概率
- 调整这个词向量来获得最大的输出概率





Word2vec 函数公式

——极大自然函数

——方向梯度求导 把极大自然函数转成最小值  = -

—— log 乘法变成甲方  /T  平均化，取平均log

![1593101652478](D:\06_Git_Repository\LanNote_MachineLearning\04_NLP_Pro\week01\NLP_Pro_LanNote_Week01.assets\1593101652478.png)

求这个概率成为求这个目标函数的关键

C输入词

O输出词



代表这两个词向量的乘积

把所有词算一遍作为分母

![1593101948750](D:\06_Git_Repository\LanNote_MachineLearning\04_NLP_Pro\week01\NLP_Pro_LanNote_Week01.assets\1593101948750.png)







### Word2vec 两种模型 ⭐

#### Skip-gram模型

输入中间词预测两边的词，输入一个，输出多个

![1593145749972](D:\06_Git_Repository\LanNote_MachineLearning\04_NLP_Pro\week01\NLP_Pro_LanNote_Week01.assets\1593145749972.png)



构建数据集

![1593145774274](D:\06_Git_Repository\LanNote_MachineLearning\04_NLP_Pro\week01\NLP_Pro_LanNote_Week01.assets\1593145774274.png)

如何计算

字典——读热 编码



#### CBOW模型

相反



#### Sg与cbow的区别

+ 计算复杂度Ｏ　　主要计算集中在反向求导上面
  + ｓｇ　Ｏ（ｋＶ）
  + O（V）
+ 周围词的影响



词向量有什么优化方法？

+ 分层softmax
+ 负采样

#### Hierarchical Softmax

哈夫曼树

![1593190631739](D:\06_Git_Repository\LanNote_MachineLearning\04_NLP_Pro\week01\NLP_Pro_LanNote_Week01.assets\1593190631739.png)

![1593190695764](D:\06_Git_Repository\LanNote_MachineLearning\04_NLP_Pro\week01\NLP_Pro_LanNote_Week01.assets\1593190695764.png)

把词频更高的词放到离根节点更近的位置

 优势：查找路径更短

ｄｄ俄德法的说ｄ	ｄＤＤ　ＦＤＳＳＡＦ打发打发ｄｆｄ



哈夫曼编码

树左0 右1



Logistic Regression

LR计算公式的推导

离散——>连续



分层softmax？

把所有的输出词建立成为哈夫曼二叉树，放在前面两个模型之一去计算

把W‘换成哈夫曼二叉树

![1593192054773](D:\06_Git_Repository\LanNote_MachineLearning\04_NLP_Pro\week01\NLP_Pro_LanNote_Week01.assets\1593192054773.png)



第二个优化方法：

结构不变，策略变了

只挑少部分的权重进行更新



![1593192483538](D:\06_Git_Repository\LanNote_MachineLearning\04_NLP_Pro\week01\NLP_Pro_LanNote_Week01.assets\1593192483538.png)



重点 ：

![1593192625451](D:\06_Git_Repository\LanNote_MachineLearning\04_NLP_Pro\week01\NLP_Pro_LanNote_Week01.assets\1593192625451.png)





## 三、词向量实践与应用









## 四、预训练的双向语言模型