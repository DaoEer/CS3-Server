
#include "NPCExtCompose.h"
#include "Util/GolbalBPFunctionLibrary.h"


KBE_BEGIN_ENTITY_METHOD_MAP(NPCExtCompose, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCExtCompose, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

NPCExtCompose::NPCExtCompose()
{
	_fActorName = FString("NPCExtCompose");
	//_fCompontentName = FName( "UNPCActorComponent" );
}

NPCExtCompose::~NPCExtCompose()
{
}

UClass* NPCExtCompose::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPC")); 
}