#pragma once

#include "KBEngine.h"

/*
* 文件名称：CSOLPersonality.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/

/**
*登入断线数据设置时的回调
*/
class CSOLPersonality : public KBEngine::KBEPersonality
{
public:
	/**
	*当某个space data被改变或设置时，此方法被触发
	*
	*@param spaceID  （uint32）
	*@param key ，调用方法时的KEY（FString）
	*@param value，要输入的信息（FString）
	*
	*@return 无
	*/
	virtual void OnSetSpaceData(uint32 spaceID, const FString &key, const FString &value);

	/**
	*当某个space data被删除时，此方法被触发
	*
	*@param spaceID  （uint32）
	*@param key ，调用方法时的KEY（FString）
	*
	*@return 无
	*/
	virtual void OnDelSpaceData(uint32 spaceID, const FString &key);

	/**
	*当服务器中的Space加载了地图的导航数据时，此方法被触发
	*
	*@param spaceID  （uint32）
	*@param respath （FString）
	*
	*@return 无
	*/
	virtual void OnAddSpaceGeometryMapping(uint32 spaceID, const FString &respath);

	/**
	*当登录失败时，此方法被触发
	*
	*@param errCode  ，错误的代码（uint32）
	*@param errName ，错误的名称（FString）
	*@param errDesc ，错误（FString）
	*
	*@return 无
	*/
	virtual void OnLoginFailed(int32 errCode, const FString& errName, const FString& errDesc, const TArray<uint8>& serverDatas);///<当登录失败时，此方法被触发

	virtual void OnDisconnect();///<当与服务器的连接断开时，此方法被触发 
};