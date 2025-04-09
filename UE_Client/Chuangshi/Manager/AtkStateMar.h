// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "../Fight/AtkState/AtkState.h"
#include "../Fight/FightAssist.h"
#include "../GameData/AutomaticFightData.h"
#include "AtkStateMar.generated.h"

/*
* 文件名称：AtkStateMar.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：huting
* 创建时间：2017-10-15
*/

DECLARE_DELEGATE(FAtkNoParamDelegate);
DECLARE_DYNAMIC_DELEGATE_OneParam(FMoveToDelegate, bool, IsSuccess);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnReviveOnOrigin, bool, IsOnOrigin);
/**
 * 
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkStateMar : public UCS3Object
{
	GENERATED_BODY()
	
public:
	UAtkStateMar();
	~UAtkStateMar();

	virtual void BeginDestroy() override;

	void Leave();
public:

	void AddAllState();

	/**
	*切换无辅助
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchNullAtt(bool IsActivate);

	/**
	*切换连续普攻
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
	void SwitchContinuityAtt(bool IsActivate);

	/**
	*切换自动战斗
	*
	*@param IsActivate  是否为激活
	*@param BreakType  打断类型
	*@param level  开启的关卡名字
	*@param IDString  额外的信息
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
	void SwitchAutoFight(bool IsActivate, EBreakAutomaticType BreakType, FName level = "", FString IDString = "");

	/**
	*切换一键连招
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
	void SwitchAutoOnceAtt(bool IsActivate);

	/**
	*切换一键连招
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
	void SwitchSkillOnceAtt(bool IsActivate);

	/**
	*自动引导攻击
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
	void SwitchHomingSpellAtt(bool IsActivate);

	/**
	*半自动引导攻击
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
	void SwitchHalfHomingSpellAtt(bool IsActivate);

	/**
	*剧情中战斗状态
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
	void SwitchFightInStoryAtt(bool IsActivate);

	/**
	*切换心魔
	*
	*@param IsActivate  是否为激活
	*@param ExcludeSkillList  排除技能列表
	*@param ActForbidList  可以使用的技能类型列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
	void SwitchFightInXinMo(bool IsActivate, const TArray<FString>& ExcludeSkillList, const TArray<FString>& ActForbidList);
	
	/**
	*切换嘲讽模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchChaoFengMode(bool IsActivate);

	/**
	*切换钓鱼模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchFishMode(bool IsActivate);
	/**
	*切换野外竞速模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchJingSuMode(bool IsActivate);

	/**
	*切换雷阵模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchLeiZhenMode(bool IsActivate);
	/**
	*混乱模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchConfusionMode(bool IsActivate);

	/**
	*滑翔模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchGlidingMode(bool IsActivate, float ForwardForceSpeed, float DownForceSpeed);

	/**
	*举盾模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchPutOnShieldMode(bool IsActivate);

	/**
	*上荷花模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchOnHehuaMode(bool IsActivate);
	/**
	*轨道飞行模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchFlyOrbitMode(bool IsActivate, FString FlyPatrolID, float DelayTime = 0.0f);

	/**
	*自动寻路
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchNavigateMoveMode(bool IsActivate, FVector DstPosition, float NearbyRange, FString DstSpaceName, int AutoQuestID, bool IsSearch, bool IsArrived, int32 GossipWithType);

	/**
	*轨道飞行模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchShootMode(bool IsActivate, FString StateType=TEXT(""), FString Param1 = TEXT(""));

	/**
	*神风秘径模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchShenFengMiJingMode(bool IsActivate);

	/**
	*降落模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchFallMode(bool IsActivate);

	/**
	*八卦阵模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchBaGuaZhenMode(bool IsActivate, float Scale = 10.0f);

	/**
	*飞升模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchFeiShengMode(bool IsActivate, float Scale = 10.0f);

	/**
	*切换新版秘境模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchMiJingMode(bool IsActivate);


	/**
	*切换操作炮台模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchBatteryMode(bool IsActivate);

	/**
	*切换鬼瞳之眼探查模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchGhostEyeMode(bool IsActivate);

	/**
	*切换练兵模式
	*
	*@param IsActivate  是否为激活
	*@param ArmLength  摄像机臂长
	*@param CameraRotation  摄像机朝向
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchTrainSoldierMode(bool IsActivate,float ArmLength = 1500.0f, FVector CameraRotation = FVector(0.0f, 0.0f, 0.0f));

	/**
	*切换帮会掠夺战器械建造模式
	*
	*@param IsActivate  是否为激活
	*@param SkillID  技能ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchEquipBuildMode(bool IsActivate, const FString& ScriptID = TEXT(""), const FString& ItemUID = TEXT(""));
	FString GetEquipScriptID();
	FString GetEquipItemUID();

	/**
	*切换到移动骑乘模式
	*
	*@param IsActivate  是否为激活
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UAtkStateMar")
		void SwitchMoveVehicle(bool IsActivate);
	/**
	*此状态是否激活
	*
	*@param AttackState  攻击模式状态
	*
	*@return bool
	*/

	UFUNCTION(BlueprintPure, Category = "UAtkStateMar")
	bool IsActivateState(const EATTACT_STATE AttackState);

	/**
	*当前状态是否为全自动状态
	*
	*
	*@return bool
	*/

	UFUNCTION(BlueprintPure, Category = "UAtkStateMar")
	bool IsCurAutoState();

	/**
	*当前状态是否能激活行为
	*
	*
	*@return bool
	*/

	UFUNCTION(BlueprintPure, Category = "UAtkStateMar")
	bool IsCanActivateBehav(ECAN_ACTIVATE_BEHAV Behav);

	/**
	*获取心魔数据
	*
	*
	*@return bool
	*/

	UFUNCTION(BlueprintPure, Category = "UAtkStateMar")
		void GetXinMoData(TArray<FString>& _ExcludeList, TArray<FString>& _ActForbids);

	UAtkStateBase* GetCurAtkState(){ return CurAtkState;};///<当前状态
#pragma region	行为功能
public:
	/**
	*搜索目标
	*
	*@param UClass* SearchClass 搜索的蓝本
	*@param TArray<UClass*>& MaskClass  要屏蔽的类型，搜索以蓝本为目标，搜索完后的结果中将屏蔽的类型剔除。
	*@param TArray<ENTITY_STATE>& MaskClass  要屏蔽的状态，角色的状态，搜索结果中如果角色处于这些状态中的一个则被剔除
	*@param COMBAT_RELATION CombatRelation  阵营关系
	*@param FVector SearchCenter  搜索中心
	*@param float SearchRange  搜索半径（单位：m）
	*
	*@return 找到的目标
	*/
	UFUNCTION(BlueprintPure, Category = "AtkStateMar")
		AActor* SearchTargets(UClass* SearchClass, COMBAT_RELATION CombatRelation, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState,
			const TArray<ENTITY_FLAG>& MaskFlags, float SearchRange, FVector SearchCenter = FVector::ZeroVector);

	/**
	*目标是否OK
	*
	*@param UClass* SearchClass 搜索的蓝本
	*@param TArray<UClass*>& MaskClass  要屏蔽的类型，搜索以蓝本为目标，搜索完后的结果中将屏蔽的类型剔除。
	*@param TArray<ENTITY_STATE>& MaskClass  要屏蔽的状态，角色的状态，搜索结果中如果角色处于这些状态中的一个则被剔除
	*@param COMBAT_RELATION CombatRelation  阵营关系
	*
	*@return 找到的目标
	*/
	UFUNCTION(BlueprintPure, Category = "AtkStateMar")
		bool IsTargetOK(UClass* SearchClass, COMBAT_RELATION CombatRelation, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState,
			const TArray<ENTITY_FLAG>& MaskFlags, AActor* TargetActor);
	/**
	*自动战斗搜索目标
	*
	*@param UClass* SearchClass 搜索的蓝本
	*@param TArray<UClass*>& MaskClass  要屏蔽的类型，搜索以蓝本为目标，搜索完后的结果中将屏蔽的类型剔除。
	*@param TArray<ENTITY_STATE>& MaskClass  要屏蔽的状态，角色的状态，搜索结果中如果角色处于这些状态中的一个则被剔除
	*@param COMBAT_RELATION CombatRelation  阵营关系
	*@param TArray<AServerCharacter>  屏蔽Actors
	*@param FVector SearchCenter  搜索中心
	*@param float SearchRange  搜索半径（单位：m）
	*@param bool bReturnNotInEnemyList  没在敌对列表，是否返回
	*
	*@return 找到的目标
	*/
	UFUNCTION(BlueprintPure, Category = "AtkStateMar")
		AActor* SearchTargetsOfAutoAtt(UClass* SearchClass, COMBAT_RELATION CombatRelation, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState,
			const TArray<ENTITY_FLAG>& MaskFlags, const TArray<AServerCharacter*>& MaskActors, float SearchRange, FVector SearchCenter = FVector::ZeroVector, bool bReturnNotInEnemyList = true);

	/**
	*自动战斗目标是否OK
	*
	*@param UClass* SearchClass 搜索的蓝本
	*@param TArray<UClass*>& MaskClass  要屏蔽的类型，搜索以蓝本为目标，搜索完后的结果中将屏蔽的类型剔除。
	*@param TArray<ENTITY_STATE>& MaskClass  要屏蔽的状态，角色的状态，搜索结果中如果角色处于这些状态中的一个则被剔除
	*@param COMBAT_RELATION CombatRelation  阵营关系
	*
	*@return 找到的目标
	*/
	UFUNCTION(BlueprintPure, Category = "AtkStateMar")
		bool IsTargetOKOfAutoAtt(UClass* SearchClass, COMBAT_RELATION CombatRelation, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState,
			const TArray<ENTITY_FLAG>& MaskFlags, AActor* TargetActor, bool IsCheckPlayerTarget = true);

	/**
	*嘲讽模式搜索目标
	*
	*@param UClass* SearchClass 搜索的蓝本
	*@param TArray<UClass*>& MaskClass  要屏蔽的类型，搜索以蓝本为目标，搜索完后的结果中将屏蔽的类型剔除。
	*@param TArray<ENTITY_STATE>& MaskClass  要屏蔽的状态，角色的状态，搜索结果中如果角色处于这些状态中的一个则被剔除
	*@param FVector SearchCenter  搜索中心
	*@param float SearchRange  搜索半径（单位：m）
	*
	*@return 找到的目标
	*/
	UFUNCTION(BlueprintPure, Category = "AtkStateMar")
		AActor* SearchTargetOfChaoFeng(UClass* SearchClass, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState,
			const TArray<ENTITY_FLAG>& MaskFlags, float SearchRange, FVector SearchCenter = FVector::ZeroVector);

	/**
	*嘲讽目标是否OK
	*
	*@param UClass* SearchClass 搜索的蓝本
	*@param TArray<UClass*>& MaskClass  要屏蔽的类型，搜索以蓝本为目标，搜索完后的结果中将屏蔽的类型剔除。
	*@param TArray<ENTITY_STATE>& MaskClass  要屏蔽的状态，角色的状态，搜索结果中如果角色处于这些状态中的一个则被剔除
	*
	*@return 找到的目标
	*/
	UFUNCTION(BlueprintPure, Category = "AtkStateMar")
		bool IsTargetOKOfChaoFeng(UClass* SearchClass, const TArray<UClass*>& MaskClass, const TArray<ENTITY_STATE>& MaskState,
			const TArray<ENTITY_FLAG>& MaskFlags, float SearchRange, AActor* TargetActor);
	/**
	*移动到目标
	*
	*@param AActor* Target  要移动到的目标
	*@param float TraceRange  目标多少范围停下
	*@param FTraceCallback MoveDelegate 移动委托事件
	*
	*@return 
	*/
	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
		void MoveToTarget(AActor* Target, float TraceRange, FMoveToDelegate TraceCallback);

	/**
	*移动到位置
	*
	*@param FVector TargetPos  要移动到的目标
	*@param float TraceRange  目标多少范围停下
	*@param FTraceCallback MoveDelegate 移动委托事件
	*
	*@return 
	*/
	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
		void MoveToPos(FVector TargetPos, float TraceRange, FMoveToDelegate TraceCallback);

	/**
	*使用技能
	*
	*@param AServerCharacter UseCharacter  使用技能的character
	*@param int32 SkillID  技能ID
	*@param int32 TargetID  目标ID
	*@param FUseSkillForTargetDelegate& OnUseSkill 使用技能回调
	*
	*@return 是否能使用技能
	*/
	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
		bool UseSkill(AServerCharacter* UseCharacter, int32 SkillID, int32 TargetID, FUseSkillForTargetDelegate OnUseSkill);

	/**
	*获取可以拾取的列表
	*
	*@param AActor* DropBox  掉落宝箱
	*@param TArray<UItemBase*>& CanPickUpItemList 获取的列表
	*
	*@return
	*/
	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
		void CheakUpDropBoxList(AActor* DropBox, TArray<UItemBase*>& CanPickUpItemList);

	/**
	*使用物品
	*
	*@param int32 SkillID  要移动到的目标
	*
	*@return 是否成功
	*/
	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
		bool UseItem(int32 ID,AServerCharacter* UseCharacter, int32 &ItemUseMsg);

	/**
	*复活
	*
	*
	*/
	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
		void AutoRevive();

	/**
	*添加屏蔽的EntityID
	*
	*@param int32 EntityID  要屏蔽的ID
	*
	*@return
	*/
	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
		void AddMaskEntityID(int32 EntityID);

	/**
	*添加屏蔽的EntityID
	*
	*@param int32 EntityID  要屏蔽的ID
	*
	*@return
	*/
	UFUNCTION(BlueprintPure, Category = "AtkStateMar")
		bool IsEntityBeMask(int32 EntityID);

	//设置可以拾取的类型
	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
	void SetCanPickUpType(TArray<EAutomaticPickupType> _CanPickupType);

	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
	bool IsHaveState(const EATTACT_STATE AttackState);///<是否有此状态

	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
	FString GetShootModeState();///<获取射击模式下的状态

	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
		void SetShootModeOtherValue(FString OtherValue);///<获取射击模式下的状态
	/**
	* BlueprintCallable,添加冲刺力(冲刺技能支持)
	*
	*@param Dire	力的方向
	*@param ForceSpeed 力的速度
	*@param ForceTime 力持续的时间
	*
	* @return 这个力的ID
	*/
	int32 AddFlyForce(int Dire, float ForceSpeed, float ForceTime);

	// 目标是否隐身不可见（只有敌对关系，才是隐身不可见。其他关系，隐身半透明）
	bool IsTargetHideInGame(AServerCharacter* PlayerCharacter, AServerCharacter* TargetCharacter);

	float GetBaGuaZhenModeValue();///<获取八卦阵下移动Scale数据
	UFUNCTION(BlueprintCallable, Category = "AtkStateMar")
	void SetBaGuaZhenModeCanMove(bool InCanMove);
	bool GetBaGuaZhenModeCanMove();
private:
	//此类型是否被屏蔽
	bool IsTargetClassBeMask(const TArray<UClass*>& MaskClasses,AActor* TargetActor);
	//此状态是否被屏蔽
	bool IsTargetStateBeMask(const TArray<ENTITY_STATE>& MaskStates, AActor* TargetActor);
	//此标志位是否被屏蔽
	bool IsTargetFlagBeMask(const TArray<ENTITY_FLAG>& MaskFlags, AActor* TargetActor);
	//装备筛选
	void CheakUpEquip(UItemBase* _Item, TArray<UItemBase*>& CanPickUpItemList);
	//是否可以拾取这个类型装备
	bool IsHasPickupType(EAutomaticPickupType ItemType);
	//敌对关系判断
	bool IsRelationshipOk(AActor* Character1, AActor* Character2,COMBAT_RELATION CombatRelation);
#pragma endregion

	//归命符箓复活CD
	void ReviveCDTimerByCostItem();
	//金钱复活CD
	void ReviveCDTimerByCostMoney();

protected:

	
	bool AddAttackState(const EATTACT_STATE AttackState);///<添加状态
	bool RemoveAttackState(const EATTACT_STATE AttackState,TArray<FVariant> Parameters = {});///<移除状态

	UAtkStateBase* FindAtkStateByStateID(const EATTACT_STATE AttackState);///<通过状态ID找到这个攻击状态

	void CheakAllActiveState();///<检查所有激活的状态，切换他们的激活

	void ActivateFuntion(const EATTACT_STATE AttackState);///<激活状态功能

	bool CheakCanActivate(UAtkStateBase* WantsActivate);

public:
	//自动原地复活
	UPROPERTY(BlueprintAssignable, Category = "UAtkStateMar|Event|Revive")
		FOnReviveOnOrigin OnReviveOnOrigin;

private:
	UPROPERTY()
	UAtkStateBase* CurAtkState;///<当前状态

	EATTACT_STATE OldState;///<旧的状态

	UPROPERTY()
	TArray<UAtkStateBase* > ActivateState;///<当前激活的状态

	UPROPERTY()
	TArray<UAtkStateBase* > AllState;///<所有状态

	//所有状态的记录
	FAtkNoParamDelegate OnNullAtt;
	FAtkNoParamDelegate OnContinuityAtt;
	FAtkNoParamDelegate OnAutoFight;
	FAtkNoParamDelegate OnAutoOnceAtt;
	FAtkNoParamDelegate OnSkillOnceAtt;
	FAtkNoParamDelegate OnHomingSpellAtt;
	FAtkNoParamDelegate OnHalfHomingSpellAtt;
	FAtkNoParamDelegate OnFightInStoryAtt;
	FAtkNoParamDelegate OnFightInXinMo;
	FAtkNoParamDelegate OnArderFishMode;
	FAtkNoParamDelegate OnArderJingsuMode;
	FAtkNoParamDelegate OnConfusionMode;
	FAtkNoParamDelegate OnGlidingMode;
	FAtkNoParamDelegate OnHehuaMode;
	FAtkNoParamDelegate OnPutOnShieldMode;
	FAtkNoParamDelegate OnFlyDeliveryMode;
	FAtkNoParamDelegate OnNavigateMoveMode;
	FAtkNoParamDelegate OnLeiZhenMode;
	FAtkNoParamDelegate OnShootMode;
	FAtkNoParamDelegate OnChaoFengMode;
	FAtkNoParamDelegate OnShenFengMiJingMode;
	FAtkNoParamDelegate OnFallMode;
	FAtkNoParamDelegate OnBaGuaZhenMode;
	FAtkNoParamDelegate OnFeiShengMode;
	FAtkNoParamDelegate OnArderMiJingMode;
	FAtkNoParamDelegate OnArderBatteryMode;
	FAtkNoParamDelegate OnGhostEyeMode;
	FAtkNoParamDelegate OnTrainSoldierMode;
	FAtkNoParamDelegate OnEquipBuildMode;
	FAtkNoParamDelegate OnMoveVehicleMode;

	TArray<EAutomaticPickupType> CanPickupType;
	TArray<int32> MaskEntityID;

	TArray<int32> FlyForceIDArr;//飞行力的ID容器
	
	TArray<FVariant> CurStateLeaveParameters;//当前状态离开时需要的数据

	FVector m_DstPosition;
	float m_NearbyRange;
	FString m_DstSpaceName;
	int m_AutoQuestID;
	bool m_IsSearch;

	FTimerHandle ReviveCDTimerHandle;
	int32 ReviveCD;
};
