#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'wanghaotian' 

'''
非交互型合并网段:
1.在ip_addr.txt文件中写入要合并的网段,格式为X.X.X.X/X,一行一个网段
2.结果写入到ip_addr_aggre_result.txt文件中,一个网段一行
3.如果想修改结果网段之间的分隔符,修改format全局变量
'''

import ipaddress,re,os

# 单引号中间的值是结果网段分隔符,\n表示回车
format = '\n'

# 程序文件路经
script_dir = os.path.dirname(__file__)

# 聚和函数,参数是IPv4Network类型的列表,里面是待聚和的网段
def aggre_net(ip_prefix_list):
    collapse_prefix = ipaddress.collapse_addresses(ip_prefix_list)
    aggre_net_list = [ ipaddr for ipaddr in collapse_prefix ]
    return aggre_net_list

if __name__ == '__main__' :
    # 初始化待合并的IP地址列表
    ip_prefix_list = []
    # 读取IP地址文件
    with open(os.path.join(script_dir,'ip_addr.txt'),'r') as f:
        # 读入一行
        line = f.readline()
        # 去除行尾的\n和空格
        line = line.strip('\n').strip('\r').strip()
        num = 1
        while line:
            if '/' in line:
                ip_prefix = line.split('/')
                # 格式检查
                if re.fullmatch(r'^((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])$',ip_prefix[0]) and re.fullmatch(r'^(\d)|(1\d)|(2\d)|(3[0-2])$',ip_prefix[1]):
                    ip_prefix_list.append(ipaddress.IPv4Network(line,strict=False))
                    num +=1
                # 格式检查
                elif re.fullmatch(r'^((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])$',ip_prefix[0]) and re.fullmatch(r'^((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])$',ip_prefix[1]):
                    ip_prefix_list.append(ipaddress.IPv4Network(line,strict=False))
                    num +=1
                else:
                    raise ValueError(f'line {num}: {line} format error!')
            line = f.readline()
            # 去除行尾的\n和空格
            line = line.strip('\n').strip('\r').strip()
    aggre_net_list = aggre_net(ip_prefix_list)
    
    # 将结果写入文件
    with open(os.path.join(script_dir,'ip_addr_aggre_result.txt'),'w+') as f:
        total_script = ''
        for i in aggre_net_list:
            total_script = f'{total_script}{i}{format}'
        total_script = total_script.rstrip(f'{format}')
        f.write(total_script)
        print('Done')