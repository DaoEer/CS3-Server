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
                "name": "对话", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    17: [
                        {
                            "comment": "妖魔对话", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction126", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "t3|抱歉，打扰了|0", 
                                    "param2": "t1|妖魔还不速速现形！|0", 
                                    "param1": "上师请问有什么事吗？"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition56", 
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
                            "comment": "非妖魔对话", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction126", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "t3|抱歉，打扰了|0", 
                                    "param2": "t2|妖魔还不速速现形！|0", 
                                    "param1": "上师，请问有什么事吗？"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition57", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "id": 10
                        }
                    ], 
                    18: [
                        {
                            "comment": "妖魔对话", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction129", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Cy000139", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [
                                8
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition58", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }
                            ], 
                            "id": 8
                        }, 
                        {
                            "comment": "非妖魔对话", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction126", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "t4|是我鲁莽了，待我捋清思绪从头来过。|0", 
                                    "param1": "上…上师饶命，小人乃是地地道道的人族，还望上师明鉴！"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition58", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t2"
                                }
                            ], 
                            "id": 11
                        }, 
                        {
                            "comment": "t3关闭对话框", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction129", 
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
                                    "script": "AICondition58", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t3"
                                }
                            ], 
                            "id": 13
                        }, 
                        {
                            "comment": "t4错误惩罚并且关闭对话框", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction129", 
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
                                    "script": "AICondition58", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t4"
                                }
                            ], 
                            "id": 15
                        }, 
                        {
                            "comment": "t3关闭对话框", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction129", 
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
                                    "script": "AICondition58", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t3"
                                }
                            ], 
                            "id": 16
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