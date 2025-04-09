// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Animation/AnimInstance.h"
#include "GameFramework/Character.h"
//数据
#include "GameData/CharacterData.h"
#include "BaseAnimInstance.generated.h"
/*
* 文件名称：BaseAnimInstance.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-02-07
*/

class AGameCharacter; 
DECLARE_MULTICAST_DELEGATE_TwoParams(FActionOverDelegate, ACharacter *, FACTION_DATA);///单个动作播放完毕[对象，动作]
DECLARE_MULTICAST_DELEGATE_TwoParams(FActionContinuousOverDelegate, ACharacter *, int32);///连续动作播放完毕[对象]
DECLARE_MULTICAST_DELEGATE_TwoParams(FActionBlendOutDelegate, ACharacter *, FACTION_DATA);///蒙太奇混出完毕[对象，动作]
DECLARE_MULTICAST_DELEGATE_OneParam(FActionReadyChangeDelegate, FACTION_DATA);///当前动作准备改变时
DECLARE_MULTICAST_DELEGATE_OneParam(FActionChangeFinishDelegate, FACTION_DATA);///当前动作改变完成时
DECLARE_MULTICAST_DELEGATE_OneParam(FActionPlayNewDelegate, FACTION_DATA);///新动作播放通知，只用于通知骑乘上面的玩家复制品播放动作

DECLARE_STATS_GROUP(TEXT("UBaseAnimInstance"), STATGROUP_UBaseAnimInstance, STATCAT_Advanced);

UCLASS(Blueprintable, hideCategories = BaseAnimInstance, BlueprintType, meta = (BlueprintThreadSafe), Within = SkeletalMeshComponent)
class CHUANGSHI_API UBaseAnimInstance : public UAnimInstance
{
	GENERATED_BODY()
public:
	UBaseAnimInstance();
	~UBaseAnimInstance();

	/*----------------动作播放核心功能-------------------------------*/
	virtual void BeginDestroy() override;
	void ClearData();
	void PostInitProperties() override;
	void NativeInitializeAnimation() override;
	void NativeUpdateAnimation(float DeltaSeconds) override;
	void NativeUninitializeAnimation() override;
	/**
	*播放动作
	*
	*@param InActionId 动作id
	*@param InStartPostion 动画起始时间
	*@param InActionOverDelegate 播放完毕回调函数
	*@param InContinuousId 连续动作ID
	*
	*@return 无
	*/
	virtual void PlayAction(FName InActionId, float InStartPostion = 0.0f,
		const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate(), 
		int32 InContinuousId = 0,
		const FActionBlendOutDelegate& InActionBlendOutDelegate = FActionBlendOutDelegate());

	/**
	*播放连续动作
	*
	*@param InContinuousAction 连续动作数据
	*@param InContinuousActionOverDelegate 播放完毕回调函数
	*
	*@return 无
	*/
	void PlayContinuousActions(FACTION_CONTINUOUS &InContinuousAction,
		const FActionContinuousOverDelegate& InContinuousActionOverDelegate = FActionContinuousOverDelegate());

	void StopAction();///停止角色当前动作
	void StopFrontAction();///停止当前播放的蒙太奇
	void StopActionById(FName ActionId);///停止指定的动作
	void StopActionByType(ACTION_TYPE_ENUM InActionType);///停止某种类动作
	void StopContinuousAction(int32 InContinuousId = 0);///停止连续动作

	UFUNCTION(BlueprintCallable, Category = "BaseAnimInstance")
		void PlayOverCurActionCallBack();///状态机中切换状态完成回调

	/*----------------动作常用表现接口-------------------------------*/
	///检查使用普通待机or战斗待机
	void PlayStandbyAction();
	///播放移动动作
	void PlayMoveAction();
	///播放死亡动作
	void PlayDeadAction(const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate());
	///播放复活动作
	void PlayRebornAction();
	///播放晕动作
	void PlayDizzyAction();
	///播放睡动作
	void PlaySleepAction();
	///播放随机动作
	void PlayRandomAction(FName ActionId);
	///播放收刀动作
	virtual void PlayShouDaoAction(const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate()) {};
	///播放拔刀动作
	virtual void PlayBaDaoAction(const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate()) {};
	///播放着陆动作
	void PlayFallLandAction();
	///播放空中下落动作
	void PlayFallingAction();
	///播放攀爬动作
	virtual void PlayClimbLadderAction() {};
	
	/*----------------常用数据、状态获取-------------------------------*/
	///根据ID获取动画蓝图中现拥有的动作数据
	FACTION_DATA GetActionDataById(FName ActionId);
	///获取当前正在播放的动作数据
	FACTION_DATA GetCurPlayActionData();
	///获取当前正在播放的连续动作数据
	FACTION_CONTINUOUS GetCurPlayContinuousActionData();
	///分别获取前、背景动作数据
	void GetFronAndBackAction(FString& BackActionId, FString& FrontActionId);
	///是否处于待机状态
	bool IsStandByState();
	///刷新数据
	void RefreshData();

protected:
	///停止角色背景动作
	void StopBackAction();

	///动作分类执行表现
	void StarPlayAction(FACTION_DATA& InActionData);
	///检查新动作是否能播放[数据有效性、优先级]
	bool CheckCanPlayNewAction(FName InActionId, FACTION_DATA& ActionData, bool& IsBreakFront);
	///检测动作数据是否有效
	bool CheckActionDataValid(FACTION_DATA& InActionData);
	///检测优先级
	bool CheckActionPriority(FACTION_DATA& InActionData, bool &IsBreakFront);

	///获取Pose对应动作数据
	UFUNCTION(BlueprintPure,  Category = "BaseAnimInstance")
		FACTION_DATA GetActionData(ACTION_POSE_ENUM InActionPose);
	///获取分层混合半身融合的类型（0是不融合，1是半身融合，2脸部融合）
	UFUNCTION(BlueprintPure, Category = "BaseAnimInstance")
		int32 GetBlendBoneNameIndex();

	///是否死亡
	UFUNCTION(BlueprintPure, Category = "BaseAnimInstance")
		bool IsDead();

	UFUNCTION(BlueprintNativeEvent, Category = "BaseAnimInstance")
		void MontageStartEvent(UAnimMontage* MontageToPlay);
	UFUNCTION(BlueprintNativeEvent, Category = "BaseAnimInstance")
		void MontageEndEvent(UAnimMontage* MontageToPlay, bool bInterrupted);
	UFUNCTION(BlueprintNativeEvent, Category = "BaseAnimInstance")
		void MontageBlendOutEvent(UAnimMontage* MontageToPlay, bool bInterrupted);

	virtual bool IsInWater() { return false; };///是否在水中
	virtual void UpdateMoveSpeed();///更新匹配动作速度
	virtual void UpdateMoveDirection();///更新匹配动作方向
	virtual FName GetMontageSectionId(FACTION_DATA& InActionData);///获取蒙太奇片段ID

	void PlayPoseBackAction(ACTION_POSE_ENUM ActionPoseType, const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate());
	void PlayPoseFrontAction(ACTION_POSE_ENUM ActionPoseType, const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate());

private:
	void BroadcastActionReadyChange(FACTION_DATA& InActionData);///广播动作打断(链刃职业打当正在播放的动作时，要通知武器动作也要停止)
	void CallBackForActionOver(FACTION_DATA InActionData);///动作播完广播回调
	void CallBackForActionBlendOut(FACTION_DATA InActionData);///动作播完广播回调

	void CheckActionPause(FACTION_DATA &InActionData);///检查需暂停的动作[不支持蒙太奇类型]
	void CheckChangeBackAction(FACTION_DATA &InActionData);///播放前景动作时，检测绑定的背景动作
	void CheckChangeFrontAction(FACTION_DATA &InActionData);///播放背景动作时，检测绑定的前景动作
	void UpdateActionPauseTime(float DeltaSeconds);///更新暂停动作的时候
	void ClearPauseAction();///清理正在表现暂停功能检测的前景动作

	void StartPlayBackAction(FACTION_DATA &InActionData);///播放背景动作

	void PlayInitStandByAction(FName ActionId);///播放出生时的动作
	void PlayNormalStandbyAction();///播放普通待机动作
	void PlayFightStandbyAction();///播放战斗待机动作
	bool PlayEffectStateBackAction();///检查播放效果状态背景动作
	void PlayNormalMoveAction();///播放普通移动动作
	void PlayFightMoveAction();///播放战斗移动动作
	void PlayWaterMoveAction();///播放水中移动动作

	void CheckNextContinuousAction();///检测下一个连续动作
	void RemoveConutinuousActionDatas(int32 InContinuousId);///删除连续动作播放数据
	void OnActionOverForContinuous(ACharacter* Character, FACTION_DATA InActionData);///连续动作播放时单个动作播放完毕回调函数
	bool IsContinuousPlaying();///是否连续动作播放中

	//void SetAssetRootMotion(FACTION_DATA& InActionData);
	FName GetSlotNameByIndex(int32 Index);

public:
	///当前动作准备改变时
	FActionReadyChangeDelegate OnActionReadyChange;
	///当前动作发生改变并成功改变时
	FActionChangeFinishDelegate OnActionChangeFinish;
	///新动作请求播放
	FActionPlayNewDelegate OnPlayNewAction;

protected:
	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		AGameCharacter* CurCharacter;///当前角色

	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		FACTION_DATA BeforBackActionData;///上一次的背景动作数据

	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		FACTION_DATA CurBackActionData;///当前的背景动作数据

	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		FACTION_DATA BeforFrontActionData;///上一次的前景动作数据 

	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		FACTION_DATA CurFrontActionData;///当前的前景动作数据

	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		float CurMoveSpeed;///当前的移动速度(取值为0-6)

	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		float CurMoveDirection;///当前的方向

	//==========瞄准射击相关========
	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		FACTION_DATA AimOffsetActionData;///上、中、下瞄准偏移动作数据

	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		bool IsAimOffsetBlend = false;///是否上、中、下瞄准偏移融合模式
	//==========瞄准射击相关========

	//==========攀爬梯子相关========
	UPROPERTY(BlueprintReadOnly, Category = "BaseAnimInstance")
		float ClimbLadderActionFramePos;///攀爬梯子loop动作计算动作时间轴点位置
	bool IsClimbLaddering;///是否攀爬过程中
	//==========攀爬梯子相关========

	TMap<int32, FActionOverDelegate> ActionOverDelegateMap;
	TMap<int32, FActionBlendOutDelegate> ActionBlendOutDelegateMap;

	int32 ActionDynamicId;///动作动态id记载

	bool bTickUpdate;///tick开关

private:
	FTimerHandle ActionPauseDelayHandle;///暂停在最后一帧的定时器
	FACTION_PAUSE_DATA CurActionPauseData;///当前暂停的动作数据
	FACTION_DATA SaveCurBackActionData;///同背景播放时,缓存当前的背景动作数据
	FACTION_DATA SaveCurFrontActionData;///播放背景时,缓存播放的前景动作数据

	FTimerHandle FilterStateDelayHandle;///动作过器
	FTimerHandle FilterSaveStateDelayHandle;///过渡缓存状态定时器
	ACTION_GROUND_TYPE_ENUM CurGroundType;///当前播放的动作类型(前景or背景)
	bool IsCompelBreak;///是否强制中断

	FACTION_CONTINUOUS CurContinuousAction;///当前连续动作数据
	TMap<int32, FActionContinuousOverDelegate> ContinuousActionOverMap;///连续播放动作结束回调事件map集合

	bool IsPlayerControll;///仅供调试方便
	int32 EntityId;///仅供调试方便
	bool IsOpenDebug = false;///仅供调试方便
};
