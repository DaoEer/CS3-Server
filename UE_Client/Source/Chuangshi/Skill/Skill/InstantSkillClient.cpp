#include "InstantSkillClient.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/StateInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "CS3Base/GameObject.h"

UInstantSkillClient::UInstantSkillClient()
{
}

UInstantSkillClient::~UInstantSkillClient()
{
}

int32 UInstantSkillClient::useableCheck(CS3Entity * caster, USkillTargetObjImpl * target)
{
	//施法者是否有禁止标记
	if (_casterActForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		UStateInterface * StateInterface = ((GameObject*)caster)->Interface_Cache.StateInterface;
		if (IsValid(StateInterface) && StateInterface->IsActionForbid(_casterActForbid))
		{
			return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
		}
	}

	//技能目标是否有禁止标记
	if (_targetActForbid != ACTION_FLAG::ACTION_FORBID_NONE && target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY)
	{
		UStateInterface * StateInterface = ((GameObject*)target->getObject())->Interface_Cache.StateInterface;
		if (IsValid(StateInterface) && StateInterface->IsActionForbid(_casterActForbid))
		{
			return (int32)SKILL_MESSAGE::SKILL_STATE_CANT_CAST;
		}

	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));

	//检查技能cooldown
	if (isCasterCooldown(caster))
	{
		return (int32)SKILL_MESSAGE::SKILL_NOT_READY;
	}

	//检查技能cooldown
	if (target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY)
	{
		if (isTargetCooldown(target))
		{
			return (int32)SKILL_MESSAGE::SKILL_TARGET_NOT_READY;
		}
	}

	//施法需求检查
	int state = checkCasterRequire(caster);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}

	//施法目标需求检查
	//if (target->getType() == SKILL_TARGET_TYPE::SKILL_TARGET_OBJECT_ENTITY)
	//{
	///	state = checkTargetRequire(target);
	//	if ( state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	//	{
	//		return state;
	//	}
	//}

	//施法者检查
	state = castValidCheck(caster, caster);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}

	//施法目标检查
	state = targetValidCheck(caster, target);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}

	//检查目标是否符合法术施展
	state = getCastObject()->CastValid(caster, target);
	if (state != (int32)SKILL_MESSAGE::SKILL_GO_ON)
	{
		return state;
	}
	return (int32)SKILL_MESSAGE::SKILL_GO_ON;
}

void UInstantSkillClient::onSkillBegin(CS3Entity * caster, USkillTargetObjImpl * target)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->onSkillBegin(this, target);
	}
	bool isHit = true;
	addHoldEffect(caster);

	if (IsValid(CSkillInterface))
	{
		CSkillInterface->triggerEventSkillBegin(this);
	}
	if (IsValid(CSkillInterface) && CSkillInterface->IsInterruptInstantSkill(getID()))
	{
		CSkillInterface->interruptInstantSkill(this, (int32)SKILL_MESSAGE::SKILL_CAST_FAILED);
		isHit = false;
	}
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->setIsInterruptInstantSkill(getID(), true);
	}
	if (isHit)
	{
		_hitData->begin(this, caster, target);
	}
}

void UInstantSkillClient::onSkillEnd(CS3Entity * caster, USkillTargetObjImpl * target, bool castResult)
{
	USkill::onSkillEnd(caster, target, castResult);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->setIsInterruptInstantSkill(getID(), false);
	}

}

void UInstantSkillClient::triggerSkillEvent(CS3Entity * caster, ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict)
{
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if(!IsValid(CSkillInterface))
	{
		return;
	}
	if (eventType == ENUM_SKILL_EVENT::ActWorldChangeEvent)
	{
		ACTION_FLAG actWord = ACTION_FLAG::ACTION_FORBID_NONE;
		if (pDict.Contains("actWord"))
		{
			actWord = (ACTION_FLAG)pDict["actWord"].GetValue<int32>();
		}
		if (actWord == _casterActForbid)
		{
			if(CSkillInterface->IsInterruptInstantSkill(getID()))
			{
				CSkillInterface->interruptInstantSkill(this, (int32)SKILL_MESSAGE::SKILL_CAST_FAILED);
			} else {
				CSkillInterface->setIsInterruptInstantSkill(getID(), true);
			}	
		}
	}
	if (_interruptEvent->canTriggerEvent(eventType, pDict))
	{
		CSkillInterface->interruptInstantSkill(this, (int32)SKILL_MESSAGE::SKILL_CAST_FAILED);
	}
}

void UInstantSkillClient::triggerReceiverSkillEvent(CS3Entity * caster, CS3Entity * receiver, ENUM_SKILL_EVENT eventType, int32 triggerID, TMap<FString, FVariant> pDict)
{
}

bool UInstantSkillClient::isInstantSkill()
{
	return true;
}
