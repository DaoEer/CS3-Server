# -*- coding: utf-8 -*-
Datas = {
    "10001351": {
        "talks": [
            {
                "msg": "@S{4}欢迎来到轮回秘境，我是这里的指引导师水清清。@B@B@S{4}在这个秘境中，你可以捕捉到心仪的幻兽，建造私人洞府，并且还能打造稀有绿装。@B@B@S{4}想了解具体的玩法，可查阅下列介绍。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "huanshou", 
                        "title": "如何获得幻兽？"
                    }, 
                    {
                        "type": 0, 
                        "key": "dongfu", 
                        "title": "如何建造洞府？"
                    }, 
                    {
                        "type": 0, 
                        "key": "linglong", 
                        "title": "没有洞府怎么办？"
                    }, 
                    {
                        "type": 0, 
                        "key": "luopan", 
                        "title": "获取灵气罗盘"
                    }, 
                    {
                        "type": 0, 
                        "key": "chuansong", 
                        "title": "返回凤鸣城"
                    }
                ], 
                "functions": [], 
                "key": "Talk", 
                "visibles": []
            }, 
            {
                "msg": "@S{4}从轮回秘境的第二层开始，便有妖兽凶禽出没，将它们消灭就有几率可获得原兽。@B@B@S{4}原兽即是尚未驯服的野生幻兽，按照品质分为凡兽、灵兽和圣兽。凡兽捕捉后即可迅速将其驯服为你所用，但灵兽和圣兽野性难驯，必须先在洞府兽栏或玲珑仙府贵宝处驯养一番后，方可驱使。@B@B@S{4}注意！原兽只在每日的19:00-20:00才会掉落。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "Talk", 
                        "title": "返回上一页"
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
                                "param1": "C001520"
                            }
                        ]
                    }
                ], 
                "key": "huanshou", 
                "visibles": []
            }, 
            {
                "msg": "@S{4}洞府是稀有资源。在轮回秘境第一层，仅有200个洞府福地，它们都隐藏在地表之下，需借助我的灵气罗盘才能找到它们的位置。只要占领了福地，并收集到相应的建筑材料即可建造自己的洞府。@B@B@S{4}洞府建成之后，便可在府内驯养原兽，打造稀有绿装，炼制药品，开辟灵田种植灵花异草等等！总而言之，拥有洞府，便是身份的象征。@B@B@S{4}注意！每周六20:00-20:15将开启洞府争夺战，届时你可以争夺别人的洞府。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "Talk", 
                        "title": "返回上一页"
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
                                "param1": "C001521"
                            }
                        ]
                    }
                ], 
                "key": "dongfu", 
                "visibles": []
            }, 
            {
                "msg": "@S{4}若你没能建立属于自己的洞府，也不用太过担心。在前面不远处有一座玲珑仙府，府内各种设施齐全。只要你能获得玲珑真人的认可，得到他赐下的玲珑玉令，就可以在玲珑仙府中驯养原兽、打造稀有绿装、炼制药品等！", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "Talk", 
                        "title": "返回上一页"
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
                                "param1": "C001522"
                            }
                        ]
                    }
                ], 
                "key": "linglong", 
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
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -86.5", 
                                "param2": "23614.0 21573.0 12230.0", 
                                "param1": "L_FMC"
                            }
                        ]
                    }
                ], 
                "key": "chuansong", 
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
                                "param1": "303020008"
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
                "key": "luopan", 
                "visibles": [
                    {
                        "key": "TVPlayerOccupySpaceType", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "0", 
                        "param1": "1|3"
                    }
                ]
            }
        ], 
        "npcID": "10001351"
    }
}