#pragma once
#include "CoreMinimal.h"
#include "EntityDataCache.generated.h"

// 在GameObject类中缓存
// 由于UGolbalBPFunctionLibrary::GetInterfaceByName效率较低,这里缓存使用频率比较高的结果 CST-9943
USTRUCT(BlueprintType, Category = "EntityDataCache")
struct FEntityInterface_Cache
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "EntityDataCache")
	class UStateInterface* StateInterface = nullptr;

	UPROPERTY(BlueprintReadOnly, Category = "EntityDataCache")
	class USkillInterface* SkillInterface = nullptr;

	UPROPERTY(BlueprintReadOnly, Category = "EntityDataCache")
	class UGameObjectInterface* GameObjectInterface = nullptr;

	UPROPERTY(BlueprintReadOnly, Category = "EntityDataCache")
	class URoleTeamInterface* RoleTeamInterface = nullptr;

	UPROPERTY(BlueprintReadOnly, Category = "EntityDataCache")
	class UEntitySpaceEventInterface* EntitySpaceEventInterface = nullptr;

	UPROPERTY(BlueprintReadOnly, Category = "EntityDataCache")
	class UCombatInterface* CombatInterface = nullptr;
};