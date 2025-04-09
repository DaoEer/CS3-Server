// Fill out your copyright notice in the Description page of Project Settings.

#include "NewCreateRoleLevel.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/BaseWindow.h"
#include "Actor/Player/LoginCharacter.h"
#include "Manager/LoginManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/ConvertUtil.h"
#include "GameData/RoleCreateUIData.h"
#include "Manager/LevelManager.h"
#include "Component/AppearanceComponent.h"
#include "GameData/EnumCsvDefine.h"
#include "GameData/CharacterData.h"
#include "Engine/LevelStreaming.h"
#include "Camera/CameraActor.h"
#include "Kismet/GameplayStatics.h"
#include "Camera/CameraComponent.h"
#include "Manager/GameStatus.h"
#include "GameData/GameDeFine.h"

CONTROL_COMPILE_OPTIMIZE_START
void ANewCreateRoleLevel::BeginPlay()
{
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
		LatentInfo.ExecutionFunction = FName(TEXT("LoadBlockStreamLevelCreateRoleFinished"));
		LatentInfo.UUID = UGolbalBPFunctionLibrary::LevelManager()->GetUUID();
		LatentInfo.Linkage = 0;
		UGameplayStatics::LoadStreamLevel(this, FName(*SubLevel), false, true, LatentInfo);
	}
	Super::BeginPlay();
}

void ANewCreateRoleLevel::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	//销毁创建角色界面
	UBaseWindow* CreateRoleWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("CreateRole"));
	if (IsValid(CreateRoleWidget))
	{
		CreateRoleWidget->Destroy();
	}
	Super::EndPlay(EndPlayReason);
}

void ANewCreateRoleLevel::LoadBlockStreamLevelCreateRoleFinished()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GameStatus)
		&& UUECS3GameInstance::Instance->GameStatus->GetLastStatus() == EGameStatus::CreateRole
		&& UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::Teleport)
	{
		return;
	}

	LoadLevelIndex++;
	if (LoadLevelIndex == 4)
	{
		UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportCreateRoleLevel();
		CloseLoadingWidget();

		int32 Index = ((int32)SelectRoleProfessionID) - 1;
		AActor* AccountActor = ProfessionActors[Index];
		UUECS3GameInstance::Instance->LoginManager->SelectRole(AccountActor);
	}
}

void ANewCreateRoleLevel::CreateDynamicRes()
{
	//获取BP_LoginManager中ChooseCamp的值
	int32 ChooseCamp = UGolbalBPFunctionLibrary::LoginManager()->GetIntPropertyByKey(FString(TEXT("ChooseCamp")));
	//创建当前阵营男女按顺序来共8个待选的BP_Account
	for (int32 i = 1; i < 9; i++)
	{
		int32 RowIndex = i;
		if (ChooseCamp == 2) //阵营1仙 2魔
		{
			RowIndex = i + 8;
		}
		const FRoleCreateUIData* RoleCreateUIData = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_CREATE)->GetRow<FRoleCreateUIData>(INT_TO_FSTRING(RowIndex));
		if (RoleCreateUIData)
		{
			FROLEINFO RoleInfo;
			RoleInfo.ModelID = FNAME_TO_FSTRING(RoleCreateUIData->RoleModelName);
			RoleInfo.Index = RowIndex;
			RoleInfo.profession = RoleCreateUIData->RoleProfession;
			RoleInfo.camp = ChooseCamp;
			RoleInfo.playerName = RoleCreateUIData->ProfessionName.ToString();
			RoleInfo.level = -1;//等级传-1是为了避免在角色创建中选择职业时需要隐藏等级的信息
			RoleInfo.IsAccount = false;

			ALoginCharacter* AccountActor = SPawnBPAccount(RoleInfo);
			ProfessionActors.Add(AccountActor);
			if (IsValid(AccountActor))
			{
				AccountActor->SetRoleLevelActor(this);
			}
		}
	}
}

void ANewCreateRoleLevel::ChangeCreateRole(ROLE_PROFESSION_ENUM Job, ROLE_GENDER_ENUM Gender)
{
	SelectRoleProfessionID = Job;
	SelectGender = Gender;
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewCreateRoleLevel::ChangeCreateRole Job=%d,Gender=%d"), Job, Gender);

	int32 Index = GetSelectIndex();//1-16范围[DT_RoleCreateUICfg表的行数]
	const FRoleCreateUIData* RoleCreateUIData = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
		CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_CREATE)->GetRow<FRoleCreateUIData>(
			FSTRING_TO_FNAME(INT_TO_FSTRING(Index)));
	if (RoleCreateUIData)
	{
		//显示关卡
		UWorld* InWorld = GetWorld();
		for (ULevelStreaming* LevelStreaming : InWorld->GetStreamingLevels())
		{
			FString FileName = FPaths::GetCleanFilename(LevelStreaming->GetWorldAssetPackageName());
			if (FileName.Contains(RoleCreateUIData->LevelCreateName))
			{
				LevelStreaming->SetShouldBeVisible(true);
			}
			else
			{
				LevelStreaming->SetShouldBeVisible(false);
			}
		}

		//显示摄像机
		if (CreateRoleCameras.Contains(Index))
		{
			AActor* CreateRoleCamera = *CreateRoleCameras.Find(Index);
			Cast<ACameraActor>(CreateRoleCamera)->GetCameraComponent()->SetConstraintAspectRatio(false);
			UUECS3GameInstance::Instance->CS3PC->SetViewTargetWithBlend(CreateRoleCamera);
		}
		else
		{
			//创建关卡摄像机
			AActor* CreateRoleCamera = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, RoleCreateUIData->SpawnCameraId);
			Cast<ACameraActor>(CreateRoleCamera)->GetCameraComponent()->SetConstraintAspectRatio(false);
			UUECS3GameInstance::Instance->CS3PC->SetViewTargetWithBlend(CreateRoleCamera);
			CreateRoleCameras.Add(Index, CreateRoleCamera);
		}

		//显示人物模型
		OpenSelectRole();
	}
}

void ANewCreateRoleLevel::OpenSelectRole()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewCreateRoleLevel::OpenSelectRole---------------------------- "));
	//因与阵营无关，所以可无视阵营值
	int32 ActorIndex = int32(SelectRoleProfessionID) - 1;
	if (SelectGender == ROLE_GENDER_ENUM::ROLE_GENDER_TYPE_FEMALE)
	{
		ActorIndex += 4;
	}

	int32 length = ProfessionActors.Num();
	for (int32 i = 0; i < length; i++)
	{
		ALoginCharacter* CreateRoleCharacter = (ALoginCharacter*)ProfessionActors[i];
		if (i == ActorIndex)
		{
			CreateRoleCharacter->GetMesh()->SetVisibility(true, true);
			CreateRoleCharacter->PlayLoginCreatAction(false);//播放动作
			CreateRoleCharacter->SetModelLight(false);
		}
		else
		{
			CreateRoleCharacter->GetMesh()->SetVisibility(false, true);
			CreateRoleCharacter->PlayLoginCreatAction(true);//停止动作
			CreateRoleCharacter->SetModelLight(true);
		}
	}
}

void ANewCreateRoleLevel::OnCreateModelFinished()
{
	CreateFinishCount++;
	if (CreateFinishCount >= 8)
	{
		//显示人物模型
		OpenSelectRole();
	}
}

//void ANewCreateRoleLevel::OnLoadLevelFinished()
//{
//	UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportCreateRoleLevel();
//}

ALoginCharacter* ANewCreateRoleLevel::SPawnBPAccount(FROLEINFO RoleInfo)
{
	UClass* ActorUClass = UGolbalBPFunctionLibrary::GetUClassByStr(FString(TEXT("BP_Account")));
	const FRoleCreateUIData* RoleCreateUIData = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
		CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_CREATE)->GetRow<FRoleCreateUIData>(INT_TO_FSTRING(RoleInfo.Index));
	AActor* RetActor;
	if (RoleCreateUIData)
	{
		RetActor = UGolbalBPFunctionLibrary::SpawnActor<AActor>(ActorUClass, RoleCreateUIData->Position);
	}
	else
	{
		RetActor = UGolbalBPFunctionLibrary::SpawnActor<AActor>(ActorUClass);
	}
	ALoginCharacter* LoginCharacter = Cast<ALoginCharacter>(RetActor);
	if (!IsValid(LoginCharacter))
		return nullptr;
	//外观
	FString InitModelNumber = RoleInfo.ModelID;//初始化列表
	LoginCharacter->Index = RoleInfo.Index;
	if (RoleInfo.IsAccount)
	{
		AliasRoleInfo* ARoleInfo = UUECS3GameInstance::Instance->LoginManager->GetARoleInfo(
			RoleInfo.playerName);
		if (ARoleInfo != nullptr)
		{
			LoginCharacter->CampID = ARoleInfo->Camp;
			LoginCharacter->ProfessionID = ARoleInfo->Profession;
			LoginCharacter->PlayerDbid = INT64_TO_FSTRING(ARoleInfo->DBid);
			TArray<FVariant> args;
			if (!ARoleInfo->ModelNumber.IsEmpty())
			{
				//模型编号
				LoginCharacter->GetAppearanceComponent()->CreateAppearance(ARoleInfo->ModelNumber);
			}
			else if (!InitModelNumber.IsEmpty())
			{
				//组合模型
				LoginCharacter->GetAppearanceComponent()->CreateAppearanceByModelInfo(InitModelNumber, ARoleInfo->AModelInfo);
			}
		}
	}
	else if (!InitModelNumber.IsEmpty())
	{
		LoginCharacter->GetAppearanceComponent()->CreateAppearance(InitModelNumber);
	}

	//设置生成BP_Account的职业和阵营
	UIntProperty *Prop = FindField<UIntProperty>(RetActor->GetClass(), TEXT("ProfessionID"));
	Prop->SetPropertyValue_InContainer(RetActor, RoleInfo.profession);
	UIntProperty *Prop1 = FindField<UIntProperty>(RetActor->GetClass(), TEXT("CampID"));
	Prop1->SetPropertyValue_InContainer(RetActor, RoleInfo.camp);

	//更新模型头顶的名字和等级(由于等级传的-1，等级的信息并不会显示),调用BP_Account中的OnRep_PlayerDbid事件
	FString arg = FString(TEXT("OnShowNameAndLevel"));
	FString param1 = RoleInfo.playerName;
	FString param2 = INT_TO_FSTRING(RoleInfo.level);
	arg = *FString::Printf(TEXT("%s %s %s"), *arg, *param1, *param2);
	FOutputDeviceNull ar;
	RetActor->CallFunctionByNameWithArguments(*arg, ar, NULL, true);

	return LoginCharacter;
}

void ANewCreateRoleLevel::CloseLoadingWidget()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("NewSelectRoleNewCreateRoleLevel::CloseLoadingWidget--------------------- "));
}

int32 ANewCreateRoleLevel::GetSelectIndex()
{
	int32 Index = int32(SelectRoleProfessionID);
	//获取BP_LoginManager中ChooseCamp的值
	int32 ChooseCamp = UGolbalBPFunctionLibrary::LoginManager()->GetIntPropertyByKey(FString(TEXT("ChooseCamp")));
	if (ChooseCamp == 2)//阵营1仙 2魔
	{
		Index += 8;
	}
	if (SelectGender == ROLE_GENDER_ENUM::ROLE_GENDER_TYPE_FEMALE)//性别1男 2女
	{
		Index += 4;
	}
	return Index;
}
CONTROL_COMPILE_OPTIMIZE_END

