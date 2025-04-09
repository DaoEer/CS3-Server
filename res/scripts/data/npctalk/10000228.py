# -*- coding: utf-8 -*-
Datas = {
    "10000228": {
        "talks": [
            {
                "msg": "Q017151", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "dakai", 
                        "title": "购买首饰"
                    }, 
                    {
                        "type": 0, 
                        "key": "mofadan", 
                        "title": "金前辈，我来挑战驭火打靶。"
                    }
                ], 
                "functions": [], 
                "key": "Talk", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TAOpenShop", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "FMCshipin"
                            }
                        ]
                    }
                ], 
                "key": "dakai", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [
                            {
                                "key": "TCQuestStatus", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "80135058:3;2:3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 50", 
                                "param2": "44209.597656 27779.882813 14517.071289", 
                                "param1": "L_FMC_Planes203"
                            }
                        ]
                    }
                ], 
                "key": "mofadan", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "80135058:3;2:3"
                    }
                ]
            }
        ], 
        "npcID": "10000228"
    }
}