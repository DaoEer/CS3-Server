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
                "name": "检测", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "玩家失去保护Buff，通知附近的小怪攻击/喊话\\n魔道鼠辈！敢来五庄观撒野，葬身在幻阵之中吧！", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1", 
                                    "param2": "20002563|20002564", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [
                                4
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Role"
                                }
                            ], 
                            "id": 4
                        }
                    ]
                }, 
                "initiativeAreaXZ": "5.000000", 
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