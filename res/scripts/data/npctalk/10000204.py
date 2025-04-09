# -*- coding: utf-8 -*-
Datas = {
    "10000204": {
        "talks": [
            {
                "msg": "@F{n=/Game/miscs/Fonts/SIMLI;fc=c18; fs=20;ft=Regular }@S{6}试炼秘境@F{n=/Game/miscs/Fonts/SIMLI;fc=c18; fs=20;ft=Regular }@B玩法规则@F{n=/Game/miscs/Fonts/msyh;fc=c2; fs=12;ft=Regular }@B@B@S{4}20级试炼秘境副本群由三个副本组成，每次挑战将随机进入一个副本。@B@B@S{4}若能成功通关，则有机会挑战其余副本，获取更多奖励。@B@B@S{4}试炼副本有大量经验奖励，若你在主线任务中遇到经验瓶颈，欢迎前来挑战。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "cs2", 
                        "title": "开启试炼秘境（单人体验）"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs1", 
                        "title": "开启试炼秘境"
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
                                "param1": "C000067"
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
                                "key": "TCEnterChuanChengBunch", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "BunchSpace_1"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TAEnterChuanChengBunchSpace", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "BunchSpace_1"
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
                                "key": "TCEnterChuanChengBunch", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "BunchSpace_1_1"
                            }, 
                            {
                                "key": "TCQuestStatus", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20101230:3;1:3|20101201:3;1:3|20101704:3;1:3|20101705:3;1:3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TAEnterChuanChengBunchSpace", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "BunchSpace_1_1"
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
                        "param1": "20101230:3;1:3|20101201:3;1:3|20101704:3;1:3|20101705:3;1:3"
                    }
                ]
            }
        ], 
        "npcID": "10000204"
    }
}