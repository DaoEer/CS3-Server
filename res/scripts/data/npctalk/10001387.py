# -*- coding: utf-8 -*-
Datas = {
    "10001387": {
        "talks": [
            {
                "msg": "@S{4}主人，我是洞府的长老，负责维护灵泉的运转，并且管理洞府的各个建筑的建造和升级。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "lingqing", 
                        "title": "打开灵泉"
                    }, 
                    {
                        "type": 0, 
                        "key": "xiufu", 
                        "title": "修复灵泉"
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
                                "key": "TAOpenLingQuanUI", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ]
                    }
                ], 
                "key": "lingqing", 
                "visibles": [
                    {
                        "key": "TVDFBuildIsDestroy", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "0", 
                        "param1": "1"
                    }
                ]
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
                                "key": "TAOpenRepairBuildUI", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ]
                    }
                ], 
                "key": "xiufu", 
                "visibles": [
                    {
                        "key": "TVDFBuildIsDestroy", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "1", 
                        "param1": "1"
                    }
                ]
            }
        ], 
        "npcID": "10001387"
    }
}