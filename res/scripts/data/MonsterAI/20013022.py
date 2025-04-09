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
                                "param2": "20012507|20012508|20012511", 
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
                            9
                        ], 
                        "Conditions": [], 
                        "id": 9
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "有子弹时，切换状态2", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction267", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "30", 
                                    "param2": "30", 
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
                        }, 
                        {
                            "comment": "收到没有弹药指令，告诉将领不能操控器械", 
                            "odds": 0.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12561", 
                                    "param2": "20013030|20013031|20013032|20013033|20013040|20013233|20013234|20013235|20013236|20013237", 
                                    "param1": "10"
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
                                    "param1": "40"
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
                "name": "发射状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "设置目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction267", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "30", 
                                "param2": "30", 
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
                        "comment": "有AI目标，开炮，发送指令，切换等级1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction254", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122109001"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "12561", 
                                "param2": "20013030|20013031|20013032|20013033|20013040|20013233|20013234|20013235|20013236|20013237", 
                                "param1": "10"
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
                                "param2": "30", 
                                "param1": "0"
                            }
                        ], 
                        "id": 3
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
    }
}