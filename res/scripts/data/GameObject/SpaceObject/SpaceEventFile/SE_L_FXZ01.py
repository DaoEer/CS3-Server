# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "设置区域", 
            "describe": "初始化，设置起点，设置终点", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "360", 
                    "param1": "time", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "240", 
                    "param1": "time12", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "40000158|40000164|40000314", 
                    "param1": "kwx|1|10000", 
                    "param4": "", 
                    "id": 151
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "300", 
                    "param1": "-7390 -1660 1759", 
                    "param4": "", 
                    "id": 211
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "50", 
                    "param2": "0", 
                    "param1": "200", 
                    "param4": "", 
                    "id": 213
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
            "title": "重新刷出道具箱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "12", 
                    "param1": "1|2|3|4|5|6|7|8|9|10|11|12|13|15|16|17|19|21|22|23|24|25|27|28|29|30|31|32|33|34|35|36|38", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "12", 
                    "param1": "39|40|41|42|43|46|50|51|52|53|61|62|63|64|68|69|70|83|84|85|86|87|88|89|90", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "7", 
                    "param1": "91|92|93|94|95|96|97|98|99|100|101", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "24", 
                    "param1": "1|2|5|6|12|13|14|15|21|22|23|27|30|31|32|33|34|35|36|37|38|39|40|41|42|43|44|45|46|47|48|49|50|51|52|53|54|56|57|58|59|60|61|62|63|64|65|66|67|68|69|70|71|72|73|74|75|76", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "20", 
                    "param1": "77|78|79|80|81|82|83|84|85|86|87|88|89|90|91|92|93|94|95|96|97|98|99|100|101|102|103|104|105|106|107|108|109", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20005515", 
                    "param2": "1", 
                    "param1": "1|2|3", 
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
            "id": 1
        }, 
        {
            "title": "第一次缩圈", 
            "describe": "缩小范围圈，并且设置复活点", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "121", 
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
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "120", 
                    "param4": "", 
                    "id": 215
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12052803", 
                    "param4": "", 
                    "id": 216
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
            "id": 2
        }, 
        {
            "title": "设置第二圈", 
            "describe": "设置第二圈", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "100", 
                    "param2": "0", 
                    "param1": "100", 
                    "param4": "", 
                    "id": 213
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "300", 
                    "param1": "time2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 214
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
                    "id": 215
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "121", 
                    "param1": "time3", 
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
                    "param1": "time2", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "设置第三圈", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20", 
                    "param2": "0", 
                    "param1": "60", 
                    "param4": "", 
                    "id": 213
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "240", 
                    "param1": "time4", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 214
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time3", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "第三次缩圈", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "120", 
                    "param4": "", 
                    "id": 215
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "121", 
                    "param1": "time5", 
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
                    "param1": "time4", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "设置第四圈", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "5", 
                    "param2": "0", 
                    "param1": "40", 
                    "param4": "", 
                    "id": 213
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "180", 
                    "param1": "time6", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 214
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time5", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "第四次缩圈", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "120", 
                    "param4": "", 
                    "id": 215
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000460", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "121", 
                    "param1": "time7", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time6", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "设置第五圈", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "5", 
                    "param2": "0", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 213
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "120", 
                    "param1": "time8", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 214
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time7", 
                    "param2": ""
                }
            ], 
            "id": 9
        }, 
        {
            "title": "第五次缩圈（最后一次）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "60", 
                    "param4": "", 
                    "id": 215
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
                    "param1": "time8", 
                    "param2": ""
                }
            ], 
            "id": 10
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
                    "param1": "6", 
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
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 212
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 232
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
                    "param2": "12", 
                    "param1": "1|2|3|4|5|6|7|8|9|10|11|12|13|15|16|17|19|21|22|23|24|25|27|28|29|30|31|32|33|34|35|36|38", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "12", 
                    "param1": "39|40|41|42|43|46|50|51|52|53|61|62|63|64|68|69|70|83|84|85|86|87|88|89|90", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000158", 
                    "param2": "7", 
                    "param1": "91|92|93|94|95|96|97|98|99|100|101", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "24", 
                    "param1": "1|2|5|6|12|13|14|15|21|22|23|27|30|31|32|33|34|35|36|37|38|39|40|41|42|43|44|45|46|47|48|49|50|51|52|53|54|56|57|58|59|60|61|62|63|64|65|66|67|68|69|70|71|72|73|74|75|76", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000164", 
                    "param2": "20", 
                    "param1": "77|78|79|80|81|82|83|84|85|86|87|88|89|90|91|92|93|94|95|96|97|98|99|100|101|102|103|104|105|106|107|108|109", 
                    "param4": "", 
                    "id": 172
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20005515", 
                    "param2": "1", 
                    "param1": "1|2|3", 
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
                    "param3": "", 
                    "param2": "30000437:1", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 51
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0.1", 
                    "param2": "40000157", 
                    "param1": "0.3", 
                    "param4": "8", 
                    "id": 227
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