from typing import List

from pydantic import BaseModel, Field
from datetime import datetime

class VerificatReq(BaseModel):
    mk: str
    datetime: datetime
    code: str
    Input_method : str
    input_costs : int
    from_date :datetime
    dead_date :datetime
class StocckSearchReq(BaseModel):
    mk: str
    code: str
    page: int =1
    page_size: int=30
    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example':     {
  "mk": "cn",
  "code": "1",
  "page": 1,
  "page_size": 10
}
        }

class SearchMinuteReq(BaseModel):
    mk: str
    choose_date :datetime
    code :str

class SearchReq(BaseModel):
    mk: str
    from_date :datetime
    dead_date :datetime
    page: int
    page_size: int
    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example':     {
        "mk": "cn",
        "from_date": '2021-10-21 10:36:37',
        "dead_date": '2021-11-21 10:36:44',
        "page": 1,
        "page_size": 5
    }
        }

class CombinSearchReq(BaseModel):
    combin_id: int
    page: int
    page_size: int
    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example':     {
        "mk": "cn",
        "from_date": '2021-10-21 10:36:37',
        "dead_date": '2021-11-21 10:36:44',
        "page": 1,
        "page_size": 5
    }
        }


class StockCodeReq(BaseModel):
    stock_code :str
    stock_name :str
    stock_industry :str
    stock_url :str
    stock_market :str

class UpdateStockCombinReqBase(BaseModel):
    stock_hold :str
    stock_code :str
    stock_combin_id :int
    from_mk :str
    stock_combin_id :int

class UpdateStockCombinReq(BaseModel):
    stock_combin_id :int
    data : List[UpdateStockCombinReqBase]

class StockCombinListReq(BaseModel):
    id :int
    stock_hold :str
    stock_code :str
    stock_combin_id :int
    from_mk :str