# -*- coding: utf-8 -*-

import KBEDebug

class FaceInfo(dict):

    def __int__(self):
        dict.__init__(self)

    def getDictFromObj(self, obj):
        """
        The method converts a wrapper instance to a FIXED_DICT instance.

        @param obj: The obj parameter is a wrapper instance.
        @return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
        """
        dict = {"boneName": obj["boneName"], "boneData": obj["boneData"]}
        return dict


    def createObjFromDict(self, dict):
        """
        his method converts a FIXED_DICT instance to a wrapper instance.

        @param dict: The dict parameter is a FIXED_DICT instance.
        @return: The method should return the wrapper instance constructed from the information in dict.
        """
        obj=self.__class__()
        obj["boneName"]=dict["boneName"]
        obj["boneData"]=dict["boneData"]
        return obj


    def isSameType(self, obj):
        """
        This method check whether an object is of the wrapper type.

        @param obj: The obj parameter in an arbitrary Python object.
        @return: This method should return true if obj is a wrapper instance.
        """
        if obj is None: return False
        return isinstance(obj, FaceInfo)





class FaceInfoList(dict):

    def __int__(self):
        dict.__init__(self)

    def getDictFromObj(self, obj):
        """
        The method converts a wrapper instance to a FIXED_DICT instance.

        @param obj: The obj parameter is a wrapper instance.
        @return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
        """
        datas=[]
        dict={"infos": datas}
        for d in obj["infos"]:
            datas.append(d)
        return dict

    def createObjFromDict(self, dict):
        """
        This method converts a FIXED_DICT instance to a wrapper instance.

        @param dict: The dict parameter is a FIXED_DICT instance.
        @return: The method should return the wrapper instance constructed from the information in dict.
        """
        obj = self.__class__()
        obj["infos"] = []
        for dct in dict["infos"]:
            o = FaceInfo().createObjFromDict(dct)
            obj["infos"].append(o)
        return obj

    def isSameType(self, obj):
        """
        This method check whether an object is of the wrapper type.

        @param obj: The obj parameter in an arbitrary Python object.
        @return: This method should return true if obj is a wrapper instance.
        """
        if obj is None: return False
        return isinstance(obj, FaceInfoList)


instance = FaceInfo()
instance1 = FaceInfoList()
