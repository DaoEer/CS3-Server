#pragma once

#include "CoreMinimal.h"
#include "Manager/Delegate/RelationDelegateObject.h"
#include "PetDelegateObject.generated.h"

/**
 * 幻兽系统 委托声明对象
 */

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnUpdatePetShenTongSkill, FString, PetUID);

UCLASS()
class CHUANGSHI_API UPetDelegateObject : public URelationDelegateObject
{
	GENERATED_BODY()
public:
#pragma region	/** 幻兽神通技能 */
	//更新幻兽神通技能（增加、删除、更新次数）
	UPROPERTY(BlueprintAssignable, Category = "Pet")
		FOnUpdatePetShenTongSkill OnUpdatePetShenTongSkillEvent;
#pragma endregion
};
