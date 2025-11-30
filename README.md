# TinyML Vehicle Driving Status Detection System

A real-time vehicle driving status detection system based on the QuecPython embedded platform, utilizing the MPU6500 sensor and a Random Forest classifier.

## System Overview

This TinyML system employs machine learning directly on embedded hardware to detect vehicle driving status in real time. The system uses a small sensor called MPU6500 to measure motion and rotation, and it is currently optimized for motion along the X-axis, Y-axis, Z-axis, and gyroscopic motion.

## Features

- **Real-time Detection**: Recognition response time ranges from 150ms to 300ms
- **Memory Efficiency**: Automatic buffer management with overflow prevention
- **False Alarm Prevention**: Requires 3 consecutive consistent results before detection confirmation
- **Timer-based Processing**: Non-blocking hardware timer architecture
- **Gesture Separation**: Independent analysis of each gesture to avoid mutual interference

## Directory Structure

```plaintext
tinyml-car/
├── src
	├── _main.py              # Main application based on the timer system
	├── mpu6500.py            # MPU6500 sensor driver with m/s² scaling
	├── random_forest.py      # Pre-trained random forest model
	├── tinyml.py             # TinyML pipeline with anti-shake mechanism
├── fw
├── LICENSE
├── README.md
└── README_zh.md
```

## Technical Details

- **Platform**: Quectel embedded module running MicroPython
- **Sensor**: MPU6500 6-axis IMU (3-axis accelerometer + 3-axis gyroscope)
- **Model**: Random Forest classifier (4 categories: 1 = driving on flat ground, 2 = uphill, 3 = downhill, 4 = skidding)
- **Sampling**: 50Hz sensor reading, 20Hz inference
- **Detection**: 3 consecutive consistent results within a 450ms window
- **Data Format**: Accelerometer (m/s²), Gyroscope (deg/s)

## Current Status

- **X/Y/Z-axis Motion** - Reliable operation and stable detection
- **Memory Management** - Buffer contamination issue resolved
- **Real-time Processing** - Timer-based architecture implemented
- **Anti-shake System** - False alarm prevention function working properly
- **Circular Motion** - Currently under development

## Quick Start

### Prerequisites

Before you start, please ensure you have the following prerequisites:

- **Hardware**:
  - A QuecPython development board
  - A computer (Windows 7, Windows 10, or Windows 11)
  - An MPU6500 sensor
- **Software**:
  - Debugging tool [QPYcom](https://developer.quectel.com/wp-content/uploads/2024/09/QPYcom_V3.9.0.zip)
  - QuecPython firmware (The EG912U firmware can be found in the `fw` directory of the repository)
  - Python text editor (e.g., [VSCode](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/download/))

### Installation

1. **Clone the repository**:

```plaintext
git clone https://github.com/aaronchenzhihe/Tinyml-car.git
```

   2.**Flash the firmware**: Flash the firmware to the development board according to the instructions.

### Run the Application

1. **Hardware Connection**: Correctly connect the MPU6500 sensor to the I2C interface of the development board.
2. **Connect to the host computer via Type-C cable**.
3. Download the code to the device:
   - Launch the QPYcom debugging tool.
   - Connect the data cable to the computer.
   - Press the **PWRKEY** button on the development board to power it on.
   - Import all files in the `src` folder into the module's file system while maintaining the directory structure, following the [instructions](https://developer.quectel.com/doc/quecpython/Getting_started/en/4G/first_python.html).
4. Run the code
   - Select the `File` tab.
   - Select the `_main.py` script.
   - Right-click and select `Run` to execute the script.

## Usage

The system automatically performs real-time detection. When a vehicle driving status is recognized, it outputs the classification result (1, 2, 3, 4) and clears all buffers to prevent interference from previous results.

## Performance

- **Detection Latency**: Theoretical minimum of 150ms, actual range of 200-300ms
- **Memory Usage**: Total < 50KB
- **Accuracy**: Optimized for X/Y/Z-axis motion and gyroscopic motion