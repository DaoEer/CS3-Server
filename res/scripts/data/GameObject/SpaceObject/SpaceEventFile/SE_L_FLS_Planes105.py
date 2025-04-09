# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段4完成，设置玩家完成任务“飞溅崖”", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101741", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    12: [
        {
            "title": "前面三波小怪全部死亡，刷精英", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "1|2|3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "精英死亡，刷浮空怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "小怪死亡，刷boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "5|6", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "收到风玄通知，播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000215", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003913"
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "玩家进入范围3，刷跳出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "45", 
                    "param3": "-35899.816406 -51141.332031 12467.515625", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "12967|12267"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入范围1，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q030878", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q030879", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "-18061.769531 -43269.589844 4371.005859", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "4471|4071"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家进入范围2，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q030881", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "-19831.769531 -44799.589844 10453.517578", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "10953|10053"
                }
            ], 
            "id": 3
        }
    ]
}