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
                "name": "特殊战斗状态（远程）", 
                "tickTimer": 3.0, 
                "statesAI": [
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
                        "id": 1
                    }, 
                    {
                        "comment": "远程技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction42", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "101128001|101129001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 2
                    }
                ], 
                "eventsAI": {
                    1: [
                        {
                            "comment": "敌人列表有玩家进入真实打", 
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
                            "EID": [
                                14, 
                                11
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "id": 14
                        }
                    ], 
                    5: [
                        {
                            "comment": "清除敌人列表，重新寻找可攻击的敌人", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction33", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 3
                        }
                    ], 
                    6: [
                        {
                            "comment": "生命值低于30%回复到80", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction164", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "80"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "30"
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
    "free": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}