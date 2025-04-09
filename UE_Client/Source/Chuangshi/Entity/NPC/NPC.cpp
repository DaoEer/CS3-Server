
#include "NPC.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/NPC/NPCInterface.h"
#include "Interface/NPC/NPCQuestInterface.h"
#include "Interface/EntitySpaceEventInterface.h"

DEF_INTERFACE_BEGIN(NPC, Supper)
DEF_INTERFACE(UNPCInterface)
DEF_INTERFACE(UNPCQuestInterface)
DEF_INTERFACE(UEntitySpaceEventInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPC, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPC, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

NPC::NPC()
{
	_fActorName = FString("NPC");
	//_fCompontentName = FName( "UNPCActorComponent" );
}

NPC::~NPC()
{
}

UClass* NPC::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPC")); 
}