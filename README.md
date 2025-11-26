# wifi-rvr-iperf3
基于IPerf3的WiFi RVR自动化测试
实践加学习，不断完善，尽力做到适配各种系统并简化配置
# src 目录说明

- **main.py**：程序入口，负责项目逻辑调度
- **att.py**：衰减器控制，目前只支持特定的衰减器，后面需要拓展为通用支持方式
- **config.ini**: 测试配置文件，包括DUT, STA，Iperf3等等
- **config.py**: 配置函数文件，将config.ini中的参数进行处理
- **data.py**: 数据函数文件，处理测试得到的各种数据
- **iper.py**: iperf3 server和client指令的调用
- **parameters.py**: 通过config函数将ini中的配置生成调用参数，考虑和config.py进行合并优化
- **report.py**: 将测试结果生成Excel形式的测试报告
- **rssi.py**: 获取无线网卡端的RSSI
- **rssi_product**:通过指令获取测试中的相关统计信息，比如RSSI, NSS, RATE, MODE等等
- **switch.py**: switch开关，在有必要的情况下切换线路使用
- **throughput.py**: 处理iperf3测试结果中的TP值
- **turntable.py，turntable_telnetlib3.py**: 转台函数，调用转台旋转，目前只支持特定转台，后面需要拓展为通用支持方式
- **write_datas.py**:将测试中的数据写入txt文件中
