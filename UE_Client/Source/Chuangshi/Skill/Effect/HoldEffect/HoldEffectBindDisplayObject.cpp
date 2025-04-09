#include "HoldEffectBindDisplayObject.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/GameObjectInterface.h"
#include "CS3Base/GameObject.h"


UHoldEffectBindDisplayObject::UHoldEffectBindDisplayObject()
{
	_meshID = "";
}

UHoldEffectBindDisplayObject::~UHoldEffectBindDisplayObject()
{
}

void UHoldEffectBindDisplayObject::init(FHOLD_EFFECT dictDat, USkill * skill)
{
	UHoldEffect::init(dictDat, skill);
	_meshID = dictDat.Param1;
}

void UHoldEffectBindDisplayObject::onBegin(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UHoldEffect::onBegin(effectData, receiver);
	UGameObjectInterface *GameObjectInterface = ((GameObject*)receiver)->Interface_Cache.GameObjectInterface;
	if (IsValid(GameObjectInterface))
	{
		GameObjectInterface->CLIENT_BindDisplayObject(_meshID);
	}
}

void UHoldEffectBindDisplayObject::onEnd(UHoldEffectDataType * effectData, CS3Entity * receiver)
{
	UGameObjectInterface *GameObjectInterface = ((GameObject*)receiver)->Interface_Cache.GameObjectInterface;
	if (IsValid(GameObjectInterface))
	{
		GameObjectInterface->CLIENT_UnbindDisplayObject(_meshID);
	}

	UHoldEffect::onEnd(effectData, receiver);
}
