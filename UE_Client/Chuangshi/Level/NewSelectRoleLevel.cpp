// Fill out your copyright notice in the Description page of Project Settings.


#include "NewSelectRoleLevel.h"
#include "Actor/Player/LoginCharacter.h"
#include "GameData/GameDefault.h"
#include "Camera/CameraActor.h"
#include "GameData/RoleCreateUIData.h"
#include "Entity/Account/Account.h"
#include "Camera/CameraComponent.h"
#include "Manager/LoginManager.h"
#include "Manager/GameStatus.h"
#include "Component/AppearanceComponent.h"
#include "Manager/CustomTimerManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/UIManager.h"
#include "Manager/LoginManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "GameData/EnumCsvDefine.h"
#include "Manager/CfgManager.h"
#include "Manager/LevelManager.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/MediaPlayerManager.h"
#include "Kismet/GameplayStatics.h"
#include "GameData/UIDataDefine.h"
#include "Engine/LevelStreaming.h"
#include "GameData/GameDeFine.h"

void ANewSelectRoleLevel::BeginPlay()
{
	if (IsValid(InputComponent))
	{
		InputComponent->BindKey(EKeys::Tab, EInputEvent::IE_Pressed, this, &ANewSelectRoleLevel::OnSelectRoleByTabKey);
		InputComponent->BindKey(EKeys::Escape, EInputEvent::IE_Pressed, this, &ANewSelectRoleLevel::StopMediaSkip);
	}
	CurrSelectIndex = 0;
	CreateFinishCount = 0;
	CurrDBID = "";

	TArray<FString> LevelNameDatas;
	LevelNameDatas.Add("L_CJJS_04");
	LevelNameDatas.Add("L_CJJS_03");
	LevelNameDatas.Add("L_CJJS_05");
	LevelNameDatas.Add("L_CJJS_07");

	for (int32 i = 0; i < LevelNameDatas.Num(); ++i)
	{
		FString SubLevel = LevelNameDatas[i];
		FLatentActionInfo LatentInfo;
		LatentInfo.CallbackTarget = this;
		LatentInfo.ExecutionFunction = FName(TEXT("LoadBlockStreamLevelSelectFinished"));
		LatentInfo.UUID = UGolbalBPFunctionLibrary::LevelManager()->GetUUID();
		LatentInfo.Linkage = 0;
		UGameplayStatics::LoadStreamLevel(this, FName(*SubLevel), false, true, LatentInfo);
	}
	Super::BeginPlay();
}

void ANewSelectRoleLevel::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		UBaseWindow* SelectRoleWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SelectRole"));
		if (SelectRoleWidget)
		{
			SelectRoleWidget->Destroy();
		}
	}
	Super::EndPlay(EndPlayReason);
}

void ANewSelectRoleLevel::LoadBlockStreamLevelSelectFinished()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GameStatus)
		&& UUECS3GameInstance::Instance->GameStatus->GetLastStatus() == EGameStatus::SelectRole
		&& UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::Teleport)
	{
		return;
	}

	LoadLevelIndex++;
	if (LoadLevelIndex == 4)
	{
		UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportSelectRoleLevel();
		CloseLoadingWidget();

		//选中上次登录所用的DBID的index
		TArray<FROLEINFO> roleinfos = UUECS3GameInstance::Instance->LoginManager->GetRoleInfos();
		FString DBID = "";
		if (roleinfos.Num() > 0)
		{
			DBID = roleinfos[0].dbid;
			if (GetLastLoginDBID() > 0)
			{
				DBID = INT64_TO_FSTRING(GetLastLoginDBID());
			}
		}
		ChangeSelectRole(DBID);
	}
}

void ANewSelectRoleLevel::CreateDynamicRes()
{
	//显示角色选择关卡界面
	UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, 
		EGameStatus::SelectRole, TEXT("SelectRole"));

	//根据RoleInfos的信息创建角色;位置是需要计算的，其它可以使用配置表中的
	TArray<FROLEINFO> roleinfos = UUECS3GameInstance::Instance->LoginManager->GetRoleInfos();
	//目前限制不能超过5人
	check(roleinfos.Num() <= 5);
	//不用判断roleinfos的数量，如果它为0.那个在此之前就转到阵营选择
	for (FROLEINFO roleinfo : roleinfos)
	{
		AddAccountActor(roleinfo);
	}
}

void ANewSelectRoleLevel::ChangeSelectRole(const FString& DBID)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewSelectRoleLevel::ChangeSelectRole DBID=%s"), *DBID);
	CurrDBID = DBID;
	if (DBID.IsEmpty())//由创建角色界面“取消创建”功能触发[显示关卡，不需要显示角色]
	{
		CurrSelectIndex = 0;
		int32 DefultProfession = (int32)ROLE_PROFESSION_ENUM::ROLE_PROFESSION_TYPE_ZHAN_SHI;
		FName DefultRowName = FSTRING_TO_FNAME(INT_TO_FSTRING(DefultProfession));
		const FRoleCreateUIData* DefultRoleCreateUIData = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_CREATE)->GetRow<FRoleCreateUIData>(DefultRowName);
		//显示关卡
		OpenSelectLevel(*DefultRoleCreateUIData);
		//显示摄像机
		int32 Index = int32(DefultRoleCreateUIData->RoleProfession);
		if (DefultRoleCreateUIData->RoleCamp == 2)
		{
			Index += 8;
		}
		OpenSelectCamera(Index, *DefultRoleCreateUIData);
		return;
	}

	FROLEINFO RoleInfo = GetRoleInfoByDBID(FSTRING_TO_INT64(DBID));
	int32 RowIndex = GetRowIndex(RoleInfo.profession, RoleInfo.gender, RoleInfo.camp);
	const FRoleCreateUIData* RoleCreateUIData = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
		CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_CREATE)->GetRow<FRoleCreateUIData>(
			FSTRING_TO_FNAME(INT_TO_FSTRING(RowIndex)));
	if (RoleCreateUIData)
	{
		//显示关卡
		OpenSelectLevel(*RoleCreateUIData);

		//显示摄像机
		int32 Index = int32(RoleInfo.profession);
		if (RoleInfo.camp == 2)
		{
			Index += 8;
		}
		OpenSelectCamera(Index, *RoleCreateUIData);

		//显示角色
		OpenSelectRole(DBID);

		//通知界面更新
		UBaseWindow* SelectRoleWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SelectRole"));
		if (SelectRoleWidget)
		{
			FString arg = FString(TEXT("SelectDBID"));
			FString param1 = DBID;         //INT_TO_FSTRING(DBID);
			int32 param2 = CurrSelectIndex; 
			arg = *FString::Printf(TEXT("%s %s %d"), *arg, *param1, param2);
			FOutputDeviceNull ar;
			SelectRoleWidget->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
		}
	}
}

void ANewSelectRoleLevel::OpenSelectLevel(FRoleCreateUIData RoleCreateUIData)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("ANewSelectRoleLevel::OpenSelectLevel------------------------------"));
	UWorld* InWorld = GetWorld();
	for (ULevelStreaming* LevelStreaming : InWorld->GetStreamingLevels())
	{
		FString FileName = FPaths::GetCleanFilename(LevelStreaming->GetWorldAssetPackageName());
		if (FileName.Contains(RoleCreateUIData.LevelCreateName))
		{
			LevelStreaming->SetShouldBeVisible(true);
		}
		else
		{
			LevelStreaming->SetShouldBeVisible(false);
		}
	}
}

void ANewSelectRoleLevel::OpenSelectCamera(int32 Index, FRoleCreateUIData RoleCreateUIData)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewSelectRoleLevel::OpenSelectCamera  Index=%d"), Index);
	if (CreateRoleCameras.Contains(Index))
	{
		AActor* CreateRoleCamera = *CreateRoleCameras.Find(Index);
		Cast<ACameraActor>(CreateRoleCamera)->GetCameraComponent()->SetConstraintAspectRatio(false);
		UUECS3GameInstance::Instance->CS3PC->SetViewTargetWithBlend(CreateRoleCamera);
	}
	else
	{
		//创建关卡摄像机
		AActor* CreateRoleCamera = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, RoleCreateUIData.SpawnCameraId);
		Cast<ACameraActor>(CreateRoleCamera)->GetCameraComponent()->SetConstraintAspectRatio(false);
		UUECS3GameInstance::Instance->CS3PC->SetViewTargetWithBlend(CreateRoleCamera);
		CreateRoleCameras.Add(Index, CreateRoleCamera);
	}
}

void ANewSelectRoleLevel::OpenSelectRole(FString Dbid)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewSelectRoleLevel::OpenSelectRole Dbid=%s"), *Dbid);
	int32 length = AccountActors.Num();
	for (int32 i = 0; i < length; i++)
	{
		ALoginCharacter* SelectRoleCharacter = (ALoginCharacter*)AccountActors[i];
		if (SelectRoleCharacter->PlayerDbid == Dbid)
		{
			CurrSelectIndex = i;
			SelectRoleCharacter->GetMesh()->SetVisibility(true, true);
			SelectRoleCharacter->PlayLoginSelectAction(false, true);
			SelectRoleCharacter->SetModelLight(false);
		}
		else
		{
			SelectRoleCharacter->GetMesh()->SetVisibility(false, true);
			SelectRoleCharacter->PlayLoginSelectAction(true, false);
			SelectRoleCharacter->StopAction();
			SelectRoleCharacter->SetModelLight(true);
		}
	}
}

void ANewSelectRoleLevel::OnCreateModelFinished()
{
	CreateFinishCount += 1;
	TArray<FROLEINFO> roleinfos = UUECS3GameInstance::Instance->LoginManager->GetRoleInfos();
	if (CreateFinishCount >= roleinfos.Num())
	{
		CloseLoadingWidget();
		OpenSelectRole(CurrDBID);
	}
}

void ANewSelectRoleLevel::AddAccountActor(FROLEINFO RoleInfo) 
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewSelectRoleLevel::AddAccountActor----------------------- "));
	UClass* ActorUClass = UGolbalBPFunctionLibrary::GetUClassByStr(FString(TEXT("BP_Account")));
	ALoginCharacter* AccountActor = UGolbalBPFunctionLibrary::SpawnActor<ALoginCharacter>(ActorUClass);
	if (IsValid(AccountActor))
	{
		AccountActor->SetRoleLevelActor(this);
		AccountActor->Index = GetRowIndex(RoleInfo.profession, RoleInfo.gender, RoleInfo.camp);
		AccountActor->PlayerDbid = RoleInfo.dbid;
		AccountActor->CampID = RoleInfo.camp;
		AccountActor->ProfessionID = RoleInfo.profession;
		AccountActor->GenderID = RoleInfo.gender;
		AccountActor->Bonedatas = RoleInfo.bonedatas;
		AccountActor->BoneNames = RoleInfo.bonenames;
		AccountActor->FaceStyleDatas = RoleInfo.facestyledata;
		AccountActor->OfflineTime = FSTRING_TO_INT64(RoleInfo.offlineTime);
		FName RowIndex = FSTRING_TO_FNAME(INT_TO_FSTRING(AccountActor->Index));
		const FRoleCreateUIData* RoleCreateUIData = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_CREATE)->GetRow<FRoleCreateUIData>(RowIndex);

		FString intModelNumber = TEXT("");
		if (ensureMsgf(RoleCreateUIData, TEXT("ANewSelectRoleLevel::AddAccountActor Unexpected null RoleCreateUIData! ")))
		{
			intModelNumber = RoleCreateUIData->RoleModelName.ToString();//初始化列表
		}
		AliasRoleInfo* ARoleInfo = UUECS3GameInstance::Instance->LoginManager->GetARoleInfo(RoleInfo.playerName);
		if (!ARoleInfo->ModelNumber.IsEmpty())
		{
			//模型编号
			AccountActor->GetAppearanceComponent()->CreateAppearance(ARoleInfo->ModelNumber);
		}
		else if (!intModelNumber.IsEmpty())
		{
			//组合模型
			AccountActor->GetAppearanceComponent()->CreateAppearanceByModelInfo(intModelNumber, ARoleInfo->AModelInfo);
		}
		else
		{
			//采用默认预定义
			AccountActor->GetAppearanceComponent()->CreateAppearance(intModelNumber);
		}

		//设置位置和朝向
		if (RoleCreateUIData)
		{
			AccountActor->SetActorTransform(RoleCreateUIData->Position);
		}
		AccountActors.Add(AccountActor);

		//更新模型头顶的名字和等级,调用BP_Account中的OnRep_PlayerDbid事件
		FString arg = FString(TEXT("OnRep_PlayerDbid"));
		FOutputDeviceNull ar;
		AccountActor->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
	}
}

void ANewSelectRoleLevel::OnAddAccount(const FString& DBID)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewSelectRoleLevel::OnAddAccount DBID=%s"), *DBID);
	//创建BP_Account
	FROLEINFO RoleInfo;
	UUECS3GameInstance::Instance->LoginManager->GetRoleInfo(DBID, RoleInfo);
	AddAccountActor(RoleInfo);

	ChangeSelectRole(DBID);
	
}

void ANewSelectRoleLevel::OnDelAccount(const FString& DBID)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewSelectRoleLevel::OnDelAccount DBID=%s"), *DBID);
	//删除此BP_Account
	ALoginCharacter* FindActor;
	FindActor = nullptr;
	for (AActor* actor : AccountActors)
	{
		ALoginCharacter* character = Cast<ALoginCharacter>(actor);
		if (DBID == character->PlayerDbid)
		{
			if (IsValid(character))
			{
				FindActor = character;
				break;
			}
		}
	}
	if (IsValid(FindActor))
	{
		AccountActors.Remove(FindActor);
		FindActor->SetActorHiddenInGame(true);
		FindActor->Destroy();
	}

	//通知界面删除此DBID的显示
	if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		UBaseWindow* SelectRoleWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SelectRole"));
		if (SelectRoleWidget)
		{
			FString arg = FString(TEXT("OnDelAccount"));
			FString param1 = DBID; //INT_TO_FSTRING(DBID);
			arg = *FString::Printf(TEXT("%s %s"), *arg, *param1);
			FOutputDeviceNull ar;
			SelectRoleWidget->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
		}
	}
	TArray<FROLEINFO> roleinfos = UUECS3GameInstance::Instance->LoginManager->GetRoleInfos();
	if (roleinfos.Num() > 0)
	{
		CurrSelectIndex = 0;//选中第一个，更新界面
		ChangeSelectRole(roleinfos[0].dbid);
	}
}

ALoginCharacter* ANewSelectRoleLevel::GetActorByDBID(const uint64& dbid)
{
	for (AActor* Actor : AccountActors)
	{
		ALoginCharacter* AccountActor = Cast<ALoginCharacter>(Actor);
		if (IsValid(AccountActor) && FSTRING_TO_INT64(AccountActor->PlayerDbid) == dbid)
		{
			return AccountActor;
		}
	}
	return nullptr;
}

FROLEINFO ANewSelectRoleLevel::GetRoleInfoByDBID(const uint64& dbid)
{
	FROLEINFO RoleInfo = FROLEINFO();
	TArray<FROLEINFO> roleinfos = UUECS3GameInstance::Instance->LoginManager->GetRoleInfos();
	for (int32 i = 0; i < roleinfos.Num(); i++)
	{
		FROLEINFO FindRoleInfo = roleinfos[i];
		if (FindRoleInfo.dbid == INT64_TO_FSTRING(dbid))
		{
			RoleInfo = FindRoleInfo;
			break;
		}
	}
	return RoleInfo;
}

void ANewSelectRoleLevel::CloseLoadingWidget()
{
	
}

void ANewSelectRoleLevel::OnSelectRoleByTabKey()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewSelectRoleLevel::OnSelectRoleByTabKey------------------------ "));
	SelectRoleByTabKey();
}

uint64 ANewSelectRoleLevel::GetLastLoginDBID()
{
	KBEngine::Entity *entity = UUECS3GameInstance::pKBEApp->Player();
	if (entity != nullptr)
	{
		CS3Entity* pEntity_Player = (CS3Entity*)(entity);
		if (pEntity_Player->IsPlayerAccount())
		{
			Account *account = (Account *)entity;
			if (account)
			{
				uint64 LastLoginDBID = account->GetDefinedProperty(TEXT("lastLogonDBID")).GetValue<uint64>();
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("ANewSelectRoleLevel::GetLastLoginDBID()   LastLoginDBID=[%i]  "), LastLoginDBID);
				return LastLoginDBID;

			}
		}
	}
	return 0;
}

int32 ANewSelectRoleLevel::GetRowIndex(int32 Profession, int32 Gender, int32 Camp)
{
	int32 RowIndex = Profession;
	if (Camp == 2)//阵营1仙 2魔
	{
		RowIndex += 8;
	}
	if (Gender == 2)//性别1男 2女
	{
		RowIndex += 4;
	}
	return RowIndex;
}

//void ANewSelectRoleLevel::OnLoadLevelFinished()
//{
//	UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportSelectRoleLevel();
//}

void ANewSelectRoleLevel::StopMediaSkip()
{
	UGolbalBPFunctionLibrary::MediaPlayerManager()->OnShowMediaSkipTime_BP();
}