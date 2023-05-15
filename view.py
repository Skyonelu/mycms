"""
URL视图处理
"""
import asyncio
import copy
import json
import ntpath
import os
import shutil
import traceback
import uuid
from collections import ChainMap
from typing import List, Any, Union, Optional
from datetime import timedelta, datetime
from fastapi import FastAPI, BackgroundTasks
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, status, HTTPException, Request, UploadFile, File, Path
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sync2asyncio import simple_run_in_executor
from tortoise import Tortoise
from tortoise.expressions import F
from tortoise.functions import Sum
from tortoise.query_utils import Q
from tortoise.transactions import in_transaction
from typing import Optional
from utils.myoss import imgUpdate
from . import crud, schema, model
from core import settings
from utils.response_code import ResultResponse, HttpStatus
from utils import logger
from utils.utils import verify_password, get_password_hash
from auth.auth import create_access_token
from auth.auth_casbin import Authority
from .model import *
from .model import TbPicture
from .schema import *
from dateutil.relativedelta import relativedelta
router = APIRouter()


@router.post("/login",
             summary="用户登录认证",
            response_model=schema.Token
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    通过用户名和密码登录获取 token 值
    :param form_data:avatar
    :return:
    """
    # 验证用户
    user = await crud.get_user_by_name(username=form_data.username)
    if not user:
        logger.info(
            f"用户名认证错误: username:{form_data.username} password:{form_data.password}"
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='username or password error')

    # 验证密码
    if not verify_password(form_data.password, user.password):
        logger.info(
            f"用户密码错误: username:{form_data.username} password:{form_data.password}"
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='username or password error')

    # 登录成功后返回token
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.username,
                                       expires_delta=access_token_expires)

    # return ResultResponse[schema.Token](result={
    #     'access_token': access_token,
    #     'token_type': 'bearer'
    # })
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/register',
             summary='用户注册',
             description='注册新用户',
             response_model=ResultResponse[model.UserOut],tags=["用户/登录"])
async def register(user: schema.UserCreate):
    user = await crud.create_user(user)
    return ResultResponse[model.UserOut](result=user)

@router.get("/info",
            summary="获取当前用户信息",
            name="获取当前用户信息",
            response_model=ResultResponse[model.UserOut])
async def get_user_info(request: Request):
    return ResultResponse[model.UserOut](result=request.state.user)
@router.post("/update_info",
            summary="管理系统的用户名修改和密码修改",
            name="管理系统的用户名修改和密码修改",
            response_model=ResultResponse[model.UserOut])
async def update_user_info(request: Request,bp: UserPasswordReq):
    password=get_password_hash(bp.password)
    await  TblUser.filter(id=request.state.user.id).update(username=bp.username,password=password)
    return ResultResponse[model.UserOut](result=request.state.user)

# @router.post("/info",
#             summary="获取当前用户信息",
#             name="获取当前用户信息",
#             response_model=ResultResponse[model.UserOut])
# async def get_user_info(request: Request):
#     return ResultResponse[model.UserOut](result=request.state.user)

# @router.get('/list',
#             summary='获取用户列表',
#             description='获取用户列表',
#             response_model=ResultResponse[List[model.UserOut]])
# async def get_user_list():
#     user_list = await crud.get_user_list()
#     return ResultResponse[List[model.UserOut]](result=user_list)

#
# @router.post('/add/role',
#              summary='添加角色',
#              name='添加角色',
#              response_model=ResultResponse[model.RoleCreate],
#              dependencies=[Depends(Authority('role,add'))])
# async def add_role(role: model.RoleOut):
#     if await crud.has_role(role.name):
#         return ResultResponse[str](code=HttpStatus.HTTP_601_ROLE_EXIST, message='角色已存在')
#
#     role = await crud.create_role(role)
#     return ResultResponse[model.RoleOut](result=role)
#
#
# @router.post('/del/role',
#              summary='删除角色',
#              name='删除角色',
#              response_model=ResultResponse[str],
#              dependencies=[Depends(Authority('role,del'))])
# async def del_role(request: Request, role_name: str):
#     result = await crud.delete_role_by_name(role_name)
#     if not result:
#         return ResultResponse[str](code=HttpStatus.HTTP_600_ROLE_NOT_EXIST, message='角色不存在')
#
#     return ResultResponse[str](message='角色已删除')


#可视化显示
@router.post('/download/point',
             summary='下载埋点,type=1下载 type=2浏览量，',
             name='下载埋点',
             response_model=ResultResponse[str])
async def download_point( type: int):

    obj, created = await Tbpoint.get_or_create(created_at__year=datetime.now().year,created_at__month=datetime.now().month,created_at__day=datetime.now().day)
    if type==1:#
        obj.download_count = F('download_count') + 1
    if type==2:
        obj.page_views = F('page_views') + 1
    await obj.save()
    return ResultResponse[str](code=HttpStatus.HTTP_200_OK, message='success')






#图库图片接口部分
#1.上传图片 2.图片列表，3.浏览排行，4.点赞排行
UPLOAD_DIRECTORY = os.getcwd()
async def run_in_process(fn):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, fn)  # wait and return result

@router.post("/image", summary="上传图片", tags=["UploadFile"])
async def image(request: Request,image: UploadFile = File(...)):
    user =request.state.user
    image_bytes = image.file.read()
    logger.info(f"用户{user.username}->上传文件:{image.filename}")
    myfilename =str(uuid.uuid1()) +image.filename
    filename = os.path.join("https://cms-img.oss-cn-shenzhen.aliyuncs.com/",myfilename)
    await simple_run_in_executor(imgUpdate, myfilename, image_bytes)
    obj=await TbPicture.create(path=filename, filename=image.filename, user_id=user.id)
    obj.sort_id=obj.id
    await obj.save()
    return generate_response(data={"filename": filename})


@router.post("/userimage_url", summary="用户上传图片接口", tags=["UploadFile"])
async def image11(image: UploadFile = File(...)):
    image_bytes = image.file.read()
    myfilename =str(uuid.uuid1()) +image.filename
    filename = os.path.join("https://cms-img.oss-cn-shenzhen.aliyuncs.com/",myfilename)
    await simple_run_in_executor(imgUpdate, myfilename, image_bytes)
    return generate_response(data={"filename": filename})

#获取图库列表
from fastapi.responses import JSONResponse, Response

def generate_response(data:Union[list, dict, str]=None, code:int=200,message:Optional[str]=None)-> Response:
    message = "200"
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "message": message,
            "code": code,
            "data": data
        }
    ))
@router.get("/showimage", summary="图片列表获取图库types=1,封面图库列表types=2")
async def UserlibraryDetail(page:int,page_size:int,types:int) -> Any:
    try:
        limit = page_size
        offset = page_size * (page - 1)
        if types==1:
            project = await TbPicture.filter(types=1).limit(limit=limit).offset(offset=offset).order_by("-sort_id").order_by("-id")
        else:
            project = await TbPicture.filter(types=2).limit(limit=limit).offset(offset=offset).order_by("-sort_id").order_by("-id")

        return generate_response(data=project)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))
@router.delete("/deleteimage", summary="删除图片")
async def UserlibraryDetail(pid:int) -> Any:
    try:
        await TbPicture.filter(id=pid).delete()
        await TbFavor.filter(pid=pid).delete()

        return generate_response(data=None)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

#浏览量买点
@router.post('/browse/point',
             summary='浏览量,点赞埋点',
             name='浏览量,点赞埋点',
             response_model=ResultResponse[str])
async def browse_point(bp: BrowsePointReq):
    obj, created = await TbPageViewRank.get_or_create(user_id=bp.user_id,type=bp.type)
    obj.count = F('count') + 1
    await obj.save()
    if bp.pic_id and bp.type==2:#当点赞图片时候，则转移图片到封面
        await TbPicture.filter(id=bp.pic_id, type=2)
    return ResultResponse[str](code=HttpStatus.HTTP_200_OK, message='success')
@router.get("/browse_ranking", summary="浏览,点赞排行，types=1浏览量，types=2点赞量",response_model=ResultResponse[str])
async def UserlibraryDetail(types : int):
    try:
        project = await TbPageViewRank.filter(type=types).values()
        # return  paginate(project)
        return generate_response(data=(project))

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


#用户浏览代码分布埋点
@router.post("/browse_code", summary="用户浏览代码分布埋点",response_model=ResultResponse[str])
async def UserBrowseCode(devicetype:str,bp: BrowseLogsReq):
    try:
        bp.devicetype= devicetype
        await TbBrowseLogs.create(**bp.dict())

        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

#订阅
from fastapi.concurrency import run_in_threadpool
async def task(bp: SubscribeReq):
    #先查出订阅所有的 codedate  code name   buy     close  AN或BC列
    allcode =await  TbSubscribe.filter(user_id=bp.user_id).values("code","mk","stock_name")
    all_name =[{mca["code"]:mca["stock_name"]} for mca in allcode]
    all_name = dict(ChainMap(*all_name))

    uscode=[ i['code']  for i in allcode if i['mk']=="US"]
    hkcode=[ i['code']  for i in allcode if i['mk']=="HK"]
    cncode=[ i['code']  for i in allcode if i['mk']=="CN"]
    data=[]
    usobj=await Stockcnperminute5Excelus.filter(stock_code__in=uscode).filter( Q(an="BUY") | Q(bc="SELL")).values("data_time","stock_code","stock_close","an","bc")
    hkobj=await Stockcnperminute5Excelhk.filter(stock_code__in=hkcode).filter( Q(an="BUY") | Q(bc="SELL")).values("data_time","stock_code","stock_close","an","bc")
    cnobj=await Stockcnperminute5Excelcn.filter(stock_code__in=cncode).filter( Q(an="BUY") | Q(bc="SELL")).values("data_time","stock_code","stock_close","an","bc")
    for i in usobj:
        buy_sell= i["an"]  if i["an"]=="BUY"   else  i["bc"]
        data.append({"data_time":i["data_time"].strftime("%m/%d/%Y, %H:%M:%S"),"stock_code":i['stock_code'],"stock_close":i['stock_close'],"stock_name":all_name[i['stock_code']],"buy_sell":buy_sell})
    for i in hkobj:
        buy_sell= i["an"]  if i["an"]=="BUY"    else  i["bc"]

        data.append({"data_time":i["data_time"].strftime("%m/%d/%Y, %H:%M:%S"),"stock_code":i['stock_code'],"stock_close":i['stock_close'],"stock_name":all_name[i['stock_code']],"buy_sell":buy_sell})
    for i in cnobj:
        buy_sell= i["an"]  if i["an"]=="BUY"   else  i["bc"]

        data.append({"data_time":i["data_time"].strftime("%m/%d/%Y, %H:%M:%S"),"stock_code":i['stock_code'],"stock_close":i['stock_close'],"stock_name":all_name[i['stock_code']],"buy_sell":buy_sell})
    await TbMessage.create(send_id=0, receive_id=bp.user_id, type=1, content=json.dumps(data, ensure_ascii=False),  send_time=datetime.now())
@router.post("/subscribe", summary="用户订阅代码",response_model=ResultResponse[str])
async def UserSubscribe(bp: SubscribeReq,# 指定参数类型为 BackgroundTasks
        background_task: BackgroundTasks):
    try:

        isexist=await TbSubscribe.filter(user_id=bp.user_id,code=bp.code).exists()
        if not isexist:
            await TbSubscribe.create(**bp.dict())

        #订阅成功后，异步发送消息订阅
        # 添加后台任务
        # 第一个参数：可调用对象，一般就是函数
        # 后面的参数：write_notification 函数所需要的参数
        # background_task.add_task(task, bp)

        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

# #订阅取消
# @router.post("/subscribe_cancel", summary="用户订阅代码取消",response_model=ResultResponse[str])
# async def UserSubscribe(id: int):
#     try:
#         await TbSubscribe.filter(id=id).delete()
#
#         return generate_response()
#
#     except Exception as e:
#         logger.error(traceback.format_exc())
#         await TbMessage.create( type=4, content=str(e))
#
#         return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

#个人信息表展示
@router.get("/fronted_info", summary="个人信息表展示,子账号列表，搜索代码，",response_model=ResultResponse[str])
async def UserFrontedInfo(id : int):
    try:
        project = await AuthUser.get_or_none(id=id)
        project1 = await UserInfo.get_or_none(user_id=id)
        project2 = await TbLoginLog.filter(user_id=id).first()
        project3 = await TbChildAccount.filter(user_id=id).values()
        #判断会员是否到期，
        if   project1.vip_dead_time =="" or project1.vip_dead_time==None:
            isvip=0
        else:
            isvip=   1      if  datetime.now()<=   (project1.vip_dead_time).replace(tzinfo=None)   else 0
        #判断ispay字段来表示，此用户从注册开始到目前时间内，存在支付成功的状态
        paystatus=await  TbOrderInfo.filter(user_id=id,pay_status="TRADE_SUCCESS").first()
        ispay= 1 if paystatus   else 0
        data={
                "email": project.email,
                "id": project.id,
                "date_joined": project.date_joined,
                "username": project.username,
                "first_login": project.date_joined,
            "is_company": project1.is_company,
            "isvip": isvip,
            "ispay": ispay,
            "actual_name": project1.actual_name,
            "user_license": project1.user_license,
            "vip_create_time": project1.vip_create_time,
            "vip_dead_time": project1.vip_dead_time,
            "license_number": project1.license_number,
            "type_of_certificate": project1.type_of_certificate,
            "phone": project1.phone,
            "avatar": project1.avatar,
            "ip": project2.ip if project2 else None,
            "ip_addr": project2.ip_addr if project2 else None,
            "the_child_account":project3
        }
        # return  paginate(project)s
        return generate_response(data=(data))

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))



#个人信息表代码按照市场查询
@router.get("/fronted_info_code", summary="个人信息表代码按照市场查询",response_model=ResultResponse[str])
async def UserFrontedInfo1(id : int,mk: str,day:int):
    try:
        conn = Tortoise.get_connection("default")
        # print(id,mk)
        if day==0:#按天查询
            sql=f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk='{mk}' and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC ;"""
        elif  day==1:#按周查询
            sql=f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk='{mk}' and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC;"""

        elif day == 2:  # 按月查询
            sql=f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk='{mk}' and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC;"""

        elif day == 3:  # 按年查询
            sql=f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk='{mk}' and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC;"""
        else:#所有
            sql=f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk='{mk}' GROUP BY(code)  ORDER BY(COUNT(id)) DESC ;"""

        print(sql)
        result = await conn.execute_query_dict(sql)
        # return  paginate(project)s
        return generate_response(data=result)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

#个人信息一日，一年，一月的搜索代码排行
@router.get("/fronted_info_code_rank", summary="个人信息一日，一年，一月的搜索代码排行",response_model=ResultResponse[str])
async def UserFrontedInfo2(id : int,day: int):
    try:
        conn = Tortoise.get_connection("default")
        # print(id,day)
        if day==0:#按天查询
            sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="cn" and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql1 = f"""SELECT   code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="hk" and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}'and mk="us" and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            result = await conn.execute_query_dict(sql)
            result1 = await conn.execute_query_dict(sql1)
            result2 = await conn.execute_query_dict(sql2)

        elif  day==1:#按周查询
            sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="cn" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql1 = f"""SELECT    code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="hk" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}'and mk="us" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            result = await conn.execute_query_dict(sql)
            result1 = await conn.execute_query_dict(sql1)
            result2 = await conn.execute_query_dict(sql2)
        elif  day==2:#按月查询
            sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="cn" and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql1 = f"""SELECT   code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="hk" and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}'and mk="us" and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            result = await conn.execute_query_dict(sql)
            result1 = await conn.execute_query_dict(sql1)
            result2 = await conn.execute_query_dict(sql2)
        elif  day==3:#按年查询
            sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="cn" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql1 = f"""SELECT   code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="hk" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}'and mk="us" and created_at>DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            result = await conn.execute_query_dict(sql)
            result1 = await conn.execute_query_dict(sql1)
            result2 = await conn.execute_query_dict(sql2)
        else:#所有
            sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="cn"  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql1 = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}'and mk="hk"  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}'and mk="us"  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
            result = await conn.execute_query_dict(sql)
            result1 = await conn.execute_query_dict(sql1)
            result2 = await conn.execute_query_dict(sql2)

        return generate_response(data={
            "cn":result,"hk":result1,"us":result2
        })

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


#个人信息表代码和登录记录分布图,订阅列表
@router.get("/fronted_info_device_subscribe", summary="个人信息中登录设备分布，订阅排名",response_model=ResultResponse[str])
async def UserFrontedInfo1(id : int):
    try:
        conn = Tortoise.get_connection("default")
        sql=f"""SELECT type,COUNT("type") as cout  FROM   tb_real_login_log where user_id='{id}'  GROUP BY "type";"""
        result = await conn.execute_query_dict(sql)
        project1 = await TbSubscribe.filter(user_id=id).values("code","stock_name","created_at","mode")
        data={

            "device_info":result,
            "subscribe":project1
        }
        # return  paginate(project)s
        return generate_response(data=data)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))



@router.post('/base/info',
             summary='基本信息，浏览量，',
             name='基本信息',
             response_model=ResultResponse[str])
async def base_info1():
    last_year= datetime.now().year-1  if datetime.now().month-1<1  else datetime.now().year
    last_month =12 if datetime.now().month-1<1 else  datetime.now().month-1
    #浏览量：按打开网页或APP计算
    login_count_all = await Tbpoint.all().annotate(page_views_sum=Sum('page_views'),sum_download=Sum("download_count")).values("page_views_sum","sum_download")#浏览量：按打开网页或APP计算
    print("总数",login_count_all)
    login_count_current = await Tbpoint.filter(created_at__year=datetime.now().year,created_at__month=datetime.now().month,created_at__day=datetime.now().day).annotate(page_views_sum=Sum('page_views'),sum_download=Sum("download_count")).values("page_views_sum","sum_download")##这个月
    print("今日",login_count_current)

    login_count_last = await Tbpoint.filter(created_at__year=(datetime.now()- timedelta(days=1)).year,created_at__month=(datetime.now()- timedelta(days=1)).month,created_at__day=(datetime.now()- timedelta(days=1)).day).annotate(page_views_sum=Sum('page_views'),sum_download=Sum("download_count")).values("page_views_sum","sum_download")##上个月

    #注册量
    member_all=await AuthUser.all().count()#所有注册
    member_current=await AuthUser.filter(date_joined__year=datetime.now().year,date_joined__month=datetime.now().month,date_joined__day=datetime.now().day).count()#当月数据
    member_last = await AuthUser.filter(date_joined__year=(datetime.now()- timedelta(days=1)).year,date_joined__month=(datetime.now()- timedelta(days=1)).month,date_joined__day=(datetime.now()- timedelta(days=1)).day).count()#上一个月数据
    #会员量
    vip_all=await UserInfo.filter(vip_dead_time__gte=datetime.now()).count()#目前为止所有会员量
    vip_current=await UserInfo.filter(vip_dead_time__gte=datetime.now().date()).count()# 到今天为止全部
    vip_current=vip_all-vip_current
    vip_last=await UserInfo.filter(vip_dead_time__gte=datetime.now().date()- timedelta(days=1)).count()#到昨天为止全部
    vip_last=vip_all-vip_last
    #收益额TRADE_SUCCESS
    order_pay_all =await  TbOrderInfo.filter(pay_status="TRADE_SUCCESS").annotate(income=Sum("order_mount")).values("income")
    order_pay_current =await  TbOrderInfo.filter(pay_status="TRADE_SUCCESS",pay_time__year=datetime.now().year,pay_time__month=datetime.now().month,pay_time__day=datetime.now().day).annotate(income=Sum("order_mount")).values("income")
    order_pay_last =await  TbOrderInfo.filter(pay_status="TRADE_SUCCESS",pay_time__year=(datetime.now()- timedelta(days=1)).year,pay_time__month=(datetime.now()- timedelta(days=1)).month,pay_time__day=(datetime.now()- timedelta(days=1)).day).annotate(income=Sum("order_mount")).values("income")
    #搜索量
    search_all = await  TbBrowseLogs.all().count()
    search_current=await TbBrowseLogs.filter(created_at__year=datetime.now().year,created_at__month=datetime.now().month,created_at__day=datetime.now().day).count()#当天数据

    search_last = await  TbBrowseLogs.filter(created_at__year=(datetime.now()- timedelta(days=1)).year,created_at__month=(datetime.now()- timedelta(days=1)).month,created_at__day=(datetime.now()- timedelta(days=1)).day).count()
    #新老用户登录分布
    conn = Tortoise.get_connection("default")
    sql = f"""SELECT DATE_FORMAT(date_joined,'%m') as time,count(id)  cout FROM auth_user where DATE_SUB(CURDATE(), INTERVAL 3 DAY) <= date(date_joined) GROUP BY  time   """#三天内统计
    sql1 = f"""SELECT DATE_FORMAT(date_joined,'%m') as time,count(id)  cout FROM auth_user where DATE_SUB(CURDATE(), INTERVAL 3 DAY) >= date(date_joined) GROUP BY  time   """#
    sql2 = f"""SELECT DATE_FORMAT(date_joined,'%m') as time,count(id)  cout FROM auth_user  GROUP BY  time   """#
    new_user = await conn.execute_query_dict(sql)#新用户统计
    old_new = await conn.execute_query_dict(sql1)  #老用户统计
    all_new = await conn.execute_query_dict(sql2)  #所有用户统计
    #搜索a，hk,us分布
    sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="cn" GROUP BY  time   """
    sql1 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="hk" GROUP BY  time   """#
    sql2 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="us" GROUP BY  time  """#
    cn = await conn.execute_query_dict(sql)#cn
    hk = await conn.execute_query_dict(sql1)  #hk
    us = await conn.execute_query_dict(sql2)  #us
    #搜索排行前10
    sql = f"""SELECT code FROM tb_browse_logs  WHERE  mk="cn" ORDER BY id DESC """
    sql1 = f"""SELECT code FROM tb_browse_logs  WHERE  mk="hk" ORDER BY id DESC"""#
    sql2 = f"""SELECT code FROM tb_browse_logs  WHERE  mk="us" ORDER BY id DESC """#
    cn20 = await conn.execute_query_dict(sql)#cn
    hk20 = await conn.execute_query_dict(sql1)  #hk
    us20 = await conn.execute_query_dict(sql2)  #us
    top20=[]
    for x in range(20):
        cc=cn20[x]["code"]  if len(cn20)>x  else None
        hh=hk20[x]["code"]  if len(hk20)>x  else None
        uu=us20[x]["code"]  if len(us20)>x  else None
        top20.append({"cn20":cc,"hk20":hh,"us20":uu})

    # 2023.02.11新加 4个算法页面 分别的搜索量
    ag1 = await StockViewCount.filter(stock_type=1).count()
    ag1_current = await StockViewCount.filter(stock_type=1,add_time__year=datetime.now().year,add_time__month=datetime.now().month,add_time__day=datetime.now().day).count()  # 当天数据
    ag1_last = await StockViewCount.filter(stock_type=1,add_time__year=datetime.now().year,add_time__month=datetime.now().month,add_time__day=(datetime.now()- timedelta(days=1)).day).count()  # 昨天数据
    # 会员量
    ag2 = await StockViewCount.filter(stock_type=2).count()
    ag2_current = await StockViewCount.filter(stock_type=2,add_time__year=datetime.now().year,add_time__month=datetime.now().month,add_time__day=datetime.now().day).count()  # 当天数据
    ag2_last = await StockViewCount.filter(stock_type=2,add_time__year=datetime.now().year,add_time__month=datetime.now().month,add_time__day=(datetime.now()- timedelta(days=1)).day).count()  # 昨天数据
    ag3 = await StockViewCount.filter(stock_type=3).count()
    ag3_current = await StockViewCount.filter(stock_type=3,add_time__year=datetime.now().year,add_time__month=datetime.now().month,add_time__day=datetime.now().day).count()  # 当天数据
    ag3_last = await StockViewCount.filter(stock_type=3,add_time__year=datetime.now().year,add_time__month=datetime.now().month,add_time__day=(datetime.now()- timedelta(days=1)).day).count()  # 昨天数据
    ag4 = await StockViewCount.filter(stock_type=4).count()
    ag4_current = await StockViewCount.filter(stock_type=4,add_time__year=datetime.now().year,add_time__month=datetime.now().month,add_time__day=datetime.now().day).count()  # 当天数据
    ag4_last = await StockViewCount.filter(stock_type=4,add_time__year=datetime.now().year,add_time__month=datetime.now().month,add_time__day=(datetime.now()- timedelta(days=1)).day).count()  # 昨天数据
    data={
        "ag1":{"ag1_all":ag1,"ag1_current":ag1_current,"ag1_last":ag1_last},"ag2":{"ag2_all":ag2,"ag2_current":ag2_current,"ag2_last":ag2_last},"ag3":{"ag3_all":ag3,"ag3_current":ag3_current,"ag3_last":ag3_last}
        ,"ag4":{"ag4_all":ag4,"ag4_current":ag4_current,"ag4_last":ag4_last},
        "login_data":{"login_count_all":login_count_all[0]["page_views_sum"],"login_count_current":login_count_current[0]["page_views_sum"],"login_count_last":login_count_last[0]["page_views_sum"]},
        "register_data":{"member_all":member_all,"member_current":member_current,"member_last":member_last},
        "vip_member":{"vip_all":vip_all,"vip_current":vip_current,"vip_last":vip_last},
        "download_count":{"download__all":login_count_all[0]["sum_download"],"download__current":login_count_current[0]["sum_download"],"download__last":login_count_last[0]["sum_download"]},
        "order_pay":{"all":int(order_pay_all[0]["income"]),"order_pay_current":order_pay_current[0]["income"],"order_pay_last":order_pay_last[0]["income"]},
        "search_count":{"search_all":search_all,"search_current":search_current,"search_last":search_last},
        #======下面是折线图
        "new_older_user":{"new_user":new_user,"old_new":old_new,"all_new":all_new},
        "dis_cn_hk_us":{"cn":cn,"hk":hk,"us":us},
        "rank_cn_hk_us":top20

    }
    return generate_response(data=data)


@router.get("/userinfolist", summary="基本信息用户列表")
async def CloudList(page:int,page_size:int) -> Any:
    try:
        limit = page_size
        offset = page_size * (page - 1)
        conn = Tortoise.get_connection("default")
        sql=f"""SELECT a.id,a.username,u.is_company,a.date_joined ,l.modified_at FROM auth_user a LEFT JOIN   user_info u   ON  a.id=u.user_id  LEFT JOIN   tb_real_login_log l ON a.id=l.user_id limit {limit} offset {offset};"""
        result = await conn.execute_query_dict(sql)
        for j in result:
            dnow=datetime.now()
            if dnow<=(j.get("date_joined")+timedelta(days=3) if j.get("date_joined")!=None else dnow):
                j.update({"is_news": 1})
            else:
                j.update({"is_news": 0})


        return generate_response(data=result)
    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return generate_response(data=str(e), code=500)


@router.get("/realtime_userlist", summary="基本信息实时列表")
async def CloudList1(page:int,page_size:int) -> Any:
    try:
        limit = page_size
        offset = page_size * (page - 1)
        conn = Tortoise.get_connection("default")
        sql=f"""SELECT u.modified_at,u.ip,u.type FROM   tb_login_log u  limit {limit} offset {offset};"""
        # print(sql)
        result = await conn.execute_query_dict(sql)
        # print(result)
        for i in result:
            if datetime.now()-i.get("modified_at")<=timedelta(days=3):
                i.update({"is_news": 1})
            else:
                i.update({"is_news": 0})

        return generate_response(data=result)
    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return generate_response(data=str(e), code=500)

#个人信息一日，一年，一月的搜索代码排行
@router.get("/new_sug", summary="2023.2.12新的四页算法浏览量分布排行",response_model=ResultResponse[str])
# @logger.catch()
async def NewSug(day: int):
    try:
        conn = Tortoise.get_connection("default")
        # print(id,day)
        # 新的算法四个，分成us，hk novity;gemini;symmetry:trinity
        sql1 = f"""SELECT   stock_code,COUNT(id) as cout  FROM   stock_view_count where  stock_mk="HK" and stock_type=1 and to_days(add_time)=to_days(now()) GROUP BY(stock_code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
        sql2 = f"""SELECT  stock_code,COUNT(id) as cout FROM   stock_view_count where  stock_mk="US" and stock_type=1 and to_days(add_time)=to_days(now()) GROUP BY(stock_code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
        result1 = await conn.execute_query_dict(sql1)
        result2 = await conn.execute_query_dict(sql2)
        sql1 = f"""SELECT   stock_code,COUNT(id) as cout  FROM   stock_view_count where  stock_mk="HK" and stock_type=2 and to_days(add_time)=to_days(now()) GROUP BY(stock_code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
        sql2 = f"""SELECT  stock_code,COUNT(id) as cout FROM   stock_view_count where  stock_mk="US" and stock_type=2 and to_days(add_time)=to_days(now()) GROUP BY(stock_code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
        result21 = await conn.execute_query_dict(sql1)
        result22 = await conn.execute_query_dict(sql2)
        sql1 = f"""SELECT   stock_code,COUNT(id) as cout  FROM   stock_view_count where  stock_mk="HK" and stock_type=3 and to_days(add_time)=to_days(now()) GROUP BY(stock_code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
        sql2 = f"""SELECT  stock_code,COUNT(id) as cout FROM   stock_view_count where  stock_mk="US" and stock_type=3 and to_days(add_time)=to_days(now()) GROUP BY(stock_code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
        result31 = await conn.execute_query_dict(sql1)
        result32 = await conn.execute_query_dict(sql2)
        sql1 = f"""SELECT   stock_code,COUNT(id) as cout  FROM   stock_view_count where  stock_mk="HK" and stock_type=4 and to_days(add_time)=to_days(now()) GROUP BY(stock_code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
        sql2 = f"""SELECT  stock_code,COUNT(id) as cout FROM   stock_view_count where  stock_mk="US" and stock_type=4 and to_days(add_time)=to_days(now()) GROUP BY(stock_code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
        result41 = await conn.execute_query_dict(sql1)
        result42 = await conn.execute_query_dict(sql2)
        return generate_response(data={
            "su_stock_type1":{"hk":result1,"us":result2},"su_stock_type2":{"hk":result21,"us":result22},"su_stock_type3":{"hk":result31,"us":result32},"su_stock_type4":{"hk":result41,"us":result42}
        })

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

# 定义一个函数，接受一个列表作为参数
def merge_time(lst):
  # 使用字典推导式，将列表中的每个元素按照时间合并为一个字典
  result = {y["time"]: sum(x["cout"] for x in lst if x.get("time") == y["time"]) for y in lst if isinstance(y, dict) and "time" in y and "cout" in y}
  # 使用列表推导式，将字典中的每个键值对转换为一个包含time和cout两个键的字典，并返回一个列表
  return [{"time": k, "cout": v} for k, v in result.items()]

def mix_sql(a,b):
    c = merge_time(sorted(a + b, key=lambda x: x["time"]))
    print(c)
    d = copy.deepcopy(c)
    e = copy.deepcopy(c)
    for i in range(len(c)):
        for j in a:
            if c[i]["time"] == j["time"]:
                if c[i]["time"] == '2023-03-27':
                    print(c[i]["cout"] - j["cout"], c[i]["cout"], j["cout"])
                d[i]["cout"] = c[i]["cout"] - j["cout"]
        for jj in b:
            if c[i]["time"] == jj["time"]:
                e[i]["cout"] = c[i]["cout"] - jj["cout"]
    return  e,d

#个人信息一日，一年，一月的搜索代码排行
@router.get("/info_code_rank", summary="基本信息一日，一年，一月的搜索代码排行",response_model=ResultResponse[str])
# @logger.catch()
async def UserFrontedInfo21(day: int,id: Optional[int] = 0):
    try:
        conn = Tortoise.get_connection("default")
        # print(id,day)
        if  id:
            sql_page_view_list2 = []
            if day == 0:  # 按天查询
                # 搜索a，hk,us分布
                sql = f"""SELECT DATE_FORMAT(created_at,'%H') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and mk="cn" and to_days(created_at)=to_days(now()) GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%H') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and  mk="hk" and to_days(created_at)=to_days(now()) GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%H') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and  mk="us" and to_days(created_at)=to_days(now()) GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="cn" and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT   code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="hk" and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}' and  mk="us" and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)
                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs where user_id='{id}' and  to_days(created_at)=to_days(now());"""  # 1天内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  # 1天内pc占比
                print(device_rate)
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d %H') as time,count(id)  cout FROM tb_browse_logs where user_id='{id}' and  to_days(created_at)=to_days(now()) GROUP BY  time   """  # 三天内统计
                sql_page_view_list1 = await conn.execute_query_dict(sql_page_view)
                print(sql_page_view)
                sql_page_view_list = [{"time": i, "cout": 0} for i in range(24)]
                index_list = list(map(lambda x: x["time"], sql_page_view_list1))
                for i in sql_page_view_list:
                    for j in sql_page_view_list1:
                        if int(j["time"][-2::]) == int(i["time"]):
                            sql_page_view_list[int(i["time"])]["cout"] = int(j["cout"])

            elif day == 1:  # 按周查询
                sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and  mk="cn" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and  mk="hk" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and  mk="us" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="cn" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT    code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="hk" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}' and  mk="us" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)
                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs where user_id='{id}' and DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(created_at);"""  # 1周内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  # 1天内pc占比
                print(device_rate)
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y/%m/%d') as time,count(id)  cout FROM tb_browse_logs where user_id='{id}' and DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(created_at) GROUP BY  time   """  # 三天内统计
                sql_page_view_list = await conn.execute_query_dict(sql_page_view)

            elif day == 2:  # 按月查询
                sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and  mk="cn" and date_sub(curdate(), INTERVAL 30 DAY) <= date(created_at) GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  user_id='{id}' and mk="hk" and date_sub(curdate(), INTERVAL 30 DAY) <= date(created_at) GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and  mk="us" and date_sub(curdate(), INTERVAL 30 DAY) <= date(created_at) GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="cn" and date_sub(curdate(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT   code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="hk" and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}' and  mk="us" and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)
                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs where user_id='{id}' and DATE_SUB(CURDATE(), INTERVAL 1 month ) <= date(created_at);"""  # 1周内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  # 1天内pc占比
                print(device_rate)
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y/%m/%d') as time,count(id)  cout FROM tb_browse_logs where user_id='{id}' and DATE_SUB(CURDATE(), INTERVAL 1 MONTH ) <= date(created_at) GROUP BY  time   """  # 三天内统计

                sql_page_view_list = await conn.execute_query_dict(sql_page_view)
            elif day == 3:  # 按年查询
                sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and  mk="cn" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR)  GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE user_id='{id}' and  mk="hk" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR)  GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  user_id='{id}' and mk="us" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR)  GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="cn" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT   code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="hk" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}' and  mk="us" and created_at>DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)
                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs where user_id='{id}' and DATE_SUB(CURDATE(), INTERVAL 1 year ) <= date(created_at);"""  # 1周内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  # 1天内pc占比
                print(device_rate)
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y/%m/%d') as time,count(id)  cout FROM tb_browse_logs where user_id='{id}' and DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) <= date(created_at) GROUP BY  time   """  # 三天内统计
                sql_page_view_list = await conn.execute_query_dict(sql_page_view)
            else:  # 所有
                sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  user_id='{id}' and mk="cn" GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  user_id='{id}' and mk="hk" GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  user_id='{id}' and mk="us" GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="cn" GROUP BY(code) ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where user_id='{id}' and  mk="hk" GROUP BY(code) ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where user_id='{id}' and  mk="us" GROUP BY(code) ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)
                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs where user_id='{id}' ;"""  # 1周内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  # 1天内pc占比
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y/%m/%d/%H') as time,count(id)  cout FROM tb_browse_logs where user_id='{id}' GROUP BY  time   """  # 三天内统计
                sql_page_view_list = await conn.execute_query_dict(sql_page_view)
        else:
            if day==0:#按天查询
                # 搜索a，hk,us分布
                sql = f"""SELECT DATE_FORMAT(created_at,'%H') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="cn" and to_days(created_at)=to_days(now()) GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%H') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="hk" and to_days(created_at)=to_days(now()) GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%H') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="us" and to_days(created_at)=to_days(now()) GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="cn" and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT   code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="hk" and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where  mk="us" and to_days(created_at)=to_days(now()) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)


                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs where to_days(created_at)=to_days(now());"""  # 1天内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  #1天内pc占比
                print(device_rate)
                last_data = datetime.now()
                beginime = datetime(last_data.year, last_data.month, last_data.day, 0, 0)
                app1=await  StockViewCount.filter(add_time__range=(beginime, last_data)).count()
                device_rate[0]["app1"]=app1
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d %H') as time,count(id)  cout FROM tb_browse_logs where to_days(created_at)=to_days(now()) GROUP BY  time   """  # 三天内统计
                sql_page_view_list1 = await conn.execute_query_dict(sql_page_view)
                print(sql_page_view_list1)
                sql_page_view2 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d %H') as time,count(id)  cout FROM stock_view_count where to_days(add_time)=to_days(now()) GROUP BY  time   """  # 三天内统计
                sql_page_view_list12 = await conn.execute_query_dict(sql_page_view2)

                sql_page_view_list=[ {"time": i,"cout": 0} for i in range(24)]
                sql_page_view_list2=[ {"time": i,"cout": 0} for i in range(24)]
                index_list=list(map(lambda x:x["time"],sql_page_view_list1))
                for i in sql_page_view_list:
                    for j in sql_page_view_list12:
                        if int(j["time"][-2::])==int(i["time"]):
                            sql_page_view_list2[int(i["time"])]["cout"]= int(j["cout"])
                for i in sql_page_view_list:
                    for j in sql_page_view_list1:
                        if int(j["time"][-2::])==int(i["time"]):
                            sql_page_view_list[int(i["time"])]["cout"]= int(j["cout"])

            elif  day==1:#按周查询
                sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="cn" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="hk" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="us" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="cn" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code) ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT    code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="hk" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where mk="us" and date_sub(curdate(), INTERVAL 7 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)
                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(created_at);"""  # 1周内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  #1天内pc占比
                print(device_rate)
                last_data = datetime.now()
                beginime = datetime(last_data.year, last_data.month, last_data.day, 0, 0) - timedelta(days=7)
                app1=await  StockViewCount.filter(add_time__range=(beginime, last_data)).count()
                device_rate[0]["app1"]=app1
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(created_at) GROUP BY  time   """  # 三天内统计
                sql_page_view_list = await conn.execute_query_dict(sql_page_view)
                sql_page_view2 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(add_time) GROUP BY  time   """  # 三天内统计
                sql_page_view_list2 = await conn.execute_query_dict(sql_page_view2)
                sql_page_view_list,sql_page_view_list2=mix_sql(sql_page_view_list, sql_page_view_list2)


            elif  day==2:#按月查询
                sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="cn" and date_sub(curdate(), INTERVAL 30 DAY) <= date(created_at) GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="hk" and date_sub(curdate(), INTERVAL 30 DAY) <= date(created_at) GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="us" and date_sub(curdate(), INTERVAL 30 DAY) <= date(created_at) GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="cn" and date_sub(curdate(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT   code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="hk" and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where  mk="us" and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(created_at) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)
                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs where DATE_SUB(CURDATE(), INTERVAL 1 month ) <= date(created_at);"""  # 1周内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  #1天内pc占比
                print(device_rate)
                last_data = datetime.now()
                beginime = datetime(last_data.year, last_data.month, last_data.day, 0, 0) - timedelta(days=30)
                app1=await  StockViewCount.filter(add_time__range=(beginime, last_data)).count()
                device_rate[0]["app1"]=app1
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs where DATE_SUB(CURDATE(), INTERVAL 1 MONTH ) <= date(created_at) GROUP BY  time   """  # 三天内统计

                sql_page_view_list = await conn.execute_query_dict(sql_page_view)
                sql_page_view2 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count where DATE_SUB(CURDATE(), INTERVAL 1 MONTH ) <= date(add_time) GROUP BY  time   """  # 三天内统计
                sql_page_view_list2 = await conn.execute_query_dict(sql_page_view2)
                sql_page_view_list,sql_page_view_list2=mix_sql(sql_page_view_list, sql_page_view_list2)


            elif  day==3:#按年查询
                sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="cn" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR)  GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="hk" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR)  GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="us" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR)  GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="cn" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT   code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="hk" and created_at >DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where  mk="us" and created_at>DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY(code)  ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)
                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs where DATE_SUB(CURDATE(), INTERVAL 1 year ) <= date(created_at);"""  # 1周内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  #1天内pc占比
                print(device_rate)
                sql11 = f"""SELECT COUNT(id) as cout FROM   stock_view_count where  add_time>DATE_SUB(CURDATE(), INTERVAL 1 YEAR) """  # 1天内单个市场的排名前20
                appp1 = await conn.execute_query_dict(sql11)
                device_rate[0]["app1"]=appp1[0]['cout']
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs where DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) <= date(created_at) GROUP BY  time   """  # 三天内统计
                sql_page_view_list = await conn.execute_query_dict(sql_page_view)
                sql_page_view2 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count where DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) <= date(add_time) GROUP BY  time   """  # 三天内统计
                sql_page_view_list2 = await conn.execute_query_dict(sql_page_view2)
                sql_page_view_list,sql_page_view_list2=mix_sql(sql_page_view_list, sql_page_view_list2)

            else:#所有
                sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="cn" GROUP BY  time   """
                sql1 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="hk" GROUP BY  time   """  #
                sql2 = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  WHERE  mk="us" GROUP BY  time  """  #
                cn = await conn.execute_query_dict(sql)  # cn
                hk = await conn.execute_query_dict(sql1)  # hk
                us = await conn.execute_query_dict(sql2)  # us
                sql = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="cn" GROUP BY(code) ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql1 = f"""SELECT  code,COUNT(id) as cout  FROM   tb_browse_logs where  mk="hk" GROUP BY(code) ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                sql2 = f"""SELECT  code,COUNT(id) as cout FROM   tb_browse_logs where  mk="us" GROUP BY(code) ORDER BY(COUNT(id)) DESC"""  # 1天内单个市场的排名前20
                result = await conn.execute_query_dict(sql)
                result1 = await conn.execute_query_dict(sql1)
                result2 = await conn.execute_query_dict(sql2)
                sqldevice = f"""select sum(if(devicetype='pc',1,0)) as pc,sum(if(devicetype='h5',1,0)) as h5 ,sum(if(devicetype='app',1,0)) as app from tb_browse_logs ;"""  # 1周内pc占比
                device_rate = await conn.execute_query_dict(sqldevice)  #1天内pc占比
                print(device_rate)
                app1=await  StockViewCount.filter().count()
                device_rate[0]["app1"]=app1
                sql_page_view = f"""SELECT DATE_FORMAT(created_at,'%Y-%m-%d') as time,count(id)  cout FROM tb_browse_logs  GROUP BY  time   """  # 三天内统计
                sql_page_view_list = await conn.execute_query_dict(sql_page_view)
                sql_page_view2 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count  GROUP BY  time   """  # 三天内统计
                sql_page_view_list2 = await conn.execute_query_dict(sql_page_view2)
                sql_page_view_list,sql_page_view_list2=mix_sql(sql_page_view_list, sql_page_view_list2)

        return generate_response(data={
            "cn":result,"hk":result1,"us":result2,"device_rate":device_rate,        "sql_page_view_list":sql_page_view_list, "sql_page_view_list2":sql_page_view_list2 ,      "dis_cn_hk_us":{"cn":cn,"hk":hk,"us":us},

        })

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


#新增2023.3.28
@router.get("/UsHkrank", summary="美股，港股，四张图分布次数图2023.3.28",response_model=ResultResponse[str])
async def UsHkrank(day: int,pid: int):
    try:
        conn = Tortoise.get_connection("default")

        if day==0:#按天查询
            # 搜索a，hk,us分布
            sql1 = f"""SELECT DATE_FORMAT(add_time,'%H') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="hk" and to_days(add_time)=to_days(now())  and stock_type={pid} GROUP BY  time   """ #
            sql2 = f""" SELECT DATE_FORMAT(add_time,'%H') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="us" and to_days(add_time)=to_days(now())  and stock_type={pid} GROUP BY  time   """  #
            hk = await conn.execute_query_dict(sql1)  # hk
            us = await conn.execute_query_dict(sql2)  # us


        elif  day==1:#按周查询
            sql1 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="hk" and date_sub(curdate(), INTERVAL 7 DAY) <= date(add_time) and stock_type={pid} GROUP BY  time   """  #
            sql2 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="us" and date_sub(curdate(), INTERVAL 7 DAY) <= date(add_time) and stock_type={pid} GROUP BY  time  """  #
            hk = await conn.execute_query_dict(sql1)  # hk
            us = await conn.execute_query_dict(sql2)  # us
        elif  day==2:#按月查询
            sql1 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="hk" and date_sub(curdate(), INTERVAL 30 DAY) <= date(add_time) and stock_type={pid} GROUP BY  time   """  #
            sql2 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="us" and date_sub(curdate(), INTERVAL 30 DAY) <= date(add_time) and stock_type={pid} GROUP BY  time  """  #
            hk = await conn.execute_query_dict(sql1)  # hk
            us = await conn.execute_query_dict(sql2)  # us
        elif  day==3:#按年查询
            sql1 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="hk" and date_sub(curdate(), INTERVAL 1 YEAR) <= date(add_time) and stock_type={pid} GROUP BY  time   """  #
            sql2 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="us" and date_sub(curdate(), INTERVAL 1 YEAR) <= date(add_time) and stock_type={pid} GROUP BY  time  """  #
            hk = await conn.execute_query_dict(sql1)  # hk
            us = await conn.execute_query_dict(sql2)  # us
        else:#所有
            sql1 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="hk"  and stock_type={pid} GROUP BY  time   """  #
            sql2 = f"""SELECT DATE_FORMAT(add_time,'%Y-%m-%d') as time,count(id)  cout FROM stock_view_count  WHERE  stock_mk="us"  and stock_type={pid} GROUP BY  time  """  #
            hk = await conn.execute_query_dict(sql1)  # hk
            us = await conn.execute_query_dict(sql2)  # us
        return generate_response(data={
             "dis_cn_hk_us":{"cn":[],"hk":hk,"us":us},

        })

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))



#缺少用户子账号列表，缺少新增修改删除接口，
@router.get("/sub_account_list", summary="用户子账号列表")
async def UserFrontedInfo1(page:int,page_size:int,id :int):
    try:
        limit = page_size
        offset = page_size * (page - 1)
        project = await TbChildAccount.filter(user_id=id).limit(limit=limit).offset(offset=offset)
        ccount = await TbChildAccount.filter(user_id=id).count()
        data={"count":ccount,"data":project}
        return generate_response(data=data)

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

#缺少新增修改删除接口，
@router.post("/not/sub_account_add", summary="用户子账号新增")
async def SubAccountADD(bp:SubAccountReq):
    try:
        obj=await TbChildAccount.create(**bp.dict(),password="00000000")
        obj.name=bp.name if bp.name!="" else str(bp.user_id)+str(obj.id)
        await obj.save()
        await TbMessage.create(send_id=0, receive_id=bp.user_id, type=3, content=f'{bp.name}子帐号新增成功', send_time=datetime.now())

        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/not/sub_account_delete", summary="用户子账号删除")
async def SubAccountDelete(id:int):
    try:
        await TbChildAccount.filter(id=id).delete()

        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/not/sub_account_edit", summary="用户子账号编辑")
async def SubAccountEdit(bp:SubAccountReqEdit):
    try:
        await TbChildAccount.filter(id=bp.id).update(**bp.dict(exclude={'id'}))

        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/update_userinfo", summary="修改用户的信息")
async def UpdateUserinfo(bp:UpdateUserinfoReq):
    try:
        await AuthUser.filter(id=bp.id).update(username=bp.name,email=bp.email)
        await UserInfo.filter(user_id=bp.id).update(is_company=bp.is_company,phone=bp.phone)

        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))

@router.post("/avatar", summary="修改用户的头像,type=1为pc，type=0为管理系统")
async def UpdateUserinfo(bp:AvatarUpdate):
    try:
        if  bp.type==1:#pc,app头像
            await UserInfo.filter(user_id=bp.user_id).update(avatar=bp.avatar)
        else:#管理系统头像
            await TblUser.filter(id=bp.user_id).update(avatar=bp.avatar)
        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/imgcollect", summary="图片收藏和取消收藏,收藏为type==1,取消收藏为type==0")
async def ImgUpdate(bp:ImgUpdateReq):
    try:
        if  bp.type==1:#
            await TbPicture.filter(id=bp.id).update(types=1)
        else:
            await TbPicture.filter(id=bp.id).update(types=2)
        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/imgsort", summary="图片排序即两张图片交换排序id")
async def ImgUpdate(bp:ImgSorted):
    try:
        async with in_transaction(connection_name="default"):
            await TbPicture.filter(id=bp.old_id).update(sort_id=bp.new_sortid)
            await TbPicture.filter(id=bp.new_id).update(sort_id=bp.old_sortid)
        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.post("/vipinfo", summary="修改vip会员到期时间")
async def ImgUpdate(bp:VipSchema):
    try:
        async with in_transaction(connection_name="default"):
            paystatus = await  TbOrderInfo.filter(user_id=bp.id, pay_status="TRADE_SUCCESS").first()
            if paystatus:
                await UserInfo.filter(user_id=bp.id).update(vip_dead_time=bp.vip_dead_time)
            else:
                await UserInfo.filter(user_id=bp.id).update(vip_dead_time=bp.vip_dead_time,vip_create_time=bp.vip_dead_time-relativedelta(years=1))
        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        await TbMessage.create( type=4, content=str(e))

        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))