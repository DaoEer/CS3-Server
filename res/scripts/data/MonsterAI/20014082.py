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
                        "comment": "发送死亡指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "12561", 
                                "param2": "20012517", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 4
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
                "name": "子状态", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到没有弹药指令，告诉将领不能操控器械", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12561", 
                                    "param2": "20014088|20014089|20014090", 
                                    "param1": "5"
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
                                    "param1": "NoAmmo"
                                }
                            ], 
                            "id": 1
                        }, 
                        {
                            "comment": "有子弹时，切换状态2", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction267", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "30", 
                                    "param2": "50", 
                                    "param1": "0"
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
                            "id": 2
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
                                    "param2": "20014088|20014089|20014090", 
                                    "param1": "10"
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
                            "id": 8
                        }
                    ]
                }, 
                "initiativeAreaXZ": "65|15", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "发送状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "有AI目标，开炮，发送指令，切换等级1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction254", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122108001"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "12561", 
                                "param2": "20014088|20014089|20014090", 
                                "param1": "5"
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
                                "param3": "30", 
                                "param2": "50", 
                                "param1": "0"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "没有目标，设置目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction267", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "30", 
                                "param2": "50", 
                                "param1": "0"
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
                        "comment": "有玩家发送下器械指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "12561", 
                                "param2": "20014088|20014089|20014090", 
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
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "5"
                            }
                        ], 
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
    "pead": {
        "subStateDatas": {
            1: {
                "name": "霸体", 
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
                            6
                        ], 
                        "Conditions": [], 
                        "id": 6
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
    }
}