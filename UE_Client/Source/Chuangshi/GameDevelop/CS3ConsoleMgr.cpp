// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3ConsoleMgr.h"
#include "Manager/LevelManager.h"
#include "Actor/ServerCharacter.h"
#include "Actor/NPC/NPCCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "JsonObjectConverter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/StrToClass.h"
#include "Manager/CfgManager.h"
#include "GenericPlatformFile.h"
#include "StringConv.h"
#include "HAL/FileManagerGeneric.h"
#include "Less.h"
#include "Map.h"
#include "GameFramework/Actor.h"
#include "AssetRegistryModule.h"
#include "ModuleManager.h"
#include "GameData/EffectScreenData.h"
#include "Engine/DataTable.h"
#include "Casts.h"
#include "Kismet/KismetStringLibrary.h"
#include "LandscapeSample.h"
#include "SampleLevelManager.h"
#include "EffectscapeSample.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"
#include "Manager/GameStatus.h"
#include "Manager/StoryManager.h"
#include "CS3Base/UIManager.h"
#include "time.h"
#include "Manager/AudioManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "Component/AppearanceComponent.h"
#include "Manager/VisibleManager.h"
#include "GameData/GameDefault.h"
#include "GameDevelop/CS3PlayerController.h"
#include "AutoTest/AutoTestManager.h"
#include "Manager/TutorialManager.h"
#include "GameData/EffectEmitterData.h"
#include "Actor/Particle/EffectEmitter.h"
#include "Manager/AtkStateMar.h"
#include "Operation/RoleCtrl/RoleCtrlStateMgr.h"
#include "Manager/TextShieldMgr.h"
#include "Manager/MediaPlayerManager.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Component/PhysicsFilterActorComponent.h"
#include "Component/DumbFilterActorComponent.h"
#include "Component/SpringArmComponentEX.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "GameData/CharacterData.h"
#include "Engine/LevelScriptActor.h"
#include "Level/NewCreateRoleLevel.h"
#include "Interface/SkillInterface.h"
#include "Manager/LoginManager.h"
#include "CS3GameInstance.h"
#include "GameData/PlayerLightData.h"
#include "Util/ConvertUtil.h"
#include "Logging/LogSuppressionInterface.h"
#include "Particles/ParticleSystem.h"
#include "Component/Role/RideCarrierComponent.h"
#include "Manager/ParticleManager.h"
#include "Manager/AudioManager.h"


CONTROL_COMPILE_OPTIMIZE_START

// Sets default values for this component's properties
UCS3ConsoleMgr::UCS3ConsoleMgr()
{
	CacheModelIds.Reset(0);
}

void UCS3ConsoleMgr::CS3_CurrGameState()
{
	int32 state = (int32)UUECS3GameInstance::Instance->GameStatus->GetCurrStatus();
	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_GameState CurState = %d"), state);
}

void UCS3ConsoleMgr::CS3_SetScreenPrintLog(bool isToggled /*= true*/, bool isEnabled /*= true*/)
{
	if (isToggled)
		GAreScreenMessagesEnabled = !GAreScreenMessagesEnabled;
	else
		GAreScreenMessagesEnabled = isEnabled;
}

void UCS3ConsoleMgr::CS3_CurrLevel()
{
	ULevelManager* LevelManager = UGolbalBPFunctionLibrary::LevelManager();
	FName CurrLevelName = LevelManager->GetCurrLevelName();
	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_CurrLevel CurrLevel = %s"), *CurrLevelName.ToString());
}

void UCS3ConsoleMgr::CS3_EntityNumber()
{
	int32 NpcNumber = 0;
	int32 MonsterNumber = 0;
	int32 PlayerRoleNumber = 0;
	TArray<AActor*> EntityList = UGolbalBPFunctionLibrary::GetActorsInRange(AServerCharacter::StaticClass(),8000.0f);
	if (EntityList.Num()> 0 )
	{
		for (AActor* EntityNumb : EntityList)
		{
			if (EntityNumb->GetClass()->IsChildOf(ANPCCharacter::StaticClass()))
			{
				NpcNumber += 1;
			}
			else if (EntityNumb->GetClass()->IsChildOf(AMonsterCharacter::StaticClass()))
			{
				MonsterNumber += 1;
			}
			else if (EntityNumb->GetClass()->IsChildOf(APlayerCharacter::StaticClass()))
			{
				PlayerRoleNumber += 1;
			}
		}
	}

	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_EntityNumber NpcNumber = %d, MonsterNumber = %d ,APlayerCharacter = %d"), (NpcNumber), (MonsterNumber), (PlayerRoleNumber));
}

void UCS3ConsoleMgr::CS3_EntityInRange(float Range)
{
	int32 NpcNumber= 0;
	int32 MonsterNumber= 0;
	int32 PlayerRoleNumber= 0;
	TArray<AActor*> EntityList = UGolbalBPFunctionLibrary::GetActorsInRange(AServerCharacter::StaticClass(), Range);
	if (EntityList.Num() > 0)
	{

		for (AActor* EntityNumb : EntityList)
		{
			if (EntityNumb->GetClass()->IsChildOf(ANPCCharacter::StaticClass()))
			{
				NpcNumber += 1;
			}
			else if (EntityNumb->GetClass()->IsChildOf(AMonsterCharacter::StaticClass()))
			{
				MonsterNumber += 1;
			}
			else if (EntityNumb->GetClass()->IsChildOf(APlayerCharacter::StaticClass()))
			{
				PlayerRoleNumber += 1;
			}
		}
	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_EntityNumber NpcNumber = %d, MonsterNumber = %d ,APlayerCharacter = %d"), NpcNumber, MonsterNumber, PlayerRoleNumber);
}

void UCS3ConsoleMgr::CS3_Pos(int32 EntityID)
{

	TArray<AActor*> EntityList = UGolbalBPFunctionLibrary::GetActorsInRange(AServerCharacter::StaticClass(), 8000.0f);
	for (AActor* EntityNumb : EntityList)
	{
		AServerCharacter* CurrEntity = Cast<AServerCharacter>(EntityNumb);
		if (CurrEntity->EntityId == EntityID)
		{
			
			CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_Pos Entity = %d ,%d ,%d"), CurrEntity->GetActorLocation().X, CurrEntity->GetActorLocation().Y, CurrEntity->GetActorLocation().Z);
		}
	}
}

void UCS3ConsoleMgr::CS3_GameActorNumber()
{
	int32 GameActorNumber = 0;
	TArray<AActor*> EntityList = UGolbalBPFunctionLibrary::GetActorsInRange(AServerCharacter::StaticClass(), 8000.0f);
	for (AActor* EntityNumb : EntityList)
	{
			GameActorNumber += 1;
	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_GameActorNumber GameActorNumber = %d"), GameActorNumber);
}

void UCS3ConsoleMgr::CS3_QueryActorVS(int32 entityid)
{
	KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(entityid);
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3ConsoleMgr::CS3_QueryActorVS : entity!"));
		return;
	}
	if (!IsValid(entity->Actor()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3ConsoleMgr::CS3_QueryActorVS : entity->Actor()!"));
		return;
	}
	VISIBLE_STYLE rule = UGolbalBPFunctionLibrary::VisibleManager()->GetModelVisibleStyle(entity->Actor());
	switch (rule)
	{
	case VISIBLE_STYLE::VISIBLE_STYLE_FALSE:
	{
		CS3_Display(CS3DebugType::CL_GM, TEXT("entity[%d]'s Actor can't see"), entityid);
		break;
	}
	case VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT:
	{
		CS3_Display(CS3DebugType::CL_GM, TEXT("entity[%d]'s Actor is translucent"), entityid);
		break;
	}
	case VISIBLE_STYLE::VISIBLE_STYLE_TRUE:
	{
		CS3_Display(CS3DebugType::CL_GM, TEXT("entity[%d]'s Actor can see"), entityid);
		break;
	}
	default:	break;
	}
}

void UCS3ConsoleMgr::CS3_PlayerNumber()
{
	int32 PlayerRoleNumber = 0;
	TArray<AActor*> EntityList = UGolbalBPFunctionLibrary::GetActorsInRange(AServerCharacter::StaticClass(), 8000.0f);
	for (AActor* EntityNumb : EntityList)
	{
		if (EntityNumb->GetClass()->IsChildOf(APlayerCharacter::StaticClass()))
			PlayerRoleNumber += 1;

	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_PlayerNumber PlayerNumber = %d"), PlayerRoleNumber);
}

void UCS3ConsoleMgr::CS3_SwitchFly()
{
	AServerCharacter* Actor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(Actor) && IsValid(Cast<APlayerCharacter>(Actor)))
	{
		Cast<APlayerCharacter>(Actor)->SwitchFly();
	}
}
                                                    

void UCS3ConsoleMgr::CS3_SwitchFish()
{

		if (UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->IsActivateState(EATTACT_STATE::ARDER_FISH_MODE))
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchFishMode(false);
		}
		else
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchFishMode(true);
		}
}

void UCS3ConsoleMgr::CS3_MonsterNumber()
{
	int32 MonsterNumber = 0;
	TArray<AActor*> EntityList = UGolbalBPFunctionLibrary::GetActorsInRange(AServerCharacter::StaticClass(), 8000.0f);
	for (AActor* EntityNumb : EntityList)
	{
		if (EntityNumb->GetClass()->IsChildOf(AMonsterCharacter::StaticClass()))
			MonsterNumber += 1;

	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_MonsterNumber MonsterNumber = %d"), MonsterNumber);
}

void UCS3ConsoleMgr::CS3_NPCNumber()
{
	int32 NpcNumber= 0;
	TArray<AActor*> EntityList = UGolbalBPFunctionLibrary::GetActorsInRange(AServerCharacter::StaticClass(), 8000.0f);
	for (AActor* EntityNumb : EntityList)
	{
		if (EntityNumb->GetClass()->IsChildOf(ANPCCharacter::StaticClass()))
			NpcNumber += 1;

	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_NpcNumber NpcNumber = %d"), NpcNumber);
}

void UCS3ConsoleMgr::CS3_TestCallCell(const int32& entityID, const FString &methodname, const FString& argument)
{
	if (entityID != 0)
	{
		TArray<FString> arguments = UGolbalBPFunctionLibrary::SplitString(argument);
		UGolbalBPFunctionLibrary::CellCall(entityID, methodname, arguments);
	}
}

void UCS3ConsoleMgr::CS3_TestCallClient(const int32& entityID, const FString& methodname, const FString& argument)
{

	if (entityID != 0)
	{
		KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(entityID);
		CS3Entity* implEntity = static_cast<CS3Entity*>(entity);
		if (implEntity)
		{
			if (implEntity->m_interfaceContainer.Num() <= 0)
			{
				CS3_Display(CS3DebugType::CL_GM, TEXT(" ------------m_interfaceContainer is Null: Functionname[%s] "), *methodname);
				return;
			}
			TArray<FVariant> args;
			TArray<FString> arguments = UGolbalBPFunctionLibrary::SplitString(argument);
			for (int i = 0; i < arguments.Num(); i++) {
				args.Add(arguments[i]);
			}
			
			for (auto It = implEntity->m_interfaceContainer.CreateConstIterator(); It; ++It)
			{
				It.Value()->OnRemoteMethodCall(methodname, args );
			}
		}
	}
}


void UCS3ConsoleMgr::CS3_TestCallBase(const int32& entityID, const FString &methodname, const FString& argument)
{
	if (entityID != 0)
	{
		TArray<FString> arguments = UGolbalBPFunctionLibrary::SplitString(argument);
		UGolbalBPFunctionLibrary::BaseCall(entityID, methodname, arguments);
	}
}

void UCS3ConsoleMgr::CS3_TestAsyncLoadAllMesh(const FString& Args)
{
	if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary = NewObject<UObjectLibrary>(UObjectLibrary::StaticClass());
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary->AddToRoot();
	}

	TArray<FString> LoadPartArray;
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	auto ModelPartTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PART_MODEL);
	auto ModelTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_MODEL);

	FString SplitStr = FString(TEXT(";"));
	TArray<FString> ModelSplitArray = UGolbalBPFunctionLibrary::SplitString(Args, true, SplitStr);
	for (auto ModelNumber : ModelSplitArray)
	{
		if (CacheModelIds.Contains(ModelNumber))
		{
			continue;
		}
		CacheModelIds.Add(ModelNumber);

		const FMODEL_DATA* ModelData = ModelTable->GetRow<FMODEL_DATA>(ModelNumber);
		TMap<int, FString> NewPartMap;
		if (ModelData != nullptr)
		{
			for (FPartItem PratItem : ModelData->PartArray)
			{
				NewPartMap.Add((int)PratItem.posType, PratItem.PartID);
			}
		}
		else
		{
			CS3_Warning(TEXT("--------------------ACS3PlayerController::CS3_TestAsyncLoadAllMesh:the ModelNumber[%s] is error!-----------"), *ModelNumber);
			continue;
		}

		for (TPair<int, FString> Part : NewPartMap)
		{
			if (!Part.Value.IsEmpty())
			{
				auto pPartData = ModelPartTable->GetRow<FMODEL_PART_DATA>(Part.Value);
				if (pPartData)
				{
					FString PackageName = pPartData->ModelPartPath.ToSoftObjectPath().GetLongPackageName();
					FString DirName;
					PackageName.Split(TEXT("/"), &DirName, NULL, ESearchCase::IgnoreCase, ESearchDir::FromEnd);
					LoadPartArray.AddUnique(DirName);
				}
			}
		}

		if (ModelData->AnimationPath.ToSoftObjectPath().IsValid())
		{
			FString PackageName = ModelData->AnimationPath.ToSoftObjectPath().GetLongPackageName();
			FString DirName;
			PackageName.Split(TEXT("/"), &DirName, NULL, ESearchCase::IgnoreCase, ESearchDir::FromEnd);
			//动画蓝图
			LoadPartArray.AddUnique(DirName);
			//动画蓝图中的动作对象
			if (ModelData->ActionConfigPath.ToSoftObjectPath().IsValid())
			{
				const UDataTable* TableData = CfgManager->GetTableByPath(ModelData->ActionConfigPath)->GetBaseTable();
				for (auto object : TableData->GetRowMap())
				{
					FACTION_DATA* ActionData = (FACTION_DATA*)object.Value;
					if (ActionData->AnimPath.ToSoftObjectPath().IsValid())
					{
						PackageName = ActionData->AnimPath.ToSoftObjectPath().GetLongPackageName();
						DirName = "";
						PackageName.Split(TEXT("/"), &DirName, NULL, ESearchCase::IgnoreCase, ESearchDir::FromEnd);
						LoadPartArray.AddUnique(DirName);
					}
				}
			}
		}

	}

	if (LoadPartArray.Num() <= 0)
	{
		return;
	}

	UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary->LoadAssetDataFromPaths(LoadPartArray);
	clock_t BeginAssetTime = clock();
	//ObjectLibrary->LoadAssetDataFromPath(TEXT("/Game/Meshs/SkeletonMeshs"));

	TArray<FAssetData> AssetDataList;
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary->GetAssetDataList(AssetDataList);
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary->LoadAssetsFromAssetData();
	clock_t EndAssetTime = clock();
	CS3_Warning(TEXT("Load Time From path:%f"), (EndAssetTime - BeginAssetTime) / 1000.0);
}

void UCS3ConsoleMgr::CS3_TestLoadParticles()
{
	if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary = NewObject<UObjectLibrary>(UObjectLibrary::StaticClass());
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary->AddToRoot();
	}

	auto AddLoadPartArray = [this](TSoftObjectPtr<UObject> AssetData, TArray<FString>& LoadPartArray)
	{
		if (AssetData.ToSoftObjectPath().IsValid())
		{
			FString PackageName = AssetData.ToSoftObjectPath().GetLongPackageName();
			FString DirName;
			PackageName.Split(TEXT("/"), &DirName, NULL, ESearchCase::IgnoreCase, ESearchDir::FromEnd);
			LoadPartArray.AddUnique(DirName);
		}
	};

	FString SplitStr = FString(TEXT(";"));
	TArray<FString> LoadPartArray;
	auto EffectTestTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PARTICLE_TEST);
	for (auto EffectID : EffectTestTable->GetRowNames())
	{
		const FEFFECT_EMITTER_DATA* EffectEmitterData = EffectTestTable->GetRow<FEFFECT_EMITTER_DATA>(EffectID);
		if (EffectEmitterData)
		{
			AddLoadPartArray(EffectEmitterData->ParticleData.ParticleSystemAsset, LoadPartArray);
			if (EffectEmitterData->SkeletalMesh.AnimAssetList.Num())
			{
				AddLoadPartArray(EffectEmitterData->SkeletalMesh.AnimAssetList[0], LoadPartArray);
			}
			AddLoadPartArray(EffectEmitterData->SkeletalMesh.SkeletalMeshAsset, LoadPartArray);
			AddLoadPartArray(EffectEmitterData->StaticMesh.StaticMeshAsset, LoadPartArray);
		}
	}
	auto EffectTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PARTICLE);
	for (auto EffectID : EffectTable->GetRowNames())
	{
		const FEFFECT_EMITTER_DATA* EffectEmitterData = EffectTable->GetRow<FEFFECT_EMITTER_DATA>(EffectID);
		if (EffectEmitterData)
		{
			AddLoadPartArray(EffectEmitterData->ParticleData.ParticleSystemAsset, LoadPartArray);
			if (EffectEmitterData->SkeletalMesh.AnimAssetList.Num())
			{
				AddLoadPartArray(EffectEmitterData->SkeletalMesh.AnimAssetList[0], LoadPartArray);
			}
			AddLoadPartArray(EffectEmitterData->SkeletalMesh.SkeletalMeshAsset, LoadPartArray);
			AddLoadPartArray(EffectEmitterData->StaticMesh.StaticMeshAsset, LoadPartArray);
		}
	}

	LoadPartArray.AddUnique(TEXT("/Game/BluePrints/Effect/"));

	UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary->LoadAssetDataFromPaths(LoadPartArray);
	clock_t BeginAssetTime = clock();

	TArray<FAssetData> AssetDataList;
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary->GetAssetDataList(AssetDataList);
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->ObjectLibrary->LoadAssetsFromAssetData();
	clock_t EndAssetTime = clock();
	CS3_Warning(TEXT("Load Time From path:%f"), (EndAssetTime - BeginAssetTime) / 1000.0)
}

void UCS3ConsoleMgr::CS3_PlayParticles(FString EffectId)
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(PlayerActor))
	{
		return;
	}
	UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectId, 0.0f, PlayerActor, PlayerActor);
}

void UCS3ConsoleMgr::CS3_ChangeServerIP(const FString& ServerIP)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->GameDefault->ServerIPAddress = ServerIP;
	}
}

void UCS3ConsoleMgr::CS3_ChangeLoginMode(int32 Type)
{
	switch (Type)
	{
	case 0:
		UUECS3GameInstance::Instance->GameDefault->IsEnterGame = true;
		break;
	case 1:
		UUECS3GameInstance::Instance->GameDefault->IsEnterGame = false;
		break;
	default:
		UUECS3GameInstance::Instance->GameDefault->IsEnterGame = false;
		break;
	}
}

void UCS3ConsoleMgr::CS3_PlaySound(const FString& AudioPath)
{
	AAudioManager* AudioManager = UGolbalBPFunctionLibrary::AudioManager();
	if (IsValid(AudioManager))
	{
		bool bIsPlay= AudioManager->PlayPreviewSound(AudioPath);
		if (!bIsPlay)
		{
			GEngine->AddOnScreenDebugMessage(1, 3, FColor::Yellow, FString::Printf(TEXT("ACS3PlayerController::CS3_ClientPlaySound -> AudioPath[%s] is not Find!"), *AudioPath));
			CS3_Warning(TEXT("ACS3PlayerController::CS3_ClientPlaySound -> AudioPath[%s] is not Find!"), *AudioPath);
		}
	}
}

void UCS3ConsoleMgr::CS3_StopSound()
{
	AAudioManager* AudioManager = UGolbalBPFunctionLibrary::AudioManager();
	if (IsValid(AudioManager))
	{
		AudioManager->StopPreviewSound();
	}
}

void UCS3ConsoleMgr::CS3_TogglePlayAudioSystem()
{
	AAudioManager* AudioManager = UGolbalBPFunctionLibrary::AudioManager();
	if (IsValid(AudioManager))
	{
		AudioManager->TogglePlayAudioSystem();
	}
}

void UCS3ConsoleMgr::CS3_PlayStory(const FString& SequenceId)
{
	UGolbalBPFunctionLibrary::GStoryManager()->PlaySequence(SequenceId);
}

void UCS3ConsoleMgr::CS3_StopStory()
{
	UGolbalBPFunctionLibrary::GStoryManager()->StopSequence();
}

void UCS3ConsoleMgr::CS3_PlayMedia(const FString& MediaId)
{
	UGolbalBPFunctionLibrary::MediaPlayerManager()->PlayMedia(MediaId);
}

void UCS3ConsoleMgr::CS3_StopMedia()
{
	UGolbalBPFunctionLibrary::MediaPlayerManager()->Close(true);
}

void UCS3ConsoleMgr::CS3_QueryVSWnd()
{
	TArray<UBaseWindow*> VSWnds;
	VSWnds = UGolbalBPFunctionLibrary::GUIManager()->GetVSWindows();
}

void UCS3ConsoleMgr::CS3_SetIsPromptSkillName(bool IsPromptSkillName)
{
	Console_IsPromptSkillName = IsPromptSkillName;
}

void UCS3ConsoleMgr::CS3_ItemInfo(int32 order)
{
	UCS3EntityInterface* kitbagInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"));
}


void UCS3ConsoleMgr::CS3_QueryRelation()
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3ConsoleMgr::CS3_QueryRelation : PlayerActor!"));
		return;
	}
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(PlayerActor);
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3ConsoleMgr::CS3_QueryRelation : PlayerCharacter!"));
		return;
	}
	int32 TargetID = UGolbalBPFunctionLibrary::GetTargetEntityID();
	AActor* TargetActor = UGolbalBPFunctionLibrary::GetActorByID(TargetID);
	if (!IsValid(TargetActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3ConsoleMgr::CS3_QueryRelation : TargetActor!"));
		return;
	}
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetActor);
	if (!IsValid(TargetCharacter))
	{
		return;
	}

	TMap<COMBAT_RELATION, FString> RelChineseMap;
	RelChineseMap.Add(COMBAT_RELATION::COMBAT_RELATION_NORMAL, TEXT("友好"));
	RelChineseMap.Add(COMBAT_RELATION::COMBAT_RELATION_ENEMY, TEXT("敌对"));
	RelChineseMap.Add(COMBAT_RELATION::COMBAT_RELATION_NEUTRALLY, TEXT("中立"));
	RelChineseMap.Add(COMBAT_RELATION::COMBAT_RELATION_NONE, TEXT("无关"));

	COMBAT_RELATION PositiveRel = PlayerCharacter->QueryRelation(TargetActor);
	COMBAT_RELATION ReverseRel = TargetCharacter->QueryRelation(PlayerActor);
	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_QueryRelation:: [%s %d][%s %d]"), *RelChineseMap[PositiveRel], int(PositiveRel), *RelChineseMap[ReverseRel], int(ReverseRel));
}



void UCS3ConsoleMgr::CS3_Test(const FString& FunctionName)
{
	UCS3EntityInterface* baseinterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("TestInterface"), 0);
	if (baseinterface)
	{
		TArray<FVariant> args;
		baseinterface->OnRemoteMethodCall(FunctionName, args);
	}
}

void UCS3ConsoleMgr::CS3_StartAT(const FString& FunctionName)
{
	FString arg(FunctionName);
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::pKBEApp)
	{
		UAutoTestManager* ATM = UUECS3GameInstance::Instance->AutoTestManager;
		const FName Message = FName(*FunctionName);
		UFunction* Function = ATM->FindFunction(Message);
		if (NULL == Function)
		{
			return;
		}
		FOutputDeviceNull ar;
		ATM->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
	}
}

void UCS3ConsoleMgr::CS3_SearchInputState(int32 IT_Type, FName IT_Key)
{
	// 指令开始
	FString S_Order = FString("CS3_SearchInputState: ---> Ctrl State:[");
	// 控制状态
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()))
	{
		for (auto& CtrlState : UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()->GetCtrlStateList())
		{
			S_Order += CtrlState->ToString() + "/";
		}
	}
	// 输出状态
	S_Order += FString("] ---> Input State:[") + FNAME_TO_FSTRING(IT_Key) + "/";
	bool IsActive = true;
	switch (IT_Type) {
	case 0: { IsActive = CheckBindKeyActive(FKey(IT_Key)); }break;
	case 1: { IsActive = CheckBindActionActive(IT_Key); }break;
	case 2: { IsActive = CheckBindAxisActive(IT_Key); }break;
	case 3: { IsActive = CheckBindAxisKeyActive(IT_Key); }break;
	default: { S_Order += "Type is not find"; }break;
	}
	S_Order += INT_TO_FSTRING(IsActive) + "]";
	UKismetSystemLibrary::PrintString(this, S_Order, true, true, FLinearColor(1.f, .0f, .0f, 1.f), 5.f);
}

void UCS3ConsoleMgr::CS3_CurrEntityAnimation()
{
	FString BackActionId, FrontActionId;
	int32 TargetID = UGolbalBPFunctionLibrary::GetTargetEntityID();
	AActor* TargetActor = UGolbalBPFunctionLibrary::GetActorByID(TargetID);
	AGameCharacter* entityCharacter = Cast<AGameCharacter>(TargetActor);
	if (!IsValid(entityCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3ConsoleMgr::CS3_CurrEntityAnimation : entityCharacter!"));
		return;
	}
	UBaseAnimInstance* entityAnimInstace = entityCharacter->GetBaseAnimInstance();
	entityAnimInstace->GetFronAndBackAction(BackActionId, FrontActionId);
	CS3_Display(CS3DebugType::CL_GM, TEXT("--------CS3_CurrEntityAnimation ------ EntityID = %d  BackActionId = %s, FrontActionId = %s "), TargetID, (*BackActionId), (*FrontActionId));

}


void UCS3ConsoleMgr::CS3_TestLG()
{

}

void UCS3ConsoleMgr::CS3_SwitchHomingSpellAtt()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		if (UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT))
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchHomingSpellAtt(false);
		}
		else
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchHomingSpellAtt(true);
		}
	}
}

void UCS3ConsoleMgr::CS3_SwitchHalfHomingSpellAtt()
{
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		if (UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT))
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchHalfHomingSpellAtt(false);
		}
		else
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchHalfHomingSpellAtt(true);
		}
	}
	else
	{
		CS3_Warning(TEXT(" UCS3ConsoleMgr::CS3_SwitchHalfHomingSpellAtt --- AtkStateMar = Null!"));
	}
}

void UCS3ConsoleMgr::CS3_SwitchNullAtt()
{
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();

	if (IsValid(AtkStateMar))
	{
		if (AtkStateMar->IsActivateState(EATTACT_STATE::NULL_ATT))
		{
			AtkStateMar->SwitchNullAtt(false);
		}
		else
		{
			AtkStateMar->SwitchNullAtt(true);
		}
	}

}

void UCS3ConsoleMgr::CS3_Trigger(const int32& Type, const FString& Param1, const FString& Param2)
{
	UGolbalBPFunctionLibrary::TutorialManager()->OnTrigger(ETUTORIALTRIGGERTYPE(Type), Param1, Param2);
}

void UCS3ConsoleMgr::CS3_GetAllActorsNum()
{
	int32 ActorsNum = 0;
	if (UUECS3GameInstance::pKBEApp != nullptr && UUECS3GameInstance::pKBEApp->Entities() != nullptr) 
	{
		TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
		for (auto& Elem : EntitiesMap)
		{
			KBEngine::Entity* Entity = Elem.Value;
			if (Entity != nullptr)
			{
				AActor* Actor = Entity->Actor();
				if (IsValid(Actor))
				{
					ActorsNum += 1;
				}
			}
		}
	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllActorsNum Num of Actors is %d"), ActorsNum);

}

void UCS3ConsoleMgr::CS3_GetAllActorsTypeAndNum()
{
	if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Entities() == nullptr)
	{
		CS3_Display(CS3DebugType::CL_GM, TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllActorsTypeAndNum pKBEApp->Entities is null !"));
		return;
	}
	TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
	TMap<FString, int32> TypeToNums;
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity != nullptr)
		{
			AActor* Actor = Entity->Actor();
			if (IsValid(Actor))
			{
				FString ActorClassName = Actor->GetClass()->GetName();
				//FString ActorClassName = Actor->GetName();
				if (TypeToNums.Contains(ActorClassName))
				{
					TypeToNums[ActorClassName] += 1;
				}
				else
				{
					TypeToNums.Add(ActorClassName, 1);
				}
			}
		}
	}
	FString Infos = TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllActorsTypeAndNum");
	for (auto TypeToNum : TypeToNums)
	{
		Infos += FString::Printf(TEXT(" %s:%d,"), *TypeToNum.Key, TypeToNum.Value);
	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("%s"), *Infos);

}

void UCS3ConsoleMgr::CS3_GetAllActorsInRangeTypeAndNum(float Range)
{
	TArray<AActor*> Actors = UGolbalBPFunctionLibrary::GetActorsInRange(nullptr, Range);
	TMap<FString, int32> TypeToNums;
	for (auto Actor:Actors)
	{
		if (IsValid(Actor))
		{
			FString ActorClassName = Actor->GetClass()->GetName();
			//FString ActorClassName = Actor->GetName();
			if (TypeToNums.Contains(ActorClassName))
			{
				TypeToNums[ActorClassName] += 1;
			}
			else
			{
				TypeToNums.Add(ActorClassName, 1);
			}
		}
	}
	FString Infos = TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllActorsInRangeTypeAndNum");
	for (auto TypeToNum : TypeToNums)
	{
		Infos += FString::Printf(TEXT(" %s:%d,"), *TypeToNum.Key, TypeToNum.Value);
	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("%s"), *Infos);
	
}

void UCS3ConsoleMgr::CS3_GetAllEntitiesNum()
{
	if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Entities() == nullptr)
	{
		CS3_Display(CS3DebugType::CL_GM, TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllEntitiesNum pKBEApp->Entities is null !"));
		return;
	}
	TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
	CS3_Display(CS3DebugType::CL_GM, TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllEntitiesNum Num of Entities is %d"), EntitiesMap.Num());
}

void UCS3ConsoleMgr::CS3_GetAllEntitiesTypeAndNum()
{
	if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Entities() == nullptr)
	{
		CS3_Display(CS3DebugType::CL_GM, TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllEntitiesTypeAndNum: pKBEApp->Entities is null !"));
		return;
	}
	TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
	TMap<FString, int32> TypeToNums;
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity != nullptr)
		{
			FString ClassName = Entity->ClassName();
			if (TypeToNums.Contains(ClassName))
			{
				TypeToNums[ClassName] += 1;
			}
			else
			{
				TypeToNums.Add(ClassName, 1);
			}
		}
	}
	FString Infos = TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllEntitiesTypeAndNum");
	for (auto TypeToNum : TypeToNums)
	{
		Infos += FString::Printf(TEXT(" %s:%d,"), *TypeToNum.Key, TypeToNum.Value);
	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("%s"), *Infos);
}

void UCS3ConsoleMgr::CS3_GetAllEntitiesInRangeTypeAndNum(float Range)
{
	if (!IsValid(UUECS3GameInstance::Instance))
	{
		return;
	}
	if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Entities() == nullptr || UUECS3GameInstance::pKBEApp->Player() == nullptr)
	{
		CS3_Display(CS3DebugType::CL_GM, TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllEntitiesInRangeTypeAndNum: pKBEApp->Entities is null !"));
		return;
	}

	KBEngine::Entity* PlayerEntity = UUECS3GameInstance::pKBEApp->Player();

	CS3Entity* pEntity_Player = (CS3Entity*)(PlayerEntity);
	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("UCS3ConsoleMgr::CS3_GetAllEntitiesInRangeTypeAndNumno this PlayerRole"));
		return;
	}
		
	

	TMap<FString, int32> TypeToNums;
	TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity != nullptr)
		{
			if (Entity->IsPlayer())
			{
				continue;
			}
			float dist;
			dist = FVector::Distance(PlayerEntity->Position(), Entity->Position());
			if (dist <= Range)
			{
				FString ClassName = Entity->ClassName();
				if (TypeToNums.Contains(ClassName))
				{
					TypeToNums[ClassName] += 1;
				}
				else
				{
					TypeToNums.Add(ClassName, 1);
				}
			}
		}
	}

	FString Infos = TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetAllEntitiesTypeAndNum");
	for (auto TypeToNum : TypeToNums)
	{
		Infos += FString::Printf(TEXT(" %s:%d,"), *TypeToNum.Key, TypeToNum.Value);
	}
	CS3_Display(CS3DebugType::CL_GM, TEXT("%s"), *Infos);
}

void UCS3ConsoleMgr::CS3_GetEntityDefProperty(int32 EntityID, FString Attr)
{
	KBEngine::Entity* ent = UGolbalBPFunctionLibrary::FindEntity(EntityID);
	if (ent != NULL)
	{
		FString Property = ent->GetDefinedProperty(Attr);
		CS3_Display(CS3DebugType::CL_GM, TEXT("########ClientProfile######### UCS3ConsoleMgr::CS3_GetEntityDefProperty %s:%s"), *Attr, *Property);
	}
}

void UCS3ConsoleMgr::CS3_SwtichGameMode()
{
	if (!IsValid(oldPlayer))
	{
		oldPlayer =UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
		APlayerCharacter* oldCharacter = Cast<APlayerCharacter>(oldPlayer);
		FString itemName = "BP_Character";
		const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STRTOCLASS);
		FStrToClass* data = const_cast<FStrToClass*>(table->GetRow<FStrToClass>(itemName));
		UClass* playerCharacter = data->GetTargetClass();
		APlayerCharacter* NewCharacter = UGolbalBPFunctionLibrary::SpawnActor<APlayerCharacter>(playerCharacter);
		NewCharacter->SetActorLocation(oldCharacter->GetActorLocation());
		NewCharacter->SetActorRotation(oldCharacter->GetActorRotation());
		NewCharacter->SwitchControlToSelf();
		UCharacterMovementComponent* MovementComponent = NewCharacter->GetCharacterMovement();
		MovementComponent->SetMovementMode(MOVE_Flying);
	}
	else
	{
		APlayerCharacter* oldCharacter = Cast<APlayerCharacter>(oldPlayer);
		oldCharacter->SwitchControlToSelf();
		oldPlayer = nullptr;
	}
}

void UCS3ConsoleMgr::CS3_ModelsProfile(int32 ModelTextNumb)
{
	UGolbalBPFunctionLibrary::SetModelTextNumber(ModelTextNumb);
	CS3_SwitchFly();
	

}

void UCS3ConsoleMgr::CS3_CreateFile(bool ModelorEffect)
{
	if (ModelorEffect)
	{
		FString Catalog = FPaths::GetPath(FPaths::GetProjectFilePath()) + "/Saved" + "/PerformanceText";
		IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
		if (!PlatformFile.DirectoryExists(*Catalog))
		{
			PlatformFile.CreateDirectory(*Catalog);
			if (!PlatformFile.DirectoryExists(*Catalog))
			{
				CS3_Display(CS3DebugType::CL_GM, TEXT("CS3_CreateFile ------ false"));
			}
		}
		CS3_Display(CS3DebugType::CL_GM, TEXT("CS3_CreateFile ------ true"));
		FString FileName = FString("MyModelText.txt");
		bool AllowOverwriting = false;
		if (PlatformFile.CreateDirectoryTree(*Catalog))
		{
			FString AbsoluteFilePath = Catalog + "/" + FileName;

			if (AllowOverwriting || !PlatformFile.FileExists(*AbsoluteFilePath))
			{
				FFileHelper::SaveStringToFile("", *AbsoluteFilePath);
			}
		}
	}
	else
	{
		FString Catalog = FPaths::GetPath(FPaths::GetProjectFilePath()) + "/Saved" + "/PerformanceText";
		IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
		if (!PlatformFile.DirectoryExists(*Catalog))
		{
			PlatformFile.CreateDirectory(*Catalog);
			if (!PlatformFile.DirectoryExists(*Catalog))
			{
				CS3_Display(CS3DebugType::CL_GM, TEXT("CS3_CreateFile ------ false"));
			}
		}
//		CS3_Display(CS3DebugType::CL_GM, TEXT("CS3_CreateFile ------ true"));
		FString FileName = "MyEffectText.txt";
		bool AllowOverwriting = false;
		if (PlatformFile.CreateDirectoryTree(*Catalog))
		{
			FString AbsoluteFilePath = Catalog + "/" + FileName;

			if (AllowOverwriting || !PlatformFile.FileExists(*AbsoluteFilePath))
			{
				FFileHelper::SaveStringToFile("", *AbsoluteFilePath);
			}
		}
	}
}

void UCS3ConsoleMgr::CS3_WriteFile(TArray<FString> content, bool ModelorEffect)
{
	if (content.Num()>0)
	{
		const FTransform spawnTransform;
		AEffectscapeSample* landSample = Cast<AEffectscapeSample>(UGameplayStatics::BeginDeferredActorSpawnFromClass(this, AEffectscapeSample::StaticClass(), spawnTransform));
		landSample->SaveSampleResult(content, ModelorEffect);
		landSample->Destroy(false, true);
	}
}

void UCS3ConsoleMgr::CS3_WriteText(FString content, bool Peer)
{
	FString Catalog = FPaths::GetPath(FPaths::GetProjectFilePath()) + "/Saved" + "/PerformanceText" + "/MyEffectText.txt";
	IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
	IFileManager* FileManager = &FFileManagerGeneric::Get();
	if (PlatformFile.FileExists(*Catalog))
	{
		if (Peer)
		{
			FFileHelper::SaveStringToFile(content, *Catalog, FFileHelper::EEncodingOptions::ForceUTF8, FileManager, EFileWrite::FILEWRITE_Append);
		}
		else
		{
			FFileHelper::SaveStringToFile("\n" + content, *Catalog, FFileHelper::EEncodingOptions::ForceUTF8, FileManager, EFileWrite::FILEWRITE_Append);
		}
	}
	else
	{
		CS3_CreateFile(false);
		CS3_WriteText(content,Peer);
	}
}

void UCS3ConsoleMgr::CS3_TestShieldText()
{
	const UConfigTable* ShieldTestTextTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TEXT_SHIELD_TEST_DATA);
	if (ShieldTestTextTable)
	{
		TArray<FTEXT_SHIELD_TEST_DATA*> ShieldTextTestDatas;
		ShieldTestTextTable->GetAllRows(ShieldTextTestDatas);
		for (auto ShieldTextTest : ShieldTextTestDatas)
		{
			FString NewMsgText = UUECS3GameInstance::Instance->TextShieldMgr->FilterMsgText(ShieldTextTest->ShieldTextTest);
			CS3_Display(CS3DebugType::CL_GM, TEXT("CS3_TestShieldText:msg is %s,newMsgText is %s"), *(ShieldTextTest->ShieldTextTest), *NewMsgText);
		}
	}
}

void UCS3ConsoleMgr::CS3_SetIsUseShield(bool UseShield)
{
	UUECS3GameInstance::Instance->GameDefault->bIsUseShieldText = UseShield;
}

void UCS3ConsoleMgr::CS3_HideOrShowVSWindows(bool bIsHide)
{
	UGUIManager* GUIManager = UUECS3GameInstance::Instance->GUIManager;
	if (IsValid(GUIManager))
	{
		GUIManager->SetIsHideAllUI(bIsHide);
		GUIManager->HideOrShowVSWindows(bIsHide);
	}
}

void UCS3ConsoleMgr::CS3_HideOrShowLoginWindow(bool bIsHide)
{
	UGUIManager* GUIManager = UUECS3GameInstance::Instance->GUIManager;
	if (IsValid(GUIManager))
	{
		UBaseWindow* Window = GUIManager->GetWindow(TEXT("Login"));
		if (IsValid(Window))
		{
			if (bIsHide)
			{
				Window->Hide();
			}
			else
			{
				Window->Show();
			}
		}
	}
}

void UCS3ConsoleMgr::CS3_GetAssetsByEffect()
{
#if WITH_EDITOR
	TArray<FString> NameFix;
	TArray<FString> NameAssest;
	UGolbalBPFunctionLibrary::CheckFileInPathByPrefix("/Game/Effects/Particles", NameFix, "P_", NameAssest);
	FString TableName = "/Game/Miscs/ContentConfig/Effect/DT_EffectScreenCfg";
	UDataTable* Table = LoadObject<UDataTable>(NULL, *TableName);
	FEFFECT_SCREEN_DATA EffectCreen;
	const IAssetRegistry& Registry = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry").Get();
	for (int i = 0;i <NameFix.Num();i++ )
	{
		EffectCreen.ParticleSystemPtr = Registry.GetAssetByObjectPath(*NameFix[i]).GetAsset();
		FName rowname1 = FSTRING_TO_FNAME(FPackageName::GetLongPackageAssetName(NameAssest[i]));
		FEFFECT_SCREEN_DATA* TableNames = Table->FindRow<FEFFECT_SCREEN_DATA>(rowname1,TEXT(""));
		if (!TableNames)
		{
			Table->AddRow(rowname1, EffectCreen);
		}
	}
#endif
}

void UCS3ConsoleMgr::CS3_GetAssetsByRoleLight()
{
#if WITH_EDITOR
	FString TableName = "/Game/Miscs/ContentConfig/Role/DT_RoleLightCfg";
	UDataTable* Table = LoadObject<UDataTable>(NULL, *TableName);

	auto HashMapTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_LEVELMAP);
	TArray<FLEVEL_HASHMAP*> HashMapDatas;
	HashMapTable->GetAllRows(HashMapDatas);
	for (FLEVEL_HASHMAP* hashMap : HashMapDatas)
	{
		FPLAYER_LIGHT_DATA PlayerRoleLight;
		//PlayerRoleLight.LevelName = FNAME_TO_FSTRING( hashMap->LevelName );
		Table->AddRow(hashMap->LevelName, PlayerRoleLight);
	}
#endif
}

void UCS3ConsoleMgr::CS3_TestAutoNavigate(const FVector& DstPosition)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (Player)
	{
		Player->ActivateNavigateMoveModeOperation(true, DstPosition, 2.0, "", 123, false, false);
	}
}

void UCS3ConsoleMgr::CS3_TestQuestNavigate(const FString& NPCScriptID, FString DstSpaceName /*= ""*/)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		PlayerActor->StartQuestNavigate(true, "", NPCScriptID, DstSpaceName, FVector::ZeroVector, 2.0, 20101000);
	}
}

void UCS3ConsoleMgr::CS3_TestSpaceAllQuestNavigate(const FString& DstSpaceName)
{
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->SpaceNavigateInfo.Empty();
	const UConfigTable* NPCPositionTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC_POINT_DATAS);
	const FSPACE_NPC_ID_TO_POSITION* NPCPositionData = NPCPositionTable->GetRow<FSPACE_NPC_ID_TO_POSITION>(DstSpaceName);
	if (NPCPositionData != nullptr)
	{
		TArray<FNPC_ID_TO_POSITION> NPCIDToPositions = NPCPositionData->NPCIDToPositions;
		for (auto NPCIDToPosition : NPCIDToPositions)
		{
			FString NPCID = NPCIDToPosition.NPCID;
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->SpaceNavigateInfo.Add(NPCID);
		}
	}
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) && UGolbalBPFunctionLibrary::GetCS3PlayerController()->SpaceNavigateInfo.Num() > 0)
	{
		PlayerActor->StartQuestNavigate(true, "", UGolbalBPFunctionLibrary::GetCS3PlayerController()->SpaceNavigateInfo[0], DstSpaceName, FVector::ZeroVector, 1.0, 20101000);
	}
}

void UCS3ConsoleMgr::CS3_CreateClientPlayer()
{
	UClass* BP_Character = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Character"));
	APlayerCharacter* PlayActor = UGolbalBPFunctionLibrary::SpawnActor<APlayerCharacter>(BP_Character);
	if (ensureMsgf(PlayActor, TEXT("PlayActor is NULL")))
	{
		if (IsValid(PlayActor))
		{
			UGolbalBPFunctionLibrary::SetActorAndCompVisibility(PlayActor, UPrimitiveComponent::StaticClass());

			PlayActor->BindLinkEntity(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetSelfEntity());

			FCREATE_APPEARANCE_DATA CreateAppData;
			CreateAppData.RoleProfession = 1;
			CreateAppData.RoleGender = 1;
			CreateAppData.RoleCamp = 1;
			PlayActor->GetAppearanceComponent()->CreateRideAppearance(CreateAppData);

			PlayActor->SetInitialized(true);

			//玩家的actor创建完毕通知
			PlayActor->OnActorCreateFinish.Broadcast();

			PlayActor->EntityId = 0;

			PlayActor->SetActorTransform(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetPawn()->GetActorTransform());
		}
	}
}

void UCS3ConsoleMgr::CS3_SwitchControlPlayer()
{
	UGolbalBPFunctionLibrary::GetCS3PlayerController()->OnSwitchControlPlayer();
}

TArray<FString> UCS3ConsoleMgr::CS3_StringSort(TArray<FString> stringarray)
{
	stringarray.Sort([](const FString& data1, const FString& data2) {
		FString L_LeftS;
		FString L_RightS;
		data1.Split("|", &L_LeftS, &L_RightS);
		FString R_LeftS;
		FString R_RightS;
		data2.Split("|", &R_LeftS, &R_RightS);
		return  UKismetStringLibrary::Conv_StringToInt(L_RightS)< UKismetStringLibrary::Conv_StringToInt(R_RightS);
	});
	return stringarray;
}

void UCS3ConsoleMgr::CS3_SwitchEmptyLogicLevel()
{
	ULevelManager* LevelManager = UUECS3GameInstance::Instance->LevelManager;
	if (LevelManager)
	{
		if (LevelManager->GetSpecialEmptyLogicLevel().IsEmpty())
		{
			LevelManager->SetSpecialEmptyLogicLevel(TEXT("L_Empty"));
		}
		else
		{
			LevelManager->SetSpecialEmptyLogicLevel(TEXT(""));
		}
		
	}
}

void UCS3ConsoleMgr::CS3_ChangeSubLebelLoadMode(int32 LoadMode)
{
	ULevelManager* LevelManager = UUECS3GameInstance::Instance->LevelManager;
	if (LevelManager)
	{
		if (LoadMode == 0)
		{
			LevelManager->SetIsLoadNineSubLevelAfterSplit(true);
			LevelManager->SetIsLoadAllOtherLevelAfterSplit(true);
		}
		else if(LoadMode == 1)
		{
			LevelManager->SetIsLoadNineSubLevelAfterSplit(true);
			LevelManager->SetIsLoadAllOtherLevelAfterSplit(false);
		}
		else if (LoadMode == 2)
		{
			LevelManager->SetIsLoadNineSubLevelAfterSplit(false);
			LevelManager->SetIsLoadAllOtherLevelAfterSplit(false);
		}
	}
}

void UCS3ConsoleMgr::CS3_TargetDistanceDIsplay()
{
	APlayerCharacter* Player =Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	Player->OnTargetDistanceDIsplay();
}

void UCS3ConsoleMgr::CS3_TargetDistanceHiding()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	Player->OnTargetDistanceHiding();
}

void UCS3ConsoleMgr::CS3_PauseActorAnims(bool bIsPause, float FindRangle)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	TArray<AActor*> CharacterList = UGolbalBPFunctionLibrary::GetActorsInRange(
		AGameCharacter::StaticClass(), FindRangle * 100, Player->GetActorLocation());
	CharacterList.Add(Player);

	for (AActor *Objec : CharacterList)
	{
		ACharacter *Character = Cast<ACharacter>(Objec);
		if (Character)
		{
			Character->GetMesh()->bPauseAnims = bIsPause;
		}
	}
}

void UCS3ConsoleMgr::CS3_PauseActorCloth(bool bIsPause, float FindRangle)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	TArray<AActor*> CharacterList = UGolbalBPFunctionLibrary::GetActorsInRange(
		AGameCharacter::StaticClass(), FindRangle * 100, Player->GetActorLocation());
	CharacterList.Add(Player);

	for (AActor *Objec : CharacterList)
	{
		AGameCharacter* Character = Cast<AGameCharacter>(Objec);
		if (IsValid(Character))
		{
			for (auto Iter = Character->GetMeshPartComponentDatas().CreateConstIterator(); Iter; ++Iter)
			{
				MODEL_PART_TYPE Type = Iter.Key();
				USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Iter.Value());
				if (!IsValid(MeshComponent))
				{
					continue;
				}
				if (bIsPause)
				{
					MeshComponent->SuspendClothingSimulation();
				}
				else
				{
					MeshComponent->ResumeClothingSimulation();
				}
			}
		}
	}
}

void UCS3ConsoleMgr::CS3_OpenScope()
{
	if (APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
	{
		if (Player->IsOpenScope)
		{
			Player->IsOpenScope = false;
		}
		else
		{
			Player->IsOpenScope = true;
		}
	}
}

void UCS3ConsoleMgr::CS3_CareamModeChange()
{
	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		isArmLimit = !isArmLimit;
		CS3_SwitchFly();
		if (isArmLimit)
		{
			UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, 0.0f);
			PlayerActor->GetMesh()->SetVisibility(!isArmLimit , true);
			
		}
		else
		{
			UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerActor->SpringArmCompent, 500.0f);
			PlayerActor->GetMesh()->SetVisibility(!isArmLimit , true);
		}
	}
}

void UCS3ConsoleMgr::CS3_ChangeFlySpeed(float MaxSpeed = 2000.0f)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		PlayerActor->GetCharacterMovement()->MaxFlySpeed = MaxSpeed;
	}
}

void UCS3ConsoleMgr::CS3_RotateRroundToTarget(float Speed = 100.0f, float Disatance = 100.0f, float Height = 0.0f, float angle = 0.0f)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor)&&IsValid(PlayerActor->CurPlayerTarget))
	{
		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
		if (IsValid(ControllerModeMgr))
		{
			ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::YControlMode, CC_MODE_REASON::CCM_RRTT_CONTROLLER_MODE);
		}
		CS3_CareamModeChange();
		PlayerActor->RotateRroundToTarget(PlayerActor->CurPlayerTarget,Speed,Disatance,Height,angle);
	}
}

void UCS3ConsoleMgr::CS3_StopRotateRroundToTarget()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) )
	{
		PlayerActor->StopRoateToTarget();
		CS3_CareamModeChange();
		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
		if (IsValid(ControllerModeMgr))
		{
			ControllerModeMgr->RecoveryMode();
		}
	}
}

void UCS3ConsoleMgr::CS3_OpenLookCamera()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		PlayerActor->isOpenLookCamera = !PlayerActor->isOpenLookCamera;
	}
}

void UCS3ConsoleMgr::CS3_ChangePart(int32 PartType, FString PartId)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		PlayerActor->ChangeModelPart((MODEL_PART_TYPE)PartType, PartId);
	}
}

void UCS3ConsoleMgr::CS3_ChangeRidePet(FString CarrideId)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		PlayerActor->ChangeRidePet(CarrideId);
	}
}

void UCS3ConsoleMgr::CS3_ChangeBodyLightEffect(FString EffectId)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		PlayerActor->PreviewBodyLightEffect(EffectId);
	}
}

void UCS3ConsoleMgr::CS3_ShowControllerModeInfo()
{
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	CS3_Log(TEXT("CurControllerMode: %d"), ControllerModeMgr->CurControllerMode);
	CS3_Log(TEXT("OldControllerMode: %d"), ControllerModeMgr->OldControllerMode);
	CS3_Log(TEXT("BackControllerMode: %d"), ControllerModeMgr->BackControllerMode);
	for (int32 i = 0; i < ControllerModeMgr->OtherValue.Num(); i++)
	{
		CS3_Log(TEXT("OtherValue: %s"), *(ControllerModeMgr->OtherValue[i]));
	}
	

	for (TMap<FString, FInputInforAndInstruction>::TIterator it = ControllerModeMgr->m_InforAndInstructions.CreateIterator(); it; ++it)
	{
		CS3_Log(TEXT("m_InforAndInstructions key: %s"), *(it->Key));
		CS3_Log(TEXT("m_InforAndInstructions InputInfor: %s"), *(it->Value.InputInfor));
		for (int32 i = 0; i < it->Value.Instructions.Num(); i++)
		{
			CS3_Log(TEXT("OtherValue: %s"), *(it->Value.Instructions[i]));
		}
	}
}


void UCS3ConsoleMgr::CS3_SetComponentTickState(FString& ComponentName, bool NewTickState)
{
	APlayerController* MyPC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UWorld* World = MyPC->GetWorld();

	//APlayerCharacter    AGameCharacter   AActor
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		TInlineComponentArray<UActorComponent*> Components(*It);
		for (auto Component : Components)
		{
			if (ComponentName == Component->GetName())
			{
				Component->SetComponentTickEnabled(NewTickState);
			}
		}
	}
}

void UCS3ConsoleMgr::CS3_SetPlayerAllComponentTickState(bool NewTickState)
{
	APlayerController* MyPC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UWorld* World = MyPC->GetWorld();

	//APlayerCharacter    AGameCharacter   AActor
	for (TActorIterator<APlayerCharacter> It(World); It; ++It)
	{
		TInlineComponentArray<UActorComponent*> Components(*It);
		for (auto Component : Components)
		{
			Component->SetComponentTickEnabled(NewTickState);
		}
	}
}

void UCS3ConsoleMgr::CS3_SetPlayerVisibleState(bool NewVisibleState)
{
	APlayerController* MyPC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UWorld* World = MyPC->GetWorld();

	//APlayerCharacter    AGameCharacter   AActor
	for (TActorIterator<APlayerCharacter> It(World); It; ++It)
	{
		It->SetActorHiddenInGame(!NewVisibleState);
		TInlineComponentArray<USceneComponent*> Components(*It);
		for (auto Component : Components)
		{
			Component->SetVisibility(NewVisibleState);
		}
	}
}

void UCS3ConsoleMgr::CS3_RetainPlayerSkeletalMesh()
{
	APlayerController* MyPC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UWorld* World = MyPC->GetWorld();
	int32 PlayerEntityId = UGolbalBPFunctionLibrary::GetPlayerID();

	//APlayerCharacter    AGameCharacter   AActor
	for (TActorIterator<APlayerCharacter> It(World); It; ++It)
	{
		if (It->EntityId == PlayerEntityId)
		{
			continue;
		}

		It->SetActorTickEnabled(false);
		TInlineComponentArray<UActorComponent*> Components(*It);
		for (auto Component : Components)
		{
			if (USkeletalMeshComponent* MeshComponent = Cast<USkeletalMeshComponent>(Component))
			{
				MeshComponent->SetAnimationMode(EAnimationMode::AnimationSingleNode);
			}
			else
			{
				Component->DestroyComponent();
			}
		}
	}
}

void UCS3ConsoleMgr::CS3_ToggleEntityServerPos(bool bIsPlayer)
{
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	bool bEnable = true;
	if (bIsPlayer)
	{
		bEnable = !GetEnablePlayerServerPos();
		SetEnablePlayerServerPos(bEnable);
		
	}
	else
	{
		bEnable = !GetEnableEntityServerPos();
		SetEnableEntityServerPos(bEnable);
		
	}
	//废弃
// 	TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
// 	for (auto& Elem : EntitiesMap)
// 	{
// 		KBEngine::Entity* Entity = Elem.Value;
// 		if (Entity)
// 		{
// 			if (IsValid(Entity->Actor()))
// 			{
// 				AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Entity->Actor());
// 				if (IsValid(ServerCharacter))
// 				{
// 					if ((bIsPlayer && Entity->ClassName().Compare(FString("Role"))) || (!bIsPlayer && (!Entity->ClassName().Compare(FString("Role")))))
// 					{
// 						continue;
// 					}
// 					UFilterActorComponent* MFilterComponent = ServerCharacter->GetFilterComponent();
// 					if(IsValid(MFilterComponent))
// 					{
// 						MFilterComponent->EnableEntityServerPos(bEnable);
// 					}
// 					
// 
// 				}
// 			}
// 		}
// 	}
}

//由于需要使用Associations属性,但是又没法改引擎源码,这里复制一份FLogSuppressionImplementation类用于强行访问
class FLogSuppressionImplementation : public FLogSuppressionInterface, private FSelfRegisteringExec
{
public:
	/** Associates a category pointer with the name of the category **/
	TMap<FLogCategoryBase*, FName> Associations;
	/** Associates a category name with a set of category pointers; the inverse of the above.  **/
	TMultiMap<FName, FLogCategoryBase*> ReverseAssociations;
	/** Set of verbosity and break values that were set at boot time. **/
	TMap<FName, uint8> BootAssociations;
	/** For a given category stores the last non-zero verbosity...to support toggling without losing the specific verbosity level **/
	TMap<FName, uint8> ToggleAssociations;
};

void UCS3ConsoleMgr::CS3_Debug(bool isDebug)
{
	FLogSuppressionImplementation& LogSuppression = (FLogSuppressionImplementation&)FLogSuppressionInterface::Get();
	for (TMap<FLogCategoryBase*, FName>::TIterator It(LogSuppression.Associations); It; ++It)
	{
		FLogCategoryBase* Verb = It.Key();
		FString Name = It.Value().ToString();
		if (Name.Contains(CS3DebugTypeName_Prefix))
		{
			if (isDebug)
			{
				Verb->SetVerbosity(ELogVerbosity::Display);
			}
			else
			{
				Verb->SetVerbosity(ELogVerbosity::Warning);
			}
		}
	}
}

void UCS3ConsoleMgr::CS3_DebugByName(FString& CS3DebugTypeName, bool isDebug)
{
	FLogSuppressionImplementation& LogSuppression = (FLogSuppressionImplementation&)FLogSuppressionInterface::Get();
	for (TMap<FLogCategoryBase*, FName>::TIterator It(LogSuppression.Associations); It; ++It)
	{
		FLogCategoryBase* Verb = It.Key();
		FString Name = It.Value().ToString();
		if (Name == CS3DebugTypeName)
		{
			if (isDebug)
			{
				Verb->SetVerbosity(ELogVerbosity::Display);
			}
			else
			{
				Verb->SetVerbosity(ELogVerbosity::Warning);
			}
		}
	}
}

void UCS3ConsoleMgr::CS3_NotEnablePhysics()
{
	APlayerController* MyPC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UWorld* World = MyPC->GetWorld();

	//APlayerCharacter    AGameCharacter   AActor
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		TInlineComponentArray<UPrimitiveComponent*> Components(*It);
		for (auto Component : Components)
		{
			Component->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			Component->SetGenerateOverlapEvents(false);
		}
	}
}

void UCS3ConsoleMgr::CS3_NotHair()
{
	APlayerController* MyPC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UWorld* World = MyPC->GetWorld();

	//APlayerCharacter    AGameCharacter   AActor
	for (TActorIterator<APlayerCharacter> It(World); It; ++It)
	{
		USkeletalMeshComponent* HairMeshCpt = Cast<USkeletalMeshComponent>(It->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_HAIRS));
		if (IsValid(HairMeshCpt))
		{
			HairMeshCpt->SetSkeletalMesh(nullptr);
		}
}
}

void UCS3ConsoleMgr::CS3_NotModel()
{
	APlayerController* MyPC = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UWorld* World = MyPC->GetWorld();

	//APlayerCharacter    AGameCharacter   AActor
	for (TActorIterator<AGameCharacter> It(World); It; ++It)
	{
		TInlineComponentArray<USkeletalMeshComponent*> Components(*It);
		for (auto Component : Components)
		{
			Component->SetSkeletalMesh(nullptr);
		}
	}
}

void UCS3ConsoleMgr::CS3_ChangeJobCreateRoleLevel(int32 Job)
{
	if (Job > 0 && Job < 5)
	{
		ANewCreateRoleLevel *NewCreateRoleLevel11 = Cast<ANewCreateRoleLevel>(
			UUECS3GameInstance::Instance->LoginManager->CurLevelScriptActor);

		UWorld* RWorld = GetWorld();
		ALevelScriptActor *LevelScriptActor = RWorld->GetLevelScriptActor();
		ANewCreateRoleLevel *NewCreateRoleLevel = Cast<ANewCreateRoleLevel>(LevelScriptActor);
		if (NewCreateRoleLevel)
		{
			//NewCreateRoleLevel->ChangeCreateRole(ROLE_PROFESSION_ENUM(Job)); 
		}
	}
}

void UCS3ConsoleMgr::CS3_SetModelHide(FString ScriptId)
{
	AServerCharacter* Actor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	TArray<AActor*> EntityActorList = UGolbalBPFunctionLibrary::GetActorsInRange(
		AServerCharacter::StaticClass(), 8000.0f, Actor->GetActorLocation());
	if (EntityActorList.Num() > 0)
	{
		for (AActor* EntityActor : EntityActorList)
		{
			AServerCharacter* ServerCharacter = Cast<AServerCharacter>(EntityActor);
			if (!IsValid(ServerCharacter) || !ServerCharacter->GetSelfEntity())
			{
				continue;
			}
			if (ScriptId.IsEmpty())
			{
				ServerCharacter->SetActorHiddenInGame(false);
			}
			else
			{
				FString FintdScriptID = ServerCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("scriptID"));
				if (!FintdScriptID.Equals(ScriptId))
				{
					continue;
				}
				ServerCharacter->SetActorHiddenInGame(true);
			}
		}
	}
}

void UCS3ConsoleMgr::CS3_StopModeCurAction(FString ScriptId)
{
	ExectModelActionSetup(1, ScriptId);
}

void UCS3ConsoleMgr::CS3_CancelStopModeCurAction(FString ScriptId)
{
	ExectModelActionSetup(2, ScriptId);
}

void UCS3ConsoleMgr::CS3_StopModelAnim(FString ScriptId)
{
	ExectModelActionSetup(3, ScriptId);
}

void UCS3ConsoleMgr::CS3_CancelStopModelAnim(FString ScriptId)
{
	ExectModelActionSetup(4, ScriptId); 
}

void UCS3ConsoleMgr::ExectModelActionSetup(int32 type, FString ScriptId)
{ 
	AServerCharacter* Actor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	TArray<AActor*> EntityActorList = UGolbalBPFunctionLibrary::GetActorsInRange(
		AServerCharacter::StaticClass(), 8000.0f, Actor->GetActorLocation());
	if (EntityActorList.Num() > 0)
	{
		for (AActor* EntityActor : EntityActorList)
		{
			AServerCharacter* ServerCharacter = Cast<AServerCharacter>(EntityActor);
			if (!IsValid(ServerCharacter) || !ServerCharacter->GetSelfEntity())
			{
				continue;
			}
			FString FintdScriptID = ServerCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("scriptID"));
			if (!FintdScriptID.Equals(ScriptId))
			{
				continue;
			}

			if (type == 1 || type == 2)
			{
				if (type == 1)
				{
					if (IsValid(ServerCharacter->GetMesh()))
					{
						ServerCharacter->GetMesh()->GlobalAnimRateScale = 0.0f;
					}
				}
				else
				{
					ServerCharacter->GetMesh()->GlobalAnimRateScale = 1.0f;
				}
			}
			else if (type == 3 || type == 4)
			{
				if (type == 3)
				{
					if (IsValid(ServerCharacter->GetBaseAnimInstance()))
					{
						ServerCharacter->GetMesh()->SetAnimInstanceClass(nullptr);
					}
				}
				else
				{
					UClass* AnimClass = ServerCharacter->GetCurModelData()->AnimationPath.Get();
					if (IsValid(AnimClass))
					{
						ServerCharacter->GetMesh()->SetAnimInstanceClass(AnimClass);
					}
				}
			}
		}
	}
}

void UCS3ConsoleMgr::CS3_LedgesJumpDrawDebug(int32 DrawType)
{
	AServerCharacter* Actor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(Actor) && IsValid(Cast<APlayerCharacter>(Actor)))
	{
		Cast<APlayerCharacter>(Actor)->DrawDebugType = EDrawDebugTrace::Type(DrawType); 
	}
}

void UCS3ConsoleMgr::CS3_DisplayStoryLog(bool isDebug)
{
	if (isDebug)
	{
		bEnableDisplayStoryLog = true;
	}
	else
	{
		bEnableDisplayStoryLog = false;
	}
}

void UCS3ConsoleMgr::DisplayStoryLog(FString StoryID, bool bIsPlay)
{
	if (bEnableDisplayStoryLog)
	{
		FString Log;
		if (bIsPlay)
		{
			Log = TEXT("正在播放") + StoryID + TEXT("镜头。");
		}
		else 
		{
			Log = TEXT("结束播放") + StoryID + TEXT("镜头。");
		}
		if (GEngine)
		{
			GEngine->AddOnScreenDebugMessage(-1,5.0f, FColor::Red, Log);
		}
	}
}

bool UCS3ConsoleMgr::CheckBindKeyActive(FKey Key)
{
	
	bool IsActive = true;
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()))
	{
		for (auto& CtrlState : UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()->GetCtrlStateList())
		{
			if (!IsValid(CtrlState)) continue;
			IsActive = IsActive && CtrlState->CheckKeyActive(Key);
			// 有不激活状态即返回
			if (!IsActive) return false;
		}
	}
	return true;
}

bool UCS3ConsoleMgr::CheckBindActionActive(FName Name)
{
	bool IsActive = true;
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()))
	{
		for (auto& CtrlState : UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()->GetCtrlStateList())
		{
			if (!IsValid(CtrlState)) continue;
			IsActive = IsActive && CtrlState->CheckActionActive(Name);
			// 有不激活状态即返回
			if (!IsActive) return false;
		}
	}
	return true;
}

bool UCS3ConsoleMgr::CheckBindAxisActive(FName Name)
{
	bool IsActive = true;
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()))
	{
		for (auto& CtrlState : UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()->GetCtrlStateList())
		{
			if (!IsValid(CtrlState)) continue;
			IsActive = IsActive && CtrlState->CheckAxisActive(Name);
			// 有不激活状态即返回
			if (!IsActive) return false;
		}
	}
	return true;
}

bool UCS3ConsoleMgr::CheckBindAxisKeyActive(FKey Key)
{
	bool IsActive = true;
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()))
	{
		for (auto& CtrlState : UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetStateCtrlComp()->GetCtrlStateList())
		{
			if (!IsValid(CtrlState)) continue;
			IsActive = IsActive && CtrlState->CheckAxisKeyActive(Key);
			// 有不激活状态即返回
			if (!IsActive) return false;
		}
	}
	return true;
}

void UCS3ConsoleMgr::CS3_SampleLevel(bool isConfig,float xDelta, float yDelta,float sampleTime)
{
	UE_LOG(LogTemp, Warning, TEXT(" JL:Spawn Sample Level"));
	USampleLevelManager::GetInstance()->StartSample(isConfig,xDelta,yDelta,sampleTime);
}

void UCS3ConsoleMgr::CS3_GetPlayerPos()
{
	KBEngine::Entity* PlayerEntity = UUECS3GameInstance::pKBEApp->Player();
	FVector Pos = PlayerEntity->Position();
	FVector LPos = KBEMath::Unreal2KBEnginePosition(PlayerEntity->LocalPosition());
	int32 id = 0;
	id = PlayerEntity->ParentID();
	CS3_Display(CS3DebugType::CL_GM, TEXT("------------CS3_GetPlayerPos:pos:[%.2f,%.2f,%.2f]---------Localpos:id:%d[%.2f,%.2f,%.2f]---------------"),Pos.X,Pos.Y, Pos.Z,id, LPos.X, LPos.Y, LPos.Z);
}

void UCS3ConsoleMgr::CS3_GetPlayerFloorTracePos()
{
	FVector Pos = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetActorLocation();
	FVector LPos = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->FloorTrace(Pos);
	CS3_Display(CS3DebugType::CL_GM, TEXT("------------CS3_GetPlayerFloorTracePos:pos:[%.2f,%.2f,%.2f]---------Localpos:[%.2f,%.2f,%.2f]---------------"), LPos.X, LPos.Y, LPos.Z, Pos.X, Pos.Y, Pos.Z);
}

void UCS3ConsoleMgr::CS3_ForceGarbageCollection()
{
	UGolbalBPFunctionLibrary::ForceGC();
}

void UCS3ConsoleMgr::CS3_AsyncPlay3DSound(FString AudioId, int32 count)
{
	for (int32 i = 0; i < count; i++)
	{

		UUECS3GameInstance::Instance->AudioManager->AsyncPlay3DSound(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter(), AudioId);
	}
}

void UCS3ConsoleMgr::CS3_AsyncPlay3DSoundRandomCount(int32 count, int32 times)
{	
	for (int32 j = 0; j < times; j++)
	{
		FTimerHandle PlayTimeHandle;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, PlayTimeHandle, FTimerDelegate::CreateLambda([count,j]()
		{
			//const FAUDIO_DATA* AudioData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AUDIO)->GetRow<FAUDIO_DATA>(AudioId);
			for (int32 i = 0; i < count; i++)
			{
				UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
				TArray<FAUDIO_DATA*> AllSounds;
				TArray<FName> RowNames = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AUDIO)->GetRowNames();
				int32 NumSounds = RowNames.Num();
				int32 RandIndex = FMath::RandRange(0, NumSounds-1);
				AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
				AActor* NewActor = UGolbalBPFunctionLibrary::SpawnActor<AActor>(PlayerCharacter->GetClass(), PlayerCharacter->GetActorLocation());
				NewActor->SetLifeSpan(0.1f);
				if (i % 2 == 0)
				{

					UUECS3GameInstance::Instance->AudioManager->Play3DSound(NewActor, RowNames[RandIndex].ToString());
				}
				else
				{
					UUECS3GameInstance::Instance->AudioManager->AsyncPlay3DSound(NewActor, RowNames[RandIndex].ToString());
				}
			}
			GEngine->PerformGarbageCollectionAndCleanupActors();
			TryCollectGarbage(GARBAGE_COLLECTION_KEEPFLAGS, false);
			GEngine->ForceGarbageCollection(true);
		}), j*0.1f, false);
	}
}





CONTROL_COMPILE_OPTIMIZE_END
