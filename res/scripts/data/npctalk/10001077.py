# -*- coding: utf-8 -*-
Datas = {
    "10001077": {
        "talks": [
            {
                "msg": "Q017217", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "CS_CSG", 
                        "title": "前往藏书阁"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_SLD", 
                        "title": "前往神龙道"
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
                                "param1": "20102653:3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-180.0 0.0 2030.0", 
                                "param1": "L_CSG"
                            }
                        ]
                    }
                ], 
                "key": "CS_CSG", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "20102653:3"
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
                                "param1": "20102652:3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -120", 
                                "param2": "328570.0 -297650.0 6260.0", 
                                "param1": "L_SLD"
                            }
                        ]
                    }
                ], 
                "key": "CS_SLD", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "20102653:3"
                    }
                ]
            }
        ], 
        "npcID": "10001077"
    }
}