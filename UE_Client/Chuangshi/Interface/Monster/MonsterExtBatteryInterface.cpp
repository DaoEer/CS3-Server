// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtBatteryInterface.h"
#include "Manager/CfgManager.h"
#include "Manager/ShapeManager.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"

UMonsterExtBatteryInterface::UMonsterExtBatteryInterface()
{
	
}

void UMonsterExtBatteryInterface::Initiative()
{
	if (KBEngine::Entity* entity_ = GetEntity())
	{
		FString ScriptID = entity_->GetDefinedProperty(TEXT("scriptID"));
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const FMONSTER_DATA* MonsterData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MONSTER)->GetRow<FMONSTER_DATA>(ScriptID);
		if (MonsterData)
		{
			TArray<FString> tempDatas = UGolbalBPFunctionLibrary::SplitString(MonsterData->Param1);
			if (tempDatas.Num() >= 1)
			{
				BatteryEffect = tempDatas[0];
			}
			if (tempDatas.Num() >= 3)
			{
				AmmoType = BATTERY_AMMO_TYPE(FSTRING_TO_INT(tempDatas[2]));
			}

			tempDatas = UGolbalBPFunctionLibrary::SplitString(MonsterData->Param2);
			if (tempDatas.Num() >= 1)
			{
				InputYawScale = FSTRING_TO_FLOAT(tempDatas[0]);
			}
			TArray<FString> PosStrList;
			if (tempDatas.Num() >= 2)
			{
				PosStrList = UGolbalBPFunctionLibrary::SplitString(tempDatas[1], false, TEXT(","));
				if (PosStrList.Num() >= 3)
				{
					CamerLocation = FVector(FSTRING_TO_FLOAT(PosStrList[0]), FSTRING_TO_FLOAT(PosStrList[1]), FSTRING_TO_FLOAT(PosStrList[2]));
				}
			}
			if (tempDatas.Num() >= 3)
			{
				PosStrList = UGolbalBPFunctionLibrary::SplitString(tempDatas[2], false, TEXT(","));
				if (PosStrList.Num() >= 3)
				{
					CamerRotation = FRotator(FSTRING_TO_FLOAT(PosStrList[1]), FSTRING_TO_FLOAT(PosStrList[2]), FSTRING_TO_FLOAT(PosStrList[0]));
				}
			}
			if (tempDatas.Num() >= 4)
			{
				TurnAngle = FSTRING_TO_INT(tempDatas[3]);
			}
			LoadCD = FSTRING_TO_FLOAT(MonsterData->Param3);
			tempDatas = UGolbalBPFunctionLibrary::SplitString(MonsterData->Param4);
			if (tempDatas.Num() >= 1)
			{
				FlySpeed = FSTRING_TO_FLOAT(tempDatas[0]);
				GravityScale = 1.0;
				if (tempDatas.Num() >= 2)
				{
					GravityScale = FSTRING_TO_FLOAT(tempDatas[1]);
				}
			}
			SkillID = FSTRING_TO_INT(MonsterData->Param5);
		}
	}
}

void UMonsterExtBatteryInterface::InitiativeRocket()
{
	if (KBEngine::Entity* entity_ = GetEntity())
	{
		FString ScriptID = entity_->GetDefinedProperty(TEXT("scriptID"));
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const FMONSTER_DATA* MonsterData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MONSTER)->GetRow<FMONSTER_DATA>(ScriptID);
		if (MonsterData)
		{
			TArray<FString> tempDatas = UGolbalBPFunctionLibrary::SplitString(MonsterData->Param1);
			if (tempDatas.Num() >= 1)
			{
				BatteryEffect = tempDatas[0];
			}
			if (tempDatas.Num() >= 4)
			{
				GuidInterval = FSTRING_TO_FLOAT(tempDatas[2]);
				GuidTimer = FSTRING_TO_INT(tempDatas[3]);
			}

			tempDatas = UGolbalBPFunctionLibrary::SplitString(MonsterData->Param2);
			if (tempDatas.Num() >= 1)
			{
				InputYawScale = FSTRING_TO_FLOAT(tempDatas[0]);
			}
			TArray<FString> PosStrList;
			if (tempDatas.Num() >= 2)
			{
				PosStrList = UGolbalBPFunctionLibrary::SplitString(tempDatas[1], false, TEXT(","));
				if (PosStrList.Num() >= 3)
				{
					CamerLocation = FVector(FSTRING_TO_FLOAT(PosStrList[0]), FSTRING_TO_FLOAT(PosStrList[1]), FSTRING_TO_FLOAT(PosStrList[2]));
				}
			}
			if (tempDatas.Num() >= 3)
			{
				PosStrList = UGolbalBPFunctionLibrary::SplitString(tempDatas[2], false, TEXT(","));
				if (PosStrList.Num() >= 3)
				{
					CamerRotation = FRotator(FSTRING_TO_FLOAT(PosStrList[1]), FSTRING_TO_FLOAT(PosStrList[2]), FSTRING_TO_FLOAT(PosStrList[0]));
				}
			}
			if (tempDatas.Num() >= 4)
			{
				TurnAngle = FSTRING_TO_INT(tempDatas[3]);
			}

			LoadCD = FSTRING_TO_FLOAT(MonsterData->Param3);
			tempDatas = UGolbalBPFunctionLibrary::SplitString(MonsterData->Param4);
			if (tempDatas.Num() >= 1)
			{
				FlySpeed = FSTRING_TO_FLOAT(tempDatas[0]);
				GravityScale = 1.0;
				if (tempDatas.Num() >= 2)
				{
					GravityScale = FSTRING_TO_FLOAT(tempDatas[1]);
				}
			}
			tempDatas = UGolbalBPFunctionLibrary::SplitString(MonsterData->Param5);
			if (tempDatas.Num() >= 1)
			{
				SkillID = FSTRING_TO_INT(tempDatas[0]);
				tempDatas.RemoveAt(0);
			}
			for (FString Data : tempDatas)
			{
				PosStrList = UGolbalBPFunctionLibrary::SplitString(Data, false, TEXT(","));
				if (PosStrList.Num() >= 3)
				{
					FirePos.Add(FVector(FSTRING_TO_FLOAT(PosStrList[0]), FSTRING_TO_FLOAT(PosStrList[1]), FSTRING_TO_FLOAT(PosStrList[2])));
				}
			}
		}
	}
}

void UMonsterExtBatteryInterface::AddTrap()
{
	AActor* Monster = GetActor();
	if (!IsValid(Monster))
	{
		return;
	}
	UUECS3GameInstance::Instance->ShapeManager->CreateShape(Monster, this, SHAPE_TYPE::SHPERE, FVector(3, 3, 3), &UMonsterExtBatteryInterface::OnPlayerBeginOverlap, &UMonsterExtBatteryInterface::OnPlayerEndOverlap);

}

void UMonsterExtBatteryInterface::OnPlayerBeginOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(MonsterActor);
}

void UMonsterExtBatteryInterface::OnPlayerEndOverlap()
{
	AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(MonsterActor)) return;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(MonsterActor);
}

void UMonsterExtBatteryInterface::OnRep_operatorID()
{
	int32 NewOperatorID = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("operatorID"));
	if (NewOperatorID)
	{
		OpertorID = NewOperatorID;
		OnObjectOpertionBattery(NewOperatorID);
		if (OpertorID == UGolbalBPFunctionLibrary::GetPlayerID())
		{
			APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			if (!IsValid(PlayerActor)) return;
			PlayerActor->SetOperatorBatteryID(EntityID);
		}
	}
	else if(OpertorID != 0)
	{
		int32 oldID = OpertorID;
		OpertorID = 0;
		OnCancelOperationBattery(oldID);
		if (OpertorID == UGolbalBPFunctionLibrary::GetPlayerID())
		{
			APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			if (!IsValid(PlayerActor)) return;
			PlayerActor->SetOperatorBatteryID(0);
		}
	}
}

void UMonsterExtBatteryInterface::OperationBattery(const int32& EntityID_)
{
	if (UGolbalBPFunctionLibrary::GetPlayerID() != EntityID_)return;
	
	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray param;
		entity_->CellCall(TEXT("CELL_operationBattery"), param);
	}
	
}

void UMonsterExtBatteryInterface::CLIENT_OnSelfOpertionBattery_Implementation(const int32 & Ammo_, const FString & EndTime_)
{
	Ammo = Ammo_;
	//LoadCD = LoadCD_;
	EndTime = EndTime_;
//	FlySpeed = FlySpeed_;
//	Gravity = Gravity_;
}

void UMonsterExtBatteryInterface::OnObjectOpertionBattery_Implementation(const int32 & EntityID_)
{
	OpertorID = EntityID_;
}

void UMonsterExtBatteryInterface::CancelOperationBattery()
{
	if (UGolbalBPFunctionLibrary::GetPlayerID() != OpertorID)return;
	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray param;
		entity_->CellCall(TEXT("CELL_cancelOperationBattery"), param);
	}
}

void UMonsterExtBatteryInterface::OnCancelOperationBattery_Implementation(const int32& EntityID_)
{
	OpertorID = 0;
}

void UMonsterExtBatteryInterface::ProjectBattery(const float& Yaw, const float& Pitch)
{
#if WITH_EDITOR
	Initiative();
#endif // WITH_EDITOR
	if (!CDIsReady())return;
	if (UGolbalBPFunctionLibrary::GetPlayerID() != OpertorID)return;
	if (Ammo <= 0)return;
	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray param;
		param.Add(Yaw);
		param.Add(Pitch);
		entity_->CellCall(TEXT("CELL_projectBattery"), param);
	}
}

void UMonsterExtBatteryInterface::CLIENT_OnProjectBattery_Implementation(const float& Yaw, const float& Pitch)
{
	Ammo -= 1;
	CDTimer = FDateTime::Now() + LoadCD * ETimespan::TicksPerSecond;
	
}

void UMonsterExtBatteryInterface::DelayFire()
{
	AServerCharacter* Character_ = Cast<AServerCharacter>(GetActor());
	if (IsValid(Character_))
	{
		Character_->PlayAction(TEXT("Show_01"));
	}
}

bool UMonsterExtBatteryInterface::CDIsReady()
{
	return FDateTime::Now() >= CDTimer;
}

void UMonsterExtBatteryInterface::ProjectRocketBattery(const float & Yaw)
{
#if WITH_EDITOR
	InitiativeRocket();
#endif // WITH_EDITOR

	if (UGolbalBPFunctionLibrary::GetPlayerID() != OpertorID)return;
	if (Ammo <= 0)return;
	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray param;
		param.Add(Yaw);
		entity_->CellCall(TEXT("CELL_projectRocketBattery"), param);
	}
}

void UMonsterExtBatteryInterface::CLIENT_OnProjectRocketBattery_Implementation(const int32& Index, const float& Yaw)
{
	if (Index == GuidTimer)
	{
		FinishProjectRocketBattery();
	}
}

void UMonsterExtBatteryInterface::FinishProjectRocketBattery_Implementation()
{
	Ammo -= 1;
	CDTimer = FDateTime::Now() + LoadCD * ETimespan::TicksPerSecond;
}

void UMonsterExtBatteryInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnSelfOpertionBattery");
	ArrBlueFunc.Add("CLIENT_OnProjectBattery");
	ArrBlueFunc.Add("CLIENT_OnProjectRocketBattery");
	UMonsterInterface::InitBlueCB();
}