#pragma once
#include "CoreMinimal.h"
#include "Skill/SkillBase/Buff.h"
#include "BuffClientHold.generated.h"


/*
* 文件名称：BuffClientHold.h
* 功能说明：客户端持有buff
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-24
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UBuffClientHold :public UBuff
{
	GENERATED_BODY()
public:
	UBuffClientHold();
	~UBuffClientHold();

private:

};
