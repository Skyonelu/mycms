import datetime
import decimal
import json
import math
import traceback
from typing import Any, List

from fastapi import APIRouter, UploadFile, File, Form,Request
from tortoise import Tortoise
from tortoise.transactions import in_transaction
from .crud import su_us_hk

from utils import logger
from utils.excel_tools import ExcelTools
from .schema import *
from utils.response_code import ResultResponse, HttpStatus
from ..user.model import *
from ..user.view import generate_response

router = APIRouter()

def  judp_third_fourth_fifth(third,second,count,all_count):
    second2=second
    if 1 <= third <= 8:  # 添加第二种：    取收盘价第三位数字，若第三位是1 - 8，则第二位不变；
        pass
    elif third == 9 or third == 0:
        if count < all_count * 0.1:  # 若第三位是9，第二位数字（0 - 9）出现的次数小于天数 * 10 %，则第二位不变；
            pass
        else:  # 若第三位是9，第二位数字（0 - 9）出现的次数大于天数 * 10 %，则第二位变大一个数字（9到0）
            if third == 9:
                if second == 9:
                    second2 = 0
                else:
                    second2 += 1
            else:
                if second == 0:
                    second2 = 9
                else:
                    second2 -= 1
    else:
        pass
    return second2

def first_second_list(a):
    x=decimal.Decimal(str(a)) *1000000000
    x=str(x)
    first, second,third,fourth,fifth = x[0], x[1],x[2],x[3],x[4]
    return int(first), int(second),int(third),int(fourth),int(fifth)


def isa10(a, b):
    if a == 1 and b == 1:
        return 0
    elif a == 1:
        return 10 - b
    elif b == 1:
        return a - 10
    else:
        return a - b




def sut(a, shouwei):
    # a=[2471,516,131,34,104,231,68,118,373,4046]
    ben_l = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
    """1. 规定排列顺序序号 1 2 3 4 5 6 7 8 9
    2. 固定对应顺序序号的理论概率如下 1=30.1% 2=17.6% 3=12.5% 4=9.7% 5=7.9% 6=6.7% 7=5.8% 8=5.% 9=4.6%
    3. 将现有数据库stock_info_a_rate(或者stock_hk_rate stock_us_rate)中现有的首位发生概率（stock_actual_probability）列进行排序
    4. 最大概率的排列序号为1，依次对应（比如最大概率的首位在数据库那一列里是5 概率是50%，那么首位5=序号1，首位6=序号2，首位7=序号3，首位8=序号4，首位9=序号5，首位1=序号6，首位2=序号7，首位3=序号8，首位4=序号9）
    5. 之后查找对应序号（1-9）的固定理论概率（也就是第二步那个表里的数据）"""
    sort_base=[1,2,3,4,5,6,7,8,9]
    a_9=a[:9:]#取1~9占的个数
    a_index=a.index(max(a_9))#取数组中最多的数
    a_list=[]
    a_list.extend(ben_l[a_index::])
    a_list.extend(ben_l[:a_index:])
    a_sort=sort_base[a_index::]+sort_base[:a_index:]
    b = [round(i * a[-1]) for i in a_list]
    # print(b)#[1218, 712, 506, 392, 320, 271, 235, 206, 186]
    list_result = list(map(lambda x, y: y - x, a, b))  # 差值
    # print(list_result)#[-1253, 196, 375, 358, 216, 40, 167, 88, -187]
    Glist1 = [1 if (shouwei[8] == 1 or shouwei[1] == 1) and list_result[0] > 0 else 0]
    Glist2 = [1 if (shouwei[7] == 1 or shouwei[0] == 1) and list_result[8] > 0 else 0]
    Glist = Glist1 + [1 if (shouwei[i - 1] == 1 or shouwei[i + 1] == 1) and list_result[i] > 0 else 0 for i in
                      range(1, 8)] + Glist2
    # print("GList",Glist)
    Mlist = [list_result[i] if (shouwei[i] == 1 and list_result[i] > 0) else 0 for i in range(9)]
    # print(Mlist)
    Nlist1 = [list_result[0] if (Glist[0] == 1 and Mlist[8] == 0 and Mlist[1] == 0 and list_result[0] > 0) else 0]
    Nlist2 = [list_result[8] if (Glist[8] == 1 and Mlist[7] == 0 and Mlist[0] == 0 and list_result[8] > 0) else 0]
    Nlist = Nlist1 + [
        list_result[i] if (Glist[i] == 1 and Mlist[i - 1] == 0 and Mlist[i + 1] == 0 and list_result[i] > 0) else 0 for
        i in range(1, 8)] + Nlist2
    # print(Nlist)
    Olist1 = [Nlist[0] if ((Nlist[0] - Nlist[2]) < 0 or (Nlist[0] - Nlist[7]) < 0) else 0]
    Olist2 = [Nlist[1] if ((Nlist[1] - Nlist[3]) < 0 or (Nlist[1] - Nlist[8]) < 0) else 0]
    Olist3 = [Nlist[7] if ((Nlist[7] - Nlist[0]) < 0 or (Nlist[7] - Nlist[5]) < 0) else 0]
    Olist4 = [Nlist[8] if ((Nlist[8] - Nlist[1]) < 0 or (Nlist[8] - Nlist[6]) < 0) else 0]
    Olist = Olist1 + [Nlist[i] if ((Nlist[i] - Nlist[i + 2]) < 0 or (Nlist[i] - Nlist[i - 2]) < 0) else 0 for i in
                      range(2, 7)] + Olist2 + Olist3 + Olist4
    # print(Olist)
    Plist1 = [Nlist[0] if ((Nlist[0] - Nlist[2]) > 0 and (Nlist[0] - Nlist[7]) > 0) else 0]
    Plist2 = [Nlist[1] if ((Nlist[1] - Nlist[3]) > 0 and (Nlist[1] - Nlist[8]) > 0) else 0]
    Plist3 = [Nlist[7] if ((Nlist[7] - Nlist[0]) > 0 and (Nlist[7] - Nlist[5]) > 0) else 0]
    Plist4 = [Nlist[8] if ((Nlist[8] - Nlist[1]) > 0 and (Nlist[8] - Nlist[6]) > 0) else 0]
    Plist = Plist1 + [Nlist[i] if ((Nlist[i] - Nlist[i + 2]) > 0 and (Nlist[i] - Nlist[i - 2]) > 0) else 0 for i in
                      range(2, 7)] + Plist2 + Plist3 + Plist4
    # print(Plist)
    # H10=M10 + O10 + P10#思诺假设个数（天）*
    Hlist = list(map(lambda x, y, z: x + y + z, Mlist, Olist, Plist))
    # IF(F8=1,(9-B8)/D8,0)      IF(F12=1,9/D12,0)
    Ilist1 = [round(9 / a[8], 4) if shouwei[8] == 1 else 0]
    Ilist = [round((8 - i) / a[i], 4) if shouwei[i] == 1 else 0 for i in range(0, 8)] + Ilist1  # 个股当前首位位置
    # =IF(I9 > 0, 1 / I9, 0)变动1单位个数（天）
    Jlist = [int(1 / Ilist[i]) if Ilist[i] > 0 else 0 for i in range(0, 9)]  # 变动1单位个数（天）
    # 9 / E13总速率（首位单位/天）
    chazhi_add = sum([i for i in list_result if i > 0])
    K_one = round(9 / chazhi_add, 4) if chazhi_add != 0 else 0
    jiashe = list(map(lambda x, y, z: x + y + z, a, Mlist, Olist))
    sumjiashe = sum(jiashe)
    # print("斯洛假设天数",jiashe)
    gailv1 = [round(i / sumjiashe, 4) if sumjiashe != 0 else 0 for i in jiashe]
    # print("斯洛假设概率=斯洛假设天数/除以总数",gailv1)
    # print("============================================")
    jiashe = list(map(lambda x, y, z: x + y + z, a, Mlist, Plist))
    sumjiashe = sum(jiashe)
    # print("斯洛假设天数*",jiashe)
    gailv2 = [round(i / sumjiashe, 4) if sumjiashe != 0 else 0 for i in jiashe]

    return ((
            json.dumps(shouwei), json.dumps(Glist), json.dumps(Hlist), json.dumps(Ilist), json.dumps(Jlist), str(K_one),
            json.dumps(list_result), json.dumps(gailv1), json.dumps(gailv2),json.dumps(a_sort),), Hlist,)


def su_stocks_relevance_stocks_determination(percentlist):
    avg = '11.11'
    ben_l1 = ['30.10', '17.60', '12.50', '9.70', '7.90', '6.70', '5.80', '5.10', '4.60']
    SS_tot = 0
    SS_res = 0
    SS_tot_ben = 0
    fen_zi = 0
    for a in range(1, 10):
        # print(count_info)
        percent = percentlist[a - 1]
        # print(str(a), percent)
        # percent_sum += decimal.Decimal(percent)
        SS_tot += (decimal.Decimal(percent) - decimal.Decimal(avg)) ** 2
        SS_tot_ben += (decimal.Decimal(percent) - decimal.Decimal(avg)) ** 2
        SS_res += (decimal.Decimal(percent) - decimal.Decimal(ben_l1[a - 1])) ** 2
        fen_zi += (decimal.Decimal(percent) - decimal.Decimal(avg)) * (
                decimal.Decimal(ben_l1[a - 1]) - decimal.Decimal(avg))
    fen_mu = math.sqrt(SS_tot_ben * SS_tot)
    stocks_determination = round(1 - SS_res / SS_tot, 4)
    stocks_relevance = round(fen_zi / decimal.Decimal(fen_mu), 4)
    return (stocks_determination, stocks_relevance)

#
# @router.post("/verf_base_info", summary="验证系统基本信息")
# async def verf_base_info(bp: VerificatReq) -> Any:
#     try:
#         mk=bp.mk
#         code=bp.code
#         Input_method=bp.Input_method
#         input_costs= bp.input_costs
#         from_date=bp.from_date
#         dead_date=bp.dead_date
#
#         conn = Tortoise.get_connection("default")
#         row=await StockA.filter(stock_code=code).count()
#         sql = f"""select stock_code, data_time,stock_open,stock_close,stock_open_after,stock_close_after,stock_ChangeAmount from stock_a_info where stock_code='{code}';"""
#         #print(sql)
#         t = await conn.execute_query_dict(sql)
#         sql = f"""select stock_code, ex_div_date,split_ratio,per_share_div_ratio,per_share_trans_ratio,allotment_ratio,allotment_price,per_cash_div from stock_a_rehab where stock_code='{code}';"""
#         rehab = await conn.execute_query_dict(sql)
#         ex_div_date=[]
#         split_ratio=[]
#         per_share_div_ratio=[]
#         per_share_trans_ratio=[]
#         allotment_ratio=[]
#         allotment_price=[]
#         per_cash_div=[]
#         for reh in rehab:
#             ex_div_date.append(reh[1])
#             split_ratio.append(reh[2])
#             per_share_div_ratio.append(reh[3])
#             per_share_trans_ratio.append(reh[4])
#             allotment_ratio.append(reh[5])
#             allotment_price.append(reh[6])
#             per_cash_div.append(reh[7])
#         AC = 100
#         # print(t)
#         insertsqllist = []
#         C = []  # 收盘列表
#         D = []  # 开盘价列表
#         E = []  # 涨跌幅列表
#         F = []  # 实际首位列表
#         G = []  # 实际二位列表
#         G1 = []  # 第二位判断后列表
#         C1 = []  # 后复权收盘列表
#         ex_div_date_list=[]
#         split_ratio_list=[]
#         per_share_div_ratio_list=[]
#         per_share_trans_ratio_list=[]
#         allotment_ratio_list=[]
#         allotment_price_list=[]
#         per_cash_div_list=[]
#         a =        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 1~9 ,sum#当前1~9，sum的列表
#         a_second = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]  # 0~9 ,sum#当前1~9，sum的列表
#         a_third = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]  # 0~9 ,sum#当前1~9，sum的列表
#         a_fourth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]  # 0~9 ,sum#当前1~9，sum的列表
#         a_fifth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]  # 0~9 ,sum#当前1~9，sum的列表
#         ben_l = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
#         Probability_of_Big_First = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 出现大首位概率列表
#
#         jindu = {
#             1: 0, 2: 40, 3: 80, 4: 120, 5: 160, 6: -160, 7: -120, 8: -80, 9: -40
#         }
#         countdata = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, "sum": 0}
#         countloop = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, "sum": 0}  # 用来识别是否一个循环
#         loopindex = 0  # 循环次数
#         CycleTime = []
#         nn = 0
#         m_ball = 0
#         L_ball = 0
#         t_ball = 0
#         last_loop_days = 0  # 初始化第一次循环结束的天数
#         stock_code = 0
#         data_time = 0
#         for i in t:
#
#             stock_open = float(i[2])  # 开盘价
#             stock_close = float(i[3])  # 收盘价
#             stock_open_after = float(i[4])  # 后复权开盘价
#             stock_close_after = float(i[5])  # 后复权收盘价
#             first, second,third,fourth,fifth = first_second_list(i[3])  # 首位，二位,三位，四位
#             if first == 0:
#                 continue
#             #//判断若当日涨跌额（ChangeAmount)的绝对值在0到9区间内，用第一种判断
#             #  若当日涨跌额（ChangeAmount)的绝对值在10到99区间内，用第二种判断
#             # 若当日涨跌额（ChangeAmount)的绝对值在100到999区间内，用第三种判断
#             a_second[second] += 1
#             a_second[-1] += 1
#             a_third[third] += 1
#             a_third[-1] += 1
#             a_fourth[fourth] += 1
#             a_fourth[-1] += 1
#             changeamount=math.fabs(float(i[-1]))
#             second2=second
#             if 0<=changeamount <10:
#                 pass
#             elif 10<=changeamount <100:#第二种
#                 second2=judp_third_fourth_fifth(third, second, a_second[second], a_second[-1])
#             elif 100<=changeamount <1000:#第三种
#                 third2=judp_third_fourth_fifth(fourth, third, a_third[third], a_third[-1])
#                 second2=judp_third_fourth_fifth(third2, second, a_second[second], a_second[-1])
#             else:#第四种
#                 fourth2=judp_third_fourth_fifth(fifth, fourth, a_fourth[fourth], a_fourth[-1])
#                 third2=judp_third_fourth_fifth(fourth2, third, a_third[third], a_third[-1])
#                 second2=judp_third_fourth_fifth(third2, second, a_second[second], a_second[-1])
#
#             C.append(stock_close)
#             D.append(stock_open)
#             E.append(float(i[-1]))
#             F.append(first)
#             G.append(second)
#             C1.append(stock_close_after)
#             G1.append(second2)
#             ex_div_date_list.append(( ex_div_date.pop(0) if i[1] in ex_div_date else None))
#             split_ratio_list.append(( split_ratio.pop(0) if i[1] in ex_div_date else None))
#             per_share_div_ratio_list.append((per_share_div_ratio.pop(0) if i[1] in ex_div_date else None))
#             per_share_trans_ratio_list.append(( per_share_trans_ratio.pop(0) if i[1] in ex_div_date else None))
#             allotment_ratio_list.append(( allotment_ratio.pop(0) if i[1] in ex_div_date else None))
#             allotment_price_list.append(( allotment_price.pop(0) if i[1] in ex_div_date else None))
#             per_cash_div_list.append(( per_cash_div.pop(0) if i[1] in ex_div_date else None))
#             shouwei = [0, 0, 0, 0, 0, 0, 0, 0, 0]
#             a[first - 1] += 1
#             a[-1] += 1
#             shouwei[first - 1] = 1
#             result_sut = sut(a, shouwei)  # 带入函数求斯洛概率和概率*
#             result = result_sut[0]
#             # ====================计算当前时间段相关性和判定系数
#             percentlist100 = [p / a[9] * 100 for p in a[:9:]]  # 乘100用于计算
#             percentlist = [round(p / a[9], 4) for p in a[:9:]]
#             relevance_stocks_determination = su_stocks_relevance_stocks_determination(percentlist100)
#             rate_lilun = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]  # 理论概率列表
#             Probability_of_Big_First[first - 1] += 1 if percentlist[first - 1] > rate_lilun[
#                 first - 1] else 0  # 出现大首位概率列表，最后概率需要每个数/总数
#             result = (i[0], i[1], str(a[-1]), json.dumps(a[:9:]), json.dumps(percentlist),
#                       json.dumps(Probability_of_Big_First),) + result + relevance_stocks_determination
#             # =============================================================合并ball
#             stock_code = i[0]
#             data_time = i[1]
#             if nn < 1:
#                 CycleTime = []
#                 CycleTime.append(data_time)
#                 nn += 1
#             countdata[first] += 1  # 个数
#             countdata['sum'] += 1  # 个数
#             if countloop[first] == 0:
#                 countloop['sum'] += 1
#             countloop[first] += 1  # 循环
#             y = jindu[first]  # 经度东经0，西经-0，北纬-90   南纬s  90
#             x = countdata[first]
#             tup1 = [x, y, first]
#             if countloop['sum'] == 9:
#                 countloop = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, "sum": 0}
#                 loopindex += 1
#                 CycleTime.append(data_time)
#                 CycleTime_show = CycleTime
#                 nn = 0
#                 loop_days = countdata['sum'] - last_loop_days  # 两次循环天数的差
#                 if loop_days / row == 1:
#                     m_ball = 0
#                     L_ball = 0
#                     t_ball = 0
#                 else:
#                     m_ball = round(9 / (1 - (loop_days / row) ** 2) ** 0.5, 2)
#                     L_ball = round(1 * (1 - (loop_days / row) ** 2) ** 0.5, 2)
#                     t_ball = round(1 / (1 - (loop_days / row) ** 2) ** 0.5, 2)
#                     last_loop_days = countdata['sum']
#             junfei = 180 / max(countdata.values())  # 选择最大个数的首位作为均分单位操作，180/个数
#             countlist = [i for i in countdata.items()]
#             list_show = [round(-90 + tup1[0] * junfei, 2), tup1[1], tup1[2]]
#             if loopindex == 0:
#                 CycleTime_show = ""
#             result1 = (loopindex, str(CycleTime_show), m_ball, L_ball, t_ball, str(list_show))
#             # =============================================================合并ball
#             # =============================================================合并第二位数据
#             # a_second[second] += 1
#             # a_second[-1] += 1
#             Classicalprobability = 0.1 * a_second[-1]  # 古典概率
#             accuracy_rate = [round((10 - i) / a_second[i], 4) if a_second[i] != 0 else 0 for i in
#                              range(10)]  # 速率（首位单位/天
#             stock_jlist = [round(1 / i, 4) if i != 0 else 0 for i in accuracy_rate]  # 变动1单位个数（天）
#             xx = sum([Classicalprobability - i for i in a_second[:10:] if i <= Classicalprobability])
#             sum_rate = round(10 / xx if xx != 0 else 0, 4)  # 总速率（首位单位/天）
#             result2 = (json.dumps(a_second[:10:]), json.dumps(accuracy_rate), json.dumps(stock_jlist), str(sum_rate))
#
#             result_all = result + result2 + result1
#
#             # =============================================================合并第二位数据
#
#             insertsqllist.append(result_all)
#         # ==========数据聚合
#         print("长度",len(C),len(D))
#         H, I, J, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, AA, AB, S_all, T_all, W_all, X_all, AB_all, AC_all, AE, AF,AE1,AF1,point,AE1_all,AF1_all,AG,AH,AI = last_SU(
#             C, D,E, F, G, AC,C1,G1,ex_div_date_list,split_ratio_list,per_share_div_ratio_list,per_share_trans_ratio_list,allotment_ratio_list,allotment_price_list,per_cash_div_list)  # 计算
#         list1 = list(map(
#             lambda C, D, F, G, H, I, J, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, AA, AB, S_all, T_all, W_all, X_all,
#                    AB_all, AC_all, AE, AF,AE1,AF1,point,AE1_all,AF1_all,AG,AH,AI: (
#             C, D, F, G, H, I, J, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, AA, AB, S_all, T_all, W_all, X_all,
#             AB_all, AC_all, AE, AF,AE1,AF1,point,AE1_all,AF1_all,AG,AH,AI), C, D, F, G, H, I, J, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, AA, AB, S_all,
#             T_all, W_all, X_all, AB_all, AC_all, AE, AF,AE1,AF1,point,AE1_all,AF1_all,AG,AH,AI))
#         last_insert_list = list(map(lambda x, y: x + y, insertsqllist, list1))
#         result = await conn.execute_query_dict(sql)
#         return generate_response(data=result)
#
#     except Exception as e:
#         logger.error(traceback.format_exc())
#         await TbMessage.create( type=4, content=str(e))
#
#         return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/stock_research", summary="股票模糊查询接口")
async def zz(request: Request,bp: StocckSearchReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        code = bp.code  # 股票模糊
        limit = bp.page_size
        offset = bp.page_size * (bp.page - 1)
        conn = Tortoise.get_connection("default")
        if market.lower()=="cn":
            sql = f"""SELECT  *  FROM  stock_code  WHERE  stock_code like '%{code}%' and stock_market= "SZ&SH"   LIMIT {limit} offset {offset}"""

        elif market.lower()=="hk":
            sql = f"""SELECT  *  FROM  stock_code  WHERE  stock_code like '%{code}%' and stock_market= "HK"   LIMIT {limit} offset {offset}"""

        else:
            sql = f"""SELECT  *  FROM  stock_code  WHERE  stock_code like '%{code}%' and stock_market= "US"   LIMIT {limit} offset {offset}"""


        #print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

@router.post("/intraday_trend", summary="日内趋势")
async def Intradaytrend(bp: SearchMinuteReq) -> Any:
    try:
        from datetime import timedelta
        market = bp.mk  # 市场来源
        code = bp.code  # 市场来源
        if market=="us":
            beginime = datetime(bp.choose_date.year, bp.choose_date.month, bp.choose_date.day, 21,
                                30) - timedelta(days=1)
            endtime = datetime(bp.choose_date.year, bp.choose_date.month, bp.choose_date.day, 5, 0)
            data = await Stockcnperminute5Excelus.filter(stock_code=code, data_time__range=(beginime, endtime)).values("data_time","n","o","p")
            if not data:
                last_data = await Stockcnperminute5Excelus.filter(stock_code=code).limit(1).order_by("-id").values("data_time")
                beginime = datetime(last_data[0]['data_time'].year, last_data[0]['data_time'].month, last_data[0]['data_time'].day, 21,
                                    30) - timedelta(days=1)
                endtime = datetime(last_data[0]['data_time'].year, last_data[0]['data_time'].month, last_data[0]['data_time'].day, 5, 0)
                if last_data:
                    data = await Stockcnperminute5Excelus.filter(stock_code=code,  data_time__range=(beginime, endtime)).values("data_time",
                                                                                                           "n", "o",
                                                                                                           "p")
        elif market=="hk":
            data = await Stockcnperminute5Excelhk.filter(stock_code=code,data_time__year=bp.choose_date.year,data_time__month=bp.choose_date.month,data_time__day=bp.choose_date.day).values("data_time","n","o","p")
            if not data:
                last_data = await Stockcnperminute5Excelhk.filter(stock_code=code).limit(1).order_by("-id").values("data_time")
                if last_data:
                    data = await Stockcnperminute5Excelhk.filter(stock_code=code, data_time__year=last_data[0]['data_time'].year,
                                                                 data_time__month=last_data[0]['data_time'].month,
                                                                 data_time__day=last_data[0]['data_time'].day).values("data_time",
                                                                                                           "n", "o",
                                                                                                           "p")

                    # print(data.as_query())
        else:
            # data =  Stockcnperminute5Excelcn.filter(stock_code=code,data_time=bp.choose_date.date()).values("n","o","p").as_query()
            data =await  Stockcnperminute5Excelcn.filter(stock_code=code,data_time__year=bp.choose_date.year,data_time__month=bp.choose_date.month,data_time__day=bp.choose_date.day).values("data_time","n","o","p")
            if not data:
                last_data = await Stockcnperminute5Excelcn.filter(stock_code=code).limit(1).order_by("-id").values(
                    "data_time")
                if last_data:
                    data = await Stockcnperminute5Excelcn.filter(stock_code=code,
                                                                 data_time__year=last_data[0]['data_time'].year,
                                                                 data_time__month=last_data[0]['data_time'].month,
                                                                 data_time__day=last_data[0]['data_time'].day).values(
                        "data_time",
                        "n", "o",
                        "p")
        return generate_response(data=data)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))
@router.post("/ktrend", summary="日K趋势")
async def Ktrend(bp: SearchMinuteReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        code = bp.code  # 市场来源
        if market=="us":
            data = await StockperdaysExcelus.filter(stock_code=code).values("data_time","n","o","p")

        elif market=="hk":
            data = await StockperdaysExcelhk.filter(stock_code=code).values("data_time","n","o","p")

        else:
            # data =  Stockcnperminute5Excelcn.filter(stock_code=code,data_time=bp.choose_date.date()).values("n","o","p").as_query()
            data =await  StockperdaysExcelcn.filter(stock_code=code).values("data_time","n","o","p")
            print(data)

        return generate_response(data=data)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

@router.post("/lifeline", summary="生命线")
async def Lifeline(bp: SearchMinuteReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        code = bp.code  # 市场来源
        if market=="us":
            data = await StockperdaysExcelus.filter(stock_code=code).values("data_time","ac")

        elif market=="hk":
            data = await StockperdaysExcelhk.filter(stock_code=code).values("data_time","ac")

        else:
            # data =  Stockcnperminute5Excelcn.filter(stock_code=code,data_time=bp.choose_date.date()).values("n","o","p").as_query()
            data =await  StockperdaysExcelcn.filter(stock_code=code).values("data_time","ac")
            # print(data)
        return generate_response(data=data)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/buy_list", summary="买入列表")
async def UserlibraryDetail(request: Request,bp: SearchReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        from_date=bp.from_date
        dead_date=bp.dead_date
        bp.page_size=20
        limit = bp.page_size
        offset = bp.page_size * (bp.page - 1)
        conn =  Tortoise.get_connection("default")
        if market=="cn":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_a_rate a RIGHT JOIN stock_code  b  ON a.stock_code=b.stock_code WHERE  L_last= "BUY" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        elif market=="hk":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_hk_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  L_last= "BUY" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        else:
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_us_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  L_last= "BUY" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

"""

10.算法收益>0:S_all>0的代码（标记复投)，W_all>0的代码(标记单投)，单投优先显示
11.单投>持有列表:AE1_ALL>0的代码;
12.复投>持有列表:AF1_ALL>0的代码。
以下数据来自: stock_combin表。
1.组合折线图: protfolio_yield列;
2.熔断个数折线图: up_down_negative_na列; 
3.最下方列表:(先把以上接口完成，最后再说)"""
@router.post("/hold_list", summary="持有列表")
async def UserlibraryDetail1(request: Request,bp: SearchReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        from_date=bp.from_date
        dead_date=bp.dead_date
        bp.page_size=20

        limit = bp.page_size
        offset = bp.page_size * (bp.page - 1)
        conn = Tortoise.get_connection("default")
        if market=="cn":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_a_rate a RIGHT JOIN stock_code  b  ON a.stock_code=b.stock_code WHERE  M_last= "HOLD" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}' """

        elif market=="hk":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_hk_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  M_last= "HOLD" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}' """

        else:
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_us_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  M_last= "HOLD" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'   """

        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

@router.post("/sell_list", summary="卖出列表")
async def UserlibraryDetail2(request: Request,bp: SearchReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        from_date=bp.from_date
        dead_date=bp.dead_date
        bp.page_size=20

        limit = bp.page_size
        offset = bp.page_size * (bp.page - 1)
        conn = Tortoise.get_connection("default")
        if market=="cn":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_a_rate a RIGHT JOIN stock_code  b  ON a.stock_code=b.stock_code WHERE  O= "SELL" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        elif market=="hk":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_hk_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  O= "SELL" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        else:
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_us_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  O= "SELL" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """
        print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

@router.post("/no_trading_list", summary="不交易列表")
async def UserlibraryDetail3(request: Request,bp: SearchReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        from_date=bp.from_date
        dead_date=bp.dead_date
        bp.page_size=20

        limit = bp.page_size
        offset = bp.page_size * (bp.page - 1)
        conn = Tortoise.get_connection("default")
        if market=="cn":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_a_rate a RIGHT JOIN stock_code  b  ON a.stock_code=b.stock_code WHERE L_last="N/A" AND    M_last="N/A" AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        elif market=="hk":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_hk_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  L_last="N/A" AND    M_last="N/A"  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        else:
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_us_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  L_last="N/A" AND    M_last="N/A"  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        #print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/hold_gte_list", summary="持有收益>0")
async def UserlibraryDetail5(request: Request,bp: SearchReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        from_date=bp.from_date
        dead_date=bp.dead_date
        bp.page_size=20
        limit = bp.page_size
        offset = bp.page_size * (bp.page - 1)
        conn = Tortoise.get_connection("default")
        if market=="cn":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_a_rate a RIGHT JOIN stock_code  b  ON a.stock_code=b.stock_code WHERE AB_all>0 AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}' """

        elif market=="hk":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_hk_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE AB_all>0  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'   """

        else:
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_us_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  AB_all>0  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'   """

        print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

@router.post("/algorithm_gte_list", summary="算法收益>0")
async def UserlibraryDetail6(request: Request,bp: SearchReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        from_date=bp.from_date
        dead_date=bp.dead_date
        bp.page_size=20
        limit = bp.page_size
        offset = bp.page_size * (bp.page - 1)
        conn = Tortoise.get_connection("default")
        if market=="cn":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_a_rate a RIGHT JOIN stock_code  b  ON a.stock_code=b.stock_code WHERE W_all>0 AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}' """

        elif market=="hk":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_hk_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE W_all>0  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}' """

        else:
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_us_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  W_all>0 AND    M_last="N/A"  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        #print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

@router.post("/singo_gte_list", summary="单投>持有列表")
async def UserlibraryDetail7(request: Request,bp: SearchReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        from_date=bp.from_date
        dead_date=bp.dead_date
        bp.page_size=20

        limit = bp.page_size
        offset = bp.page_size * (bp.page - 1)
        conn = Tortoise.get_connection("default")
        if market=="cn":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_a_rate a RIGHT JOIN stock_code  b  ON a.stock_code=b.stock_code WHERE AE1_ALL>0 AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        elif market=="hk":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_hk_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE AE1_ALL>0  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        else:
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_us_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE  AE1_ALL>0 AND    M_last="N/A"  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        #print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

@router.post("/double_gte_list", summary="复投>持有列表")
async def UserlibraryDetail8(request: Request,bp: SearchReq) -> Any:
    try:
        market = bp.mk  # 市场来源
        from_date=bp.from_date
        dead_date=bp.dead_date
        bp.page_size=20

        limit = bp.page_size
        offset = bp.page_size * (bp.page - 1)
        conn = Tortoise.get_connection("default")
        if market=="cn":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_a_rate a RIGHT JOIN stock_code  b  ON a.stock_code=b.stock_code WHERE AF1_ALL>0 AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        elif market=="hk":
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_hk_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE AF1_ALL>0  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'  """

        else:
            sql = f"""SELECT  DISTINCT(b.stock_code),b.stock_name  FROM  stock_us_rate a RIGHT JOIN stock_code b  ON a.stock_code=b.stock_code WHERE AF1_ALL>0 AND    M_last="N/A"  AND  a.data_time BETWEEN '{from_date}' AND '{dead_date}'   """

        #print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))



@router.post("/combin/show", summary="组合列表")
async def UserlibraryDetail9(request: Request) -> Any:
    try:
        conn = Tortoise.get_connection("default")
        sql = f"""SELECT  * FROM stock_combin_name;"""

        #print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))
@router.get("/protfolio_yield_list", summary="组合折线图: protfolio_yield列")
async def UserlibraryDetail91(combin_id:int) -> Any:
    try:

        obj = await   StockCombin.filter(combin_id=combin_id).order_by("-id").first()
        obj_old = await StockCombin.filter(combin_id=combin_id).first()
        combin_list =await StockCombinList.filter(stock_combin_id=combin_id)
        count1 = await StockCombinList.filter(stock_combin_id=combin_id).count()
        first_time = obj_old.data_time
        last_time = obj.data_time
        all_indus = await StockCode.filter(stock_code__in=combin_list).count()
        technology =await StockCode.filter(stock_industry__icontains="科技", stock_code__in=combin_list).count()
        advertise =await StockCode.filter(stock_industry__icontains="广告", stock_code__in=combin_list).count()
        medical =await StockCode.filter(stock_industry__icontains="医疗", stock_code__in=combin_list).count()
        protfolio_yield_list=  await StockCombin.filter(combin_id=combin_id).values("portfolio_yield","data_time")
        combin_list_content=  await StockCombinList.filter(stock_combin_id=combin_id).values()#该组合下所有的股票代码列表

        data={"input_costs":obj.input_costs,"portfolio_profit_and_loss":obj.portfolio_profit_and_loss,"portfolio_yield":obj.portfolio_yield,"portfolio_equity":obj.portfolio_equity,"count":count1,"first_time":first_time,"last_time":last_time,"all_indus":all_indus,
                         "technology":technology,"advertise":advertise,"medical":medical,"protfolio_yield_list":protfolio_yield_list,"combin_list_content":combin_list_content}
        return generate_response(data=data)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))






@router.get("/Fuse_list", summary="熔断个数折线图cc=1是两年内统计，cc=2该组合的所有，cc=0所有组合的统计")
async def UserlibraryDetail3(request: Request,cc:int,combin:int=0) -> Any:
    try:

        conn = Tortoise.get_connection("default")
        if cc==1:
            sql = f"""SELECT DATE_FORMAT(data_time,'%Y%m') as time,sum(up_down_negative_na)  ud FROM stock_combin where DATE_SUB(CURDATE(), INTERVAL 2 YEAR) <= date(data_time) AND combin_id ={combin}  GROUP BY  time   """  # 两年内统计

        elif cc==2:
            sql = f"""SELECT DATE_FORMAT(data_time,'%Y%m') as time,sum(up_down_negative_na)  ud FROM stock_combin where combin_id ={combin} GROUP BY  time   """  # 上市其
        else:#所有合并
            return generate_response(data=None)


        #print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))
        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


from openpyxl import load_workbook


@router.post("/upload_stock", summary="批量上传股票")
async def UserlibraryDetail3(excelfile: UploadFile = File(..., description="使用form表单上传文件")) -> Any:
    try:
        # 如果是上传的文件，则可以直接从上传的files中提取，不在本地保存
        # FastApi文件上传 files: UploadFile  = File(...),
        result = {"type": "import"}
        if excelfile:
            excel_tool = ExcelTools()

            filename = excelfile.filename
            ext = filename.split('.')[-1].replace('"', '')

            if ext not in ['xls', 'xlsx']:
                result.update({
                    "status": "failed",
                    "msg": "can't parse file format"
                })
                return result

            parsed_dict = excel_tool.excel_to_dict(excelfile.file.read())
            result.update({
                "file_name": filename,
                "data": parsed_dict
            })
            async with in_transaction(connection_name="default"):
                for i in parsed_dict:
                     await StockCode.update_or_create(defaults=dict(stock_name=i['名称'],), stock_code=i['代码'])
                return generate_response(result)
        return generate_response(result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create(type=4, content=str(e))
        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/update_combin", summary="更新该组合")
async def UserlibraryDetailupdatecombin( combin_id: int = Form(...),excelfile: UploadFile = File(..., description="使用form表单上传文件")) -> Any:
    try:
        # 如果是上传的文件，则可以直接从上传的files中提取，不在本地保存
        # FastApi文件上传 files: UploadFile  = File(...),
        if not  combin_id:
            return ResultResponse[str](code=HttpStatus.HTTP_422_QUERY_PARAM_EXCEPT, message='参数错误', data=None)

        result = {"type": "import"}
        if excelfile:
            excel_tool = ExcelTools()

            filename = excelfile.filename
            ext = filename.split('.')[-1].replace('"', '')

            if ext not in ['xls', 'xlsx']:
                result.update({
                    "status": "failed",
                    "msg": "can't parse file format"
                })
                return result

            parsed_dict = excel_tool.excel_to_dict(excelfile.file.read())
            result.update({
                "file_name": filename,
                "data": parsed_dict
            })
            market=await  StockCombinName.filter(id=combin_id).first()
            async with in_transaction(connection_name="default"):
                for i in parsed_dict:
                    stock_code=str(i['代码'])
                    stock_code= stock_code.zfill(6) if market.mk=="CN" else (stock_code.zfill(5) if market.mk=="HK" else  stock_code)
                    await StockCombinList.update_or_create(defaults=dict(stock_hold=i['投入方式'],from_mk=market.mk), stock_code=stock_code,stock_combin_id=combin_id)

                return generate_response(result)
        return generate_response(result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create(type=4, content=str(e))
        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))




@router.get("/combin/list", summary="组合列表完整")
async def UserlibraryDetai20(request: Request) -> Any:
    try:
        conn = Tortoise.get_connection("default")
        sql = f"""SELECT  a.*,b.* FROM  stock_combin_name a LEFT JOIN  stock_combin_list b ON a.id=b.stock_combin_id;"""

        #print(sql)
        result = await conn.execute_query_dict(sql)
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))





@router.post("/combin_list_delete", summary="组合列表中删除组合,请勿随便删除组合")
async def UserlibraryDetail3(stock_combin_id: int) -> Any:
    try:
        async with in_transaction(connection_name="default"):

             await StockCombinName.filter(id=stock_combin_id).delete()
             await StockCombinList.filter(stock_combin_id=stock_combin_id).delete()
             return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create(type=4, content=str(e))
        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))



@router.get("/stock_minute", summary="2023.2.9新更新接口,x，圆，方框，三角形 四种图形 view_type==1,2,3,4")
async def StockMinute2(user_id: int,view_type :int, mk: str="US", code : str="AXP", endtime :str=str(datetime.now())) -> Any:
    ret = {}

    from datetime  import  datetime,timedelta
    from tortoise.expressions import F as FCC
    try:
        endtime = endtime.split(" ")[0]
        if mk == "US" or mk == "us":
            timekey = datetime.strptime(endtime, "%Y-%m-%d")
            beginime = datetime(timekey.year, timekey.month, timekey.day, 21, 30)
            endtime = datetime(timekey.year, timekey.month, timekey.day, 5, 0) + timedelta(days=1)
            obj_count =await Stockusperminute1.filter(stock_code=code, data_time__range=(beginime, endtime)).count()
            # obj1 =await Stockusperminute1.filter(stock_code=code, data_time__range=(beginime, endtime)).order_by("id").values()
            I1 = 100
            stock_v = 390
            if obj_count == 0:  # 今天的数据没有的话，显示昨天的
                last_us = await Stockusperminute1.filter(stock_code=code,data_time__lt=beginime).order_by("-id").first()
                beginime = datetime(last_us.data_time.year, last_us.data_time.month, last_us.data_time.day, 21,
                                    30) - timedelta(days=1)
                endtime = datetime(last_us.data_time.year, last_us.data_time.month, last_us.data_time.day, 5, 0)
            obj1 =await Stockusperminute1.filter(stock_code=code, data_time__range=(beginime, endtime)).values()
        elif mk == "HK" or mk == "hk":
            timekey = datetime.strptime(endtime, "%Y-%m-%d")
            beginime = datetime(timekey.year, timekey.month, timekey.day, 9, 30)
            endtime = datetime(timekey.year, timekey.month, timekey.day, 16, 0)
            obj_count =await Stockhkperminute1.filter(stock_code=code, data_time__range=(beginime, endtime)).count()
            I1 = 100
            stock_v = 390
            if obj_count == 0:  # 今天的数据没有的话，显示昨天的
                last_time = await Stockhkperminute1.filter(stock_code=code).order_by("-id").first()
                last_us=last_time.data_time
                beginime = datetime(last_us.year, last_us.month, last_us.day, 9, 30)
                endtime = datetime(last_us.year, last_us.month, last_us.day, 16, 0)
            obj1 =await Stockhkperminute1.filter(stock_code=code, data_time__range=(beginime, endtime)).values()
        else:
            return ResultResponse[str](code=HttpStatus.HTTP_422_QUERY_PARAM_EXCEPT, message='fail', data="错误mk参数")

        B = [i  for i in range(len(obj1))]
        C = [float(i["stock_close"]) for i in obj1]
        D = [float(i["stock_open"]) for i in obj1]
        F = [float(i["stock_low"]) for i in obj1]
        E = [C[0] - D[0]] + [C[i] - C[i - 1] for i in range(1, len(obj1))]

        HU,HV,IJ,KE,KF,KV,SF,SG,SU,UP,UQ,VG,XX,XY = su_us_hk(B, C, E, F, I1, stock_v)
        ret["HU"] = [{"time": obj1[i]["data_time"], "values": HU[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["HV"] = [{"time": obj1[i]["data_time"], "values": HV[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["IJ"] = [{"time": obj1[i]["data_time"], "values": IJ[i], "close": obj1[i]["stock_close"],"stock_code": IJ[i]} if IJ[i]==1 else {"time": obj1[i]["data_time"], "values": IJ[i], "close": obj1[i]["stock_close"]}  for i in range(len(obj1))]
        ret["KE"] = [{"time": obj1[i]["data_time"], "values": KE[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["KF"] = [{"time": obj1[i]["data_time"], "values": KF[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["KV"] = [{"time": obj1[i]["data_time"], "values": KV[i], "close": obj1[i]["stock_close"],"stock_code": KV[i]}   if KV[i]==1  else {"time": obj1[i]["data_time"], "values": KV[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["SF"] = [{"time": obj1[i]["data_time"], "values": SF[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["SG"] = [{"time": obj1[i]["data_time"], "values": SG[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["SU"] = [{"time": obj1[i]["data_time"], "values": SU[i], "close": obj1[i]["stock_close"],"stock_code": SU[i]} if SU[i]==1 else {"time": obj1[i]["data_time"], "values": SU[i], "close": obj1[i]["stock_close"]}  for i in range(len(obj1))]
        ret["UP"] = [{"time": obj1[i]["data_time"], "values": UP[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["UQ"] = [{"time": obj1[i]["data_time"], "values": UQ[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["VG"] = [{"time": obj1[i]["data_time"], "values": VG[i], "close": obj1[i]["stock_close"],"stock_code": VG[i]} if VG[i]==1  else  {"time": obj1[i]["data_time"], "values": VG[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["XX"] = [{"time": obj1[i]["data_time"], "values": XX[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        ret["XY"] = [{"time": obj1[i]["data_time"], "values": XY[i], "close": obj1[i]["stock_close"]} for i in range(len(obj1))]
        all_vlues=await Stockcnperminute1ExcelCheck.filter(stock_mk=mk).first()
        all_kv=all_vlues.kv
        all_vg=all_vlues.vg
        all_ij=all_vlues.ij
        all_su=all_vlues.su
        ret["KV_CODE"]=json.loads(all_kv)   if   all_kv    else    all_kv
        ret["VG_CODE"]=json.loads(all_vg)  if all_vg   else all_vg
        ret["IJ_CODE"]=json.loads(all_ij)  if   all_ij   else all_ij
        ret["SU_CODE"]=json.loads(all_su)    if all_su    else  all_su
        await  StockViewCount.create(stock_mk=mk, stock_code=code, stock_type=view_type, stock_view_count=1,add_time=datetime.now(),user_id=user_id)


        view_count =await  StockViewCount.filter(stock_code=code).first()
        ret["view_count"]=view_count.stock_view_count
        return generate_response(data=ret)
    except Exception as e:
        logger.error(traceback.format_exc())
        # await TbMessage.create(type=4, content=str(e))
        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))