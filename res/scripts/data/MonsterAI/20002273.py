# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "show": {
        "subStateDatas": {
            1: {
                "name": "走进泉水", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "移动到指定位置", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction1", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "-3413.0 10538.0 2512.0"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "L_FLS_Planes003", 
                                "param2": "1", 
                                "param1": "-3413.0 10538.0 2512.0"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "到达指定位置，切换状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "L_FLS_Planes003", 
                                "param2": "1", 
                                "param1": "-3413.0 10538.0 2512.0"
                            }
                        ], 
                        "id": 4
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到大巫巫承死亡通知，设置标记xx", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "xx"
                                }
                            ], 
                            "EID": [
                                1
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "44", 
                                    "param1": ""
                                }
                            ], 
                            "id": 1
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "开始酿造神水", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "坐下，开始表演。记录t1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction70", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1.833|50", 
                                "param1": "show_01|show_02"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }
                        ], 
                        "EID": [
                            5
                        ], 
                        "Conditions": [], 
                        "id": 5
                    }, 
                    {
                        "comment": "t1=3,通知副本101，开始刷怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "101"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "3", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 9
                    }, 
                    {
                        "comment": "播放一系列动作，计时xiong", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction70", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1.7|1|1.8", 
                                "param1": "Show_03|Idel_Free|Show_15"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "xiong"
                            }
                        ], 
                        "EID": [
                            12
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "xx"
                            }, 
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "5"
                            }
                        ], 
                        "id": 12
                    }, 
                    {
                        "comment": "3秒给副本发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "666"
                            }
                        ], 
                        "EID": [
                            13
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "3", 
                                "param1": "xiong"
                            }
                        ], 
                        "id": 13
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到大巫巫承死亡通知，设置标记xx", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "xx"
                                }, 
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Q030124", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [
                                8
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "44", 
                                    "param1": ""
                                }
                            ], 
                            "id": 8
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
    "FSM": 2, 
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
                        "comment": "一定范围内的玩家没有传送保护，进入表演状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction61", 
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
                                "script": "AICondition37", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "Role", 
                                "param2": "12345607", 
                                "param1": "50"
                            }
                        ], 
                        "id": 2
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令，进入表演状态", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction61", 
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
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "123", 
                                    "param1": ""
                                }
                            ], 
                            "id": 11
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
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}