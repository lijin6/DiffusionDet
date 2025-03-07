import os.path as osp
import os
from PIL import Image
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# COCO标注模板生成
def coco_annotations(bbox, cid, bbox_id, img_id, iscrowd):
    """
    生成COCO格式的标注信息
    bbox格式要求：(x_min, y_min, x_max, y_max)
    """
    x1, y1, x2, y2 = bbox
    width = x2 - x1
    height = y2 - y1
    return {
        'segmentation': [[x1, y1, x2, y1, x2, y2, x1, y2]],
        'bbox': [x1, y1, width, height],  # 修正为正确的[x,y,width,height]格式
        'category_id': cid,
        'area': width * height,
        'iscrowd': iscrowd,
        'image_id': img_id,
        'id': bbox_id
    }

def coco_images(file_name, height, width, img_id):
    """生成图片信息条目"""
    return {
        'file_name': osp.basename(file_name),  # 只保留文件名
        'height': height,
        'width': width,
        'id': img_id
    }

def validate_coordinates(coords, img_width, img_height):
    """
    验证坐标的合法性
    返回：(是否合法, 错误信息)
    """
    x1, y1, x2, y2 = coords
    
    # 检查坐标顺序
    if x1 >= x2 or y1 >= y2:
        return False, f"Invalid box coordinates: x1({x1}) >= x2({x2}) or y1({y1}) >= y2({y2})"
    
    # 检查是否超出图像边界（允许1像素的容差）
    if (x1 < -1 or y1 < -1 or 
        x2 > img_width + 1 or 
        y2 > img_height + 1):
        return False, f"Coordinates out of bounds: image size ({img_width}x{img_height}), box ({x1},{y1},{x2},{y2})"
    
    # 检查有效面积
    if (x2 - x1) * (y2 - y1) < 1:
        return False, f"Invalid area: {x2 - x1}x{y2 - y1}"
    
    return True, "Valid coordinates"

def process_annotation_line(line, img_width, img_height, label_path):
    """处理单行标注"""
    parts = line.strip().split()
    
    # 基础验证
    if len(parts) < 10:
        logging.warning(f"Invalid line format in {label_path}: {line.strip()}")
        return None
    
    try:
        # 解析坐标
        coords = list(map(float, parts[:8]))
        cls_name = parts[-2]
        iscrowd = int(parts[-1])
    except (ValueError, IndexError) as e:
        logging.warning(f"Parsing error in {label_path}: {e} - Line: {line.strip()}")
        return None
    
    # 计算边界框
    x1 = min(coords[0], coords[2], coords[4], coords[6])
    x2 = max(coords[0], coords[2], coords[4], coords[6])
    y1 = min(coords[1], coords[3], coords[5], coords[7])
    y2 = max(coords[1], coords[3], coords[5], coords[7])
    
    # 验证坐标
    valid, msg = validate_coordinates((x1, y1, x2, y2), img_width, img_height)
    if not valid:
        logging.warning(f"Skipping invalid box in {label_path}: {msg}")
        return None
    
    return (x1, y1, x2, y2, cls_name, iscrowd)

def process_annotation_file(label_path, img_path, img_id, anno_id):
    """处理单个标注文件"""
    annos = []
    
    try:
        # 获取图像尺寸
        with Image.open(img_path) as img:
            img_width, img_height = img.size
    except Exception as e:
        logging.error(f"Cannot open image {img_path}: {e}")
        return [], anno_id
    
    # 读取标注文件
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        logging.error(f"Cannot read annotation file {label_path}: {e}")
        return [], anno_id
    
    # 处理有效行（跳过前两行注释）
    for line in lines[2:]:
        result = process_annotation_line(line, img_width, img_height, label_path)
        if not result:
            continue
        
        x1, y1, x2, y2, cls_name, iscrowd = result
        
        # 类别验证
        if cls_name not in cls_name2id:
            logging.warning(f"Skipping unknown class '{cls_name}' in {label_path}")
            continue
        
        # 生成标注条目
        annos.append(coco_annotations(
            bbox=(x1, y1, x2, y2),
            cid=cls_name2id[cls_name],
            bbox_id=anno_id,
            img_id=img_id,
            iscrowd=iscrowd
        ))
        anno_id += 1
    
    return annos, anno_id

def generate_coco_dataset(data_root, anno_root, img_root, output_path):
    """生成完整的COCO数据集"""
    dataset = {
        "images": [],
        "annotations": [],
        "categories": categories,
        "type": "instance"
    }
    
    img_id = 0
    anno_id = 0
    
    # 遍历标注文件
    for anno_file in os.listdir(osp.join(data_root, anno_root)):
        if not anno_file.endswith('.txt'):
            continue
            
        base_name = osp.splitext(anno_file)[0]
        img_file = f"{base_name}.png"
        label_path = osp.join(data_root, anno_root, anno_file)
        img_path = osp.join(data_root, img_root, img_file)
        
        if not osp.exists(img_path):
            logging.warning(f"Image file missing: {img_path}")
            continue
        
        # 处理单个文件
        annos, anno_id = process_annotation_file(
            label_path=label_path,
            img_path=img_path,
            img_id=img_id,
            anno_id=anno_id
        )
        
        # 更新数据集
        if annos:
            dataset["annotations"].extend(annos)
            dataset["images"].append(coco_images(
                file_name=img_file,
                height=Image.open(img_path).height,
                width=Image.open(img_path).width,
                img_id=img_id
            ))
            img_id += 1
    
    # 保存数据集
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    logging.info(f"Dataset generated: {len(dataset['images'])} images, {len(dataset['annotations'])} annotations")

# 类别配置
classes = (
    'plane', 'baseball-diamond', 'bridge', 'ground-track-field',
    'small-vehicle', 'large-vehicle', 'ship', 'tennis-court',
    'basketball-court', 'storage-tank', 'soccer-ball-field',
    'roundabout', 'harbor', 'swimming-pool', 'helicopter', 'container-crane'
)

# 创建类别映射
cls_name2id = {cls_name: i+1 for i, cls_name in enumerate(classes)}
categories = [
    {
        "id": i+1,
        "name": cls_name,
        "supercategory": cls_name
    } for i, cls_name in enumerate(classes)
]

# 配置路径
data_root = './datasets'
anno_root = 'coco/label'
img_root = 'coco/images'
output_json = osp.join(data_root, 'coco/instances_train.json')

# 生成数据集
generate_coco_dataset(
    data_root=data_root,
    anno_root=anno_root,
    img_root=img_root,
    output_path=output_json
)