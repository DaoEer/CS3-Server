
#include "NPCExtMove.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/NPC/NPCExtMoveInterface.h"


DEF_INTERFACE_BEGIN(NPCExtMove, Supper)
DEF_INTERFACE(UNPCExtMoveInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPCExtMove, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCExtMove, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCExtMove::NPCExtMove()
{
	_fActorName = FString("NPCExtMove");
	//_fCompontentName = FName("UNPCActorComponent");
}

NPCExtMove::~NPCExtMove()
{
}

UClass* NPCExtMove::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPCExtMove")); 
}