#pragma once

#include "UObjectArray.h"

/*
* 文件名称：CS3Listener.h
* 功能说明：主要作用就是用于在新创建UObject或删除UObject时做一些事情，目前就是输出一条日志。
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

class CS3CreateListener : public FUObjectArray::FUObjectCreateListener
{
	virtual void NotifyUObjectCreated(const class UObjectBase *Object, int32 Index) override;
};

class CS3DeleteListener : public FUObjectArray::FUObjectDeleteListener
{
	virtual void NotifyUObjectDeleted(const class UObjectBase *Object, int32 Index) override;
};