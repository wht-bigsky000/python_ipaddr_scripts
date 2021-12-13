#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'wanghaotian' 

'''
交互型切分网段:
1.输入汇总网段
2.输入要从汇总网段中去除的网段,格式为X.X.X.X/X,多个以空格分隔
3.结果写入到split_result.txt文件中,格式为一横行,以逗号分隔
4.如果想修改结果网段之间的分隔符,修改format全局变量
'''

import ipaddress,re,os

# 单引号中间的值是结果网段分隔符,\n表示回车
format = ','

# 程序文件路经
script_dir = os.path.dirname(__file__)

# 输入网段,返回IPv4Network类型列表exclude_prefix
def input_exclude_addr()->list:
    exclude_addr = input('请输入需要去除的网段,格式为X.X.X.X/X,多个地址段用空格分隔:\n')
    while True:
        #去掉首尾空格
        exclude_addr = exclude_addr.strip()
        #以空格分隔
        exclude_addr = exclude_addr.split(' ')
        #格式错误的网段数
        wrong_num = 0
        for ip_prefix in exclude_addr:
            #将网段分成地址和掩码
            ip_prefix = ip_prefix.split('/')
            if re.fullmatch(r'^((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])$',ip_prefix[0]) and re.fullmatch(r'^(\d)|(1\d)|(2\d)|(3[0-2])$',ip_prefix[1]):
                continue
            else:
                wrong_num = 1
                break
        if wrong_num == 1:
            exclude_addr = input('输入格式不对,请重新输入:\n')
        else:
            break
    # 初始化IPv4Network类型列表
    exclude_prefix = []
    # 将exclude_addr的str转换成IPv4Network类型
    for i in exclude_addr:
        exclude_prefix.append(ipaddress.ip_network(i,strict=False))
    return exclude_prefix

# 在汇总网段列表summary_prefix中去拆分出exclude_prefix这个网段,返回IPv4Network类型的列表
def split_prefix(summary_prefix:list,exclude_prefix):
    # 待返回的网段列表
    network_list = summary_prefix
    for j in network_list:
        # 如果汇总网段j包含要排除的网段
        if exclude_prefix.subnet_of(j):
            # 在network_list中将汇总网段j,替换切分后的网段
            network_list.remove(j)
            network_list.extend(list(j.address_exclude(exclude_prefix)))
    return network_list

if __name__ == '__main__':
    # 这里得到str类型的summary_prefix
    summary_prefix = input('请输入汇总网段,格式为X.X.X.X/X:\n')
    while True:
        if '/' in summary_prefix:
            ip_prefix = summary_prefix.split('/')
            if re.fullmatch(r'^((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])$',ip_prefix[0]) and re.fullmatch(r'^(\d)|(1\d)|(2\d)|(3[0-2])$',ip_prefix[1]):
                break
            else:
                summary_prefix = input('输入格式不对,请重新输入: ')
        else:
            summary_prefix = input('输入格式不对,请重新输入: ')

    # 将str类型的summary_prefix,转换为IPv4Network类型的list
    summary_prefix_list = []
    summary_prefix_list.append(ipaddress.ip_network(summary_prefix,strict=False))
    # 要排除的子网,IPv4Network类型的list
    exclude_prefix_list = input_exclude_addr()
    # 在汇总网段列表中排除特定网段,获得最终拆分后的网段summary_prefix_list
    for exclude_prefix in exclude_prefix_list:
        summary_prefix_list = split_prefix(summary_prefix_list,exclude_prefix)
    # 将拆分后的网段从小到大排序
    summary_prefix_list.reverse()
    with open(os.path.join(script_dir,'split_results.txt'),'w+') as f:
        total_script = ''
        for summary_prefix in summary_prefix_list:
            total_script = f'{total_script}{summary_prefix}{format}'
        total_script = total_script.rstrip(f'{format}')
        f.write(total_script)
        print('Done')