// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Manager/Delegate/PublicDelegateObject.h"
#include "EntityPropertyDelegateObject.generated.h"


DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnPropertyChangedEventEntityIDIntInt, int32, entityID, int32, val1, int32, val2);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPropertyChangedEventString, FString, val);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPropertyChangedEventInt, int32, val);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPropertyChangedEventStringInt, FString, strVal, int32, intVal);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPropertyChangedEventEntityIDInt, int32, val1, int32, val2);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnPrefixNameChange, int32, entityID, FString, newVal, FString, oldVal);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FCS3ExchangeGiftSuccesd);

/**
 * entity属性变动委托声明对象
 */
UCLASS()
class CHUANGSHI_API UEntityPropertyDelegateObject : public UPublicDelegateObject
{
	GENERATED_BODY()
public:
	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDIntInt OnHPChangedEvent;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDIntInt OnMPChangedEvent;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventString OnPlayerNameChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventStringInt OnProfessionChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDInt OnLevelChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDIntInt OnExpChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDInt OnCampChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDIntInt OnGangQiChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDInt OnGangQiStateChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDInt OnTempCampChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDInt OnJingJieLevelChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDIntInt OnGangQiProgressChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDInt OnCombatPowerChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDIntInt OnPlayerVitPointChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventEntityIDInt OnTitleChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnCorporeityChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnStrengthChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnIntellectChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnDexterityChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnDamageChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnMagicDamageChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnArmorChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnMagicArmorChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnCriticalstrikeChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnDiscernChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnParryChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnSpeedChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnHitrateChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnDodgerateChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnHealingrateChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnFeatsChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnPotentialChange;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnXiuweiChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnXiuweiLevelChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnCureChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnIceDamageChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnFireDamageChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnThunderDamageChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnXuanDamageChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnIceArmorChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnFireArmorChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnThunderArmorChanged;

	UPROPERTY(BlueprintAssignable, Category = "Property Changed|base")
		FOnPropertyChangedEventInt OnXuanArmorChanged;

	UPROPERTY(BlueprintAssignable, Category = "Login|Gift")
		FCS3ExchangeGiftSuccesd OnExchangeGiftSuccesd;
};
