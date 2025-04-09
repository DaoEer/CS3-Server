# -*- coding: utf-8 -*-
Datas = {
    3: [
        {
            "title": "移除玩家身上加移速buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11066601", 
                    "param4": "", 
                    "id": 26
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
            "title": "第一波小怪死亡，刷第二波小怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
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
            "title": "第三波小怪死亡，刷BOSS", 
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
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "BOSS死亡，死亡喊话/完成任务目标1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045077", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102020", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20004473", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    30: [
        {
            "title": "boss死亡喊话结束，退出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045078", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_BQDB", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q045077", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "第一波小怪喊话结束，通知小怪攻击", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20005974|20005975|20005982", 
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
                    "param1": "Q045066", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "第二波小怪喊话结束，通知小怪攻击", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20005984|20005979|20005978", 
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
                    "param1": "Q045070", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    15: [
        {
            "title": "进入第一波怪物范围，喊话/通知小怪进战", 
            "describe": "我们蛇王岛百蛇汇聚，乃万毒之源。闯入者必将尸骨无存！\n虚张声势！尔等蛇妖敢在水源下毒，今日我便要踏平这蛇王岛！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045065|Q045066", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "-42280.035156 41513.781250 -1387.160645", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-887|-1887"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "进入第三波怪物范围，喊话/通知小怪进战", 
            "describe": "姐妹们！张开你们的獠牙，把这来犯的小贼撕碎了！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045070", 
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
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "-48690.527344 50014.832031 -834.224121", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-334|-1334"
                }
            ], 
            "id": 2
        }
    ]
}