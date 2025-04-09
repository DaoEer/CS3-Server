#pragma once
#include "HoldEffect.h"

#include "HoldEffectFix.generated.h"


/*
* 文件名称：HoldEffectFix.h
* 功能说明：持有效果：定身（无法转向，跳跃，移动）
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffectFix :public UHoldEffect
{
	GENERATED_BODY()
public:
	UHoldEffectFix();
	~UHoldEffectFix();

public:
	/*效果开始*/
	virtual void onBegin(UHoldEffectDataType* effectData, CS3Entity* receiver);

	/*效果结束*/
	virtual void onEnd(UHoldEffectDataType* effectData, CS3Entity* receiver);

private:

};

