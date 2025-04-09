// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleCommanderInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CMonsterInterface.h"
#include "Entity/Monster/CMonster.h"
#include "MonsterAI/MonsterAIController.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MonsterAI/MonsterAIEnum.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/SkillInterface.h"
#include "Manager/CfgManager.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Runtime/NavigationSystem/Public/NavigationSystem.h"
#include "Manager/EventManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/UIManager.h"
#include "GameData/EnumCsvDefine.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(URoleCommanderInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RoleRemoveSoldier, &URoleCommanderInterface::RoleRemoveSoldier, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RoleCmdOnControlled, &URoleCommanderInterface::RoleCmdOnControlled, const FString& , const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RoleDestroyArms, &URoleCommanderInterface::RoleDestroyArms)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RoleCmdUseSkillToPosition, &URoleCommanderInterface::RoleCmdUseSkillToPosition, const int32&, const FVector&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RoleCmdUseSkillToEntity, &URoleCommanderInterface::RoleCmdUseSkillToEntity, const int32&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RoleCmdUseSkillToSelf, &URoleCommanderInterface::RoleCmdUseSkillToSelf, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitRoleCmdArmsScriptID, &URoleCommanderInterface::InitRoleCmdArmsScriptID, const FString&, const FString&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowRoleCmdUI, &URoleCommanderInterface::ShowRoleCmdUI, const uint8&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(RoleCmdClimb, &URoleCommanderInterface::RoleCmdClimb)

CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleCommanderInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()


void URoleCommanderInterface::InitBlueCB()
{
	//ArrBlueFunc.Add("ShowRoleCmdUI");
	Supper::InitBlueCB();
}

void URoleCommanderInterface::ShowRoleCmdUI(const uint8& isShow)
{
	if (isShow)
	{
		if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
		{
			UBaseWindow* guardSoldierInfo = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("GuardSoldierInfoWidget"));
			if (!IsValid(guardSoldierInfo))
			{
				UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::InWorld, TEXT("GuardSoldierInfoWidget"));
			}
		}
	}
	else
	{
		if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
		{
			UBaseWindow* guardSoldierInfo = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("GuardSoldierInfoWidget"));
			if (IsValid(guardSoldierInfo))
			{
				guardSoldierInfo->Destroy();
			}

		}
	}
}

void URoleCommanderInterface::InitSoldierFollow(int32 entityID)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player)) { return; }

	CMonster* pCMonster = (CMonster*)(UGolbalBPFunctionLibrary::FindEntity(entityID));
	if (!pCMonster)
	{
		return;
	}

	const FCLIENT_MOSNTER_AI_DATA* data = GetClientMonsterAIConfig(ArmsData.SoldierScriptID);
	//初始化 层数 层间距 等分角
	float Distance = data->Follow.FollowSpace;
	float Extension = data->Follow.FollowStartDist; //起始距离
	int32 IndexMax = (int32)data->Follow.FollowMaxIndex;


	FVector CenterPos = Player->GetActorLocation();
	//用FloorTrace在多层导航的时候返回位置不对 返回的是下层导航的位置
	//CenterPos = Player->FloorTrace(CenterPos);
	CenterPos = GetVerticalPos(CenterPos).IsZero()? Player->FloorTrace(CenterPos): GetVerticalPos(CenterPos);

	FRotator TargetRotator = Player->GetActorRotation();

	int32 ArmIndex = ArmsData.SoldierEntityIDList.IndexOfByKey(entityID);
	FVector TargetPos;
	FVector RelativePos;
	CalcInitSoldierFollow(Distance, Extension, IndexMax, ArmIndex, CenterPos, TargetPos, RelativePos, TargetRotator);

	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(pCMonster->Actor());
	pCMonster->SoldierCmdFollowUpdate(TargetPos, CenterPos, RelativePos, TargetRotator);
}

void URoleCommanderInterface::CalcInitSoldierFollow(const float& Distance, const float& Extension, const int32& IndexMax, const int32& ArmIndex, const FVector& CenterPos, FVector& TargetPos, FVector& RelativePos, const FRotator& TargetRotator)
{
	int LeftDist = IndexMax / 2 * Distance;
	int32 Layer = 0;
	int32 Index = 0;

	float radian = FMath::DegreesToRadians(TargetRotator.Yaw);
	FVector2D vCenter = FVector2D(CenterPos.X, CenterPos.Y);
	FVector2D vDir = FVector2D(FMath::Cos(radian), FMath::Sin(radian));
	FVector2D vForward = vDir.GetRotated(180);
	FVector2D vLeft = vDir.GetRotated(-90);
	FVector2D vRight = vDir.GetRotated(90);
	FVector2D vBase = vForward * Extension + vLeft * LeftDist;

	int32 Num = ArmIndex + 1;
	Index = Num % IndexMax ? Num % IndexMax - 1 : IndexMax - 1;

	Layer = Num % IndexMax ? Num / IndexMax + 1 : Num / IndexMax;
	Layer--;

	FVector2D vTarget = (vForward * Layer + vRight * Index) * Distance + vBase;
	RelativePos = FVector(vTarget.X, vTarget.Y, 0);
	TargetPos = CenterPos + RelativePos;

	FVector newPos = GetVerticalPos(TargetPos);
	if (newPos.IsZero())
	{
		bool bFind = false;
		if (Index < IndexMax / 2)
		{
			for (int i = IndexMax + Index; i >= IndexMax; i--)
			{
				vTarget = (vForward * Layer + vRight * i) * Distance + vBase;
				RelativePos = FVector(vTarget.X, vTarget.Y, 0);
				newPos = CenterPos + RelativePos;
				newPos = GetVerticalPos(newPos);
				if (!newPos.IsZero())
				{
					TargetPos = newPos;
					bFind = true;
					break;
				}
			}
		}
		else if (Index > IndexMax / 2)
		{
			for (int i = Index - IndexMax; i < 0; i++)
			{
				vTarget = (vForward * Layer + vRight * i) * Distance + vBase;
				RelativePos = FVector(vTarget.X, vTarget.Y, 0);
				newPos = CenterPos + RelativePos;
				newPos = GetVerticalPos(newPos);
				if (!newPos.IsZero())
				{
					TargetPos = newPos;
					bFind = true;
					break;
				}
			}
		}

		if (!bFind)
		{
			if (UNavigationSystemV1::NavigationRaycast(this, CenterPos, TargetPos, newPos))
			{
				TargetPos = newPos;
				bFind = true;
			}
		}
	}
}

void URoleCommanderInterface::ResetGuardFollow(int32 entityID)
{
	float angle;
	if (ArmsData.LeftGuardEntityID == entityID)
	{
		angle = -90;
	}
	else if (ArmsData.RightGuardEntityID == entityID)
	{
		angle = 90;
	}
	else
	{
		return;
	}

	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player)) { return; }
	
	FRotator TargetRotator = Player->GetActorRotation();
	float Distance = FollowSpace;
	float radian = FMath::DegreesToRadians(TargetRotator.Yaw);
	FVector2D vDir = FVector2D(FMath::Cos(radian), FMath::Sin(radian));
	FVector2D vLeft = vDir.GetRotated(angle)*Distance;
	FVector RelativePos = FVector(vLeft.X, vLeft.Y, 0.0);
	FVector CenterPos = Player->GetActorLocation();
	//CenterPos = Player->FloorTrace(CenterPos);
	CenterPos = GetVerticalPos(CenterPos).IsZero() ? Player->FloorTrace(CenterPos) : GetVerticalPos(CenterPos);
	FVector TargetPos = CenterPos + RelativePos;
	//TargetPos = Player->FloorTrace(TargetPos);
	CMonster* pCMonster = (CMonster*)(UGolbalBPFunctionLibrary::FindEntity(entityID));
	if (pCMonster)
	{
		pCMonster->SoldierCmdFollowUpdate(TargetPos, CenterPos, RelativePos, TargetRotator);
	}
}


void URoleCommanderInterface::SoldierFollow()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player)) { return; }

	
	const FCLIENT_MOSNTER_AI_DATA* data = GetClientMonsterAIConfig(ArmsData.SoldierScriptID);

	//初始化 层数 层间距 等分角
	float Distance = data->Follow.FollowSpace;
	float Extension = data->Follow.FollowStartDist; //起始距离
	int IndexMax = data->Follow.FollowMaxIndex;

	FVector CenterPos = Player->GetActorLocation();
	//CenterPos = Player->FloorTrace(CenterPos);
	CenterPos = GetVerticalPos(CenterPos).IsZero() ? Player->FloorTrace(CenterPos) : GetVerticalPos(CenterPos);
	FRotator TargetRotator = Player->GetActorRotation();

	FVector TargetPos;
	FVector RelativePos;

	for (auto& entityID: ArmsData.SoldierEntityIDList)
	{
			KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(entityID);
			if (pEntity)
			{
				CMonster* pCMonster = static_cast<CMonster*>(pEntity);
				if (pCMonster)
				{
					int32 ArmIndex = ArmsData.SoldierEntityIDList.IndexOfByKey(entityID);
					CalcInitSoldierFollow(Distance, Extension, IndexMax, ArmIndex, CenterPos, TargetPos, RelativePos, TargetRotator);
					pCMonster->SoldierCmdFollowUpdate(TargetPos, CenterPos, RelativePos, TargetRotator);
				}
			}
		}
	

}

void URoleCommanderInterface::SoldierFormationRect()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player)) { return; }

	const FCLIENT_MOSNTER_AI_DATA* data = GetClientMonsterAIConfig(ArmsData.SoldierScriptID);
	//初始化 当前行数 当前列数 每行最大列数
	int Layer = 1;
	float Distance = data->Formations.Find(MONSTER_AI_FORMATION::Rectangle)->FollowSpace;
	float Extension = data->Formations.Find(MONSTER_AI_FORMATION::Rectangle)->FollowStartDist; //起始距离
	int IndexMax = data->Formations.Find(MONSTER_AI_FORMATION::Rectangle)->FollowMaxIndex;
	int Index = 0;
	int Total = ArmsData.SoldierEntityIDList.Num();
	Layer = Total % IndexMax ? Total / IndexMax : Total / IndexMax - 1;


	FVector TargetPos;
	FVector RelativePos;
	int LeftDist = IndexMax / 2 * Distance;

	FVector CenterPos = Player->GetActorLocation();
	//CenterPos = Player->FloorTrace(CenterPos);
	CenterPos = GetVerticalPos(CenterPos).IsZero() ? Player->FloorTrace(CenterPos) : GetVerticalPos(CenterPos);
	FRotator TargetRotator = Player->GetActorRotation();
	float radian = FMath::DegreesToRadians(TargetRotator.Yaw);
	FVector2D vCenter = FVector2D(CenterPos.X, CenterPos.Y);
	FVector2D vDir = FVector2D(FMath::Cos(radian), FMath::Sin(radian));
	FVector2D vForward = vDir;
	FVector2D vLeft = vDir.GetRotated(-90);
	FVector2D vRight = vDir.GetRotated(90);
	FVector2D vBase = vForward * Extension + vLeft * LeftDist;
	for (auto& entityID : ArmsData.SoldierEntityIDList)
	{
		KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(entityID);
		if (pEntity)
		{
			CMonster* pCMonster = static_cast<CMonster*>(pEntity);
			if (pCMonster)
			{
				FVector2D vTarget = (vForward*Layer + vRight * Index)*Distance + vBase;
				RelativePos = FVector(vTarget.X, vTarget.Y, 0);
				TargetPos = CenterPos + RelativePos;
				//TargetPos = Player->FloorTrace(TargetPos);
				FVector newPos = GetVerticalPos(TargetPos);
				if (newPos.IsZero())
				{
					bool isFind = false;
					for (int newLayer = Layer; newLayer >= -6; newLayer--)
					{
						vTarget = (vForward*newLayer + vRight * Index)*Distance + vBase;

						if (!GetVerticalPos(CenterPos + FVector(vTarget.X, vTarget.Y, 0)).IsZero())
						{
							RelativePos = FVector(vTarget.X, vTarget.Y, 0);
							TargetPos = CenterPos + RelativePos;
							isFind = true;
							break;
						}
						if (Index <= IndexMax / 2)
						{
							for (int newIndex = IndexMax + Index; newIndex >= IndexMax; newIndex--)
							{
								vTarget = (vForward*newLayer + vRight * newIndex)*Distance + vBase;
								RelativePos = FVector(vTarget.X, vTarget.Y, 0);
								newPos = CenterPos + RelativePos;
								newPos = GetVerticalPos(newPos);
								if (!newPos.IsZero())
								{
									TargetPos = newPos;
									isFind = true;
									break;
								}
							}
						}
						else if (Index >= IndexMax / 2)
						{
							for (int newIndex = Index - IndexMax; newIndex < 0; newIndex++)
							{
								vTarget = (vForward*newLayer + vRight * newIndex)*Distance + vBase;
								RelativePos = FVector(vTarget.X, vTarget.Y, 0);
								newPos = CenterPos + RelativePos;
								newPos = GetVerticalPos(newPos);
								if (!newPos.IsZero())
								{
									TargetPos = newPos;
									isFind = true;
									break;
								}
							}
						}					
						if (isFind)	break;
					}
				}

				pCMonster->SoldierCmdFormationUpdate(MONSTER_AI_FORMATION::Rectangle, TargetPos, TargetRotator);

				Index++;
				if (Index == IndexMax)
				{
					Layer--;
					Index = 0;
				}
			}
		}
	}
}

void URoleCommanderInterface::SoldierFormationCircle()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player)) { return; }

	const FCLIENT_MOSNTER_AI_DATA* data = GetClientMonsterAIConfig(ArmsData.SoldierScriptID);
	//初始化 层数 层间距 等分角
	int Layer = 1;
	float Distance = data->Formations.Find(MONSTER_AI_FORMATION::Circle)->FollowSpace;
	float Extension = data->Formations.Find(MONSTER_AI_FORMATION::Circle)->FollowStartDist; //起始距离
	int IndexMax = data->Formations.Find(MONSTER_AI_FORMATION::Circle)->FollowMaxIndex;
	int Index = 0;
	float Radian = FMath::DegreesToRadians(360.0 / IndexMax);

	FVector CenterPos = Player->GetActorLocation();
	//CenterPos = Player->FloorTrace(CenterPos);
	CenterPos = GetVerticalPos(CenterPos);
	FRotator TargetRotator;
	float CenterYaw = FMath::DegreesToRadians(Player->GetActorRotation().Yaw);
	FVector TargetPos;
	FVector RelativePos;

	int Total = ArmsData.SoldierEntityIDList.Num();

	Layer = Total % IndexMax ? Total / IndexMax : Total / IndexMax - 1;

	for (auto& entityID : ArmsData.SoldierEntityIDList)
	{
		KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(entityID);
		if (pEntity)
		{
			CMonster* pCMonster = static_cast<CMonster*>(pEntity);
			if (pCMonster)
			{
				float _Radian = Radian * (0.5*(Layer % 2) + Index) + CenterYaw;

				float X = FMath::Cos(_Radian)*(Layer*Distance + Extension);
				float Y = FMath::Sin(_Radian)*(Layer*Distance + Extension);
				RelativePos = FVector(X, Y, 0);
				TargetPos = CenterPos + RelativePos;
				TargetRotator = FRotator(0.0, FMath::RadiansToDegrees(_Radian), 0.0);

				if (GetVerticalPos(TargetPos).IsZero())
				{
					for (int i = Layer-1; i >= 0; i--)
					{
						_Radian = Radian * (0.5*(i % 2) + Index) + CenterYaw;

						X = FMath::Cos(_Radian)*(i*Distance + Extension);
						Y = FMath::Sin(_Radian)*(i*Distance + Extension);
						RelativePos = FVector(X, Y, 0);
						TargetPos = CenterPos + RelativePos;
						TargetRotator = FRotator(0.0, FMath::RadiansToDegrees(_Radian), 0.0);
						//TargetPos = Player->FloorTrace(TargetPos);
						if (!GetVerticalPos(TargetPos).IsZero())
						{
							break;
						}
					}
				}

				pCMonster->SoldierCmdFormationUpdate(MONSTER_AI_FORMATION::Circle, TargetPos, TargetRotator);
				Index++;
				if (Index == IndexMax)
				{
					Layer--;
					Index = 0;
				}
			}
		}
	}
}

void URoleCommanderInterface::SoldierAttack()
{
	for (auto& entityID : ArmsData.SoldierEntityIDList)
	{
		KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(entityID);
		if (pEntity)
		{
			CMonster* pCMonster = static_cast<CMonster*>(pEntity);
			if (pCMonster)
			{
				pCMonster->SoldierCmdAttackUptate();
			}
		}

	}
}

void URoleCommanderInterface::GuardFollow()
{
	ResetGuardFollow(ArmsData.LeftGuardEntityID);
	ResetGuardFollow(ArmsData.RightGuardEntityID);
}

void URoleCommanderInterface::GuardAttack()
{
	CMonster* pCMonster;
	pCMonster = (CMonster*)UGolbalBPFunctionLibrary::FindEntity(ArmsData.LeftGuardEntityID);
	if (pCMonster)
	{
		pCMonster->SoldierCmdAttackUptate();
	}

	pCMonster = (CMonster*)UGolbalBPFunctionLibrary::FindEntity(ArmsData.RightGuardEntityID);
	if (pCMonster)
	{
		pCMonster->SoldierCmdAttackUptate();
	}
}

FVector URoleCommanderInterface::GetVerticalPos(FVector Pos)
{
	FNavLocation ProjectLoc;
	UNavigationSystemV1 *const NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());
	bool bProjectedLocationValid = NavSys->ProjectPointToNavigation(Pos, ProjectLoc);
	if (bProjectedLocationValid)
	{
		return ProjectLoc.Location;
	}
	return FVector::ZeroVector;
}

const FCLIENT_MOSNTER_AI_DATA* URoleCommanderInterface::GetClientMonsterAIConfig(FString scriptID)
{
	if (MonsterAIDatas == nullptr)
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		MonsterAIDatas = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MONSTER_BTREE);
	}
	
	const FCLIENT_MOSNTER_AI_DATA* data = MonsterAIDatas->GetRow<FCLIENT_MOSNTER_AI_DATA>(scriptID);
	return data;
}


void URoleCommanderInterface::RoleCmdOnControlled(const FString& ScriptID, const int32& entityID)
{
	CMonster* pCMonster = (CMonster*)UGolbalBPFunctionLibrary::FindEntity(entityID);
	if (!pCMonster)
	{
		return;
	}
	UCSkillInterface* CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), entityID));
	if (!IsValid(CSkillInterface))
	{
		return;
	}
	
	uint8 category = pCMonster->GetDefinedProperty(TEXT("category"));
	const FCLIENT_MOSNTER_AI_DATA* data = GetClientMonsterAIConfig(ScriptID);

	if (ScriptID == ArmsData.LeftGuardScriptID && category == FSoldierCategory::LeftGuard)
	{
		ArmsData.LeftGuardEntityID = entityID;
		ResetGuardFollow(entityID);
	}
	else if (ScriptID == ArmsData.RightGuardScriptID && category == FSoldierCategory::RightGuard)
	{
		ArmsData.RightGuardEntityID = entityID;
		ResetGuardFollow(entityID);
	}
	else if(ScriptID == ArmsData.SoldierScriptID && category == FSoldierCategory::Sodier)
	{
		ArmsData.SoldierEntityIDList.AddUnique(entityID);
		InitSoldierFollow(entityID);
	}
	if (data != nullptr)
	{
		pCMonster->InitRemoteAttr(data->isRemote);
		if (data->initBuffID != 0)
		{
			CSkillInterface->addBuff(pCMonster, data->initBuffID);
		}
	}
	
	if (!IsValid(UUECS3GameInstance::Instance))
		return;
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRoleCmdControlled.Broadcast(category, ScriptID, entityID);
	}
}

void URoleCommanderInterface::RoleDestroyArms()
{
	ArmsData.Reset();
}




void URoleCommanderInterface::CommandFollow() 
{
	SoldierFollow();
	GuardFollow();
}


void URoleCommanderInterface::CommandAttack()
{
	SoldierAttack();
	GuardAttack();
}

void URoleCommanderInterface::CommandUseSkill()
{
	USkillInterface* SkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(Player))
	{
		AServerCharacter* Target = Player->CurPlayerTarget;
		int32 TargetID = IsValid(Target) ? Target->EntityId : 0;
		if (!SoldierMonsterAIData)
		{
			return;
		}
		SkillInterface->UseSkill(SoldierMonsterAIData->CmdSkillID, TargetID);
	}

}

void URoleCommanderInterface::CommandArrayRectangle()
{
	SoldierFormationRect();
}

void URoleCommanderInterface::CommandArrayCircle()
{
	SoldierFormationCircle();

}

void URoleCommanderInterface::CmdUseSkillToPosition(int32 SkillID, FVector TargetPos)
{
	for (auto& entityID : ArmsData.SoldierEntityIDList)
	{
		KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(entityID);
		if (pEntity) {
			CMonster* pCMonster = static_cast<CMonster*>(pEntity);
			if (pCMonster) {
				UCSkillInterface* skillIntf = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), entityID));
				if (!IsValid(skillIntf))
				{
					return;
				}

				if (skillIntf->isCastingSkill())
				{
					skillIntf->interruptSkill((int32)SKILL_MESSAGE::SKILL_AI_INTERRUPT);
				}
				skillIntf->useCSkillToPosition(SkillID,TargetPos);
					
			}
		}
	}
}

void URoleCommanderInterface::CmdUseSkillToEntity(int32 SkillID, int32 TargetID)
{
	for (auto& entityID : ArmsData.SoldierEntityIDList)
	{
		KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(entityID);
		if (pEntity) {
			CMonster* pCMonster = static_cast<CMonster*>(pEntity);
			if (pCMonster) {
				UCSkillInterface* skillIntf = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), entityID));
				if (!IsValid(skillIntf))
				{
					return;
				}

				if (skillIntf->isCastingSkill())
				{
					skillIntf->interruptSkill((int32)SKILL_MESSAGE::SKILL_AI_INTERRUPT);
				}
				skillIntf->useCSkillToEntity(SkillID, TargetID);

			}
		}
	}
}

void URoleCommanderInterface::CmdUseSkillToSelf(int32 SkillID)
{
	for (auto& entityID : ArmsData.SoldierEntityIDList)
	{
		KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(entityID);
		if (pEntity) {
			CMonster* pCMonster = static_cast<CMonster*>(pEntity);
			if (pCMonster) {
				UCSkillInterface* skillIntf = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), entityID));
				if (!IsValid(skillIntf))
				{
					return;
				}

				if (skillIntf->isCastingSkill())
				{
					skillIntf->interruptSkill((int32)SKILL_MESSAGE::SKILL_AI_INTERRUPT);
				}
				skillIntf->useCSkillToEntity(SkillID, entityID);
			}
		}	
	}
}

void URoleCommanderInterface::CmdClimb()
{
	TArray<int32> entityIDList;
	entityIDList.Append(ArmsData.SoldierEntityIDList);
	entityIDList.Add(ArmsData.LeftGuardEntityID);
	entityIDList.Add(ArmsData.RightGuardEntityID);

	for (auto& entityID : entityIDList)
	{
		KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(entityID);
		if (pEntity) {
			CMonster* pCMonster = static_cast<CMonster*>(pEntity);
			if (pCMonster) {
				AMonsterCharacter* monsterCharacter = Cast<AMonsterCharacter>(pCMonster->Actor());
				if (IsValid(monsterCharacter))
				{
					AMonsterAIController* controller = Cast<AMonsterAIController>(monsterCharacter->GetController());
					if (IsValid(controller))
					{
						controller->blackboardComponent->SetValueAsEnum(FName("CurrCmd"), uint8(MONSTER_AI_COMMAND::CLIMB));
					}
				}
			}
		}
	}
}


void URoleCommanderInterface::RoleCmdUseSkillToPosition(const int32& SkillID, const FVector& TargetPos)
{
	CmdUseSkillToPosition(SkillID, TargetPos);
}

void URoleCommanderInterface::RoleCmdUseSkillToEntity(const int32& SkillID, const int32& TargetID)
{
	CmdUseSkillToEntity(SkillID,TargetID);
}

void URoleCommanderInterface::RoleCmdUseSkillToSelf(const int32& SkillID)
{
	CmdUseSkillToSelf(SkillID);
}

void URoleCommanderInterface::InitRoleCmdArmsScriptID(const FString& leftGuardScriptID, const FString& rightGuardScriptID, const FString& soldierScriptID)
{
	ArmsData.Reset();
	ArmsData.LeftGuardScriptID = leftGuardScriptID;
	ArmsData.RightGuardScriptID = rightGuardScriptID;
	ArmsData.SoldierScriptID = soldierScriptID;

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	SoldierMonsterAIData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MONSTER_BTREE)->GetRow<FCLIENT_MOSNTER_AI_DATA>(soldierScriptID);
}

void URoleCommanderInterface::RoleRemoveSoldier(const int32& soldierID)
{
	if (soldierID == ArmsData.LeftGuardEntityID)
	{
		ArmsData.LeftGuardScriptID = "";
		ArmsData.LeftGuardEntityID = 0;
	}
	else if (soldierID==ArmsData.RightGuardEntityID)
	{
		ArmsData.RightGuardScriptID = "";
		ArmsData.RightGuardEntityID = 0;
	}
	else if(ArmsData.SoldierEntityIDList.Contains(soldierID))
	{
		ArmsData.SoldierEntityIDList.Remove(soldierID);
	}
	if (!IsValid(UUECS3GameInstance::Instance))
		return;
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRoleRemoveSoldier.Broadcast(soldierID);
	}
}

void URoleCommanderInterface::RoleCmdClimb()
{
	CmdClimb();
}

