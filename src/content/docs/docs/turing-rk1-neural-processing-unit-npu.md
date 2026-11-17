---
title: "NPU"
description: "The Turing RK1 compute module is equipped with an NPU (Neural Processing Unit), a neural network acceleration engine that can deliver up to 6 TOPS of…"
head:
  - tag: title
    content: "Neural Processing Unit (NPU) | Turing RK1 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## NPU and RKNN SDK

The Turing RK1 compute module is equipped with an NPU (Neural Processing Unit), a neural network acceleration engine that can deliver up to 6 TOPS of processing performance. To utilize this NPU, you'll need to download the RKNN SDK, which provides programming interfaces for platforms with the RK3588 chip. This SDK simplifies the deployment of RKNN models exported by RKNN-Toolkit2, accelerating the development of AI applications.

## RKNN Model

RKNN is the model type used by the Rockchip NPU platform. It's a model file with the .rknn suffix. The RKNN SDK provides a comprehensive Python tool for model transformation, allowing users to convert their self-developed algorithm model into an RKNN model. The RKNN model can run directly on the Turing RK1. There are demos available under rknpu2/examples. You can refer to the README.md to compile Linux Demo (cross-compile environment needed). You can also download the compiled demo and run it on the Turing RK1.

## Non-RKNN Model

For other models like `Caffe`, `TensorFlow`, etc., to run on the RK3588 platform, conversions are needed. You can use the RKNN-Toolkit2 to convert these models into an RKNN model.

## RKNN-Toolkit2

### Introduction of Tool

RKNN-Toolkit2 is a development kit that provides model conversion, inference, and performance evaluation on PC and Rockchip NPU platforms. Users can easily complete the following functions through the Python interface provided by the tool:

* **Model conversion**: Supports the conversion of `Caffe` / `TensorFlow` / `ONNX` / `Darknet` / `PyTorch` models to RKNN models. It supports RKNN model import/export, which can be used on Rockchip NPU platform later.
* **Quantization**: Supports the conversion of float models to quantization models. Currently, it supports quantized methods including asymmetric quantization(asymmetric\_quantized-8, asymmetric\_quantized-16), and hybrid quantization. Asymmetric\_quantized-16 is not supported yet.
* **Model inference**: Able to simulate Rockchip NPU to run RKNN model on PC and get the inference result. This tool can also distribute the RKNN model to the specified NPU device to run, and get the inference results.
* **Performance evaluation**: Distribute the RKNN model to the specified NPU device to run, and evaluate the model performance in the actual device.
* **Memory evaluation**: Evaluate memory consumption at runtime of the model. When using this function, the RKNN model must be distributed to the NPU device to run, and then call the relevant interface to obtain memory information.
* **Quantitative error analysis**: This function will give the Euclidean or cosine distance of each layer of inference results before and after the model is quantized. This can be used to analyze how quantitative error occurs, and provide ideas for improving the accuracy of quantitative models.

### Environment Dependence

The system needs:

* Ubuntu 18.04 (x64) or later. 
* Python version: 3.6/3.8
* Python dependencies are listed in the document doc/requirements\_cp36-1.3.0.txt for Python 3.6 and doc/requirements\_cp38-1.3.0.txt for Python 3.8.

```python
#Python3.6
cat doc/requirements_cp36-1.3.0.txt
numpy==1.16.6
onnx==1.7.0
onnxoptimizer==0.1.0
onnxruntime==1.6.0
tensorflow==1.14.0
tensorboard==1.14.0
protobuf==3.12.0
torch==1.6.0
torchvision==0.7.0
psutil==5.6.2
ruamel.yaml==0.15.81
scipy==1.2.1
tqdm==4.27.0
requests==2.21.0
opencv-python==4.4.0.46
PuLP==2.4
scikit_image==0.17.2
# if install bfloat16 failed, please install numpy manually first. "pip install numpy==1.16.6"
bfloat16==1.1
flatbuffers==1.12

#Python3.8
cat doc/requirements_cp38-1.3.0.txt
numpy==1.17.3
onnx==1.7.0
onnxoptimizer==0.1.0
onnxruntime==1.6.0
tensorflow==2.2.0
tensorboard==2.2.2
protobuf==3.12.0
torch==1.6.0
torchvision==0.7.0
psutil==5.6.2
ruamel.yaml==0.15.81
scipy==1.4.1
tqdm==4.27.0
requests==2.21.0
opencv-python==4.4.0.46
PuLP==2.4
scikit_image==0.17.2
# if install bfloat16 failed, please install numpy manually first. "pip install numpy==1.17.3"
bfloat16==1.1
```

## RKNN-Toolkit2 installation

It is recommended to use `virtualenv` to manage the python environment because there may be multiple versions of the

python environment in the system at the same time. Here's how you can install it using Python 3.6 as an example:

1. Install `virtualenv`, Python3.6, and pip3:

```python
sudo apt install virtualenv
sudo apt-get install python3 python3-dev python3-pip
```

2. Install dependent libraries:

```python
sudo apt-get install libxslt1-dev zlib1g zlib1g-dev libglib2.0-0 libsm6 libgl1-mesa-glx libprotobuf-dev gcc
```

3. Use `virtualenv` and install Python dependency, such as requirements\_cp36-1.3.0.txt:

```python
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip3 install -r doc/requirements_cp36-*.txt
```

4. Install RKNN-Toolkit2, such as rknn\_toolkit2-1.3.0\_11912b58-cp36-cp36m-linux\_x86\_64.whl:

```python
sudo pip3 install packages/rknn_toolkit2*cp36*.whl
```

5. Check if RKNN-Toolkit2 is installed successfully or not, press key ctrl+d to exit:

```python
(venv) turing@T-chip:~/rknn-toolkit2$ python3
>>> from rknn.api import RKNN
>>>
```

The installation is successful if the import of RKNN module doesn’t fail.

### Model Conversion Demo

Toolkit Demos are under `rknn-toolkit2/examples`. Here we run a model conversion demo for example, this demo shows the process of converting `tflite` to RKNN, exporting model, inferencing, deploying on NPU and fetching results. For detailed implementation of the model conversion, please refer to the source code in Demo and the documents at the end of this page.

### Other Toolkit Demo

Other Toolkit demos can be found under rknn-toolkit2/examples/, such as quantization, accuracy analysis demos. For detailed implementation, please refer to the source code in Demo and the detailed development documents.

## Official Documents

[https://github.com/rockchip-linux/rknpu2](https://github.com/rockchip-linux/rknpu2)
