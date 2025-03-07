## DiffusionDet: Diffusion Model for Object Detection

**DiffusionDet is the first work to apply diffusion models to object detection.**

![](teaser.png)

> [**DiffusionDet: Diffusion Model for Object Detection**](https://arxiv.org/abs/2211.09788)  
> [Shoufa Chen](https://www.shoufachen.com/), [Peize Sun](https://peizessun.github.io/), [Yibing Song](https://ybsong00.github.io/), [Ping Luo](http://luoping.me/)  
> *[arXiv 2211.09788](https://arxiv.org/abs/2211.09788)*  

---

## Latest Updates
• **(11/2022)** Code and pre-trained models are now available.
• **(Custom Update)** Added support for custom datasets (e.g., DOTA, FAIR1) and training scripts.

---

## Pre-trained Models

| Method               | Box AP (1 step) | Box AP (4 steps) | Download |
|----------------------|:---------------:|:----------------:|:--------:|
| COCO-Res50           | 45.5            | 46.1             | [model](https://github.com/ShoufaChen/DiffusionDet/releases/download/v0.1/diffdet_coco_res50.pth) |
| COCO-Res101          | 46.6            | 46.9             | [model](https://github.com/ShoufaChen/DiffusionDet/releases/download/v0.1/diffdet_coco_res101.pth) |
| COCO-SwinBase        | 52.3            | 52.7             | [model](https://github.com/ShoufaChen/DiffusionDet/releases/download/v0.1/diffdet_coco_swinbase.pth) |
| LVIS-Res50           | 30.4            | 31.8             | [model](https://github.com/ShoufaChen/DiffusionDet/releases/download/v0.1/diffdet_lvis_res50.pth) |
| LVIS-Res101          | 31.9            | 32.9             | [model](https://github.com/ShoufaChen/DiffusionDet/releases/download/v0.1/diffdet_lvis_res101.pth) |
| LVIS-SwinBase        | 40.6            | 41.9             | [model](https://github.com/ShoufaChen/DiffusionDet/releases/download/v0.1/diffdet_lvis_swinbase.pth) |

---

## Getting Started

For installation instructions and usage guidelines, please refer to [Getting Started with DiffusionDet](GETTING_STARTED.md).

---

## Custom Dataset Support

### Added Features
1. **Support for Custom Datasets**:
   • Added functionality to train on custom datasets such as **DOTA** and **FAIR1**.
   • Includes a data preprocessing script (`transdata.py`) to convert custom datasets into the required format.

2. **Training on Custom Datasets**:
   • Added `mytrain.py` for training on custom datasets.
   • Easily configure dataset paths and training parameters in the script.

### Usage
1. **Data Preprocessing**:
   • Run `transdata.py` to preprocess your custom dataset:
     ```bash
     python transdata.py --dataset_path /path/to/your/dataset --output_path /path/to/output
     ```

2. **Training**:
   • Use `mytrain.py` to train on your custom dataset:
     ```bash
     python mytrain.py --config /path/to/config --dataset_path /path/to/preprocessed/dataset
     ```

---

## License

This project is licensed under the **CC-BY-NC 4.0** license. For more details, see the [LICENSE](LICENSE) file.

---

## Citing DiffusionDet

If you use DiffusionDet in your research or wish to reference the baseline results, please cite the following paper:

```BibTeX
@article{chen2022diffusiondet,
      title={DiffusionDet: Diffusion Model for Object Detection},
      author={Chen, Shoufa and Sun, Peize and Song, Yibing and Luo, Ping},
      journal={arXiv preprint arXiv:2211.09788},
      year={2022}
}
```

---

## Acknowledgments

We thank the authors and contributors for their groundbreaking work in applying diffusion models to object detection. For any questions or issues, please open an issue on the [GitHub repository](https://github.com/ShoufaChen/DiffusionDet).

---

## Contact

For further inquiries, please contact [Shoufa Chen](https://www.shoufachen.com/) or the project maintainers.

---

## Custom Modifications

This repository has been extended to support custom datasets and training. For more details on the modifications, refer to the `transdata.py` and `mytrain.py` scripts.