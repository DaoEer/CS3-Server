#pragma once

#include "Actor/GameCharacter.h"
#include "RiderCharacter.generated.h"

/*
* 文件名称：RiderCharacter.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-08-15
*/

/**
 * 骑士基类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API ARiderCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	ARiderCharacter();
	virtual void OnCreateModelOver() override;
	virtual void BeginPlay()override;

	virtual void SetInitAction() override;///<重写SetInitAction
	void ApplayModelByPartsMap(TMap<MODEL_PART_TYPE, FString>& NewPartMap);
	void ChangeActorPart(MODEL_PART_TYPE pos, FString PartID);
	void UseRideAnimData(TSoftClassPtr<UAnimInstance> AnimationPath, TSoftObjectPtr<UDataTable> ActionConfigPath);
	void SetModelData(TSharedPtr<FMODEL_DATA> ModelData);
	void SetPlayerCharacter(AGameCharacter* InPlayerCharacter);

protected:
	virtual void InitBaseComponent() override;

	void OnNotifyActionChangeFinish(FACTION_DATA ActionData);

	UPROPERTY()
		AGameCharacter* GameCharacter;//玩家
};
