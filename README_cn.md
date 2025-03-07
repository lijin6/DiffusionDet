## DiffusionDet: 基于扩散模型的目标检测

**DiffusionDet 是首个将扩散模型应用于目标检测的工作。**

![](teaser.png)

关于安装说明和使用指南，请参考 [DiffusionDet 快速入门](GETTING_STARTED.md)。

## 自定义功能更新

### 新增功能
1. **支持自定义数据集**：
   • 新增了对自定义数据集（如 **DOTA** 和 **FAIR1**）的训练支持。
   • 提供了数据预处理脚本 (`transdata.py`)，用于将自定义数据集转换为所需格式。

2. **自定义数据集训练**：
   • 新增了 `mytrain.py` 脚本，用于在自定义数据集上进行训练。
   • 可以在脚本中轻松配置数据集路径和训练参数。

### 使用方法
1. **数据预处理**：
   • 运行 `transdata.py` 对自定义数据集进行预处理：
     ```bash
     python transdata.py --dataset_path /path/to/your/dataset --output_path /path/to/output
     ```

2. **训练**：
   • 使用 `mytrain.py` 在自定义数据集上注册并进行训练：
     ```bash
     python mytrain.py --config /path/to/config --dataset_path /path/to/preprocessed/dataset
     ```

---

## 自定义修改说明

本仓库已扩展以支持自定义数据集和训练。关于修改的更多详情，请参考 `transdata.py` 和 `mytrain.py` 脚本。