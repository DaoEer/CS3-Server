
#include "GameplayEventManager.h"
#include"Chuangshi.h"

UGameplayEventManager::UGameplayEventManager()
{

}

UGameplayEventManager::~UGameplayEventManager()
{

}

UGameplayEventManager* UGameplayEventManager::GetInstance()
{
	cs3_checkNoReentry();

	return (UGameplayEventManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_GameplayEventManager")));
}

