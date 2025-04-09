
#include "DropBox.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/DropBox/DropBoxCharacter.h"
#include "Interface/Role/RoleDropBoxInterface.h"
#include "Interface/DropBox/DropBoxInterface.h"

DEF_INTERFACE_BEGIN(DropBox, Supper)
DEF_INTERFACE(UDropBoxInterface)
DEF_INTERFACE_END()


KBE_BEGIN_ENTITY_METHOD_MAP(DropBox, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(DropBox, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

DropBox::DropBox()
{
	_fActorName = FString("DropBox");
	//_fCompontentName = FName("UDropBoxActorComponent");
}

DropBox::~DropBox()
{
}


void DropBox::OnEnterWorld()
{
	Supper::OnEnterWorld();
}

void DropBox::OnLeaveWorld()
{
	UCS3EntityInterface* BInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleDropBoxInterface"), 0);
	if (IsValid(BInterface))
	{
		URoleDropBoxInterface* RoleDropBoxInterface = Cast<URoleDropBoxInterface>(BInterface);
		if (IsValid(RoleDropBoxInterface))
		{
			RoleDropBoxInterface->OnDropBoxDestroyed(ID());
		}
	}
	Supper::OnLeaveWorld();
}

UClass* DropBox::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_DropBox")); 
}