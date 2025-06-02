# 企业微信配置
WECOM_CONFIG = {
    'webhook_url': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d0a09574-50c3-4067-957a-fbdb13125870',  # 替换为您的webhook地址
}

# 区块监控配置
BLOCK_CONFIG = {
    'target_heights': [
        899573,  # 目标区块
    ],
    'check_interval': 60,  # 检查间隔（秒）
    'early_alert_diff': 3,  # 提前多少个区块发出提醒
} 