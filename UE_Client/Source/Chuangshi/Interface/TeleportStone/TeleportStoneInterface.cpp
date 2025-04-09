// Fill out your copyright notice in the Description page of Project Settings.


#include "TeleportStoneInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/Role/RoleTeleportInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/TeleportPointData.h"
#include "Manager/CfgManager.h"
#include "CS3Base/GameObject.h"
#include "Util/GolbalBPFunctionLibrary.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(UTeleportStoneInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UTeleportStoneInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()


UTeleportStoneInterface::UTeleportStoneInterface()
{
}

UTeleportStoneInterface::~UTeleportStoneInterface()
{

}

void UTeleportStoneInterface::OnRep_modelNumber()
{
	Supper::OnRep_modelNumber();
}

void UTeleportStoneInterface::OnRep_modelScale()
{
	Supper::OnRep_modelScale();
}

void UTeleportStoneInterface::OnEnterTriggerRange()
{
	if (nullptr == GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTeleportStoneInterface::OnEnterTriggerRange:GetEntity()!"));
		return;
	}

	//传送点本来就已经开启
	GameObject* entity = (GameObject*)GetEntity();
	int32 isOpen = (int32)(entity->GetDefinedProperty(TEXT("isOpen")));
	if (isOpen != 0)return;

	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player) || Player->GetSelfEntity() == nullptr)return;
	KBEngine::Entity* PlayerEntity = Player->GetSelfEntity();
	URoleTeleportInterface* roleTeleportInterface = Cast<URoleTeleportInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTeleportInterface"), PlayerEntity->ID()));
	if (nullptr == roleTeleportInterface) return;

	FString scriptID = (FString)(entity->GetDefinedProperty(TEXT("scriptID")));
	const UConfigTable* TeleportPointTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TELEPORT_POINT_DATA);
	TArray<FName> TeleportPointIndexs = TeleportPointTable->GetRowNames();
	for (auto TeleportPointIndex : TeleportPointIndexs)
	{
		//对自己而言，传送点是否已开启
		const FTELEPORT_POINT_DATA* TeleportPoint = TeleportPointTable->GetRow<FTELEPORT_POINT_DATA>(TeleportPointIndex);
		if (scriptID.Equals(TeleportPoint->DstNPCID))
		{
			if (roleTeleportInterface->IsOpen(TeleportPoint->RowName.ToString()))
			{
				return;
			}
			break;
		}
	}

	//等级
	int32 limitLv = (int32)(entity->GetDefinedProperty(TEXT("limitLv")));
	int32 level = (int16)(PlayerEntity->GetDefinedProperty(TEXT("level")));
	if (level < limitLv)return;

	//阵营
	int32 limitCamp = (int32)(entity->GetDefinedProperty(TEXT("limitCamp")));
	int32 camp = (int32)(PlayerEntity->GetDefinedProperty(TEXT("camp")));
	if (limitCamp != camp && limitCamp != 0) return;

	KBEngine::FVariantArray Args;
	GetEntity()->CellCall(TEXT("CELL_onEnterTriggerRange"), Args);
}

void UTeleportStoneInterface::OnLeaveTriggerRange()
{
	
}

