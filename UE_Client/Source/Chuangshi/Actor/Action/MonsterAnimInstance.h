#pragma once
#include "BaseAnimInstance.h"
#include "MonsterAnimInstance.generated.h"

/*
* 文件名称：MonsterAnimInstance.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-02-23
*/
UCLASS(Blueprintable, hideCategories = MonsterAnimInstance, BlueprintType, meta = (BlueprintThreadSafe), Within = SkeletalMeshComponent)
class CHUANGSHI_API UMonsterAnimInstance : public UBaseAnimInstance
{
	GENERATED_BODY()
public:
	UMonsterAnimInstance();
	~UMonsterAnimInstance();
protected:
	virtual bool IsInWater()override;
	virtual void UpdateMoveDirection()override;
private:

};

