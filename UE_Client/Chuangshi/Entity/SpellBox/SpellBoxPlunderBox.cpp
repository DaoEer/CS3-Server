
#include "SpellBoxPlunderBox.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Role/RoleSpellBoxDropItemInterface.h"

KBE_BEGIN_ENTITY_METHOD_MAP(SpellBoxPlunderBox, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBoxPlunderBox, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

SpellBoxPlunderBox::SpellBoxPlunderBox()
{
}

SpellBoxPlunderBox::~SpellBoxPlunderBox()
{
}

void SpellBoxPlunderBox::OnEnterWorld()
{
	Supper::OnEnterWorld();
}

void SpellBoxPlunderBox::OnLeaveWorld()
{
	URoleSpellBoxDropItemInterface* RoleSpellBoxDropInterface = Cast<URoleSpellBoxDropItemInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleDropBoxInterface"), 0));
	if (IsValid(RoleSpellBoxDropInterface))
	{
		RoleSpellBoxDropInterface->OnSpellBoxPickItemDestroyed(ID());
	}
	Supper::OnLeaveWorld();
}

UClass* SpellBoxPlunderBox::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBoxPlunderBox"));
}