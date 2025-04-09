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
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "落地", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction293", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            11
                        ], 
                        "Conditions": [], 
                        "id": 11
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
        "subStateDatas": {
            1: {
                "name": "战斗状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "feitian"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [], 
                        "id": 2
                    }, 
                    {
                        "comment": "落地结束移除霸体移除浮空标志位回到1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction39", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "9"
                            }
                        ], 
                        "EID": [
                            4
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12192604"
                            }, 
                            {
                                "script": "AICondition92", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "feitian"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "对目标位置放技能", 
                        "odds": 0.899999976158, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121929001"
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
                                "param1": "2"
                            }
                        ], 
                        "id": 8
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "被蛛网射中落地", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12192604"
                                }, 
                                {
                                    "script": "AIAction283", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "2.5", 
                                    "param2": "2", 
                                    "param1": "-10"
                                }, 
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "feitian"
                                }
                            ], 
                            "EID": [
                                6
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "zhuwang", 
                                    "param1": ""
                                }
                            ], 
                            "id": 6
                        }
                    ], 
                    23: [
                        {
                            "comment": "飞天（落地）结束清除飞天（落地）buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction43", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12192603|12192604"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition127", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "0", 
                                    "param1": "23"
                                }
                            ], 
                            "id": 7
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
    "free": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}