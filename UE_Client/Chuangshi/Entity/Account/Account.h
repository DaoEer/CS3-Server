#pragma once

#include "KBEngine.h"
#include "Entity/Alias.h"
#include "GameData/RoleInfo.h"
#include "CS3Base/CS3Entity.h"

/*
* 文件名称：Account.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/


class Account : public CS3Entity
{
	KBE_DECLARE_ENTITY_MAP();
	typedef CS3Entity Supper;

public:
	Account();
	~Account();
	

	void RequestInitRoles();///<请求初始化角色

	/**
	*Define method
	*请求初始化角色服务器数据
	*
	*@param val ，角色数据列表（FVariant&）
	*
	*@return 无
	*/
	void RequestInitRolesCB(const FVariant& val);

	/**
	*添加角色
	*
	*@param playerName ，角色名称（FString）
	*@param profession ，角色职业（int32）
	*@param camp ，角色阵营（int32）
	*@param gender ，角色性别（int32）
	*
	*@return 无
	*/
	void AddRole( FString playerName, int32 profession, int32 camp, int32 gender);

	/**
	*Define method
	*添加角色服务器数据
	*
	*@param val ，角色数据（FVariant&）
	*
	*@return 无
	*/
	void AddRoleCB(const FVariant& val);


	void EnterGame(uint64 dbid);///<开始游戏服务器数据
	void Logoff();///<log关
	void DeleteRole(uint64 dbid);///<删除角色

	void RoleFrozenNotification(const FString& EndTime);///角色处于冻结状态通知

	/**
	*Define method
	*删除角色服务器数据
	*
	*@param dbid ，角色数据库唯一标识（uint64）
	*
	*@return 无
	*/
	void DeleteRoleCB(uint64 dbid);;///<删除角色服务器数据

	/**
	*Define method
	*创建服务器数据
	*
	*
	*@return 无
	*/
	void AccountCreateCB();

	void SetAccountInfo(const FVariant& val);
	///游戏付费时间已经用完通知
	void GameTimeHasUsedUp();
	/**
	*Define method
	*客户端同步服务器时间
	*
	*@param ServerTime 服务器时间
	*
	*@return 无
	*/
	void TimeSynchronization(FString& ServerTime);

	/**
	*Define method
	*服务器状态消息
	*
	*@param statusID ，状态ID（int32&）
	*@param args ，参数（FString&）
	*
	*@return 无
	*/
	void OnStatusMessageCB(const int32& statusID, const FString& args);


	/**
	*设置2D坐标信息
	*
	*@param nv ，（FVector2D）
	*@param ov ，（FVector2D）
	*
	*@return 无
	*/
	void set_vector2Value(const FVector2D &nv, const FVector2D &ov);

	/**
	*设置3D坐标信息
	*
	*@param nv ，（FVector）
	*@param ov ，（FVector）
	*
	*@return 无
	*/
	void set_vector3Value(const FVector &nv, const FVector &ov);

	/**
	*Define method
	*创建角色回调
	*
	*@return 无
	*/
	void CreateRoleCallback();

	/**
	*Define method
	*通知登录排队信息
	*
	*@param rank,排名队列中每次
	*@param time,平均登陆时间
	*@param count,排队总人数
	*
	*@return 无
	*/
		void ReceiveWattingInfo(const int32& rank, const float& time, const int32& count);

		//取消登陆排队
		void CancelLoginQueue();

		/**
		*Define method
		*通知取消排队
		*
		*@param isInQueue,是否还在排队队列中(如果还在，意味着取消失败)
		*
		*@return 无
		*/
		void OnCancelLoginQueue(const int32& isInQueue);


	void setModifyFaceData(FaceInfoList& faceinfolist,FaceStyle& facestyleinfo,ModelList& modelList);

	/**
	*输入礼包码
	*
	*@return 无
	*/
	void RequestActivationKey(const FString& key, const FString& playerName);

	/**
	*礼包码激活结果 (1:成功，0：失败)
	*
	*@return 无
	*/
	void onActivationKeyResult(const int8& result);

public:
	FROLEINFO roleInfos[3];///<标签信息数组
};


