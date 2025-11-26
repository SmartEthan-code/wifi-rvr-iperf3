# -*- coding: utf-8 -*-

# 使用布局管理器重新设计的RVR GUI界面
# 基于原始rvrgui.py文件，但使用布局管理器来实现自适应布局

import os
import json
import datetime
import logging
import threading
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from status_check import StatusCheck


class ConfigManager:
    def __init__(self):
        self.config_dir = "config"
        self._ensure_config_dir()
        self.default_config = {
            "window_width": 800,
            "window_height": 600,
            "turntable_enabled": False,
            "turntable_port": "COM3"
        }
        
    def _ensure_config_dir(self):
        """确保配置目录存在"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
    def get_all_configs(self):
        """获取所有配置文件"""
        self._ensure_config_dir()
        configs = []
        for file in os.listdir(self.config_dir):
            if file.endswith(".json"):
                configs.append(file[:-5])  # 移除 .json 后缀
        return configs
    
    def save_config(self, name, config_data):
        """保存配置到文件"""
        self._ensure_config_dir()
        config_data["name"] = name
        config_data["created_at"] = datetime.datetime.now().isoformat()
        config_data["updated_at"] = config_data["created_at"]
        
        file_path = os.path.join(self.config_dir, f"{name}.json")
        with open(file_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        return True
    
    def load_config(self, name=None):
        """从文件加载配置，未指定名称时返回默认配置"""
        if name is None:
            return self.default_config
            
        file_path = os.path.join(self.config_dir, f"{name}.json")
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def delete_config(self, name):
        """删除配置文件"""
        file_path = os.path.join(self.config_dir, f"{name}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

class ConfigManagerDialog(QtWidgets.QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("Manage Configurations")
        self.resize(400, 300)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # 配置列表
        self.list_widget = QtWidgets.QListWidget(self)
        layout.addWidget(self.list_widget)
        
        # 按钮布局
        button_layout = QtWidgets.QHBoxLayout()
        
        self.btn_delete = QtWidgets.QPushButton("Delete", self)
        self.btn_delete.clicked.connect(self.delete_config)
        button_layout.addWidget(self.btn_delete)
        
        self.btn_load = QtWidgets.QPushButton("Load", self)
        self.btn_load.clicked.connect(self.accept)
        button_layout.addWidget(self.btn_load)
        
        self.btn_cancel = QtWidgets.QPushButton("Cancel", self)
        self.btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_cancel)
        
        layout.addLayout(button_layout)
        
        # 加载配置列表
        self.load_config_list()
        
    def load_config_list(self):
        """加载配置列表"""
        self.list_widget.clear()
        configs = self.config_manager.get_all_configs()
        for config in configs:
            self.list_widget.addItem(config)
    
    def delete_config(self):
        """删除选中的配置"""
        current_item = self.list_widget.currentItem()
        if current_item:
            config_name = current_item.text()
            reply = QtWidgets.QMessageBox.question(
                self, 
                "Confirm Delete",
                f"Are you sure you want to delete configuration '{config_name}'?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                self.config_manager.delete_config(config_name)
                self.load_config_list()
    
    def get_selected_config(self):
        """获取选中的配置名称"""
        current_item = self.list_widget.currentItem()
        if current_item:
            return current_item.text()
        return None

class Ui_MainWindow(object):
    def __init__(self):
        # 自动加载上次的配置
        self.load_last_config()
        
    def save_last_config(self):
        """保存当前配置到文件"""
        import json
        config = self.collect_config()
        with open("last_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
    def load_last_config(self):
        """从文件加载上次的配置"""
        import json
        import os
        
        if os.path.exists("last_config.json"):
            try:
                with open("last_config.json", "r") as f:
                    config = json.load(f)
                    self.apply_config(config)
            except Exception as e:
                print(f"加载上次配置失败: {str(e)}")
        """收集所有配置参数"""
        
    def _get_selected_radios(self):
        """获取选中的Radio"""
        radios = []
        if self.radioButton2.isChecked():
            radios.append("2G")
        if self.radioButton5.isChecked():
            radios.append("5G")
        if self.radioButton6.isChecked():
            radios.append("6G")
        return radios
        

    def _get_test_type(self):
        """获取测试类型，默认选择OTA方式"""
        from switch import Switch
        try:
            switch = Switch("192.168.1.1")  # 替换为实际的交换机IP
            if not switch.is_connected():
                self.log_message("Switch未连接，使用默认测试类型", logging.WARNING)
                return "OTA"
            test_type = switch.get_test_type()
            if test_type not in ["OTA", "Conducted"]:
                test_type = "OTA"  # 默认选择OTA
            return test_type
        except Exception as e:
            self.log_message(f"获取测试类型失败: {e}", logging.ERROR)
            return "OTA"  # 默认选择OTA
        """获取测试类型"""
        if self.radioButton_ota.isChecked():
            return "OTA"
        else:
            return "Conducted"
            
    def collect_config(self):
        """收集当前UI中的所有配置数据"""
        config = {}
        
        # AP配置
        ap_config = {
            "connection_type": "SSH" if self.sshButton.isChecked() else "ADB",
            "ap_ip": self.ApIp.text(),
            "username": self.Username.text(),
            "password": self.Password.text(),
            "ap_name": self.ApName.text(),
            "radio": self._get_selected_radios(),
            "ssid": self.ApSSID.text(),
            "channel": self.Channel.text(),
            "ap_lan": self.ap_lan.text()
        }
        config["ap_config"] = ap_config
        
        # Station配置
        sta_config = {}
        if self.staTypeCombo.currentText() == "Wireless Card-PC":
            sta_config["sta_type"] = "Wireless Card-PC"
            sta_config["sta_ip"] = self.WcStaIp.text(),
            sta_config["username"] = self.WcUsername.text(),
            sta_config["password"] = self.WcPassword.text()
        else:
            sta_config["sta_type"] = "Client-DUT"
            sta_config["sta_ip"] = self.CdStaIp.text(),
            sta_config["username"] = self.CdUsername.text(),
            sta_config["password"] = self.CdPassword.text()
        config["station_config"] = sta_config
        
        # 衰减器配置
        atten_config = {
            "start": self.Start.text(),
            "end": self.End.text(),
            "step": self.Step.text(),
            "cable_loss": self.LineLoss.text(),
            "atten_ip": self.AttenIP.text()
        }
        config["attenuation_config"] = atten_config
        
        # 转台配置
        turntable_config = {
            "ip": self.TurnIp.text(),
            "angles": self.angles_num.text()
        }
        config["turntable_config"] = turntable_config
        
        # 测试类型
        config["test_type"] = self._get_test_type()
        
        # 本地PC角色
        config["local_pc_role"] = self.localPcRoleCombo.currentText()
        
        return config
            
    def check_dependencies(self):
        """检查依赖项"""
        try:
            # 检查 paramiko 库
            import paramiko
            self.log_message("paramiko 库已安装", logging.INFO)
        except ImportError:
            self.log_message("缺少 paramiko 库，尝试安装...", logging.WARNING)
            try:
                import subprocess
                subprocess.check_call(["pip", "install", "paramiko"])
                self.log_message("paramiko 安装成功", logging.INFO)
            except Exception as e:
                self.log_message(f"无法安装 paramiko: {str(e)}", logging.ERROR)
                self.log_message("请手动运行: pip install paramiko", logging.ERROR)
                
        # 检查 iperf3 命令行工具
        try:
            import subprocess
            result = subprocess.run(["iperf3", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.log_message(f"本地iperf3 已安装: {result.stdout.strip()}", logging.INFO)
            else:
                self.log_message("iperf3 命令测试失败", logging.WARNING)
        except Exception as e:
            self.log_message("iperf3 命令不可用，请确保已安装", logging.WARNING)
            self.log_message("Windows: 请从 https://iperf.fr/iperf-download.php 下载并安装", logging.INFO)
            self.log_message("Linux: 请运行 sudo apt install iperf3 或 sudo yum install iperf3", logging.INFO)
            
    def save_results_to_file(self):
        """保存测试结果到文件"""
        # 获取结果文本
        result_text = self.resultBrowser.toPlainText()
        if not result_text:
            QtWidgets.QMessageBox.warning(
                self.MainWindow,
                "警告",
                "没有测试结果可保存。"
            )
            return
            
        # 打开文件保存对话框
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.MainWindow,
            "保存测试结果",
            "",
            "文本文件 (*.txt);;所有文件 (*)",
            options=options
        )
        
        if file_name:
            try:
                # 如果用户没有指定扩展名，添加 .txt 扩展名
                if not file_name.endswith('.txt'):
                    file_name += '.txt'
                    
                # 写入文件
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(result_text)
                    
                self.log_message(f"测试结果已保存到: {file_name}", logging.INFO)
                QtWidgets.QMessageBox.information(
                    self.MainWindow,
                    "成功",
                    "测试结果已保存到:\n" + file_name
                )
            except Exception as e:
                error_msg = f"保存结果失败: {str(e)}"
                self.log_message(error_msg, logging.ERROR)
                QtWidgets.QMessageBox.critical(
                    self.MainWindow,
                    "错误",
                    error_msg
                )
                
    def clear_results(self):
        """清除测试结果"""
        reply = QtWidgets.QMessageBox.question(
            self.MainWindow,
            "确认",
            "确定要清除所有测试结果吗？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.resultBrowser.clear()
            self.log_message("测试结果已清除", logging.INFO)

    def apply_config(self, config):
        """应用配置到界面"""
        # AP配置
        ap_config = config.get("ap_config", {})
        connection_type = ap_config.get("connection_type", "SSH")
        self.sshButton.setChecked(connection_type == "SSH")
        self.adbButton.setChecked(connection_type == "ADB")
        
        self.ApIp.setText(ap_config.get("ap_ip", ""))
        self.Username.setText(ap_config.get("username", ""))
        self.Password.setText(ap_config.get("password", ""))
        self.ApName.setText(ap_config.get("ap_name", ""))
        
        # 设置Radio选择
        radios = ap_config.get("radio", [])
        self.radioButton2.setChecked("2G" in radios)
        self.radioButton5.setChecked("5G" in radios)
        self.radioButton6.setChecked("6G" in radios)
        
        self.ApSSID.setText(ap_config.get("ssid", ""))
        self.Channel.setText(ap_config.get("channel", ""))
        self.ap_lan.setText(ap_config.get("lan", ""))
        
        # Station配置
        sta_config = config.get("station_config", {})
        sta_type = sta_config.get("sta_type", "")
        self._set_combobox_value(self.staTypeCombo, sta_type)
        
        if sta_type == "Wireless Card-PC":
            self.WcStaIp.setText(sta_config.get("sta_ip", ""))
            self.WcUsername.setText(sta_config.get("username", ""))
            self.WcPassword.setText(sta_config.get("password", ""))
        else:  # Client-DUT
            self.CdStaIp.setText(sta_config.get("sta_ip", ""))
            self.CdUsername.setText(sta_config.get("username", ""))
            self.CdPassword.setText(sta_config.get("password", ""))
        
        # Iperf配置
        iperf_config = config.get("iperf_config", {})
        self.iperf_tcp.setChecked(iperf_config.get("mode", "") == "TCP")
        self.iperf_udp.setChecked(iperf_config.get("mode", "") == "UDP")
        self.PairNumber.setText(iperf_config.get("pair_number", ""))
        self.Duration.setText(iperf_config.get("duration", ""))
        
        # Attenuation配置
        atten_config = config.get("attenuation_config", {})
        self.Start.setText(atten_config.get("start", ""))
        self.End.setText(atten_config.get("end", ""))
        self.Step.setText(atten_config.get("step", ""))
        self.LineLoss.setText(atten_config.get("cable_loss", ""))
        self.AttenIP.setText(atten_config.get("atten_ip", ""))
        
        # Turntable配置
        turntable_config = config.get("turntable_config", {})
        self.TurnIp.setText(turntable_config.get("ip", ""))
        self.angles_num.setText(turntable_config.get("angles", ""))
        
        # 测试类型
        test_type = config.get("test_type", "OTA")
        if test_type == "Conducted":
            self.radioButton_cdt.setChecked(True)
        else:
            self.radioButton_ota.setChecked(True)  # 确保默认选中OTA

    def _set_combobox_value(self, combobox, value):
        """设置下拉框的值"""
        index = combobox.findText(value)
        if index >= 0:
            combobox.setCurrentIndex(index)
            
    def save_config_dialog(self):
        """保存配置对话框"""
        name, ok = QtWidgets.QInputDialog.getText(
            self.MainWindow,
            "Save Configuration",
            "Enter configuration name:"
        )
        
        if ok and name:
            config = self.collect_config()
            if self.config_manager.save_config(name, config):
                QtWidgets.QMessageBox.information(
                    self.MainWindow,
                    "Success",
                    f"Configuration '{name}' saved successfully."
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self.MainWindow,
                    "Error",
                    "Failed to save configuration."
                )

    def load_config_dialog(self):
        """加载配置对话框"""
        configs = self.config_manager.get_all_configs()
        if not configs:
            QtWidgets.QMessageBox.information(
                self.MainWindow,
                "No Configurations",
                "No saved configurations found."
            )
            return
            
        name, ok = QtWidgets.QInputDialog.getItem(
            self.MainWindow,
            "Load Configuration",
            "Select configuration:",
            configs,
            0,
            False
        )
        
        if ok and name:
            self.load_config(name)

    def load_config(self, name):
        """加载指定名称的配置"""
        config = self.config_manager.load_config(name)
        if config:
            self.apply_config(config)
            QtWidgets.QMessageBox.information(
                self.MainWindow,
                "Success",
                f"Configuration '{name}' loaded successfully."
            )
        else:
            QtWidgets.QMessageBox.warning(
                self.MainWindow,
                "Error",
                f"Failed to load configuration '{name}'."
            )
            
    def manage_configs(self):
        """管理配置对话框"""
        dialog = ConfigManagerDialog(self.config_manager, self.MainWindow)
        result = dialog.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            config_name = dialog.get_selected_config()
            if config_name:
                self.load_config(config_name)

    def updateSSID(self):
        """根据选中的Radio按钮更新SSID值"""
        ssids = []
        
        # 检查每个按钮的状态并添加相应的默认SSID
        if self.radioButton2.isChecked():
            ssids.append("RVR_2G")  # 2G默认SSID
        
        if self.radioButton5.isChecked():
            ssids.append("RVR_5G")  # 5G默认SSID
        
        if self.radioButton6.isChecked():
            ssids.append("RVR_6G")  # 6G默认SSID
        
        # 如果没有按钮被选中，使用空字符串
        if not ssids:
            self.ApSSID.setText("")
        else:
            # 用逗号连接多个SSID值
            self.ApSSID.setText(",".join(ssids))
    
    def updateChannel(self):
        """根据选中的Radio按钮更新Channel值"""
        channels = []
        
        # 检查每个按钮的状态并添加相应的默认Channel
        if self.radioButton2.isChecked():
            channels.append("6")  # 2G默认Channel
        
        if self.radioButton5.isChecked():
            channels.append("36")  # 5G默认Channel
        
        if self.radioButton6.isChecked():
            channels.append("37")  # 6G默认Channel
        
        # 如果没有按钮被选中，使用空字符串
        if not channels:
            self.Channel.setText("")
        else:
            # 用逗号连接多个Channel值
            self.Channel.setText(",".join(channels))
    
    def toggleSshConfig(self):
        """处理SSH按钮点击事件"""
        if self.sshButton.isChecked():
            self.sshWidget.setVisible(True)
            self.adbWidget.setVisible(False)
    
    def toggleAdbConfig(self):
        """处理ADB按钮点击事件"""
        if self.adbButton.isChecked():
            self.adbWidget.setVisible(True)
            self.sshWidget.setVisible(False)
    
    def toggleStaConfig(self, index):
        """处理Station Type选择变化事件"""
        if index == 0:  # Wireless Card-PC
            self.wirelessCardConfig.setVisible(True)
            self.clientDutConfig.setVisible(False)
        else:  # Client-DUT
            self.wirelessCardConfig.setVisible(False)
            self.clientDutConfig.setVisible(True)
            
    def updateLocalPcRoleUI(self):
        """根据本地PC角色更新UI上的连接设置可用性"""
        local_pc_role = self.localPcRoleCombo.currentText()
        self.log_message(f"程序运行PC连接对象: {local_pc_role}")
        
        # 不再禁用任何连接设置，因为即使本地角色也需要这些设置
        # 例如：本地AP角色仍需要SSH设置来连接到AP
        # 本地Wireless Card-PC角色仍需要IP地址来ping检查
        # 本地Client-DUT角色仍需要SSH设置来连接到DUT
        
        # 启用所有连接设置
        self.ApIp.setEnabled(True)
        self.Username.setEnabled(True)
        self.Password.setEnabled(True)
        self.WcStaIp.setEnabled(True)
        self.WcUsername.setEnabled(True)
        self.WcPassword.setEnabled(True)
        self.CdStaIp.setEnabled(True)
        self.CdUsername.setEnabled(True)
        self.CdPassword.setEnabled(True)
        
        # 根据本地角色添加提示信息
        if local_pc_role == "AP-LAN":
            self.log_message("提示：程序运行在与AP LAN口相连的PC上")
        elif local_pc_role == "Wireless Card-PC/Demo-LAN":
            self.log_message("提示：程序运行在无线网卡或与Demo/DUT LAN口相连的PC上")

    def setup_label_properties(self, label):
        """设置标签的通用属性，包括大小策略和固定高度"""
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        label.setSizePolicy(sizePolicy)
        # label.setMinimumWidth(60)
        # label.setFixedHeight(25)  # 设置固定高度，确保标签高度不变
    
    def toggle_lan_enabled(self, checkbox, ip_input, username_input, password_input):
        """根据复选框状态切换输入框的可用性"""
        ip_input.setEnabled(checkbox.isChecked())
        username_input.setEnabled(checkbox.isChecked())
        password_input.setEnabled(checkbox.isChecked())

    def setup_text_properties(self, text_edit):
        """设置文本输入框的通用属性，包括大小策略和固定高度"""
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        text_edit.setSizePolicy(sizePolicy)
        # text_edit.setMinimumWidth(60)
        # text_edit.setFixedHeight(25)  # 设置固定高度，确保文本框高度不变
        
    def setup_groupbox_properties(self, groupbox, stretch_factor):
        """设置GroupBox的尺寸策略和最小高度"""
        # 使用Minimum垂直策略，使GroupBox可以根据内容扩展
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(stretch_factor)
        groupbox.setSizePolicy(sizePolicy)
               
    def setup_button_properties(self, button):
        """设置按钮的通用属性，包括大小策略和固定高度"""
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        button.setSizePolicy(sizePolicy)
        # button.setFixedHeight(25)  # 设置固定高度，确保按钮高度不变
    
    def setup_combobox_properties(self, combobox):
        """设置下拉框的通用属性，包括大小策略和固定高度"""
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        combobox.setSizePolicy(sizePolicy)
        # combobox.setFixedHeight(25)  # 设置固定高度，确保下拉框高度不变
    
    def setup_radiobutton_properties(self, radiobutton):
        """设置单选按钮的通用属性，包括大小策略和固定高度"""
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        radiobutton.setSizePolicy(sizePolicy)
        # radiobutton.setFixedHeight(25)  # 设置固定高度，确保单选按钮高度不变
    
    def setupUi(self, MainWindow):
        # 保存对MainWindow的引用
        self.MainWindow = MainWindow
        # 设置窗口基本属性
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))  # 设置最小尺寸
        
        # 设置窗口调色板
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        
        # 设置窗口字体
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        MainWindow.setFont(font)
        
        # 设置窗口图标
        icon = QtGui.QIcon.fromTheme("./64.ico")
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        
        # 创建中央部件
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # 创建主布局
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")
        
        # 创建分割器，允许用户拖拉调整左右两侧的大小
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        
        # 创建左侧配置区的容器
        self.leftWidget = QtWidgets.QWidget()
        
        # 创建左侧布局
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.leftLayout.setObjectName("leftLayout")
        self.leftLayout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        
        # 创建滚动区域
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)  # 允许内容widget调整大小
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)  # 需要时显示垂直滚动条
        
        # 创建滚动区域的内容widget
        self.scrollContent = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollContent)
        self.scrollLayout.setObjectName("scrollLayout")
        self.scrollLayout.setContentsMargins(5, 5, 5, 5)  # 设置小边距
        
        # ===== AP配置框架 =====
        self.APframe = QtWidgets.QGroupBox("AP")
        self.APframe.setObjectName("APframe")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.APframe.setFont(font)

        # 设置AP框架的背景色
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.APframe.setPalette(palette)
        self.APframe.setAutoFillBackground(True)
        
        # AP框架内部使用表单布局
        self.apFormLayout = QtWidgets.QFormLayout(self.APframe)
        self.apFormLayout.setObjectName("apFormLayout")
        # 设置表单布局的字段增长策略为所有字段都增长
        self.apFormLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        # 设置标签对齐方式
        self.apFormLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
        # 设置行包装策略
        self.apFormLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        
        # AP Name
        self.label_ap_name = QtWidgets.QLabel("AP Name")
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_ap_name.setFont(font)
        self.setup_label_properties(self.label_ap_name)
        self.ApName = QtWidgets.QLineEdit()
        self.setup_text_properties(self.ApName)
        self.ApName.setText("GW12")
        ap_layout1 = QtWidgets.QHBoxLayout()
        ap_layout1.addWidget(self.label_ap_name)
        ap_layout1.addWidget(self.ApName)
        self.apFormLayout.addRow(ap_layout1)

        # AP IP
        self.label_ap_ip = QtWidgets.QLabel("AP IP")
        self.label_ap_ip.setFont(font)
        self.setup_label_properties(self.label_ap_ip)
        self.ApIp = QtWidgets.QLineEdit()
        self.setup_text_properties(self.ApIp)
        self.ApIp.setText("192.168.1.1")
        # self.apFormLayout.addRow(self.label_ap_ip, self.ApIp)
        
        self.label_username = QtWidgets.QLabel("Username")
        self.label_username.setFont(font)
        self.setup_label_properties(self.label_username)
        self.Username = QtWidgets.QLineEdit()
        self.setup_text_properties(self.Username)
        self.Username.setText("root")
        # self.apFormLayout.addRow(self.label_username, self.Username)
        
        self.label_password = QtWidgets.QLabel("Password")
        self.label_password.setFont(font)
        self.setup_label_properties(self.label_password)
        self.Password = QtWidgets.QLineEdit()
        self.setup_text_properties(self.Password)
        self.Password.setText("adminadminadmina")
        # self.apFormLayout.addRow(self.label_password, self.Password)
        ap_layout2 = QtWidgets.QHBoxLayout()
        # ap_layout.addWidget(self.label_ap_name)
        # ap_layout.addWidget(self.ApName)
        ap_layout2.addWidget(self.label_ap_ip)
        ap_layout2.addWidget(self.ApIp)
        ap_layout2.addWidget(self.label_username)
        ap_layout2.addWidget(self.Username)
        ap_layout2.addWidget(self.label_password)
        ap_layout2.addWidget(self.Password)
        self.apFormLayout.addRow(ap_layout2)
         
        # Radio - 使用可切换的按钮而不是单选按钮，允许多选
        self.label_radio = QtWidgets.QLabel("Radio")
        self.label_radio.setFont(font)
        self.setup_label_properties(self.label_radio)
        self.radioLayout = QtWidgets.QHBoxLayout()
        self.radioButton2 = QtWidgets.QPushButton("2G")
        self.radioButton2.setCheckable(True)
        self.setup_button_properties(self.radioButton2)
        self.radioButton5 = QtWidgets.QPushButton("5G")
        self.radioButton5.setCheckable(True)
        self.setup_button_properties(self.radioButton5)
        self.radioButton6 = QtWidgets.QPushButton("6G")
        self.radioButton6.setCheckable(True)
        self.setup_button_properties(self.radioButton6)
        self.radioLayout.addWidget(self.radioButton2)
        self.radioLayout.addWidget(self.radioButton5)
        self.radioLayout.addWidget(self.radioButton6)
        # 设置默认选中2G
        self.radioButton2.setChecked(True)
        self.apFormLayout.addRow(self.label_radio, self.radioLayout)
        
        # SSID
        self.label_ssid = QtWidgets.QLabel("SSID")
        self.label_ssid.setFont(font)
        self.setup_label_properties(self.label_ssid)
        self.ApSSID = QtWidgets.QLineEdit()
        self.setup_text_properties(self.ApSSID)
        self.ApSSID.setText("RVR-2G")
        self.apFormLayout.addRow(self.label_ssid, self.ApSSID)
        
        # SSID值将在Radio按钮创建后初始化

        # Channel
        self.label_channel = QtWidgets.QLabel("Channel")
        self.label_channel.setFont(font)
        self.setup_label_properties(self.label_channel)
        self.Channel = QtWidgets.QLineEdit()
        self.setup_text_properties(self.Channel)
        self.Channel.setText("6")
        self.apFormLayout.addRow(self.label_channel, self.Channel)

        # 连接信号和槽
        self.radioButton2.clicked.connect(self.updateChannel)
        self.radioButton5.clicked.connect(self.updateChannel)
        self.radioButton6.clicked.connect(self.updateChannel)
        self.radioButton2.clicked.connect(self.updateSSID)
        self.radioButton5.clicked.connect(self.updateSSID)
        self.radioButton6.clicked.connect(self.updateSSID)        
        
        # 初始化Channel和SSID值
        self.updateSSID()
        self.updateChannel()

        # AP LAN口外接PC时IP地址，iperf需要用到
        self.checkbox_ap_lan = QtWidgets.QCheckBox("AP LAN")
        self.checkbox_ap_lan.setChecked(True)
        self.checkbox_ap_lan.stateChanged.connect(lambda: self.toggle_lan_enabled(self.checkbox_ap_lan,self.ap_lan, self.ap_lan_username,self.ap_lan_password))
        self.label_ap_lan = QtWidgets.QLabel("IP")
        self.label_ap_lan.setFont(font)
        self.setup_label_properties(self.label_ap_lan)
        self.ap_lan = QtWidgets.QLineEdit()
        self.setup_text_properties(self.ap_lan)
        self.ap_lan.setText("192.168.1.101")
        self.label_ap_lan_username = QtWidgets.QLabel("Username")
        self.label_ap_lan_username.setFont(font)
        self.setup_label_properties(self.label_ap_lan_username)
        self.ap_lan_username = QtWidgets.QLineEdit()
        self.setup_text_properties(self.ap_lan_username)
        self.ap_lan_username.setText("nsb")
        self.label_ap_lan_password = QtWidgets.QLabel("Password")
        self.label_ap_lan_password.setFont(font)
        self.setup_label_properties(self.label_ap_lan_password)
        self.ap_lan_password = QtWidgets.QLineEdit()
        # self.ap_lan_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setup_text_properties(self.ap_lan_password)
        self.ap_lan_password.setText("Nokia#1234")
        ap_lan_layout = QtWidgets.QHBoxLayout()
        ap_lan_layout.addWidget(self.checkbox_ap_lan)
        ap_lan_layout.addWidget(self.label_ap_lan)
        ap_lan_layout.addWidget(self.ap_lan)
        ap_lan_layout.addWidget(self.label_ap_lan_username)
        ap_lan_layout.addWidget(self.ap_lan_username)
        ap_lan_layout.addWidget(self.label_ap_lan_password)
        ap_lan_layout.addWidget(self.ap_lan_password)
        self.apFormLayout.addRow(ap_lan_layout)

        
        # 设置AP框架的尺寸策略和拉伸因子
        self.setup_groupbox_properties(self.APframe, 0)  # AP配置较多，给予更多空间
        
        # 添加AP框架到滚动区域布局
        self.scrollLayout.addWidget(self.APframe)
        
        # ===== STATION配置框架 =====
        self.STAframe = QtWidgets.QGroupBox("STATION")
        self.STAframe.setObjectName("STAframe")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.STAframe.setFont(font)
        
        # 设置STATION框架的背景色
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.STAframe.setPalette(palette)
        self.STAframe.setAutoFillBackground(True)
        
        # STATION框架内部使用表单布局
        self.staFormLayout = QtWidgets.QFormLayout(self.STAframe)
        self.staFormLayout.setObjectName("staFormLayout")
        # 设置表单布局的字段增长策略为所有字段都增长
        self.staFormLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        # 设置标签对齐方式
        self.staFormLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
        # 设置行包装策略
        self.staFormLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        
        # STA Type
        self.label_sta = QtWidgets.QLabel("STA Type")
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_sta.setFont(font)
        self.setup_label_properties(self.label_sta)
        self.staTypeCombo = QtWidgets.QComboBox()
        self.setup_combobox_properties(self.staTypeCombo)
        self.staTypeCombo.addItem("Wireless Card-PC")
        self.staTypeCombo.addItem("Client-DUT")
        self.staFormLayout.addRow(self.label_sta, self.staTypeCombo)
        
        # 创建两个配置容器，根据选择显示不同的配置项
        self.wirelessCardConfig = QtWidgets.QWidget()
        self.wirelessCardLayout = QtWidgets.QFormLayout(self.wirelessCardConfig)
        self.wirelessCardLayout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        
        # Wireless Card-PC 配置项
        self.label_wc_ip = QtWidgets.QLabel("STA IP")
        self.label_wc_ip.setFont(font)
        self.setup_label_properties(self.label_wc_ip)
        self.WcStaIp = QtWidgets.QLineEdit()
        self.setup_text_properties(self.WcStaIp)
        self.WcStaIp.setText("192.168.1.9")
        # self.wirelessCardLayout.addRow(self.label_wc_ip, self.WcStaIp)
        
        self.label_wc_username = QtWidgets.QLabel("Username")
        self.label_wc_username.setFont(font)
        self.setup_label_properties(self.label_wc_username)
        self.WcUsername = QtWidgets.QLineEdit()
        self.setup_text_properties(self.WcUsername)
        self.WcUsername.setText("root")
        # self.wirelessCardLayout.addRow(self.label_wc_username, self.WcUsername)
        
        self.label_wc_password = QtWidgets.QLabel("Password")
        self.label_wc_password.setFont(font)
        self.setup_label_properties(self.label_wc_password)
        self.WcPassword = QtWidgets.QLineEdit()
        self.setup_text_properties(self.WcPassword)
        self.WcPassword.setText("nsb@1234")
        # self.wirelessCardLayout.addRow(self.label_wc_password, self.WcPassword)
        sta_layout = QtWidgets.QHBoxLayout()
        sta_layout.addWidget(self.label_wc_ip)
        sta_layout.addWidget(self.WcStaIp)
        sta_layout.addWidget(self.label_wc_username)
        sta_layout.addWidget(self.WcUsername)
        sta_layout.addWidget(self.label_wc_password)
        sta_layout.addWidget(self.WcPassword)
        self.wirelessCardLayout.addRow(sta_layout)
        
        # Client-DUT 配置项
        self.clientDutConfig = QtWidgets.QWidget()
        self.clientDutLayout = QtWidgets.QFormLayout(self.clientDutConfig)
        self.clientDutLayout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        
        self.label_cd_ip = QtWidgets.QLabel("DEMO/DUT  IP")
        self.label_cd_ip.setFont(font)
        self.CdStaIp = QtWidgets.QLineEdit()
        self.setup_text_properties(self.CdStaIp)
        self.CdStaIp.setText("192.168.1.10")
        # self.clientDutLayout.addRow(self.label_cd_ip, self.CdStaIp)
        
        self.label_cd_username = QtWidgets.QLabel("Username")
        self.label_cd_username.setFont(font)
        self.setup_label_properties(self.label_cd_username)
        self.CdUsername = QtWidgets.QLineEdit()
        self.setup_text_properties(self.CdUsername)
        self.CdUsername.setText("admin")
        # self.clientDutLayout.addRow(self.label_cd_username, self.CdUsername)
        
        self.label_cd_password = QtWidgets.QLabel("Password")
        self.label_cd_password.setFont(font)
        self.setup_label_properties(self.label_cd_password)
        self.CdPassword = QtWidgets.QLineEdit()
        self.setup_text_properties(self.CdPassword)
        self.CdPassword.setText("password")
        # self.clientDutLayout.addRow(self.label_cd_password, self.CdPassword)
        cd_layout = QtWidgets.QHBoxLayout()
        cd_layout.addWidget(self.label_cd_ip)
        cd_layout.addWidget(self.CdStaIp)
        cd_layout.addWidget(self.label_cd_username)
        cd_layout.addWidget(self.CdUsername)
        cd_layout.addWidget(self.label_cd_password)
        cd_layout.addWidget(self.CdPassword)
        self.clientDutLayout.addRow(cd_layout)


        # STA Demo LAN口外接PC时IP地址，iperf需要用到
        self.checkbox_sta_lan = QtWidgets.QCheckBox("STA LAN")
        self.checkbox_sta_lan.setChecked(True)
        self.checkbox_sta_lan.stateChanged.connect(lambda: self.toggle_lan_enabled(self.checkbox_sta_lan,self.ap_lan, self.ap_lan_username,self.ap_lan_password))
        self.label_sta_lan = QtWidgets.QLabel("IP")
        self.label_sta_lan.setFont(font)
        self.setup_label_properties(self.label_sta_lan)
        self.sta_lan = QtWidgets.QLineEdit()
        self.setup_text_properties(self.sta_lan)
        self.sta_lan.setText("192.168.1.201")
        self.label_sta_lan_username = QtWidgets.QLabel("Username")
        self.label_sta_lan_username.setFont(font)
        self.setup_label_properties(self.label_sta_lan_username)
        self.sta_lan_username = QtWidgets.QLineEdit()
        self.setup_text_properties(self.sta_lan_username)
        self.sta_lan_username.setText("nsb")
        self.label_sta_lan_password = QtWidgets.QLabel("Password")
        self.label_sta_lan_password.setFont(font)
        self.setup_label_properties(self.label_sta_lan_password)
        self.sta_lan_password = QtWidgets.QLineEdit()
        # self.sta_lan_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setup_text_properties(self.sta_lan_password)
        self.sta_lan_password.setText("Nokia#1234")
        sta_lan_layout = QtWidgets.QHBoxLayout()
        sta_lan_layout.addWidget(self.checkbox_sta_lan)
        sta_lan_layout.addWidget(self.label_sta_lan)
        sta_lan_layout.addWidget(self.sta_lan)
        sta_lan_layout.addWidget(self.label_sta_lan_username)
        sta_lan_layout.addWidget(self.sta_lan_username)
        sta_lan_layout.addWidget(self.label_sta_lan_password)
        sta_lan_layout.addWidget(self.sta_lan_password)
        self.clientDutLayout.addRow(sta_lan_layout)
        
        # 添加配置容器到布局
        self.staFormLayout.addRow("", self.wirelessCardConfig)
        self.staFormLayout.addRow("", self.clientDutConfig)
        
        # 默认显示第一个配置
        self.clientDutConfig.hide()
        
        # 设置STATION框架的尺寸策略和拉伸因子
        self.setup_groupbox_properties(self.STAframe, 0)  # STATION配置较多，给予更多空间
        
        # 添加STATION框架到滚动区域布局
        self.scrollLayout.addWidget(self.STAframe)
        
        # ===== IPERF配置框架 =====
        self.IPERFframe = QtWidgets.QGroupBox("IPERF")
        self.IPERFframe.setObjectName("IPERFframe")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.IPERFframe.setFont(font)

        # 设置iperf框架的背景色
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.IPERFframe.setPalette(palette)
        self.IPERFframe.setAutoFillBackground(True)
        
        # IPERF框架内部使用表单布局
        self.iperfFormLayout = QtWidgets.QFormLayout(self.IPERFframe)
        self.iperfFormLayout.setObjectName("iperfFormLayout")
        # 设置表单布局的字段增长策略为所有字段都增长
        self.iperfFormLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        # 设置标签对齐方式
        self.iperfFormLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
        # 设置行包装策略
        self.iperfFormLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        
        # Pair Number
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_pair = QtWidgets.QLabel("Pair Number")
        self.label_pair.setFont(font)
        self.setup_label_properties(self.label_pair)
        self.PairNumber = QtWidgets.QLineEdit()
        self.setup_text_properties(self.PairNumber)
        self.PairNumber.setText("4")
        # self.iperfFormLayout.addRow(self.label_pair, self.PairNumber)
        
        # Duration
        self.label_duration = QtWidgets.QLabel("Duration")
        self.label_duration.setFont(font)
        self.setup_label_properties(self.label_duration)
        self.Duration = QtWidgets.QLineEdit()
        self.setup_text_properties(self.Duration)
        self.Duration.setText("30")
        # self.iperfFormLayout.addRow(self.label_duration, self.Duration)
        iperf_base = QtWidgets.QHBoxLayout()
        iperf_base.addWidget(self.label_pair)
        iperf_base.addWidget(self.PairNumber)
        iperf_base.addWidget(self.label_duration)
        iperf_base.addWidget(self.Duration)
        self.iperfFormLayout.addRow(iperf_base)

        # Server script
        self.label_server_script = QtWidgets.QLabel("Server Script")
        self.label_server_script.setFont(font)
        self.setup_label_properties(self.label_server_script)
        self.server_script = QtWidgets.QLineEdit()
        self.setup_text_properties(self.server_script)
        self.server_script.setText("-s")
        # self.iperfFormLayout.addRow(self.label_server_script, self.server_script)

        # Client script
        self.label_client_script = QtWidgets.QLabel("Client Script")
        self.label_client_script.setFont(font)
        self.setup_label_properties(self.label_client_script)
        self.client_script = QtWidgets.QLineEdit()
        self.setup_text_properties(self.client_script)
        self.client_script.setText("-S 0x08")
        # self.iperfFormLayout.addRow(self.label_client_script, self.client_script)
        iperf_extra = QtWidgets.QHBoxLayout()
        iperf_extra.addWidget(self.label_server_script)
        iperf_extra.addWidget(self.server_script)
        iperf_extra.addWidget(self.label_client_script)
        iperf_extra.addWidget(self.client_script)
        self.iperfFormLayout.addRow(iperf_extra)
        
        
        # 设置IPERF框架的尺寸策略和拉伸因子
        self.setup_groupbox_properties(self.IPERFframe, 0)  # IPERF配置较少，给予较少空间
        
        # 添加IPERF框架到滚动区域布局
        self.scrollLayout.addWidget(self.IPERFframe)
        
        # ===== ATTENUATION配置框架 =====
        self.ATTframe = QtWidgets.QGroupBox("ATTENUATION")
        self.ATTframe.setObjectName("ATTframe")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ATTframe.setFont(font)

        # 设置ATTENUATION框架的背景色
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.ATTframe.setPalette(palette)
        self.ATTframe.setAutoFillBackground(True)
        
        # ATTENUATION框架内部使用网格布局
        self.attGridLayout = QtWidgets.QGridLayout(self.ATTframe)
        self.attGridLayout.setObjectName("attGridLayout")
        
        # Start, End, Step
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        
        self.label_att_start = QtWidgets.QLabel("Start")
        self.label_att_start.setFont(font)
        self.setup_label_properties(self.label_att_start)
        self.Start = QtWidgets.QLineEdit()
        self.setup_text_properties(self.Start)
        self.Start.setText("0")
        self.attGridLayout.addWidget(self.label_att_start, 0, 0)
        self.attGridLayout.addWidget(self.Start, 0, 1)
        
        self.label_att_end = QtWidgets.QLabel("End")
        self.label_att_end.setFont(font)
        self.setup_label_properties(self.label_att_end)
        self.End = QtWidgets.QLineEdit()
        self.setup_text_properties(self.End)
        self.End.setText("110")
        self.attGridLayout.addWidget(self.label_att_end, 0, 2)
        self.attGridLayout.addWidget(self.End, 0, 3)
        
        self.label_att_step = QtWidgets.QLabel("Step")
        self.label_att_step.setFont(font)
        self.setup_label_properties(self.label_att_step)
        self.Step = QtWidgets.QLineEdit()
        self.setup_text_properties(self.Step)
        self.Step.setText("3")
        self.attGridLayout.addWidget(self.label_att_step, 0, 4)
        self.attGridLayout.addWidget(self.Step, 0, 5)
        
        # Cable Loss
        self.label_cableloss = QtWidgets.QLabel("PathLoss")
        self.label_cableloss.setFont(font)
        self.setup_label_properties(self.label_cableloss)
        self.LineLoss = QtWidgets.QLineEdit()
        self.setup_text_properties(self.LineLoss)
        self.LineLoss.setText("0")
        self.attGridLayout.addWidget(self.label_cableloss, 1, 0, 1, 2)
        self.attGridLayout.addWidget(self.LineLoss, 1, 2, 1, 2)
        
        # Attenuator IP
        self.label_atten_ip = QtWidgets.QLabel("IP")
        self.label_atten_ip.setFont(font)
        self.setup_label_properties(self.label_atten_ip)
        self.AttenIP = QtWidgets.QLineEdit()
        self.setup_text_properties(self.AttenIP)
        self.AttenIP.setText("10.1.0.28")
        self.attGridLayout.addWidget(self.label_atten_ip, 1, 4, 1, 2)
        self.attGridLayout.addWidget(self.AttenIP, 1, 6, 1, 2)
        
        # 设置ATTENUATION框架的尺寸策略和拉伸因子
        self.setup_groupbox_properties(self.ATTframe, 0)  # ATTENUATION配置适中，给予中等空间
        
        # 添加ATTENUATION框架到滚动区域布局
        self.scrollLayout.addWidget(self.ATTframe)
        
        # ===== TURNTABLE配置框架 =====
        self.TTframe = QtWidgets.QGroupBox("TURNTABLE")
        self.TTframe.setObjectName("TTframe")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.TTframe.setFont(font)

        # 设置TT框架的背景色
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.TTframe.setPalette(palette)
        self.TTframe.setAutoFillBackground(True)
        
        # TURNTABLE框架内部使用表单布局
        self.turnFormLayout = QtWidgets.QFormLayout(self.TTframe)
        self.turnFormLayout.setObjectName("turnFormLayout")
        
        # Angles
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.Angle1 = QtWidgets.QLabel("Angles")
        self.Angle1.setFont(font)
        self.setup_label_properties(self.Angle1)
        self.angles_num = QtWidgets.QLineEdit()
        self.setup_text_properties(self.angles_num)
        self.angles_num.setText("1")
        # self.turnFormLayout.addRow(self.Angle1, self.angles_num)

        # IP
        self.label_turn_ip = QtWidgets.QLabel("IP")
        self.label_turn_ip.setFont(font)
        self.setup_label_properties(self.label_turn_ip)
        self.TurnIp = QtWidgets.QLineEdit()
        self.setup_text_properties(self.TurnIp)
        self.TurnIp.setText("10.1.0.18")
        # self.turnFormLayout.addRow(self.label_turn_ip, self.TurnIp)
        angle_layout = QtWidgets.QHBoxLayout()
        angle_layout.addWidget(self.Angle1)
        angle_layout.addWidget(self.angles_num)
        angle_layout.addWidget(self.label_turn_ip)
        angle_layout.addWidget(self.TurnIp)
        self.turnFormLayout.addRow(angle_layout)    
   
        
        # 设置TURNTABLE框架的尺寸策略和拉伸因子
        self.setup_groupbox_properties(self.TTframe, 0)  # TURNTABLE配置较少，给予较少空间
        
        # 添加TURNTABLE框架到滚动区域布局
        self.scrollLayout.addWidget(self.TTframe)
        
        # ===== TEST TYPE配置框架 =====
        self.TESTframe = QtWidgets.QGroupBox("TEST TYPE")
        self.TESTframe.setObjectName("TESTframe")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.TESTframe.setFont(font)
        
        # 设置TEST TYPE框架的背景色
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.TESTframe.setPalette(palette)
        self.TESTframe.setAutoFillBackground(True)

        # TEST TYPE框架内部使用水平布局
        self.testHLayout = QtWidgets.QHBoxLayout(self.TESTframe)
        self.testHLayout.setObjectName("testHLayout")
        
        # OTA/Conducted单选按钮, DL/UL 多选框
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.radioButton_ota = QtWidgets.QRadioButton("OTA")
        self.radioButton_ota.setFont(font)
        self.setup_radiobutton_properties(self.radioButton_ota)
        self.radioButton_ota.setChecked(True)
        self.radioButton_cdt = QtWidgets.QRadioButton("Conducted")
        self.radioButton_cdt.setFont(font)
        self.setup_radiobutton_properties(self.radioButton_cdt)
        self.testHLayout.addWidget(self.radioButton_ota)
        self.testHLayout.addWidget(self.radioButton_cdt)
        # self.testHLayout.addStretch(1)  # 添加弹性空间
        self.checkbox_dl = QtWidgets.QCheckBox("DL")
        self.checkbox_dl.setChecked(True)
        self.checkbox_ul = QtWidgets.QCheckBox("UL")
        self.checkbox_ul.setChecked(True)
        self.testHLayout.addWidget(self.checkbox_dl)
        self.testHLayout.addWidget(self.checkbox_ul)
        
        # 设置TEST TYPE框架的尺寸策略和拉伸因子
        self.setup_groupbox_properties(self.TESTframe, 0)  # TEST TYPE配置较少，给予较少空间
        
        # 添加TEST TYPE框架到滚动区域布局
        self.scrollLayout.addWidget(self.TESTframe)
        
        # ===== LOCAL PC ROLE配置框架 =====
        self.LOCALPCframe = QtWidgets.QGroupBox("LOCAL PC ROLE")
        self.LOCALPCframe.setObjectName("LOCALPCframe")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.LOCALPCframe.setFont(font)
        
        # 设置LOCAL PC ROLE框架的背景色
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.LOCALPCframe.setPalette(palette)
        self.LOCALPCframe.setAutoFillBackground(True)

        # LOCAL PC ROLE框架内部使用表单布局
        self.localPcFormLayout = QtWidgets.QFormLayout(self.LOCALPCframe)
        self.localPcFormLayout.setObjectName("localPcFormLayout")
        
        # 本地PC角色选择
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label_local_pc_role = QtWidgets.QLabel("程序运行PC选择")
        self.label_local_pc_role.setFont(font)
        self.setup_label_properties(self.label_local_pc_role)
        self.localPcRoleCombo = QtWidgets.QComboBox()
        self.setup_combobox_properties(self.localPcRoleCombo)
        self.localPcRoleCombo.addItem("Wireless Card-PC/Demo-LAN")
        self.localPcRoleCombo.addItem("AP-PC-LAN")
        self.localPcFormLayout.addRow(self.label_local_pc_role, self.localPcRoleCombo)
        
        # 添加说明标签
        self.label_local_pc_desc = QtWidgets.QLabel("注意: 需要选择程序运行的PC所属角色，会影响远程控制逻辑！")
        self.label_local_pc_desc.setFont(font)
        self.label_local_pc_desc.setWordWrap(True)  # 允许文本换行
        self.localPcFormLayout.addRow("", self.label_local_pc_desc)
        
        # 设置LOCAL PC ROLE框架的尺寸策略和拉伸因子
        self.setup_groupbox_properties(self.LOCALPCframe, 0)
        
        # 添加LOCAL PC ROLE框架到滚动区域布局
        self.scrollLayout.addWidget(self.LOCALPCframe)
        
        # 设置滚动区域的内容widget
        self.scrollArea.setWidget(self.scrollContent)
        
        # 将滚动区域添加到左侧布局
        self.leftLayout.addWidget(self.scrollArea)
        
        # 不再添加弹性空间，让控件按比例分布
        
        # 将左侧配置区添加到分割器
        self.splitter.addWidget(self.leftWidget)
        
        # ===== 右侧日志/结果面板 =====
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setObjectName("tabWidget")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        
        # 测试结果标签页
        self.resultTab = QtWidgets.QWidget()
        self.resultTab.setObjectName("resultTab")
        self.resultLayout = QtWidgets.QVBoxLayout(self.resultTab)
        self.resultLayout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        
        self.resultBrowser = QtWidgets.QTextBrowser()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.resultBrowser.setFont(font)
        self.resultBrowser.setObjectName("resultBrowser")
        self.resultLayout.addWidget(self.resultBrowser)
        
        # 添加按钮布局
        self.resultButtonLayout = QtWidgets.QHBoxLayout()
        self.resultButtonLayout.setContentsMargins(10, 5, 10, 5)
        
        # 添加保存结果按钮
        self.saveResultButton = QtWidgets.QPushButton("保存结果")
        self.saveResultButton.setObjectName("saveResultButton")
        self.saveResultButton.setMinimumHeight(30)
        self.saveResultButton.clicked.connect(self.save_results_to_file)
        self.resultButtonLayout.addWidget(self.saveResultButton)
        
        # 添加清除结果按钮
        self.clearResultButton = QtWidgets.QPushButton("清除结果")
        self.clearResultButton.setObjectName("clearResultButton")
        self.clearResultButton.setMinimumHeight(30)
        self.clearResultButton.clicked.connect(self.clear_results)
        self.resultButtonLayout.addWidget(self.clearResultButton)
        
        # 添加按钮布局到主布局
        self.resultLayout.addLayout(self.resultButtonLayout)
        
        self.tabWidget.addTab(self.resultTab, "Test Results")
        
        # 日志窗口标签页
        self.logTab = QtWidgets.QWidget()
        self.logTab.setObjectName("logTab")
        self.logLayout = QtWidgets.QVBoxLayout(self.logTab)
        self.logLayout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        
        self.logBrowser = QtWidgets.QTextBrowser()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.logBrowser.setFont(font)
        self.logBrowser.setObjectName("logBrowser")
        self.logLayout.addWidget(self.logBrowser)
        
        # 检查依赖项
        self.check_dependencies()
        
        self.tabWidget.addTab(self.logTab, "Log Window")
        
        # 确保第二个标签页（日志窗口）是启用的
        self.logTab.setEnabled(True)
        
        # 将标签页控件添加到分割器
        self.splitter.addWidget(self.tabWidget)
        
        # 设置分割器的初始大小比例
        # 使用固定值，因为此时MainWindow尚未完全初始化
        self.splitter.setSizes([300, 300])
        

        # 设置分割器的样式，使分隔线更容易看到和拖动
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #cccccc;
                border: 1px solid #999999;
                width: 4px;
                margin-top: 1px;
                margin-bottom: 1px;
            }
            QSplitter::handle:hover {
                background-color: #999999;
            }
        """)
        
        # 添加分割器到主布局
        self.mainLayout.addWidget(self.splitter)
        
        # ===== 底部按钮区域 =====
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        
        # 添加按钮
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        
        
        
        self.Start = QtWidgets.QPushButton("Start")
        self.Start.setFont(font)
        self.Start.setObjectName("Start")
        self.setup_button_properties(self.Start)
        self.buttonLayout.addWidget(self.Start)
        self.Stop = QtWidgets.QPushButton("Stop")
        self.Stop.setFont(font)
        self.Stop.setObjectName("Stop")
        self.setup_button_properties(self.Stop)
        self.buttonLayout.addWidget(self.Stop)
        
        
        
        # 添加弹性空间，使按钮靠左对齐
        self.buttonLayout.addStretch(1)
        
        # 添加按钮布局到主布局
        self.mainLayout.addLayout(self.buttonLayout)
        
        # 设置中央部件
        MainWindow.setCentralWidget(self.centralwidget)
        
        # 创建菜单栏
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        
        # 添加 Configuration 菜单
        self.menuConfig = QtWidgets.QMenu(self.menubar)
        self.menuConfig.setTitle("Configuration")
        self.menubar.addAction(self.menuConfig.menuAction())

        # 添加菜单项
        self.actionSaveConfig = QtWidgets.QAction(MainWindow)
        self.actionSaveConfig.setText("Save Configuration")
        self.menuConfig.addAction(self.actionSaveConfig)

        self.actionLoadConfig = QtWidgets.QAction(MainWindow)
        self.actionLoadConfig.setText("Load Configuration")
        self.menuConfig.addAction(self.actionLoadConfig)

        self.menuConfig.addSeparator()

        self.actionManageConfig = QtWidgets.QAction(MainWindow)
        self.actionManageConfig.setText("Manage Configurations")
        self.menuConfig.addAction(self.actionManageConfig)
        
        MainWindow.setMenuBar(self.menubar)
        
        # 创建状态栏
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # 设置标签页的当前索引
        self.tabWidget.setCurrentIndex(0)
        
        # 连接Station Type选择变化信号
        self.staTypeCombo.currentIndexChanged.connect(self.toggleStaConfig)
        
        # 连接本地PC角色选择变化信号
        self.localPcRoleCombo.currentIndexChanged.connect(self.updateLocalPcRoleUI)
        
        # 初始化UI状态
        self.updateLocalPcRoleUI()
        
        # 连接信号和槽
        
        # # 动态文本框布局（添加到原有布局之后）
        # self.dynamic_layout = QtWidgets.QVBoxLayout()
        # self.scrollContent.layout().addLayout(self.dynamic_layout)
        
        # # 添加初始的“增加”按钮
        # self.btn_add_textbox = QtWidgets.QPushButton("增加文本框", self.scrollContent)
        # self.btn_add_textbox.clicked.connect(self.add_dynamic_textbox)
        # self.scrollContent.layout().addWidget(self.btn_add_textbox)
        
        # # 确保动态布局不会覆盖原有内容
        # self.scrollContent.layout().setStretch(0, 1)
        # self.scrollContent.layout().setStretch(1, 0)
        
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # 设置窗口标题
        MainWindow.setWindowTitle("Wi-Fi Rate over Range Test")
        
        # 创建配置管理器
        self.config_manager = ConfigManager()

        # 连接菜单项的信号和槽
        self.actionSaveConfig.triggered.connect(self.save_config_dialog)
        self.actionLoadConfig.triggered.connect(self.load_config_dialog)
        self.actionManageConfig.triggered.connect(self.manage_configs)
        
        # 连接Run按钮的点击事件
        self.Start.clicked.connect(self.start_test)
        self.Stop.clicked.connect(self.stop_test)
    
    def check_status(self):
        """检查各个组件的连接状态"""
        # 确保日志记录器已初始化
        if not hasattr(self, 'logger'):
            self.setup_logger()
        
        self.log_message("开始检查各组件连接状态")
        
        # 获取当前配置
        config = {}
        
        # 获取本地PC角色
        local_pc_role = self.localPcRoleCombo.currentText()
        self.log_message(f"程序运行PC连接对象: {local_pc_role}")
        
        # AP配置
        is_local_ap = (local_pc_role == "AP")
        ap_config = {
            "connection_type": "ssh" if self.sshButton.isChecked() else "adb",
            "ip": self.ApIp.text(),
            "port": 22,  # 默认SSH端口
            "username": self.Username.text(),
            "password": self.Password.text(),
            "is_local": is_local_ap
        }
        config["ap"] = ap_config
        self.log_message(f"AP配置: 连接类型={ap_config['connection_type']}, IP={ap_config['ip']}, 本地设备={is_local_ap}")
        
        # STATION配置
        sta_type = self.staTypeCombo.currentText()
        is_local_wc_pc = (local_pc_role == "Wireless Card-PC" and sta_type == "Wireless Card-PC")
        is_local_client_dut = (local_pc_role == "Client-DUT" and sta_type == "Client-DUT")
        
        if sta_type == "Wireless Card-PC":
            sta_config = {
                "connection_type": "local" if is_local_wc_pc else "ssh",
                "ip": self.WcStaIp.text(),
                "port": 22,  # 默认SSH端口
                "username": "" if is_local_wc_pc else self.WcUsername.text(),
                "password": "" if is_local_wc_pc else self.WcPassword.text(),
                "is_local": is_local_wc_pc,
                "type": "Wireless Card-PC"  # 明确设置STATION类型
            }
            self.log_message(f"STATION配置: 类型=Wireless Card-PC, IP={sta_config['ip']}, 本地设备={is_local_wc_pc}")
            
            # 网卡PC配置 (与Wireless Card-PC相同)
            config["nic_pc"] = sta_config.copy()
            self.log_message(f"网卡PC配置: IP={sta_config['ip']}, 本地设备={is_local_wc_pc}")
            
            # 不包含Client-DUT配置
            config.pop("client", None)
        else:  # Client-DUT
            sta_config = {
                "connection_type": "ssh",
                "ip": self.CdStaIp.text(),
                "port": 22,  # 默认SSH端口
                "username": self.CdUsername.text(),
                "password": self.CdPassword.text(),
                "is_local": is_local_client_dut,
                "type": "Client-DUT"  # 明确设置STATION类型
            }
            self.log_message(f"STATION配置: 类型=Client-DUT, IP={sta_config['ip']}, 本地设备={is_local_client_dut}")
            
            # Client-DUT配置 (与STATION相同)
            config["client"] = sta_config.copy()
            self.log_message(f"Client-DUT配置: IP={sta_config['ip']}, 本地设备={is_local_client_dut}")
            
            # 不包含网卡PC配置
            config.pop("nic_pc", None)
        
        config["station"] = sta_config
        
        # 衰减器配置
        att_config = {
            "ip": self.AttenIP.text(),
            "username": "",  # 如果需要登录凭据，可以添加相应的UI元素
            "password": ""
        }
        config["attenuator"] = att_config
        self.log_message(f"衰减器配置: IP={att_config['ip']}")
        
        # 转台配置
        turntable_config = {
            "ip": self.TurnIp.text(),
            "username": "",  # 如果需要登录凭据，可以添加相应的UI元素
            "password": ""
        }
        config["turntable"] = turntable_config
        self.log_message(f"转台配置: IP={turntable_config['ip']}")
        
        # 创建状态检查对象
        checker = StatusCheck()
        
        # 显示状态检查进度对话框
        # 根据选择的STATION类型确定总步骤数
        total_steps = 5  # AP, STATION, 根据STATION类型的一个设备, 衰减器, 转台
        progress_dialog = QtWidgets.QProgressDialog("正在检查连接状态...", "取消", 0, total_steps, self.MainWindow)
        progress_dialog.setWindowTitle("状态检查")
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.show()
        
        # 检查所有组件的连接状态
        try:
            # 检查AP连接
            progress_dialog.setLabelText("正在检查AP连接...")
            progress_dialog.setValue(1)
            QtWidgets.QApplication.processEvents()
            self.log_message("正在检查AP连接...")
            
            # 检查STATION连接
            progress_dialog.setLabelText("正在检查STATION连接...")
            progress_dialog.setValue(2)
            QtWidgets.QApplication.processEvents()
            self.log_message("正在检查STATION连接...")
            
            # 根据选择的STATION类型检查相应的连接
            if sta_type == "Wireless Card-PC":
                # 检查网卡PC连接
                progress_dialog.setLabelText("正在检查网卡PC连接...")
                progress_dialog.setValue(3)
                QtWidgets.QApplication.processEvents()
                self.log_message("正在检查网卡PC连接...")
            elif sta_type == "Client-DUT":
                # 检查Client-DUT连接
                progress_dialog.setLabelText("正在检查Client-DUT连接...")
                progress_dialog.setValue(3)
                QtWidgets.QApplication.processEvents()
                self.log_message("正在检查Client-DUT连接...")
            
            # 检查衰减器连接
            progress_dialog.setLabelText("正在检查衰减器连接...")
            progress_dialog.setValue(5)
            QtWidgets.QApplication.processEvents()
            self.log_message("正在检查衰减器连接...")
            
            # 检查转台连接
            progress_dialog.setLabelText("正在检查转台连接...")
            progress_dialog.setValue(6)
            QtWidgets.QApplication.processEvents()
            self.log_message("正在检查转台连接...")
            
            # 执行实际的状态检查
            status = checker.check_all_status(config)
            self.log_message("状态检查完成")
            
            # 根据本地PC角色，更新UI上的连接设置可用性
            local_pc_role = self.localPcRoleCombo.currentText()            
            
            # # 如果是本地Wireless Card-PC，禁用相关连接设置，这个功能不需要，因为需要IP地址配合打流
            # is_local_wc_pc = (local_pc_role == "Wireless Card-PC")
            # self.WcStaIp.setEnabled(not is_local_wc_pc)
            # self.WcUsername.setEnabled(not is_local_wc_pc)
            # self.WcPassword.setEnabled(not is_local_wc_pc)
            
        except Exception as e:
            # 关闭进度对话框
            progress_dialog.close()
            
            # 记录错误日志
            error_message = f"检查连接状态时发生错误：{str(e)}"
            self.log_message(error_message, logging.ERROR)
            
            # 显示错误消息
            QtWidgets.QMessageBox.critical(
                self.MainWindow,
                "状态检查错误",
                error_message
            )
            return False
        finally:
            # 确保关闭所有连接
            checker.close_all_connections()
        
        # 关闭进度对话框
        progress_dialog.close()
        
        # 显示状态检查结果
        status_message = "连接状态检查结果"
        all_ready = True
        
        # 记录状态检查结果到日志
        self.log_message("连接状态检查结果")
        
        # 获取当前选择的STATION类型
        sta_type = self.staTypeCombo.currentText()
        
        # 定义组件显示名称映射
        component_display_names = {
            "ap": "AP",
            "station": "STATION",
            "nic_pc": "网卡PC",
            "client": "Client-DUT",
            "attenuator": "衰减器",
            "turntable": "转台"
        }
        
        # 根据STATION类型确定需要显示的组件
        components_to_show = ["ap", "station", "attenuator", "turntable"]
        if sta_type == "Wireless Card-PC":
            components_to_show.append("nic_pc")
        elif sta_type == "Client-DUT":
            components_to_show.append("client")
        
        self.log_message(f"当前STATION类型: {sta_type}，将显示以下组件状态: {', '.join(components_to_show)}")
        
        for component, is_connected in status.items():
            # 只显示与当前STATION类型相关的组件
            if component not in components_to_show:
                self.log_message(f"跳过显示组件 {component} 的状态，因为与当前STATION类型无关", logging.DEBUG)
                continue
                
            # 获取组件的显示名称
            display_name = component_display_names.get(component, component)
            
            status_text = "已就绪" if is_connected else "未就绪"
            status_message += f"\n{display_name}: {status_text}"
            
            # 记录每个组件的状态到日志
            log_level = logging.INFO if is_connected else logging.WARNING
            self.log_message(f"{display_name}: {status_text}", log_level)
            
            if not is_connected:
                all_ready = False
        
        # 显示状态检查结果对话框
        msg_box = QtWidgets.QMessageBox(self.MainWindow)
        msg_box.setWindowTitle("状态检查结果")
        msg_box.setText(status_message)
        
        if all_ready:
            msg_box.setIcon(QtWidgets.QMessageBox.Information)
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            result = msg_box.exec_()
            self.log_message("所有组件已就绪，可以开始测试")
            return True
        else:
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setInformativeText("有组件未就绪，是否继续测试？")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            result = msg_box.exec_()
            if result == QtWidgets.QMessageBox.Yes:
                self.log_message("用户选择继续测试，尽管有组件未就绪", logging.WARNING)
                return True
            else:
                self.log_message("用户选择取消测试，因为有组件未就绪", logging.WARNING)
                return False
    
    def setup_logger(self):
        """设置日志记录器"""
        # 确保log文件夹存在
        if not os.path.exists("log"):
            os.makedirs("log")
        
        # 创建日志文件名，使用当前日期和时间
        log_filename = os.path.join("log", f"rvr_test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        # 配置日志记录器
        self.logger = logging.getLogger("RVR_GUI")
        self.logger.setLevel(logging.INFO)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        self.logger.addHandler(file_handler)
        
        # 记录初始日志
        self.logger.info("日志记录器初始化完成")
        if hasattr(self, 'logBrowser'):
            self.logBrowser.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 日志记录器初始化完成")
            self.logBrowser.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 日志文件: {log_filename}")
    
    def log_message(self, message, level=logging.INFO):
        """记录日志消息"""
        # 确保日志记录器已初始化
        if not hasattr(self, 'logger'):
            self.setup_logger()
        
        # 记录到日志文件
        self.logger.log(level, message)
        
        # 显示在日志窗口
        log_level_prefix = ""
        if level == logging.WARNING:
            log_level_prefix = "[警告] "
        elif level == logging.ERROR:
            log_level_prefix = "[错误] "
        elif level == logging.CRITICAL:
            log_level_prefix = "[严重] "
        
        if hasattr(self, 'logBrowser'):
            self.logBrowser.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {log_level_prefix}{message}")
    
    def start_test(self):
        """Start the test and update button text to Running"""
        self.Start.setText("Running")
        # Original test logic goes here
        self.run_test()

    def stop_test(self):
        """Stop the test and reset button text to Start"""
        self.Start.setText("Start")
        # Add stop logic here

    def run_test(self):
        """运行测试"""
        # 导入所需模块
        import time
        from att import Attenuate
        from turntable import Turntable
        
        # 确保日志记录器已初始化
        if not hasattr(self, 'logger'):
            self.setup_logger()
            
        # 检查各个组件的连接状态
        if not self.check_status():
            self.log_message("测试取消：状态检查未通过", logging.WARNING)
            return
        
        # 记录测试开始日志
        self.log_message("测试开始")
        
        # 获取测试配置
        try:
            # OTA or Conducted
            from switch import Switch
            swt_ip= self.TurnIp.text()            
            if self.radioButton_ota.isChecked():
                self.log_message("测试模式：OTA")
                swt = Switch(swt_ip, test_type="OTA", max_retries=3)
                swt.set_switch_runtype()
            elif self.radioButton_cdt.isChecked():
                self.log_message("测试模式: Conducted")
                swt = Switch(swt_ip, test_type="CDT", max_retries=3)
                swt.set_switch_runtype()
            
            # 查询程序运行PC角色
            current_pc_role = self.localPcRoleCombo.currentText()
            if current_pc_role == "Wireless Card-PC/Demo-PC":
                self.log_message("程序运行在无线网卡PC或连接Demo LAN口的PC上")
            elif current_pc_role == "AP-PC":
                self.log_message("程序运行在连接AP LAN口的PC上")

            # 查询AP打流设置，即AP端 iperf将运行在哪里
            selected_ap_lans = []
            selected_ap_lansip = []
            selected_ap_lansuser = []
            selected_ap_lanspwd = []
            if self.checkbox_ap_lan.isChecked():
                selected_ap_lans.append("LAN1")
                selected_ap_lansip.append(self.ap_lan.setText())
                selected_ap_lansuser.append(self.ap_lan_user.setText())
                selected_ap_lanspwd.append(self.ap_lan_pwd.setText())  
            if self.checkbox_ap_lan2.isChecked():
                selected_ap_lans.append("LAN2")
                selected_ap_lansip.append(self.ap_lan2.setText())
                selected_ap_lansuser.append(self.ap_lan2_user.setText())
                selected_ap_lanspwd.append(self.ap_lan2_pwd.setText())    
            if self.checkbox_ap_lan3.isChecked():
                selected_ap_lans.append("LAN3")
                selected_ap_lansip.append(self.ap_lan3.setText())
                selected_ap_lansuser.append(self.ap_lan3_user.setText())
                selected_ap_lanspwd.append(self.ap_lan3_pwd.setText())
            if self.checkbox_ap_lan4.isChecked():
                selected_ap_lans.append("LAN4")
                selected_ap_lansip.append(self.ap_lan4.setText())
                selected_ap_lansuser.append(self.ap_lan4_user.setText())
                selected_ap_lanspwd.append(self.ap_lan4_pwd.setText())              
            self.log_message(f"选择了 {len(selected_ap_lans)} 个：{', '.join(selected_ap_lans)}")
            ap_ex_mode = True
            if selected_ap_lans == None:
                ap_ip = self.ApIp.setText()
                ap_ex_mode = False

            # 查询STA打流设置，即STA端 iperf将运行在哪里
            sta_type = self.staTypeCombo.currentText()
            if sta_type == "Wireless Card-PC":
                self.log_message("STA是无线网卡")
                sta_ip = self.WcStaIp.setText()
            elif sta_type == "Client-DUT":
                self.log_message("STA是DUT或DEMO")
                if self.sta_lan.isChecked():
                    sta_ip = self.sta_lan_ip.setText()
                    sta_ex_mode = True
                else:
                    sta_ip = self.CdStaIp.setText()
                    sta_ex_mode = False

            # 获取衰减器配置
            start_att = float(self.Start.text())
            end_att = float(self.End.text())
            step_att = float(self.Step.text())
            
            # 获取角度配置
            angles_num = int(self.angles_num.text())
            
            # 记录测试参数
            self.log_message(f"衰减配置: 起始值={start_att}dB, 结束值={end_att}dB, 步进值={step_att}dB")
            self.log_message(f"角度配置: 测试角度数量={angles_num}")
            
            # 确认测试参数
            confirm_msg = (f"将执行以下测试:\n\n"
                          f"衰减范围: {start_att}dB 到 {end_att}dB, 步进值: {step_att}dB\n"
                          f"每个衰减值测试 {angles_num} 个角度\n\n"
                          f"总测试点数: {int((end_att - start_att) / step_att + 1) * angles_num}\n\n"
                          f"是否继续?")
            
            reply = QtWidgets.QMessageBox.question(
                self.MainWindow,
                "确认测试参数",
                confirm_msg,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.No:
                self.log_message("用户取消测试", logging.INFO)
                return
            
            # 创建进度对话框
            total_steps = int((end_att - start_att) / step_att + 1) * angles_num
            progress_dialog = QtWidgets.QProgressDialog("测试进行中...", "取消", 0, total_steps, self.MainWindow)
            progress_dialog.setWindowTitle("测试进度")
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.show()
            
            # 初始化测试结果
            self.resultBrowser.clear()
            self.resultBrowser.append("===== 测试结果 =====\n")
            self.resultBrowser.append(f"开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # 添加测试参数信息
            self.resultBrowser.append("--- 测试参数 ---")
            self.resultBrowser.append(f"测试类型: {self._get_test_type()}")
            
            # 添加衰减器和转台参数
            self.resultBrowser.append(f"\n衰减范围: {start_att}dB 到 {end_att}dB, 步进值: {step_att}dB")
            self.resultBrowser.append(f"每个衰减值测试 {angles_num} 个角度\n")

            # 添加 iperf3 测试参数 
            self.resultBrowser.append("iperf3 参数")
            # self.resultBrowser.append(f"  测试模式: {self.TestMode.currentText()}") # 默认TCP
            self.resultBrowser.append(f"  测试时长: {self.Duration.text()} 秒")
            self.resultBrowser.append(f"  流数: {self.PairNumber.text()}")
            self.resultBrowser.append(f"  服务端参数: {self.server_script.text()}")
            self.resultBrowser.append(f"  客户端参数: {self.client_script.text()}")
            
            # 执行测试循环
            current_step = 0
            
            # 循环衰减值
            current_att = start_att
            while current_att <= end_att:
                self.log_message(f"设置衰减值: {current_att}dB")
                self.resultBrowser.append(f"\n--- 衰减值: {current_att}dB ---")
                
                # 设置衰减器的衰减值
                try:
                    from att import Attenuate
                    att_ip = self.AttenIP.text()
                    att_controller = Attenuate(att_ip)
                    self.log_message(f"连接衰减器: {att_ip}")
                    att_controller.set_att(current_att)
                    self.log_message(f"衰减器设置成功: {current_att}dB")
                except Exception as e:
                    error_msg = f"衰减器设置失败: {str(e)}"
                    self.log_message(error_msg, logging.ERROR)
                    raise Exception(error_msg)
                
                # 循环测试角度
                angle_step = 360 / angles_num
                for i in range(angles_num):
                    # 计算当前角度
                    current_angle = i * angle_step
                    self.log_message(f"设置角度: {current_angle}°")
                    self.resultBrowser.append(f"\n角度: {current_angle}°")
                    
                    # 设置转台的角度
                    # 类初始化时加一个状态标志
                    self.turntable_available = True  # 假设默认能连接

                    # 设置转台角度逻辑
                    if self.turntable_available:
                        try:
                            from turntable import Turntable
                            turntable_ip = self.TurnIp.text()
                            turntable_controller = Turntable(turntable_ip)
                            self.log_message(f"连接转台: {turntable_ip}")
                            turntable_controller.set_angle(current_angle)
                            self.log_message(f"转台角度设置成功: {current_angle}°")
                            time.sleep(5)  # 等待转台旋转到位
                        except Exception as e:
                            error_msg = f"转台连接或角度设置失败，将继续当前角度测试: {str(e)}"
                            self.log_message(error_msg, logging.WARNING)
                            self.turntable_available = False  # 标记后续不再尝试连接转台

                    
                    # 更新进度对话框
                    progress_dialog.setValue(current_step)
                    progress_dialog.setLabelText(f"测试中: 衰减={current_att}dB, 角度={current_angle}°")
                    QtWidgets.QApplication.processEvents()
                    
                    # 检查是否取消
                    if progress_dialog.wasCanceled():
                        self.log_message("用户取消测试", logging.WARNING)
                        self.resultBrowser.append("\n测试被用户取消")
                        progress_dialog.close()
                        return
                    
                    # 执行实际的iperf3测试，这里需要完善DL/UL测试参数配置，需要根据当前运行程序的PC角色来决定DL/UL测试参数设置
                    try:
                        from iperf import server_run, iperf3_client, iperf3_client_localDL, iperf3_client_localUL
                        if current_pc_role == "Wireless Card-PC/Demo-PC":
                            # 程序运行在无线网卡电脑或者连接Demo的电脑上，此时PC上执行客户端
                            if ap_ex_mode == False:
                                # 使用AP内置iperf，开启iperf server
                                server_run(ap_ip, self.Username.text(), self.Password.text(), '5201') #在AP上开启iperf server
                                if sta_type == "Wireless Card-PC":
                                    # STA为无线网卡，无线网卡的PC本地执行iperf client
                                    # 运行iperf3 client，传入ap_ip, sta_ip,
                                    if self.checkbox_dl.isChecked():
                                        iperf3_client_localDL(ap_ip,sta_ip,'5201', current_att, current_angle)
                                    if self.checkbox_ul.isChecked():
                                        iperf3_client_localUL(ap_ip,sta_ip,'5201', current_att, current_angle)                        
                                elif sta_type == "Client-DUT":
                                    # STA为Demo
                                    if sta_ex_mode == True:
                                        # 外置，此时iperf client从PC上执行，目前只设计了一个LAN口, 需要ssh登录到LAN口连接的PC去执行iperf client
                                        client_run = iperf3_client(sta_ip, self.sta_lan_username.setText(), self.sta_lan_password.setText())
                                    else:
                                        # 内置,此时在Demo上执行iperf client 
                                        client_run = iperf3_client(sta_ip, self.CdUsername.setText(), self.CdPassword.setText())
                                    # 测试DL/UL
                                    if self.checkbox_dl.isChecked():
                                        client_run.iper_DL(ap_ip, sta_ip, '5201', current_att, current_angle)
                                    if self.checkbox_ul.isChecked():
                                        client_run.iper_UL(ap_ip, sta_ip, '5201', current_att, current_angle)
                            elif ap_ex_mode == True:
                                # AP 通过LAN口连接外部PC， 在外部PC上执行iperf server
                                # 均使用ssh远程登录PC
                                # 根据选择的LAN口远程开启iperf server
                                base_port = 5201
                                for i, lan_ip in enumerate(selected_ap_lansip):
                                    port = base_port + i
                                    server_run(lan_ip, selected_ap_lansuser[i], selected_ap_lanspwd[i], port)
                                if sta_type == "Client-DUT":
                                    # 客户端为Demo
                                    if sta_ex_mode == False:
                                        # 内置，客户端为DEMO，Demo上执行iperf client
                                        client_run = iperf3_client(sta_ip, self.CdUsername.setText(), self.CdPassword.setText())
                                        base_port = 5201
                                        # 测试DL/UL
                                        for i, lan_ip in enumerate(selected_ap_lansip):
                                            port = base_port + i
                                            if self.checkbox_dl.isChecked():
                                                client_run.iper_DL(lan_ip, sta_ip, port, current_att, current_angle)
                                            if self.checkbox_ul.isChecked():
                                                client_run.iper_UL(lan_ip, sta_ip, port, current_att, current_angle)
                                    else:
                                        # 外置，使用和Demo LAN口相连的PC以太网口，目前只设计了一个LAN口
                                        # 当前PC上运行程序，本地执行iperf client
                                        base_port = 5201
                                        for i, lan_ip in enumerate(selected_ap_lansip):
                                            port = base_port + i
                                            if self.checkbox_dl.isChecked():
                                                iperf3_client_localDL(lan_ip, sta_ip, port, current_att, current_angle)
                                            if self.checkbox_ul.isChecked():
                                                iperf3_client_localUL(lan_ip, sta_ip, port, current_att, current_angle)     
                        elif current_pc_role == "AP-PC":
                            # 程序运行在和AP LAN口相连的PC上
                            # server端均需远程
                            if ap_ex_mode == False:
                                # AP内置，使用AP内置iperf执行iperf client
                                if sta_type == "Wireless Card-PC":
                                    # 无线网卡
                                    server_run(sta_ip, self.WcUsername.setText(), self.WcPassword.setText(), '5201') #在STA上开启iperf server                             
                                elif sta_type == "Client-DUT":
                                    # Demo 
                                    if sta_ex_mode == False:
                                        # 内置
                                        server_run(sta_ip, self.CdUsername.setText(), self.CdPassword.setText(), '5201') #在STA上开启iperf server
                                    else:
                                        # 外置，需要ssh远程登录到PC上执行iperf server，此时只考虑一个LAN口，根据选择的LAN口执行iperf server
                                        server_run(sta_ip, self.sta_lan_username.setText(), self.sta_lan_password.setText(), '5201')
                                    #登录到AP 执行iperf client
                                    client_run = iperf3_client(ap_ip, self.Username.setText(), self.Password.setText()) 
                                    if self.checkbox_dl.isChecked():
                                        client_run.iper_UL(sta_ip, ap_ip,'5201', current_att, current_angle) # DL反向，使用UL指令
                                    if self.checkbox_ul.isChecked():
                                        iperf3_client_localDL(sta_ip, ap_ip,'5201', current_att, current_angle) # UL反向，使用DL指令 
                            elif ap_ex_mode == True:
                                # AP 接LAN口，此时需要分程序运行在哪个LAN口上来判断远程还是本地运行iperf client
                                base_port = 5201
                                lan_ip, lan_username, lan_password = [], [], []
                                for i, lan_ip in enumerate(selected_ap_lansip):
                                    lan_username.append(selected_ap_lansuser[i])
                                    lan_password.append(selected_ap_lanspwd[i])
                                    port = base_port + i
                                    if sta_type == "Wireless Card-PC":
                                        # 无线网卡，外置，远程执行iperf server
                                        server_run(sta_ip, self.WcUsername.setText(), self.WcPassword.setText(), port) #根据AP外接的LAN口配置，在无线网卡PC上开启对应的iperf server 
                                    elif sta_type == "Client-DUT":
                                        # Demo
                                        if sta_ex_mode == False:
                                            # 内置
                                            server_run(sta_ip, self.CdUsername.setText(), self.CdPassword.setText(), port) #在Demo内部开启对应的iperf server 
                                        else:
                                            # 外置，需要ssh远程登录到PC上执行iperf server
                                            server_run(sta_ip, self.sta_lan_username.setText(), self.sta_lan_password.setText(), port)#在STA上开启iperf server
                                    # 根据选择的LAN口远程运行 iperf client


                    except Exception as e:
                        error_msg = f"iperf测试失败: {str(e)}"
                        self.log_message(error_msg, logging.ERROR)
                        raise Exception(error_msg)
                    
                    # 等待一段时间，确保测试完成
                    QtWidgets.QApplication.processEvents()
                    # time.sleep(1)  # 实际测试中可能需要更长时间
                    
                    current_step += 1
                
                # 增加衰减值
                current_att += step_att
            
            # 关闭进度对话框
            progress_dialog.close()
            
            # 重置设备状态
            try:
                # 重置衰减器到默认状态
                self.log_message("重置衰减器到默认状态")
                att_controller = Attenuate(self.AttenIP.text())
                att_controller.set_default()
                att_controller.close()
                
                # 重置转台到默认位置
                self.log_message("重置转台到默认位置")
                turntable_controller = Turntable(self.TurnIp.text())
                turntable_controller.set_default()
                turntable_controller.close()
            except Exception as e:
                self.log_message(f"重置设备状态时出错: {str(e)}", logging.WARNING)
            
            # 记录测试完成
            end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.log_message(f"测试完成，结束时间: {end_time}")
            self.resultBrowser.append(f"\n测试完成")
            self.resultBrowser.append(f"结束时间: {end_time}")
            
            # 显示测试完成消息
            QtWidgets.QMessageBox.information(
                self.MainWindow,
                "测试完成",
                f"测试已完成，共测试了 {current_step} 个测试点。\n\n结果已显示在测试结果标签页中。"
            )
            
        except ValueError as e:
            # 处理输入参数错误
            error_msg = f"参数错误: {str(e)}"
            self.log_message(error_msg, logging.ERROR)
            QtWidgets.QMessageBox.critical(
                self.MainWindow,
                "参数错误",
                error_msg
            )
        except Exception as e:
            # 处理其他错误
            error_msg = f"测试过程中发生错误: {str(e)}"
            self.log_message(error_msg, logging.ERROR)
            QtWidgets.QMessageBox.critical(
                self.MainWindow,
                "测试错误",
                error_msg
            )


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    # 获取屏幕尺寸
    screen = app.desktop().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
    
    # 计算窗口大小为屏幕大小的75%
    window_width = int(screen_width * 0.75)
    window_height = int(screen_height * 0.75)
    
    MainWindow = QtWidgets.QMainWindow()
    
    # 重写关闭事件
    def closeEvent(event):
        # 保存当前配置
        ui.save_last_config()
        event.accept()
    
    MainWindow.closeEvent = closeEvent
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    # 设置窗口大小
    MainWindow.resize(window_width, window_height)
    
    # 居中显示窗口
    MainWindow.move((screen_width - window_width) // 2, (screen_height - window_height) // 2)
    
    MainWindow.show()
    sys.exit(app.exec_())