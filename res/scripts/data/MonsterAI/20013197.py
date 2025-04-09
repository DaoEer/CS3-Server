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
                        "comment": "死亡发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "12561", 
                                "param2": "20012584|20012585|20012586|20012587|20012588", 
                                "param1": "5|2"
                            }
                        ], 
                        "EID": [
                            8
                        ], 
                        "Conditions": [], 
                        "id": 8
                    }, 
                    {
                        "comment": "发送取消移动指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2554", 
                                "param1": "20012584|20012585|20012586|20012587|20012588"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 14
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
                "name": "状态", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
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
                                    "param2": "70", 
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
                            "id": 1
                        }, 
                        {
                            "comment": "发送指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12561", 
                                    "param2": "20013187|20013188|20013189|20013190", 
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
                            "id": 7
                        }
                    ], 
                    12: [
                        {
                            "comment": "有玩家", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction280", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12554", 
                                    "param2": "20012543", 
                                    "param1": "79"
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
                                    "param1": "70|30"
                                }
                            ], 
                            "id": 9
                        }, 
                        {
                            "comment": "有攻城梯", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction280", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12554", 
                                    "param2": "20012543", 
                                    "param1": "79"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "MonsterExtAttackCityLadder", 
                                    "param1": "70|30"
                                }
                            ], 
                            "id": 10
                        }, 
                        {
                            "comment": "有撞车", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction280", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12554", 
                                    "param2": "20012543", 
                                    "param1": "79"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "MonsterExtCollisionCar", 
                                    "param1": "70|30"
                                }
                            ], 
                            "id": 13
                        }
                    ]
                }, 
                "initiativeAreaXZ": "65", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 4
            }, 
            2: {
                "name": "被操控", 
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
                                "param1": "122107001|122107002|122107003|122107004"
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
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "id": 2
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
                                "param2": "70", 
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
                        "id": 3
                    }, 
                    {
                        "comment": "没有目标，记录时间", 
                        "odds": 1.0, 
                        "Actions": [
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
                            4
                        ], 
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
                        "id": 4
                    }, 
                    {
                        "comment": "10秒内，没有AI目标，跳回常规状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "12561", 
                                "param2": "20012584|20012585|20012586|20012587|20012588", 
                                "param1": "5|2"
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "7"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "t1"
                            }, 
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
                        "comment": "有AI目标，移除时间", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "7"
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
                                "script": "AICondition104", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 6
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
                                    "param2": "20012584|20012585|20012586|20012587|20012588", 
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
                            "id": 11
                        }, 
                        {
                            "comment": "收到 1004 发送 12561 指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12561", 
                                    "param2": "20012584|20012585|20012586|20012587|20012588", 
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
                                    "param1": "1004"
                                }
                            ], 
                            "id": 15
                        }
                    ], 
                    12: [
                        {
                            "comment": "发送指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "12561", 
                                    "param2": "20012584|20012585|20012586|20012587|20012588", 
                                    "param1": "5|3"
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
                                    "param1": "12"
                                }
                            ], 
                            "id": 12
                        }
                    ]
                }, 
                "initiativeAreaXZ": "5.0", 
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