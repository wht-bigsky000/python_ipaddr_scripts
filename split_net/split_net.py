#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'wanghaotian' 

'''
交互型切分网段:
1.排序原始地址文件origin_ip.txt，自行观察哪些地址需要合并分割
2.输入要合并到的汇总地址段，并从中剔除部分已占用子网
3.对原始地址进行剔除合并，结果写入final_result.txt
PS:如果想修改结果网段之间的分隔符,修改format全局变量
'''

import ipaddress,re,os

# 单引号中间的值是结果网段分隔符,\n表示回车
output_format = ','

# 原始ip文件
origin_ip_file = 'origin_ip.txt'

# 结果ip文件
final_result_file = 'final_result.txt'

# 程序文件路经
script_dir = os.path.dirname(__file__)

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

# 将IPv4Network类型列表排序写入到文件ip_file中
def write_ip_file(ip_file,IPv4Network_list,format='\n'):
    IPv4Network_list = sorted(IPv4Network_list)
    with open(os.path.join(script_dir,ip_file),'w+',encoding='utf8') as f:
        script = ''
        for IPv4Network in IPv4Network_list:
            script = f'{script}{IPv4Network}{format}'
        script = script.rstrip(format)
        f.write(script)

# 在汇总网段列表summary_prefix中去拆分出exclude_prefix这个网段,返回IPv4Network类型的列表
def split_prefix(summary_prefix:list,exclude_prefix)->list:
    # 待返回的网段列表
    network_list = list(summary_prefix)
    for j in summary_prefix:
        # 如果汇总网段j包含要排除的网段
        if exclude_prefix.subnet_of(j):
            # 在network_list中将汇总网段j,替换切分后的网段
            network_list.remove(j)
            network_list.extend(list(j.address_exclude(exclude_prefix)))
    return network_list

# 在原始网段中将部分网段替换为聚合拆分网段,返回IPv4Network类型的列表
def replace_IPv4Network(origin_IPv4Network:list,summary_IPv4Network:list,splited_IPv4Network:list)->list:
    replaced_IPv4Network_list = list(origin_IPv4Network)
    # 如果没有切分地址，将汇总地址赋给切分地址，最终将汇总地址并入原始地址
    if len(splited_IPv4Network) == 0:
        splited_IPv4Network_list = summary_IPv4Network
    else:
        splited_IPv4Network_list = splited_IPv4Network
    # 删除原始地址中属于汇总地址的子网部分
    for IPv4Network in origin_IPv4Network:
        if IPv4Network.subnet_of(summary_IPv4Network[0]):
            replaced_IPv4Network_list.remove(IPv4Network)
    replaced_IPv4Network_list.extend(splited_IPv4Network_list)
    return replaced_IPv4Network_list

if __name__ == '__main__':
    long_banner = '1.排序文件中的IP地址\n2.进行汇总网段分割\n3.分割网段替换进文件中\nq.退出\n请输入: '
    short_banner = '1.排序文件中的IP地址 2.进行汇总网段分割 3.分割网段替换进文件中 q.退出\n请输入: '
    a = input(long_banner)
    while True:
        if a == '1':
            ip_str = read_ip_file(origin_ip_file)
            # 原始地址
            global origin_IPv4Network_list
            origin_IPv4Network_list = ip_str_to_IPv4Network(ip_str)
            write_ip_file(origin_ip_file,origin_IPv4Network_list)
            print('Done')
            a = input(short_banner)
        elif a == '2':
            # 这里得到str类型的summary_prefix
            summary_prefix = input('请输入汇总网段,格式为X.X.X.X/X: ')
            # 格式校验
            while True:
                if '/' in summary_prefix:
                    ip_prefix = summary_prefix.split('/')
                    if re.fullmatch(r'^((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])$',ip_prefix[0]) and re.fullmatch(r'^(\d)|(1\d)|(2\d)|(3[0-2])$',ip_prefix[1]):
                        break
                    else:
                        summary_prefix = input('输入格式不对,请重新输入: ')
                else:
                    summary_prefix = input('输入格式不对,请重新输入: ')
            # 将str类型的summary_prefix,转换为IPv4Network类型
            summary_IPv4Network = ipaddress.ip_network(summary_prefix,strict=False)
            # 制作summary_IPv4Network_list
            global summary_IPv4Network_list
            summary_IPv4Network_list = []
            summary_IPv4Network_list.append(summary_IPv4Network)
            # 要排除的子网,IPv4Network类型的list
            exclude_prefix_list = input('请输入需要去除的网段,格式为X.X.X.X/X,多个地址段用空格或,分隔:\n')
            if exclude_prefix_list:
                while True:
                    #去掉首尾空格
                    exclude_prefix_list = exclude_prefix_list.strip()
                    #以空格分隔
                    exclude_prefix_list = re.split(' |,', exclude_prefix_list )
                    #格式错误的网段数
                    wrong_num = 0
                    for ip_prefix in exclude_prefix_list:
                        # 将网段分成地址和掩码
                        ip_prefix = ip_prefix.split('/')
                        # 格式校验
                        if re.fullmatch(r'^((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])$',ip_prefix[0]) and re.fullmatch(r'^(\d)|(1\d)|(2\d)|(3[0-2])$',ip_prefix[1]):
                            continue
                        else:
                            wrong_num = 1
                            break
                    if wrong_num == 1:
                        exclude_prefix_list = input(f'{ip_prefix[0]}/{ip_prefix[1]}输入格式不对,请重新输入:\n')
                    else:
                        break
            exclude_IPv4Network_list = ip_str_to_IPv4Network(exclude_prefix_list)
            # 初始化拆分后的网段
            global splited_IPv4Network_list
            # splited_IPv4Network_list = []
            splited_IPv4Network_list = summary_IPv4Network_list
            # 在汇总网段列表中排除特定网段,获得最终拆分后的网段splited_IPv4Network_list
            for exclude_IPv4Network in exclude_IPv4Network_list:
                # splited_IPv4Network_list = split_prefix(summary_IPv4Network_list,exclude_IPv4Network)
                splited_IPv4Network_list = split_prefix(splited_IPv4Network_list,exclude_IPv4Network)
            # 将拆分结果写入文件
            write_ip_file('split_results.txt',splited_IPv4Network_list)
            print('Done')
            a = input(short_banner)
        elif a == '3':
            replaced_IPv4Network_list = replace_IPv4Network(origin_IPv4Network_list,summary_IPv4Network_list,splited_IPv4Network_list)
            write_ip_file(final_result_file,replaced_IPv4Network_list,format=output_format)
            print('Done')
            a = input(short_banner)
        elif a == 'q' :
            print('Quit')
            break
        else :
            a = input('输入错误，请输入1-3、q: ')