# -*- coding: utf-8 -*-

# FLOAT；单位：秒
# 每次查询Machine时等待响应的最长时间
MACHINES_QUERY_WAIT_TIME = 1.0

# FLOAT；单位：秒
# 每次查询Machine失败重试次数
MACHINES_QUERY_ATTEMPT_COUNT = 1

# MACHINES地址配置
# 当此参数不为空时，则由原来的广播探测改为固定地址探测，
# WebConsole仅会以此配置的地址进行探测，
# 当服务器存在跨网段的情况时，此方案犹为有用。
# 例子：
# MACHINES_ADDRESS = ["10.11.131.154", "10.11.131.155", "10.11.131.156"]
MACHINES_ADDRESS = ["127.0.0.1"]