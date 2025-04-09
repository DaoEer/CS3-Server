// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Actor/NPCBaseCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "PetCharacter.generated.h"

/*
* 文件名称：PetCharacter.h
* 功能说明：幻兽Character
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2017-06-30
*/

class GameObject;
class UBehaviorTree;

UCLASS(BlueprintType)
class CHUANGSHI_API APetCharacter : public ANPCBaseCharacter
{
	GENERATED_BODY()
#pragma region	Avatar功能相关
public:

	virtual void InitFilterActorComponent() override;

#pragma endregion
	typedef ANPCBaseCharacter Super;
public:
	APetCharacter();
	virtual void BeginPlay()override;
	virtual bool IsActiveMoveing();///是否主动移动中（不包括击飞相关的位移）
	virtual float GetMoveSpeed() override;
	virtual bool IsMoveing();

	inline bool PetIsPlayer() { 
		return UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("activePetID")) == EntityId;
	};

	virtual void ReSetOpenScen3DUI() { OpenScene3DUI = true; };

	void RunDefaultAITree();

	void OnChangePetAI(FString AIIndex);
	void OnFinishChangePetAI();

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	virtual void InitCharacterComponent() override;
	//初始化位置同步组件
	void InitPosSyncComponent();

public:
	UPROPERTY()
		class UPetPosSyncComponent* PetPosSyncComponent;
	
	UFUNCTION(BlueprintImplementableEvent, Category = "Game|pet")
		void OnKillingValueChanged();//

	// 幻兽使用神通技能之后，自动使用的技能
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> STSkillArr;
private:
	UBehaviorTree* DefaultBTree;
};
