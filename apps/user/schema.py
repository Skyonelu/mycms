"""
请求参数模型
"""
from typing import List, Optional

from pydantic import BaseModel, Field

from .model import UserBase, TbPicture
from datetime import datetime


class Token(BaseModel):
    access_token: str = Field(..., description='Token值')
    token_type: str = Field(..., description='Token类型')


# 创建账号需要验证的条件
class UserCreate(UserBase):
    confirm: str = Field(..., description='确认密码')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'username': 'guest',
                'nickname': '访客',
                'email': 'guest@example.com',
                'mobile': '10086',
                'password': '123456',
                'confirm': '123456',
                'avatar': 'https://img2.woyaogexing.com/2021/05/03/dfcfaaffa8ed4e1a819eba8c10b856d4!400x400.jpeg'
            }
        }

class PicListBase(BaseModel):
    path: str
    user_id: int
class PicListOut(PicListBase):
    id : int

    class Config:
        orm_mode = True
    # class Config:#内部类Config用于定义模型的某些配置。 在这里，我们告诉Pydantic，我们使用的是自定义类型(由arbitrary_types_allowed )，也为JSON序列化映射(由json_encoders )。
    #     arbitrary_types_allowed = True
        # json_encoders = {
        #     ObjectId: str
        # }
# 修改用户名和密码
class UserPasswordReq(BaseModel):
    username: str = Field(..., description='用户名')
    password: str = Field(..., description='密码')

# 浏览量买点schema
class BrowsePointReq(BaseModel):
    type: int = Field(..., description='类型')
    user_id: int = Field(..., description='用户id')
    pic_id : int
    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'type': 1,
                'user_id': 1,
                'pic_id': 1
            }
        }

# 浏览记录
class BrowseLogsReq(BaseModel):
    user_id: int = Field(..., description='用户id')
    code: str
    mk : str
    devicetype : Optional[str]

# 浏览记录
class SubscribeReq(BaseModel):
    user_id: int = Field(..., description='用户id')
    code: str
    mk : str
    stock_name :str
    mode :str


#用户子帐号新增
class SubAccountReq(BaseModel):
    user_id: int = Field(..., description='用户id')
    name: str
    phone: str
    email: str
    controller: str
    remark: str

class SubAccountReqEdit(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    controller: str
    remark: str


class UpdateUserinfoReq(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    is_company: int


class AvatarUpdate(BaseModel):
    type: int
    user_id: int
    avatar: str

class ImgUpdateReq(BaseModel):
    id: int
    type: int

class ImgSorted(BaseModel):
    old_id: int = Field(..., description='之前的图片id')
    old_sortid: int = Field(..., description='之前的图片排序id')
    new_id: int = Field(..., description='之后的图片id')
    new_sortid: int = Field(..., description='之后的图片排序id')


class VipSchema(BaseModel):
    id: int
    vip_dead_time: datetime