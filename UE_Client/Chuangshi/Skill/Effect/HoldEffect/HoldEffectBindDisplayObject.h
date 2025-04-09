#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "HoldEffect.h"

#include "HoldEffectBindDisplayObject.generated.h"

/*
* 文件名称：HoldEffectBindDisplayObject.h
* 功能说明：持有效果：模型绑定部件
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-12-9
*/


UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffectBindDisplayObject :public UHoldEffect
{
	GENERATED_BODY()
public:
	UHoldEffectBindDisplayObject();
	~UHoldEffectBindDisplayObject();

public:
	/*读取技能配置*/
	virtual void init(FHOLD_EFFECT dictDat, USkill * skill);

	/*效果开始*/
	virtual void onBegin(UHoldEffectDataType* effectData, CS3Entity* receiver);

	/*效果结束*/
	virtual void onEnd(UHoldEffectDataType* effectData, CS3Entity* receiver);
private:
	FString _meshID;
};

