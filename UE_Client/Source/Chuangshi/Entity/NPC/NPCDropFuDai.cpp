#include "NPCDropFuDai.h"
#include "Interface/NPC/NPCGinsengFruitInterface.h"
#include "Actor/ServerCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/NPCDropFuDaiInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(NPCDropFuDai, Supper)
DEF_INTERFACE(UNPCDropFuDaiInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPCDropFuDai, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCDropFuDai, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCDropFuDai::NPCDropFuDai()
{
}


NPCDropFuDai::~NPCDropFuDai()
{
}


UClass* NPCDropFuDai::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPCDropFuDai"));
}

CONTROL_COMPILE_OPTIMIZE_END
