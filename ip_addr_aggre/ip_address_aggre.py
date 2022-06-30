#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'wanghaotian' 

'''
非交互型合并网段:
1.在origin_ip.txt文件中写入要合并的网段,格式为X.X.X.X/X,一行一个网段
2.结果写入到final_result.txt文件中,一个网段一行
3.如果想修改结果网段之间的分隔符,修改format全局变量
'''

import ipaddress,re,os

from numpy import append


# 单引号中间的值是结果网段分隔符,\n表示回车
format = '\n'

# 程序文件路经
script_dir = os.path.dirname(__file__)

# ip和netmask正则表达式
ip_pattern = re.compile(r'^((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])$')
netmask_pattern = re.compile(r'^(\d)|(1\d)|(2\d)|(3[0-2])$')

# 原始ip地址文件
origin_file = "origin_ip.txt"

# 结果地址文件
result_file = "final_result.txt"


# 从文件读取ip信息，返回str类型的网段list
def read_ip_file(ip_file)->list:
    # 读取文件中的ip信息，从SC拷贝出来的ip地址以"，"分隔，就1行数据
    # 也支持每行一段ip地址的情况排序
    with open(os.path.join(script_dir,ip_file),'r') as f:
        try:
            line = f.readlines()
        except:
            raise RuntimeError('ip addr document is empty!')
        else:
            line = "".join(line)
            line = line.rstrip('\n')
            line = re.split(',|\n',line)
            return line

# 通过str类型的网段list,返回IPv4Network类型列表IPv4Network_list
def ip_str_to_IPv4Network(origin_ip_list)->list:
    # 初始化IPv4Network类型列表
    IPv4Network_list = []
    # 将origin_ip_list的str转换成IPv4Network类型
    for i in origin_ip_list:
        try:
            IPv4Network_list.append(ipaddress.ip_network(i,strict=False))
        except:
            raise RuntimeError('ip addr document is empty!')
    IPv4Network_list = sorted(IPv4Network_list)
    return IPv4Network_list

# 将IPv4Network类型列表排序写入到文件ip_file中
def write_ip_file(ip_file,IPv4Network_list,format='\n'):
    IPv4Network_list = sorted(IPv4Network_list)
    with open(os.path.join(script_dir,ip_file),'w+',encoding='utf8') as f:
        script = ''
        for IPv4Network in IPv4Network_list:
            script = f'{script}{IPv4Network}{format}'
        script = script.rstrip(format)
        f.write(script)

# 聚和函数,参数是IPv4Network类型的列表,里面是待聚和的网段
def aggre_net(ip_prefix_list)->list:
    collapse_prefix = ipaddress.collapse_addresses(ip_prefix_list)
    aggre_net_list = [ ipaddr for ipaddr in collapse_prefix ]
    return aggre_net_list

if __name__ == '__main__' :
    # # 初始化待合并的IP地址列表
    # ip_prefix_list = []
    # # 读取IP地址文件
    # with open(os.path.join(script_dir,origin_file),'r') as f:
    #     # 读入一行
    #     line = f.readline()
    #     # 去除行尾的\n和空格
    #     line = line.strip('\n').strip('\r').strip()
    #     num = 1
    #     while line:
    #         if '/' in line:
    #             ip_prefix = line.split('/')
    #             # 格式检查
    #             if ip_pattern.fullmatch(ip_prefix[0]) and netmask_pattern.fullmatch(ip_prefix[1]):
    #                 ip_prefix_list.append(ipaddress.IPv4Network(line,strict=False))
    #                 num +=1
    #             # 格式检查
    #             elif ip_pattern.fullmatch(ip_prefix[0]) and ip_pattern.fullmatch(ip_prefix[1]):
    #                 ip_prefix_list.append(ipaddress.IPv4Network(line,strict=False))
    #                 num +=1
    #             else:
    #                 raise ValueError(f'line {num}: {line} format error!')
    #         elif ip_pattern.fullmatch(line):
    #             try:
    #                 ip_prefix_list.append(ipaddress.IPv4Network(line,strict=False))
    #                 num +=1
    #             except:
    #                 raise ValueError(f'line {num}: {line} format error!')
    #         line = f.readline()
    #         # 去除行尾的\n和空格
    #         line = line.strip('\n').strip('\r').strip()
    # aggre_net_list = aggre_net(ip_prefix_list)
    
    # # 将结果写入文件
    # with open(os.path.join(script_dir,'final_result.txt'),'w+') as f:
    #     total_script = ''
    #     for i in aggre_net_list:
    #         total_script = f'{total_script}{i}{format}'
    #     total_script = total_script.rstrip(f'{format}')
    #     f.write(total_script)
    #     print('Done')

    # 获取str类型的origin_ip_list列表
    origin_ip_list = read_ip_file(origin_file)
    # 将str类型转换为IPv4Network类型
    origin_ip_list = ip_str_to_IPv4Network(origin_ip_list)
    # 聚合地址
    aggre_ip_list = aggre_net(origin_ip_list)
    # 写入文件
    write_ip_file(result_file,aggre_ip_list)