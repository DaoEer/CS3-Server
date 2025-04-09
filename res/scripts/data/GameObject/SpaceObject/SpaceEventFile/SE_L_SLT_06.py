# -*- coding: utf-8 -*-
Datas = {
    3: [
        {
            "title": "刷帝江/设置阶段1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11000813", 
                    "param4": "", 
                    "id": 34
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 1
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
            "title": "小怪死亡刷boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
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
            "title": "boss死亡，通知帝江next/完成任务目标3/boss死亡喊话", 
            "describe": "天亡……我木傀族……", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "next", 
                    "param1": "20003031", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20101710", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20101711", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q032722", 
                    "param4": "", 
                    "id": 19
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
        }
    ], 
    8: [
        {
            "title": "阶段1完成，开启阶段2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 1
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
    12: [
        {
            "title": "帝江销毁，通知biaoyan给纪宁", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "biaoyan", 
                    "param1": "20003054", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 23, 
                    "param1": "20003031", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    13: [
        {
            "title": "技能清除帝江buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110021002", 
                    "param4": "", 
                    "id": 16
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
            "title": "接到帝江到位通知，帝江语音，刷表演怪并通知一堆/开启阶段3", 
            "describe": "7：纪宁。8：四个亲卫。帝江语音（12s）结束，通知表演怪起身1，箱子发光111，小怪走向箱子2。刷传送门5，发送likai通知帝江离开。\n锁灵塔已归魔门，我会派我弟子纪宁收集塔内先天灵气。斗士这便与我返回逍遥门复命。", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q032723", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20003055|20003056|20003057|20003062|20003054", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 12.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20003055|20003056|20003057|20003062|20003054", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 9.0, 
                    "param3": "", 
                    "param2": "111", 
                    "param1": "20003058|20003059|20003060|20003061", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 15.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 16.0, 
                    "param3": "", 
                    "param2": "likai", 
                    "param1": "20003031", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 15.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 1
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "qinwei", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003031"
                }
            ], 
            "id": 1
        }
    ], 
    17: [
        {
            "title": "技能清除帝江buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110021002", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}