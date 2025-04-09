# -*- coding: utf-8 -*-
Datas = {
    3: [
        {
            "title": "计数初始化", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "A", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "B", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "玩家没有301010109且没有跟法阵交互，重新添加301010109", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010109", 
                    "param4": "", 
                    "id": 42
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "A", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 42, 
                    "param1": "301010109", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家没有301010110且没有跟法阵交互，重新添加301010110", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010110", 
                    "param4": "", 
                    "id": 42
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "B", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 42, 
                    "param1": "301010110", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    5: [
        {
            "title": "第1波怪物死亡，刷第2波小怪和精英", 
            "describe": "给刷怪点发送通知", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10", 
                    "param1": "20008814|20008815|20008816", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20008822|20008823|20008824|20008825|20008826", 
                    "param2": "1|1|1|1|1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "第2波怪物死亡，刷第3波小Boss和小怪", 
            "describe": "给刷怪点发送通知", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20", 
                    "param1": "20008814|20008815|20008816", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20009336|20008830|20008831", 
                    "param2": "1|1|1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "第3波怪物死亡，刷Boss", 
            "describe": "给刷怪点发送通知", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "50", 
                    "param1": "20008814", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20009341|20008829|20008832", 
                    "param2": "1|1|1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    7: [
        {
            "title": "玄冥血量低于31%任务完成", 
            "describe": "1.完成当前阶段，2.完成任务目标，3.播放一个镜头技能", 
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
                    "param2": "1", 
                    "param1": "20102125", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102126", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000431", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 14, 
                    "param1": "20009344", 
                    "param2": "0.31"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到阵柱A发送100", 
            "describe": "收到柱子A发送的100  计数 A加一等于A1", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "A", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "100", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到阵柱B发送200", 
            "describe": "收到柱子B发送的100  计数 B加一等于B1", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "B", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "200", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "玩家离开某个范围，广成子喊话", 
            "describe": "喊话 三秒通知场景可交互，通知广成子走到夸父后面\n广成子前辈，我已将重生之水和续骨神壤带来。\n万事俱备，勇士你这便将宝物融入阵眼，激活大阵，助夸父觉醒神力", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045417|Q045419", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.5, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "40000451", 
                    "param4": "", 
                    "id": 199
                }, 
                {
                    "delayTime": 4.5, 
                    "param3": "", 
                    "param2": "200", 
                    "param1": "40000452", 
                    "param4": "", 
                    "id": 199
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20008810", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "1007.0 -45539.0 3154.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "7000|-2000"
                }
            ], 
            "id": 1
        }
    ], 
    16: [
        {
            "title": "两个阵柱激活，召唤阵法光效", 
            "describe": "两个阵柱激活，召唤阵法光效，五秒后魔道进攻。\n玄月涅槃大阵，起！\n全军冲锋，拿下夸父！\n勇士，快拦住来犯的魔道，绝不能让他们打扰夸父觉醒！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045420", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 9.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q045421|Q045422", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20008811|20008810", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 89
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "A", 
                    "param2": "1"
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "B", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}