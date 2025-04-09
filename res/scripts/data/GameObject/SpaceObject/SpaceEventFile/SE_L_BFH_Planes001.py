# -*- coding: utf-8 -*-
Datas = {
    3: [
        {
            "title": "玩家进入副本，完成任务目标1/开场剧情", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102167", 
                    "param4": "", 
                    "id": 15
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051022", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "阶段1完成，刷机关/阻挡墙/巨神龟", 
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
                    "delayTime": 0.0, 
                    "param3": "10001356:1", 
                    "param2": "0 0 56", 
                    "param1": "-12179.0 -13062.0 1336.0", 
                    "param4": "", 
                    "id": 6
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
    14: [
        {
            "title": "收到hurt，播语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051024", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "hurt", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "玩家进入水区域，对玩家使用技能-浪花漩涡", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110747001", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "8540.822266 14915.212891 -20.767181|4692.728027 9108.375000 -20.767090|-1017.832031 9842.255859 -20.767151|-2831.018555 12136.984375 -20.767090|-7709.238281 10974.805664 -20.767151|-5585.032227 14764.288086 -20.767181|9939.004883 21925.755859 -20.767151|10064.746094 20040.078125 -20.767090|9373.742188 18950.201172 -20.767090|6701.035645 17941.011719 -20.767120|6534.434570 16762.396484 -20.767120", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "480|-520"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入水区域，对玩家使用技能-浪花漩涡", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110747001", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "14728.283203 10593.641602 -20.767151|13731.261719 11673.763672 -20.767151|11400.918945 10908.716797 -20.767120|10438.340820 11598.539063 -20.767120|9602.691406 10430.479492 -20.767090|10027.085938 8882.676758 -20.767181|8204.011719 5449.859375 -20.767090|8105.604980 4044.982422 -20.767151|6119.310547 4075.587891 -20.7671203606.756836 5507.627930 -20.767151|358.919922 5517.917480 -20.767120|-715.240234 3245.045898 -20.767120|-2182.003906 Y=2801.812500 -20.767181|-1785.015625 1612.958984 -7.567902|1016.291992 -233.286133 -20.767120|6276.291992 -1703.286133 -17.669861|8566.291992 -1703.286133 -20.767151|16462.908203 9859.070313 -20.767181", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "480|-520"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家进入中心台子，通知第一波怪跳出", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20010446|20010447|20010448|20010449|20010450", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051026", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "30", 
                    "param3": "5709.969727 7460.020020 193.348160", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "243|-243"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家靠近洞口，通知机关攻击玩家", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20010454|20010455", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "-9460.166992 -8502.692383 1714.276367", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2214|1214"
                }
            ], 
            "id": 4
        }
    ], 
    28: [
        {
            "title": "阶段1目标2完成，刷第二波怪", 
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
                    "param4": "", 
                    "param3": "", 
                    "id": 43, 
                    "param1": "1", 
                    "param2": "2"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "阶段2目标2完成，销毁阻挡墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30001023", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 43, 
                    "param1": "2", 
                    "param2": "2"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "阶段2目标3完成，完成任务目标2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20102167", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q051028", 
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
                    "id": 43, 
                    "param1": "2", 
                    "param2": "3"
                }
            ], 
            "id": 3
        }
    ], 
    30: [
        {
            "title": "BB结束，退出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_BFH", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q051028", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}