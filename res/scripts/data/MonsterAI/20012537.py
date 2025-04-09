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
                "name": "自由状态", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    8: [
                        {
                            "comment": "一号攻城梯进入时，向刀盾兵将领发送指令（废弃）", 
                            "odds": 0.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12537", 
                                    "param1": "20012586"
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
                            "EID": [
                                1
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition68", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "20012564", 
                                    "param2": "MonsterExtAttackCityLadder", 
                                    "param1": "7"
                                }
                            ], 
                            "id": 1
                        }, 
                        {
                            "comment": "一号攻城梯进入时，给副本发送指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction59", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1013"
                                }, 
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1052", 
                                    "param1": "20012530"
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
                            "EID": [
                                5
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition68", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "20012564", 
                                    "param2": "MonsterExtAttackCityLadder", 
                                    "param1": "7"
                                }
                            ], 
                            "id": 5
                        }
                    ], 
                    9: [
                        {
                            "comment": "收到 1012 设置 5 6 EAI", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [
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
                                    "param1": "1012"
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
            }, 
            2: {
                "name": "检测攻城梯BUFF", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "攻城梯有 12210502 buff，给20012564 发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "12564", 
                                "param2": "20012564", 
                                "param1": "7"
                            }, 
                            {
                                "script": "AIAction32", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0.5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "20012564", 
                                "param3": "MonsterExtAttackCityLadder", 
                                "param2": "12210502", 
                                "param1": "7"
                            }
                        ], 
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
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}