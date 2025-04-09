
#include "RoleAutoFightInterface.h"
#include "KBEngine.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleAutoFightInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleAutoFightInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()


URoleAutoFightInterface::URoleAutoFightInterface()
{
}


URoleAutoFightInterface::~URoleAutoFightInterface()
{
}

void URoleAutoFightInterface::AddSkillOnList(int32 skillKey, int32 skillID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleAutoFightInterface::AddSkillOnList no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(skillKey);
	args.Add(skillID);
	entity->CellCall(TEXT("CELL_addSkillOnList"), args);
}

void URoleAutoFightInterface::RemoveSkillOnListByKey(int32 skillKey)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleAutoFightInterface::RemoveSkillOnListByKey no this Entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(skillKey);
	entity->CellCall(TEXT("CELL_removeSkillOnList"), args);
}


