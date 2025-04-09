# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 1, 
    "dead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "fight": {
        "subStateDatas": {
            1: {
                "name": "通用战斗状态（远程法系）", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "呼叫同伴", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [], 
                        "id": 3
                    }, 
                    {
                        "comment": "火系远程普攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100093001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100093001"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "每隔三秒，选择最高伤害为攻击目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction8", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "id": 5
                    }
                ], 
                "eventsAI": {
                    5: [
                        {
                            "comment": "切换目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction13", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 6
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "暗怪（自由远程）", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "把20米范围内的玩家加入敌人列表", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "20"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "20"
                            }
                        ], 
                        "id": 1
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}