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
                "name": "收到镜头的指令，改变模型", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "移动到某个坐标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction1", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "10", 
                                "param2": "1", 
                                "param1": "-43011.0 -26000.0 -206.0"
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
                                "param1": "tt"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "到达位置   改变朝向", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction26", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0 0 87"
                            }
                        ], 
                        "EID": [
                            4, 
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "-43011.0 -26000.0 -206.0"
                            }
                        ], 
                        "id": 4
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到镜头的指令，播放战斗待机动作", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Idle_Fight"
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
                                    "param2": "1234", 
                                    "param1": ""
                                }
                            ], 
                            "id": 1
                        }, 
                        {
                            "comment": "收到指令，记录tt", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "tt"
                                }
                            ], 
                            "EID": [
                                2
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12345", 
                                    "param1": ""
                                }
                            ], 
                            "id": 2
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