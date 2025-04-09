// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Manager/Delegate/KitbagDelegateObject.h"
#include "GameData/Skill/QuickSkillData.h"
#include "QuickBarDelegateObject.generated.h"

/**
 * 快捷栏/技能 委托声明对象
 */

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUpdateQBItem, FQB_ITEM, QBItem);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRemoveQBItem, int32, Index);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUpdateMoreQBItem, FQB_ITEM, QBItem);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRemoveMoreQBItem, int32, Index);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAddShenTongSKill, int32, SkillID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRemoveShenTongSKill, int32, SkillID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdateShenTongSKill, int32, SkillID, int32, Times);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAddChuanChengSkill, int32, SkillID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRemoveChuanChengSkill, int32, SkillID);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUpdateChuanChengSkillBar, int32, Index);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnUpdateChaunChengExp, int32, SkillID, int32, Exp);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUnlockChuanChengSkillBar, int32, Index);

UCLASS()
class CHUANGSHI_API UQuickBarDelegateObject : public UKitbagDelegateObject
{
	GENERATED_BODY()
public:

#pragma region	/** 主快捷栏 */
	UPROPERTY(BlueprintAssignable, Category = "QuickBar|Main")
		FOnUpdateQBItem OnUpdateQBItemEvent;
	UPROPERTY(BlueprintAssignable, Category = "QuickBar|Main")
		FOnRemoveQBItem OnRemoveQBItemEvent;
#pragma endregion

#pragma region	/** 副快捷栏 */
	UPROPERTY(BlueprintAssignable, Category = "QuickBar|More")
		FOnUpdateMoreQBItem OnUpdateMoreQBItemEvent;
	UPROPERTY(BlueprintAssignable, Category = "QuickBar|More")
		FOnRemoveMoreQBItem OnRemoveMoreQBItemEvent;
#pragma endregion

#pragma region	/** 神通技能 */
	UPROPERTY(BlueprintAssignable, Category = "Skill|ShenTong")
		FOnAddShenTongSKill OnAddShenTongSKillEvent;
	UPROPERTY(BlueprintAssignable, Category = "Skill|ShenTong")
		FOnRemoveShenTongSKill OnRemoveShenTongSKillEvent;
	UPROPERTY(BlueprintAssignable, Category = "Skill|ShenTong")
		FOnUpdateShenTongSKill OnUpdateShenTongSKillEvent;
#pragma endregion

#pragma region	/** 传承技能 */
	UPROPERTY(BlueprintAssignable, Category = "Skill|ChuanCheng")
		FOnAddChuanChengSkill OnAddChuanChengSkillEvent;
	UPROPERTY(BlueprintAssignable, Category = "Skill|ChuanCheng")
		FOnRemoveChuanChengSkill OnRemoveChuanChengSkillEvent;
	UPROPERTY(BlueprintAssignable, Category = "Skill|ChuanCheng")
		FOnUpdateChuanChengSkillBar OnUpdateChuanChengSkillBarEvent;
	UPROPERTY(BlueprintAssignable, Category = "Skill|ChuanCheng")
		FOnUpdateChaunChengExp OnUpdateChaunChengExpEvent;
	UPROPERTY(BlueprintAssignable, Category = "Skill|ChuanCheng")
		FOnUnlockChuanChengSkillBar OnUnlockChuanChengSkillBarEvent;
#pragma endregion

};
