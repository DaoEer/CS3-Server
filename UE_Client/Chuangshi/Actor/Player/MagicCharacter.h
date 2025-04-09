// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "GameData/FaBaoData.h"
#include "SharedPointer.h"
#include "MagicCharacter.generated.h"



/**
 * 
 */

DECLARE_STATS_GROUP(TEXT("UAppearanceComponent"), STATGROUP_AMagicCharacter, STATCAT_Advanced);

UCLASS(BlueprintType)
class CHUANGSHI_API AMagicCharacter : public AGameCharacter
{
	GENERATED_BODY()

public:
	AMagicCharacter();
	virtual void OnCreateApperanceOver() override;

	UFUNCTION(BlueprintCallable, Category = "Game|Magic")
	void PlayActionAim(FName AimName);

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Magic")
	void DestroyFaBao();
		
	//使用法宝技能
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Magic")
	void UseSkill(AServerCharacter* TargetActor, AServerCharacter* PlayerActor, const FString& actionid, const FString& effectID, const FString& playtime);

	//使用莲花技能
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Magic")
	void UseLotusSkill();

	void Init(AServerCharacter* TargetActor,FString FaBaoRowName);//初始化数据

	UFUNCTION(BlueprintImplementableEvent, Category = "Game|Magic")
	void InitOver();//初始化完成回调

	void SetFaBaoData(const FFABAO_DATA* fabaodata);

	UFUNCTION(BlueprintCallable, Category = "Game|Magic")
	void GetFaBaoData(FFABAO_DATA& fabao);



private:
	const FFABAO_DATA* FaBaoData;

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent


};
