"""
URL视图处理
"""
import os
import shutil
import traceback
from typing import List, Any, Union, Optional
from datetime import timedelta, datetime

from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, status, HTTPException, Request, UploadFile, File, Path
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from tortoise import Tortoise
from tortoise.expressions import F
from tortoise.query_utils import Q

from . import crud, schema, model
from core import settings
from utils.response_code import ResultResponse, HttpStatus
from utils import logger
from .schema import *
from ..user.model import *
from ..user.view import generate_response

router = APIRouter()


#cha
@router.post('/message/send',
             summary='发送消息',
             name='发送消息',
             response_model=ResultResponse[str])
async def cc(request: Request,bp: SearchReq):
    user =request.state.user

    project = await TbMessage.create(send_id=user.id,receive_id=bp.receive_id,type=bp.type,content=bp.content,send_time=bp.send_time)
    return ResultResponse[str](code=HttpStatus.HTTP_200_OK, message='success')

@router.get('/message/list',
             summary='消息列表',
             name='消息列表',
             response_model=ResultResponse[str])

async def cc21(page:int,page_size:int,ms_type:int=0,mb_type:int=0,status :int=-1) -> Any:
    try:
        limit = page_size
        offset = page_size * (page - 1)
        if  ms_type:
            cc =await TbMessage.filter(type=ms_type).limit(limit=limit).offset(offset=offset).order_by("-id").values()
            count1=await TbMessage.filter(type=ms_type).count()
            for i in cc:#1企业，2个人，3免费
                obj=await UserInfo.get_or_none(user_id=i['receive_id'])
                if  ms_type!=4 and obj!=None:
                    i["mbtype"] =1  if obj.is_company  else 2
        else:
            cc =await TbMessage.filter(~Q(type=4)).limit(limit=limit).offset(offset=offset).order_by("-id").values()
            count1 = await TbMessage.filter(~Q(type=4)).count()
            for i in cc:#1企业，2个人，3免费
                obj=await UserInfo.get_or_none(user_id=i['receive_id'])
                if obj!=None:
                    i["mbtype"] =1  if obj.is_company  else 2
        data={"data":cc,"count": count1}
        return generate_response(data=data)

    except Exception as e:
        logger.error(traceback.format_exc())
        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))


@router.delete('/message/delete',
             summary='删除消息',
             name='删除消息',
             response_model=ResultResponse[str])

async def cc21(msid:int) -> Any:
    try:

        await TbMessage.filter(id=msid).delete()

        return generate_response()

    except Exception as e:
        logger.error(traceback.format_exc())
        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))
@router.get('/message/receive',
             summary='用户查看自己消息列表',
             name='用户查看自己消息列表',
             response_model=ResultResponse[str])
async def cc4(page:int,page_size:int,userid:int) -> Any:
    try:
        limit = page_size
        offset = page_size * (page - 1)
        # project = await TbMessage.filter(receive_id__in=[0,userid]).limit(limit=limit).offset(offset=offset)
        project = await TbMessage.filter(receive_id=userid).order_by("-id").limit(limit=limit).offset(offset=offset)
        ct=await TbMessage.filter(receive_id=userid).count()
        data={"data":project,"count":ct}
        return generate_response(data=data)

    except Exception as e:
        logger.error(traceback.format_exc())
        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))
@router.get('/message/system',
             summary='问题发生分布数，占比暂时无法统计',
             name='问题发生数',
             response_model=ResultResponse[str])

async def cc3() -> Any:
    try:
        conn = Tortoise.get_connection("default")
        sql = f"""SELECT DATE_FORMAT(created_at,'%Y-%m') as time,count(id)  cout FROM tb_message where type=4 GROUP BY  time   """  # 系统问题发生个数
        sys = await conn.execute_query_dict(sql)  # 新用户统计
        return generate_response(data=sys)

    except Exception as e:
        logger.error(traceback.format_exc())
        return ResultResponse[str](code=HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR, message='fail', data=str(e))
