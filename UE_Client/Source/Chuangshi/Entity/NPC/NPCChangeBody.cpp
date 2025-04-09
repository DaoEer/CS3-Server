
#include "NPCChangeBody.h"
#include "Util/GolbalBPFunctionLibrary.h"


KBE_BEGIN_ENTITY_METHOD_MAP(NPCChangeBody, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCChangeBody, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

NPCChangeBody::NPCChangeBody()
{
	_fActorName = FString("NPCChangeBody");
	//_fCompontentName = FName( "UNPCActorComponent" );
}

NPCChangeBody::~NPCChangeBody()
{
}

UClass* NPCChangeBody::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPC")); 
}