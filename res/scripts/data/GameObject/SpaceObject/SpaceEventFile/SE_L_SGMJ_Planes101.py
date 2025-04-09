# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "第3批怪物死亡，光墙消失", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20003602", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 14
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "巨灵石像死亡，光墙销毁", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20003604", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 14
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "5", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "生命火球全部死亡，发送指令给巨灵石像", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4444", 
                    "param1": "20003603", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "6", 
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
            "title": "收到怪物指令，播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000095", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "666", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20002375"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到镜头指令12345，触发玩家完成任务目标，传送玩家出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20101627", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_SGMJ", 
                    "param4": "", 
                    "id": 20
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
                    "param2": "95"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到巨灵石像通知666，召唤两个小弟", 
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
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "666", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003603"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到巨灵石像通知6666，召唤三个生命球", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020849", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "6666", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003603"
                }
            ], 
            "id": 4
        }
    ]
}