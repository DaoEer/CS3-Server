# -*- coding: utf-8 -*-
Datas = {
    "10000205": {
        "talks": [
            {
                "msg": "@F{n=/Game/miscs/Fonts/SIMLI;fc=c18; fs=20;ft=Regular }@S{6}潜能幻境@F{n=/Game/miscs/Fonts/SIMLI;fc=c18; fs=20;ft=Regular }@B玩法规则@F{n=/Game/miscs/Fonts/msyh;fc=c2; fs=12;ft=Regular }@B@B@S{4}25级潜能幻境副本群由三个副本组成，每次挑战将随机进入一个副本。@B@B@S{4}若能成功通关，则有机会挑战其余副本，获取更多奖励。@B@B@S{4}潜能副本有大量潜能奖励，若你需要潜能修行功法，欢迎前来挑战。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "cs2", 
                        "title": "开启潜能幻境（单人体验）"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs1", 
                        "title": "开启潜能幻境"
                    }
                ], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TAPlayGossipVoice", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "C000068"
                            }
                        ]
                    }
                ], 
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
                                "key": "TCEnterPotentailBunch", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "25", 
                                "param1": "BunchSpace_2"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TAEnterPotentailBunchSpace", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "25", 
                                "param1": "BunchSpace_2"
                            }
                        ]
                    }
                ], 
                "key": "cs1", 
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
                                "key": "TCEnterPotentailBunch", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "25", 
                                "param1": "BunchSpace_2_1"
                            }, 
                            {
                                "key": "TCQuestStatus", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20101210:3;1:3|20101226:3;1:3|20101720:3;1:3|20101721:3;1:3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TAEnterPotentailBunchSpace", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "25", 
                                "param1": "BunchSpace_2_1"
                            }
                        ]
                    }
                ], 
                "key": "cs2", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "20101210:3;1:3|20101226:3;1:3|20101720:3;1:3|20101721:3;1:3"
                    }
                ]
            }
        ], 
        "npcID": "10000205"
    }
}