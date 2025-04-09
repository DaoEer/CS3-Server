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
                "name": "传送门播放镜头陷阱", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "根据玩家任务状态，播放传送门镜头（剑客）", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction111", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "110000119"
                                }, 
                                {
                                    "script": "AIAction119", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101506"
                                }, 
                                {
                                    "script": "AIAction112", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "5", 
                                    "param1": "20101506"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition49", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1:3", 
                                    "param2": "3", 
                                    "param1": "20101506"
                                }, 
                                {
                                    "script": "AICondition45", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101506"
                                }, 
                                {
                                    "script": "AICondition45", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101506"
                                }
                            ], 
                            "id": 1
                        }, 
                        {
                            "comment": "根据玩家任务状态，播放传送门镜头（战士）", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction111", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "110000119"
                                }, 
                                {
                                    "script": "AIAction119", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101525"
                                }, 
                                {
                                    "script": "AIAction112", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "5", 
                                    "param1": "20101525"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition49", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1:3", 
                                    "param2": "3", 
                                    "param1": "20101525"
                                }, 
                                {
                                    "script": "AICondition45", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101525"
                                }, 
                                {
                                    "script": "AICondition45", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101525"
                                }
                            ], 
                            "id": 3
                        }, 
                        {
                            "comment": "根据玩家任务状态，播放传送门镜头（链刃）", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction111", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "110000119"
                                }, 
                                {
                                    "script": "AIAction119", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101526"
                                }, 
                                {
                                    "script": "AIAction112", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "5", 
                                    "param1": "20101526"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition49", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1:3", 
                                    "param2": "3", 
                                    "param1": "20101526"
                                }, 
                                {
                                    "script": "AICondition11", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "110000119"
                                }, 
                                {
                                    "script": "AICondition45", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101526"
                                }
                            ], 
                            "id": 4
                        }, 
                        {
                            "comment": "根据玩家任务状态，播放传送门镜头（法师）", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction111", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "110000119"
                                }, 
                                {
                                    "script": "AIAction119", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101527"
                                }, 
                                {
                                    "script": "AIAction112", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "5", 
                                    "param1": "20101527"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition49", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1:3", 
                                    "param2": "3", 
                                    "param1": "20101527"
                                }, 
                                {
                                    "script": "AICondition45", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20101527"
                                }
                            ], 
                            "id": 5
                        }
                    ]
                }, 
                "initiativeAreaXZ": "9.000000", 
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