# 1.ip_addr_aggre
ip_address_aggre.py是ip地址聚和程序,将多个网段自动聚和为汇总网段
程序执行为非交互模式:
- 在ip_addr.txt文件中写入要合并的网段,格式为X.X.X.X/X,一行一个网段
- 结果写入到ip_addr_aggre_result.txt文件中,一个网段一行
- 如果想修改结果网段之间的分隔符,修改`ip_address_aggre.py`代码文件中第`16`行`format`全局变量

# 2.split_net
split_net.py是ip地址切分程序,从1个汇总网段中排除出n个子网,再将剩余的网段进行汇聚
程序执行为交互模式:
- 输入汇总网段
- 输入要从汇总网段中去除的网段,格式为X.X.X.X/X,多个以空格分隔
- 结果写入到split_result.txt文件中,格式为一横行,以逗号分隔
- 如果想修改结果网段之间的分隔符,修改`split_net.py`代码文件中第`17`行`format`全局变量
