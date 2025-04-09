# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 1, 
    "dead": {
        "subStateDatas": {
            1: {
                "name": "死亡", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "无", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "12608", 
                                "param2": "20012608", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [
                            7
                        ], 
                        "Conditions": [], 
                        "id": 7
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "fight": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "检测状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "添加霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10000001"
                            }
                        ], 
                        "EID": [
                            12
                        ], 
                        "Conditions": [], 
                        "id": 12
                    }
                ], 
                "eventsAI": {
                    8: [
                        {
                            "comment": "有玩家", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12547", 
                                    "param2": "20013030|20013031|20013032|20013033|20013040|20013233|20013234|20013235|20013236|20013237", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "120|30"
                                }
                            ], 
                            "id": 1
                        }
                    ], 
                    9: [
                        {
                            "comment": "切换子状态", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction267", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "30", 
                                    "param2": "120", 
                                    "param1": "10"
                                }, 
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
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ReadyFire"
                                }
                            ], 
                            "id": 3
                        }
                    ], 
                    12: [
                        {
                            "comment": "有玩家", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12547", 
                                    "param2": "20013030|20013031|20013032|20013033|20013040|20013233|20013234|20013235|20013236|20013237", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "120|30"
                                }
                            ], 
                            "id": 11
                        }
                    ]
                }, 
                "initiativeAreaXZ": "65|15", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 1, 
                "initiativeTrapShape": 4
            }, 
            2: {
                "name": "工作状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "有AI目标，判断能否开炮", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction254", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122107005|122107006|122107007|122107008"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "zd1", 
                                "param2": "20013240|20013029", 
                                "param1": "50|20"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition104", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AICondition106", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20", 
                                "param2": "100", 
                                "param1": "20"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "没有 AI目标，执行设置AI目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction267", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "30", 
                                "param2": "120", 
                                "param1": "10"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition105", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "指令", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "zd1", 
                                "param2": "20013240|20013029", 
                                "param1": "50|20"
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [], 
                        "id": 9
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "发送指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12561", 
                                    "param2": "20013030|20013031|20013032|20013033|20013040|20013233|20013234|20013235|20013236|20013237", 
                                    "param1": "10"
                                }, 
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1"
                                }
                            ], 
                            "EID": [
                                1, 
                                2, 
                                3, 
                                4, 
                                5, 
                                6
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "NoAmmo"
                                }
                            ], 
                            "id": 6
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
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