// Fill out your copyright notice in the Description page of Project Settings.

#include "MonsterOwnerInterface.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Dom/JsonValue.h"
#include "Json.h"
#include "Interface/Role/RoleTeamInterface.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterOwnerInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterOwnerInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
UMonsterOwnerInterface::UMonsterOwnerInterface()
{
	bootOwnerList.Empty();
	bootOwnerIDList.Empty();
}

UMonsterOwnerInterface::~UMonsterOwnerInterface(){}


bool UMonsterOwnerInterface::PlayerIsOwner()
{
	int playerID = UGolbalBPFunctionLibrary::GetPlayerID();
	URoleTeamInterface* interface = Cast<URoleTeamInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTeamInterface"), playerID));
	for (auto inst : bootOwnerList) 
	{
		if (inst.type == 1)	//¸öÈË
		{
			if (CheckOwner(1, playerID))
				return true;
		}
		else if (inst.type == 2)//¶ÓÎé
		{
			if (interface != nullptr && CheckOwner(2, interface->Team_ID))
				return true;
		}
		else if (inst.type == 3)
		{
		}
	}
	return false;
}

void UMonsterOwnerInterface::CLIENT_OnSetBootyOwner_Implementation(const FString& data)
{
	bootOwnerList.Empty();
	bootOwnerIDList.Empty();
	TSharedRef<TJsonReader<TCHAR>> jsonReader = TJsonReaderFactory<TCHAR>::Create(data);
	TSharedPtr<FJsonValue> jsonParsed;
	TSharedPtr<FJsonObject> jsonObject;
	bool BFlag = FJsonSerializer::Deserialize(jsonReader, jsonParsed);
	if (BFlag)
	{
		for (auto& jsonValue : jsonParsed->AsArray())
		{
			FBootOwnerData inst;
			jsonObject = jsonValue->AsObject();
			inst.type = jsonObject->GetIntegerField("type");
			inst.ownerID = jsonObject->GetIntegerField("owner");
			bootOwnerList.Add(inst);
			bootOwnerIDList.Add(inst.ownerID);
		}
	}
	AMonsterCharacter* actor = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(actor))
	{
		actor->OnMonsterBootyOwnerChangedBP();
	}
	if (OnSetBootyOwnerAssist.IsBound())
	{
		OnSetBootyOwnerAssist.Broadcast(EntityID);
	}
}


bool UMonsterOwnerInterface::CheckOwner(int32 type, int32 id)
{
	for (FBootOwnerData& data : bootOwnerList)
	{
		if (data.type == type && data.ownerID == id)
			return true;
	}
	return false;
}

bool UMonsterOwnerInterface::hasOwner()
{
	return bootOwnerIDList.Num() > 0;
}


void UMonsterOwnerInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnSetBootyOwner");
	Supper::InitBlueCB();
}