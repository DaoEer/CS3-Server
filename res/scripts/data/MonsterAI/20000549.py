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
            2: {
                "name": "光墙结界", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "精英死亡通知boss 销毁", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "450", 
                                "param2": "20000553", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction32", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition22", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20000550|20000551|20000552", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 9
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "50.000000", 
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