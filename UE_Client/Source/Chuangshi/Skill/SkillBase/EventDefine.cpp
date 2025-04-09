#include "EventDefine.h"
#include "Skill.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/StateInterface.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"

CONTROL_COMPILE_OPTIMIZE_START

UBaseEvent::UBaseEvent()
{
}

UBaseEvent::~UBaseEvent()
{
}

void UBaseEvent::init(FSKILL_EVENT args)
{

}

bool UBaseEvent::canTriggerEvent(TMap<FString, FVariant> pDict)
{
	return false;
}

UOnDieEvent::UOnDieEvent()
{
	eventType = ENUM_SKILL_EVENT::OnDieEvent;
}

UOnDieEvent::~UOnDieEvent()
{
}

void UOnDieEvent::init(FSKILL_EVENT args)
{
	if (args.Param1 != "")
	{
		int32 Param1 = FSTRING_TO_INT(args.Param1);
		_actForbid = (ACTION_FLAG)Param1;
	}
	if (args.Param2 != "")
	{
		_type = FSTRING_TO_INT(args.Param2);
	}
}

bool UOnDieEvent::canTriggerEvent(TMap<FString, FVariant> pDict)
{
	if (_actForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		int32 temp = pDict["actForbid"].GetValue<int32>();
		if (_actForbid != (ACTION_FLAG)temp)
		{
			return false;
		}
	}
	if (_type != NULL && pDict.Contains("type") && pDict["type"].GetValue<int32>() != _type)
	{
		return false;
	}
	return true;
}

UStateChangeEvent::UStateChangeEvent()
{
	eventType = ENUM_SKILL_EVENT::StateChangeEvent;
}

UStateChangeEvent::~UStateChangeEvent()
{
}

void UStateChangeEvent::init(FSKILL_EVENT args)
{
	if (args.Param1 != "")
	{
		_oldState = FSTRING_TO_INT(args.Param1);
	}
	if (args.Param2 != "")
	{
		_newState = FSTRING_TO_INT(args.Param2);
	}
}

bool UStateChangeEvent::canTriggerEvent(TMap<FString, FVariant> pDict)
{
	if (_oldState != NULL && _oldState != pDict["oldState"].GetValue<int32>())
	{
		return false;
	}
	if (_newState != NULL && _newState != pDict["newState"].GetValue<int32>())
	{
		return false;
	}
	return true;
}

UActWorldChangeEvent::UActWorldChangeEvent()
{
	eventType = ENUM_SKILL_EVENT::ActWorldChangeEvent;
}

UActWorldChangeEvent::~UActWorldChangeEvent()
{
}

void UActWorldChangeEvent::init(FSKILL_EVENT args)
{
	if (args.Param1 != "")
	{
		int32 Param1 = FSTRING_TO_INT(args.Param1);
		_actWord = (ACTION_FLAG)Param1;
	}
	if (args.Param2 != "")
	{
		int32 Param2 = FSTRING_TO_INT(args.Param1);
		_disable = (bool)Param2;
	}
}

bool UActWorldChangeEvent::canTriggerEvent(TMap<FString, FVariant> pDict)
{
	if (_actWord != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		int32 temp = pDict["actWord"].GetValue<int32>();
		if (_actWord != (ACTION_FLAG)temp)
		{
			return false;
		}
	}

	if (_disable != NULL && _disable != pDict["disabled"].GetValue<bool>())
	{
		return false;
	}
	return true;
}

UEffectStateChangeEvent::UEffectStateChangeEvent()
{
	eventType = ENUM_SKILL_EVENT::EffectStateChangeEvent;
}

UEffectStateChangeEvent::~UEffectStateChangeEvent()
{
}

void UEffectStateChangeEvent::init(FSKILL_EVENT args)
{
	if (args.Param1 != "")
	{
		int32 Param1 = FSTRING_TO_INT(args.Param1);
		_effectState = (EFFECT_STATE)Param1;
	}
	if (args.Param2 != "")
	{
		int32 Param2 = FSTRING_TO_INT(args.Param1);
		_disable = (bool)Param2;
	}
}

bool UEffectStateChangeEvent::canTriggerEvent(TMap<FString, FVariant> pDict)
{
	if (_effectState != EFFECT_STATE::EFFECT_STATE_NULL)
	{
		int32 temp = pDict["effectState"].GetValue<int32>();
		if (_effectState != (EFFECT_STATE)temp)
		{
			return false;
		}
	}

	if (_disable != NULL && _disable != pDict["disabled"].GetValue<bool>())
	{
		return false;
	}
	return true;
}

UCustomEvent::UCustomEvent()
{
	eventType = ENUM_SKILL_EVENT::CustomEvent;
}

UCustomEvent::~UCustomEvent()
{
}

void UCustomEvent::init(FSKILL_EVENT args)
{
	if (args.Param1 != "")
	{
		_id = FSTRING_TO_INT(args.Param1);
	}
	if (args.Param2 != "")
	{
		int32 Param2 = FSTRING_TO_INT(args.Param2);
		_actWord = (ACTION_FLAG)Param2;
	}

}

bool UCustomEvent::canTriggerEvent(TMap<FString, FVariant> pDict)
{
	if (_id != NULL && _id != pDict["id"].GetValue<int32>())
	{
		return false;
	}

	if (_actWord != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		ACTION_FLAG actFb = ACTION_FLAG::ACTION_FORBID_NONE;
		if (pDict.Contains("actWord"))
		{
			int32 temp = pDict["actWord"].GetValue<int32>();
			actFb = (ACTION_FLAG)temp;
		}
		
		if (actFb == ACTION_FLAG::ACTION_FORBID_NONE || _actWord != actFb)
		{
			return false;
		}
	}

	return true;
}

USkillEvent::USkillEvent()
{
}

USkillEvent::~USkillEvent()
{
}

void USkillEvent::init(FSKILL_EVENT args)
{
	if (args.Param1 != "")
	{
		int32 Param1 = FSTRING_TO_INT(args.Param1);
		_actForbid = (ACTION_FLAG)Param1;
	}

	if (args.Param2 != "")
	{
		_type = FSTRING_TO_INT(args.Param2);
	}

	if (args.Param3 != "")
	{
		_skillID = FSTRING_TO_INT(args.Param3);
	}
}

bool USkillEvent::canTriggerEvent(TMap<FString, FVariant> pDict)
{
	if (_actForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		int32 temp = pDict["actForbid"].GetValue<int32>();
		if (_actForbid != (ACTION_FLAG)temp)
		{
			return false;
		}
	}
	if (_type != NULL && pDict.Contains("type") && _type != pDict["type"].GetValue<int32>())
	{
		return false;
	}

	if (_skillID != NULL && pDict.Contains("skillID") && _skillID != pDict["skillID"].GetValue<int32>())
	{
		return false;
	}
	return true;
}

UCureEvent::UCureEvent()
{
	eventType = ENUM_SKILL_EVENT::CureEvent;
}

UCureEvent::~UCureEvent()
{
}

UHurtEvent::UHurtEvent()
{
	eventType = ENUM_SKILL_EVENT::HurtEvent;
}

UHurtEvent::~UHurtEvent()
{
}

void UHurtEvent::init(FSKILL_EVENT args)
{
	if (args.Param1 != "")
	{
		int32 Param1 = FSTRING_TO_INT(args.Param1);
		_actForbid = (ACTION_FLAG)Param1;
	}

	if (args.Param2 != "")
	{
		_type = FSTRING_TO_INT(args.Param2);
	}
	if (args.Param3 != "")
	{
		_conditions = UGolbalBPFunctionLibrary::SplitString(args.Param3);
	}
}

bool UHurtEvent::canTriggerEvent(TMap<FString, FVariant> pDict)
{
	if (_actForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		int32 temp = pDict["actForbid"].GetValue<int32>();
		if (_actForbid != (ACTION_FLAG)temp)
		{
			return false;
		}
	}
	if (_type != NULL && pDict.Contains("type") && _type != pDict["type"].GetValue<int32>())
	{
		return false;
	}
	for (auto i : _conditions)
	{
		if (!pDict.Contains(i))
		{
			return false;
		}
		else if (pDict[i].GetValue<int32>() != 0)
		{
			false;
		}
	}
	return true;
}

USkillProcessEvent::USkillProcessEvent()
{
	eventType = ENUM_SKILL_EVENT::SkillProcessEvent;
}

USkillProcessEvent::~USkillProcessEvent()
{
}

UBuffProcessEvent::UBuffProcessEvent()
{
	eventType = ENUM_SKILL_EVENT::BuffProcessEvent;
}

UBuffProcessEvent::~UBuffProcessEvent()
{
}

void UBuffProcessEvent::init(FSKILL_EVENT args)
{
	if (args.Param1 != "")
	{
		int32 Param1 = FSTRING_TO_INT(args.Param1);
		_actForbid = (ACTION_FLAG)Param1;
	}

	if (args.Param2 != "")
	{
		_type = FSTRING_TO_INT(args.Param2);
	}

	if (args.Param3 != "")
	{
		_buffID = FSTRING_TO_INT(args.Param3);
	}
}

bool UBuffProcessEvent::canTriggerEvent(TMap<FString, FVariant> pDict)
{
	if (_actForbid != ACTION_FLAG::ACTION_FORBID_NONE)
	{
		int32 temp = pDict["actForbid"].GetValue<int32>();
		if (_actForbid != (ACTION_FLAG)temp)
		{
			return false;
		}
	}
	if (_type != NULL && pDict.Contains("type") && _type != pDict["type"].GetValue<int32>())
	{
		return false;
	}

	if (_buffID != NULL && pDict.Contains("buffID") && _buffID != pDict["buffID"].GetValue<int32>())
	{
		return false;
	}
	return true;
}


UEventDefine::UEventDefine()
{

}

UEventDefine::~UEventDefine()
{

}

void UEventDefine::init(TArray<FSKILL_EVENT> datas)
{
	for (auto data : datas)
	{
		UBaseEvent* Instance = CreateEventInstance(data);
		if (Instance == nullptr)
		{
			continue;
		}
		if (!_eventList.Contains(data.EventType))
		{
			FEVENT_DATAS Temp;
			Temp.EventList.Add(Instance);
			_eventList.Add(data.EventType, Temp);
		}
		_eventList[data.EventType].EventList.Add(Instance);
	}
	
}

UBaseEvent * UEventDefine::CreateEventInstance(FSKILL_EVENT data)
{
	UBaseEvent* Instance = nullptr;
	if (data.EventType == ENUM_SKILL_EVENT::OnDieEvent)
	{
		UOnDieEvent* Temp = NewObject<UOnDieEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::StateChangeEvent)
	{
		UStateChangeEvent* Temp = NewObject<UStateChangeEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::ActWorldChangeEvent)
	{
		UActWorldChangeEvent* Temp = NewObject<UActWorldChangeEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::EffectStateChangeEvent)
	{
		UEffectStateChangeEvent* Temp = NewObject<UEffectStateChangeEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::CustomEvent)
	{
		UCustomEvent* Temp = NewObject<UCustomEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::CureEvent)
	{
		UCureEvent* Temp = NewObject<UCureEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::HurtEvent)
	{
		UHurtEvent* Temp = NewObject<UHurtEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	return Instance;
}

void UEventDefine::registerEvent(USkill* skill, CS3Entity * caster)
{
	if (!caster )
	{
		return;
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	
	for (auto i : _eventList)
	{
		CSkillInterface->registerSkillEvent(i.Key, skill->getID());
	}

}

void UEventDefine::unRegisterEvent(USkill* skill, CS3Entity * caster)
{
	if (!caster)
	{
		return;
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}

	for (auto i : _eventList)
	{
		CSkillInterface->unRegisterSkillEvent(i.Key, skill->getID());
	}
}

void UEventDefine::registerBuffEvent(UBuffDataType * buffData, CS3Entity * caster, CS3Entity * receiver)
{
	if (!caster || !receiver)
	{
		return;
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	for (auto i : _eventList)
	{
		CSkillInterface->registerCasterBuffEvent(i.Key, receiver->ID(), buffData->index);
	}
}

void UEventDefine::unRegisterBuffEvent(UBuffDataType * buffData, CS3Entity * caster, CS3Entity * receiver)
{
	if (!caster || !receiver)
	{
		return;
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), caster->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	for (auto i : _eventList)
	{
		CSkillInterface->unRegisterCasterBuffEvent(i.Key, receiver->ID(), buffData->index);
	}
}

bool UEventDefine::canTriggerEvent(ENUM_SKILL_EVENT eventType, TMap<FString, FVariant> pDict)
{
	if (_eventList.Contains(eventType))
	{
		for (auto inst : _eventList[eventType].EventList)
		{
			if (inst->canTriggerEvent(pDict))
			{
				return true;
			}
		}
	}
	return false;
}


UReceiverEventDefine::UReceiverEventDefine()
{
}

UReceiverEventDefine::~UReceiverEventDefine()
{
}

void UReceiverEventDefine::init(TArray<FSKILL_EVENT> datas)
{
	for (auto data : datas)
	{
		UBaseEvent* Instance = CreateEventInstance(data);
		if (Instance == nullptr)
		{
			continue;
		}
		if (!_receiverEventList.Contains(data.EventType))
		{
			FEVENT_DATAS Temp;
			Temp.EventList.Add(Instance);
			_receiverEventList.Add(data.EventType, Temp);
		}
		_receiverEventList[data.EventType].EventList.Add(Instance);
	}
}

UBaseEvent * UReceiverEventDefine::CreateEventInstance(FSKILL_EVENT data)
{
	UBaseEvent* Instance = nullptr;
	if (data.EventType == ENUM_SKILL_EVENT::OnDieEvent)
	{
		UOnDieEvent* Temp = NewObject<UOnDieEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if(data.EventType == ENUM_SKILL_EVENT::StateChangeEvent)
	{
		UStateChangeEvent* Temp = NewObject<UStateChangeEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::ActWorldChangeEvent)
	{
		UActWorldChangeEvent* Temp = NewObject<UActWorldChangeEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::EffectStateChangeEvent)
	{
		UEffectStateChangeEvent* Temp = NewObject<UEffectStateChangeEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::CustomEvent)
	{
		UCustomEvent* Temp = NewObject<UCustomEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::CureEvent)
	{
		UCureEvent* Temp = NewObject<UCureEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	else if (data.EventType == ENUM_SKILL_EVENT::HurtEvent)
	{
		UHurtEvent* Temp = NewObject<UHurtEvent>();
		Temp->init(data);
		Instance = (UBaseEvent*)Temp;
	}
	return Instance;
}

void UReceiverEventDefine::registerEvent(USkill* skill, CS3Entity * caster, USkillTargetObjImpl* target)
{
	//由于技能流程关系 unRegister 不在此处处理
	if (skill->getTargetType() == ENUM_CAST_TARGET_TYPE::TargetPosition)
	{
		return;
	}
	if (!target || !caster)
	{
		return;
	}
	CS3Entity* receiver = target->getObject();
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}

	for (auto i : _receiverEventList)
	{
		CSkillInterface->registerReceiverSkillEvent(i.Key, caster->ID(), skill->getID());
	}
}

void UReceiverEventDefine::registerBuffEvent(UBuffDataType * buffData, CS3Entity * receiver)
{
	if (!receiver)
	{
		return;
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	for (auto i : _receiverEventList)
	{
		CSkillInterface->registerBuffEvent(i.Key, buffData->index);
	}
}

void UReceiverEventDefine::unRegisterBuffEvent(UBuffDataType * buffData, CS3Entity * receiver)
{
	if (!receiver)
	{
		return;
	}
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), receiver->ID()));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	for (auto i : _receiverEventList)
	{
		CSkillInterface->unRegisterBuffEvent(i.Key, buffData->index);
	}
}


bool UReceiverEventDefine::canTriggerEvent(ENUM_SKILL_EVENT eventType, TMap<FString, FVariant> pDict)
{
	if (_receiverEventList.Contains(eventType))
	{
		for (auto inst : _receiverEventList[eventType].EventList)
		{
			if (inst->canTriggerEvent(pDict))
			{
				return true;
			}
		}
	}
	return false;
}

CONTROL_COMPILE_OPTIMIZE_END