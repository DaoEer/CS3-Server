
#include "NPCTorture.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/NPC/NPCTortureInterface.h"

DEF_INTERFACE_BEGIN(NPCTorture, Supper)
DEF_INTERFACE(UNPCTortureInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPCTorture, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCTorture, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCTorture::NPCTorture()
{
	_fActorName = FString("NPCTorture");
	//_fCompontentName = FName("UNPCActorComponent");
}

NPCTorture::~NPCTorture()
{
}

UClass* NPCTorture::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPCTorture")); 
}