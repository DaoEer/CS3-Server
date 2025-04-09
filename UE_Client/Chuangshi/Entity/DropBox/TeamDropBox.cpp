
#include "TeamDropBox.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/DropBox/TeamDropBoxInterface.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/NPCBaseObjectInterface.h"

DEF_INTERFACE_BEGIN(TeamDropBox, Supper)
DEF_INTERFACE(UGameObjectInterface)
DEF_INTERFACE(UNPCBaseObjectInterface)
DEF_INTERFACE(UTeamDropBoxInterface)
DEF_INTERFACE_END()


KBE_BEGIN_ENTITY_METHOD_MAP(TeamDropBox, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(TeamDropBox, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

TeamDropBox::TeamDropBox()
{
	_fActorName = FString("TeamDropBox");
}

TeamDropBox::~TeamDropBox()
{
}


void TeamDropBox::OnEnterWorld()
{
	Supper::OnEnterWorld();
}

void TeamDropBox::OnLeaveWorld()
{
	Supper::OnLeaveWorld();
}

UClass* TeamDropBox::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_TeamDropBox")); 
}