import akshare as ak
import pandas as pd
import pyarrow.feather as feather
import time


# 1. 获得全市场股票代码
stock_info_a_code_name_df = ak.stock_info_a_code_name()
# print(stock_info_a_code_name_df)

# 其他几种获得股票代码的方法，信息更为丰富
# stock_info_sh_name_code_df = ak.stock_info_sh_name_code(symbol="主板A股")
# print(stock_info_sh_name_code_df)

# stock_info_sz_name_code_df = ak.stock_info_sz_name_code(symbol="A股列表")
# print(stock_info_sz_name_code_df)

# stock_info_bj_name_code_df = ak.stock_info_bj_name_code()
# print(stock_info_bj_name_code_df)

# 将股票名写入文件,使用feather格式，名字为 "CodeName+日期.dat"
today_tuple = time.localtime(time.time())[0:3]
today_str = [str(i) for i in today_tuple]
filename = 'CodeName_' + ''.join(today_str) + '.dat'
stock_info_a_code_name_df.to_feather('./data/'+filename)

# 2. 获得30个交易日的数据
# 2.1 获得最近30个交易日的时间
# 截止2023-12-29，共有8070个交易日
tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
# print(tool_trade_date_hist_sina_df)
today = '-'.join(today_str)
trade_list_30 = []
for i in tool_trade_date_hist_sina_df[::-1].index:
    # print(tool_trade_date_hist_sina_df.iloc[i])
    if str(tool_trade_date_hist_sina_df.iloc[i]['trade_date']) <= today:
        print(str(tool_trade_date_hist_sina_df.iloc[i]['trade_date']))
        trade_list_30 = [str(i) for i in tool_trade_date_hist_sina_df[i-29:i+1]['trade_date']]
        break
        # trade_list_30 = [str(i) for i in list(tool_trade_date_hist_sina_df[i:30])]
# 2.2