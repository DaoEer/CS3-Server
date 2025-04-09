// Fill out your copyright notice in the Description page of Project Settings.


#include "PeadState.h"

#include "GameData/GameDeFine.h"

#include "Actor/ServerCharacter.h"
#include "CS3Base/GameObject.h"
#include "Interface/GameObjectInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

void UPeadState::Enter()
{
	GameObject* GameEntity = (GameObject *)(CurrentEntity);	
	if (GameEntity && !GameEntity->IsPlayer())
	{
		UGameObjectInterface * Interface = Cast<UGameObjectInterface>(
			((GameObject*)GameEntity)->Interface_Cache.GameObjectInterface);
		if (IsValid(Interface)&& Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
		{
			AServerCharacter* ServerCharacter = (AServerCharacter *)CurrentEntity->Actor();
			if (!ServerCharacter)
			{
				CS3_Warning(TEXT("-->Null Pointer error:UPeadState::Enter: ServerCharacter!"));
				return;
			}
			//目前已经不再采用pend状态来处理准备状态的相关处理
			//UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(ServerCharacter);
		}
	}
}

void UPeadState::Execute()
{

}

void UPeadState::Exit()
{
	GameObject* GameEntity = (GameObject *)(CurrentEntity);	
	if (GameEntity && !GameEntity->IsPlayer())
	{
		UGameObjectInterface * Interface = Cast<UGameObjectInterface>(((GameObject*)GameEntity)->Interface_Cache.GameObjectInterface);
		if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
		{
			AServerCharacter* ServerCharacter = (AServerCharacter *)CurrentEntity->Actor();
			if (!ServerCharacter)
			{
				CS3_Warning(TEXT("-->Null Pointer error:UPeadState::Exit: ServerCharacter!"));
				return;
			}
			//目前已经不再采用pend状态来处理准备状态的相关处理
			//UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(ServerCharacter);
		}
	}
}