# -*- coding: utf-8 -*-
Datas = {
    "10000419": {
        "talks": [
            {
                "msg": "@S{2}@F{fc=c36}欢迎来到人参果园。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "pickup", 
                        "title": "摘取人参果"
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
                        "conditions": [
                            {
                                "key": "TCQuestStatus", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "80135030:3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-270.00006 6180.0 210.0", 
                                "param1": "cycle_L_RSGY"
                            }
                        ]
                    }
                ], 
                "key": "pickup", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "80135030:3"
                    }
                ]
            }
        ], 
        "npcID": "10000419"
    }
}