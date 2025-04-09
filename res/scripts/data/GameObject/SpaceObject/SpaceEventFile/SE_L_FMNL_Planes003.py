# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段3完成，设置玩家完成任务目标“探寻盘古法力”", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101105", 
                    "param4": "", 
                    "id": 2
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
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    12: [
        {
            "title": "后半程怪物全部死亡，设置完成阶段2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20", 
                    "param1": "20001904", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "2|3|4|5", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "玩家达到位置1，给哮天犬发送AI指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "99", 
                    "param1": "20001904|20001903", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020068", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 1
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "12", 
                    "param3": "97761.007813 31370.587891 -9422.469727", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-8000|-18000"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入范围21，刷跳出暗怪", 
            "describe": "玩家进入范围1，刷跳出暗怪", 
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
                    "param4": "35", 
                    "param3": "94406.953125 35157.089844 -8892.191406", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-8000|-23000"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家进入范围23，刷第二批暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "20001899:2", 
                    "id": 28
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "20001900:3", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "82526.460938 30091.615234 -8076.672363", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-8000|-23000"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家进入范围22，半身像界面提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020067", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "86976.539063 32814.902344 -8419.664063", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-7456|-9456"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "玩家进入范围12，刷第二批暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "98703.304688 19816.515625 -13369.188477", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-8000|-23000"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "玩家进入范围11，半身像界面提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020064", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q020065", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "94612.898438 14707.501953 -15162.980469", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-8000|-23000"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "玩家进入范围24，播放镜头，完成任务", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000055", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "24", 
                    "param1": "20001904", 
                    "param4": "", 
                    "id": 10
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
                    "param4": "10", 
                    "param3": "73370.000000 26060.000000 -7390.000000", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-6000|-16000"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "玩家进入位面，通知哮天犬巡逻", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "66", 
                    "param1": "20001904", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "100015.679688 15603.693359 -16657.369141", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-8000|-23000"
                }
            ], 
            "id": 8
        }
    ]
}