# Install Detectron2

## To use Detectron2 with Docker please see this [link](https://github.com/facebookresearch/detectron2/blob/master/docker)

### Basic Requirements
- Linux or macOS with Python ≥ 3.6
- PyTorch ≥ 1.6 and [torchvision](https://github.com/pytorch/vision/).
- OpenCV is optional and needed by demo and visualization

NOTE: requirements.txt file should contains all the requirements except Detectron2 where it should be installed from the source. 

### Build Detectron2 from Source

```
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

# Or to install it from a local clone
git clone https://github.com/facebookresearch/detectron2.git
```



