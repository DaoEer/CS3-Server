

#include "CMonster.h"

#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MonsterAI/MonsterAIController.h"
#include "Engine/Classes/Engine/EngineTypes.h"
#include "BehaviorTree/BehaviorTree.h"
#include "GameData/ClientMonsterAIData.h"
#include "GameData/EnumCsvDefine.h"
#include "Manager/CfgManager.h"
#include "Interface/StateInterface.h"
#include "GameData/GameDeFine.h"

#include "Interface/Monster/CMonsterInterface.h"
#include "Interface/Monster/CMonsterStateInterface.h"
#include "Interface/Monster/CMonsterCombatInterface.h"
#include "Interface/Monster/CMonsterAIInterface.h"


DEF_INTERFACE_BEGIN(CMonster, Supper)
DEF_INTERFACE(UCMonsterInterface)
DEF_INTERFACE(UCMonsterStateInterface)
DEF_INTERFACE(UCMonsterCombatInterface)
DEF_INTERFACE(UCMonsterAIInterface)
DEF_INTERFACE_END()

CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(CMonster, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(CMonster, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

CMonster::CMonster()
{
	Supper();
	controlEntityID = 0;
}

CMonster::~CMonster()
{
}

void CMonster::__init__()
{
	Supper::__init__();

	FString ScriptID = GetDefinedProperty(TEXT("scriptID"));
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	MonsterAIData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MONSTER_BTREE)->GetRow<FCLIENT_MOSNTER_AI_DATA>(ScriptID);
	const FCLIENT_MOSNTER_AI_DATA* row = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MONSTER_BTREE)->GetRow<FCLIENT_MOSNTER_AI_DATA>(ScriptID);
	if (row && row->BTree)
	{
		InitiativeRange(row->InitiativeRange);
		DistanceControler(row->DistanceControler);
		BehaviorTree(row->BTree);
	}
	controlEntityID = (int32)GetDefinedProperty(TEXT("controlEntityID"));
}

UClass* CMonster::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_CMonster"));
}


void CMonster::OnControlled(bool isControlled)
{
	//controlEntityID = (int32)GetDefinedProperty(TEXT("controlEntityID"));

	if (isControlled && IsValid(Actor()) && AIBTree )
	{
		AMonsterCharacter* mc = Cast<AMonsterCharacter>(Actor());
		mc->AutoPossessAI = EAutoPossessAI::PlacedInWorld;
		mc->AIControllerClass = AMonsterAIController::StaticClass();
		AMonsterAIController* controller = UUECS3GameInstance::Instance->GetWorld()->SpawnActor<AMonsterAIController>(AMonsterAIController::StaticClass());
		controller->SetPawn( mc );
		controller->Possess( mc );
		controller->ControllerEntityID = controlEntityID;

		//准备完成，通知服务器切换状态
		KBEngine::FVariantArray args;
		UStateInterface* StateIns = Cast<UStateInterface>( GetInterfaceByName(TEXT("StateInterface")));
		args.Add(StateIns->CurrentState);
		args.Add(int32( ENTITY_STATE::EntityStateFree ));
		CellCall(TEXT("CState_change"), args);
	}
}


void CMonster::InitRemoteAttr(bool isRemote)
{
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(Actor());
	if (IsValid(MonsterCharacter))
	{
		AMonsterAIController* MonsterAIController = Cast<AMonsterAIController>(MonsterCharacter->GetController());
		if (IsValid(MonsterAIController))
		{
			MonsterAIController->blackboardComponent->SetValueAsBool(FName("IsRemote"), isRemote);
		}
	}
}

void CMonster::InitCmd()
{
	_isExeCmd = false;
}

void CMonster::ReciveControlCMD(MONSTER_AI_COMMAND cmd, KBEngine::FVariantArray args)
{
	_controlCmd = cmd;
	_controlArgs = args;
	InitCmd();
}


bool CMonster::IsControlClient()
{
	if (controlEntityID == 0)
		return false;

	if(controlEntityID == UGolbalBPFunctionLibrary::GetPlayerID() )
		return true;

	return false;
}

CS3Role* CMonster::GetControlRole()
{
	if (controlEntityID == 0)
	{
		controlEntityID = (int32)GetDefinedProperty(TEXT("controlEntityID"));
	}
	if (controlEntityID == 0)
	{
		return nullptr;
	}
	KBEngine::Entity* controlEntity = UGolbalBPFunctionLibrary::FindEntity(controlEntityID);
	if (controlEntity == nullptr)
		return nullptr;
	else
		return static_cast<CS3Role*>(controlEntity);
}

KBEngine::Entity* CMonster::GetControlEntity()
{
	if (controlEntityID == 0)
	{
		controlEntityID = (int32)GetDefinedProperty(TEXT("controlEntityID"));
	}
	if (controlEntityID == 0)
	{
		return nullptr;
	}
	return UGolbalBPFunctionLibrary::FindEntity(controlEntityID);
}

void CMonster::ChangeCMonsterState(ENTITY_STATE NewState)
{
	KBEngine::FVariantArray args;
	UStateInterface* StateIns = Cast<UStateInterface>(GetInterfaceByName(TEXT("StateInterface")));
	args.Add(StateIns->CurrentState);
	args.Add(int32(NewState));
	CellCall(TEXT("CState_change"), args);
}

void CMonster::SoldierCmdFollowUpdate(FVector TargetPos, FVector CenterPos, FVector RelativePos, FRotator Rotation)
{
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(Actor());
	if (IsValid(MonsterCharacter))
	{
		AMonsterAIController* MonsterAIController = Cast<AMonsterAIController>(MonsterCharacter->GetController());
		if (IsValid(MonsterAIController))
		{
			//更新rvo radius
			MonsterCharacter->GetCharacterMovement()->AvoidanceConsiderationRadius = MonsterAIData->Follow.AvoidanceConsiderationRadius;

			MonsterAIController->blackboardComponent->SetValueAsVector(FName("TargetPos"), TargetPos);
			MonsterAIController->blackboardComponent->SetValueAsVector(FName("CenterPos"), CenterPos);
			MonsterAIController->blackboardComponent->SetValueAsVector(FName("RelativePos"), RelativePos);
			MonsterAIController->blackboardComponent->SetValueAsRotator(FName("Rotation"), Rotation);
			MonsterAIController->blackboardComponent->SetValueAsEnum(FName("CurrCmd"), uint8(MONSTER_AI_COMMAND::FOLLOW));
			MonsterAIController->blackboardComponent->SetValueAsFloat(FName("AttackRange"), MonsterAIData->Follow.AttackRange);
			MonsterAIController->blackboardComponent->SetValueAsFloat(FName("SearchRange"), MonsterAIData->Follow.SearchRange);
			//MonsterAIController->blackboardComponent->SetValueAsInt(FName("SkillID"), MonsterAIData->Follow.SkillID);
			InitGroupSkills(MonsterAIData->Follow.SkillID);

			FString ModelID = MonsterAIData->Follow.ModelID;
			if (ModelID != "")
			{
				KBEngine::FVariantArray Args;
				Args.Add(ModelID);
				Args.Add(FString(""));
				Args.Add(FString(""));
				CellCall("RPC_ChangePosture", Args);
			}
		}

	}

}


void CMonster::SoldierCmdFormationUpdate(MONSTER_AI_FORMATION formation, FVector TargetPos, FRotator Rotation)
{
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(Actor());
	if (IsValid(MonsterCharacter))
	{
		AMonsterAIController* MonsterAIController = Cast<AMonsterAIController>(MonsterCharacter->GetController());
		if (IsValid(MonsterAIController))
		{	//更新rvo radius
			MonsterCharacter->GetCharacterMovement()->AvoidanceConsiderationRadius = MonsterAIData->Formations.Find(formation)->AvoidanceConsiderationRadius;

			MonsterAIController->blackboardComponent->SetValueAsVector(FName("TargetPos"), TargetPos);
			MonsterAIController->blackboardComponent->SetValueAsRotator(FName("Rotation"), Rotation);
			MonsterAIController->blackboardComponent->SetValueAsEnum(FName("CurrCmd"), uint8(MONSTER_AI_COMMAND::FORMATION));
			MonsterAIController->blackboardComponent->SetValueAsEnum(FName("CurrFormation"), uint8(formation));
			MonsterAIController->blackboardComponent->SetValueAsFloat(FName("AttackRange"), MonsterAIData->Formations.Find(formation)->AttackRange);
			MonsterAIController->blackboardComponent->SetValueAsFloat(FName("SearchRange"), MonsterAIData->Formations.Find(formation)->SearchRange);
			//MonsterAIController->blackboardComponent->SetValueAsInt(FName("SkillID"), MonsterAIData->Formations.Find(formation)->SkillID);
			InitGroupSkills(MonsterAIData->Formations.Find(formation)->SkillID);

			FString ModelID = MonsterAIData->Formations.Find(formation)->ModelID;
			if (ModelID != "")
			{
				KBEngine::FVariantArray Args;
				Args.Add(ModelID);
				Args.Add(FString(""));
				Args.Add(FString(""));
				CellCall("RPC_ChangePosture", Args);
			}

		}

	}
}

void CMonster::SoldierCmdAttackUptate()
{
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(Actor());
	if (IsValid(MonsterCharacter))
	{
		AMonsterAIController* MonsterAIController = Cast<AMonsterAIController>(MonsterCharacter->GetController());
		if (IsValid(MonsterAIController))
		{
			//更新rvo radius
			MonsterCharacter->GetCharacterMovement()->AvoidanceConsiderationRadius = MonsterAIData->Attack.AvoidanceConsiderationRadius;
			MonsterAIController->blackboardComponent->SetValueAsEnum(FName("CurrCmd"), uint8(MONSTER_AI_COMMAND::ATTACK));
			MonsterAIController->blackboardComponent->SetValueAsFloat(FName("AttackRange"), MonsterAIData->Attack.AttackRange);
			MonsterAIController->blackboardComponent->SetValueAsFloat(FName("SearchRange"), MonsterAIData->Attack.SearchRange);
			//MonsterAIController->blackboardComponent->SetValueAsInt(FName("SkillID"), MonsterAIData->Attack.SkillID);
			InitGroupSkills(MonsterAIData->Attack.SkillID);

			FString ModelID = MonsterAIData->Attack.ModelID;
			if (ModelID != "")
			{
				KBEngine::FVariantArray Args;
				Args.Add(ModelID);
				Args.Add(FString(""));
				Args.Add(FString(""));
				CellCall("RPC_ChangePosture", Args);
			}
		}
	}
}


void CMonster::InitGroupSkills(TArray<int32> Skills)
{
	GroupSkills = Skills;
	GroupSkillIndex = -1;
}

int32 CMonster::GetGroupSkillID()
{
	if (GroupSkillIndex < 0)
	{
		GroupSkillIndex = 0;
	}
	if (GroupSkillIndex < GroupSkills.Num())
	{
		return GroupSkills[GroupSkillIndex];
	}
	
	return 0;
}

void CMonster::onSkillEnd(USkill * skill, bool castResult)
{
	if (GroupSkillIndex>=0)
	{
		GroupSkillIndex++;
		//最后一个组技能
		if (GroupSkillIndex == GroupSkills.Num())
		{
			GroupSkillIndex = -1;
		}
	}
}


CONTROL_COMPILE_OPTIMIZE_END
