#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/GameDeFine.h"
#include "GameData/Skill/SkillTableData.h"
#include "GameData/Skill/HoldEffectDataType.h"

#include "HoldEffect.generated.h"

class USkill;
/*
* 文件名称：HoldEffect.h
* 功能说明：持有效果基类
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/


UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffect:public UCS3Object
{
	GENERATED_BODY()
public:
	UHoldEffect();
	~UHoldEffect();

public:
	/*读取技能配置*/
	virtual void init(FHOLD_EFFECT dictDat, USkill * skill);

	/*生成持有效果数据*/
	virtual UHoldEffectDataType* getNewEffectData(CS3Entity* caster, CS3Entity* receiver);

	/*效果添加检测*/
	virtual bool canEffect(CS3Entity* caster, CS3Entity* receiver);

	/*效果开始*/
	virtual void onBegin(UHoldEffectDataType* effectData, CS3Entity* receiver);

	/*效果结束*/
	virtual void onEnd(UHoldEffectDataType* effectData, CS3Entity* receiver);

	/*receiver在某客户端被创建出来*/
	virtual void onClientActorCreate(UHoldEffectDataType* effectData, CS3Entity* receiver);
};

