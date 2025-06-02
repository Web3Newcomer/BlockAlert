# 比特币区块监控提醒

这是一个用于监控比特币区块高度并发送提醒的Python脚本。当区块高度达到指定目标时，会通过企业微信发送提醒消息。

## 功能特点

- 监控指定区块高度
- 支持多个目标区块高度
- 支持提前提醒（当区块高度接近目标时）
- 通过企业微信发送提醒消息
- 显示详细的区块信息

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

在 `config.py` 文件中配置以下参数：

1. 企业微信配置（WECOM_CONFIG）：
   - webhook_url：企业微信机器人的webhook地址

2. 区块监控配置（BLOCK_CONFIG）：
   - target_heights：目标区块高度列表
   - check_interval：检查间隔（秒）
   - early_alert_diff：提前提醒的区块数

## 使用方法

1. 配置 `config.py` 文件
2. 运行脚本：
```bash
python block_alert.py
```

## 提醒内容

提醒消息包含以下信息：
- 当前时间
- 当前区块高度
- 目标区块高度
- 剩余区块数
- 预计到达时间

## 注意事项

- 请确保网络连接正常
- 建议使用Python 3.6或更高版本
- 请妥善保管企业微信webhook地址 