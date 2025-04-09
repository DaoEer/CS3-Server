# -*- coding: utf-8 -*-
Datas = {
    "10001368": {
        "talks": [
            {
                "msg": "@F{n=/Game/miscs/Fonts/SIMLI;fc=c18; fs=15;ft=Regular }@S{16}阵营战场@F{n=/Game/miscs/Fonts/msyh;fc=c2; fs=12;ft=Regular }@B@B@S{6}天下英雄集结于此，为各自阵营热血奋战。阵营战场开启后，勇士可报名参加活动，匹配成功后随机进入一处战场：英雄王座、上古密阵、25人绝命战场、灵脉战场、5人绝命战场。进入战场后和同阵营玩家一起对抗敌对阵营玩家，孰强孰弱，战场一分高下！@F{n=/Game/miscs/Fonts/msyh;fc=c3; fs=10;ft=Regular }@B{2}@S{0}活动规则：@B{1}@S{0}1、阵营战场开放时间：每周三、六、日的20:00-24:00。@B{1}@S{0}2、阵营战场为跨服匹配，可与其他服同阵营玩家一同奋战。@B{1}@S{0}3、玩家可以单人匹配，也可以组队匹配。@B{1}@S{0}4、组队匹配时，由队长操作匹配。队伍成员必须同一阵营，并且在同一等级段：30-39级或40-49级。@B{1}@S{0}5、每周可以参加的五处战场均有次数限制，可通过NPC查询剩余次数。每周战场次数在周日晚24点重置。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "cs1", 
                        "title": "英雄王座匹配"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs2", 
                        "title": "上古密阵匹配"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs3", 
                        "title": "大荒战场匹配"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs4", 
                        "title": "灵脉战场匹配"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs5", 
                        "title": "绝命战场匹配"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs6", 
                        "title": "战场次数查询"
                    }
                ], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TAPlayGossipVoice", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "C001392"
                            }
                        ]
                    }
                ], 
                "key": "Talk", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TACampActivityRandomFit", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }
                        ]
                    }
                ], 
                "key": "cs1", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TACampActivityRandomFit", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "6"
                            }
                        ]
                    }
                ], 
                "key": "cs2", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TABattleActivitySignUp", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "7"
                            }
                        ]
                    }
                ], 
                "key": "cs3", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TABattleActivitySignUp", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "8"
                            }
                        ]
                    }
                ], 
                "key": "cs4", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TACampActivityRandomFit", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "9"
                            }
                        ]
                    }
                ], 
                "key": "cs5", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TAQueryPublicActRecord", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5|6|7|8|9"
                            }
                        ]
                    }
                ], 
                "key": "cs6", 
                "visibles": []
            }
        ], 
        "npcID": "10001368"
    }
}