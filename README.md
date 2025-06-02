# 比特币区块监控提醒工具

这是一个用于监控比特币区块高度并在特定区块到达时发送提醒的工具。当目标区块的前三个区块到达时，会通过企业微信发送提醒消息。

## 功能特点

- 监控指定的比特币区块高度
- 在目标区块的前三个区块到达时发送提醒
- 通过企业微信发送提醒消息
- 显示当前区块高度、目标区块高度、剩余区块数和预计到达时间
- 支持自定义检查间隔时间

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/felixfung/clock.git
cd clock
```

2. 安装依赖：
```bash
# 使用 pip 安装依赖
pip3 install -r requirements.txt

# 或者直接安装 requests
pip3 install requests==2.31.0
```

3. 配置企业微信：
   - 在 `config.py` 文件中设置您的企业微信 webhook 地址
   - 修改 `early_alert_diff` 参数可以调整提前提醒的区块数量
   - 修改 `check_interval` 参数可以调整检查间隔时间（秒）

## 使用方法

运行脚本时，需要指定目标区块高度：

```bash
python3 block_alert.py <目标区块高度>
```

例如，要监控区块 899480：
```bash
python3 block_alert.py 899480
```

脚本会：
1. 监控指定的目标区块高度
2. 在目标区块的前三个区块到达时发送提醒
3. 显示当前区块高度和预计到达时间
4. 当目标区块到达时自动结束监控

## 提醒消息内容

提醒消息包含以下信息：
- 当前时间
- 当前区块高度
- 目标区块高度
- 剩余区块数
- 预计到达时间

## 注意事项

- 确保网络连接正常
- 企业微信 webhook 地址必须正确配置
- 目标区块高度必须是有效的数字
- 按 Ctrl+C 可以随时停止监控

## 配置说明

在 `config.py` 文件中可以修改以下配置：

```python
# 企业微信配置
WECOM_CONFIG = {
    'webhook_url': 'YOUR_WEBHOOK_URL',  # 替换为您的webhook地址
}

# 区块监控配置
BLOCK_CONFIG = {
    'check_interval': 60,  # 检查间隔（秒）
    'early_alert_diff': 3,  # 提前多少个区块发出提醒
}
```

## 依赖说明

项目依赖：
- Python 3.6+
- requests==2.31.0

## 许可证

MIT License
