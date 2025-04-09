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
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "试剑台暗怪召唤陷阱一", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "a1到达1秒召唤光效", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "0", 
                                "param3": "", 
                                "param2": "-8234.789063 -41271.058594 12139.614258", 
                                "param1": "20000242"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "0", 
                                "param3": "", 
                                "param2": "-7982.374512 -40954.726563 12139.614258", 
                                "param1": "20000242"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "0", 
                                "param3": "", 
                                "param2": "-7952.249023 -41270.382813 12139.614258", 
                                "param1": "20000242"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "a1"
                            }
                        ], 
                        "id": 1
                    }, 
                    {
                        "comment": "a1到达2秒召唤怪物", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "0", 
                                "param3": "0 0 -50", 
                                "param2": "-7952.249023 -41270.382813 12139.614258", 
                                "param1": "20000262"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "0", 
                                "param3": "0 0 -50", 
                                "param2": "-7982.374512 -40954.726563 12139.614258", 
                                "param1": "20000262"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "0", 
                                "param3": "0 0 -50", 
                                "param2": "-8234.789063 -41271.058594 12139.614258", 
                                "param1": "20000262"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "a1"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "a1到达60S循环开始", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1|2|4"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "a1"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "a1"
                            }
                        ], 
                        "id": 3
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "玩家进入范围召怪计时", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "a1"
                                }
                            ], 
                            "EID": [
                                4
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Role"
                                }
                            ], 
                            "id": 4
                        }
                    ]
                }, 
                "initiativeAreaXZ": "15.000000", 
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