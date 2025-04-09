# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "设置区域", 
            "describe": "初始化，设置起点，设置终点", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "-27120.0 30330.0 100", 
                    "param2": "28470.0 -29760.0 100", 
                    "param1": "-27120.0 -29760.0 100", 
                    "param4": "28470.0 30330.0 100", 
                    "id": 141
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "-8163.0 12000.1 1245", 
                    "param2": "8765 -4736.0 1245", 
                    "param1": "-8157.0 -4705.0 1245", 
                    "param4": "8765 12000.1 1245", 
                    "id": 142
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "780", 
                    "param1": "time", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "300", 
                    "param1": "time12", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "40000158|40000164", 
                    "param1": "kwx|1|1000", 
                    "param4": "", 
                    "id": 151
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    2: [
        {
            "title": "开始缩小范围圈", 
            "describe": "缩小范围圈，并且设置复活点", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "240", 
                    "param4": "", 
                    "id": 146
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12052803", 
                    "param4": "", 
                    "id": 147
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0|0 0 0|0 0 0|0 0 0", 
                    "param1": "7730 10950 1485|7730 -3680 1485|-7110 -3680 1485|-7110 10950 1485", 
                    "param4": "", 
                    "id": 173
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "240", 
                    "param1": "time1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000460", 
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
                    "param1": "time", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "重新刷出道具箱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "8", 
                    "param1": "1|2|3|4|5|6|7|8|9|10|11|12|13|15|16|17|19|21|22|23|24|25|27|28|29|30|31|32|33|34|35|36|38", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "7", 
                    "param1": "39|40|41|42|43|46|50|51|52|53|61|62|63|64|68|69|70|83|84|85|86|87|88|89|90", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "12", 
                    "param1": "61|62|63|64|65|66|67|68|69|70|71|72|73|74|75|76|77|78|79|80|81|82|83|84|85|86|87|88|89|90", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "12", 
                    "param1": "1|2|5|6|12|13|14|15|21|22|23|27|30|31|32|33|34|35|36|37|38|39|40|41|42|43|44|45|46|47|48|49|50|51|52|53|54|56|57|58|59|60", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "8", 
                    "param1": "55|7|8|9|10|11|4|3|18|17|16|19|20|24|25|26|28|29", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "10", 
                    "param1": "61|62|63|64|65|66|67|68|69|70|71|72|73|74|75|76|77|78|79|80|81|82|83|84|85", 
                    "param4": "", 
                    "id": 172
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time12", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "设置第二个圈", 
            "describe": "设置第二个圈", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "-2456.16333 6376.672852 1569.745605", 
                    "param2": "3183.83667 886.672729 1569.745605", 
                    "param1": "-2456.16333 886.672729 1569.745605", 
                    "param4": "3183.83667 6376.672852 1569.745605", 
                    "id": 142
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "540", 
                    "param1": "time2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 145
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time1", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "第二次缩圈", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "120", 
                    "param4": "", 
                    "id": 146
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0|0 0 0|0 0 0|0 0 0", 
                    "param1": "-1856.0 5776.0 1951.0|-1856.0 1536.0 1951.0|2433.0 1536.0 1951.0|2433.0 5776.0 1951.0", 
                    "param4": "", 
                    "id": 173
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000460", 
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
                    "param1": "time2", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    3: [
        {
            "title": "添加额外道具栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 119
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    13: [
        {
            "title": "关闭额外道具栏", 
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
                    "param1": "303010001|303010002|303010003|303010004|303010005", 
                    "param4": "", 
                    "id": 23
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12052801|12052802|12052803|12052804", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "玩家进入显示范围", 
            "describe": "玩家进入显示范围", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 143
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 144
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "刷出道具箱子", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "8", 
                    "param1": "1|2|3|4|5|6|7|8|9|10|11|12|13|15|16|17|19|21|22|23|24|25|27|28|29|30|31|32|33|34|35|36|38", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "7", 
                    "param1": "39|40|41|42|43|46|50|51|52|53|61|62|63|64|68|69|70|83|84|85|86|87|88|89|90", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "12", 
                    "param1": "14|20|18|26|58|57|56|55|54|47|48|49|45|44|60|37|59|65|66|67|71|72|73|74|75|76|78|79|80|81|82", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "12", 
                    "param1": "1|2|5|6|12|13|14|15|21|22|23|27|30|31|32|33|34|35|36|37|38|39|40|41|42|43|44|45|46|47|48|49|50|51|52|53|54|56|57|58|59|60", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "8", 
                    "param1": "55|7|8|9|10|11|4|3|18|17|16|19|20|24|25|26|28|29", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "10", 
                    "param1": "61|62|63|64|65|66|67|68|69|70|71|72|73|74|75|76|77|78|79|80|81|82|83|84|85", 
                    "param4": "", 
                    "id": 172
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    23: [
        {
            "title": "瓜分积分", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0.1", 
                    "param2": "40000157", 
                    "param1": "0.2", 
                    "param4": "6", 
                    "id": 139
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30000437:1", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 51
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    25: [
        {
            "title": "击杀小怪，获得1积分", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 140
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005503|20005504|20005505|20005506|20005507|20005508|20005509|20005510", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "击杀精英，获得5积分", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 140
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005511|20005512|20005513|20005514", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "击杀BOSS，获得50积分", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "50", 
                    "param4": "", 
                    "id": 140
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005515", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ]
}