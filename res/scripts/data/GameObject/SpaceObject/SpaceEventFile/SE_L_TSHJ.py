# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段4完成，放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000022", 
                    "param4": "", 
                    "id": 17
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
            "id": 1
        }
    ], 
    5: [
        {
            "title": "石像2-1死亡，通知1-2销毁并刷2-2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "112", 
                    "param1": "20000054", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "4", 
                    "param2": "20000053:4"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "石像2-2死亡，通知1-3销毁并刷2-3", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "113", 
                    "param1": "20000055", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "4", 
                    "param2": "20000054:4"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "石像2-3死亡，放南极仙翁伪装镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000021", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 10, 
                    "param1": "4", 
                    "param2": "20000055:4"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "收到镜头通知，获得物品", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110001003", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12345", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "22"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "（战士）收到镜头通知，刷太古心魔", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "20000239:1", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "111", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "21"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "（剑客）收到镜头通知，刷太古心魔", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "20000045:1", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "222", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "21"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "（链刃）收到镜头通知，刷太古心魔", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "333", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "21"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "（法师）收到镜头通知，刷太古心魔", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "9", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "444", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "21"
                }
            ], 
            "id": 5
        }
    ], 
    15: [
        {
            "title": "玩家达到牌坊处，刷暗怪，发通知", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "20000050", 
                    "param1": "3", 
                    "param4": "20000056:3", 
                    "id": 28
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "1", 
                    "param2": "20000050", 
                    "param1": "3", 
                    "param4": "20000051:4", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "-3414.913086 -766.80896 14789.927734", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "19000|9000"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家上楼梯且阶段2完成，放旁白", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q010545", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "40", 
                    "param3": "-3840 -7770 15395.232422", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "20000|10000"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家到达阶梯上阶段2完成，通知1-1销毁刷1-2并播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "111", 
                    "param1": "20000053", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q010546", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "-3840 -7770 15395.232422", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "22000|12000"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家进入平台发送通知", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20000271|20000272", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "30", 
                    "param3": "-3291.748047 2538.833008 14611.603516", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "21000|11000"
                }
            ], 
            "id": 4
        }
    ]
}