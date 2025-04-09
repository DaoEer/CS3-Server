# -*- coding: utf-8 -*-
Datas = {
    "10000224": {
        "talks": [
            {
                "msg": "Q017083", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "Shop", 
                        "title": "购买药品"
                    }, 
                    {
                        "type": 0, 
                        "key": "caibaoding", 
                        "title": "我是来挑战猜宝鼎的。"
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
                                "param1": "FMCyaopin"
                            }
                        ]
                    }
                ], 
                "key": "Shop", 
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
                                "param1": "80135025:3;2:3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TAEnterPlane", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "FMC_yaopin_shop"
                            }
                        ]
                    }
                ], 
                "key": "caibaoding", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "80135025:3;2:3"
                    }
                ]
            }
        ], 
        "npcID": "10000224"
    }
}