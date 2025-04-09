
#include "TimeManager.h"
#include "CS3Base/CS3Entity.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CustomTimerManager.h"
#include "Interface/Role/RoleInterface.h"
#include <time.h>
#include"Chuangshi.h"
#include "Util/CS3Debug.h"
#include "CS3Base/GameObject.h"

CONTROL_COMPILE_OPTIMIZE_START
UTimeManager* UTimeManager::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UTimeManager>();
}

FDateTime UTimeManager::GetClientTime()
{
	int64 NowTime = (FDateTime::UtcNow() - FDateTime(1970, 1, 1)).GetTicks();
	int64 clientTime = NowTime - DiffTime;
	return SetTimeToDateTime(clientTime);
}

int64 UTimeManager::GetMultipleClientTime()
{
	int64 NowTime = (FDateTime::UtcNow() - FDateTime(1970, 1, 1)).GetTicks();
	int64 MultipleClientTime = NowTime - DiffTime;
	return MultipleClientTime;
}

bool UTimeManager::ISTimeValid()
{
	return IsValid;
}

FDateTime UTimeManager::ServerTimeToClientTime(const int64& severTime)
{
	int64 clienttime = severTime + DiffTime;
	return SetTimeToDateTime(clienttime);
}

void UTimeManager::SetDiffTime(const FString& serverTime, const int32& severIndex)
{
	if (severIndex != Index)
	{
		IsValid = false;
		return;
	}
	else
	{
		IsValid = true;
	}
	
	int64 valuetime = FSTRING_TO_INT64(serverTime);
	int64 NowTime = (FDateTime::UtcNow() - FDateTime(1970, 1, 1)).GetTicks();
	int64 LastDiffTime = NowTime - valuetime;
	if (LastDiffTime <= -TIME_PERMISSIBLE_ERROR || LastDiffTime >= TIME_PERMISSIBLE_ERROR)
	{
		DiffTime = LastDiffTime;
	}
}

void UTimeManager::VerifyClientTime()
{
	if (GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity())
	{
		if (URoleInterface* RoleInterface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface))
		{
			RoleInterface->verifyClientTime(Index);
		}
	}

	//if (KBEngine::Entity* Player = UUECS3GameInstance::Instance->pKBEApp->Player())
	//{
	//	KBEngine::FVariantArray Args;
	//	Args.Add(Index);
	//	Player->CellCall(TEXT("verifyClientTime"), Args);
	//}
	FTimerHandle VerifyHandle;
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(VerifyHandle, this, &UTimeManager::SetIndex, 1.0f, false);
}

void UTimeManager::OnPlayerEnter()
{
	this->VerifyClientTime();
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(CycleHandle, this, &UTimeManager::VerifyClientTime, MYTICKTIME, true);
}

void UTimeManager::OnPlayerLeave()
{
	DiffTime = 0;
}

void UTimeManager::SetIndex()
{
	++Index;
}

UTimeManager::UTimeManager()
{	

}


UTimeManager::~UTimeManager()
{
}

FDateTime UTimeManager::SetTimeToDateTime(const int64& MulTime)
{
	FDateTime UIDiffTime = FDateTime(1970, 1, 1) + MulTime + ((int64)8 * 3600) * TIME_ENLARGE_MULTIPLE;
	return UIDiffTime;
}
CONTROL_COMPILE_OPTIMIZE_END