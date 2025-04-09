#pragma once
#include "BaseAnimInstance.h"
#include "NpcAnimInstance.generated.h"
/*
* 文件名称：NpcAnimInstance.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-02-23
*/
UCLASS(Blueprintable, hideCategories = NpcAnimInstance, BlueprintType, meta = (BlueprintThreadSafe), Within = SkeletalMeshComponent)
class CHUANGSHI_API UNpcAnimInstance : public UBaseAnimInstance
{
	GENERATED_BODY()
public:
	UNpcAnimInstance();
	~UNpcAnimInstance();
protected:
	virtual bool IsInWater()override;
private:

};

