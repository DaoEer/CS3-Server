# -*- coding: utf-8 -*-
Datas = {
    "10000629": {
        "talks": [
            {
                "msg": "@F{n=/Game/miscs/Fonts/SIMLI;fc=c18; fs=15;ft=Regular }@S{16}万象仙府@F{n=/Game/miscs/Fonts/msyh;fc=c2; fs=11;ft=Regular }@B@B@S{4}万象仙府机缘与挑战并存，开始你的修行之旅吧。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "qifei", 
                        "title": "开始挑战"
                    }, 
                    {
                        "type": 0, 
                        "key": "jiangli", 
                        "title": "领取通关奖励"
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
                                "key": "TASpaceCopyMagicMazeFlyToSubSpace", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "4000"
                            }
                        ]
                    }
                ], 
                "key": "qifei", 
                "visibles": [
                    {
                        "key": "TVSpaceCopyMagicMazeHide", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "3"
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
                                "key": "TAGetRewardByLevel", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "23:29|30:39|40:99", 
                                "param2": "205040052|205040053|205040054", 
                                "param1": "3"
                            }
                        ]
                    }
                ], 
                "key": "jiangli", 
                "visibles": [
                    {
                        "key": "TVValidatePotentialSpaceReward", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "3"
                    }
                ]
            }
        ], 
        "npcID": "10000629"
    }
}