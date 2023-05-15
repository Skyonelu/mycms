from datetime import datetime

from pydantic import BaseModel


class SearchReq(BaseModel):
    receive_id : int
    type : int#消息类型
    content :str
    send_time :datetime#发送时间
    # class Config:
    #     """
    #     schema_extra中设置参数的例子，在API文档中可以看到
    #     """
    #     schema_extra = {
    #         'example':     {
    #     "mk": "cn",
    #     "from_date": '2021-10-21 10:36:37',
    #     "dead_date": '2021-11-21 10:36:44',
    #     "page": 1,
    #     "page_size": 5
    # }
    #     }
