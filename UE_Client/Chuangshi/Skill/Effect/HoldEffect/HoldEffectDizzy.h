#pragma once
#include "HoldEffect.h"

#include "HoldEffectDizzy.generated.h"


/*
* 文件名称：HoldEffectDizzy.h
* 功能说明：持有效果：眩晕
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffectDizzy :public UHoldEffect
{
	GENERATED_BODY()
public:
	UHoldEffectDizzy();
	~UHoldEffectDizzy();

public:
	/*效果开始*/
	virtual void onBegin(UHoldEffectDataType* effectData, CS3Entity* receiver);

	/*效果结束*/
	virtual void onEnd(UHoldEffectDataType* effectData, CS3Entity* receiver);
private:

};

