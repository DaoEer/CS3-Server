#include "CS3PlayRole.h"
#include "CoreMinimal.h"

#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/LocalDataSaveManager.h"
#include "CS3Base/UIManager.h"
#include "Manager/LoginManager.h"
#include "Interface/Role/PlayerRoleCombatInterface.h"
#include "Interface/Role/GMTestInterface.h"

KBE_BEGIN_ENTITY_METHOD_MAP(CS3PlayRole, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(CS3PlayRole, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

DEF_INTERFACE_BEGIN(CS3PlayRole, Supper)
DEF_INTERFACE(UPlayerRoleCombatInterface)
DEF_INTERFACE(UGMTestInterface)
DEF_INTERFACE_END()


CS3PlayRole::CS3PlayRole()
{
	UUECS3GameInstance::Instance->CS3Player(this);
}

CS3PlayRole::~CS3PlayRole()
{
	UUECS3GameInstance::Instance->CS3Player(nullptr);
}

void CS3PlayRole::__init__()
{
	Supper::__init__();
}

void CS3PlayRole::OnDestroy()
{
	CS3_Log(TEXT("CS3PlayRole::OnDestroy!"));
	Supper::OnDestroy();
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OnRoleLeaveWorld();
	}
	if (IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager))
	{
		UUECS3GameInstance::Instance->LocalDataSaveManager->OnPlayerLeaveWorld();
	}
}

void CS3PlayRole::OnEnterWorld()
{
	CS3_Log( TEXT("CS3PlayRole::OnEnterWorld!"));
	bIsLeavingWorld = false;
	Supper::OnEnterWorld();
	UUECS3GameInstance::Instance->LoginManager->SetLoginStage(ELoginStage::StageRoleLogin);
	UUECS3GameInstance::Instance->LocalDataSaveManager->OnPlayerEnterWorld();
}

void CS3PlayRole::OnLeaveWorld()
{
	CS3_Log(TEXT("CS3PlayRole::OnLeaveWorld!"));
	bIsLeavingWorld = true;
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OnRoleLeaveWorld();
	}
	if (IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager))
	{
		UUECS3GameInstance::Instance->LocalDataSaveManager->OnPlayerLeaveWorld();
	}
	Supper::OnLeaveWorld();
}

void CS3PlayRole::OnLeaveScenes()
{
	Supper::OnLeaveScenes();
	if (!bIsLeavingWorld)
	{
		UnBindActorToEntity();
	}
}
