import akshare as ak
import pandas as pd
import pyarrow.feather as feather
import time


# 1. 获得全市场股票代码
stock_info_a_code_name_df = ak.stock_info_a_code_name()
# print(stock_info_a_code_name_df)

############################################################################
# 其他几种获得股票代码的方法，信息更为丰富
# stock_info_sh_name_code_df = ak.stock_info_sh_name_code(symbol="主板A股")
# print(stock_info_sh_name_code_df)

# stock_info_sz_name_code_df = ak.stock_info_sz_name_code(symbol="A股列表")
# print(stock_info_sz_name_code_df)

# stock_info_bj_name_code_df = ak.stock_info_bj_name_code()
# print(stock_info_bj_name_code_df)
############################################################################

# 将股票名写入文件,使用feather格式，名字为 "CodeName+日期.dat"
today_tuple = time.localtime(time.time())[0:3]
today_str = [str(i) for i in today_tuple]
#定义‘今天’，文本，格式‘1900-01-01’
today = '-'.join(today_str)
filename = 'CodeName_' + ''.join(today_str) + '.dat'
stock_info_a_code_name_df.to_feather('./data/'+filename)

# 2. 获得30个交易日的数据
# 2.1 获得最近30个交易日的时间
# 截止2023-12-29，共有8070个交易日
tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
# print(tool_trade_date_hist_sina_df)
# 定义一个包含最近30个交易日日期的list，日期为文本，格式为1900-01-01
trade_list_30 = []
for i in tool_trade_date_hist_sina_df[::-1].index:
    # print(tool_trade_date_hist_sina_df.iloc[i])
    if str(tool_trade_date_hist_sina_df.iloc[i]['trade_date']) <= today:
        print(str(tool_trade_date_hist_sina_df.iloc[i]['trade_date']))
        trade_list_30 = [str(i) for i in tool_trade_date_hist_sina_df[i-29:i+1]['trade_date']]
        break
        # trade_list_30 = [str(i) for i in list(tool_trade_date_hist_sina_df[i:30])]
# 2.2 获得股票数据
# 2.2.1 
###########################################################################################
# 5分钟数据 period=1，5，15，30，60 获取相应分钟的数据
# 新浪接口，只能获得当日数据
# stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol='sh600751', period='1', adjust="qfq")
# print(stock_zh_a_minute_df)
###########################################################################################

# 分时数据-东财
# 接口: stock_zh_a_hist_min_em
# 目标地址: http://quote.eastmoney.com/concept/sh603777.html?from=classic
# 描述: 东方财富网-行情首页-沪深京 A 股-每日分时行情; 该接口只能获取近期的分时数据，注意时间周期的设置
# 限量: 单次返回指定股票、频率、复权调整和时间区间的分时数据, 其中 1 分钟数据只返回近 5 个交易日数据且不复权
# 名称	        类型	描述
# symbol    	str	symbol='sh000300'; 股票代码
# start_date	str	start_date="1979-09-01 09:32:00"; 日期时间; 默认返回所有数据
# end_date	    str	end_date="2222-01-01 09:32:00"; 日期时间; 默认返回所有数据
# period	    str	period='5'; choice of {'1', '5', '15', '30', '60'}; 其中 1 分钟数据返回近 5 个交易日数据且不复权
# adjust	    str	adjust=''; choice of {'', 'qfq', 'hfq'}; '': 不复权, 'qfq': 前复权, 'hfq': 后复权, 其中 1 分钟数据返回近 5 个交易日数据且不复权
# 5 min 数据返回32天
# 60 min 数据返回31天
data_60 = []
for i in stock_info_a_code_name_df['code']:
    get_data = ak.stock_zh_a_hist_min_em(symbol=i,end_date=today,period='60',adjust='qfq')
    data_60.append(get_data)

# It is worth noting that concat() makes a full copy of the data, and that constantly
#  reusing this function can create a significant performance hit. If you need to use
#  the operation over several datasets, use a list comprehension.
# frames = [process_your_file(f) for f in files]
# result = pd.concat(frames)

data_60_df = pd.concat(data_60)

data_60_df.to_feather('./data/'+today+'-data')