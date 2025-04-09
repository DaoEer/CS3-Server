# -*- coding: utf-8 -*-
Datas = {
    "10000105": {
        "talks": [
            {
                "msg": "Q017157", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "KYDF", 
                        "title": "前往开阳洞府"
                    }, 
                    {
                        "type": 0, 
                        "key": "RYDD", 
                        "title": "前往熔岩地洞"
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
                                "param1": "20102677:3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -50", 
                                "param2": "-24971.708984 1356.114258 1385.470947", 
                                "param1": "L_KYDF"
                            }
                        ]
                    }
                ], 
                "key": "KYDF", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "20102677:3"
                    }
                ]
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
                                "param1": "20102678:3|20102679:3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -180", 
                                "param2": "12259.74707 -2343.082031 3172.076172", 
                                "param1": "L_RYDD"
                            }
                        ]
                    }
                ], 
                "key": "RYDD", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "20102678:3|20102679:3"
                    }
                ]
            }
        ], 
        "npcID": "10000105"
    }
}