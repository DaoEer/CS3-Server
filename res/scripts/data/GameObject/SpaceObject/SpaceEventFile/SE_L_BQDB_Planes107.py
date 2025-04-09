# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "华成和小弟死完了，刷出Boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041643", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "Boss死了之后，给牢笼发送通知", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "12345", 
                    "param1": "20006399", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "牢笼死亡后，完成任务目标，喊话，刷出传送门，给丹朱发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041645", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "5", 
                    "param1": "20102574", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "12345", 
                    "param1": "20006400", 
                    "param4": "", 
                    "id": 10
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
            "id": 3
        }
    ], 
    30: [
        {
            "title": "Q041634喊话结束，通知报信小怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20006394", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q041634", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "Q041637喊话结束，通知所有怪物战斗", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20006396|20006397|20006398", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q041637", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "Q041641喊话结束，通知报信小怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "111", 
                    "param1": "20006396|20006397|20006398|20006394", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q041641", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    15: [
        {
            "title": "一系列喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041640|Q041641|Q041634|Q041636|Q041637", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "35", 
                    "param3": "32533.5 -7066.118164 1500.73877", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "5000|-2000"
                }
            ], 
            "id": 1
        }
    ]
}