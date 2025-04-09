# -*- coding: utf-8 -*-

import KBEDebug

class FaceStyle(dict):
    def __init__(self):
        dict.__init__(self)

    def getDictFromObj(self, obj):
        """
        The method converts a wrapper instance to a FIXED_DICT instance.

        @param obj: The obj parameter is a wrapper instance.
        @return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
        """
        dict = {
                "ChunzhuangIndex": obj["ChunzhuangIndex"],
                "ChunzhuangShape": obj["ChunzhuangShape"],
                "HuXuIndex": obj["HuXuIndex"],
                "LianWenIndex": obj["LianWenIndex"],
                "MeiMaoIndex": obj["MeiMaoIndex"],
                "MeiMaoShape": obj["MeiMaoShape"],
                "YanXianIndex": obj["YanXianIndex"],
                "SaiHongIndex": obj["SaiHongIndex"],
                "SaiHongShape": obj["SaiHongShape"],
                "YanYingIndex": obj["YanYingIndex"],
                "YanYingShape": obj["YanYingShape"],
                "Brightness": obj["Brightness"],
                "ColorDepth": obj["ColorDepth"],
                "EyeIndex": obj["EyeIndex"],
                "EyeScale": obj["EyeScale"]
                }
        return dict


    def createObjFromDict(self, dict):
        """
        his method converts a FIXED_DICT instance to a wrapper instance.

        @param dict: The dict parameter is a FIXED_DICT instance.
        @return: The method should return the wrapper instance constructed from the information in dict.
        """
        obj = self.__class__()
        if not dict:
            obj["ChunzhuangIndex"] = 0
            obj["ChunzhuangShape"] = "0.0"
            obj["HuXuIndex"] = 0
            obj["LianWenIndex"] = 0
            obj["MeiMaoIndex"] = 0
            obj["MeiMaoShape"] = "0.0"
            obj["YanXianIndex"] = 0
            obj["SaiHongIndex"] = 0
            obj["SaiHongShape"] = "0.0"
            obj["YanYingIndex"] = 0
            obj["YanYingShape"] = "0.0"
            obj["Brightness"] = "0.0"
            obj["ColorDepth"] = "0.0"
            obj["EyeIndex"] = 0
            obj["EyeScale"] = "0.0"
        else:
            obj["ChunzhuangIndex"] = dict["ChunzhuangIndex"]
            obj["ChunzhuangShape"] = dict["ChunzhuangShape"]
            obj["HuXuIndex"] = dict["HuXuIndex"]
            obj["LianWenIndex"] = dict["LianWenIndex"]
            obj["MeiMaoIndex"] = dict["MeiMaoIndex"]
            obj["MeiMaoShape"] = dict["MeiMaoShape"]
            obj["YanXianIndex"] = dict["YanXianIndex"]
            obj["SaiHongIndex"] = dict["SaiHongIndex"]
            obj["SaiHongShape"] = dict["SaiHongShape"]
            obj["YanYingIndex"] = dict["YanYingIndex"]
            obj["YanYingShape"] = dict["YanYingShape"]
            obj["Brightness"] = dict["Brightness"]
            obj["ColorDepth"] = dict["ColorDepth"]
            obj["EyeIndex"] = dict["EyeIndex"]
            obj["EyeScale"] = dict["EyeScale"]
        return obj


    def isSameType(self, obj):
        """
        This method check whether an object is of the wrapper type.

        @param obj: The obj parameter in an arbitrary Python object.
        @return: This method should return true if obj is a wrapper instance.
        """
        if obj is None:
            return False
        return isinstance(obj, FaceStyle)


instance = FaceStyle()
