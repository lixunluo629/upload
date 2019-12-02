from odoo import models,fields,api
from ..zabbix_api.zabbix_client import ZabbixApi
from odoo.exceptions import UserError
import datetime

class ZabbixTrigger(models.Model):
    _name = 'zabbix.trigger'
    _description = 'Zabbix触发器'

    trigger_id = fields.Many2one('zabbix.event','触发器事件')
    eventid = fields.Char(string='事件ID',related='trigger_id.event_id')
    descrtiption = fields.Char('描述信息')
    objectid = fields.Char('对象id')
    host_id = fields.Many2one('zabbix_host',string='触发器主机',ondelete='set null')
    priority = fields.Selection([('0','未分类'),
                                 ('1','信息'),
                                 ('2','警告'),
                                 ('3','平均'),
                                 ('4','高'),
                                 ('5','灾难')],string='优先级',default='0')
    status = fields.Selection([('0','启用'),
                               ('1','禁用')],string='是否启用触发器',default='0')
    last_change = fields.Char('最近修改时间')
    state = fields.Selection([('0','待确认'),('1','已确认'),('2','已解决')])
    active = fields.Boolean('问题激活',default=True)

    @api.model
    def compute_active(self):
        Client = self.env['settings_configure'].Client()


    def get_trigger(self):
        Client = self.env['settings_configure'].Client()
        trigger = Client.gettrigetID()
        localtrigger = self.env['zabbix.trigger'].search([('active','=',True)])
        localobjectid = [record.objectid for record in localtrigger]
        objectids = [x.get('triggerid') for x in trigger]
        updateids = [y for y in localobjectid if y not in objectids ]
        if len(updateids)>0:
            self.update_trigger(updateids,Client)

        if len(trigger)>0:
            for t in trigger:
                if len(t.get('hosts')) < 1:
                    device = ''
                else:
                    host = t.get('hosts')[0]
                    device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
                    if not device:
                        self.env['settings_configure'].get_host_data()
                        device = self.env['zabbix_host'].search([('host_id', '=', host.get('hostid'))]).id
                # last_time = datetime.datetime.fromtimestamp(int(t["lastchange"]))
                event = self.env['zabbix.event'].check_objects(t.get('triggerid'),Client)
                vals={
                    "objectid" :t.get('triggerid'),
                    "trigger_id" : event,
                    "descrtiption" : t['description'],
                    "priority" : t['priority'],
                    "status" : t['status'],
                    "last_change" : t.get("lastchange"),
                    "host_id" : device,
                    "state":t['state'],
                    "active":True

                }
                rec = self.env['zabbix.trigger'].search([('objectid', '=', t.get('triggerid'))])
                if rec:
                    self.env['zabbix.trigger'].write(vals)
                else:
                    self.env['zabbix.trigger'].create(vals)
                    self.env['alarm.event'].create_event(vals)
    def update_trigger(self,updateids,Client):
        for id in updateids:
            print(type(id))
            record = self.env['zabbix.trigger'].search([('objectid', '=', id)])
            record.write({'active':False})
            print(record.eventid)
            event = Client.eventid_get(record.eventid)[0]
            print(event)
            self.env['zabbix.event'].createvals(event)
            r_event = Client.eventid_get(event.get("r_eventid"))[0]
            print(r_event)
            self.env['zabbix.event'].createvals(r_event)


    @api.constrains('active')
    def check_cron(self):
        self.ensure_one()
        for record in self:
            if not record.active:
                name = record.objectid + '事件推送任务'
                rec =self.env['ir.cron'].search([('name','=',name)])
                if rec:
                    rec.unlink()

    @api.multi
    def open_trigger(self):
        rec = self.env['ir.cron'].search([('name', '=', '定时获取问题事件')])
        if rec:
            raise UserError('已开启同步问题事件任务')
        model_id = self.env.ref("szoms_gaa.model_zabbix_trigger").id
        self.env['zabbix.trigger'].get_trigger()
        self.env['ir.cron'].sudo().create({
            'name': '定时获取问题事件',  # 定时任务名
            'interval_type': 'minutes',  # 定时间隔的单位
            'interval_number': 1,  # 定时间隔
            'numbercall': -1,  # 循环次数（-1代表无限循环）
            'doall': False,  # 服务器重启错过时机，是否补回执行
            'model_id': model_id,  # 任务绑定的Model
            'state': 'code',
            'code': "model.get_trigger()"
        })


    def event_change(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "name": "问题更新",
            "res_model": "zabbix.ensure",
            "view_mode": "form"
        }
        action['context']={
            'eventid' :self.eventid
        }
        return action

