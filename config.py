# 邮件配置
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # 替换为您的SMTP服务器
    'smtp_port': 465,                 # 替换为您的SMTP端口
    'username': 'your-email@gmail.com',  # 替换为您的邮箱
    'password': 'your-app-password',     # 替换为您的邮箱密码或应用专用密码
    'from_email': 'your-email@gmail.com',  # 替换为您的邮箱
    'to_email': 'recipient@example.com'    # 替换为接收通知的邮箱
}

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
    'notify_first_n_blocks': 1,  # 通知前N个区块
    'early_alert_diff': 3,  # 提前多少个区块发出提醒
    'early_alert_sent': False  # 是否已发送提前提醒
} 