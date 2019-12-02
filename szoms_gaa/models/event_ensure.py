from odoo import models,fields,api
from ..zabbix_api.zabbix_client import ZabbixApi
from odoo.exceptions import UserError

class ZabbixConfirm(models.TransientModel):
    _name = 'zabbix.confirm'
    _description = u'确认'

    info = fields.Char("信息")
    model = fields.Char('模型')
    method = fields.Char('方法')

    @api.multi
    def execute(self):
        self.ensure_one()
        active_ids = self._context.get('record_ids')
        rs = self.env[self.model].browse(active_ids)
        ret = getattr(rs, self.method)()
        return ret

    @api.multi
    def execute_with_info(self):
        self.ensure_one()
        active_ids = self._context.get('record_ids')
        rs = self.env[self.model].browse(active_ids)
        ret = getattr(rs, self.method)(self.info)
        return ret

class EventEnsure(models.TransientModel):
    _name = 'zabbix.ensure'

    event_id = fields.Char('事件id')
    message = fields.Char('信息')
    ensure = fields.Boolean('确认问题',default=False)
    close = fields.Boolean('关闭问题',default=False)
    severity = fields.Selection([('0', '未分类'),
                                 ('1', '信息'),
                                 ('2', '警告'),
                                 ('3', '平均'),
                                 ('4', '高'),
                                 ('5', '灾难')], string='更改问题严重性')


    def eventchange(self):
        eventid = self.env.context.get('eventid')
        actions = 0
        parms = {'eventids':eventid}
        for record in self:
            if record.message:
                parms["message"] = record.message
                actions += 2
            if record.close:
                actions += 1
            if record.ensure:
                self.env['alarm.event'].delate_record(eventid)
                actions += 4
            if record.severity:
                parms["severity"] = int(record.severity)
                actions += 8
            parms["action"] = actions
            if actions ==0:
                raise UserError('请选择更新的项目，不更新请点击取消按钮')
            Client = self.env['settings_configure'].Client()
            Client.eventackknowledge(parms)

