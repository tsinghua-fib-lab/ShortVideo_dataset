import os
import numpy as np
import torch
from torchtext.vocab import GloVe
from torchtext.data.utils import get_tokenizer
from tqdm import tqdm 

# 定义输入和输出路径
input_folder = 'asr_en'  # 替换为包含 txt 文件的文件夹路径
output_file = 'text_features_glove_50d.npy'

# 加载轻量化 GloVe 预训练嵌入（50 维）
glove = GloVe(name='6B', dim=50)  # 使用 50 维度的 GloVe 嵌入
tokenizer = get_tokenizer("basic_english")  # 基本的英文分词器

# 定义文本嵌入提取函数
def extract_text_features(text):
    tokens = tokenizer(text)  # 分词
    vectors = [glove[token] for token in tokens if token in glove.stoi]  # 查找嵌入向量
    if len(vectors) == 0:
        return np.zeros(glove.dim)  # 如果没有匹配的单词，返回零向量
    return torch.mean(torch.stack(vectors), dim=0).numpy()  # 平均所有单词的嵌入

# 遍历文件夹并提取特征
text_features = []
text_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]

for i in range(1, len(text_files) + 1):
    file_path = os.path.join(input_folder, str(i) + '.txt')
    print(f"Processing {str(i) + '.txt'}...")
    try:
        # 读取文本内容
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().strip()
        
        # 提取文本特征
        feature = extract_text_features(text)
        text_features.append(feature)
        print(feature.shape)
    except Exception as e:
        print(f"Error processing {str(i) + '.txt'}: {e}")

# 转换特征为 numpy 数组
text_features = np.array(text_features)

# 如果某个特征全为 0，则替换为所有非零特征的平均值
non_zero_features = text_features[~np.all(text_features == 0, axis=1)]  # 筛选非全零特征
mean_feature = np.mean(non_zero_features, axis=0) if len(non_zero_features) > 0 else np.zeros(glove.dim)

for idx in range(len(text_features)):
    if np.all(text_features[idx] == 0):  # 判断是否全零
        print(f"Feature for file {idx + 1}.txt is all zeros. Replacing with mean feature.")
        text_features[idx] = mean_feature

# 保存特征到 .npy 文件
np.save(output_file, text_features)
print(f"Features saved to {output_file}")
