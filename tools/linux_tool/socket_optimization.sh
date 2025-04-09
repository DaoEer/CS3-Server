#!/bin/bash

# set ulimit
limit()
{
echo "ulimit -SHn 102400" >>/etc/rc.local
cat >> /etc/security/limits.conf << EOF
*           soft   nofile       102400
*           hard   nofile       102400
EOF
}

# set sysctl
sysctl()
{
cp /etc/sysctl.conf /etc/sysctl.conf-$(date +%F).bak
true > /etc/sysctl.conf
cat >> /etc/sysctl.conf << EOF
#关闭ipv4转发
net.ipv4.ip_forward = 0

#开启严格的反向路径校验，需谨慎配置。0为关闭，2为松散
net.ipv4.conf.all.rp_filter = 0
net.ipv4.conf.default.rp_filter = 1

#处理无源路由的包
net.ipv4.conf.default.accept_source_route = 0

#禁用SysRq的全部功能
kernel.sysrq = 0

#控制内核的系统请求调试功能开启，控制核心转储附加PID到核心文件名，适用于多线程
kernel.core_uses_pid = 1

#开启SYN洪水攻击保护
net.ipv4.tcp_syncookies = 1

#内核消息/内存管理设置
#每个消息队列的最大字节限制
kernel.msgmnb = 65536

#每个消息的最大值
kernel.msgmax = 65536

#共享内存段的最大值，应设置为大于本机实际内存。
kernel.shmmax = 68719476736

#系统一次可以使用的共享内存总量（以页为单位）
kernel.shmall = 4294967296

#表示系统同时保持TIME_WAIT套接字的最大数量
net.ipv4.tcp_max_tw_buckets = 262144

#启用有选择的应答，（对于广域网通信来说）这个选项应该启用，但是会增加对CPU的占用。
net.ipv4.tcp_sack = 1

#启用RFC 1323定义的window scaling，要支持超过64KB的TCP窗口，必须启用该值
net.ipv4.tcp_window_scaling = 1

#增加TCP最大缓冲区大小
#为自动调优定义socket使用的内存。第一个值是为socket接收缓冲区分配的最少字节数；第二个值是默认值（该值会被rmem_default覆盖），缓冲区在系统负载不重的情况下可以增长到这个值；第三个值是接收缓冲区空间的最大字节数（该值会被rmem_max覆盖）。
net.ipv4.tcp_rmem = 4096 87380 4194304

#为自动调优定义socket使用的内存。第一个值是为socket发送缓冲区分配的最少字节数；第二个值是默认值（该值会被wmem_default覆盖），缓冲区在系统负载不重的情况下可以增长到这个值；第三个值是发送缓冲区空间的最大字节数（该值会被wmem_max覆盖）。
net.ipv4.tcp_wmem = 4096 16384 4194304

#默认的TCP数据发送窗口大小（字节）
net.core.wmem_default = 8388608

#默认的TCP数据接收窗口大小（字节）
net.core.rmem_default = 8388608

#最大的TCP数据接收窗口（字节）
net.core.rmem_max = 16777216

#最大的TCP数据发送窗口(字节)
net.core.wmem_max = 16777216

#在每个网络接口接收数据包的速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目。
net.core.netdev_max_backlog = 262144

#定义了系统中每一个端口最大的监听队列的长度。
net.core.somaxconn = 262144

#最大孤儿套接字数，单位是个
net.ipv4.tcp_max_orphans = 3276800

#对于还未获得对方确认的连接请求，可保存在队列中的最大数目。对于经常出现过载的服务器，可以尝试增加这个数字。
net.ipv4.tcp_max_syn_backlog = 262144

#TCP时间戳（会在TCP包头增加12个字节），以一种比重发超时更精确的方法（参考RFC 1323）来启用对RTT 的计算，为实现更好的性能应该启用这个选项。
net.ipv4.tcp_timestamps = 1

#TCP三次握手的syn/ack阶段，重试次数
net.ipv4.tcp_synack_retries = 1

#一个新建连接，内核要发送SYN 连接请求才决定放弃的个数
net.ipv4.tcp_syn_retries = 1

#开启TCP连接中TIME-WAIT sockets的快速回收。在tcp timestamp关闭的条件下，开启tcp_tw_recycle是不起作用的；而tcp timestamp可以独立开启并起作用
net.ipv4.tcp_tw_recycle = 1

#开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接
net.ipv4.tcp_tw_reuse = 1

#确定TCP栈应该如何反映内存使用，每个值的单位都是内存页（通常是4KB）
net.ipv4.tcp_mem = 94500000 915000000 927000000

#对于本端断开的socket连接，TCP保持在FIN-WAIT-2状态的时间（秒）
net.ipv4.tcp_fin_timeout = 1

#当keepalive起用的时候，TCP发送keepalive消息的频度
net.ipv4.tcp_keepalive_time = 1200

#增加系统IP端口限制
net.ipv4.ip_local_port_range = 1024 65535

#禁ping
#net.ipv4.icmp_echo_ignore_all = 1 
EOF
/sbin/sysctl -p
echo "sysctl set OK!!"
}

#-----------------------------------------------------------------------------
limit
sysctl
