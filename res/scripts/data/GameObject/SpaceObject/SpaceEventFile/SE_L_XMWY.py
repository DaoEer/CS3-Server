# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 124", 
                    "param1": "9748 -13992 241", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "副本计时", 
            "describe": "5分钟失败计时", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "a", 
                    "param4": "", 
                    "id": 422
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "180", 
                    "param1": "c", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    2: [
        {
            "title": "10秒倒计时结束，开始副本计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "30", 
                    "param1": "t2", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "每30秒亮2个聚灵鼎", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "2", 
                    "param2": "40000997", 
                    "param1": "11045601", 
                    "param4": "", 
                    "id": 238
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "3分钟重新刷怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20014556:1", 
                    "param2": "0 0 0", 
                    "param1": "9706 -4004 241", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20014555:1", 
                    "param2": "0 0 0", 
                    "param1": "10041 399 241", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20014554:1", 
                    "param2": "0 0 0", 
                    "param1": "6162 2051 241", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20014553:1", 
                    "param2": "0 0 0", 
                    "param1": "997 3019 241", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20014552:1", 
                    "param2": "0 0 0", 
                    "param1": "-2510 -409 241", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20014551:1", 
                    "param2": "0 0 0", 
                    "param1": "-337 -7862 241", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "xiaohui", 
                    "param1": "20014551|20014552|20014553|20014554|20014555|20014556", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "c", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    6: [
        {
            "title": "怪物刷新进入虚无状态", 
            "describe": "怪物刷新时加上虚无状态BUFF", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12253102", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20014551|20014552|20014553|20014554|20014555|20014556", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "聚灵鼎刷新", 
            "describe": "聚灵鼎刷新时加上禁止交互的buff", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11045601", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "40000997", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    8: [
        {
            "title": "完成阶段1副本通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "SK_ZW0017_NPC|2|4677 -344 241|0 0 11", 
                    "param2": "3:C001905|5:C001904", 
                    "param1": "303010052:600012,600011|303010053:600022,600021|303010054:600002,600005", 
                    "param4": "30", 
                    "id": 450
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20014551|20014552|20014553|20014554|20014555|20014556|20014557|20014558|20014559|20014560|20014561|20014562|20014563|20014564|20014565|20014566", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20014661:1", 
                    "param2": "0 0 -90", 
                    "param1": "4137 -2738 241", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40001017:1", 
                    "param2": "0 0 90", 
                    "param1": "4002 -3341 241", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "玩家开启照妖镜", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "7.5", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 234
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "OPEN", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "122573001", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "4137 -2738 241", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|100"
                }
            ], 
            "id": 1
        }
    ], 
    17: [
        {
            "title": "清除副本中的数据", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "15003601", 
                    "param4": "", 
                    "id": 235
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "10秒界面计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}