"""
数据库表模型定义
"""
from tortoise import fields, Model
from tortoise.contrib.pydantic import pydantic_model_creator

from core.model import AbstractBaseModel, TimestampMixin


class TblRole(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=32, unique=True, description='角色名')
    description = fields.CharField(max_length=256, description='角色描述')

    class Meta:
        table = 'tbl_role'
        table_description = '角色表'
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "is_delete"]


class TblUser(TimestampMixin, AbstractBaseModel):
    username = fields.CharField(max_length=64, unique=True)
    nickname = fields.CharField(max_length=128, null=True)
    is_super = fields.SmallIntField(default=0)
    mobile = fields.CharField(max_length=15, null=True)
    email = fields.CharField(max_length=64, unique=True, null=True)
    password = fields.CharField(max_length=128, null=False)
    avatar = fields.CharField(max_length=256, null=True)

    class Meta:
        table = "tbl_user"
        table_description = "用户表信息"
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", 'is_delete']


class AuthUser(Model):
    id = fields.IntField(pk=True)
    password = fields.CharField(max_length=128)
    last_login = fields.DatetimeField(blank=True, null=True)
    is_superuser = fields.IntField()
    username = fields.CharField(unique=True, max_length=150)
    first_name = fields.CharField(max_length=150)
    last_name = fields.CharField(max_length=150)
    email = fields.CharField(max_length=254)
    is_staff = fields.IntField()
    is_active = fields.IntField()
    date_joined = fields.DatetimeField()
    class Meta:
        table = "auth_user"
        table_description = "用户表"
        ordering = [ "id"]

class UserInfo(Model):
    id = fields.IntField(pk=True)
    phone = fields.CharField(max_length=11)
    user_id = fields.IntField()
    sex = fields.IntField()
    age = fields.CharField(max_length=100)
    is_company = fields.IntField()
    user_license = fields.CharField(max_length=255)
    isvip = fields.IntField(db_column='isvip')
    vip_create_time = fields.DatetimeField(blank=True, null=True)
    vip_dead_time = fields.DatetimeField(blank=True, null=True)
    number_of_queries = fields.IntField(default=0)
    license_number = fields.CharField(max_length=64, blank=True, null=True)
    type_of_certificate = fields.IntField(blank=True, null=True)
    query_code = fields.CharField(max_length=255, default="")
    actual_name = fields.CharField(max_length=255, blank=True, null=True)
    avatar = fields.TextField(blank=True, null=True)

    class Meta:
        table = "user_info"
        table_description = "用户表附属1"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']

class Tbpoint(TimestampMixin, AbstractBaseModel):
    page_views = fields.IntField(default=0)
    download_count = fields.IntField(default=0)
    search_count = fields.IntField(default=0)
    login_count = fields.IntField(default=0)


    class Meta:
        table = "tb_point"
        table_description = "埋点统计表"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']

class TbPicture(TimestampMixin, AbstractBaseModel):
    path = fields.CharField(max_length=255, blank=True, null=True)
    types = fields.IntField(default=1)
    user_id = fields.IntField(default=0)
    filename = fields.CharField(max_length=255, blank=True, null=True)
    sort_id = fields.IntField()

    class Meta:
        table = "tb_picture"
        table_description = "图片库"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']
class TbPageViewRank(TimestampMixin, AbstractBaseModel):
    count = fields.IntField(default=0)
    user_id = fields.IntField(default=0)
    type = fields.IntField(default=0)


    class Meta:
        table = "tb_page_view_rank"
        table_description = "浏览量，点赞数表"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']

class TbFavor(TimestampMixin, AbstractBaseModel):
    pid = fields.IntField()
    user_id = fields.IntField()


    class Meta:
        table = "tb_favor"
        unique_together = ('pid', 'user_id',)
        table_description = "用户点赞表"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']

class TbLoginLog(TimestampMixin, AbstractBaseModel):
    user_id = fields.IntField(default=0)#用户id
    type = fields.CharField(default="",max_length=11)#登录类型
    ip = fields.CharField(default="",max_length=255)##登录ip
    ip_addr = fields.CharField(default="",max_length=255)#登录ip地理位置



    class Meta:
        table = "tb_login_log"
        table_description = "登录记录表"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']
class TbRealLoginLog(TimestampMixin, AbstractBaseModel):
    user_id = fields.IntField(default=0)#用户id
    type = fields.CharField(default="",max_length=11)#登录类型
    ip = fields.CharField(default="",max_length=255)##登录ip
    ip_addr = fields.CharField(default="",max_length=255)#登录ip地理位置



    class Meta:
        table = "tb_real_login_log"
        table_description = "实时登录记录表"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']

class TbChildAccount(TimestampMixin, AbstractBaseModel):
    user_id = fields.IntField(default=0)#用户id
    name = fields.CharField(max_length=255, blank=True, null=True)
    phone = fields.CharField(max_length=11, blank=True, null=True)
    email = fields.CharField(max_length=254, blank=True, null=True)
    controller = fields.CharField(max_length=255, blank=True, null=True)
    remark = fields.CharField(max_length=255, blank=True, null=True)#备注
    password = fields.CharField(max_length=128)#密码


    class Meta:
        table = "tb_child_account"
        table_description = "子账号表"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']

class TbBrowseLogs(TimestampMixin, AbstractBaseModel):
    user_id = fields.IntField(default=0)#用户id
    code = fields.CharField(max_length=255, blank=True, null=True)
    mk = fields.CharField(max_length=254, blank=True, null=True)
    devicetype = fields.CharField(max_length=254, default="")


    class Meta:
        table = "tb_browse_logs"
        table_description = "浏览记录表"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']

class TbSubscribe(TimestampMixin, AbstractBaseModel):
    user_id = fields.IntField(default=0)#用户id
    code = fields.CharField(max_length=255, blank=True, null=True)
    mk = fields.CharField(max_length=254, blank=True, null=True)
    stock_name = fields.CharField(max_length=254, blank=True, null=True)
    mode = fields.CharField(max_length=254, blank=True, null=True)#订阅方式


    class Meta:
        table = "tb_subscribe"
        table_description = "订阅记录表"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']
class TbOrderInfo(Model):
    id = fields.IntField(pk=True)
    order_sn = fields.CharField(max_length=30, blank=True, null=True)
    nonce_str = fields.CharField(max_length=50, blank=True, null=True)
    trade_no = fields.CharField(max_length=100, blank=True, null=True)
    pay_status = fields.CharField(max_length=30, blank=True, null=True)
    pay_type = fields.CharField(max_length=10, blank=True, null=True)
    post_script = fields.CharField(max_length=200, blank=True, null=True)
    order_mount = fields.FloatField()
    pay_time = fields.DatetimeField(blank=True, null=True)
    add_time = fields.DatetimeField(blank=True, null=True)

    user_id = fields.IntField(default=0)#用户id


    class Meta:
        table = "orderinfo"
        table_description = "支付订单表"
        ordering = [ "id"]


class TbMessage(TimestampMixin, AbstractBaseModel):
    send_id = fields.IntField(default=0)#发送用户id
    receive_id = fields.IntField(default=0)#接受用户id
    status = fields.IntField(default=0)#消息发送状态
    type = fields.IntField(default=0)#消息类型
    content = fields.TextField( blank=True, null=True)
    send_time = fields.DatetimeField(blank=True, null=True)#发送时间



    class Meta:
        table = "tb_message"
        table_description = "消息记录表"
        ordering = [ "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']




class StockCombin(Model):
    id = fields.IntField(pk=True)

    data_time = fields.DatetimeField(blank=True, null=True)
    stock_combin = fields.CharField(max_length=50, blank=True, null=True)
    input_costs = fields.CharField(db_column='Input_costs', max_length=50, blank=True, null=True)  # Field name made lowercase.
    portfolio_profit_and_loss = fields.CharField(max_length=50, blank=True, null=True)
    portfolio_yield = fields.CharField(max_length=50, blank=True, null=True)
    portfolio_equity = fields.CharField(max_length=50, blank=True, null=True)
    up_down_negative = fields.CharField(max_length=50, blank=True, null=True)
    up_down_negative_na = fields.CharField(max_length=50, blank=True, null=True)
    combin_id = fields.IntField(blank=True, null=True)
    total_value_of_portfolio_equity = fields.CharField(max_length=50, blank=True, null=True)
    class Meta:
        table = "stock_combin"
        table_description = "组合"


class StockCombinList(Model):
    id = fields.IntField(pk=True)

    stock_hold = fields.CharField(max_length=20, default="单投")
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_combin_id = fields.IntField(blank=True, null=True)
    from_mk = fields.CharField(max_length=255, blank=True, null=True)
    create_date = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = "stock_combin_list"
        table_description = "组合列表"


class StockCombinName(Model):
    id = fields.IntField(pk=True)

    combin_name = fields.CharField(max_length=255, blank=True, null=True)
    stock_combin_id = fields.IntField(blank=True, null=True)
    mk = fields.CharField(max_length=255, blank=True, null=True)

    class Meta:
        table = "stock_combin_name"
        table_description = "组合列表"


class StockCode(Model):
    id = fields.IntField(pk=True)

    stock_code = fields.CharField(max_length=50, blank=True, null=True)
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_industry = fields.CharField(max_length=500, blank=True, null=True)
    stock_url = fields.CharField(max_length=255, blank=True, null=True)
    stock_market = fields.CharField(max_length=10, blank=True, null=True)

    class Meta:
        table = "stock_code"
        table_description = "代码库"
class StockHkSharePerLot(Model):
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_per_data = fields.IntField(blank=True, null=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    create_date = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stock_hk_share_per_lot'

class StockA(Model):
    id = fields.IntField(pk=True)

    data_time = fields.DatetimeField(blank=True, null=True)
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_volume = fields.CharField(max_length=20, blank=True, null=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    stock_tradingamount = fields.CharField(db_column='stock_TradingAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_swing = fields.CharField(db_column='stock_Swing', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_changepercent = fields.CharField(db_column='stock_ChangePercent', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_changeamount = fields.CharField(db_column='stock_ChangeAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_turnoverrate = fields.CharField(db_column='stock_TurnoverRate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_open_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_close_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_low_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_high_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_tradingamount_after = fields.CharField(db_column='stock_TradingAmount_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_swing_after = fields.CharField(db_column='stock_Swing_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_changepercent_after = fields.CharField(db_column='stock_ChangePercent_after', max_length=20)  # Field name made lowercase.
    stock_changeamount_after = fields.CharField(db_column='stock_ChangeAmount_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_turnoverrate_after = fields.CharField(db_column='stock_TurnoverRate_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stock_a_info'
class StockHk(Model):
    id = fields.IntField(pk=True)

    data_time = fields.DatetimeField(blank=True, null=True)
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_volume = fields.CharField(max_length=20, blank=True, null=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    stock_tradingamount = fields.CharField(db_column='stock_TradingAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_swing = fields.CharField(db_column='stock_Swing', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_changepercent = fields.CharField(db_column='stock_ChangePercent', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_changeamount = fields.CharField(db_column='stock_ChangeAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_turnoverrate = fields.CharField(db_column='stock_TurnoverRate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_open_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_close_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_low_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_high_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_tradingamount_after = fields.CharField(db_column='stock_TradingAmount_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_swing_after = fields.CharField(db_column='stock_Swing_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_changepercent_after = fields.CharField(db_column='stock_ChangePercent_after', max_length=20)  # Field name made lowercase.
    stock_changeamount_after = fields.CharField(db_column='stock_ChangeAmount_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_turnoverrate_after = fields.CharField(db_column='stock_TurnoverRate_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stock_hk'

class StockUs(Model):
    id = fields.IntField(pk=True)

    data_time = fields.DatetimeField(blank=True, null=True)
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_volume = fields.CharField(max_length=20, blank=True, null=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    stock_tradingamount = fields.CharField(db_column='stock_TradingAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_swing = fields.CharField(db_column='stock_Swing', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_changepercent = fields.CharField(db_column='stock_ChangePercent', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_changeamount = fields.CharField(db_column='stock_ChangeAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_turnoverrate = fields.CharField(db_column='stock_TurnoverRate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_open_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_close_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_low_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_high_after = fields.CharField(max_length=20, blank=True, null=True)
    stock_tradingamount_after = fields.CharField(db_column='stock_TradingAmount_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_swing_after = fields.CharField(db_column='stock_Swing_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_changepercent_after = fields.CharField(db_column='stock_ChangePercent_after', max_length=20)  # Field name made lowercase.
    stock_changeamount_after = fields.CharField(db_column='stock_ChangeAmount_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_turnoverrate_after = fields.CharField(db_column='stock_TurnoverRate_after', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stock_us'


class StockARate(Model):
    id = fields.IntField(pk=True)

    data_time = fields.DatetimeField(blank=True, null=True)
    stock_code = fields.CharField(max_length=50, blank=True, null=True)
    stock_count = fields.CharField(max_length=10, blank=True, null=True)
    stock_dis = fields.CharField(max_length=80, blank=True, null=True)
    stock_first_dis = fields.CharField(max_length=80, blank=True, null=True)
    stock_move_first_dis = fields.CharField(max_length=80, blank=True, null=True)
    stock_hlist = fields.CharField(max_length=80, blank=True, null=True)
    stock_ilist = fields.CharField(max_length=80, blank=True, null=True)
    stock_jlist = fields.CharField(max_length=80, blank=True, null=True)
    stock_klist = fields.CharField(max_length=10, blank=True, null=True)
    stock_actual_probability = fields.CharField(max_length=80, blank=True, null=True)
    stock_difference = fields.CharField(max_length=80, blank=True, null=True)
    stock_rate = fields.CharField(max_length=80, blank=True, null=True)
    stock_rate1 = fields.CharField(max_length=80, blank=True, null=True)
    stock_sort = fields.CharField(max_length=80, blank=True, null=True)
    stocks_relevance = fields.CharField(max_length=10, blank=True, null=True)
    stocks_determination = fields.CharField(max_length=10, blank=True, null=True)
    add_time = fields.DatetimeField(blank=True, null=True)
    probability_of_big_first = fields.CharField(max_length=255, blank=True, null=True)
    stock_dis_2 = fields.CharField(max_length=120, blank=True, null=True)
    stock_ilist_2 = fields.CharField(max_length=120, blank=True, null=True)
    stock_jlist_2 = fields.CharField(max_length=120, blank=True, null=True)
    stock_klist_2 = fields.CharField(max_length=10, blank=True, null=True)
    cycles = fields.IntField(blank=True, null=True)
    cyclestime = fields.CharField(max_length=80, blank=True, null=True)
    m = fields.FloatField(blank=True, null=True)
    l = fields.FloatField(blank=True, null=True)
    t = fields.FloatField(blank=True, null=True)
    jinweidu = fields.CharField(max_length=255, blank=True, null=True)
    cc = fields.CharField(db_column='CC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    d = fields.CharField(db_column='D', max_length=20, blank=True, null=True)  # Field name made lowercase.
    f = fields.CharField(db_column='F', max_length=20, blank=True, null=True)  # Field name made lowercase.
    g = fields.CharField(db_column='G', max_length=20, blank=True, null=True)  # Field name made lowercase.
    h = fields.CharField(db_column='H', max_length=20, blank=True, null=True)  # Field name made lowercase.
    i = fields.CharField(db_column='I', max_length=20, blank=True, null=True)  # Field name made lowercase.
    j = fields.CharField(db_column='J', max_length=20, blank=True, null=True)  # Field name made lowercase.
    l_last = fields.CharField(db_column='L_last', max_length=20, blank=True, null=True)  # Field name made lowercase.
    m_last = fields.CharField(db_column='M_last', max_length=20, blank=True, null=True)  # Field name made lowercase.
    n = fields.CharField(db_column='N', max_length=20, blank=True, null=True)  # Field name made lowercase.
    o = fields.CharField(db_column='O', max_length=20, blank=True, null=True)  # Field name made lowercase.
    p = fields.CharField(db_column='P', max_length=20, blank=True, null=True)  # Field name made lowercase.
    q = fields.CharField(db_column='Q', max_length=20, blank=True, null=True)  # Field name made lowercase.
    r = fields.CharField(db_column='R', max_length=20, blank=True, null=True)  # Field name made lowercase.
    s = fields.CharField(db_column='S', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_last = fields.CharField(db_column='T_last', max_length=20, blank=True, null=True)  # Field name made lowercase.
    u = fields.CharField(db_column='U', max_length=50, blank=True, null=True)  # Field name made lowercase.
    v = fields.CharField(db_column='V', max_length=20, blank=True, null=True)  # Field name made lowercase.
    w = fields.CharField(db_column='W', max_length=20, blank=True, null=True)  # Field name made lowercase.
    x = fields.CharField(db_column='X', max_length=20, blank=True, null=True)  # Field name made lowercase.
    y = fields.CharField(db_column='Y', max_length=20, blank=True, null=True)  # Field name made lowercase.
    z = fields.CharField(db_column='Z', max_length=20, blank=True, null=True)  # Field name made lowercase.
    aa = fields.CharField(db_column='AA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ab = fields.CharField(db_column='AB', max_length=22, blank=True, null=True)  # Field name made lowercase.
    s_all = fields.CharField(db_column='S_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_all = fields.CharField(db_column='T_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    w_all = fields.CharField(db_column='W_all', max_length=50, blank=True, null=True)  # Field name made lowercase.
    x_all = fields.CharField(db_column='X_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ab_all = fields.CharField(db_column='AB_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ac_all = fields.CharField(db_column='AC_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ae = fields.IntField(db_column='AE', blank=True, null=True)  # Field name made lowercase.
    af = fields.IntField(db_column='AF', blank=True, null=True)  # Field name made lowercase.
    ae1 = fields.CharField(db_column='AE1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af1 = fields.CharField(db_column='AF1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ae1_all = fields.CharField(db_column='AE1_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af1_all = fields.CharField(db_column='AF1_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    point = fields.CharField(max_length=3, blank=True, null=True)
    ad = fields.IntField(db_column='AD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        table = "stock_a_rate"

class StockHkRate(Model):
    id = fields.IntField(pk=True)

    data_time = fields.DatetimeField(blank=True, null=True)
    stock_code = fields.CharField(max_length=50, blank=True, null=True)
    stock_count = fields.CharField(max_length=10, blank=True, null=True)
    stock_dis = fields.CharField(max_length=80, blank=True, null=True)
    stock_first_dis = fields.CharField(max_length=80, blank=True, null=True)
    stock_move_first_dis = fields.CharField(max_length=80, blank=True, null=True)
    stock_hlist = fields.CharField(max_length=80, blank=True, null=True)
    stock_ilist = fields.CharField(max_length=80, blank=True, null=True)
    stock_jlist = fields.CharField(max_length=80, blank=True, null=True)
    stock_klist = fields.CharField(max_length=10, blank=True, null=True)
    stock_actual_probability = fields.CharField(max_length=80, blank=True, null=True)
    stock_difference = fields.CharField(max_length=80, blank=True, null=True)
    stock_rate = fields.CharField(max_length=80, blank=True, null=True)
    stock_rate1 = fields.CharField(max_length=80, blank=True, null=True)
    stock_sort = fields.CharField(max_length=80, blank=True, null=True)
    stocks_relevance = fields.CharField(max_length=10, blank=True, null=True)
    stocks_determination = fields.CharField(max_length=10, blank=True, null=True)
    add_time = fields.DatetimeField(blank=True, null=True)
    probability_of_big_first = fields.CharField(max_length=255, blank=True, null=True)
    stock_dis_2 = fields.CharField(max_length=120, blank=True, null=True)
    stock_ilist_2 = fields.CharField(max_length=120, blank=True, null=True)
    stock_jlist_2 = fields.CharField(max_length=120, blank=True, null=True)
    stock_klist_2 = fields.CharField(max_length=10, blank=True, null=True)
    cycles = fields.IntField(blank=True, null=True)
    cyclestime = fields.CharField(max_length=80, blank=True, null=True)
    m = fields.FloatField(blank=True, null=True)
    l = fields.FloatField(blank=True, null=True)
    t = fields.FloatField(blank=True, null=True)
    jinweidu = fields.CharField(max_length=255, blank=True, null=True)
    cc = fields.CharField(db_column='CC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    d = fields.CharField(db_column='D', max_length=20, blank=True, null=True)  # Field name made lowercase.
    f = fields.CharField(db_column='F', max_length=20, blank=True, null=True)  # Field name made lowercase.
    g = fields.CharField(db_column='G', max_length=20, blank=True, null=True)  # Field name made lowercase.
    h = fields.CharField(db_column='H', max_length=20, blank=True, null=True)  # Field name made lowercase.
    i = fields.CharField(db_column='I', max_length=20, blank=True, null=True)  # Field name made lowercase.
    j = fields.CharField(db_column='J', max_length=20, blank=True, null=True)  # Field name made lowercase.
    l_last = fields.CharField(db_column='L_last', max_length=20, blank=True, null=True)  # Field name made lowercase.
    m_last = fields.CharField(db_column='M_last', max_length=20, blank=True, null=True)  # Field name made lowercase.
    n = fields.CharField(db_column='N', max_length=20, blank=True, null=True)  # Field name made lowercase.
    o = fields.CharField(db_column='O', max_length=20, blank=True, null=True)  # Field name made lowercase.
    p = fields.CharField(db_column='P', max_length=20, blank=True, null=True)  # Field name made lowercase.
    q = fields.CharField(db_column='Q', max_length=20, blank=True, null=True)  # Field name made lowercase.
    r = fields.CharField(db_column='R', max_length=20, blank=True, null=True)  # Field name made lowercase.
    s = fields.CharField(db_column='S', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_last = fields.CharField(db_column='T_last', max_length=20, blank=True, null=True)  # Field name made lowercase.
    u = fields.CharField(db_column='U', max_length=50, blank=True, null=True)  # Field name made lowercase.
    v = fields.CharField(db_column='V', max_length=20, blank=True, null=True)  # Field name made lowercase.
    w = fields.CharField(db_column='W', max_length=20, blank=True, null=True)  # Field name made lowercase.
    x = fields.CharField(db_column='X', max_length=20, blank=True, null=True)  # Field name made lowercase.
    y = fields.CharField(db_column='Y', max_length=20, blank=True, null=True)  # Field name made lowercase.
    z = fields.CharField(db_column='Z', max_length=20, blank=True, null=True)  # Field name made lowercase.
    aa = fields.CharField(db_column='AA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ab = fields.CharField(db_column='AB', max_length=22, blank=True, null=True)  # Field name made lowercase.
    s_all = fields.CharField(db_column='S_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_all = fields.CharField(db_column='T_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    w_all = fields.CharField(db_column='W_all', max_length=50, blank=True, null=True)  # Field name made lowercase.
    x_all = fields.CharField(db_column='X_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ab_all = fields.CharField(db_column='AB_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ac_all = fields.CharField(db_column='AC_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ae = fields.IntField(db_column='AE', blank=True, null=True)  # Field name made lowercase.
    af = fields.IntField(db_column='AF', blank=True, null=True)  # Field name made lowercase.
    ae1 = fields.CharField(db_column='AE1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af1 = fields.CharField(db_column='AF1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ae1_all = fields.CharField(db_column='AE1_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af1_all = fields.CharField(db_column='AF1_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    point = fields.CharField(max_length=3, blank=True, null=True)
    ad = fields.IntField(db_column='AD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        table = "stock_hk_rate"

class StockUsRate(Model):
    id = fields.IntField(pk=True)

    data_time = fields.DatetimeField(blank=True, null=True)
    stock_code = fields.CharField(max_length=50, blank=True, null=True)
    stock_count = fields.CharField(max_length=10, blank=True, null=True)
    stock_dis = fields.CharField(max_length=80, blank=True, null=True)
    stock_first_dis = fields.CharField(max_length=80, blank=True, null=True)
    stock_move_first_dis = fields.CharField(max_length=80, blank=True, null=True)
    stock_hlist = fields.CharField(max_length=80, blank=True, null=True)
    stock_ilist = fields.CharField(max_length=80, blank=True, null=True)
    stock_jlist = fields.CharField(max_length=80, blank=True, null=True)
    stock_klist = fields.CharField(max_length=10, blank=True, null=True)
    stock_actual_probability = fields.CharField(max_length=80, blank=True, null=True)
    stock_difference = fields.CharField(max_length=80, blank=True, null=True)
    stock_rate = fields.CharField(max_length=80, blank=True, null=True)
    stock_rate1 = fields.CharField(max_length=80, blank=True, null=True)
    stock_sort = fields.CharField(max_length=80, blank=True, null=True)
    stocks_relevance = fields.CharField(max_length=10, blank=True, null=True)
    stocks_determination = fields.CharField(max_length=10, blank=True, null=True)
    add_time = fields.DatetimeField(blank=True, null=True)
    probability_of_big_first = fields.CharField(max_length=255, blank=True, null=True)
    stock_dis_2 = fields.CharField(max_length=120, blank=True, null=True)
    stock_ilist_2 = fields.CharField(max_length=120, blank=True, null=True)
    stock_jlist_2 = fields.CharField(max_length=120, blank=True, null=True)
    stock_klist_2 = fields.CharField(max_length=10, blank=True, null=True)
    cycles = fields.IntField(blank=True, null=True)
    cyclestime = fields.CharField(max_length=80, blank=True, null=True)
    m = fields.FloatField(blank=True, null=True)
    l = fields.FloatField(blank=True, null=True)
    t = fields.FloatField(blank=True, null=True)
    jinweidu = fields.CharField(max_length=255, blank=True, null=True)
    cc = fields.CharField(db_column='CC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    d = fields.CharField(db_column='D', max_length=20, blank=True, null=True)  # Field name made lowercase.
    f = fields.CharField(db_column='F', max_length=20, blank=True, null=True)  # Field name made lowercase.
    g = fields.CharField(db_column='G', max_length=20, blank=True, null=True)  # Field name made lowercase.
    h = fields.CharField(db_column='H', max_length=20, blank=True, null=True)  # Field name made lowercase.
    i = fields.CharField(db_column='I', max_length=20, blank=True, null=True)  # Field name made lowercase.
    j = fields.CharField(db_column='J', max_length=20, blank=True, null=True)  # Field name made lowercase.
    l_last = fields.CharField(db_column='L_last', max_length=20, blank=True, null=True)  # Field name made lowercase.
    m_last = fields.CharField(db_column='M_last', max_length=20, blank=True, null=True)  # Field name made lowercase.
    n = fields.CharField(db_column='N', max_length=20, blank=True, null=True)  # Field name made lowercase.
    o = fields.CharField(db_column='O', max_length=20, blank=True, null=True)  # Field name made lowercase.
    p = fields.CharField(db_column='P', max_length=20, blank=True, null=True)  # Field name made lowercase.
    q = fields.CharField(db_column='Q', max_length=20, blank=True, null=True)  # Field name made lowercase.
    r = fields.CharField(db_column='R', max_length=20, blank=True, null=True)  # Field name made lowercase.
    s = fields.CharField(db_column='S', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_last = fields.CharField(db_column='T_last', max_length=20, blank=True, null=True)  # Field name made lowercase.
    u = fields.CharField(db_column='U', max_length=50, blank=True, null=True)  # Field name made lowercase.
    v = fields.CharField(db_column='V', max_length=20, blank=True, null=True)  # Field name made lowercase.
    w = fields.CharField(db_column='W', max_length=20, blank=True, null=True)  # Field name made lowercase.
    x = fields.CharField(db_column='X', max_length=20, blank=True, null=True)  # Field name made lowercase.
    y = fields.CharField(db_column='Y', max_length=20, blank=True, null=True)  # Field name made lowercase.
    z = fields.CharField(db_column='Z', max_length=20, blank=True, null=True)  # Field name made lowercase.
    aa = fields.CharField(db_column='AA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ab = fields.CharField(db_column='AB', max_length=22, blank=True, null=True)  # Field name made lowercase.
    s_all = fields.CharField(db_column='S_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_all = fields.CharField(db_column='T_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    w_all = fields.CharField(db_column='W_all', max_length=50, blank=True, null=True)  # Field name made lowercase.
    x_all = fields.CharField(db_column='X_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ab_all = fields.CharField(db_column='AB_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ac_all = fields.CharField(db_column='AC_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ae = fields.IntField(db_column='AE', blank=True, null=True)  # Field name made lowercase.
    af = fields.IntField(db_column='AF', blank=True, null=True)  # Field name made lowercase.
    ae1 = fields.CharField(db_column='AE1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af1 = fields.CharField(db_column='AF1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ae1_all = fields.CharField(db_column='AE1_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    af1_all = fields.CharField(db_column='AF1_all', max_length=20, blank=True, null=True)  # Field name made lowercase.
    point = fields.CharField(max_length=3, blank=True, null=True)
    ad = fields.IntField(db_column='AD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        table = "stock_us_rate"

class Stockhkperminute1(Model):
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_volume = fields.CharField(max_length=20, blank=True, null=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    stock_latest = fields.CharField(db_column='stock_Latest', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_tradingamount = fields.CharField(db_column='stock_TradingAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stockhkperminute1'

class Stockusperminute1(Model):
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_volume = fields.CharField(max_length=20, blank=True, null=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    stock_latest = fields.CharField(db_column='stock_Latest', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stock_tradingamount = fields.CharField(db_column='stock_TradingAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stockusperminute1'

"""2023.2.9"""
class StockViewCount(Model):
    stock_mk = fields.CharField(max_length=20, blank=True, null=True)
    stock_type = fields.CharField(max_length=20, blank=True, null=True)#股票类型图
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_view_count = fields.CharField(max_length=20, blank=True, null=True,default=0)
    user_id = fields.IntField(db_column='user_id')  # Field name made lowercase.

    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stock_view_count'

class Stockcnperminute5(Model):
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_volume = fields.CharField(max_length=20, blank=True, null=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    stock_tradingamount = fields.CharField(db_column='stock_TradingAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    changepercent = fields.CharField(db_column='ChangePercent', max_length=20, blank=True, null=True)  # Field name made lowercase.
    changeamount = fields.CharField(db_column='ChangeAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    swing = fields.CharField(db_column='Swing', max_length=20, blank=True, null=True)  # Field name made lowercase.
    turnoverrate = fields.CharField(db_column='TurnoverRate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stockcnperminute5'

class Stockhkperminute5(Model):
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_volume = fields.CharField(max_length=20, blank=True, null=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    stock_tradingamount = fields.CharField(db_column='stock_TradingAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    changepercent = fields.CharField(db_column='ChangePercent', max_length=20, blank=True, null=True)  # Field name made lowercase.
    changeamount = fields.CharField(db_column='ChangeAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    swing = fields.CharField(db_column='Swing', max_length=20, blank=True, null=True)  # Field name made lowercase.
    turnoverrate = fields.CharField(db_column='TurnoverRate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stockhkperminute5'

class Stockusperminute5(Model):
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_name = fields.CharField(max_length=300, blank=True, null=True)
    stock_volume = fields.CharField(max_length=20, blank=True, null=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    stock_tradingamount = fields.CharField(db_column='stock_TradingAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    changepercent = fields.CharField(db_column='ChangePercent', max_length=20, blank=True, null=True)  # Field name made lowercase.
    changeamount = fields.CharField(db_column='ChangeAmount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    swing = fields.CharField(db_column='Swing', max_length=20, blank=True, null=True)  # Field name made lowercase.
    turnoverrate = fields.CharField(db_column='TurnoverRate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stockusperminute5'
class Stockcnperminute5Excelcn(Model):
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_count = fields.CharField(max_length=10, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    changepercent = fields.CharField(db_column='ChangePercent', max_length=100, blank=True, null=True)  # Field name made lowercase.
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    h = fields.CharField(db_column='H', max_length=20, blank=True, null=True)  # Field name made lowercase.
    i = fields.CharField(db_column='I', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)
    j = fields.CharField(db_column='J', max_length=100, blank=True, null=True)  # Field name made lowercase.
    k = fields.CharField(db_column='K', max_length=100, blank=True, null=True)  # Field name made lowercase.
    l = fields.CharField(db_column='L', max_length=100, blank=True, null=True)  # Field name made lowercase.
    m = fields.CharField(db_column='M', max_length=100, blank=True, null=True)  # Field name made lowercase.
    n = fields.CharField(db_column='N', max_length=100, blank=True, null=True)  # Field name made lowercase.
    o = fields.CharField(db_column='O', max_length=100, blank=True, null=True)  # Field name made lowercase.
    p = fields.CharField(db_column='P', max_length=100, blank=True, null=True)  # Field name made lowercase.
    q = fields.CharField(db_column='Q', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r1 = fields.CharField(db_column='R1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r = fields.CharField(db_column='R', max_length=100, blank=True, null=True)  # Field name made lowercase.
    s = fields.CharField(db_column='S', max_length=100, blank=True, null=True)  # Field name made lowercase.
    t = fields.CharField(db_column='T', max_length=100, blank=True, null=True)  # Field name made lowercase.
    u = fields.CharField(db_column='U', max_length=100, blank=True, null=True)  # Field name made lowercase.
    v = fields.CharField(db_column='V', max_length=100, blank=True, null=True)  # Field name made lowercase.
    w = fields.CharField(db_column='W', max_length=100, blank=True, null=True)  # Field name made lowercase.
    x = fields.CharField(db_column='X', max_length=100, blank=True, null=True)  # Field name made lowercase.
    y = fields.CharField(db_column='Y', max_length=100, blank=True, null=True)  # Field name made lowercase.
    z = fields.CharField(db_column='Z', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aa = fields.CharField(db_column='AA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ab = fields.CharField(db_column='AB', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ac = fields.CharField(db_column='AC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ad = fields.CharField(db_column='AD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ae = fields.CharField(db_column='AE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    af = fields.CharField(db_column='AF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ag = fields.CharField(db_column='AG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ah = fields.CharField(db_column='AH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ai = fields.CharField(db_column='AI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aj = fields.CharField(db_column='AJ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ak = fields.CharField(db_column='AK', max_length=100, blank=True, null=True)  # Field name made lowercase.
    al = fields.CharField(db_column='AL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    am = fields.CharField(db_column='AM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    an = fields.CharField(db_column='AN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ao = fields.CharField(db_column='AO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ap = fields.CharField(db_column='AP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aq = fields.CharField(db_column='AQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ar = fields.CharField(db_column='AR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    as_field = fields.CharField(db_column='AS', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    at = fields.CharField(db_column='AT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    au = fields.CharField(db_column='AU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    av = fields.CharField(db_column='AV', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aw = fields.CharField(db_column='AW', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ax = fields.CharField(db_column='AX', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ay = fields.CharField(db_column='AY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    az = fields.CharField(db_column='AZ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ba = fields.CharField(db_column='BA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bb = fields.CharField(db_column='BB', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bc = fields.CharField(db_column='BC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bd = fields.CharField(db_column='BD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    be = fields.CharField(db_column='BE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bf = fields.CharField(db_column='BF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bg = fields.CharField(db_column='BG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bh = fields.CharField(db_column='BH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bi = fields.CharField(db_column='BI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    b = fields.CharField(db_column='B', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bk = fields.CharField(db_column='BK', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bl = fields.CharField(db_column='BL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bm = fields.CharField(db_column='BM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bn = fields.CharField(db_column='BN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bo = fields.CharField(db_column='BO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bp = fields.CharField(db_column='BP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bq = fields.CharField(db_column='BQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bball = fields.CharField(db_column='BBALL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bqall = fields.CharField(db_column='BQALL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    event_list = fields.CharField(max_length=255, blank=True, null=True)
    sum_event_list = fields.CharField(max_length=255, blank=True, null=True)
    bs_index_list = fields.CharField(max_length=255, blank=True, null=True)
    class Meta:
        table = 'stockcnperminute5_excelcn'

class Stockcnperminute5Excelhk(Model):
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_count = fields.CharField(max_length=10, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    changepercent = fields.CharField(db_column='ChangePercent', max_length=100, blank=True, null=True)  # Field name made lowercase.
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    h = fields.CharField(db_column='H', max_length=20, blank=True, null=True)  # Field name made lowercase.
    i = fields.CharField(db_column='I', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)
    j = fields.CharField(db_column='J', max_length=100, blank=True, null=True)  # Field name made lowercase.
    k = fields.CharField(db_column='K', max_length=100, blank=True, null=True)  # Field name made lowercase.
    l = fields.CharField(db_column='L', max_length=100, blank=True, null=True)  # Field name made lowercase.
    m = fields.CharField(db_column='M', max_length=100, blank=True, null=True)  # Field name made lowercase.
    n = fields.CharField(db_column='N', max_length=100, blank=True, null=True)  # Field name made lowercase.
    o = fields.CharField(db_column='O', max_length=100, blank=True, null=True)  # Field name made lowercase.
    p = fields.CharField(db_column='P', max_length=100, blank=True, null=True)  # Field name made lowercase.
    q = fields.CharField(db_column='Q', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r1 = fields.CharField(db_column='R1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r = fields.CharField(db_column='R', max_length=100, blank=True, null=True)  # Field name made lowercase.
    s = fields.CharField(db_column='S', max_length=100, blank=True, null=True)  # Field name made lowercase.
    t = fields.CharField(db_column='T', max_length=100, blank=True, null=True)  # Field name made lowercase.
    u = fields.CharField(db_column='U', max_length=100, blank=True, null=True)  # Field name made lowercase.
    v = fields.CharField(db_column='V', max_length=100, blank=True, null=True)  # Field name made lowercase.
    w = fields.CharField(db_column='W', max_length=100, blank=True, null=True)  # Field name made lowercase.
    x = fields.CharField(db_column='X', max_length=100, blank=True, null=True)  # Field name made lowercase.
    y = fields.CharField(db_column='Y', max_length=100, blank=True, null=True)  # Field name made lowercase.
    z = fields.CharField(db_column='Z', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aa = fields.CharField(db_column='AA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ab = fields.CharField(db_column='AB', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ac = fields.CharField(db_column='AC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ad = fields.CharField(db_column='AD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ae = fields.CharField(db_column='AE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    af = fields.CharField(db_column='AF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ag = fields.CharField(db_column='AG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ah = fields.CharField(db_column='AH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ai = fields.CharField(db_column='AI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aj = fields.CharField(db_column='AJ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ak = fields.CharField(db_column='AK', max_length=100, blank=True, null=True)  # Field name made lowercase.
    al = fields.CharField(db_column='AL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    am = fields.CharField(db_column='AM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    an = fields.CharField(db_column='AN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ao = fields.CharField(db_column='AO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ap = fields.CharField(db_column='AP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aq = fields.CharField(db_column='AQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ar = fields.CharField(db_column='AR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    as_field = fields.CharField(db_column='AS', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    at = fields.CharField(db_column='AT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    au = fields.CharField(db_column='AU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    av = fields.CharField(db_column='AV', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aw = fields.CharField(db_column='AW', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ax = fields.CharField(db_column='AX', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ay = fields.CharField(db_column='AY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    az = fields.CharField(db_column='AZ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ba = fields.CharField(db_column='BA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bb = fields.CharField(db_column='BB', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bc = fields.CharField(db_column='BC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bd = fields.CharField(db_column='BD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    be = fields.CharField(db_column='BE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bf = fields.CharField(db_column='BF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bg = fields.CharField(db_column='BG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bh = fields.CharField(db_column='BH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bi = fields.CharField(db_column='BI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    b = fields.CharField(db_column='B', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bk = fields.CharField(db_column='BK', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bl = fields.CharField(db_column='BL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bm = fields.CharField(db_column='BM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bn = fields.CharField(db_column='BN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bo = fields.CharField(db_column='BO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bp = fields.CharField(db_column='BP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bq = fields.CharField(db_column='BQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bball = fields.CharField(db_column='BBALL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bqall = fields.CharField(db_column='BQALL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    event_list = fields.CharField(max_length=255, blank=True, null=True)
    sum_event_list = fields.CharField(max_length=255, blank=True, null=True)
    bs_index_list = fields.CharField(max_length=255, blank=True, null=True)
    class Meta:
        table = 'stockcnperminute5_excelhk'

class Stockcnperminute5Excelus(Model):
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_count = fields.CharField(max_length=10, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    changepercent = fields.CharField(db_column='ChangePercent', max_length=100, blank=True, null=True)  # Field name made lowercase.
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    h = fields.CharField(db_column='H', max_length=20, blank=True, null=True)  # Field name made lowercase.
    i = fields.CharField(db_column='I', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)
    j = fields.CharField(db_column='J', max_length=100, blank=True, null=True)  # Field name made lowercase.
    k = fields.CharField(db_column='K', max_length=100, blank=True, null=True)  # Field name made lowercase.
    l = fields.CharField(db_column='L', max_length=100, blank=True, null=True)  # Field name made lowercase.
    m = fields.CharField(db_column='M', max_length=100, blank=True, null=True)  # Field name made lowercase.
    n = fields.CharField(db_column='N', max_length=100, blank=True, null=True)  # Field name made lowercase.
    o = fields.CharField(db_column='O', max_length=100, blank=True, null=True)  # Field name made lowercase.
    p = fields.CharField(db_column='P', max_length=100, blank=True, null=True)  # Field name made lowercase.
    q = fields.CharField(db_column='Q', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r1 = fields.CharField(db_column='R1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r = fields.CharField(db_column='R', max_length=100, blank=True, null=True)  # Field name made lowercase.
    s = fields.CharField(db_column='S', max_length=100, blank=True, null=True)  # Field name made lowercase.
    t = fields.CharField(db_column='T', max_length=100, blank=True, null=True)  # Field name made lowercase.
    u = fields.CharField(db_column='U', max_length=100, blank=True, null=True)  # Field name made lowercase.
    v = fields.CharField(db_column='V', max_length=100, blank=True, null=True)  # Field name made lowercase.
    w = fields.CharField(db_column='W', max_length=100, blank=True, null=True)  # Field name made lowercase.
    x = fields.CharField(db_column='X', max_length=100, blank=True, null=True)  # Field name made lowercase.
    y = fields.CharField(db_column='Y', max_length=100, blank=True, null=True)  # Field name made lowercase.
    z = fields.CharField(db_column='Z', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aa = fields.CharField(db_column='AA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ab = fields.CharField(db_column='AB', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ac = fields.CharField(db_column='AC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ad = fields.CharField(db_column='AD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ae = fields.CharField(db_column='AE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    af = fields.CharField(db_column='AF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ag = fields.CharField(db_column='AG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ah = fields.CharField(db_column='AH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ai = fields.CharField(db_column='AI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aj = fields.CharField(db_column='AJ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ak = fields.CharField(db_column='AK', max_length=100, blank=True, null=True)  # Field name made lowercase.
    al = fields.CharField(db_column='AL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    am = fields.CharField(db_column='AM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    an = fields.CharField(db_column='AN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ao = fields.CharField(db_column='AO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ap = fields.CharField(db_column='AP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aq = fields.CharField(db_column='AQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ar = fields.CharField(db_column='AR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    as_field = fields.CharField(db_column='AS', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    at = fields.CharField(db_column='AT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    au = fields.CharField(db_column='AU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    av = fields.CharField(db_column='AV', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aw = fields.CharField(db_column='AW', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ax = fields.CharField(db_column='AX', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ay = fields.CharField(db_column='AY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    az = fields.CharField(db_column='AZ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ba = fields.CharField(db_column='BA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bb = fields.CharField(db_column='BB', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bc = fields.CharField(db_column='BC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bd = fields.CharField(db_column='BD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    be = fields.CharField(db_column='BE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bf = fields.CharField(db_column='BF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bg = fields.CharField(db_column='BG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bh = fields.CharField(db_column='BH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bi = fields.CharField(db_column='BI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    b = fields.CharField(db_column='B', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bk = fields.CharField(db_column='BK', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bl = fields.CharField(db_column='BL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bm = fields.CharField(db_column='BM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bn = fields.CharField(db_column='BN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bo = fields.CharField(db_column='BO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bp = fields.CharField(db_column='BP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bq = fields.CharField(db_column='BQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bball = fields.CharField(db_column='BBALL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bqall = fields.CharField(db_column='BQALL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    event_list = fields.CharField(max_length=255, blank=True, null=True)
    sum_event_list = fields.CharField(max_length=255, blank=True, null=True)
    bs_index_list = fields.CharField(max_length=255, blank=True, null=True)
    class Meta:
        table = 'stockcnperminute5_excelus'

class StockperdaysExcelcn(Model):
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_count = fields.CharField(max_length=10, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    changepercent = fields.CharField(db_column='ChangePercent', max_length=100, blank=True, null=True)  # Field name made lowercase.
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    h = fields.CharField(db_column='H', max_length=20, blank=True, null=True)  # Field name made lowercase.
    i = fields.CharField(db_column='I', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)
    j = fields.CharField(db_column='J', max_length=100, blank=True, null=True)  # Field name made lowercase.
    k = fields.CharField(db_column='K', max_length=100, blank=True, null=True)  # Field name made lowercase.
    l = fields.CharField(db_column='L', max_length=100, blank=True, null=True)  # Field name made lowercase.
    m = fields.CharField(db_column='M', max_length=100, blank=True, null=True)  # Field name made lowercase.
    n = fields.CharField(db_column='N', max_length=100, blank=True, null=True)  # Field name made lowercase.
    o = fields.CharField(db_column='O', max_length=100, blank=True, null=True)  # Field name made lowercase.
    p = fields.CharField(db_column='P', max_length=100, blank=True, null=True)  # Field name made lowercase.
    q = fields.CharField(db_column='Q', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r1 = fields.CharField(db_column='R1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r = fields.CharField(db_column='R', max_length=100, blank=True, null=True)  # Field name made lowercase.
    s = fields.CharField(db_column='S', max_length=100, blank=True, null=True)  # Field name made lowercase.
    t = fields.CharField(db_column='T', max_length=100, blank=True, null=True)  # Field name made lowercase.
    u = fields.CharField(db_column='U', max_length=100, blank=True, null=True)  # Field name made lowercase.
    v = fields.CharField(db_column='V', max_length=100, blank=True, null=True)  # Field name made lowercase.
    w = fields.CharField(db_column='W', max_length=100, blank=True, null=True)  # Field name made lowercase.
    x = fields.CharField(db_column='X', max_length=100, blank=True, null=True)  # Field name made lowercase.
    y = fields.CharField(db_column='Y', max_length=100, blank=True, null=True)  # Field name made lowercase.
    z = fields.CharField(db_column='Z', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aa = fields.CharField(db_column='AA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ab = fields.CharField(db_column='AB', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ac = fields.CharField(db_column='AC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ad = fields.CharField(db_column='AD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ae = fields.CharField(db_column='AE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    af = fields.CharField(db_column='AF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ag = fields.CharField(db_column='AG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ah = fields.CharField(db_column='AH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ai = fields.CharField(db_column='AI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aj = fields.CharField(db_column='AJ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ak = fields.CharField(db_column='AK', max_length=100, blank=True, null=True)  # Field name made lowercase.
    al = fields.CharField(db_column='AL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    am = fields.CharField(db_column='AM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    an = fields.CharField(db_column='AN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ao = fields.CharField(db_column='AO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ap = fields.CharField(db_column='AP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aq = fields.CharField(db_column='AQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ar = fields.CharField(db_column='AR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    as_field = fields.CharField(db_column='AS', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    at = fields.CharField(db_column='AT', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        table = 'stockperdays_excelcn'

class StockperdaysExcelhk(Model):
    id = fields.IntField(pk=True)
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_count = fields.CharField(max_length=10, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    changepercent = fields.CharField(db_column='ChangePercent', max_length=100, blank=True, null=True)  # Field name made lowercase.
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    h = fields.CharField(db_column='H', max_length=20, blank=True, null=True)  # Field name made lowercase.
    i = fields.CharField(db_column='I', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)
    j = fields.CharField(db_column='J', max_length=100, blank=True, null=True)  # Field name made lowercase.
    k = fields.CharField(db_column='K', max_length=100, blank=True, null=True)  # Field name made lowercase.
    l = fields.CharField(db_column='L', max_length=100, blank=True, null=True)  # Field name made lowercase.
    m = fields.CharField(db_column='M', max_length=100, blank=True, null=True)  # Field name made lowercase.
    n = fields.CharField(db_column='N', max_length=100, blank=True, null=True)  # Field name made lowercase.
    o = fields.CharField(db_column='O', max_length=100, blank=True, null=True)  # Field name made lowercase.
    p = fields.CharField(db_column='P', max_length=100, blank=True, null=True)  # Field name made lowercase.
    q = fields.CharField(db_column='Q', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r1 = fields.CharField(db_column='R1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r = fields.CharField(db_column='R', max_length=100, blank=True, null=True)  # Field name made lowercase.
    s = fields.CharField(db_column='S', max_length=100, blank=True, null=True)  # Field name made lowercase.
    t = fields.CharField(db_column='T', max_length=100, blank=True, null=True)  # Field name made lowercase.
    u = fields.CharField(db_column='U', max_length=100, blank=True, null=True)  # Field name made lowercase.
    v = fields.CharField(db_column='V', max_length=100, blank=True, null=True)  # Field name made lowercase.
    w = fields.CharField(db_column='W', max_length=100, blank=True, null=True)  # Field name made lowercase.
    x = fields.CharField(db_column='X', max_length=100, blank=True, null=True)  # Field name made lowercase.
    y = fields.CharField(db_column='Y', max_length=100, blank=True, null=True)  # Field name made lowercase.
    z = fields.CharField(db_column='Z', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aa = fields.CharField(db_column='AA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ab = fields.CharField(db_column='AB', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ac = fields.CharField(db_column='AC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ad = fields.CharField(db_column='AD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ae = fields.CharField(db_column='AE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    af = fields.CharField(db_column='AF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ag = fields.CharField(db_column='AG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ah = fields.CharField(db_column='AH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ai = fields.CharField(db_column='AI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aj = fields.CharField(db_column='AJ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ak = fields.CharField(db_column='AK', max_length=100, blank=True, null=True)  # Field name made lowercase.
    al = fields.CharField(db_column='AL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    am = fields.CharField(db_column='AM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    an = fields.CharField(db_column='AN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ao = fields.CharField(db_column='AO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ap = fields.CharField(db_column='AP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aq = fields.CharField(db_column='AQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ar = fields.CharField(db_column='AR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    as_field = fields.CharField(db_column='AS', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    at = fields.CharField(db_column='AT', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        table = 'stockperdays_excelhk'

class StockperdaysExcelus(Model):
    stock_code = fields.CharField(max_length=20, blank=True, null=True)
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_count = fields.CharField(max_length=10, blank=True, null=True)
    stock_close = fields.CharField(max_length=20, blank=True, null=True)
    stock_open = fields.CharField(max_length=20, blank=True, null=True)
    changepercent = fields.CharField(db_column='ChangePercent', max_length=100, blank=True, null=True)  # Field name made lowercase.
    stock_low = fields.CharField(max_length=20, blank=True, null=True)
    stock_high = fields.CharField(max_length=20, blank=True, null=True)
    h = fields.CharField(db_column='H', max_length=20, blank=True, null=True)  # Field name made lowercase.
    i = fields.CharField(db_column='I', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)
    j = fields.CharField(db_column='J', max_length=100, blank=True, null=True)  # Field name made lowercase.
    k = fields.CharField(db_column='K', max_length=100, blank=True, null=True)  # Field name made lowercase.
    l = fields.CharField(db_column='L', max_length=100, blank=True, null=True)  # Field name made lowercase.
    m = fields.CharField(db_column='M', max_length=100, blank=True, null=True)  # Field name made lowercase.
    n = fields.CharField(db_column='N', max_length=100, blank=True, null=True)  # Field name made lowercase.
    o = fields.CharField(db_column='O', max_length=100, blank=True, null=True)  # Field name made lowercase.
    p = fields.CharField(db_column='P', max_length=100, blank=True, null=True)  # Field name made lowercase.
    q = fields.CharField(db_column='Q', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r1 = fields.CharField(db_column='R1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    r = fields.CharField(db_column='R', max_length=100, blank=True, null=True)  # Field name made lowercase.
    s = fields.CharField(db_column='S', max_length=100, blank=True, null=True)  # Field name made lowercase.
    t = fields.CharField(db_column='T', max_length=100, blank=True, null=True)  # Field name made lowercase.
    u = fields.CharField(db_column='U', max_length=100, blank=True, null=True)  # Field name made lowercase.
    v = fields.CharField(db_column='V', max_length=100, blank=True, null=True)  # Field name made lowercase.
    w = fields.CharField(db_column='W', max_length=100, blank=True, null=True)  # Field name made lowercase.
    x = fields.CharField(db_column='X', max_length=100, blank=True, null=True)  # Field name made lowercase.
    y = fields.CharField(db_column='Y', max_length=100, blank=True, null=True)  # Field name made lowercase.
    z = fields.CharField(db_column='Z', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aa = fields.CharField(db_column='AA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ab = fields.CharField(db_column='AB', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ac = fields.CharField(db_column='AC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ad = fields.CharField(db_column='AD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ae = fields.CharField(db_column='AE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    af = fields.CharField(db_column='AF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ag = fields.CharField(db_column='AG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ah = fields.CharField(db_column='AH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ai = fields.CharField(db_column='AI', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aj = fields.CharField(db_column='AJ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ak = fields.CharField(db_column='AK', max_length=100, blank=True, null=True)  # Field name made lowercase.
    al = fields.CharField(db_column='AL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    am = fields.CharField(db_column='AM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    an = fields.CharField(db_column='AN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ao = fields.CharField(db_column='AO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ap = fields.CharField(db_column='AP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aq = fields.CharField(db_column='AQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ar = fields.CharField(db_column='AR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    as_field = fields.CharField(db_column='AS', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    at = fields.CharField(db_column='AT', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        table = 'stockperdays_excelus'

#2023.2.11
class Stockcnperminute1ExcelHK(Model):
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_code = fields.CharField(max_length=100, blank=True, null=True)
    hu = fields.CharField(db_column='HU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hv = fields.CharField(db_column='HV', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ij = fields.CharField(db_column='IJ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ke = fields.CharField(db_column='KE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    kf = fields.CharField(db_column='KF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    kv = fields.CharField(db_column='KV', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sf = fields.CharField(db_column='SF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sg = fields.CharField(db_column='SG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    su = fields.CharField(db_column='SU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    up = fields.CharField(db_column='UP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    uq = fields.CharField(db_column='UQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vg = fields.CharField(db_column='VG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    xx = fields.CharField(db_column='XX', max_length=100, blank=True, null=True)  # Field name made lowercase.
    xy = fields.CharField(db_column='XY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stockcnperminute1_excelhk'

class Stockcnperminute1ExcelUs(Model):
    data_time = fields.DatetimeField(blank=True, null=True)
    stock_code = fields.CharField(max_length=100, blank=True, null=True)
    hu = fields.CharField(db_column='HU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hv = fields.CharField(db_column='HV', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ij = fields.CharField(db_column='IJ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ke = fields.CharField(db_column='KE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    kf = fields.CharField(db_column='KF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    kv = fields.CharField(db_column='KV', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sf = fields.CharField(db_column='SF', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sg = fields.CharField(db_column='SG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    su = fields.CharField(db_column='SU', max_length=100, blank=True, null=True)  # Field name made lowercase.
    up = fields.CharField(db_column='UP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    uq = fields.CharField(db_column='UQ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vg = fields.CharField(db_column='VG', max_length=100, blank=True, null=True)  # Field name made lowercase.
    xx = fields.CharField(db_column='XX', max_length=100, blank=True, null=True)  # Field name made lowercase.
    xy = fields.CharField(db_column='XY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stockcnperminute1_excelus'
class Stockcnperminute1ExcelCheck(Model):
    stock_mk = fields.CharField(max_length=20, blank=True, null=True)
    ij = fields.TextField(db_column='IJ',  blank=True, null=True)  # Field name made lowercase.
    kv = fields.TextField(db_column='KV',  blank=True, null=True)  # Field name made lowercase.
    su = fields.TextField(db_column='SU',  blank=True, null=True)  # Field name made lowercase.
    vg = fields.TextField(db_column='VG',  blank=True, null=True)  # Field name made lowercase.
    add_time = fields.DatetimeField(blank=True, null=True)

    class Meta:
        table = 'stockcnperminute1_excel_check'

UserBase = pydantic_model_creator(TblUser, name="UserBase")
UserOut = pydantic_model_creator(
    TblUser,
    name='UserOut',
    include=["id",'username', 'nickname', 'mobile', 'email',"avatar"])

RoleCreate = pydantic_model_creator(TblRole, name='RoleCreate')
RoleOut = pydantic_model_creator(TblRole, name='RoleOut')
PictureOut = pydantic_model_creator(TbPicture, name='PictureOut')
TbLoginLogOut = pydantic_model_creator(TbLoginLog, name='TbLoginLog')
TbChildAccountOut = pydantic_model_creator(TbChildAccount, name='TbChildAccount')
TbBrowseLogsOut = pydantic_model_creator(TbBrowseLogs, name='TbBrowseLogs')
TbSubscribeOut = pydantic_model_creator(TbSubscribe, name='TbSubscribe')
Stockcnperminute5ExcelcnOut = pydantic_model_creator(Stockcnperminute5Excelcn, name='Stockcnperminute5Excelcn')