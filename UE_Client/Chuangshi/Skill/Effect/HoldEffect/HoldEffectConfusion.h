#pragma once
#include "HoldEffect.h"

#include "HoldEffectConfusion.generated.h"



/*
* 文件名称：HoldEffectConfusion.h
* 功能说明：持有效果：混乱（PC无法被控制，乱走）
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffectConfusion :public UHoldEffect
{
	GENERATED_BODY()
public:
	UHoldEffectConfusion();
	~UHoldEffectConfusion();

public:
	/*效果开始*/
	virtual void onBegin(UHoldEffectDataType* effectData, CS3Entity* receiver);

	/*效果结束*/
	virtual void onEnd(UHoldEffectDataType* effectData, CS3Entity* receiver);

private:

};

