#include "BuffClientHit.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Skill/SkillBase/SkillTargetObjImpl.h"

CONTROL_COMPILE_OPTIMIZE_START
UBuffClientHit::UBuffClientHit()
{
	_className = "BuffClientHit";
	_beginHitList = NewObject<UBuffHitData>();
	_endHitList = NewObject<UBuffHitData>();
}

UBuffClientHit::~UBuffClientHit()
{

}

void UBuffClientHit::init(FString BuffID, const FBUFF_TABLE_DATA * dictDat)
{
	UBuffClientHold::init(BuffID, dictDat);
	_beginHitList->init(dictDat->BeginHitList, this);
	_endHitList->init(dictDat->EndHitList, this);
}

UBuffHitDefine * UBuffClientHit::getHit(FString attrName, int32 index)
{
	if ("_beginHitList" == attrName)
	{
		return _beginHitList->getHit(index);
	}
	else if("_endHitList" == attrName)
	{
		return _endHitList->getHit(index);
	}

	return nullptr;
}

void UBuffClientHit::doBeginHit(CS3Entity * receiver, UBuffDataType * buffData)
{
	CS3Entity * caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(buffData->casterID);
	USkillTargetObjEntity* instance = NewObject<USkillTargetObjEntity>();
	instance->init(receiver);
	USkillTargetObjImpl* target = (USkillTargetObjImpl*)instance;
	target->AddToRoot();
	if (nullptr != caster && nullptr != target)
	{
		_beginHitList->onHit(this, caster, target, "_beginHitList");
	}
}

void UBuffClientHit::doEndHit(CS3Entity * receiver, UBuffDataType * buffData)
{
	CS3Entity * caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(buffData->casterID);
	USkillTargetObjEntity* instance = NewObject<USkillTargetObjEntity>();
	instance->init(receiver);
	USkillTargetObjImpl* target = (USkillTargetObjImpl*)instance;
	target->AddToRoot();
	if (nullptr != caster && nullptr != target)
	{
		_endHitList->onHit(this, caster, target, "_endHitList");
	}
}
CONTROL_COMPILE_OPTIMIZE_END