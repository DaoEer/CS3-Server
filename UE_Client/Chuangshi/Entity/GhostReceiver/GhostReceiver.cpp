
#include "GhostReceiver.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Actor/ServerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/SkillInterface.h"
#include "Interface/GhostReceiver/GhostReceiverInterface.h"

DEF_INTERFACE_BEGIN(GhostReceiver, Supper)
DEF_INTERFACE(USkillInterface)
DEF_INTERFACE(UGhostReceiverInterface)
DEF_INTERFACE_END()



KBE_BEGIN_ENTITY_METHOD_MAP(GhostReceiver, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(GhostReceiver, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

GhostReceiver::GhostReceiver()
{
	_fActorName = FString("GhostReceiver");
	IsDirectionSameToEntity = true;
	//_fCompontentName = FName("UGhostReceiverActorComponent");
}

GhostReceiver::~GhostReceiver()
{

}


bool GhostReceiver::IsState(ENTITY_STATE EntityState)
{
	int32 State = GetDefinedProperty(TEXT("state")).GetValue<int32>();
	return State == int32(EntityState);
}

UClass* GhostReceiver::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_GhostReceiver")); 
}
