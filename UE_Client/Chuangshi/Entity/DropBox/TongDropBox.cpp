
#include "TongDropBox.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/DropBox/TongDropBoxInterface.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/NPCBaseObjectInterface.h"

DEF_INTERFACE_BEGIN(TongDropBox, Supper)
DEF_INTERFACE(UGameObjectInterface)
DEF_INTERFACE(UNPCBaseObjectInterface)
DEF_INTERFACE(UTongDropBoxInterface)
DEF_INTERFACE_END()


KBE_BEGIN_ENTITY_METHOD_MAP(TongDropBox, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(TongDropBox, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

TongDropBox::TongDropBox()
{
	_fActorName = FString("TongDropBox");
}

TongDropBox::~TongDropBox()
{
}


void TongDropBox::OnEnterWorld()
{
	Supper::OnEnterWorld();
}

void TongDropBox::OnLeaveWorld()
{
	Supper::OnLeaveWorld();
}

UClass* TongDropBox::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_TongDropBox")); 
}