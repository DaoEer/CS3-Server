// Fill out your copyright notice in the Description page of Project Settings.

#include "LevelManager.h"
#include "LoginManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/CS3Debug.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/LevelHashMap.h"
#include "Interface/Role/RoleSpaceInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/GameDefault.h"
#include "MoviePlayer.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/TutorialData.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/ConstructorHelpers.h"
#include "CS3Base/UIManager.h"
#include "MapManager.h"
#include "GameStatus.h"
#include"Chuangshi.h"
#include "GameStatus.h"
#include "LoaderManager.h"
#include "TutorialManager.h"
#include "CustomTimerManager.h"
#include "Entity/Role/CS3Role.h"
#include "Util/ConvertUtil.h"
#include "Level/InWorldStreamLevel.h"
#include "Engine/Engine.h"
#include "Engine/LevelStreaming.h"

CONTROL_COMPILE_OPTIMIZE_START

ULevelManager::ULevelManager()
{
	GamelevelType = EGAMELEVELTYPE::GAME_LEVEL_TYPE_NONE;
}

ULevelManager::~ULevelManager()
{
}

ULevelManager* ULevelManager::GetInstance()
{
	cs3_checkNoReentry();
	return (ULevelManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_LevelManager")));
}

void ULevelManager::BeginDestroy()
{
	Super::BeginDestroy();
}

void ULevelManager::OnBeginTeleportNormalLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::OnBeginTeleportNormalLevel------------------ "));
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::Teleport);
	IsTeleportSubStreamLevelCompleted = false;
	if (UUECS3GameInstance::Instance->CustomTimerManager->IsTimerActive(TimerHander))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TimerHander);
	}
}

void ULevelManager::OnEndTeleportNormalLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::OnEndTeleportNormalLevel------------------ "));
	IsTeleportSubStreamLevelCompleted = true;
	GamelevelType = EGAMELEVELTYPE::GAME_LEVEL_TYPE__WORLD_NORMAL;

	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::InWorld);

	if ((CS3Entity*)UUECS3GameInstance::pKBEApp->Player() != nullptr)
	{
		RequestEnterScenes((CS3Entity*)UUECS3GameInstance::pKBEApp->Player());
		GameObjectEnterScenes();
	}

}

void ULevelManager::OnEndTeleportPersonalizeLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::OnEndTeleportPersonalizeLevel------------------ "));
	GamelevelType = EGAMELEVELTYPE::GAME_LEVEL_TYPE_LOGIN;
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::Personalize);
}

void ULevelManager::OnEndTeleportChangeClothesLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::OnEndTeleportChangeClothesLevel------------------ "));
	GamelevelType = EGAMELEVELTYPE::GAME_LEVEL_TYPE_LOGIN;
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::ChangeClothes);
}

const FLEVEL_HASHMAP * ULevelManager::GetLevelHashMapData(const FName &InSpaceScriptID)
{
	//读表，根据表来加载关卡
	auto table = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_LEVELMAP);

	if (table)
	{
		auto newlevelHash = table->GetRow<FLEVEL_HASHMAP>(InSpaceScriptID.ToString());
		if (!newlevelHash)
		{
			auto table1 = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AREA_DATA);
			TArray<FAREA_DATA*> AreaList;
			table1->GetAllRows(AreaList);
			for (const FAREA_DATA* value : AreaList)
			{
				if (value->ScriptID == InSpaceScriptID.ToString())
				{
					newlevelHash = table->GetRow<FLEVEL_HASHMAP>(value->MapScriptID);
					GotoIsPlane = true;
					break;
				}
			}
		}
		return newlevelHash;		
	}
	return nullptr;
}

void ULevelManager::OnEndTeleportLoginLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::OnEndTeleportLoginLevel------------------ "));
	GamelevelType = EGAMELEVELTYPE::GAME_LEVEL_TYPE_LOGIN;
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::Login);

}

void ULevelManager::OnEndTeleportPlaneLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::OnEndTeleportPlaneLevel------------------ "));
	GamelevelType = EGAMELEVELTYPE::GAME_LEVEL_TYPE__WORLD_PLANE;
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::InWorld);
	GameObjectEnterScenes();

}

void ULevelManager::OnEndTeleportSelectRoleLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::OnEndTeleportSelectRoleLevel------------------ "));
	GamelevelType = EGAMELEVELTYPE::GAME_LEVEL_TYPE__ROLE_SELECE;
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::SelectRole);


}

void ULevelManager::OnEndTeleportSelectCampLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::OnEndTeleportSelectCampLevel------------------ "));
	GamelevelType = EGAMELEVELTYPE::GAME_LEVEL_TYPE__CAMP_SELECT;
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::SelectCamp);

}

void ULevelManager::OnEndTeleportCreateRoleLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::OnEndTeleportCreateRoleLevel------------------ "));
	GamelevelType = EGAMELEVELTYPE::GAME_LEVEL_TYPE__ROLE_CREATE;
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::CreateRole);

}

void ULevelManager::TeleportNormalLevel(const FName &InSpaceScriptID, const LOADING_MODE_ENUM loadingMode)
{	
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::TeleportNormalLevel InSpaceScriptID=%s"), *FNAME_TO_FSTRING(InSpaceScriptID));
	//初始化当前InWorldLoading状态
	UUECS3GameInstance::Instance->GameStatus->SetIsInWorldLoadingOver(false);
	//开始加载关卡
	OnBeginTeleportNormalLevel();

	auto newlevelHash = GetLevelHashMapData(InSpaceScriptID);

	if (newlevelHash)
	{
		newLevel_ = newlevelHash->LevelName;

		if (newLevel_ == currLevel_)
		{
			//同一个关卡加载
			LoadSamelevel(newlevelHash, loadingMode);
		}
		else
		{
			//不同关卡的加载
			LoadDifferentlevel(newlevelHash);
		}
	}
	else
	{
		OnEndTeleportNormalLevel();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("HashMap has no row name [%s] !"), *(InSpaceScriptID.ToString()));
	}
}

void ULevelManager::AgainTeleportSubStreamLevel(const FName & InSpaceScriptID)
{
	FLEVEL_HASHMAP* newlevelHash = const_cast<FLEVEL_HASHMAP*>(GetLevelHashMapData(InSpaceScriptID));

	if (!IsTeleportSubStreamLevelCompleted && newlevelHash != nullptr &&
		newlevelHash->LevelName == currLevel_ && newlevelHash->SubStreamLevelName == SubStreamLevel_)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("ULevelManager::AgainTeleportSubStreamLevel InSpaceScriptID=%s  SubStreamLevel_=%s"), *FNAME_TO_FSTRING(InSpaceScriptID),*FNAME_TO_FSTRING(SubStreamLevel_));
		TeleportSubStreamLevel();
	}
	else
	{
		LoadSceneAsyc(InSpaceScriptID);
	}
}

FName ULevelManager::GetCurrLevelName() const
{
	return currLevel_;
}

void ULevelManager::TeleportPlaneLevel(const FName & InSpaceScriptID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Begin load plane level!!"));
	// 执行结束加载委托
	OnEndTeleportPlaneLevel();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("ResourceLoadComplete!"));
}

void ULevelManager::OnSetSpaceData(uint32 spaceID, const FString& key, const FString& value, const LOADING_MODE_ENUM loadingMode/*= LOADING_MODE_ENUM::LOADING_MODE_NULL*/)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("OnSetSpaceData spaceID[%d], key[%s], value[%s]"), spaceID, *key, *value);
	mWaitingEnterScenes.Empty();
	if (SpecialEmptyLogicLevel.IsEmpty())
	{
		LoadSceneAsyc(FName(*value), loadingMode);
	}
	else
	{
		LoadSceneAsyc(FName(*SpecialEmptyLogicLevel), loadingMode);
	}
}


void ULevelManager::TeleportLoginLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::TeleportLoginLevel-----------------------------"));
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::Teleport);
	SubStreamLevel_ = TEXT("");
	currLevel_ = TEXT("");
	spaceScriptID = "";
	GEngine->RedrawViewports(false);
	UGameplayStatics::OpenLevel(this, TEXT("L_Login_Logic"), true, TEXT(""));

}

void ULevelManager::TeleportSelectRoleLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::TeleportSelectRoleLevel-----------------------------"));

	currLevel_ = TEXT("");
	SubStreamLevel_ = TEXT("");

	if ((UUECS3GameInstance::Instance->LoginManager->GetRoleInfos().Num() > 0) &&
		(UUECS3GameInstance::Instance->GameDefault->IsEnterGame))
	{
		GEngine->RedrawViewports(false);
		///此处为跳过选人界面直接进入游戏
		FString DBID = UUECS3GameInstance::Instance->LoginManager->GetRoleInfos()[0].dbid;
		UUECS3GameInstance::Instance->LoginManager->EnterGame(DBID);
		GetWorld()->GetFirstPlayerController()->EnableInput(GetWorld()->GetFirstPlayerController());
	}
	else
	{
		UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::Teleport);
		GEngine->RedrawViewports(false);
		spaceScriptID = "";
		//显示加载进度条
		FEndLoadCallBack EndCallBack;
		UGolbalBPFunctionLibrary::GLoaderManager()->LoadSelectorSpace(EndCallBack);
		UGameplayStatics::OpenLevel(this, TEXT("L_NewSelectRole_Logic"), true, TEXT(""));

		//UGameplayStatics::OpenLevel(this, TEXT("L_SelectRole_Logic"), true, TEXT(""));
	}
}

void ULevelManager::TeleportSelectCampLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::TeleportSelectCampLevel-----------------------------"));
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::Teleport);
	GEngine->RedrawViewports(false);
	//显示加载进度条
	FEndLoadCallBack EndCallBack;
	UGolbalBPFunctionLibrary::GLoaderManager()->LoadCampSpace(EndCallBack);
	UGameplayStatics::OpenLevel(this, TEXT("L_ZYXZ_Logic"), true, TEXT(""));
	spaceScriptID = "";
}

void ULevelManager::TeleportCreateRoleLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::TeleportCreateRoleLevel-----------------------------"));
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::Teleport);
	GEngine->RedrawViewports(false);
	////显示加载进度条
	FEndLoadCallBack EndCallBack;
	UGolbalBPFunctionLibrary::GLoaderManager()->LoadCreatorSpace(EndCallBack);
	UGameplayStatics::OpenLevel(this, TEXT("L_NewCreateRole_Logic"), true, TEXT(""));
	spaceScriptID = "";
	//UGameplayStatics::OpenLevel(this, TEXT("L_CreateRole_Logic"), true, TEXT(""));
}

void ULevelManager::TeleportNieLianLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::TeleportNieLianLevel-----------------------------"));
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::Teleport);
	GEngine->RedrawViewports(false);
	////显示加载进度条
	FEndLoadCallBack EndCallBack;
	UGolbalBPFunctionLibrary::GLoaderManager()->LoadCreatorSpace(EndCallBack);
	UGameplayStatics::OpenLevel(this, TEXT("L_NieLian_Logic"), true, TEXT(""));
	spaceScriptID = "";
}

void ULevelManager::TeleportChangeClothesLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::TeleportChangeClothesLevel-----------------------------"));
	UUECS3GameInstance::Instance->GameStatus->ChangeStatus(EGameStatus::Teleport);
	GEngine->RedrawViewports(false);
	////显示加载进度条
	FEndLoadCallBack EndCallBack;
	UGolbalBPFunctionLibrary::GLoaderManager()->LoadCreatorSpace(EndCallBack);
	UGameplayStatics::OpenLevel(this, TEXT("L_YSG_Logic"), true, TEXT(""));
	spaceScriptID = "";
	newLevel_ = "L_YSG";
	oldLevel_ = currLevel_;
	currLevel_ = newLevel_;
}

void ULevelManager::LoadSceneAsyc(const FName& InSpaceScriptID, const LOADING_MODE_ENUM loadingMode)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------------------>server notice client to load level[%s]!"), *(InSpaceScriptID.ToString()));
	spaceScriptID = InSpaceScriptID;
	GotoIsPlane = false;
	URoleSpaceInterface * RoleSpaceInterface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface")));
	if (RoleSpaceInterface&&RoleSpaceInterface->IsPlaneLoading())
	{
		RoleSpaceInterface->IsPlaneLoading(false);
		TeleportPlaneLevel(InSpaceScriptID);
	}
	else
	{
		TeleportNormalLevel(InSpaceScriptID, loadingMode);
	}
	UUECS3GameInstance::Instance->MapManager->LoadArea(InSpaceScriptID);
	UGolbalBPFunctionLibrary::TutorialManager()->OnTrigger(ETUTORIALTRIGGERTYPE::EnterMapTrigger, InSpaceScriptID.ToString(), TEXT(""));
}

/// <summary>
/// 请求进入地图，此接口会把请求者放入队列中，如果地图加载完成，则会回调请求者的OnEnterScenes()接口
/// </summary>
/// <param name="obj"></param>
void ULevelManager::RequestEnterScenes(CS3Entity* obj)
{
	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
	{
		mWaitingEnterScenes.AddUnique(obj);
	}
	else
	{
		obj->OnEnterScenes();
	}
}

void ULevelManager::RequestLeaveScenes(CS3Entity* obj)
{
	if (mWaitingEnterScenes.Contains(obj))
	{
		mWaitingEnterScenes.Remove(obj);
	}
}

void ULevelManager::GameObjectEnterScenes()
{
	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Login))
		return;
	if (UUECS3GameInstance::pKBEApp == nullptr)return;

	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:ULevelManager::GameObjectEnterScenes : player!"));
		return;
	}

	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:ULevelManager::GameObjectEnterScenes : pEntity_Player||pEntity_Player->IsPlayerRole()!"));
		return;
	}
	//将要进入的对象排序
	mWaitingEnterScenes.Sort([](CS3Entity& v1, CS3Entity& v2)
	{
		return FVector::Dist(v1.Position(), UUECS3GameInstance::pKBEApp->Player()->Position()) > FVector::Dist(v2.Position(), UUECS3GameInstance::pKBEApp->Player()->Position());
	});
	//开始加载对象
	if (LoaderTimerHander.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(LoaderTimerHander);
	}
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(LoaderTimerHander, this, &ULevelManager::OnTimerEnterScenes, 0.02f, true);
	CS3Role *  role = (CS3Role *)UUECS3GameInstance::pKBEApp->Player();
	role->RequestPetTeleporToOwner();
}


void ULevelManager::OnTimerEnterScenes()
{
	if (mWaitingEnterScenes.Num() > 0)
	{
		CS3Entity* Obj = mWaitingEnterScenes.Pop();
		if (UUECS3GameInstance::pKBEApp->FindEntity(Obj->ID()))
		{
			Obj->OnEnterScenes();
		}
	}
	else
	{
		if (LoaderTimerHander.IsValid())
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(LoaderTimerHander);
		}
	}
}

void ULevelManager::AddWaitingEnterList()
{
	if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Entities() == nullptr)
	{
		return;
	}
	TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity != nullptr && !Entity->IsPlayer())
		{
			CS3Entity* tempEntity = (CS3Entity *)(Entity);
			if (!IsValid(tempEntity->Actor()))
			{
				mWaitingEnterScenes.AddUnique(tempEntity);
			}

		}
	}
}

void ULevelManager::SetSpecialEmptyLogicLevel(const FString& LogicLevel)
{
	SpecialEmptyLogicLevel = LogicLevel;
}

void ULevelManager::SetIsLoadNineSubLevelAfterSplit(bool IsLoaded)
{
	IsLoadNineSubLevelAfterSplit = IsLoaded;
}

void ULevelManager::SetIsLoadAllOtherLevelAfterSplit(bool IsLoaded)
{
	IsLoadAllOtherLevelAfterSplit = IsLoaded;
}

bool ULevelManager::GetIsLoadNineSubLevelAfterSplit()
{
	return IsLoadNineSubLevelAfterSplit;
}

bool ULevelManager::GetIsLoadAllOtherLevelAfterSplit()
{
	return IsLoadAllOtherLevelAfterSplit;
}

FString ULevelManager::GetSpecialEmptyLogicLevel()
{
	return SpecialEmptyLogicLevel;
}

void ULevelManager::SetCurrentLoadCompletedLevel(const FString& LevelName)
{
	CurrentLoadCompletedLevel = LevelName;
}

bool ULevelManager::IsLevelLoadCompleted()
{
	if (CurrentLoadCompletedLevel.Equals(currLevel_.ToString()))
	{
		return true;
	}
	else
	{
		return false;
	}
}

void ULevelManager::LoadSamelevel(const FLEVEL_HASHMAP * newlevelHash, const LOADING_MODE_ENUM loadingMode = LOADING_MODE_ENUM::LOADING_MODE_NULL)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::LoadSamelevel OpenLevel[%s]"), *(newlevelHash->LogicLevelName.ToString()));
	//假传送也需要终止输入,停止移动
	ACS3PlayerController* playerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (playerController)
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->EnableInputToControll(false);
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->StopMove();
	}
	bool IsLoad_BG = true;

	URoleSpaceInterface * RoleSpaceInterface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface")));
	
	if (RoleSpaceInterface && RoleSpaceInterface->IsHZMGLevel())
	{
		IsLoad_BG = (bool)(RoleSpaceInterface->GetVideoLoadLevelData()).IsLoadBG;
	}
	else
	{
		if (newlevelHash->IsNeedLoad.Num() > (int32)loadingMode)
		{
			IsLoad_BG = newlevelHash->IsNeedLoad[(int32)loadingMode];
		}
	}

	bool IsTeleportSubStreamLevel = false;

	FName NewSubStreamLevel_ = newlevelHash->SubStreamLevelName;

	if (SubStreamLevel_.ToString().Compare(NewSubStreamLevel_.ToString()))
	{
		SubStreamLevel_ = NewSubStreamLevel_;
		
		///<HZMG在传送门流程阶段不切换子关卡
		if (RoleSpaceInterface && RoleSpaceInterface->IsHZMGLevel() && RoleSpaceInterface->GetVideoLoadLevelData().IsLoadDoor)
		{
			IsLoad_BG = false;
		}
		else 
		{
			TeleportSubStreamLevel();
		}
	
		IsTeleportSubStreamLevel = true;
	}

	if (IsTeleportSubStreamLevel)
	{
		FEndLoadCallBack EndCallBack;
		UGolbalBPFunctionLibrary::GLoaderManager()->LoadTeleportSpace(EndCallBack);
		if (!IsLoad_BG)//是否需要加载loading界面
		{
			//关闭Loading界面
			if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
			{
				UBaseWindow* SwitchSceneWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SwitchScene"));
				if (IsValid(SwitchSceneWindow))
				{
					///<关闭加载界面
					SwitchSceneWindow->Hide();
				}
			}
		}
	}
	else
	{	
		if (IsLoad_BG)//是否需要加载loading界面
		{
			FEndLoadCallBack EndCallBack;
			UGolbalBPFunctionLibrary::GLoaderManager()->LoadTeleportSpace(EndCallBack);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(TimerHander, this, &ULevelManager::OnEndTeleportNormalLevel, 1.0f, false);
		}
		else
		{
			//关闭Loading界面
			if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
			{
				UBaseWindow* SwitchSceneWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SwitchScene"));
				if (IsValid(SwitchSceneWindow))
				{
					///<关闭加载界面
					SwitchSceneWindow->Hide();
				}
			}
			OnEndTeleportNormalLevel();
			UUECS3GameInstance::Instance->GameStatus->OnInWorldLoadingOver();
		}
	}
}

void ULevelManager::LoadDifferentlevel(const FLEVEL_HASHMAP * newlevelHash)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("LevelManager::LoadDifferentlevel OpenLevel[%s]"), *(newlevelHash->LogicLevelName.ToString()));
	//显示加载进度条
	FEndLoadCallBack EndCallBack;
	if (UGolbalBPFunctionLibrary::LoginManager()->bIsFirstEnterWorld)
	{
		UGolbalBPFunctionLibrary::GLoaderManager()->LoadWorldSpace(EndCallBack);
	}
	else
	{
		UGolbalBPFunctionLibrary::GLoaderManager()->LoadTeleportSpace(EndCallBack);
	}
	if (newlevelHash->SubStreamLevelName.ToString().Contains(TEXT("|")))
	{
		TArray<FString> SubStreamLevelNames = UGolbalBPFunctionLibrary::SplitString(newlevelHash->SubStreamLevelName.ToString());
		if (SubStreamLevelNames.Num()>0)
		{
			SubStreamLevel_ = FSTRING_TO_FNAME( SubStreamLevelNames[0]);
		}
		else 
		{
			SubStreamLevel_ = TEXT("");
		}		
	}
	else
	{
		SubStreamLevel_ = newlevelHash->SubStreamLevelName;
	}
	LoadLevelAsync(newlevelHash->LogicLevelName.ToString(), currLevel_, newLevel_);
	/*UGameplayStatics::OpenLevel(this, newlevelHash->LogicLevelName, true, TEXT(""));
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("ULevelManager::LoadDifferentlevel[%s]"), *(newlevelHash->LogicLevelName.ToString()));
	oldLevel_ = currLevel_;
	currLevel_ = newLevel_;*/
}

void ULevelManager::TeleportSubStreamLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("void ULevelManager::TeleportSubStreamLevel-------------------------- "));
	AInWorldStreamLevel* LevelScriptActor = Cast<AInWorldStreamLevel>(UGolbalBPFunctionLibrary::GetMainLevelActor());
	if (LevelScriptActor)
	{
		LevelScriptActor->ChangeToNextSubLevel(SubStreamLevel_);	
	}
}

void ULevelManager::LoadLevelAsync(const FString & LevelName,FName OldLevelName, FName CurLevelName)
{
	UWorld* World = GEngine->GetWorldFromContextObject(this, EGetWorldErrorMode::LogAndReturnNull);
	if (World == nullptr)
	{
		return;
	}
	const ETravelType TravelType = TRAVEL_Absolute;
	FWorldContext &WorldContext = GEngine->GetWorldContextFromWorldChecked(World);
	FString Cmd = LevelName;

	FURL TestURL(&WorldContext.LastURL, *Cmd, TravelType);
	if (TestURL.IsLocalInternal())
	{
		// make sure the file exists if we are opening a local file
		if (!GEngine->MakeSureMapNameIsValid(TestURL.Map))
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("WARNING: The map '%s' does not exist."), *TestURL.Map);
		}
	}
	TWeakObjectPtr<ULevelManager> DelayThisPtr(this);
	LoadPackageAsync(*TestURL.Map, FLoadPackageAsyncDelegate::CreateLambda([LevelName, DelayThisPtr, OldLevelName, CurLevelName](const FName& PackageName, UPackage* LoadedPackage, EAsyncLoadingResult::Type Result)
	{
		if (DelayThisPtr.IsValid()) 
		{
			if (LoadedPackage)
			{
				// Try to find a UWorld object in the level package.
				UWorld* World = UWorld::FindWorldInPackage(LoadedPackage);

				ULevel* Level = World ? World->PersistentLevel : nullptr;
				if (IsValid(Level))
				{
					ULevelManager* LevelManager = DelayThisPtr.Get();	
					
					for (ULevelStreaming* StreamingLevel : World->GetStreamingLevels())
					{
						if (StreamingLevel && StreamingLevel->ShouldBeAlwaysLoaded())
						{
							(LevelManager->StreamingLevels).Add(StreamingLevel);
							FName  WorldAssetPackageFName = StreamingLevel->GetWorldAssetPackageFName();
							TWeakObjectPtr<ULevelStreaming> DelayStreamingLevelPtr(StreamingLevel);
							LoadPackageAsync(WorldAssetPackageFName.ToString(), FLoadPackageAsyncDelegate::CreateUObject(LevelManager, &ULevelManager::AsyncPackageCallback, FSTRING_TO_FNAME(LevelName), OldLevelName, CurLevelName, DelayStreamingLevelPtr), 255, PKG_ContainsMap);
							
						}
					}
					if (LevelManager->StreamingLevels.Num() == 0)
					{
						UGameplayStatics::OpenLevel(LevelManager, FSTRING_TO_FNAME(LevelName), true, TEXT(""));
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("ULevelManager::LoadDifferentlevel[%s]"), *(LevelName));

						LevelManager->oldLevel_ = OldLevelName;
						LevelManager->currLevel_ = CurLevelName;
					}
				}
			}
		}
	}
	),255, PKG_ContainsMap);
}

void ULevelManager::AsyncPackageCallback(const FName & PackageName, UPackage * LevelPackage, EAsyncLoadingResult::Type Result, FName LevelName, FName OldLevelName, FName CurLevelName, TWeakObjectPtr<ULevelStreaming> LevelStreamingPtr)
{
	if (LevelPackage)
	{
		if (LevelStreamingPtr.IsValid())
		{
			if (StreamingLevels.Contains(LevelStreamingPtr.Get()))
			{
				StreamingLevels.Remove(LevelStreamingPtr.Get());
			}
			if (StreamingLevels.Num() == 0)
			{
				auto newlevelHash = GetLevelHashMapData(spaceScriptID);

				if (newlevelHash)
				{
					if (newlevelHash->LevelName == CurLevelName)
					{
						UGameplayStatics::OpenLevel(this, LevelName, true, TEXT(""));
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("ULevelManager::LoadDifferentlevel[%s]"), *(LevelName.ToString()));

						oldLevel_ = OldLevelName;
						currLevel_ = CurLevelName;
					}
				}
			}
		}
	}
}
CONTROL_COMPILE_OPTIMIZE_END