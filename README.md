# Install Detectron2

## To use Detectron2 with Docker please see this [link](https://github.com/facebookresearch/detectron2/blob/master/docker)

### Basic Requirements
- Linux or macOS with Python ≥ 3.6
- PyTorch ≥ 1.6 and [torchvision](https://github.com/pytorch/vision/).
- OpenCV is optional and needed by demo and visualization

NOTE: requirements.txt file should contain all the requirements except Detectron2 where it must be installed from the source.  

### Build Detectron2 from Source

```
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

# Or to install it from a local clone
git clone https://github.com/facebookresearch/detectron2.git
```

### Common Installation Issues

Click each issue for its solutions:

<details>
<summary>
ImportError: libtorchcpu.so: cannot open shared object file: No such file or directory
</summary>
<br/>

This usually happens when you use old version of PyTorch < 1.6.
Please see [pytorch.org](http://pytorch.org) to find the latest versions.

</details>

<details>
<summary>
ImportError: libcusparse.so.10.0: cannot open shared object file: No such file or directory
</summary>
<br/>

Probably because CUDA version is not compatible with PyTorch version.

<table class="docutils"><tbody><th width="80"> CUDA </th><th valign="bottom" align="left" width="100">torch 1.6</th><th valign="bottom" align="left" width="100">torch 1.5</th><th valign="bottom" align="left" width="100">torch 1.4</th> <tr><td align="left">10.2</td><td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.6/index.html
</code></pre> </details> </td> <td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.5/index.html
</code></pre> </details> </td> <td align="left"> </td> </tr> <tr><td align="left">10.1</td><td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.6/index.html
</code></pre> </details> </td> <td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.5/index.html
</code></pre> </details> </td> <td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.4/index.html
</code></pre> </details> </td> </tr> <tr><td align="left">10.0</td><td align="left"> </td> <td align="left"> </td> <td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu100/torch1.4/index.html
</code></pre> </details> </td> </tr> <tr><td align="left">9.2</td><td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu92/torch1.6/index.html
</code></pre> </details> </td> <td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu92/torch1.5/index.html
</code></pre> </details> </td> <td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu92/torch1.4/index.html
</code></pre> </details> </td> </tr> <tr><td align="left">cpu</td><td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.6/index.html
</code></pre> </details> </td> <td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.5/index.html
</code></pre> </details> </td> <td align="left"><details><summary> install </summary><pre><code>python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.4/index.html
  </code></pre> </details> </td> </tr></tbody></table>

You can use ` from torch.utils.collect_env import main main() ` to see your environment PyTorch and torchvision version, CUDA version, and versions of relevant libraries or `python -m detectron2.utils.collect_env`

</details>

<details>
<summary>
GPU problems
</summary>
<br/>

Most models can run inference (but not training) without GPU support.

</details>

<details>
<summary>
"invalid device function" or "no kernel image is available for execution".
</summary>
<br/>
Two possibilities:

* You build detectron2 with one version of CUDA but run it with a different version.

  To check whether it is the case,
  use `python -m detectron2.utils.collect_env` to find out inconsistent CUDA versions.
  In the output of this command, you should expect "Detectron2 CUDA Compiler", "CUDA_HOME", "PyTorch built with - CUDA"
  to contain cuda libraries of the same version.

  When they are inconsistent,
  you need to either install a different build of PyTorch (or build by yourself)
  to match your local CUDA installation, or install a different version of CUDA to match PyTorch.

* PyTorch/torchvision/Detectron2 is not built for the correct GPU architecture (aka. compute capability).

  The architecture included by PyTorch/detectron2/torchvision is available in the "architecture flags" in
  `python -m detectron2.utils.collect_env`. It must include
  the architecture of your GPU, which can be found at [developer.nvidia.com/cuda-gpus](https://developer.nvidia.com/cuda-gpus).

  If you're using pre-built PyTorch/detectron2/torchvision, they have included support for most popular GPUs already.
  If not supported, you need to build them from source.

  When building detectron2/torchvision from source, they detect the GPU device and build for only the device.
  This means the compiled code may not work on a different GPU device.
  To recompile them for the correct architecture, remove all installed/compiled files,
  and rebuild them with the `TORCH_CUDA_ARCH_LIST` environment variable set properly.
  For example, `export TORCH_CUDA_ARCH_LIST=6.0,7.0` makes it compile for both P100s and V100s.
</details>

<details>
<summary>
Undefined CUDA symbols; Cannot open libcudart.so
</summary>
<br/>
The version of NVCC you use to build detectron2 or torchvision does
not match the version of CUDA you are running with.
This often happens when using anaconda's CUDA runtime.

Use `python -m detectron2.utils.collect_env` to find out inconsistent CUDA versions.
In the output of this command, you should expect "Detectron2 CUDA Compiler", "CUDA_HOME", "PyTorch built with - CUDA"
to contain cuda libraries of the same version.

When they are inconsistent,
you need to either install a different build of PyTorch (or build by yourself)
to match your local CUDA installation, or install a different version of CUDA to match PyTorch.
</details>


### Test JASON request
post in /predict-image

```
{
    "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSKvPhv-QATOz9jSQBWr1TFeYDrMCWrYsJ60w&usqp=CAU"
}

```

### Expected output

```


```
