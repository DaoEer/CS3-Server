# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "阶段2完成销毁1号隐形boss", 
            "describe": "阶段2完成销毁1号隐形boss", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20003865", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -17", 
                    "param1": "-21496 -994 598", 
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
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "阶段4完成销毁2号隐形boss", 
            "describe": "阶段4完成销毁2号隐形boss", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20003866|20003872", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 72", 
                    "param1": "8935 -1183 4117", 
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
            "title": "阶段6完成销毁3号隐形boss", 
            "describe": "阶段6完成销毁3号隐形boss", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20003867|20003873", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 159", 
                    "param1": "7336 24100 8283", 
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
                    "param1": "6", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "阶段7完成召唤BOSS", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20003861:1", 
                    "param2": "0 0 66", 
                    "param1": "-9888 17121 11085", 
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
                    "id": 4, 
                    "param1": "7", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    1: [
        {
            "title": "初始化副本复活点", 
            "describe": "初始化副本复活点", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -96", 
                    "param1": "-21480 22440 -1800", 
                    "param4": "", 
                    "id": 5
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
            "title": "收到指令刷滚石", 
            "describe": "收到指令刷滚石", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "11|10|8|3|4|9|5|6|12|7", 
                    "param2": "11204 27291 12672|10105 26925 13724|9614 26730 14073|9313 26247 13461|8810 26027 13812|9196 24713 11111|6986 21803 12327|8181 21480 11520|8660 20680 12200|9202 19603 13419", 
                    "param1": "20003869:6|20003870:2", 
                    "param4": "", 
                    "id": 88
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "111", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003867"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到指令清零计数", 
            "describe": "收到指令清零计数", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 101
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "222", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003867"
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "进入范围刷第一波怪", 
            "describe": "进入范围刷第一波怪", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "20003851:1", 
                    "param2": "0 0 90", 
                    "param1": "-20557 8068 -132", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20003851:1", 
                    "param2": "0 0 110", 
                    "param1": "-20457 8098 -132", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20003851:1", 
                    "param2": "0 0 110", 
                    "param1": "-20337 8138 -132", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20003852:1", 
                    "param2": "0 0 110", 
                    "param1": "-19827 7968 -302", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20003852:1", 
                    "param2": "0 0 110", 
                    "param1": "-19697 8048 -302", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20003852:1", 
                    "param2": "0 0 110", 
                    "param1": "-19547 8068 -282", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "-21437 9788 -702", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "707|-1522"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "进入范围刷第二波怪", 
            "describe": "进入范围刷第二波怪", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20003855:1", 
                    "param2": "0 0 -149", 
                    "param1": "-14667 -3221 1544", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20003855:1", 
                    "param2": "0 0 -149", 
                    "param1": "-14687 -2991 1554", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "20003853:1", 
                    "param2": "0 0 -149", 
                    "param1": "-14157 -2881 2084", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "20003853:1", 
                    "param2": "0 0 -149", 
                    "param1": "-14077 -2741 2104", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "20003854:1", 
                    "param2": "0 0 -169", 
                    "param1": "-14077 -3101 2064", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "20003854:1", 
                    "param2": "0 0 -159", 
                    "param1": "-14047 -2961 2104", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "35", 
                    "param3": "-14367 -3911 1467", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "3217|627"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "进入范围刷第三波怪", 
            "describe": "进入范围刷第三波怪", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20003850:1", 
                    "param2": "0 0 -159", 
                    "param1": "-5207 -4191 3060", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20003850:1", 
                    "param2": "0 0 -159", 
                    "param1": "-4837 -4591 3060", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "20003850:1", 
                    "param2": "0 0 -159", 
                    "param1": "-4757 -3801 3060", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "20003850:1", 
                    "param2": "0 0 -159", 
                    "param1": "-5197 -3621 3060", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "-5207 -4191 3060", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "4760|1980"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "进入范围刷第四波怪", 
            "describe": "进入范围刷第四波怪", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20003856:1", 
                    "param2": "0 0 -160", 
                    "param1": "2422 -5831 3417", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20003856:1", 
                    "param2": "0 0 -160", 
                    "param1": "2502 -5041 3400", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "1732 -5351 3417", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "4837|2277"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "进入范围刷第五波怪", 
            "describe": "进入范围刷第五波怪", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20003856:1", 
                    "param2": "0 0 -100", 
                    "param1": "11772 15938 7031", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20003856:1", 
                    "param2": "0 0 -100", 
                    "param1": "12412 15928 7031", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20003856:1", 
                    "param2": "0 0 -100", 
                    "param1": "12122 16578 7208", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "12032 15978 7042", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "9102|5602"
                }
            ], 
            "id": 5
        }
    ]
}