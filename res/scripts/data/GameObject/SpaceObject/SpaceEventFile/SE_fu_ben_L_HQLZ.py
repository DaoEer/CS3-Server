# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "初始化副本复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -93", 
                    "param1": "-273869.9 -205489.7 -2637.7", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 164", 
                    "param2": "-269068.0 -215771.0 -1283.9", 
                    "param1": "20007591", 
                    "param4": "1", 
                    "id": 156
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 164", 
                    "param2": "-269422.0 -217552.0 -1283.9", 
                    "param1": "20007591", 
                    "param4": "1", 
                    "id": 156
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 -178.0", 
                    "param2": "-262822.9 -203872.8 956.5", 
                    "param1": "20007592", 
                    "param4": "1", 
                    "id": 156
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 -178.0", 
                    "param2": "-262822.9 -206325.8 956.5", 
                    "param1": "20007592", 
                    "param4": "1", 
                    "id": 156
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "添加结算计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "a", 
                    "param4": "", 
                    "id": 422
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    2: [], 
    8: [
        {
            "title": "石台上升\\下降", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "6", 
                    "param2": "-25", 
                    "param1": "50000110", 
                    "param4": "", 
                    "id": 182
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "6", 
                    "param2": "20", 
                    "param1": "50000111", 
                    "param4": "", 
                    "id": 182
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
            "id": 1
        }, 
        {
            "title": "完成4设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 180", 
                    "param1": "-275778.0 -205166.0 2922.0", 
                    "param4": "", 
                    "id": 5
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
            "id": 2
        }, 
        {
            "title": "完成5通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "5", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    9: [
        {
            "title": "通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "SK_ZW0017_NPC|2|-288217 -204211.0 6166.0|0 0 -6", 
                    "param2": "3:C001905|5:C001904", 
                    "param1": "303010052:600008,600007|303010053:600018,600017|303010054:600002,600005", 
                    "param4": "30", 
                    "id": 450
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20014661:1", 
                    "param2": "0 0 180", 
                    "param1": "-289189.8 -204134.4 5821.9", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40001017:1", 
                    "param2": "0 0 0", 
                    "param1": "-289388.8 -204134.4 5838.9", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    13: [
        {
            "title": "玩家离开副本，清除BUFF", 
            "describe": "", 
            "actions": [], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "玩家走入错格子，行为见说明1", 
            "describe": "销毁这一轮的阵灵和随机刷伤害陷阱的陷阱\\传送玩家回到起点\\施加定身\\并发送重新开启路径start指令", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000201|40000050", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "0 0 44", 
                    "param2": "-260675.0 -217869.0 -186.0", 
                    "param1": "fu_ben_L_HQLZ", 
                    "param4": "", 
                    "id": 22
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "start1", 
                    "param4": "", 
                    "id": 78
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14005601", 
                    "param4": "", 
                    "id": 34
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
                    "param3": "", 
                    "id": 6, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "100", 
                    "id": 9, 
                    "param1": "Trap", 
                    "param2": "30000201"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家走入错格子，行为见说明2", 
            "describe": "销毁这一轮的阵灵和随机刷伤害陷阱的陷阱\\传送玩家回到起点\\施加定身\\并发送重新开启路径start指令", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000201|40000050", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "0 0 44", 
                    "param2": "-271143.0 -207316.0 2926.0", 
                    "param1": "fu_ben_L_HQLZ", 
                    "param4": "", 
                    "id": 22
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "start2", 
                    "param4": "", 
                    "id": 78
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14005601", 
                    "param4": "", 
                    "id": 34
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
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "100", 
                    "id": 9, 
                    "param1": "Trap", 
                    "param2": "30000201"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到start1指令，显示路线", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "-260671.0 -217855.0 -186.0|-260674.0 -215111.0 -186.0|-257942.0 -217828.0 -186.0", 
                    "param2": "40000050|20004251|30000201", 
                    "param1": "5|5|9", 
                    "param4": "0 0 89.95|end|1.6", 
                    "id": 77
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
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "start1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到start2指令，显示路线", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "-271198.0 -207320.0 2927|-271212.0 -203060.0 2927|-274619.0 -207324.0 2927", 
                    "param2": "40000050|20014619|30000201", 
                    "param1": "6|5|10", 
                    "param4": "0 0 -180|end|1.6", 
                    "id": 77
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
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "start2", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "玩家成功激活一轮阵灵，行为见说明1", 
            "describe": "销毁非指定石格上的刷伤害陷阱的陷阱\\计数key1增加1", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000201", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "key1", 
                    "param4": "", 
                    "id": 31
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
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "111", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000050"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "玩家成功激活一轮阵灵，行为见说明2", 
            "describe": "销毁非指定石格上的刷伤害陷阱的陷阱\\计数key2增加1", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000201", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "key2", 
                    "param4": "", 
                    "id": 31
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
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "111", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000050"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "玩家走出方阵1，传送玩家回初始石板", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 44", 
                    "param2": "-260675.0 -217869.0 -186.0", 
                    "param1": "fu_ben_L_HQLZ", 
                    "param4": "", 
                    "id": 22
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
                    "param3": "", 
                    "id": 6, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "555", 
                    "id": 9, 
                    "param1": "Trap", 
                    "param2": "30001143"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "玩家走出方阵2，传送玩家回初始石板", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 44", 
                    "param2": "-271143.0 -207316.0 2926.0", 
                    "param1": "fu_ben_L_HQLZ", 
                    "param4": "", 
                    "id": 22
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "3", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "555", 
                    "id": 9, 
                    "param1": "Trap", 
                    "param2": "30001144"
                }
            ], 
            "id": 8
        }, 
        {
            "title": "第一次走错路径，喊话提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000183", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "100", 
                    "id": 9, 
                    "param1": "Trap", 
                    "param2": "30000201"
                }
            ], 
            "id": 9
        }, 
        {
            "title": "收到end指令，取消耗路径上的光效\\取消玩家定身", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20004251|20014619", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14005601", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "end", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 10
        }, 
        {
            "title": "完成阶段一", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20007591", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "j1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 11
        }, 
        {
            "title": "完成阶段三", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20007592", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "j3", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 12
        }
    ], 
    15: [
        {
            "title": "进入石格范围1，传送玩家到指定石格\\施加定身buff\\发送开启玩法指令start1", 
            "describe": "刷group1/group2/start/语音", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "start1", 
                    "param4": "", 
                    "id": 78
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 44", 
                    "param2": "-260675.0 -217869.0 -186.0", 
                    "param1": "fu_ben_L_HQLZ", 
                    "param4": "", 
                    "id": 22
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14005601", 
                    "param4": "", 
                    "id": 33
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001913", 
                    "param4": "", 
                    "id": 256
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
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-261793.0 -219099.0 -146.0|-261793.0 -213828.0 -142.0|-257127.0 -213828.0 -142.0|-257127.0 -219063.0 -142.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "100|-600"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "进入石格范围2，传送玩家到指定石格\\施加定身buff\\发送开启玩法指令start1", 
            "describe": "刷group1/group2/start", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "start2", 
                    "param4": "", 
                    "id": 78
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 44", 
                    "param2": "-271143.0 -207316.0 2926.0", 
                    "param1": "fu_ben_L_HQLZ", 
                    "param4": "", 
                    "id": 22
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14005601", 
                    "param4": "", 
                    "id": 33
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
            "triggerConditions": [
                {
                    "param4": "0", 
                    "param3": "-269211.0 -208955.0 3020.0|-276510.0 -208955.0 3020.0|-276510.0 -201442.0 3087.0|-269360.0 -201442.0 3087.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "3000|2450"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "刷group3/4/5", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 6.0, 
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
                    "param4": "20", 
                    "param3": "-259234.3 -210655.0 586.9", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "800|400"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "122573004", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "5", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "-289189.8 -204134.4 5821.9", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "6000|5800"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "进入石格范围1，语音提示", 
            "describe": "刷group1/group2/start", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001912", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "-272949.0 -213268.0 -1369.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-400|-1600"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "终点取得灵珠的表现", 
            "describe": "", 
            "actions": [], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 6
        }
    ], 
    16: [
        {
            "title": "激活阵灵成功数为key1=1，详情见说明", 
            "describe": "发送下一轮路径显示start指令\\传送玩家回到初始石板\\施加定身\\C001914语音", 
            "actions": [
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
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001914", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "key1", 
                    "param2": "1"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "激活阵灵成功数为key2=1，详情见说明", 
            "describe": "发送下一轮路径显示start指令\\传送玩家回到初始石板\\施加定身", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "start2", 
                    "param4": "", 
                    "id": 78
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 44", 
                    "param2": "-271143.0 -207316.0 2926.0", 
                    "param1": "fu_ben_L_HQLZ", 
                    "param4": "", 
                    "id": 22
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14005601", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "key2", 
                    "param2": "1"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "激活阵灵成功数为key2=2，详情见说明", 
            "describe": "发送下一轮路径显示start指令\\传送玩家回到初始石板\\施加定身\\C001914语音", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001914", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "key2", 
                    "param2": "2"
                }
            ], 
            "id": 3
        }
    ], 
    19: [], 
    20: []
}