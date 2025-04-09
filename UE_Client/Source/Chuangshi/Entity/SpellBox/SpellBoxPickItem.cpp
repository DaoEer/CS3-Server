
#include "SpellBoxPickItem.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Role/RoleSpellBoxDropItemInterface.h"

KBE_BEGIN_ENTITY_METHOD_MAP(SpellBoxPickItem, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBoxPickItem, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

SpellBoxPickItem::SpellBoxPickItem()
{
}

SpellBoxPickItem::~SpellBoxPickItem()
{
}

void SpellBoxPickItem::OnEnterWorld()
{
	Supper::OnEnterWorld();
}

void SpellBoxPickItem::OnLeaveWorld()
{
	URoleSpellBoxDropItemInterface* RoleSpellBoxDropInterface = Cast<URoleSpellBoxDropItemInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleDropBoxInterface"), 0));
	if (IsValid(RoleSpellBoxDropInterface))
	{
		RoleSpellBoxDropInterface->OnSpellBoxPickItemDestroyed(ID());
	}
	Supper::OnLeaveWorld();
}

UClass* SpellBoxPickItem::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBoxPickItem"));
}