
#include "MoveTrap.h"
#include "Interface/Trap/MoveTrapInterface.h"

DEF_INTERFACE_BEGIN(MoveTrap, Supper)
DEF_INTERFACE(UMoveTrapInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MoveTrap, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MoveTrap, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MoveTrap::MoveTrap()
{
	_fActorName = FString("MoveTrap");
	//_fCompontentName = FName("UMoveTrapActorComponent");
}

MoveTrap::~MoveTrap()
{
}
