// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/NPCBaseObjectInterface.h"
#include "GameData/CsvTableRowBase.h"
#include "GameData/Shape/BaseShape.h"
#include "MonsterInterface.generated.h"

/*
* 文件名称：MonsterInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：all
* 创建时间：2017-07-29
*/



/// 控制模式表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FAngleDecalTable : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()

		/// 预警光效id
		UPROPERTY(BlueprintReadWrite)
		FString DecalEffectID;
};

/**
 *
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
		typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterInterface();
	~UMonsterInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterInterface'"); } //获取蓝图对象路径



	/**
	*移动脚本类型改变
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		virtual void OnRep_moveScriptID();


	/**
	*服务器通知播放登场动作
	*
	*@param ActionId ，动作ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void CLIENT_PlayAdmissionAction(const FString& ActionId);

	/**
	*服务器通知显示特殊阶段进度条
	*
	*@param FString ，进度条说明文字
	*@param float ，进度条持续时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_ShowSpecialProgress(const FString& Text, const float& PersistTime, const FString& iconName);

	/**
	*服务器通知结束特殊阶段进度条
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_HideSpecialProgress();

	/**
	*服务器通知添加主动攻击范围
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void CLIENT_AddClientAttackTrap(const int32& Shape, const FString& Range, const float& Height);

	/**
	*服务器通知添加取消攻击范围
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void CLIENT_CancelClientAttackTrap();

	/**
	*服务器通知添加AI主动反应范围
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void CLIENT_AddClientInitiativeTrap(const int32& Shape, const FString& ShapeParams, const float& Height);

	/**
	*服务器通知取消AI主动反应范围
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void CLIENT_CancelClientInitiativeTrap();

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void OnEnterAttackRange(int32 EID);

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void RPC_CELL_onClientEnterAIAttackTrap(int32 EID);

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void OnLeaveAttackRange(int32 EID);

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void RPC_CELL_onClientLeaveAIAttackTrap(int32 EID);

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void OnEnterInitiativeRange(int32 EID);

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void RPC_CELL_onClientEnterInitiativeTrap(int32 EID);

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void OnLeaveInitiativeRange(int32 EID);

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void RPC_CELL_onClientLeaveInitiativeTrap(int32 EID);

	/**
	*服务器通知开启预警光效
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_OpenInitiactiveTrapEffect(const int32& Shape, const FString& Range, const float& Height);

	/**
	*服务器通知关闭预警光效
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_CloseInitiactiveTrapEffect();

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void CLIENT_PlayerReTriggerTrap();///玩家重新触发我的攻击陷阱和主动反应陷阱

		/**
		*服务器通知创建光墙
		*
		*@return 无
		*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_CreateFightArea();

	/**
	*服务器通知离开光墙
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_OnLeaveFightArea();

	/**
	*服务器通知怪物改变自身朝向至指定范围内的指定entity
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_SimulationCircle(const float& hornSpeed, int32 targetID);

	/**
	*服务器通知停止转向到指定entity
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_StopSimulationCircle();

	/**
	*服务器通知怪物一直朝向玩家
	*
	*@param bool ，State为true则一直面向，为false则为正常状态
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_FaceToPlayer(bool State);

	/**
	*服务器通知怪物头顶冒泡（说话气泡）
	*
	*@param FString 语音ID
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_onPlaySpeechBubbles(const FString& voiceID);

	/**
	*服务器通知客户端显示怪物刷新时间
	*
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_DisplayCounodwn(const FString& endReviveTime);

	/**
	* 怪物吹风效果
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void CLIENT_addMonsterBlow(const FVector& WindDir, const float& WindSpeed);
	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterInterface")
		void CLIENT_endMonsterBlow();


	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_onClientLeaveAIBattleRegion();

	void StartClientChase();

	void StopClientChase();

	void GetMoveTargetPosStr();

	//清楚自身的追击位置记录
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void CLIENT_RemoveChasePosInfo();

	virtual void InitBlueCB() override;

	void RPC_CELL_onAttackTarget();

	void RPC_CELL_onSetControlledBy();

	void RPC_CELL_startFalling();

	void RPC_onClickCallBack();

	void RPC_CELL_notifyChangeMonsterDirection(FString yaw);

	void RPC_CELL_updateMoveTargetPosFromClient(FString posStr);

	void RPC_CELL_OnPlayAdmissionAction();

	void RPC_CELL_ChangeMonsterParent(KBEngine::FVariantArray Args);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_OnPlayerBeginPush();
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_OnPlayerEndPush();

	void NotifyMonsterEndFallLand();

	//小地图显示怪物闪烁点提示
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void ShowMonsterLocationTwinkle(const int32& bTwinkle);

private:
	UBaseShape* CreateBoxShape(int Type, const FString& Range, const float& Height);
	UBaseShape* CreateSphereShape(int Type, const FString& Range, const float& Height);
	UBaseShape* CreateCylinderShape(int Type, const FString& Range, const float& Height);
	UBaseShape* CreateSectorShape(int Type, const FString& Range, const float& Height);
	void OnPlayerEnterAttackRange(); ///玩家进入主动攻击陷阱
	void OnPlayerLeaveAttackRange(); ///玩家离开主动攻击陷阱
	void OnPlayerEnterInitiativeRange(); ///玩家进入主动反应陷阱
	void OnPlayerLeaveInitiativeRange(); ///玩家离开主动反应陷阱


private:
	UBaseShape* pAttackShape; //主动攻击陷阱
	UBaseShape* pInitiativeShape; //主动反应陷阱

	UPROPERTY()
		FTimerHandle TurnTimer;		///转向的Timer

	UPROPERTY()
		FTimerHandle LookAtTimer;	///朝向玩家的Timer

	FTimerHandle ChaseTimerHandle; //追击Timer

	///怪物预警光效
	//UPROPERTY()
	//AEffectEmitter* MonsterTrapEffect;

	UPROPERTY()
		int32 MonsterTrapEffectUID = -1;

	//怪物是否在转向中的判断
	UPROPERTY()
		bool isTurning = false;

	//怪物游走时一直面向玩家
	UPROPERTY()
		bool isLookAt = false;

	int32 chaseEntityID;


	//------------------------------Test--------------------------
public:
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void RandomMove(float range);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterInterface")
		void ChaseActor(int32 targetID);
};
