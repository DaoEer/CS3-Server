# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "15秒倒计时结束，开始副本计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "15", 
                    "param1": "360", 
                    "param4": "", 
                    "id": 97
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14019101", 
                    "param4": "", 
                    "id": 26
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
            "title": "6分钟达到，未获得熔岩晶，副本失败", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "80135050", 
                    "param4": "", 
                    "id": 30
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
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 325
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000576", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 27, 
                    "param1": "2", 
                    "param2": "1"
                }
            ], 
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
    5: [
        {
            "title": "熔岩巨兽死亡，刷新玩家复活点并删除光墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -50", 
                    "param1": "-9615.8603516 10307.6035156 2810.5534668", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000715", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010180:1", 
                    "param2": "0 0 0", 
                    "param1": "-6997.259277 8669.193359 3440.197266", 
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
                    "id": 2, 
                    "param1": "20010176", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    13: [
        {
            "title": "删除额外物品栏", 
            "describe": "移除姿态改变buff", 
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
                    "param1": "14014701|14014702|14014703|14014704|14014705|14014706|14014707|14014708|14014709|14014710", 
                    "param4": "", 
                    "id": 25
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
            "title": "收到110通知，触发熔岩巨兽喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000647|Cy000648", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "110", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到111通知，提示使用熔岩巨石", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000646", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "111", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到112通知，旁白提醒喷火陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000645", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "112", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到114通知，触发熔岩晶旁白，任务完成", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000649", 
                    "param4": "", 
                    "id": 256
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
                    "delayTime": 1.0, 
                    "param3": "9", 
                    "param2": "环任务通关时间：", 
                    "param1": "80135050", 
                    "param4": "", 
                    "id": 331
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "714", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "140379001", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "114", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到dici通知，刷新地刺陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 20", 
                    "param1": "-10062.6 -1136.2 5519.4", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 20", 
                    "param1": "-9852.6 -1716.2 5532.6", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 20", 
                    "param1": "-10858.4 -1452.1 5634.4", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 20", 
                    "param1": "-10662.6 -1986.2 5650.1", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 70", 
                    "param1": "-11742.6 -2416.2 5758.7", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 70", 
                    "param1": "-11207.7 -2609.6 5745.9", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11866.5 -3460.8 5836.5", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11297.7 -3459.6 5854.9", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11856.5 -4470.8 5930.8", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11287.7 -4469.6 5941.6", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-12106.5 -5460.8 6118.3", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11537.7 -5459.6 6151.5", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-12126.5 -6380.8 6331.6", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11557.7 -6379.6 6318.1", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 50", 
                    "param1": "-11432.599609 -1856.199951 5777.211426", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 80", 
                    "param1": "-11852.599609 -2936.199951 5838.212402", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11297.700195 -3969.600098 5908.166016", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-10757.700195 -4109.600098 5935.702148", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-10757.700195 -4699.600098 6017.829102", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11997.700195 -4959.600098 6008.499023", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11817.700195 -5929.600098 6225.132324", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-12126.500000 -6960.799805 6397.068848", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "30000951:1", 
                    "param2": "0 0 90", 
                    "param1": "-11557.700195 -6959.600098 6397.776367", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "dici", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到chuixia通知，把玩家吹下石头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "140147001", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 53, 
                    "param1": "20010177", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "chuixia", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "点击退出按钮，任务还未成功时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 334
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 27, 
                    "param1": "2", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "SignOut", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 7
        }
    ], 
    15: [
        {
            "title": "玩家即将遇到地刺陷阱，语音提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000722", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "-10499 -1716 5604", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "10000|0"
                }, 
                {
                    "param4": "", 
                    "param3": "dici", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    17: [
        {
            "title": "删除额外物品栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12021401|14014701|14014702|14014703|14014704|14014705|14014706", 
                    "param4": "", 
                    "id": 25
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010014", 
                    "param4": "", 
                    "id": 23
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 311
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    19: [
        {
            "title": "玩家死亡后，重置石头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010177", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12021401|14014701|14014702|14014703|14014704|14014705|14014706", 
                    "param4": "", 
                    "id": 25
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20010177:1", 
                    "param2": "0 0 -30", 
                    "param1": "-9052.4 10067.3 2933.9", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 28, 
                    "param1": "1", 
                    "param2": "1"
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 27, 
                    "param1": "2", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "15秒界面倒计时，获得额外物品栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "80135050", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 170", 
                    "param1": "11934.266602 18308.937500 932.315491", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "0", 
                    "param2": "15", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "15", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 119
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000719|Cy000641|Cy000643", 
                    "param4": "", 
                    "id": 19
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
        }
    ]
}