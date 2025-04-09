#pragma once

#include "GameData/CS3Object.h"
#include "AtkState.generated.h"

/*
* 文件名称：AtkState.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：huting
* 创建时间：2017-03-08
*/


#pragma region	角色战斗状态
/*
 *	#角色战斗状态
 */
UENUM(Blueprintable)
enum class EATTACT_STATE : uint8 
{
	None                    = 0,    //无模式
	NULL_ATT				= 1,	// 无辅助攻击
	CONTINUITY_ATT			= 2,	// 连续普攻
	AUTO_ATT				= 3,	// 自动战斗
	AUTO_ONCE_ATT			= 4,	// 一键连招
	SKILL_ONCE_ATT			= 5,	// 技能攻击一次
	AUTO_HOMING_SPELL_ATT	= 6,	// 自动引导攻击
	HALF_HOMING_SPELL_ATT   = 7,    // 半自动引导攻击
	AUTO_FIGHT_IN_STORY		= 8,	// 剧情中战斗状态
	AUTO_FIGHT_IN_XINMO_CTRL= 9,	// 心魔附身状态
	ARDER_FISH_MODE         = 10,   // 钓鱼模式
	ARDER_JINGSU_MODE	    = 11,   // 野外竞速模式
	BEHAVIOR_CONFUSION      = 12,   // 混乱
	BEHAVIOR_GLIDING        = 13,   // 滑翔
	BEHAVIOR_SHIELD         = 14,   // 举盾模式
	BEHAVIOR_FLY_DEKUVERY   = 15,   // 轨道飞行模式
	NAVIGATE_MOVE           = 16,   // 自动寻路
	BEHAVIOR_HEHUA			= 17,   // 荷花模式
	BEHAVIOR_LEIZHEN		= 18,   // 雷阵模式
	BEHAVIOR_SHOOT			= 19,   // 射击模式
	BEHAVIOR_CHAOFENG		= 20,	// 嘲讽模式
	BEHAVIOR_SHENFENGMIJING = 21,	// 神风秘径
	BEHAVIOR_FALL			= 22,	// 降落模式
	BEHAVIOR_BAGUAZHEN		= 23,	// 八卦阵模式
	BEHAVIOR_FEISHENG		= 24,	// 飞升模式
	BEHAVIOR_MIJING			= 25,	// 新版秘境
	BEHAVIOR_BATTERY		= 27,	// 操作火炮
	BEHAVIOR_GHOSTEYE		= 30,	// 鬼瞳之眼探查模式
	BEHAVIOR_SHOOTYCJMD		= 31,   // 勇闯绝命岛射击模式
	BEHAVIOR_TRAINSOLDIER   = 32,   // 练兵模式
	BEHAVIOR_EQUIPBUILD		= 33,   //帮会掠夺战器械建造模式
	BEHAVIOR_MOVEVEHICLE = 34,      //可移动载具模式（多人载具）
	BEHAVIOR_YCJMD_SKY_CARRIER = 35,    //吃鸡乘大鸟载具空中飞行(新版本吃鸡)
	BEHAVIOR_YCJMD_PARACHUTE = 36,   //吃鸡跳伞未开伞(新版本吃鸡)
	BEHAVIOR_YCJMD_PARACHUTE_OPEN = 37   //吃鸡跳伞已开伞(新版本吃鸡)
};

#pragma endregion

#pragma region	能激活的行为

UENUM(Blueprintable)
enum class ECAN_ACTIVATE_BEHAV : uint8
{
	MOVE_TO_TARGET = 0, //移动到目标
	MOVE_TO_POS    = 1, //移动到位置
	USE_SKILL      = 2, //使用技能
	PICKUP_ITEM    = 3, //拾取物品
};

#pragma endregion

#pragma region	角色战斗基类
/*
 *	#角色战斗基类
 */
UCLASS(abstract)
class CHUANGSHI_API UAtkStateBase : public UCS3Object
{
	GENERATED_BODY()

public:
	UAtkStateBase();
	~UAtkStateBase();

	/** 创建不同对象实例 */
	UFUNCTION(BlueprintCallable, Category = "AtkStateBase|Create")
		static UAtkStateBase* Create(EATTACT_STATE State = EATTACT_STATE::NULL_ATT);

	/** 初始化角色战斗基类数据 */
	virtual void InitStateData();

	virtual EATTACT_STATE GetAttState() const { return EATTACT_STATE::NULL_ATT; }

	/** 是否为全自动状态 */
	virtual bool IsAutoState() { return true; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {});

	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {});

	/** 优先级 */
	int32 GetPriority() { return Priority; }

	/** 是否能激活该行为 */
	bool IsCanActivateBehav(ECAN_ACTIVATE_BEHAV Behav) { return  ActivateBehav.Contains(Behav); }


	bool GetIsleaving() { return bIsLeaveing; }
public:
	static void AddPriorityToDictionary();
	static TMap<EATTACT_STATE, int32> PriorityDictionary;//优先级
protected:
	bool bIsLeaveing = false;
	int32 Priority;///<优先级
	TArray<ECAN_ACTIVATE_BEHAV> ActivateBehav;
};
#pragma endregion

#pragma region	无状态
/*
*	#无状态
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkNullState: public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::NULL_ATT; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	连续普攻
/*
*	#连续普攻
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkContinuityState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::CONTINUITY_ATT; }

	/** 初始化角色战斗基类数据 */
	virtual void InitStateData();

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	自动战斗
/*
*	#自动战斗
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkAutoFightState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::AUTO_ATT; }

	/** 初始化角色战斗基类数据 */
	virtual void InitStateData();

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;

private:
	void OnLeaveAtkState();///<退出自动战斗
private:
	FTimerHandle LeaveAtkStateHandle;///<自动战斗定时器30分钟退出自动战斗
};

#pragma endregion

#pragma region	一键连招
/*
*	#一键连招
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkAutoOnceState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::AUTO_ONCE_ATT; }

	/** 初始化角色战斗基类数据 */
	virtual void InitStateData();

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	技能攻击一次
/*
*	#技能攻击一次
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkSkillOnceState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::SKILL_ONCE_ATT; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	自动引导攻击
/*
*	#自动引导攻击
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkHomingSpellOnceState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::AUTO_HOMING_SPELL_ATT; }

	/** 初始化角色战斗基类数据 */
	virtual void InitStateData();

	/** 是否为全自动状态 */
	virtual bool IsAutoState() { return false; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	半自动引导攻击
/*
*	#半自动引导攻击
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkHalfHomingSpellOnceState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::HALF_HOMING_SPELL_ATT; }

	/** 初始化角色战斗基类数据 */
	virtual void InitStateData();

	/** 是否为全自动状态 */
	virtual bool IsAutoState() { return false; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	剧情中战斗攻击
/*
*	#剧情中战斗攻击
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkFightInStoryState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::AUTO_FIGHT_IN_STORY; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	心魔附身状态
/*
*	#心魔附身状态
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAtkFightInXinMoState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::AUTO_FIGHT_IN_XINMO_CTRL; }

	/** 初始化角色战斗基类数据 */
	virtual void InitStateData();

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;

	void GetXinMoData(TArray<FString>& _ExcludeList, TArray<FString>& _ActForbids);
private:
	void SetXinMoParameters(TArray<FVariant> Parameters = {});

private:
	TArray<FString> ExcludeList;
	TArray<FString> ActForbids;
};

#pragma endregion

#pragma region	嘲讽行为
/*
*	#嘲讽
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UChaoFengMode : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_CHAOFENG; }

	/** 初始化角色战斗基类数据 */
	virtual void InitStateData();

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	钓鱼模式
/*
*	#钓鱼模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UArderFishState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	UArderFishState();

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::ARDER_FISH_MODE; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;

private:
	float CamUpValue;
};

#pragma endregion

#pragma region	野外竞速模式
/*
*	#野外竞速模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UArderJingSuState : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::ARDER_JINGSU_MODE; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	混乱模式
/*
*	#混乱模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConfusionState : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_CONFUSION; }

	/** 初始化角色战斗基类数据 */
	virtual void InitStateData();

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	滑翔模式
/*
*	#滑翔模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UGlidingState : public UAtkStateBase
{
	GENERATED_BODY()
public:
	UGlidingState() {};
	~UGlidingState();
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_GLIDING; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;

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

private:
	/**
	*
	*BlueprintCallable，进入滑翔模式
	*
	*@param ForwardForceSpeed 前进的速度
	*@param DownForceSpeed 下落的速度
	*
	*@return 无
	*/
	void OnEnterGliding(float ForwardForceSpeed, float DownForceSpeed);

	/**
	*
	*BlueprintCallable，离开滑翔模式
	*
	*
	*@return 无
	*/
	void OnLeaveGliding();

	/**
	* @brief 添加自动飞行力
	*
	* @return 这个力的ID
	*/

	void AddAutoFlyForce(float ForwardForceSpeed, float DownForceSpeed);

	/**
	* @brief 停止飞行力
	*
	* @return
	*/

	void StopFlyForce();
private:
	int32 GlidingCamScaleHeadle = -1;
	TArray<int32> FlyForceIDArr;//飞行力的ID容器
	TArray<FTimerHandle> FlyTimeHandles;
};

#pragma endregion

#pragma region	举盾模式
/*
*	#举盾模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UPutOnShieldMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_SHIELD; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	轨道飞行模式
/*
*	#轨道飞行模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UFlyOrbitMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_FLY_DEKUVERY; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	自动寻路
/*
*	#自动寻路
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UNavigateMoveMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::NAVIGATE_MOVE; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
private:
	bool bIsEnterExecuteOperation = false;
	bool bIsLeaveExecuteOperation = false;
};

#pragma endregion

#pragma region	荷花模式
/*
*	#荷花模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UOnHehuaMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_HEHUA; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion


#pragma region	雷阵模式
/*
*	#雷阵模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API ULeiZhenMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_LEIZHEN; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	射击模式
/*
*	#射击模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UShootMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_SHOOT; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
	FString GetStateType() { return StateType; };
	FString GetOtherValue() { return OtherValue; };
	void SetOtherValue(FString Param) { OtherValue = Param; };
private:
	FString StateType;///<射击模式下的几种状态TPS,HUOLINGFU
	FString OtherValue;
};

#pragma endregion

#pragma region	神风秘径模式
/*
*	#神风秘径模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UShenFengMiJingMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_SHENFENGMIJING; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	神风秘径降落模式
/*
*	#神风秘径降落模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UFallMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_FALL; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};
#pragma endregion

#pragma region	八卦阵模式
/*
*	#八卦阵模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UBaGuaZhenMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_BAGUAZHEN; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;

	float GetScaleValue() { return Scale; };
	void SetCanMove(bool InCanMove);
	bool IsCanMove();
private:
	float Scale;
	bool bCanMove;
};
#pragma endregion


#pragma region	飞升模式
/*
*	#飞升模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UFeiShengState : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_FEISHENG; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
private:
	AActor *FeiShengInitTargetActor = nullptr;
};

#pragma endregion

#pragma region	新版秘境模式
/*
*	#新版秘境模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UArderMiJingState : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_MIJING; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	操作火炮行为
/*
*
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UBatteryState : public UAtkStateBase
{
	GENERATED_BODY()
public:

	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_BATTERY; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};

#pragma endregion

#pragma region	鬼瞳之眼探查模式
/*
*	#鬼瞳之眼探查模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UGhostEyeState : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_GHOSTEYE; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};
#pragma endregion

#pragma region	练兵模式
/*
*	#练兵模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTrainSoldierMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_TRAINSOLDIER; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};
#pragma endregion

#pragma region	帮会掠夺战器械建造模式
/*
*	#帮会掠夺战器械建造模式
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UEquipBuildMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_EQUIPBUILD; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
	FString GetEquipScriptID() { return ScriptID; };
	FString GetEquipItemUID() { return ItemUID; };
private:
	FString ScriptID;
	FString ItemUID;
};

#pragma region	可移动载具模式（多人载具）
/*
*	#可移动载具模式（多人载具）
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMoveVehicleMode : public UAtkStateBase
{
	GENERATED_BODY()
public:
	virtual EATTACT_STATE GetAttState() const override { return EATTACT_STATE::BEHAVIOR_MOVEVEHICLE; }

	/** 进入此状态 */
	virtual void Enter(TArray<FVariant> Parameters = {}) override;
	/** 离开此状态 */
	virtual void Leave(TArray<FVariant> Parameters = {}) override;
};
#pragma endregion
	