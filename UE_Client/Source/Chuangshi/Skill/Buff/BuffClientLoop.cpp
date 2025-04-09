#include "BuffClientLoop.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Skill/SkillBase/SkillTargetObjImpl.h"


UBuffClientLoop::UBuffClientLoop()
{
	_className = "BuffClientLoop";
	_loopHitList = NewObject<UBuffHitData>();
}

UBuffClientLoop::~UBuffClientLoop()
{
}

void UBuffClientLoop::init(FString BuffID, const FBUFF_TABLE_DATA * dictDat)
{
	UBuffClientHit::init(BuffID, dictDat);
	_loopHitList->init(dictDat->LoopHitList, this);
}

void UBuffClientLoop::doBegin(CS3Entity * receiver, UBuffDataType * buffData)
{
	UBuffClientHit::doBegin(receiver, buffData);
	addBuffLoopTimer(receiver, buffData);
}

void UBuffClientLoop::doReload(CS3Entity * receiver, UBuffDataType * buffData)
{
	UBuffClientHit::doReload(receiver, buffData);
	addBuffLoopTimer(receiver, buffData);
}

void UBuffClientLoop::doEnd(CS3Entity * receiver, UBuffDataType * buffData, BUFF_END_RESON reason)
{
	if (buffData->timerID.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(buffData->timerID);
	}
	UBuffClientHit::doEnd(receiver, buffData, reason);
}

void UBuffClientLoop::doLoopHit(CS3Entity * receiver, UBuffDataType * buffData)
{
	CS3Entity * caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(buffData->casterID);
	USkillTargetObjEntity* instance = NewObject<USkillTargetObjEntity>();
	instance->init(receiver);
	USkillTargetObjImpl* target = (USkillTargetObjImpl*)instance;
	target->AddToRoot();
	if (nullptr != caster && nullptr != target)
	{
		_loopHitList->onHit(this, caster, target, "_loopHitList");
	}
}

UBuffHitDefine * UBuffClientLoop::getHit(FString attrName, int32 index)
{
	if ("_beginHitList" == attrName)
	{
		return _beginHitList->getHit(index);
	}
	else if ("_endHitList" == attrName)
	{
		return _endHitList->getHit(index);
	}
	else if ("_loopHitList" == attrName)
	{
		return _loopHitList->getHit(index);
	}
	return nullptr;
}

void UBuffClientLoop::addBuffLoopTimer(CS3Entity * receiver, UBuffDataType * buffData)
{
	if (getLoopTime() > 0.0)
	{
		int32 receiverID = receiver->ID();
		TWeakObjectPtr<UBuffClientLoop> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, buffData->timerID, FTimerDelegate::CreateLambda([DelayThisPtr, receiverID, buffData]()
		{
			if (DelayThisPtr.IsValid())
			{
				UBuffClientLoop* ThisPtr = DelayThisPtr.Get();
				CS3Entity * entity = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(receiverID);
				ThisPtr->doLoopHit(entity, buffData);
			}
		}), getLoopTime(), true);
	}
}
