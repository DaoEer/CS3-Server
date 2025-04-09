# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "倒计时结束，开启副本计时，语音提示", 
            "describe": "移除定身", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14019101", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "6000", 
                    "param4": "", 
                    "id": 97
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "副本生命结束，提示通关失败", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 4
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000413", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 60.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "LoopQuestLife", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    3: [
        {
            "title": "玩家进入副本，开启额外物品栏", 
            "describe": "同时添加定身buff。", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 119
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14019101", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "玩家进入副本，变身黑衣人（男性）", 
            "describe": "给予匕首", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14029501|14029601", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    5: [
        {
            "title": "三叉戟全部被销毁，移除boss身上增益buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14029008|14029009", 
                    "param1": "20011562", 
                    "param4": "", 
                    "id": 237
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "99", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "阶段完成，结算", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 48
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000425", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "副本通关时间为：", 
                    "param1": "80135053", 
                    "param4": "", 
                    "id": 84
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
            "id": 1
        }
    ], 
    13: [
        {
            "title": "玩家登陆其他地图，移除额外物品栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 120
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "303010021|303010022|303010023|303010024|303010025|303010026|303010027|303010028|303010029", 
                    "param4": "", 
                    "id": 23
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到BOSS残血通知，刷出三叉戟", 
            "describe": "并通知boss开始表演", 
            "actions": [
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "99", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "902", 
                    "param1": "20011562", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "201", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到长剑通知，播放长剑落地表演", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "903", 
                    "param1": "20011560", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "222", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到装备匣通知，随机给予武器", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "303010021|303010022|303010023|303010024", 
                    "param4": "", 
                    "id": 253
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "401", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到法宝匣通知，随机给予法宝", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "303010025|303010026|303010027|303010028", 
                    "param4": "", 
                    "id": 253
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "402", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    15: [
        {
            "title": "玩家靠近池塘，池塘跳出怪物", 
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
                    "param4": "30", 
                    "param3": "-22849.9 11740.0 1020.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1439|339"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家靠近左中走廊，走廊跳出怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "51", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-21460.0 1700.0|-20200.0 1700.0|-20420.0 -2680.0|-21290.0 -2680.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "2556|580"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家靠近右上走廊，刷出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "62", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "72", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "30", 
                    "param3": "-10909.8 -12360.0 1562.9", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2000|500"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家靠近右上过道，屋檐跳出怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "91", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-821.622803 -11139.702148|-821.622803 -13299.702148|-5158.861328 -13629.964844|-5138.861328 -11449.964844", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "2556|580"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "玩家靠近右边演武怪物，刷出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "63", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "16460.0 4570.0 1010.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2000|500"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "玩家靠近右边牌坊，刷出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "73", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "10670.0 7350.0 1560.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2000|500"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "玩家靠近左边过道，刷出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "61", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "71", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "-29230.0 70.0 910.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2000|500"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "玩家靠近左上荷花池，刷出精英", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "20011591:1", 
                    "id": 28
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "20011561:1", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-27720.0 -12150.0|-27680.0 -10950.0|-24480.0 -10580.0|-24480.0 -12220.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "2556|580"
                }
            ], 
            "id": 8
        }, 
        {
            "title": "玩家靠近右上水池，刷出桥上暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "64", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "74", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-16147.1 -11088.1|-16147.1 -11758.1|-19827.1 -11728.1|-19827.1 -11058.1", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "2556|580"
                }
            ], 
            "id": 9
        }, 
        {
            "title": "玩家靠近右边精英出牌坊，刷出暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "65", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "5803.2 -10234.0 1555.5", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2000|500"
                }
            ], 
            "id": 10
        }
    ], 
    18: [
        {
            "title": "拾取匕首，获得匕首技能", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14029601", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 20, 
                    "param1": "303010029", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "拾取刀，获得刀技能", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14029602", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 20, 
                    "param1": "303010021", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "拾取枪，获得枪技能", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14029603", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 20, 
                    "param1": "303010022", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "拾取弓，获得弓技能", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14029604", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 20, 
                    "param1": "303010023", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    19: [
        {
            "title": "玩家在副本中死亡，提示通关失败", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000413", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "123", 
                    "param4": "", 
                    "id": 4
                }, 
                {
                    "delayTime": 60.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 21, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "玩家进入副本，开始倒计时5秒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "0", 
                    "param2": "5", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000496", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}