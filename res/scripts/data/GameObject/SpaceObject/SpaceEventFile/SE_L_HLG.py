# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "初始化出生点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 19", 
                    "param1": "-47471 3670 289", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    5: [
        {
            "title": "阵柱全部死亡移除鼎的无敌buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "12137701", 
                    "param1": "20005724", 
                    "param4": "", 
                    "id": 237
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20005725|20005726|20005727|20005728", 
                    "param2": "1|1|1|1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "鼎死亡销毁光墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005729", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -67", 
                    "param1": "25179.0 -523.0 -929", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20005724", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "直接击杀boss通过", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005730", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "1层击杀boss设置2层等级", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 441
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005730", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 61, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "2层击杀boss掉宝箱设置3层等级", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 441
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "414008", 
                    "param2": "2", 
                    "param1": "SK_ZW0017_NPC", 
                    "param4": "", 
                    "id": 440
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005730", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 61, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "3层击杀boss掉宝箱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "414009", 
                    "param2": "2", 
                    "param1": "SK_ZW0017_NPC", 
                    "param4": "", 
                    "id": 440
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005730", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 61, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "id": 6
        }
    ], 
    8: [
        {
            "title": "阶段2完成播放镜头销毁断桥落石", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "603", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "665|667", 
                    "param4": "", 
                    "id": 208
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 45", 
                    "param1": "-2190.0 5173.0 -6979", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001016", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "阶段3完成设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0.0 0.0 -4.58", 
                    "param1": "8714.0 8663.0 -999.0", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    12: [
        {
            "title": "金符销毁召唤陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000648", 
                    "param4": "", 
                    "id": 224
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "40000458", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "冰符销毁召唤陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000649", 
                    "param4": "", 
                    "id": 224
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "40000459", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "火符销毁召唤陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000650", 
                    "param4": "", 
                    "id": 224
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "40000460", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "土符销毁召唤陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000651", 
                    "param4": "", 
                    "id": 224
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "40000461", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    13: [
        {
            "title": "离开地图清除额外物品栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 120
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到通知召唤一号BOSS", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20005742:1", 
                    "param2": "0 0 -170", 
                    "param1": "-7265 4999 240", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "20005742", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到通知召唤一号BOSS", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20005741:1", 
                    "param2": "0 0 -170", 
                    "param1": "-7265 4999 240", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "20005741", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到通知播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "582", 
                    "param4": "", 
                    "id": 170
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "5719", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005719"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "QTE结束判断播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "3", 
                    "param2": "589", 
                    "param1": "590", 
                    "param4": "", 
                    "id": 322
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0.0 0.0 6.3", 
                    "param1": "-10875.0 4285.0 173.0", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "HLG", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    15: [
        {
            "title": "进入范围增加额外物品栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 119
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "40", 
                    "param3": "20752.0 5585.0 -734.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "200|-1200"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "进入范围boss开始移动", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "667", 
                    "param1": "20005719|20005720|20005717", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "-40323 4290 531", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|100"
                }
            ], 
            "id": 2
        }
    ], 
    21: [
        {
            "title": "创建断桥和落石", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "665|667", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    27: [
        {
            "title": "离开范围清除额外物品栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 120
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "40", 
                    "param3": "20752.0 5585.0 -734.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "200|-1200"
                }
            ], 
            "id": 1
        }
    ]
}