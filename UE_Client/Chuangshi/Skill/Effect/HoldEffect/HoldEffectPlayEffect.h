#pragma once
#include "HoldEffect.h"

#include "HoldEffectPlayEffect.generated.h"


/*
* 文件名称：HoldEffectPlayEffect.h
* 功能说明：持有效果：加动作限制字
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffectPlayEffect :public UHoldEffect
{
	GENERATED_BODY()
public:
	UHoldEffectPlayEffect();
	~UHoldEffectPlayEffect();

public:
	/*读取技能配置*/
	virtual void init(FHOLD_EFFECT dictDat, USkill* skill);

	/*效果开始*/
	virtual void onBegin(UHoldEffectDataType* effectData, CS3Entity* receiver);

	/*效果结束*/
	virtual void onEnd(UHoldEffectDataType* effectData, CS3Entity* receiver);

private:
	TArray<FString> _actionID;
	TArray<FString> _actionBeginTime;
	FString _effectID;
	FString _soundID;
};

