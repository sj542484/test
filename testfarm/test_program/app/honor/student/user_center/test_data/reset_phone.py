
reset_phone_data = (
    {'reset': '182111', 'password': '456789', 'toast': ''},  # 无错误提示信息
    {'reset': '18711111134', 'password': '456789', 'toast': '用户已存在'},
    {'reset': '10764552343', 'password': '456789', 'toast': ''},
    {'reset': '18711111234', 'password': '456789', 'toast':  '手机号码不能与原号码相同'},
    {'reset': '11111111111', 'password': '456789', 'toast': '手机号 格式不正确'},
    {'reset': '18211111003', 'password': '456789'},  # 未注册手机号
    {'reset': '18711111234', 'password': '456789'},  # 恢复测试数据
)

# 验证码验证失败
reset_again_data = (
    {'reset': '18211111003', 'password': '456789'},  # 未注册手机号
    {'reset': '18711111234', 'password': '456789'},  # 恢复测试数据
)
