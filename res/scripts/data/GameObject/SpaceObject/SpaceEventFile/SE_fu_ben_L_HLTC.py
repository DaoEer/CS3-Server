# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "刷宝箱金莲", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 0|0 0 0|0 0 0|0 0 0|0 0 0|0 0 0|0 0 0|0 0 0", 
                    "param2": "-10093 -15854 621|-11102 -1868 584|-1763 6632 578|12908 1468 623|19489 -8959 686|693 -8184 617|5237 -28767 675|12702 11018 578", 
                    "param1": "40000129:4|40000132:4", 
                    "param4": "", 
                    "id": 118
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "阶段一复活点", 
            "describe": "阶段一复活点", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-8308 -27045 615", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "喊话提醒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "60", 
                    "param1": "hanhua1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "70", 
                    "param1": "hanhua2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 90.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001965", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "副本失败计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "900", 
                    "param1": "shibai", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 4
        }
    ], 
    2: [
        {
            "title": "喊话1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000442", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "hanhua1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "喊话2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000444", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "hanhua2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "20秒86boss去标志位", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "86", 
                    "param1": "20006703", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "boss", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "5秒刷传送门1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "40000167:1", 
                    "param2": "0 0 0", 
                    "param1": "-16693 49665 7763", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "chuanso", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "时间到达未完成副本436", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 436
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 4
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "shibai", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    5: [
        {
            "title": "阶段4未完成杀boss通过436", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 436
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000556:1", 
                    "param2": "0 0 -137.5", 
                    "param1": "20898 5337 469", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 -137.5", 
                    "param1": "21645 6034 601", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "cc", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20006703", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "阶段2复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 1
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "20625 5185 625", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "1", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 36, 
                    "param1": "40000132", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "阶段3复活点发86boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 1
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 131", 
                    "param1": "-18146 39008 2297", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "阶段4复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 1
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "20625 5185 625", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "阶段4完成通关436", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 436
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000556:1", 
                    "param2": "0 0 -137.5", 
                    "param1": "20898 5337 469", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 -137.5", 
                    "param1": "21645 6034 601", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 9.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "833", 
                    "param4": "", 
                    "id": 170
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "阶段1完成三段荷叶上升镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.8", 
                    "param1": "50000030|50000032|50000034", 
                    "param4": "", 
                    "id": 116
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "352", 
                    "param4": "", 
                    "id": 170
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 5
        }
    ], 
    14: [
        {
            "title": "阶段一传送", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "120872001", 
                    "param4": "", 
                    "id": 171
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "ENTER", 
                    "id": 9, 
                    "param1": "WATER", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "阶段二传送", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "120872002", 
                    "param4": "", 
                    "id": 171
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "ENTER", 
                    "id": 9, 
                    "param1": "WATER", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "阶段三传送", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "120872003", 
                    "param4": "", 
                    "id": 171
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "ENTER", 
                    "id": 9, 
                    "param1": "WATER", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "阶段四传送", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "120872002", 
                    "param4": "", 
                    "id": 171
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "ENTER", 
                    "id": 9, 
                    "param1": "WATER", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "跳出1发988", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "988", 
                    "param1": "20007582", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "888", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "跳出2发989", 
            "describe": "怪已删 无用", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "989", 
                    "param1": "20007583", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "889", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "跳出3发990", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "990", 
                    "param1": "20007581", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "890", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "精英死亡335传送5秒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "5", 
                    "param1": "chuanso", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "335", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20006702"
                }
            ], 
            "id": 8
        }
    ], 
    15: [
        {
            "title": "50000016靠近沉没", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000016", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "-11013 -21580 723", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "50000018靠近升起", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000018", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "60", 
                    "param3": "1580 -13460 320", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "50000019靠近沉没", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000019", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "26", 
                    "param3": "2060 -29480 320", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "50000021靠近升起", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000021", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "35", 
                    "param3": "8229 2713 883", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "50000022靠近下沉", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000022", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "40", 
                    "param3": "-10930 -7220 630", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "50000024靠近升起", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000024", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "45", 
                    "param3": "16546 -6625 864", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "50000026靠近下沉", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000026", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "17480 -12530|15860 -19240|17380 -19680|19920 -13070", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "1000|300"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "50000027靠近下沉", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000026", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-2460 -2090|-190 -5780|780 -4550|-490 -540", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "1000|300"
                }
            ], 
            "id": 8
        }, 
        {
            "title": "50000028靠近下沉", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000028", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "21", 
                    "param3": "-8310 2300 320", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 9
        }, 
        {
            "title": "50000029靠近下沉", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000029", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "28", 
                    "param3": "-4310 5690 320", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 10
        }, 
        {
            "title": "50000031靠近下沉", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000031", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "40", 
                    "param3": "5920 7350 320", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 11
        }, 
        {
            "title": "50000033靠近下沉", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.3", 
                    "param1": "50000033", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "13720 -1320|15250 -220|18840 -5310|17370 -6990", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "1000|300"
                }
            ], 
            "id": 12
        }, 
        {
            "title": "50000037靠近升起", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "0.6", 
                    "param1": "50000037", 
                    "param4": "", 
                    "id": 116
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "50", 
                    "param3": "7306 9531 334", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 13
        }, 
        {
            "title": "第一波", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "5189.996 -28829.998 661.749", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 14
        }, 
        {
            "title": "第二波", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "-10047 -15896.7 604.5", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 15
        }, 
        {
            "title": "第三波", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "-11010 -1860 573.76", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 16
        }, 
        {
            "title": "第四波", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "12698 11020.7 565.4", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 17
        }, 
        {
            "title": "第五波", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "11", 
                    "param3": "12950 1490 608.3", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|300"
                }
            ], 
            "id": 18
        }, 
        {
            "title": "缩小镜头boss20秒86标志位", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "60", 
                    "param4": "", 
                    "id": 44
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "829", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "20", 
                    "param1": "boss", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "24", 
                    "param3": "24839 9167 1593", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2000|1000"
                }
            ], 
            "id": 19
        }, 
        {
            "title": "被水滴击倒镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001115", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "13", 
                    "param3": "-18700 39420 2510", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "3000|300"
                }
            ], 
            "id": 20
        }, 
        {
            "title": "触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544018", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "21645 6034 601", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|500"
                }
            ], 
            "id": 21
        }, 
        {
            "title": "喊话提示采莲花", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001110", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "50", 
                    "param3": "-4650 -21010 320", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|0"
                }
            ], 
            "id": 22
        }, 
        {
            "title": "触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544018", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "4", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "cc", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "21645 6034 601", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|500"
                }
            ], 
            "id": 23
        }
    ], 
    21: [
        {
            "title": "刷表演", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "59", 
                    "param4": "", 
                    "id": 44
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "发时间", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 138
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "435", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 435
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ]
}