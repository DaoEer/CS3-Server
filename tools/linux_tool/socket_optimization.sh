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
#�ر�ipv4ת��
net.ipv4.ip_forward = 0

#�����ϸ�ķ���·��У�飬��������á�0Ϊ�رգ�2Ϊ��ɢ
net.ipv4.conf.all.rp_filter = 0
net.ipv4.conf.default.rp_filter = 1

#������Դ·�ɵİ�
net.ipv4.conf.default.accept_source_route = 0

#����SysRq��ȫ������
kernel.sysrq = 0

#�����ں˵�ϵͳ������Թ��ܿ��������ƺ���ת������PID�������ļ����������ڶ��߳�
kernel.core_uses_pid = 1

#����SYN��ˮ��������
net.ipv4.tcp_syncookies = 1

#�ں���Ϣ/�ڴ��������
#ÿ����Ϣ���е�����ֽ�����
kernel.msgmnb = 65536

#ÿ����Ϣ�����ֵ
kernel.msgmax = 65536

#�����ڴ�ε����ֵ��Ӧ����Ϊ���ڱ���ʵ���ڴ档
kernel.shmmax = 68719476736

#ϵͳһ�ο���ʹ�õĹ����ڴ���������ҳΪ��λ��
kernel.shmall = 4294967296

#��ʾϵͳͬʱ����TIME_WAIT�׽��ֵ��������
net.ipv4.tcp_max_tw_buckets = 262144

#������ѡ���Ӧ�𣬣����ڹ�����ͨ����˵�����ѡ��Ӧ�����ã����ǻ����Ӷ�CPU��ռ�á�
net.ipv4.tcp_sack = 1

#����RFC 1323�����window scaling��Ҫ֧�ֳ���64KB��TCP���ڣ��������ø�ֵ
net.ipv4.tcp_window_scaling = 1

#����TCP��󻺳�����С
#Ϊ�Զ����Ŷ���socketʹ�õ��ڴ档��һ��ֵ��Ϊsocket���ջ���������������ֽ������ڶ���ֵ��Ĭ��ֵ����ֵ�ᱻrmem_default���ǣ�����������ϵͳ���ز��ص�����¿������������ֵ��������ֵ�ǽ��ջ������ռ������ֽ�������ֵ�ᱻrmem_max���ǣ���
net.ipv4.tcp_rmem = 4096 87380 4194304

#Ϊ�Զ����Ŷ���socketʹ�õ��ڴ档��һ��ֵ��Ϊsocket���ͻ���������������ֽ������ڶ���ֵ��Ĭ��ֵ����ֵ�ᱻwmem_default���ǣ�����������ϵͳ���ز��ص�����¿������������ֵ��������ֵ�Ƿ��ͻ������ռ������ֽ�������ֵ�ᱻwmem_max���ǣ���
net.ipv4.tcp_wmem = 4096 16384 4194304

#Ĭ�ϵ�TCP���ݷ��ʹ��ڴ�С���ֽڣ�
net.core.wmem_default = 8388608

#Ĭ�ϵ�TCP���ݽ��մ��ڴ�С���ֽڣ�
net.core.rmem_default = 8388608

#����TCP���ݽ��մ��ڣ��ֽڣ�
net.core.rmem_max = 16777216

#����TCP���ݷ��ʹ���(�ֽ�)
net.core.wmem_max = 16777216

#��ÿ������ӿڽ������ݰ������ʱ��ں˴�����Щ�������ʿ�ʱ�������͵����е����ݰ��������Ŀ��
net.core.netdev_max_backlog = 262144

#������ϵͳ��ÿһ���˿����ļ������еĳ��ȡ�
net.core.somaxconn = 262144

#���¶��׽���������λ�Ǹ�
net.ipv4.tcp_max_orphans = 3276800

#���ڻ�δ��öԷ�ȷ�ϵ��������󣬿ɱ����ڶ����е������Ŀ�����ھ������ֹ��صķ����������Գ�������������֡�
net.ipv4.tcp_max_syn_backlog = 262144

#TCPʱ���������TCP��ͷ����12���ֽڣ�����һ�ֱ��ط���ʱ����ȷ�ķ������ο�RFC 1323�������ö�RTT �ļ��㣬Ϊʵ�ָ��õ�����Ӧ���������ѡ�
net.ipv4.tcp_timestamps = 1

#TCP�������ֵ�syn/ack�׶Σ����Դ���
net.ipv4.tcp_synack_retries = 1

#һ���½����ӣ��ں�Ҫ����SYN ��������ž��������ĸ���
net.ipv4.tcp_syn_retries = 1

#����TCP������TIME-WAIT sockets�Ŀ��ٻ��ա���tcp timestamp�رյ������£�����tcp_tw_recycle�ǲ������õģ���tcp timestamp���Զ���������������
net.ipv4.tcp_tw_recycle = 1

#�������á�����TIME-WAIT sockets���������µ�TCP����
net.ipv4.tcp_tw_reuse = 1

#ȷ��TCPջӦ����η�ӳ�ڴ�ʹ�ã�ÿ��ֵ�ĵ�λ�����ڴ�ҳ��ͨ����4KB��
net.ipv4.tcp_mem = 94500000 915000000 927000000

#���ڱ��˶Ͽ���socket���ӣ�TCP������FIN-WAIT-2״̬��ʱ�䣨�룩
net.ipv4.tcp_fin_timeout = 1

#��keepalive���õ�ʱ��TCP����keepalive��Ϣ��Ƶ��
net.ipv4.tcp_keepalive_time = 1200

#����ϵͳIP�˿�����
net.ipv4.ip_local_port_range = 1024 65535

#��ping
#net.ipv4.icmp_echo_ignore_all = 1 
EOF
/sbin/sysctl -p
echo "sysctl set OK!!"
}

#-----------------------------------------------------------------------------
limit
sysctl
