import os
import cv2
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torch.autograd import Variable
from torchvision import models, transforms
from tqdm import tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
video_dir1 = "raw_file"  # 替换为视频文件夹路径

def _load_video(video_dir, video_id):
    """Load and uniformly sample 4 frames from video."""
    num_frames = 4  # 每个视频采样 4 帧
    video_name = str(video_id) + ".mp4"
    cap = cv2.VideoCapture(os.path.join(video_dir, video_name))
    NumFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if NumFrames < num_frames:
        # 如果帧数不足 4 帧，填充零帧
        sampled_frms = [torch.zeros(3, 224, 224) for _ in range(num_frames)]
    else:
        # 计算均匀抽取的帧索引
        frame_indices = np.linspace(0, NumFrames - 1, num_frames, dtype=int)
        sampled_frms = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            rval, frame = cap.read()
            if rval:
                img = Image.fromarray(frame, mode='RGB')
                img = img.resize((224, 224))  # ViT 默认输入尺寸
                img = transforms.ToTensor()(img)
                img = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(img)  # 标准化
                sampled_frms.append(img)
            else:
                # 如果读取失败，填充零帧
                sampled_frms.append(torch.zeros(3, 224, 224))
    
    sampled_frms = torch.stack(sampled_frms, dim=0)  # 堆叠成 [num_frames, 3, 224, 224]
    return sampled_frms

class GridFeatBackbone(nn.Module):
    def __init__(self):
        super(GridFeatBackbone, self).__init__()
        self.net = models.vit_b_16(pretrained=True)  # 加载 ViT-B-16 模型
        self.net.heads = nn.Identity()  # 移除分类头，仅提取特征

    def forward(self, x):
        output = self.net(x)
        return output

# 获取视频文件列表并按 ID 排序
dir1 = sorted([f for f in os.listdir(video_dir1) if f.endswith('.mp4')], key=lambda x: int(x.split('.')[0]))

model = GridFeatBackbone().to(device)
all_features = []  # 存储所有视频的特征

for idx, f in tqdm(enumerate(dir1)):  
    video_id = f.split('.')[0]
    try:
        # 加载视频帧
        frms = _load_video(video_dir1, video_id)
        with torch.no_grad():
            # 提取每帧特征
            out = model(frms.to(device))  # [num_frames, feature_dim]
            video_feature = torch.cat([out[i, :].unsqueeze(0) for i in range(out.size(0))], dim=1)  # 拼接特征
            print(f"Processed video {video_id}: feature size {video_feature.size()}")
    except Exception as e:
        print(f"Error processing {video_id}: {e}")
        video_feature = torch.zeros(1, 768 * 4)  # 如果出错，用零特征填充
    all_features.append(video_feature.cpu().numpy())  # 保存当前视频的特征

# 将所有视频特征保存为一个 .npy 文件
all_features = np.concatenate(all_features, axis=0)
np.save("video_features_uniform_concat.npy", all_features)
print(f"All features saved to 'video_features_uniform_concat.npy', shape: {all_features.shape}")
