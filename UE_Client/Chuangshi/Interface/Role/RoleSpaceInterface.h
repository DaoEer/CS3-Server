// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "RoleSpaceInterface.generated.h"

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FVIDEO_LOAD_LEVEL
{
	GENERATED_USTRUCT_BODY()
	///下一个子关卡
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HZMG_LOAD_LEVEL")
		FString NextLevel=TEXT("");
	///是否加载界面
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HZMG_LOAD_LEVEL")
		int32 IsLoadBG = 0;
	///是否传送门流程中
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HZMG_LOAD_LEVEL")
		int32 IsLoadDoor = 0;

public:
	bool IsValid()
	{
		return (this->NextLevel.Compare(TEXT(""))) ? true : false;
	};
};

/*
* 文件名称：RoleSpaceInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：yikun
* 创建时间：2017-07-29
*/
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnEnterAreaNotifyDelegate);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FInWorldLoadingOverBack, FString, SpaceScriptID, INT32, SpaceType);

/**
 * 玩家副本接口类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleSpaceInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	
	CS3_DECLARE_INTERFACE_MAP()
public:
	
	static FString GetName() { return TEXT("RoleSpaceInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleSpaceInterface.BP_RoleSpaceInterface_C'"); } //获取蓝图对象路径

	/**
	*判断当前是否无缝加载
	*
	*@return bool，当前是无缝加载返回true，否则为false
	*/
	bool IsPlaneLoading() { return SeamLessLoading; }

	/**
	*设置当前无缝加载
	*
	*@param IsSeamLess 是否无缝加载
	*
	*@return 无
	*/
	void IsPlaneLoading(bool IsSeamLess) { SeamLessLoading = IsSeamLess; }

	/**
	*Define method
	*BlueprintNativeEvent，位面传送
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void SeamLessLoadLevel();///<BlueprintNativeEvent,设置当前无缝加载为True

	/**
	*Define method
	*BlueprintNativeEvent，开始进入位面，进行一些表现
	*
	*@param ScriptID 脚本ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void GotoSpacePlane(const FString& ScriptID);

	/**
	*Define method
	*BlueprintNativeEvent，离开位面，进行一些表现
	*
	*@param ScriptID 脚本ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void LeaveSpacePlane(const FString& ScriptID);

	/**
	*Define method
	*BlueprintNativeEvent，通知开始进入位面
	*
	*@param SpaceScriptID 脚本ID
	*@param SpaceType 副本类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void OnEnterSpaceNotify(const FString& SpaceScriptID, const INT32 SpaceType);

	UFUNCTION(BlueprintCallable, Category = "RoleSpaceInterface")
		void OnEnterSpaceNotifyEntrust();

	/**
	*Define method
	*BlueprintNativeEvent，同地图传送通知
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void OnEnterAreaNotify();

	/**
	*Define method
	*BlueprintNativeEvent，通知登录位面
	*
	*@param SpaceScriptID 脚本ID
	*@param SpaceType 副本类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void OnLoginSpaceNotify(const FString& SpaceScriptID, const INT32 SpaceType);

	/**
	*Define method
	*BlueprintNativeEvent，通知离开位面
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void OnLeaveSpaceNotify(const FString& ScriptID, const FString& SpaceType); ///<BlueprintNativeEvent,通知离开位面

	/**
	*BlueprintImplementableEvent,通知开始进入位面
	*
	*@param SpaceType 副本类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleSpaceInterface")
		void OnEnterSpaceNotifyBP(const INT32 SpaceType);

	/**
	*BlueprintImplementableEvent,通知登录位面
	*
	*@param SpaceType 副本类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleSpaceInterface")
		void OnLoginSpaceNotifyBP(const INT32 SpaceType);

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleSpaceInterface")
		void OnLeaveSpaceNotifyBP(const FString& ScriptID, const FString& SpaceType);///<BlueprintImplementableEvent,通知离开位面

	UFUNCTION(BlueprintCallable, Category = "RoleSpaceInterface")
		void RequestGoToSpace();	///<传承和潜能副本返回功能

	/**
	*Define method
	*BlueprintCallable，改变运动方式
	*
	*@param MovementMode ，运动方式（uint8&）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleSpaceInterface")
		void ChangeMovementMode(const uint8& MovementMode);
	/**
	*Define method
	*BlueprintNativeEvent 设置能否离开寻路边缘
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void SetCanWalkOffLedges(bool bCanWalkOffLedges);

	/**
	*Define method
	*BlueprintNativeEvent，同地图传送强制读条通知
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void CLIENT_ArticleToReadNotify(const int32 spaceID);

	//---------------------------------幻阵迷宫-------------------------------------------------------------------------
	UFUNCTION(BlueprintCallable, Category = "RoleSpaceInterface")
		void FlyToSubSpace(FString fPatrolID, FString sPatrolID, int32 sPoint, int32 pPoint, float speed, FVector enterPos);
	UFUNCTION(BlueprintCallable, Category = "RoleSpaceInterface")
		void StopFlyToSubSpace(FString fPatrolID);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void ShowMazeDice(bool IsVisible_);
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void ShowMazeNum(int MazeNum);
	//服务器通知开始视频加载切换地图
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void CLIENT_StartVideoLoading();

	//向服务器请求位面副本中记录的entity的坐标
	UFUNCTION(BlueprintCallable, Category = "RoleSpaceInterface")
		void GetSpaceEntityRecordPos(FString SctriptID);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void OnGetSpaceEntityRecordPos(const FString& PosStr);

	//请求传送到ExitSpace配置地图
	UFUNCTION(BlueprintCallable, Category = "RoleSpaceInterface")
		void RequestGotoExitSpace();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestGotoExitSpace();

	//点击离开副本按钮
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_clickedBtnGotoExitSpace();
	//通天塔点击离开副本按钮
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_clickedBtnGotoExitSpaceTTT();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DisconnectDeathToSpace();

	/**
	*Define method
	*BlueprintCallable 请求传送到某一线
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleSpaceInterface")
		void CELL_RequestGotoLineNumberSpace(uint8 lineNumber);

	/**
	*Define method
	*BlueprintNativeEvent 请求传送到某一线失败
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void CLIENT_RequestGotoLineNumberSpaceFailure();

	void OnSetSpaceData(uint32 spaceID, const FString& key, const FString& value);

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleSpaceInterface")
		void OnSpaceMaxLineNumberChanged();///<BlueprintImplementableEvent,通知最大线改变

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleSpaceInterface")
		void OnSetSpaceLineNumber();///<BlueprintImplementableEvent,通知当前线

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleSpaceInterface")
		void OnVideoLoadingStartPlay();

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleSpaceInterface")
		void OnVideoLoadingEndPlay();

	//服务器通知下一个子关卡（幻阵迷宫第三版）
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void OnVideoLoading(const FString& NextLevel, const int32& IsLoadBG, const int32& IsLoadDoor);

	//服务器通知重新加载子关卡
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void AgainNotifySpaceData(const FString& InSpaceScriptID);

	//服务器通知下一个子关卡(环任务新版流程)
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpaceInterface")
		void OnNotifyPreloadSpace(const FString& preloadLevel, const int32& isPreload);

	//服务器通知客户端是否在副本中关闭辅助跳跃 
	UFUNCTION(BlueprintCallable, Category = "RoleSpaceInterface")
		void OnRep_disableAssistJump();

	void SetPlayerRotation();

	void Notify_CreateLightWall();

	void RPC_RequestGoToSpace(FString SpaceScriptID, FVector Position, FVector Direction);
	void RPC_requestGotoDynamicRevivePos();
	virtual void InitBlueCB() override;

	bool IsHZMGLevel() { return VideoLoadData.IsValid(); };
	FVIDEO_LOAD_LEVEL GetVideoLoadLevelData() { return VideoLoadData; };
public:
	FOnEnterAreaNotifyDelegate OnEnterAreaNotifyEvent;
	FInWorldLoadingOverBack InWorldLoadingOverBackEvent;
	FString SpaceScriptid;
	INT32 Spacetype;
	FVIDEO_LOAD_LEVEL VideoLoadData;
private:
	void OnEnterPlane();//进入副本
	void OnleavePlane();//离开副本

private:
	bool SeamLessLoading = false; ///<无缝加载
};
