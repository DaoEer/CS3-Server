// Fill out your copyright notice in the Description page of Project Settings.

#include "LoginCharacter.h"
#include "GameData/RoleCreateUIData.h"
#include "Level/CS3LevelScriptActor.h"
#include "Manager/AudioManager.h"
#include "Util/ConvertUtil.h"
#include "Component/AppearanceComponent.h"
#include "Util/CS3Debug.h"
#include "GameData/CharacterData.h"
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/GameStatus.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/ModifyFaceManager.h"
#include "GameData/GameDeFine.h"


CONTROL_COMPILE_OPTIMIZE_START

ALoginCharacter::ALoginCharacter()
{
	CharacterClassName = TEXT("LoginCharacter");
	PrimaryActorTick.bCanEverTick = true;

	CampID = 0;
	Index = 0;
	ProfessionID = 0;
	//PlayerDbid = 0;
	GenderID = 0;
	OfflineTime = 0;

	CreateRoleMesh();
	InitBaseComponent();
}

void ALoginCharacter::BeginPlay()
{
	RoleLevelActor = nullptr;
	Super::BeginPlay();
}

void ALoginCharacter::BeginDestroy()
{
	RoleLevelActor = nullptr;
	Super::BeginDestroy();
}

void ALoginCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
}

void ALoginCharacter::PlayLoginSelectAction(bool IsStand, bool IsSelect_)
{
	CS3_Display(CS3DebugType::CL_Login, TEXT("LoginCharacter::PlayLoginSelectAction IsStand=%d"), IsStand);
	FString ScriptID = INT_TO_FSTRING(CampID) + INT_TO_FSTRING(ProfessionID) + INT_TO_FSTRING(GenderID);
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FSELECT_CREAT_ACTION_DATE* SelectActionData = CfgManager->GetTableByType(
		CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SELECT_CREAT_ACTION)->GetRow<FSELECT_CREAT_ACTION_DATE>(ScriptID);
	AAudioManager* AudioManager = UUECS3GameInstance::Instance->AudioManager;

	if (SelectActionData)
	{
		if (IsStand)//恢复站立
		{
			StopAction();
			if (IsValid(AudioManager))
			{
				AudioManager->StopVoice();
			}
		}
		else
		{
			if (IsSelect_)
			{
				PlayAction(SelectActionData->AnimationName);
				if (IsValid(AudioManager))
				{
					//随机播放对应阵营门派语音
					if (OfflineTime == 0)
					{
						int32 Number = FMath::RandRange(0, SelectActionData->RoleVoiceID.Num() - 1);
						FCClientVoiceComplete ClientVoiceCreate;
						AudioManager->ClientVoicePlay(SelectActionData->RoleVoiceID[Number], ClientVoiceCreate);
						return;
					}

					//服务器的OfflineTime是存的UTC世界时间
					int64 OfflineSeconds = UGolbalBPFunctionLibrary::GetFromUnixTimestamp(true) - OfflineTime;
					TArray<FString> RoleVoiceID; 
					if (OfflineSeconds < 24 * 60 * 60)
					{
						RoleVoiceID = SelectActionData->RoleVoiceID;
					}
					else if (OfflineSeconds < 72 * 60 * 60)
					{
						RoleVoiceID = SelectActionData->RoleVoiceID_1;
					}
					else if (OfflineSeconds < 168 * 60 * 60)
					{
						RoleVoiceID = SelectActionData->RoleVoiceID_2;
					}
					else if (OfflineSeconds < 720 * 60 * 60)
					{
						RoleVoiceID = SelectActionData->RoleVoiceID_3;
					}
					else
					{
						RoleVoiceID = SelectActionData->RoleVoiceID_4;
					}
					int32 Number = FMath::RandRange(0, RoleVoiceID.Num() - 1);
					FCClientVoiceComplete ClientVoiceCreate;
					AudioManager->ClientVoicePlay(RoleVoiceID[Number], ClientVoiceCreate);
				}
			}
		}
	}
}

void ALoginCharacter::PlayLoginCreatAction(bool IsStand)
{
	CS3_Display(CS3DebugType::CL_Login, TEXT("LoginCharacter::PlayLoginCreatAction IsStand=%d"), IsStand);
	//获取配置表
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;

	//获取角色阵营信息
	const FRoleCreateUIData* pRoleDefaultData = CfgManager->GetTableByType(
		CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_CREATE)->GetRow<FRoleCreateUIData>(INT_TO_FSTRING(Index));

	FString ScriptID;

	//获取阵营和职业
	if (pRoleDefaultData)
	{
		ScriptID = INT_TO_FSTRING(pRoleDefaultData->RoleCamp) + INT_TO_FSTRING(pRoleDefaultData->RoleProfession);
	}

	//通过阵营和职业ID获取其执行动作
	const FSELECT_CREAT_ACTION_DATE* CreateActionData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SELECT_CREAT_ACTION)->GetRow<FSELECT_CREAT_ACTION_DATE>(ScriptID);
	AAudioManager* AudioManager = UUECS3GameInstance::Instance->AudioManager;

	if (CreateActionData)
	{
		if (IsStand)
		{
			StopAction();
		}
		else
		{
			PlayAction(CreateActionData->AnimationGroupName);
		}
	}
}

void ALoginCharacter::SetModelLight(bool IsLight)
{
	CS3_Display(CS3DebugType::CL_Login, TEXT("LoginCharacter::SetModelLight IsLight=%d"), IsLight);
	TArray<UActorComponent*> Componests = GetComponentsByClass(UMeshComponent::StaticClass());
	for (int32 i = 0; i < Componests.Num(); i++)
	{
		UMeshComponent* MeshCmt = Cast<UMeshComponent>(Componests[i]);
		if (IsValid(MeshCmt))
		{
			MeshCmt->SetRenderCustomDepth(IsLight);
		}
	}
}

void ALoginCharacter::OnCreateApperanceOver()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GameStatus)
		&& (UUECS3GameInstance::Instance->GameStatus->GetLastStatus() == EGameStatus::SelectRole ||
		UUECS3GameInstance::Instance->GameStatus->GetLastStatus() == EGameStatus::CreateRole)
		&& UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::Teleport)
	{
		return;
	}
	Super::OnCreateApperanceOver();
	if (IsValid(RoleLevelActor))
	{
		RoleLevelActor->OnCreateModelFinished();
	}

	//加载完成后检测部件隐显
	if (IsValid(GetBaseAnimInstance()))
	{
		CheckPartHideByAction(GetBaseAnimInstance()->GetCurPlayActionData());
	}
	
	UGolbalBPFunctionLibrary::ModifyFaceManager()->SetModifyData();
	UGolbalBPFunctionLibrary::ModifyFaceManager()->SetBoneRef(this);
	///更新脸部数据
	for (int i = 0; i < Bonedatas.Num(); i++)
	{
		TArray<FString> boneDatas = UGolbalBPFunctionLibrary::SplitString(Bonedatas[i]);
		FTransform boneTran = FTransform();
		boneTran.SetLocation(FVector(FSTRING_TO_FLOAT(boneDatas[0]), FSTRING_TO_FLOAT(boneDatas[1]), FSTRING_TO_FLOAT(boneDatas[2])));
		boneTran.SetRotation(FQuat(FVector(FSTRING_TO_FLOAT(boneDatas[3]), FSTRING_TO_FLOAT(boneDatas[4]), FSTRING_TO_FLOAT(boneDatas[5])), 0.0f));
		boneTran.SetScale3D(FVector(FSTRING_TO_FLOAT(boneDatas[6]), FSTRING_TO_FLOAT(boneDatas[7]), FSTRING_TO_FLOAT(boneDatas[8])));
		UGolbalBPFunctionLibrary::ModifyFaceManager()->SetBoneTrans(this, FSTRING_TO_FNAME(BoneNames[i]), false, boneTran);
	}
	if (IsValid(UGolbalBPFunctionLibrary::ModifyFaceManager()))
	{
		UGolbalBPFunctionLibrary::ModifyFaceManager()->SetModelFaceStyle(this, FaceStyleDatas);
	}
}

void ALoginCharacter::OnChangePartOver()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GameStatus)
		&& (UUECS3GameInstance::Instance->GameStatus->GetLastStatus() == EGameStatus::SelectRole ||
			UUECS3GameInstance::Instance->GameStatus->GetLastStatus() == EGameStatus::CreateRole)
		&& UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::Teleport)
	{
		return;
	}

	if (IsValid(RoleLevelActor))
	{
		RoleLevelActor->OnCreateModelFinished();
	}
}

void ALoginCharacter::SetRoleLevelActor(ACS3LevelScriptActor *InRoleLevelActor)
{
	RoleLevelActor = InRoleLevelActor;
}


CONTROL_COMPILE_OPTIMIZE_END
