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
                "name": "检测玩家身上保护buff", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "玩家进入道场，提示变身喊话。", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Q030767", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "10"
                            }
                        ], 
                        "id": 1
                    }, 
                    {
                        "comment": "玩家身上有伪装友好，移除变身提示", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction74", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "Role", 
                                "param2": "11001310", 
                                "param1": "20"
                            }, 
                            {
                                "script": "AIAction44", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "11003618"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "Role", 
                                "param2": "11001310", 
                                "param1": "20"
                            }
                        ], 
                        "id": 2
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0", 
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