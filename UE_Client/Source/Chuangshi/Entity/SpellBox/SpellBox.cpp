
#include "SpellBox.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/SpellBox/SpellBoxInterface.h"
#include "Interface/SkillInterface.h"

DEF_INTERFACE_BEGIN(SpellBox, Supper)
DEF_INTERFACE(USpellBoxInterface)
DEF_INTERFACE(USkillInterface)
DEF_INTERFACE_END()


KBE_BEGIN_ENTITY_METHOD_MAP(SpellBox, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBox, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

SpellBox::SpellBox() 
{
	_fActorName = FString("SpellBox");
	//_fCompontentName = FName("USpellBoxActorComponent");
}

SpellBox::~SpellBox()
{
}

UClass* SpellBox::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBox")); 
}

void SpellBox::OnBindActorToEntity()
{
	Supper::OnBindActorToEntity();
}

