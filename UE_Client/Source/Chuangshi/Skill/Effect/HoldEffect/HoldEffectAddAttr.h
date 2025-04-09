#pragma once
#include "HoldEffect.h"

#include "HoldEffectAddAttr.generated.h"

/*
* 文件名称：HoldEffectAddAttr.h
* 功能说明：战斗属性 增益/减损 效果
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffectAddAttr : public UHoldEffect
{
	GENERATED_BODY()
public:
	UHoldEffectAddAttr();
	~UHoldEffectAddAttr();

public:
	/*读取技能配置*/
	virtual void init(FHOLD_EFFECT dictDat, USkill* skill);

	/*效果开始*/
	virtual void onBegin(UHoldEffectDataType* effectData, CS3Entity* receiver);

	/*效果结束*/
	virtual void onEnd(UHoldEffectDataType* effectData, CS3Entity* receiver);

private:
	TArray<int32> _propertiesList;
	int32 _attrPercent = 0;
	int32 _attrValue = 0;
};



