#pragma once
#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "../ServerCharacter.h"
#include "PetProxyCharacter.generated.h"

/*
* 文件名称：PetProxyCharacter.h
* 功能说明：用于界面上显示幻兽模型
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2020-4-26
*/


UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API APetProxyCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	APetProxyCharacter();///<构造函数
	virtual void BeginPlay()override;
	virtual void OnCreateModelOver() override;
	virtual void OnCreateApperanceOver() override;

public:
	//播放动作
	UFUNCTION(BlueprintCallable, Category = "PetProxyCharacter")
		void PlayAction_BP(FName ActionID);
	//动作播放完成
	UFUNCTION(BlueprintCallable, Category = "PetProxyCharacter")
		void PlayActionFinish(ACharacter* Character, FACTION_DATA InActionData);

	///通过ModleID更换模型
	UFUNCTION(BlueprintCallable, Category = "PetProxyCharacter")
		void ChangeModel(FString ModelID);
	
	UFUNCTION(BlueprintPure, Category = "PetProxyCharacter")
		FString GetModelID();

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	
};
