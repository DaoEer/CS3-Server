#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/GameDeFine.h"
#include "GameData/Skill/SkillTableData.h"
#include "EffectSkillBase.generated.h"

class USkill;
/*
* 文件名称：EffectSkillBase.h
* 功能说明：技能效果
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UEffectSkillBase :public UCS3Object
{
	GENERATED_BODY() 
public:
	UEffectSkillBase();
	~UEffectSkillBase();

public:
	/*读取技能配置*/
	virtual void init(FHIT_EFFECT dictDat, USkill* skill);
	/*效果添加检测*/
	virtual bool canEffect(USkill* skill, CS3Entity* caster, CS3Entity* receiver);
	/*接受效果*/
	virtual void onReceive(USkill* skill, CS3Entity* caster, CS3Entity* receiver);
protected:
	ACTION_FLAG _receiverActForbid;
	ACTION_FLAG _casterActForbid;
};

