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
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "玩家人数多1个，请求1个支援", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "12530", 
                                "param1": "20012501"
                            }
                        ], 
                        "EID": [
                            4
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AICondition122", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "玩家人数多2个，请求2个支援", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "12530", 
                                "param1": "20012497|20012501"
                            }
                        ], 
                        "EID": [
                            5
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AICondition122", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "暂时废弃，玩家人数多3个，请求3个支援", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "12530", 
                                "param3": "1", 
                                "param2": "20012497|20012501", 
                                "param1": "3"
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "t3"
                            }, 
                            {
                                "script": "AICondition122", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "清除t1时间标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1|4"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "16", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 7
                    }, 
                    {
                        "comment": "清除t2时间标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|5"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "16", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": "暂时废弃，清除t2时间标签", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3|6"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t3"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "16", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 9
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "4个人，叫一个支援", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12530", 
                                    "param1": "20012501"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition29", 
                                    "param5": "4", 
                                    "param4": "0", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "35"
                                }
                            ], 
                            "id": 10
                        }, 
                        {
                            "comment": "5个人，叫两个支援", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12530", 
                                    "param1": "20012497|20012501"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition29", 
                                    "param5": "5", 
                                    "param4": "0", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "35"
                                }
                            ], 
                            "id": 11
                        }, 
                        {
                            "comment": "暂时废弃，5个人，叫三个支援", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction288", 
                                    "param5": "", 
                                    "param4": "12530", 
                                    "param3": "1", 
                                    "param2": "20012497|20012501", 
                                    "param1": "3"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition29", 
                                    "param5": "5", 
                                    "param4": "0", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "35"
                                }
                            ], 
                            "id": 12
                        }, 
                        {
                            "comment": "收到查询指令，检查有没有玩家在附近", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12530", 
                                    "param1": "20012512"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12512"
                                }, 
                                {
                                    "script": "AICondition21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "50"
                                }
                            ], 
                            "id": 13
                        }
                    ], 
                    12: [
                        {
                            "comment": "4个人，叫一个支援，记录t1", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }, 
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12530", 
                                    "param1": "20012497"
                                }
                            ], 
                            "EID": [
                                1
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition29", 
                                    "param5": "4", 
                                    "param4": "0", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "60"
                                }
                            ], 
                            "id": 1
                        }, 
                        {
                            "comment": "5个人，叫2个支援，记录t2", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t2"
                                }, 
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12530", 
                                    "param1": "20012501"
                                }
                            ], 
                            "EID": [
                                2
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition29", 
                                    "param5": "5", 
                                    "param4": "0", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "60"
                                }
                            ], 
                            "id": 2
                        }, 
                        {
                            "comment": "暂时废弃，5个人，叫3个支援，记录t3", 
                            "odds": 0.0, 
                            "Actions": [
                                {
                                    "script": "AIAction288", 
                                    "param5": "", 
                                    "param4": "12530", 
                                    "param3": "1", 
                                    "param2": "20012497|20012501", 
                                    "param1": "3"
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t3"
                                }
                            ], 
                            "EID": [
                                3
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition29", 
                                    "param5": "5", 
                                    "param4": "0", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "35"
                                }
                            ], 
                            "id": 3
                        }
                    ]
                }, 
                "initiativeAreaXZ": "40", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}