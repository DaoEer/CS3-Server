# -*- coding: utf-8 -*-
Datas = {
    "10001405": {
        "talks": [
            {
                "msg": "@S{4}主人您好，我是佟贞，我负责管理洞府的门户，若您想要暂时离开洞府，可以来找我，我可以送您出去。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "likai", 
                        "title": "离开洞府"
                    }, 
                    {
                        "type": 0, 
                        "key": "fuyin", 
                        "title": "领取洞府符印"
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
                                "key": "TALeaveDongFuSpace", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "L_LHMJ_1"
                            }
                        ]
                    }
                ], 
                "key": "likai", 
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
                                "key": "TAItem", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "205010025"
                            }, 
                            {
                                "key": "TAClose", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ]
                    }
                ], 
                "key": "fuyin", 
                "visibles": [
                    {
                        "key": "TVPlayerHasItems", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "0", 
                        "param2": "1", 
                        "param1": "205010025"
                    }
                ]
            }
        ], 
        "npcID": "10001405"
    }
}