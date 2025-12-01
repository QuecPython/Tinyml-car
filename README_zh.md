# TinyML 汽车行驶状态检测系统

基于 QuecPython 嵌入式平台，使用 MPU6500  传感器和随机森林分类器的实时汽车行驶状态检测系统。

## 系统概述

该 TinyML 系统直接在嵌入式硬件上使用机器学习实时检测汽车行驶状态。系统采用名为 MPU6500 的小型传感器来测量运动和旋转，目前针对 X 轴 Y 轴和Z 轴以及陀螺仪运动进行了优化。

## 功能特点

*   **实时检测**识别响应时间为 150-300ms

*   **内存高效**：具有溢出预防的自动缓冲区管理

*   **误报预防**：检测前需要 3 个连续一致的结果

*   **基于定时器的处理**：非阻塞硬件定时器架构

*   **手势分离**：每个手势独立分析，避免相互干扰

## 目录结构

```plaintext
tinyml-car/
├── src
	├── _main.py              # 基于定时器系统的主应用程序
	├── mpu6500.py            # 带m/s²缩放的MPU6500传感器驱动
	├── random_forest.py      # 预训练随机森林模型
	├── tinyml.py             # 带防抖机制的TinyML流水线
├── fw
├── LICENSE
├── README.md
└── README_zh.md
```

## 技术细节

*   **平台**：运行 MicroPython 的 Quectel 嵌入式模块

*   **传感器**：MPU6500 6 轴 IMU（3 轴加速度计 + 3 轴陀螺仪）

*   **模型**：随机森林分类器（4类：1 =平地行驶，2=上坡， 3=下坡， 4=侧滑）

*   **采样**：50Hz 传感器读取，20Hz 推理

*   **检测**：450ms 窗口内 3 个连续一致的结果

*   **数据格式**：加速度计（m/s²），陀螺仪（deg/s）

## 当前状态

*   **X/Y/Z 轴运动** - 工作可靠，检测稳定

*   **内存管理** - 缓冲区污染问题已解决

*   **实时处理** - 基于定时器的架构已实现

*   **防抖系统** - 误报预防功能正常工作

*   **圆周运动** - 目前正在开发中

## 快速开始

### 前提条件

开始之前，请确保您具备以下前提条件：

* **硬件**：

  *   一块 QuecPython 开发板
  
  
    *   计算机（Windows 7、Windows 10 或 Windows 11）
  
  
    *   MPU6500 传感器
  


* **软件**：

  *   调试工具 [QPYcom](https://developer.quectel.com/wp-content/uploads/2024/09/QPYcom_V3.9.0.zip)
  
  
    *   QuecPython 固件（EG912U固件可在仓库的`fw`目录中找到）
  
  
    *   Python 文本编辑器（例如 [VSCode](https://code.visualstudio.com/)、[PyCharm](https://www.jetbrains.com/pycharm/download/)）
  

### 安装

1.  **克隆仓库：**

```python
git clone https://github.com/QuecPython/Tinyml-Fall.git
```

   2.**烧录固件：** 按照说明将固件烧录到开发板上。

### 运行应用程序

1.  **硬件连接：** 将 MPU6500 传感器正确连接到开发板的 I2C 接口。

2.  **通过 Type-C 连接到主机计算机。**

3. **将代码下载到设备：**

   *   启动 QPYcom 调试工具。

   *   将数据线连接到计算机。

   *   按下开发板上的**PWRKEY**按钮上电。

   *   按照[说明](https://developer.quectel.com/doc/quecpython/Getting_started/en/4G/first_python.html)将`src`文件夹中的所有文件导入到模块的文件系统中，保持目录结构。

4. **运行代码**

   *   选择`File`标签页。


   *   选择`_main.py`脚本。


   *   右键单击`Run`执行脚本。




## 使用方法

系统会自动实时检测。当识别到车辆行驶状态时，会输出分类结果（1、2、3、4 ）并清除所有缓冲区，以防止来自先前结果的干扰。

## 性能

*   **检测延迟**：理论最小值 150ms，实际 200-300ms

*   **内存使用**：总计 < 50KB

*   **准确性**：针对 X/Y/Z 轴以及陀螺仪运动进行了优化