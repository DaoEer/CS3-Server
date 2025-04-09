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
                            "comment": "四号攻城梯进入时，向刀盾兵将领发送指令（废弃）", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12540", 
                                    "param1": "20012588"
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
                                    "param3": "20012567", 
                                    "param2": "MonsterExtAttackCityLadder", 
                                    "param1": "7"
                                }
                            ], 
                            "id": 1
                        }, 
                        {
                            "comment": "四号攻城梯进入时，给副本发送指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction59", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1015"
                                }, 
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1052", 
                                    "param1": "20012531"
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
                                3
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition68", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "20012567", 
                                    "param2": "MonsterExtAttackCityLadder", 
                                    "param1": "7"
                                }
                            ], 
                            "id": 3
                        }
                    ], 
                    9: [
                        {
                            "comment": "收到 1014 设置 EAI  3 4", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [
                                3, 
                                4
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1014"
                                }
                            ], 
                            "id": 4
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "检测攻城梯状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "攻城梯有 12210502 buff，给20012567 发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "12567", 
                                "param2": "20012567", 
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
                                "param4": "20012567", 
                                "param3": "MonsterExtAttackCityLadder", 
                                "param2": "12210502", 
                                "param1": "7"
                            }
                        ], 
                        "id": 2
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