#pragma once
#include "BaseAnimInstance.h"
#include "EffectAnimInstance.generated.h"

/*
* 文件名称：EffectAnimInstance.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-08-04
*/
UCLASS(Blueprintable, hideCategories = EffectAnimInstance, BlueprintType, meta = (BlueprintThreadSafe), Within = SkeletalMeshComponent)
class CHUANGSHI_API UEffectAnimInstance : public UBaseAnimInstance
{
	GENERATED_BODY()
public:
	UEffectAnimInstance();
	~UEffectAnimInstance();

protected:

private:

};

