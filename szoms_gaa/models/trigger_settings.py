from odoo import models,fields,api
from ..zabbix_api.client import ZabbixClient

class Triggersettings(models.TransientModel):
    _name = 'trigger.settings'
    _description = u'告警配置'
    #_order =
    _inherit = 'res.config.settings'

    # zabbix_url = fields.Char('Zabbix Url')
    # zabbix_user = fields.Char('Zabbix 登录账号')
    # zabbix_pwd = fields.Char('Zabbix登录密码')

    wechat_cropid = fields.Char('微信Cropid')
    wechat_agentid = fields.Char('微信Agentid')
    wechat_secret = fields.Char('微信Secret')
    wechat_user = fields.Char('微信通知接收人')
    wechat_depart = fields.Char('微信通知部门')

    dingtalk_cropid = fields.Char('钉钉CropID')
    dingtalk_agentid = fields.Char('钉钉agentid')
    dingtalk_appid = fields.Char('钉钉appid')
    dingtalk_appsecret = fields.Char('钉钉appsecret')
    dingtalk_user = fields.Char('钉钉通知用户')
    dingtalk_depart = fields.Char('钉钉通知部门')


    @api.multi
    def execute(self):
        self.ensure_one()
        super(Triggersettings,self).execute()


    @api.multi
    def set_values(self):
        if not hasattr(super(Triggersettings, self), 'set_values'):
            return

        self.ensure_one()
        super(Triggersettings, self).set_values()
        config = self
        Param = self.env["ir.config_parameter"].sudo()

        # Param.set_param('zabbix_url', config.zabbix_url)
        # Param.set_param('zabbix_user', config.zabbix_user)
        # Param.set_param('zabbix_pwd', config.zabbix_pwd)

        Param.set_param('wechat_cropid', config.wechat_cropid)
        Param.set_param('wechat_agentid', config.wechat_agentid)
        Param.set_param('wechat_secret', config.wechat_secret)
        Param.set_param('wechat_user', config.wechat_user)
        Param.set_param('wechat_depart', config.wechat_depart)

        Param.set_param('dingtalk_cropid', config.dingtalk_cropid)
        Param.set_param('dingtalk_agentid', config.dingtalk_agentid)
        Param.set_param('dingtalk_appid', config.dingtalk_appid)
        Param.set_param('dingtalk_appsecret', config.dingtalk_appsecret)
        Param.set_param('dingtalk_user', config.dingtalk_user)
        Param.set_param('dingtalk_depart', config.dingtalk_depart)

    @api.model
    def get_values(self):
        res = super(Triggersettings, self).get_values()
        Param = self.env["ir.config_parameter"].sudo()

        res.update(
            # zabbix_url = Param.get_param('zabbix_url', default=''),
            # zabbix_user=Param.get_param('zabbix_user', default=''),
            # zabbix_pwd=Param.get_param('zabbix_pwd', default=''),

            wechat_cropid = Param.get_param('wechat_cropid', default=''),
            wechat_agentid = Param.get_param('wechat_agentid', default=''),
            wechat_secret = Param.get_param('wechat_secret', default=''),
            wechat_user =  Param.get_param('wechat_user', default=''),
            wechat_depart = Param.get_param('wechat_depart', default=''),

            dingtalk_cropid = Param.get_param('dingtalk_cropid', default=''),
            dingtalk_agentid = Param.get_param('dingtalk_agentid', default=''),
            dingtalk_appid = Param.get_param('dingtalk_appid', default=''),
            dingtalk_appsecret = Param.get_param('dingtalk_appsecret', default=''),
            dingtalk_user = Param.get_param('dingtalk_user', default=''),
            dingtalk_depart = Param.get_param('dingtalk_depart', default=''),
        )
        return res

    def Client(self):
        Param = self.env["ir.config_parameter"].sudo()
        url = Param.get_param('zabbix_url')
        user = Param.get_param('zabbix_user')
        pwd = Param.get_param('zabbix_pwd')


        Client = ZabbixClient(url,user,pwd)
        return Client