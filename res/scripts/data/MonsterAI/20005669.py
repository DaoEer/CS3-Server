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
                "name": "符文印记", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "检测玩家身上是否有金印记，清除金印记\\添加烙印", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction74", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "Role", 
                                "param2": "14011616", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction44", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14011616"
                            }, 
                            {
                                "script": "AIAction34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "140116019"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Cy000317", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "Role", 
                                "param2": "14011616", 
                                "param1": "5"
                            }
                        ], 
                        "id": 1
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到boss通知，播放光效", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction91", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "100984"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "501", 
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