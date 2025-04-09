// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Entity/Alias.h"
#include "CS3Base/CS3EntityInterface.h"
#include "Fight/FightAssist.h"
#include "GameFramework/Character.h"
#include "GameData/CharacterData.h"
#include "GameData/Skill/SkillData.h"
#include "GameData/Skill/BuffData.h"
#include "Component/CS3AudioComponent.h"
#include "Fight/AtkState/AtkState.h"
#include "GameData/PlayerControllerData.h"
#include "SkillInterface.generated.h"

/*
* 文件名称：SkillInterface.h
* 功能说明：
* 文件作者：wuxiaoou
* 目前维护：all
* 创建时间：2016-09-22
*/

DECLARE_STATS_GROUP(TEXT("USkillInterface"), STATGROUP_USkillInterface, STATCAT_Advanced);

//通过控制台命令控制得是否开启 显示技能名称效果
extern bool Console_IsPromptSkillName;

class GameObject;

USTRUCT()
struct FBUFF_BULLET_EFFECT_DATA
{
	GENERATED_BODY()
public:
	//效果序号：效果实例UID
	TMap<int32, int32> EffectData;
};

USTRUCT()
struct FBUFF_BULLET_EFFECT_MUTIPLE_DATA
{
	GENERATED_BODY()
public:
	//效果ID：效果数据
	TMap<FString, FBUFF_BULLET_EFFECT_DATA> BuffBulletEffectData;
};

/**
 * 文件名称：SkillInterface.h
 * 功能说明：技能接口类
 * 文件作者：JACK
 * 创建时间：2016/10/14/12:11
 * 更改记录:
 */

class UPoseableMeshComponent;

UCLASS(BlueprintType)
class CHUANGSHI_API USkillInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	USkillInterface();
	
	static FString GetName() { return TEXT("SkillInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_SkillInterface.BP_SkillInterface_C'"); } //获取蓝图对象路径

	virtual void onEnterWorld() override;
	virtual void onLeaveWorld() override;
	virtual void PostInitProperties() override;
	~USkillInterface();

	///Actor创建完成
	void OnActorCreaterFinish();
	
	void RPC_onStopFlyPatrol(FString CurFlyPatrolID);

	void RPC_onBulletCollisionBegin(KBEngine::FVariantArray args);

	void onBulletCollisionArrive(KBEngine::FVariantArray args);

	/**
	*Define method
	*BlueprintCallable,初始化玩家技能列表S2C
	*
	*@param SkillIDs 玩家技能ID列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void InitSkills(const TArray<int32>& SkillIDs);

	/**
	*Define method
	*BlueprintCallable,增加一个技能C2S
	*
	*@param SkillID 技能ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnAddSkill(const int32& SkillID);

	/*
	*Define method
	*BlueprintCallable,移除一个技能C2S
	*
	*@param SkillID 技能ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnRemoveSkill(const int32& SkillID);

	/// 玩家等级改变提示技能升级
	UFUNCTION(BlueprintCallable, Category = "RoleKitBagInterface")
		void OnPlayerLevelChange();

	/**
	*BlueprintCallable,增加一个buff
	*
	*@return 无
	*/
	void AddBuff(const BuffDataType& buffData );
	void OnAddBuff(int32 BuffIndex );
	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void OnAddBuffBP(FBuffUIData BuffUIData);

	/**
	*BlueprintCallable,移除一个buff
	*
	*@return 无
	*/
	void RemoveBuff(int32 BuffIndex);
	void OnRemoveBuff(int32 BuffIndex, int32 BuffID, FString BuffScript);
	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void OnRemoveBuffBP(int32 BuffIndex);

	/**
	*Define method
	*BlueprintCallable，开始Buff效果
	*
	*@param BuffIndex buff 下标
	*@param CasterID buff 施法者
	*@param actionIndex 动作标识号
	*@param ActionID buff动作
	*@param BeginTime 动作起始时间
	*@param EffectID buff光效
	*@param Sound buff声音
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void PlayBuffEffect(const int32 BuffIndex, const int32 CasterID, const int32& ContinuousId,
			const TArray<FString>& ActionID, const TArray<FString>& BeginTime, const FString& EffectID,
			const FString& SoundID);

	/**
	*BlueprintCallable,按照buff脚本查找buff
	*
	*@return buff index数组
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		TArray<int32> findBuffsByBuffScript(FString BuffScript);

	/**
	*BlueprintCallable,按照buffID查找buff
	*
	*@return buff index数组
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		TArray<int32> findBuffsByBuffID(const int32& BuffID);

	/**
	*BlueprintCallable,查询是否有某buffID的buff
	*
	*@return bool
	*/
	UFUNCTION(BlueprintPure, Category = "SkillInterface")
		bool HasBuffByID(const int32& BuffID);

	/**
	*BlueprintCallable,查询是否有某buffIndex的buff
	*
	*@return bool
	*/
	UFUNCTION(BlueprintPure, Category = "SkillInterface")
		bool HasBuffByIndex(const int32& BuffIndex);

	/*获取所有的buff数据*/
	TMap<int32, BuffDataType> getAttrBuffs();
	/**
	*BlueprintCallable,使用技能C2S
	*
	*@param SkillID 技能ID
	*@param targetID 目标对象ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void UseSkill(int32 SkillID, int32 TargetID);

	void RealUseSkill(int32 SkillID, int32 TargetID, FUseSkillForTargetDelegate& OnUseSkill);

	/**
	*,使用位置技能C2S
	*
	*@param SkillID 释放的技能ID
	*@param TargetPostion 目标对象位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void UsePostionSkill(const int32&  SkillID, const FVector& TargetPostion);

	///设置禁用的三段跳技能
	void CLIENT_SetForbidJumpSkillIDs(const FString& SkillIDs);

	/**
	*BlueprintCallable,设置正在使用的技能
	*
	*@param SkillID 技能ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void SetCastingSkill(const int32& skillID);

	/**
	*BlueprintCallable,是否正在使用技能
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool IsCastingSkill();

	/**
	*Define method
	*BlueprintCallable,技能中断S2C
	*
	*@param SkillID 释放的技能ID
	*@param Reason 技能中断Reason
	*@param actionIndex 动作标识号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void SkillInterrupted(int32 SkillID, int32 Reason, const int32& actionIndex);

	/**
	*Define method
	*BlueprintCallable,对目标正式施法（使用技能）S2C
	*
	*@param SkillID 释放的技能ID
	*@param targetID 目标对象ID
	*@param ActionID 动作ID
	*@param BeginTime 动作起始时间
	*@param actionIndex 动作标识号
	*@param CasterID 施法者ID
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CastSkillToTarget(int32&  SkillID, const uint8& isInstantSkill, const int32&  TargetID,
			const TArray<FString>& ActionID, const TArray<FString>& BeginTime, const int32& ContinuousId, const int32& CasterID);

	/**
	*Define method
	*BlueprintCallable，对位置正式施法（使用技能）S2C
	*
	*@param  skillID 释放的技能ID
	*@param  PosX 位置X
	*@param  PosY 位置Y
	*@param  PosZ 位置Z
	*@param ActionID 动作ID
	*@param BeginTime 动作起始时间
	*@param CasterID 施法者ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CastSkillToPosition(int32&  SkillID,const uint8& isInstantSkill, const float& PosX, const float& PosY,
			const float&  PosZ, const TArray<FString>& ActionID, const TArray<FString>& BeginTime,
			const int32& ContinuousId, const int32& CasterID);

	/**
	*Define method
	*BlueprintCallable,对目标正式施法（使用技能）S2C
	*
	*@param SkillID 释放的技能ID
	*@param targetID 目标对象ID
	*@param ActionID 动作ID
	*@param BeginTime 动作起始时间
	*@param actionIndex 动作标识号
	*@param CasterID 施法者ID
	*@param ProxyID 代理人ID
	*@return 无
	*/
	void StartCastSkillToTarget(int32&  SkillID, const uint8& isInstantSkill, const int32&  TargetID,
		const TArray<FString>& ActionID, const TArray<FString>& BeginTime, const int32& ContinuousId, const int32& CasterID, const int32& ProxyID = -1);

	/**
	*Define method
	*BlueprintCallable，对位置正式施法（使用技能）S2C
	*
	*@param  skillID 释放的技能ID
	*@param  PosX 位置X
	*@param  PosY 位置Y
	*@param  PosZ 位置Z
	*@param ActionID 动作ID
	*@param BeginTime 动作起始时间
	*@param CasterID 施法者ID
	*@param ProxyID 代理人ID
	*
	*@return 无
	*/
	void StartCastSkillToPosition(int32&  SkillID, const uint8& isInstantSkill, const float& PosX, const float& PosY,
		const float&  PosZ, const TArray<FString>& ActionID, const TArray<FString>& BeginTime,
		const int32& ContinuousId, const int32& CasterID, const int32& ProxyID = -1);
	/**
	*Define method
	*BlueprintCallable,对目标正式施法（使用客户端技能）S2C
	*
	*@param SkillID 释放的技能ID
	*@param targetID 目标对象ID
	*@param ActionID 动作ID
	*@param BeginTime 动作起始时间
	*@param actionIndex 动作标识号
	*@param CasterID 施法者ID
	*@param ProxyID 代理人ID
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
	void CastCSkillToTarget(int32&  SkillID, const uint8& isInstantSkill, const int32&  TargetID,
		const TArray<FString>& ActionID, const TArray<FString>& BeginTime, const int32& ContinuousId, const int32& CasterID, const int32& ProxyID);
	/**
	*Define method
	*BlueprintCallable，对位置正式施法（使用客户端技能）S2C
	*
	*@param  skillID 释放的技能ID
	*@param  PosX 位置X
	*@param  PosY 位置Y
	*@param  PosZ 位置Z
	*@param ActionID 动作ID
	*@param BeginTime 动作起始时间
	*@param CasterID 施法者ID
	*@param ProxyID 代理人ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
	void CastCSkillToPosition(int32&  SkillID, const uint8& isInstantSkill, const float& PosX, const float& PosY,
		const float&  PosZ, const TArray<FString>& ActionID, const TArray<FString>& BeginTime,
		const int32& ContinuousId, const int32& CasterID, const int32& ProxyID);
	/**
	*Define method
	*BlueprintCallable 受击播放动作光效（使用技能）S2C
	*@param CasterID 施放者ID
	*@param targetID 目标对象ID
	*@param actionIndex 动作标识号
	*@param ActionID 动作ID
	*@param EffectID 光效ID
	*@param SoundID 声音ID
	*@param BeginTime 动作起始时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void BeHitPlayEffect(int32 const& CasterID, int32 const& TargetID, const int32& ContinuousId,
			const TArray<FString>& ActionID, const FString& EffectID, const FString& SoundID,
			const TArray<FString>& BeginTime);

	/**
	*Define method
	*BlueprintCallable 受击播放动作光效(仅受术者客户端可见)
	*@param CasterID 施放者ID
	*@param targetID 目标对象ID
	*@param actionIndex 动作标识号
	*@param ActionID 动作ID
	*@param EffectID 光效ID
	*@param SoundID 声音ID
	*@param BeginTime 动作起始时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void BeHitPlayEffectLocal(int32 const& CasterID, int32 const& TargetID, const int32& actionIndex, const TArray<FString>& ActionID, const FString& EffectID, const FString& SoundID, const TArray<FString>& BeginTime);

	/**
	*Define method
	*BlueprintCallable持有效果HoldEffectPlayEffect播放动作光效声音（使用技能）S2C
	*
	*@param EffectIndex 持有效果索引
	*@param actionIndex 动作标识号
	*@param ActionID 动作ID
	*@param EffectID 光效ID
	*@param SoundID 声音ID
	*@param BeginTime 动作起始时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void HoldEffectPlayEffect(int32 CasterID, int32 EffectIndex, const int32& ContinuousId,
			const TArray<FString>& ActionID, const FString& EffectID, const FString& SoundID,
			const TArray<FString>& BeginTime);

	/**
	*Define method
	*BlueprintCallable持有效果HoldEffectPlayEffect结束S2C
	*
	*
	*@param EffectIndex 持有效果索引
	*@param actionIndex 动作标识号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void HoldEffectEndEffect(int32 EffectIndex, const int32& actionIndex);

	/**
	*Define method
	*BlueprintCallable 发出连线光效
	*
	*@param LinkerID 发起连线者ID
	*@param BeLinkerID 被连线者ID
	*@param BuffIndex 连线者连线buffIndex
	*@param EffectID 光效ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void BuffPlayLinkEffect(int32 BeLinkerID, int32 BuffIndex, const FString& EffectID);

	/**
	*Define method
	*BlueprintCallable 结束连线光效
	*
	*@param BuffIndex 连线者连线buffIndex
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void BuffEndPlayLinkEffect(int32 BuffIndex);

	/**
	 *Define method
	 *BlueprintCallable，接受技能处理，比如伤害S2C
	 *
	 *@param skillID  释放的技能ID
	 *@param DamageType 伤害类型
	 *@param Damage 伤害值
	 *@param ActionID 动作ID
	 *@param EffectID 光效ID
	 *
	 *@return 无
	 */
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void ReceiveSkill(int32 CasterID, int32 SkillID, int32 DamageType, int32 Damage, uint8 IsCritical, uint8 IsParry);

	/**
	*Define method
	*BlueprintCallable，闪避某人的技能打击
	*
	*@param CasterID  施法者ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void onDodgeSkillHit(int32 CasterID);

	/**
	 *Define method
	 * BlueprintCallable,设置冷却时间S2C
	 *
	 *@param CooldownIDs 冷却ID列表
	 *@param RemainingTimes 剩余时间列表
	 *@param PersistTimes   CD总时间列表
	 *
	 *@return 无
	 */
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void SetCooldown(TArray<FString>& CooldownIDs, TArray<FString>& EndTimes, TArray<FString>& PersistTimes);

	/**
	*Define method
	*
	*@param bool 是否清除所有CD
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void ClearCooldown(bool isClear);


	/**
	 *BlueprintImplementableEvent,更新技能快捷栏的数据
	 *
	 *@param SkillID  技能ID
	 *@param RemainningTime CD剩余时间
	 *@param PersistTime	CD总时间
	 *
	 *@return 无
	 */
	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void OnSetCooldown(int32 SkillID, float RemainningTime, float PersistTime);

	/**
	 *BlueprintImplementableEvent,更新角色技能列表数据
	 *
	 *@param SkillID 技能ID
	 *@param IsAddSkill 是否是添加技能
	 *
	 *@return 无
	 */
	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void UpdateSkillList(int32 SkillId, bool IsAddSkill);

	/**
	*Define method
	*BlueprintCallable,受击击退表现
	*
	*@param DX	位移X坐标
	*@param DY	位移Y坐标
	*@param DZ	位移Z坐标
	*@param MoveSpeed  击退速度
	*@param ActionID 击退动作ID
	*@param ActionBeginTime 动作起始时间
	*@param CasterID   施法者ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnBeHitBackNew(float DX, float DY, float DZ, int32 buffID, float MoveSpeed, const FString& ActionID, float ActionBeginTime, int32 CasterID);

	void MonsterBeHitBackNew(GameObject* BeAtkEntity, AServerCharacter* BeAtkActor, float MoveSpeed, FVector Dest, int32 CasterID);
	void RoleBeHitBackNew(GameObject* BeAtkEntity, AServerCharacter* BeAtkActor, float MoveSpeed, FVector Dest, int32 CasterID);
	void RPC_OnSynHitBackPos(int32 buffID, FVector desPosition);

	/**
	*Define method
	*BlueprintCallable,播放高亮效果
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void PlayModleHighlight(int32 CasterID);

	/**
	*Define method
	* BlueprintCallable,结束击退
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnEndHitBack(int32 CasterID, const FString& HitBackActionId, const FString& GetUpActionId);
	void EndHitBack(int32 CasterID, const FString& HitBackActionId, const FString& GetUpActionId);

	/**
	*Define method
	*BlueprintCallable,客户端控制的击退表现
	*@param DX	位移X坐标
	*@param DY	位移Y坐标
	*@param DZ	位移Z坐标
	*@param MoveSpeed  击退速度
	*@param ActionID 动作ID
	*@param ActionBeginTime 动作起始时间
	*@param CasterID   施法者ID
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_ControlledOnBeHitBack(float DX, float DY, float DZ, float MoveSpeed, const FString& ActionID, float ActionBeginTime, int32 CasterID);

	/**
	*Define method
	* BlueprintCallable,客户端控制的结束击退
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_ControlledEndHitBack(int32 CasterID, const FString& HitBackActionId, const FString& GetUpActionId);

	/**
	*Define method
	*BlueprintNativeEvent,狂暴效果
	*
	*@param TargetID	目标ID
	*@param vector_r	4维向量R值
	*@param vector_g	4维向量G值
	*@param vector_b    4维向量B值
	*@param vector_a	4维向量A值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnRage(int32 TargetID, float vector_r, float vector_g, float vector_b, float vector_a);

	/**
	*Define method
	*BlueprintNativeEvent,结束狂暴
	*
	*@param TargetID	目标ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void EndRage(int32 TargetID);

	/**
	*Define method
	*BlueprintNativeEvent,溶解效果
	*
	*@param TargetID	目标ID
	*@param DissolveColor	消融的边缘颜色
	*@param DissolveDirection    消融的方向
	*@param StarDissolveDegree	开始消融的程度
	*@param EndDissolveDegree	需要到到达消融的程度
	*@param DissolveTime	消融时间
	*@param StartDelayTime	消融开始延迟时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnDissolve(int32 TargetID, const FString& DissolveColor, const FString& DissolveDirection,float StarDissolveDegree, float EndDissolveDegree, float DissolveTime, float StartDelayTime);

	/**
	*Define method
	*BlueprintNativeEvent,溶解效果
	*
	*@param TargetID	目标ID
	*@param StarDissolveDegree	开始消融的程度
	*@param EndDissolveDegree	需要到到达消融的程度
	*@param DissolveTime	恢复时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void EndDissolve(int32 TargetID, float StarDissolveDegree, float EndDissolveDegree, float DissolveTime);

	/**
	*Define method
	* BlueprintCallable,拉扯表现
	*
	*@param DX	位移X坐标
	*@param DY	位移Y坐标
	*@param DZ	位移Z坐标
	*@param MoveSpeed 速度
	*@param ActionID 动作ID
	*@param ActionBeginTime 动作起始时间
	*@param CasterID   施法者ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnPull(float DX, float DY, float DZ, float MoveSpeed, const FString& ActionID, float ActionBeginTime, int32 CasterID);
	void PullRole(GameObject* BeAtkEntity, AServerCharacter* BeAtkActor, float MoveSpeed, int32 CasterID, FVector Dest);
	void PullMonster(GameObject* BeAtkEntity, AServerCharacter* BeAtkActor, float MoveSpeed, int32 CasterID, FVector Dest);

	/**
	* Define method
	* BlueprintCallable,结束拉扯
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void EndPull(int32 CasterID);

	/**
	* Define method
	* BlueprintCallable,冲锋移动表现
	*
	*@param X	X坐标
	*@param Y	Y坐标
	*@param Z	Z坐标
	*@param MoveSpeed  击退速度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnChargeToPosition(float X, float Y, float Z, float MoveSpeed);

	/**
	* Define method
	* BlueprintCallable,结束冲锋移动表现
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void onEndChargeToPosition();

	/**
	*BlueprintCallable,更改攻击状态
	*
	*@param AttackState 攻击状态
	*
	*@return bool 更改攻击状态成功返回TRUE，否则返回FALSE。
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool ChangeAttackState(EATTACT_STATE AttackState);

	/**
	*Define method
	*BlueprintCallable,设置动画播放速率
	*
	*@param RateScale 播放速率
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void SetAnimRateScale(float RateScale);

	/**
	*Define method
	* BlueprintCallable,受击状态改变
	*
	*@param actionSpeed	动作迟缓速率
	*@param actionTime	动作迟缓时间
	*@param hitSlowTime 打击迟缓时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void StartSkillHitSlow(float actionSpeed, float actionTime, float hitSlowTime);

	/**
	* Define method
	* BlueprintCallable,受击状态改变
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void StopSkillHitSlow();

	/**
	*BlueprintCallable,取消施法辅助
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool CancelSkillAssistUi();

	/**
	*Define method
	*BlueprintCallable，吟唱表现
	*
	*@param intonateTime 技能Buff吟唱总时间
	*@param intonateName 技能BUff名称
	*@param iconName 图标字符串
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void intonateSpell(float intonateTime, const int32& SkillID);

	/**
	*Define method
	*BlueprintCallable，吟唱结束
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void intonateSpellOver();

	/**
	* 界面吟唱表现蓝图实现
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void OnIntonateSpellBP(const float& intonateTime, const int32& SkillID, bool isSparSkill);

	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void OnIntonateSpellOverBP();

	/**
	*Define method
	*BlueprintCallable，怪物施放技能吟唱表现
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnShowIntonateBar(const int32 CasterID, const float HoldTime, const int32 SkillId);

	/**
	*Define method
	*BlueprintCallable，怪物施放技能吟唱结束
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnHideIntonateBar(const int32 CasterID);

	/**
	*Define method
	*BlueprintCallable，晶核吟唱表现，可手动中断
	*
	*@param intonateTime 技能Buff吟唱总时间
	*@param intonateName 技能BUff名称
	*@param iconName 图标字符串
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void intonateSparSpell(float intonateTime, const int32& SkillID);

	/**
	*Define method
	*BlueprintCallable，吟唱结束
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void intonateSparSpellOver();

	/**
	*BlueprintPure,移动类型发生改变触发移动技能事件(技能事件)
	*
	*@param NewMOveType	新的移动类型
	*@param OldMovetype 旧的移动类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void OnMoveTypeChange(CS3_MOVE_TYPE NewMOveType, CS3_MOVE_TYPE OldMovetype);

	/**
	*BlueprintCallable，调用服务器方法，移动改变时触发技能事件
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void OnPlayerMoveChange(int32 MoveType, int32 MoveState);

	/**
	*Define method
	*BlueprintCallable，开始子弹Buff效果
	*
	*@param EffectID 光效ID
	*param EffectSendAngle 发射夹角
	*@param CasterID 施法者ID
	*@param ProxyID  客户端验证ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnBuffBulletBegin(const FString& EffectID, const float EffectSendAngle, const int32 CasterID, const int32 BuffIndex, const int32 ProxyID, const int32 EffectCustomIndex);

	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnBuffBulletEnd(const int32 BuffIndex, const int32 EffectCustomIndex);

	/**
	*Define method
	*BlueprintCallable，开始子弹Buff效果
	*
	*@param EffectList 光效ID列表
	*param EffectSendAngleList 发射夹角列表，顺序对应 "光效ID列表"
	*@param CasterID 施法者ID
	*@param ProxyID  客户端验证ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnBuffBulletMultipleBegin(const FString& EffectID, const float EffectSendAngle, const int32 EffectIndex, const int32 CasterID, const int32 BuffIndex, const int32 ProxyID);

	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnBuffBulletMultipleEnd(const int32 BuffIndex, const FString& EffectID, const int32 EffectIndex);

	void CreateDataFromStream(TMap<int32, FBuffData>& Buffs, const FVariant& val);

	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void OnRep_isInPending();

	void Set_attrBuffsForClient(const  KBEngine::FVariantArray& newVal, const  KBEngine::FVariantArray& oldVal);

	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void OnRefreshBuffBP(FBuffUIData BuffUIData);

	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		TArray<FBuffUIData> GetEntityBuffUIData(const int32 OtherPlayID);

	/**
	*Define method
	*BlueprintCallable，变回原来模型透明度 (临时)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void ChangeToNormalModelVisible();

	/**
	*Define method
	*BlueprintCallable,击飞空中
	*
	*@param actionIndex 动作标识号
	*@param actionID 击飞空中动作
	*@param BeginTime 动作起始时间
	*@param hitTime   击飞空中时间
	*@param speed	 击飞空中速度 m/s
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnRiseBegin(const int32& ContinuousId, const TArray<FString>& ActionID, const TArray<FString>& BeginTime,
			const float& hitTime, const float& speed);

	/**
	*Define method
	*BlueprintCallable,击飞结束
	*
	*@param actionIndex 动作标识号
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnRiseEnd(const int32& actionIndex);

	/**
	*Define method
	*BlueprintCallable，开始炼化晶石表现
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void PlayArtificeSpar(const FString& PreActionID, const FString& CycleActionID_);

	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void OnPlayArtificeSpar(ACharacter* Character, FACTION_DATA InActionData);

	/**
	*Define method
	*BlueprintCallable，设置要抓的目标
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void SetCatchTargetId(const int32& CatchTargetId);

	UFUNCTION(BlueprintPure, Category = "SkillInterface")
		const int32& GetCatchTargetId();

	/**
	*Define method
	*BlueprintCallable，结束炼化晶石表现
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void StopArtificeSpar(const FString& PostActionID);

	/**
	*Define method
	*BlueprintCallable，闪现
	*
	*@param position 目标位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void TeleportToDstPosition(FVector& position);

	virtual void InitBlueCB() override;

	void CloseUpForce();

	void HomingLookAtTarget(AActor*AtkTarget, AActor* BeTarget);

	void UsePositionItem(FString UID, int32 SkillId);

	void UsePositionItemExt(FString UID, int32 SkillId);
	/**
	*Define method
	*BlueprintNativeEvent，Buff额外数据显示
	*
	*@param buffIndex buff索引
	*@param jsonData json数据 key不固定，可从配置表:客户端中文配置表了解
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void AddShowBuffExtraTips(const int32& buffIndex, const FString& jsonData);

	/**
	*BlueprintCallable，获得Buff数据额外显示
	*
	*@param buffIndex buff索引
	*
	*@return 无
	*/
	UFUNCTION(BlueprintPure, Category = "SkillInterface")
		FString GetBuffExtraTips(const int32& buffIndex, const FString& colorstr = TEXT("FFFFFFFF"));

	/**
	*Define method
	*BlueprintCallable，清除BUFF的时候移除Buff额外数据显示
	*
	*@param buffIndex buff索引
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void RemoveBuffExtraTips(const int32& buffIndex);


	/**
	* //开始透明效果
	*
	* @param enterTime	 透明淡入时间（秒，0代表"立刻"）
	* @param startTP	 开始透明度
	* @param endTP		 目标透明度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void StartTransparency(float enterTime, float startTP, float endTP);
	void VisibleShowTransparency();
	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void ShowTransparency(float enterTime, float startTP, float endTP);
	/**
	* //结束透明效果
	*
	* @param enterTime	透明淡出时间（秒，0代表"立刻"）
	* @param tstartTP   开始透明度
	* @param endTP		目标透明度
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void EndTransparency(float outTime, float endTP, float startTP);
	void VisibleStopTransparency();
	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void StopTransparency(float outTime, float endTP, float startTP);

	/**
	* // 开始隐身
	*
	* @param enterTime	 透明淡入时间（秒，0代表"立刻"）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void StartHideCharacter(float enterTime);
	void VisibleHideCharacter(float endTP);

	/**
	* // 结束隐身
	*
	* @param outTime	透明淡出时间（秒，0代表"立刻"）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void EndHideCharacter(float outTime);
	void VisibleShowCharacter(float startTP);
	
	/**
	* //显示额外技能栏(CST-3542)
	*
	* @param SkillIDStr		FString
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void ShowBuffExtraSkillBar(const FString&  SkillIDStr);

	//移除额外技能栏
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CloseBuffExtraSkillBar();


	/**
	* //显示额外法宝技能栏(CST-4153)
	*
	* @param SkillIDStr		FString
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void ShowBuffExtraFaBaoSkillBar(const FString&  SkillIDStr);

	//移除额外法宝技能栏
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CloseBuffExtraFaBaoSkillBar();

	/**
	*Define method
	* 屏幕螺旋扭曲
	*
	*@param fDistortMask 旋转角度
	*@param fDistortMask 遮罩大小
	*@param fStartTimeDistort 开始总计时
	*@param fRecoveryTimeDistort 结束总计时
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void LXDistortScene(float fDitortAngle, float fDistortMask, float fStartTimeDistort, float fRecoveryTimeDistort, float HoldTimer);

	/**
	*Define method
	*BlueprintCallable，抓住俘虏
	*
	*@param DesEntityID 俘虏id
	*@param Slot 插槽名字
	*@param Position 插槽偏移位置
	*@param direction 插槽偏移方向
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void BeCapture(const int32& SourceEntityID, const int32& DesEntityID, const FString& Slot, const FVector &Position, const FVector &direction);
	/**
	*Define method
	*BlueprintCallable，释放俘虏
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void BeReleased(const int32& SourceEntityID);

	/**
	*Define method
	*BlueprintNativeEvent，替换技能快捷栏
	*
	*@param jsonData 技能栏数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void ReplaceSkillBar(const FString& jsonData);

	/**
	*Define method
	*BlueprintNativeEvent，替换技能快捷栏
	*
	*@param jsonData 技能栏数据
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void AddReplaceSkillBar(const FString& jsonData);

	/**
	*Define method
	*BlueprintNativeEvent，刷新替换技能快捷栏
	*
	*@param index 技能栏index
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void RefreshReplaceSkillBar(const int32& index);

	/**
	*Define method
	*BlueprintNativeEvent，替换技能快捷栏结束
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnReplaceSkillBarEnd();
	/**
	*Define method
	*BlueprintNativeEvent，技能转向
	*
	*@param Yaw 旋转方向
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void SkillTurnToPos(const FVector& Position);

	/**
	*BlueprintCallable,请求服务器中断BUFF
	*
	*@param buffIndex Buff索引
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void RequestInitiaiveStopBuffEvent(const FString& buffIndex);

	////<检查主动技能使用基础条件
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool CheckSkillUseCondition(int32 SkillID);

	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool CheckAutoUseSkill(int32 SkillID, int32 TargetID, bool BShowMsg = true);////<客户端获取当前是否能释放技能

	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool CheckAutoUseItem(int32 ItemID);////<客户端获取当前是否能使用物品
	/**
	*BlueprintCallable,请求服务器中断SKILL
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool RequestInitiaiveStopSkillEvent();

	/**
	*Define method
	*BlueprintNativeEvent 上载具
	*
	*@param modelID 载具ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnMountCarrier(const FString& modelID);

	/**
	*Define method
	*BlueprintNativeEvent 下载具
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnDisMountCarrier();

	/**
	*Define method
	*BlueprintNativeEvent 开始遁地效果
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_StartSubmerge(const FString& EffectID);

	/**
	*Define method
	*BlueprintNativeEvent 结束遁地效果
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_EndSubmerge();
	/**
	*Define method
	*BlueprintNativeEvent 开始迷雾效果
	*@param Albedo			  迷雾颜色Vctor
	*@param ExtinctionMulity  整个体积雾的雾气浓度系数
	*@param HoleRadius   	  体积雾内部遮罩的半径
	*@param InsideExtinction  遮罩内部雾气浓度
	*@param OutsideExtinction 遮罩外部雾气浓度
	*@param EnterTime		  渐变时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_StartFog(const int32& TargetID, const FString& Albedo, const FString& ExtinctionMulity, const FString& HoleRadius, const FString& InsideExtinction, const FString& OutsideExtinction , const float& EnterTime);

	/**
	*Define method
	*BlueprintNativeEvent 以当前摄像机距离半径旋转摄像机
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_RotateCamera(const FString& Rotaitones, const float& ArmLength);

	/**
	*Define method
	*BlueprintNativeEvent 结束迷雾效果
	*@param OutTime		淡出时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_EndFog();
	/**
	*Define method
	*BlueprintNativeEvent 冻结
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void Frozee();
	void StartFrozee();

	/**
	*Define method
	*BlueprintNativeEvent 解冻
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void Unfreeze();

	/**
	*Define method
	*BlueprintNativeEvent 开始自动上升
	*@param FeiShengUpSpeed			上升速度(单位:米/秒)
	*@param FeiShengRightSpeed		左右移动速度（单位:米/秒）
	*@param FeiShengCameraLength	摄像机与玩家距离（单位:米）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_AutoRise( const float& UpSpeed, 
			const float& RightSpeed, const float& CameraLength);

	/**
	*Define method
	*BlueprintNativeEvent 停止上升
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_StopRise();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnChasePlayerFinish();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_stopRefineSpar();

	/**
	* BlueprintCallable，通过使用技能请求切换心法
	*
	* @param SkilID 心法技能ID
	*
	* @return true:是请求，false:请求不通过
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool ChangePosture(int32 SkilID);

	UFUNCTION(BlueprintImplementableEvent, Category = "SkillInterface")
		void OnRep_skillPosture();///<心法切换回调，蓝图实现

	/**
	*
	*设置正在使用对位置施法的物品UID （仅在通知服务器释放技能前有数据） 用来做一些特殊需求 详情JIRACST-6736
	*
	*@return 无
	*/
	void SetCurrentUsePosItemUID(FString itemUID);

	/**
	*Define method
	*BlueprintNativeEvent 玩家首次学习技能通知（新手技能指引）
	*@param SkilID 技能ID
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_FirstLearnSkillNotify(const int32& SkillID);

	/**
	*Define method
	*BlueprintNativeEvent 玩家追击目标
	*@param SkilID 技能ID
	*@param TargetID 目标ID
	*@param Distance 保持距离
	*@param Speed 速度
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_RoleChaseEntity(const int32& SkillID, const int32& TargetID, const float& Distance, const float& Speed);
	
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnAddEventChangMoveType(CS3_MOVE_TYPE NewMoveType, CS3_MOVE_TYPE OldMoveType);

	/**
	*Define method
	*BlueprintNativeEvent 玩家追击技能结束
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_RoleChaseEntityEnd();
	
	/**
	*BlueprintCallable 玩家追击完毕
	*@param SkilID 技能ID
	*@param isSuccess 是否追击成功
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_OnRoleChaseEntityOver(const int32& SkillID, const int32& isSuccess);

	/**
	*Define method
	*BlueprintNativeEvent 玩家冲锋到某位置
	*@param Position 目标位置
	*@param Speed 速度
	*
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_RoleChargePosition(const FVector &Position, const float& Speed);

	// ==========================五行画卷副本相关接口=======================================================
	/**
	*Define method
	*BlueprintNativeEvent,五行怪物分身进入画卷通知
	*
	*@param AttributeType 五行画卷属性类型（0:金，1:木，2:水，3:火，4:土）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_OnMonsterCopyEnterPicture(const int32& AttributeType);

	/**
	*Define method
	*BlueprintNativeEvent,光球击中画卷通知
	*
	*@param ResultType 0:击中空白画卷，1:击中正确的画卷，2:击中错误的画卷
	*@param AttributeType 五行画卷属性类型（0:金，1:木，2:水，3:火，4:土）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_OnBulletHitPicture(const int32& ResultType, const int32& AttributeType);

	/**
	*Define method
	*BlueprintNativeEvent,击中空白画卷，怪物从空白画卷中出来时通知画卷停止闪烁
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_OnPictureStopHighlight();

	/**
	*Define method
	*BlueprintNativeEvent,骑上坐骑
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		void CLIENT_OnMountSlide(const float& DelayTime, const float& SpeedScale, const float& ASpeed, const FString& ModelID, const float& InputYawScale, const int32& IsNewBuff);
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void OnMountSlideFinishRideOnModel();
	/**
	*Define method
	*BlueprintNativeEvent,下坐骑
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_OnDismountSlide();

	/**
	*Define method
	* 镜头俯瞰
	*
	*@param CameraLoaction 摄像机位置基于玩家位置+当前偏移量
	*@param CameraLoaction 摄像机旋转基于玩家位置+当前偏移量
	*@param StartTime 开始时间
	*@param LoopTime 持续时间
	*@param EndTime 结束时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void StartOverLookScene(const FString& CameraLoaction,const FString& CameraRotation, float StartTime, float LoopTime, float EndTime);

	/**
	*Define method
	* 结束镜头俯瞰
	*
	*@param EndTime 结束时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void EndOverLookScene(float EndTime);

	/**
	*Define method
	* 进入黑暗(玩家看不见)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void EnterDark();

	/**
	*Define method
	* 离开黑暗
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void LeaveDark();

	/**
	*Define method
	* 照明一定范围
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_TurnOnLight(const float& lightRange);

	/**
	*Define method
	* 取消照明
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_TurnOffLight();

	/**
	*Define method
	* 停止飞行
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_StopFlyPatrol(const FString&  FlyPatrolID);
	/**
	*Define method
	*BlueprintCallable,初始化被动技能栏
	*
	*@param val
	*
	*@return 无
	*/
	void InitPassiveSkillBar(const FVariant& datas);

	/**
	*Define method
	*BlueprintCallable,更新被动技能栏栏位
	*
	*@param val
	*
	*@return 无
	*/
	void updatePassiveSkillBar(const FVariant& data);

	/**
	*BlueprintImplementableEvent 更新被动技能栏栏位
	*@param index 栏位id
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|RPC")
		void BP_updatePassiveSkillBar(int32 index);

	/**
	*BlueprintCallable 解锁被动技能栏栏位
	*@param index 栏位id
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
	void RPC_requestUnlockPassiveSkillBar(int32 index);

	/**
	*BlueprintCallable 取消被动技能栏上被动技能放置
	*@param index 栏位id
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestCancelUnActivatePassiveSkill(int32 index);

	/**
	* BlueprintCallable，判断是否能解锁被动技能栏栏位
	*
	* @param index 栏位ID
	*
	* @return true:能，false:不能
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool IsCanUnlockPassiveSkillBar(int32 index);

	/**
	*BlueprintCallable 激活被动技能
	*@param skillID 
	*@param index 栏位id
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
	void RPC_requestActivatePassiveSkill(int32 skillID, int32 index);

	/**
	* BlueprintCallable，根据栏位ID获取栏位数据
	*
	* @param id 栏位ID
	*
	* @return true:
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
	void GetPassiveSkillBarData(int32 id, uint8& isLock, int32& skillID);

	/**
	* BlueprintCallable，根据技能ID是否已激活
	*
	* @param SkillID 技能ID
	*
	* @return 是否已激活
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillInterface")
		bool CheckPassiveSkillActiveSate(int32 SkillID);

	/**
	*Define method
	*BlueprintNativeEvent 技能受迫跳跃
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_ForcedJump(float Height);

	/**
	*Define method
	*BlueprintNativeEvent 玩家踩上石头
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_OnMountStone(const int32& EntityID_, const int32& BBegin);
	/**
	*Define method
	*BlueprintNativeEvent 玩家取消踩上石头
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "SkillInterface")
		void CLIENT_OnDisMountStone(const int32& EntityID_);

	//开始技能进阶
	void IntensifySkill(const int32& QuickID, const int32& PassiveSkillLevel, const int32& SkillLevel);
	//取消技能进阶
	void CancelIntensifySkill(const int32& QuickID, const int32& PassiveSkillLevel, const int32& SkillLevel);

	/**
	*BlueprintCallable 添加飞行路径持有效果
	*@param FlyPatrolID 飞行路径ID
	*@param HoldEffectList 是持有效果ID列表
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_AddFlyPatrolEffectList(const FString& FlyPatrolID, const TArray<int32>& HoldEffectList);
	/**
	*BlueprintCallable 移除飞行路径持有
	*@param FlyPatrolID 飞行路径ID
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RemoveFlyPatrolEffectList(const FString& FlyPatrolID);

	FORCEINLINE bool CanTransparency() { return BTranAnamorphism; }

	// 生成entity移动轨迹（毒雾）
	void OnCreateTrace(const int32& EntityID_, const FString& EffectID, const float& DrawDist, const float& LifeTime, const int32& Width, const int32& Hight, const int32& SkillID);
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|RPC")
		void OnCreateSelfTraceBP(const FString& EffectID, const float& DrawDist, const float& LifeTime, const int32& Width, const int32& Hight, const int32& SkillID);
	void OnFinishCreateTrace(const int32& EntityID_);
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|RPC")
		void OnFinishCreateSelfTraceBP();
	///进入中毒表现
	void EnterToxicosis();
	///离开中毒表现
	void LeaveToxicosis();

public:
	UPROPERTY(BlueprintReadOnly, Category = "SkillInterface")
		int32 isInPending;
	UPROPERTY(BlueprintReadOnly, Category = "SkillInterface")
		TArray<int32> BuffExtraSkillIDs;	///buff额外技能ID列表
	UPROPERTY(BlueprintReadOnly, Category = "SkillInterface")
		TArray<int32> BuffExtraFaBaoSkillIDs;	///buff额外法宝技能ID列表
	///<技能心法:0（无心法）101、102（战士）201、202（剑客）301、302（射手）401、402（法师）
	UPROPERTY(BlueprintReadOnly, Category = "SkillInterface")
		int32 skillPosture;
	UPROPERTY(BlueprintReadWrite, Category = "SkillInterface")
		float MoveScale;
	UPROPERTY(BlueprintReadOnly, Category = "SkillInterface")
		float AccelerateSpeed;
	UPROPERTY(BlueprintReadWrite, Category = "SkillInterface")
		FRotator DstRotation;
	UPROPERTY(BlueprintReadOnly, Category = "SkillInterface")
		bool BTranAnamorphism;

	// 由于策划还没决定使用那种滑雪效果,所以这里用开关区分 CST-9039 CST-8358
	// 策划确定后可以删除开关
	UPROPERTY(BlueprintReadOnly, Category = "SkillInterface|Skiing")
		bool IsNewSkiBuff = false;
private:
	UPROPERTY()
		int32 CastingSkill;

	UPROPERTY()
		int32 m_CatchTargetID;

	/*UPROPERTY()
		UAtkStateCtrl* AtkStateCtrl;///<战斗状态控制*/
	UPROPERTY()
		UFightAssist* FightAssist;///<技能施法辅助

	UPROPERTY()
		TMap<int32, UHoldEffectData*> HoldEffectDatas;///持有效果光效、动作
	UPROPERTY()
		TMap<int32, UCS3AudioComponent*> AudioComponents;///声音组件

	UPROPERTY()
		TMap<int32, UCS3AudioComponent*> TargetAudioComponents;///技能目标声音组件

	TMap<int32, TMap<int32, int32>> BuffBulletEffectUID;///子弹buff光效（BuffBullet）

	UPROPERTY()
		TMap<int32, FBUFF_BULLET_EFFECT_MUTIPLE_DATA> BuffBulletEffectsMultiple;///子弹buff光效，一个对应多个光效

	UPROPERTY()
		TMap<int32, int32> BuffLinkEffectUID;///连线buff光效

	UPROPERTY()
		TArray<int32> SkillEffectUIDList;///技能施展光效

	UPROPERTY()
		TArray<int32> BuffUIDList;///遁地Buff光效

	UPROPERTY()
		FName CycleActionID;

	UPROPERTY()
		TMap<int32, FString> BuffExtraData; ///buff额外显示的数据

	FUseSkillForTargetDelegate UseSkillForTargetDelegate;

	EMovementMode m_BeforUpForceMoveMode;///<开始击飞前的模式
	FTimerHandle m_UpForceHandle;///<击飞计时
	FTimerHandle m_LookAtHandle;///<朝向句柄

	FTimerHandle m_DissolveHandle;///溶解定时器
	FTimerHandle m_DiedDissolveHandle;///死亡消融定时器
	float DissolveTimer;///溶解定时器
	float DiedDissolveTimer;///死亡消融定时器增量
	UPROPERTY()
		TArray<UMeshComponent*> CopyMeshList;///<复制的骨骼列表

	UPROPERTY()
		TArray<UMeshComponent*> BeCopyMeshList;///<被复制的骨骼列表
	UPROPERTY()
		FString CurrentUsePosItemUID; ///<仅在通知服务器释放技能前有数据

	TMap<int32, FPASSIVE_SKILL_BAR_DATA> passiveSkillBarData; //玩家被动技能栏数据

private:
	FTimerHandle delayDestroy;
	FTimerHandle Submerge;

	int32 CameraHandle;
	FTimerHandle DelayMove;

	int32 CacheSkillID;
	float CacheMaxWalkSpeed;
	float CacheMaxAcceleration;
	FTimerHandle RoleChaseEntityHandle;

	TArray<float> TempFValue;
	float TempChangeTime;
	TMap<int32, BuffDataType> AttrBuffs;
	TMap<int32, BuffDataType> AttrClientBuffs;

	FTimerHandle FindCharacterHandle;
	int32 FindCharacterTime;
	FDelegateHandle FrozeeDelegateHandle;
};
