#pragma once

#include "KBEngine.h"
#include "Components/ActorComponent.h"
#include "FightComponent.generated.h"

/*
* 文件名称：FightComponent.h
* 功能说明：战斗组件
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-05-12
*/

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FFightComponentFightState);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FFightComponentCastSkill, FString, SkillName, bool, IsPromptSkillName);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams(FFightComponentReceiveSkill, int32, CasterID, int32, Damage, uint8, IsCritical, uint8, IsParry);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FFightComponentOnDodgeSkillHit, int32, CasterID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FFightComponentBeHitBack, int32, CasterID, FVector, Dest, float, MoveTime);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FFightComponentBeHitBackNew, int32, CasterID, FVector, Dest, float, MoveSpeed);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FFightComponentOnEndHitBack, int32, CasterID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FFightComponentCreateFightArea, FString, RowNunber, AREA_LIGHT_WALL_TYPE_ENUM, Current);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FFightComponentOnPull, int32, CasterID, FVector, Dest, float, MoveSpeed);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FFightComponentEndPull, int32, CasterID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FFightComponentBeCastSkill, FString, SkillName, bool, IsPromptSkillName, int32, TargetID);

/*
* 普通战斗组件类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UFightComponent : public UActorComponent
{
	GENERATED_BODY()
public:
	UFightComponent();///<构造函数
	virtual void BeginPlay() override;///<重写BeginPlay
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;///<重写EndPlay

	virtual void EnterFightState();///<进入战斗状态
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentFightState OnEnterFightState;///<进入战斗状态蓝图回调
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentFightState OnExitFightState;///<离开战斗状态蓝图回调
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentCreateFightArea OnCreateFightArea;///<蓝图生成战斗区域

	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentCastSkill OnCastSkill;///<释放技能蓝图回调
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentBeCastSkill OnBeCastSkill;///<对目标释放技能蓝图回调
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentReceiveSkill OnReceiveSkill;///<接受技能伤害蓝图回调
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentOnDodgeSkillHit onDodgeSkillHit;///<闪避技能打击蓝图回调
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentBeHitBackNew OnBeHitBackNew;///<新版怪物被击退蓝图回调
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentOnEndHitBack OnEndHitBack;///<怪物被击退结束蓝图回调
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentOnPull OnPull;///<怪物被拉扯蓝图回调
	UPROPERTY(BlueprintAssignable, Category = "FightComponent")
	FFightComponentEndPull EndPull;///<怪物被击退结束蓝图回调
};

/*
* 怪物战斗组件类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterFightComponent : public UFightComponent
{
	GENERATED_BODY()
public:
	UMonsterFightComponent();///<构造函数

};
