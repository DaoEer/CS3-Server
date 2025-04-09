// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3LevelScriptActor.h"
#include "KBEngine.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/LevelHashMap.h"
#include "Kismet/GameplayStatics.h"
#include "Manager/ResourceManager.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/StoryManager.h"
#include "Manager/MapManager.h"
#include "Manager/CustomTimerManager.h"
#include "Entity/Account/Account.h"
#include "PersonalizeLevel.h"
#include "Manager/LocalDataSaveManager.h"
#include "Manager/GameStatus.h"
#include "util/ConvertUtil.h"
#include "Actor/Player/LoginCharacter.h"
#include "GameData/ModifyFaceData.h"
#include "Manager/ModifyFaceManager.h"
#include "Actor/PinchFace/ModifyFaceCharacter.h"
#include "NewCreateRoleLevel.h"
#include "Manager/LoginManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/UIManager.h"
#include "GameData/UIDataDefine.h"
#include "NewSelectRoleLevel.h"
#include "Engine/LevelStreaming.h"
#include "Component/AppearanceComponent.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

ACS3LevelScriptActor::ACS3LevelScriptActor(const FObjectInitializer& ObjectInitializer)
{
	PrimaryActorTick.bCanEverTick = true;
}

void ACS3LevelScriptActor::BeginPlay()
{
	Super::BeginPlay();
	if (!CheckLoginRun())	return;

	EGameStatus CurrStatus = UUECS3GameInstance::Instance->GameStatus->GetCurrStatus();
	bool IsGameReturnLogin = UUECS3GameInstance::Instance->bIsGameReturnLogin;
	if (CurrStatus == EGameStatus::Login && !IsGameReturnLogin)
	{
		OnLanderLandGame();//进入登陆器登陆游戏流程[直接进创建角色或选择角色场景]
	}
	else
	{
		StartShowLoginLevel();
	}
}

void ACS3LevelScriptActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (IsValid(UUECS3GameInstance::Instance->MapManager))
	{
		UUECS3GameInstance::Instance->MapManager->PauseAreaDetectTimer();
	}
#if WITH_EDITOR
	//处理编辑器下Truesky，不会销毁TrueSkySequenceActor的bug
	UClass* TrueSkySequenceClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("TrueSkySequenceActor"));
	TArray<AActor*> FindActors;
	const UWorld* Worldcontext = GetWorld();
	UGameplayStatics::GetAllActorsOfClass(Worldcontext, TrueSkySequenceClass, FindActors);
	if (FindActors.Num() > 0)
	{
		for (AActor* actor : FindActors)
		{
			if (IsValid(actor))
			{
				actor->Destroy();
			}
		}
	}
#endif // WITH_EDITOR
	Super::EndPlay(EndPlayReason);

}

void ACS3LevelScriptActor::NotifyServerEvent()
{
	if (UGolbalBPFunctionLibrary::GStoryManager())
	{
		UGolbalBPFunctionLibrary::GStoryManager()->NotifyServerEvent();
	}
}

void ACS3LevelScriptActor::PlayVoiceWords()
{
	if (UGolbalBPFunctionLibrary::GStoryManager())
	{
		UGolbalBPFunctionLibrary::GStoryManager()->PlayVoiceWords();
	}
}

void ACS3LevelScriptActor::PlayTextEvent()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::PlayTextEvent---------"));
	if (UGolbalBPFunctionLibrary::GStoryManager())
	{
		UGolbalBPFunctionLibrary::GStoryManager()->PlayTextEvent();
	}
}

void ACS3LevelScriptActor::PlayRedrawViewports()
{
	if (UGolbalBPFunctionLibrary::GStoryManager())
	{
		UGolbalBPFunctionLibrary::GStoryManager()->PlayRedrawViewports();
	}
}

void ACS3LevelScriptActor::StoryEventByParams_Implementation(CSTORY_EVENT_PARAM_TYPE_ENUM EventName, const FString& Param1, const FString& Param2, const FString& Param3, const FString& Param4)
{
	if (UGolbalBPFunctionLibrary::GStoryManager())
	{
		UGolbalBPFunctionLibrary::GStoryManager()->StoryEventByParams(EventName, Param1, Param2, Param3, Param4);
	}
}
void ACS3LevelScriptActor::PlayAnimEvent()
{
	if (UGolbalBPFunctionLibrary::GStoryManager())
	{
		UGolbalBPFunctionLibrary::GStoryManager()->PlayAnimEvent();
	}
}

void ACS3LevelScriptActor::StopAnimEvent()
{
	if (UGolbalBPFunctionLibrary::GStoryManager())
	{
		UGolbalBPFunctionLibrary::GStoryManager()->StopAnimEvent();
	}
}

void ACS3LevelScriptActor::CreateDynamicRes()
{
	
}

bool ACS3LevelScriptActor::CheckLoginRun()
{
	if (!IsValid(UUECS3GameInstance::Instance))	return false;	//避免在某些关卡直接播放会崩溃
	
	return true;
}

void ACS3LevelScriptActor::OnCreateModelFinished()
{

}

void ACS3LevelScriptActor::OnLoadLevelFinished()
{
	
}

void ACS3LevelScriptActor::UpdateSelectWndAndModel(AliasRoleInfoTmap& inst)
{
	//保存服务器发送过来的玩家角色数据
	UUECS3GameInstance::Instance->LoginManager->SetRoleInfos(inst);
	//加载L_Login_S关卡，并显示加载进度条界面
	UGolbalBPFunctionLibrary::LoginManager()->OnLoginBaseapp();
	CS3_Warning(TEXT("CS3LevelScriptActor::UpdateSelectWndAndModel:-----------"));
	//构建角色站立用的台子，并根据服务器发送过来的数据创建多个角色模型
	//OnAccountRoleCreate();
	////更新角色选择界面显示,并根据角色数量判断是否要显示CG界面(角色数量为0时播放CG动画)
	//OnUpdateRole();
	//如果没有角色时，会通过UpdateWindow创建BP_CreateWindow，在它的Show事件做了清除语音，并播放CG，播放之后就会加载阵营选择关卡，显示阵营选择界面
}

void ACS3LevelScriptActor::CreateRole(FString playerName, int32 profession, int32 camp, int32 gender)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::CreateRole playerName=%s,profession=%d,camp=%d,gender=%d"), *playerName, profession, camp, gender);
	KBEngine::Entity *entity = UUECS3GameInstance::pKBEApp->Player();
	if (entity != nullptr)
	{
		CS3Entity* pEntity_Player = (CS3Entity*)(entity);
		if (pEntity_Player->IsPlayerAccount())
		{
			Account *account = (Account *)entity;
			/////储存捏脸数据
			FaceInfoList faceinfolist;
			FaceStyle facestyle;
			ModelList modelList;
			TArray<AActor*> ModifyfaceList;
			UGolbalBPFunctionLibrary::GetAllActorsOfClassExt(AModifyFaceCharacter::StaticClass(), ModifyfaceList);
			AModifyFaceCharacter* ModifyfaceActor = Cast<AModifyFaceCharacter>(ModifyfaceList[0]);
			if (IsValid(ModifyfaceActor))
			{
				TArray<FMODIFY_FACE_DATA> BoneDatas = ModifyfaceActor->ModifyFaceDatas;
				for (FMODIFY_FACE_DATA data : BoneDatas)
				{
					FVector BoneLocation = data.BoneTrans.GetLocation();
					FQuat BoneRotator = data.BoneTrans.GetRotation();
					FVector BonesScale = data.BoneTrans.GetScale3D();
					FString boneLocData = FLOAT_TO_FSTRING(BoneLocation.X) + "|" + FLOAT_TO_FSTRING(BoneLocation.Y) + "|" + FLOAT_TO_FSTRING(BoneLocation.Z) + "|";
					FString boneRotData = FLOAT_TO_FSTRING(BoneRotator.X) + "|" + FLOAT_TO_FSTRING(BoneRotator.Y) + "|" + FLOAT_TO_FSTRING(BoneRotator.Z) + "|";
					FString boneScaleData = FLOAT_TO_FSTRING(BonesScale.X) + "|" + FLOAT_TO_FSTRING(BonesScale.Y) + "|" + FLOAT_TO_FSTRING(BonesScale.Z);
					FString boneData = boneLocData + boneRotData + boneScaleData;
					FaceInfo faceinfo;
					faceinfo.boneData = boneData;
					faceinfo.boneName = data.BoneName.ToString();
					faceinfolist.infolist.Add(faceinfo);
				}
				FFACE_STYLE_DATA faceStyleData = ModifyfaceActor->FaceStyleDatas;
				facestyle.ChunzhuangIndex = faceStyleData.ChunZhuangIndex;
				facestyle.ChunzhuangShape =FLOAT_TO_FSTRING(faceStyleData.ChunZhuangShape);
				facestyle.HuXuIndex = faceStyleData.HuXuIndex;
				facestyle.LianWenIndex = faceStyleData.LianWenIndex;
				facestyle.MeiMaoIndex = faceStyleData.MeiMaoIndex;
				facestyle.MeiMaoShape = FLOAT_TO_FSTRING(faceStyleData.MeiMaoShape);
				facestyle.SaiHongIndex = faceStyleData.SaiHongIndex;
				facestyle.SaiHongShape = FLOAT_TO_FSTRING(faceStyleData.SaiHongShape);
				facestyle.YanXianIndex = faceStyleData.YanXianIndex;
				facestyle.YanYingShape = FLOAT_TO_FSTRING(faceStyleData.YanYingShape);
				facestyle.Brightness = FLOAT_TO_FSTRING(faceStyleData.Brighjtness);
				facestyle.ColorDepth = FLOAT_TO_FSTRING(faceStyleData.ColorDepth);
				facestyle.EyeIndex = faceStyleData.EyeIndex;
				facestyle.EyeScale = FLOAT_TO_FSTRING(faceStyleData.EyeScale);
				TMap<MODEL_PART_TYPE, FString> CurPartMap = ModifyfaceActor->GetAppearanceComponent()->GetPartMap();
				
				Model adornmodel;
				adornmodel.modelName = TEXT("adornModel");
				adornmodel.modelNumber = *CurPartMap.Find(MODEL_PART_TYPE::MODEL_PART_ADORN);
				Model hairModel;
				hairModel.modelName = TEXT("hairModel");
				hairModel.modelNumber = *CurPartMap.Find(MODEL_PART_TYPE::MODEL_PART_HAIRS);

				modelList.modelList.Add(hairModel);
				modelList.modelList.Add(adornmodel);
				account->setModifyFaceData(faceinfolist,facestyle,modelList);
			}
			account->AddRole(playerName, profession, camp, gender);

		}
	}
}

void ACS3LevelScriptActor::OnChangeCreateRole(int32 Profession, int32 Gender)
{
	ANewCreateRoleLevel* CreateLevelActor = Cast<ANewCreateRoleLevel>(this);
	CreateLevelActor->ChangeCreateRole(ROLE_PROFESSION_ENUM(Profession), ROLE_GENDER_ENUM(Gender));
}

void ACS3LevelScriptActor::OnChangeSelectRole(const FString& DBID)
{
	ANewSelectRoleLevel* SelectLevelActor = Cast<ANewSelectRoleLevel>(this);
	SelectLevelActor->ChangeSelectRole(DBID);
}

void ACS3LevelScriptActor::AddRoleInfo(AliasRoleInfo& inst)
{
	UUECS3GameInstance::Instance->LoginManager->roleInfos.Add(inst);
}

void ACS3LevelScriptActor::DelRoleInfo(uint64 dbid)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::DelRoleInfo dbid=%d"), dbid);
	TArray<AliasRoleInfo>& roleInfos = UUECS3GameInstance::Instance->LoginManager->roleInfos;
	for (int32 Index = 0; Index < roleInfos.Num(); Index++)
	{
		if (roleInfos[Index].DBid == dbid)
		{
			roleInfos.RemoveAt(Index);
			break;
		}
	}
}

void ACS3LevelScriptActor::DeleteRole(FString dbid)
{
	KBEngine::Entity *entity = UUECS3GameInstance::pKBEApp->Player();
	if (entity != nullptr)
	{
		CS3Entity* pEntity_Player = (CS3Entity*)(entity);
		if (pEntity_Player->IsPlayerAccount())
		{
			Account *account = (Account *)entity;
			account->DeleteRole(uint64(FSTRING_TO_INT64(dbid)));
		}
		CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::DeleteRole dbid=%s"), *dbid);
	}
}

void ACS3LevelScriptActor::RequestActivationKey(const FString & key, const FString & playerName)
{
	KBEngine::Entity *entity = UUECS3GameInstance::pKBEApp->Player();
	if (entity != nullptr)
	{
		CS3Entity* pEntity_Player = (CS3Entity*)(entity);
		if (pEntity_Player->IsPlayerAccount())
		{
			Account *account = (Account *)entity;
			account->RequestActivationKey(key, playerName);
		}
		CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::RequestActivationKey dbid=%s"), *key);
	}
}

void ACS3LevelScriptActor::PlayCG()
{
	ALoginSelectLevel* SelectLevelActor = Cast<ALoginSelectLevel>(this);
	if (IsValid(SelectLevelActor))
	{
		SelectLevelActor->PlayCG();
	}
}

void ACS3LevelScriptActor::OnAddAccount(const uint64& DBID)
{
	UGolbalBPFunctionLibrary::LocalDataSaveManager()->SaveLocalDataFile();
	//创建角色直接进入游戏
	UUECS3GameInstance::Instance->LoginManager->EnterGame(INT64_TO_FSTRING(DBID));
	GetWorld()->GetFirstPlayerController()->EnableInput(GetWorld()->GetFirstPlayerController());
}

void ACS3LevelScriptActor::OnDelAccount(const uint64& DBID)
{
	ANewSelectRoleLevel* SelectLevelActor = Cast<ANewSelectRoleLevel>(this);
	if (IsValid(SelectLevelActor))
	{
		SelectLevelActor->OnDelAccount(INT64_TO_FSTRING(DBID));
	}
}

TArray<AActor*> ACS3LevelScriptActor::GetAccountActors()
{
	TArray<AActor*> result;
	EGameStatus curstatus = UUECS3GameInstance::Instance->GameStatus->GetCurrStatus();
	switch (curstatus)
	{
	case EGameStatus::SelectRole:
	{
			ANewSelectRoleLevel* SelectLevelActor = Cast<ANewSelectRoleLevel>(this);
			if (IsValid(SelectLevelActor))
			{
				result.Append(SelectLevelActor->AccountActors);
			}
		break;
	}
	case EGameStatus::CreateRole:
	{
			ANewCreateRoleLevel* NewCreateRoleLevel = Cast<ANewCreateRoleLevel>(this);
			if (IsValid(NewCreateRoleLevel))
			{
				result.Append(NewCreateRoleLevel->ProfessionActors);
			}
		break;
	}
	case EGameStatus::Personalize:
	{
			APersonalizeLevel* PersonalizeLevel = Cast<APersonalizeLevel>(this);
			if (IsValid(PersonalizeLevel))
			{
				result.Append(PersonalizeLevel->AccountActors);
			}
		break;
	}
	default:
	{
	} 
	}
	return result;
}

UBaseWindow* ACS3LevelScriptActor::GetSelectRoleWidget()
{
	ANewSelectRoleLevel* SelectLevelActor = Cast<ANewSelectRoleLevel>(this);
	if (IsValid(SelectLevelActor))
	{
		return UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SelectRole"));
	}
	return nullptr;
}

int32 ACS3LevelScriptActor::GetSelectRoleIndex()
{
	ANewSelectRoleLevel* SelectLevelActor = Cast<ANewSelectRoleLevel>(this);
	if (IsValid(SelectLevelActor))
	{
		return SelectLevelActor->CurrSelectIndex;
	}
	return 0;
}

void ACS3LevelScriptActor::SelectRoleByTabKey()
{
	if (IsValid(UUECS3GameInstance::Instance->GameStatus) && UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::SelectRole)
	{
		int index = GetSelectRoleIndex();
		TArray<AActor*>AccountActors = GetAccountActors();
		if (AccountActors.Num() > 1)
		{
			AActor* AccountActor;
			if (index < AccountActors.Num() - 1)
			{
				AccountActor = AccountActors[index + 1];
			}
			else
			{
				AccountActor = AccountActors[0];
			}
			if (IsValid(AccountActor))
			{
				UUECS3GameInstance::Instance->LoginManager->SelectRole(AccountActor);
				ALoginCharacter*LoginCharacter = Cast<ALoginCharacter>(AccountActor);
				if (IsValid(LoginCharacter))
				{
					LoginCharacter->SetIsSelect();
				}
			}
		}
	}
}

void ACS3LevelScriptActor::OnLoadLevelDelay()
{
	OnLoadLevelFinished();
}

void ACS3LevelScriptActor::ReceiveWattingInfo(const int32& rank, const float& time, const int32& count)
{
	int index = GetSelectRoleIndex();
	TArray<AActor*>AccountActors = GetAccountActors();
	if (AccountActors.Num() > 0)
	{
		AActor* AccountActor;
		if (index >= 0 && index < AccountActors.Num())
		{
			AccountActor = AccountActors[index];
		}
		else
		{
			AccountActor = AccountActors[0];
		}
		if (IsValid(AccountActor))
		{
			ALoginCharacter* LoginCharacter = Cast<ALoginCharacter>(AccountActor);
			if (IsValid(LoginCharacter))
			{
				CS3_Log(TEXT("LoginCharacter::OnReceiveWattingInfo rank=%d,time=%f,count=%d"), rank, time, count);
				LoginCharacter->OnReceiveWattingInfo(rank, time, count);
			}
			AModifyFaceCharacter* ModifyFaceChatacter = Cast<AModifyFaceCharacter>(AccountActor);
			if (IsValid(ModifyFaceChatacter))
			{
				ModifyFaceChatacter->OnReceiveWattingInfo(rank, time, count);
			}
		}
	}
}

void ACS3LevelScriptActor::OnCancelLoginQueue(const int32& isInQueue)
{
	int index = GetSelectRoleIndex();
	TArray<AActor*>AccountActors = GetAccountActors();
	if (AccountActors.Num() > 0)
	{
		AActor* AccountActor;
		if (index >= 0 && index < AccountActors.Num())
		{
			AccountActor = AccountActors[index];
		}
		else
		{
			AccountActor = AccountActors[0];
		}
		if (IsValid(AccountActor))
		{
			ALoginCharacter* LoginCharacter = Cast<ALoginCharacter>(AccountActor);
			if (IsValid(LoginCharacter))
			{
				CS3_Log(TEXT("LoginCharacter::OnCancelLoginQueue isInQueue=%d"), isInQueue);
				LoginCharacter->OnCancelLoginQueue(isInQueue);
			}
			AModifyFaceCharacter* ModifyFaceChatacter = Cast<AModifyFaceCharacter>(AccountActor);
			if (IsValid(ModifyFaceChatacter))
			{
				ModifyFaceChatacter->OnCancelLoginQueue(isInQueue);
			}
		}
	}
}

void ACS3LevelScriptActor::StartShowLoginLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::StartShowLoginLevel---------------"));
	OnEndPlay.AddUniqueDynamic(UUECS3GameInstance::Instance, &UUECS3GameInstance::OnActorEndPlay);
	UUECS3GameInstance::Instance->LevelBeginPlayDelegate.Broadcast(nullptr);
	//加载资源关卡
	//避免直接加载卡住主线程，导致界面未及时显示穿帮
	CreateDynamicRes();
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayLoadFinishedHandle, this,
		&ACS3LevelScriptActor::OnLoadLevelDelay, 0.1f, false);

	if (IsValid(UGolbalBPFunctionLibrary::LoginManager()))
	{
		UGolbalBPFunctionLibrary::LoginManager()->CurLevelScriptActor = this;
	}
}

void ACS3LevelScriptActor::OnLanderLandGame()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::OnLanderLandGame---------------"));
	FString Type;
	FString Server;
	FString Account;
	FString Password;
	FString ServerName;
	FParse::Value(FCommandLine::Get(), TEXT("Type="), Type);
	FParse::Value(FCommandLine::Get(), TEXT("Server="), Server);
	FParse::Value(FCommandLine::Get(), TEXT("Account="), Account);
	FParse::Value(FCommandLine::Get(), TEXT("Password="), Password);
	FParse::Value(FCommandLine::Get(), TEXT("ServerName="), ServerName);
	bool IsSaveAccount = UUECS3GameInstance::Instance->LoginManager->IsSaveAccount();
	if (Type.Equals("1"))
	{
		HideLoginLevel();

		FString Type111;
		FParse::Value(FCommandLine::Get(), TEXT("Type="), Type111);
		UUECS3GameInstance::Instance->LoginManager->CS3Login(ServerName,Server, Account, Password, "", IsSaveAccount);
		UUECS3GameInstance::Instance->bIsGameReturnLogin = true;
	}
	else if (Type.Equals("2"))
	{
		HideLoginLevel();

		FString qCode;
		FString qSecret;
		FParse::Value(FCommandLine::Get(), TEXT("qCode="), qCode);
		FParse::Value(FCommandLine::Get(), TEXT("qSecret="), qSecret);
		FString Msg = *FString::Printf(TEXT("{\"LoginType\":\"1\",\"QCode\":\"%s\",\"QSecret\":\"%s\"}"),
			*qCode, *qSecret);
		UUECS3GameInstance::Instance->LoginManager->CS3Login(ServerName,Server, Account, Password, Msg, IsSaveAccount);
		UUECS3GameInstance::Instance->bIsGameReturnLogin = true;
	}
	else
	{
		StartShowLoginLevel();
	}
}

void ACS3LevelScriptActor::HideLoginLevel()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::HideLoginLevel---------------"));
	UWorld* InWorld = GetWorld();
	for (ULevelStreaming* LevelStreaming : InWorld->GetStreamingLevels())
	{
		FString FileName = FPaths::GetCleanFilename(LevelStreaming->GetWorldAssetPackageName());
		LevelStreaming->SetShouldBeVisible(false);
	}
	if (IsValid(UGolbalBPFunctionLibrary::LoginManager()))
	{
		UGolbalBPFunctionLibrary::LoginManager()->CurLevelScriptActor = this;
	}
}

CONTROL_COMPILE_OPTIMIZE_END


