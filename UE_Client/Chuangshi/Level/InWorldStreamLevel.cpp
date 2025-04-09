// Fill out your copyright notice in the Description page of Project Settings.


#include "InWorldStreamLevel.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/LevelManager.h"
#include "Engine/LevelStreaming.h"
#include "Manager/CfgManager.h"
#include "Interface/Role/RoleSpaceInterface.h"
#include "Engine/LevelStreamingVolume.h"
#include "Manager/GameStatus.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Kismet/GameplayStatics.h"


CONTROL_COMPILE_OPTIMIZE_START


void AInWorldStreamLevel::BeginPlay()
{
	Super::BeginPlay();
	CurSubLevelName = TEXT("");///<当前的子关卡
	OldSubLevelName = TEXT("");///<前一个子关卡
	NextSubLevelName = TEXT("");///<下一个子关卡
	NewSubLevelName = TEXT("");///<新的子关卡
	IsLoadNextSubLevelFinished = false;///<下一个子关卡是否加载完成
	IsLoadSubLevelFinished = false; ///<当前子关卡是否加载完成
	IsLoadNextSubLevelFinished = false; ///<下个子关卡是否加载完成
	IsLoadStreamingLevel = false; ///<是否加载主场景流关卡
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GameStatus))
	{
		UUECS3GameInstance::Instance->GameStatus->InWorldLoadingOver.AddDynamic(this, &AInWorldStreamLevel::PostChangeInWorldOver);
	}
	LoadDefaultSubLevel();
}

void AInWorldStreamLevel::OnLoadLevelFinished()
{
	IsLoadLevelFinished = true;
	if (IsBlockLevelFinished && IsLoadSubLevelFinished)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::OnLoadLevelFinished ------"));
		UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportNormalLevel();
	}
}

void AInWorldStreamLevel::ChangeToNextSubLevel(FName LevelName)
{	
	if (!LevelName.Compare(TEXT(""))) return;
	///<切换的关卡与下一个子关卡不一致
	if ((LevelName.ToString()).Compare(NextSubLevelName)) 
	{
		NextSubLevelName = FNAME_TO_FSTRING(LevelName);
		NewSubLevelName = NextSubLevelName;
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::ChangeToNextSubLevel LevelName not Compare NextSubLevelName NextSubLevelName=%s"),*NextSubLevelName);
		LoadNextSubLevel(true);
	}
	else
	{
		///<下一个子关卡已加载完成
		if (IsLoadNextSubLevelFinished)
		{
			NewSubLevelName = TEXT("");
			OldSubLevelName = CurSubLevelName;
			CurSubLevelName = NextSubLevelName;
			///< 获取下一个子关卡名
			SetNextSubLevelName();
			///<显示当前子关卡
			UpdateSubLevelVisiblity(FSTRING_TO_FNAME(CurSubLevelName), FSTRING_TO_FNAME(OldSubLevelName));
			IsLoadNextSubLevelFinished = false;
			IsLoadSubLevelFinished = true;
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::ChangeToNextSubLevel IsLoadNextSubLevelFinished=TRUE CurSubLevelName=%s NextSubLevelName=%s"), *CurSubLevelName,*NextSubLevelName);
		}
		else
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::ChangeToNextSubLevel IsLoadNextSubLevelFinished=FALSE CurSubLevelName=%s NextSubLevelName=%s"), *CurSubLevelName, *NextSubLevelName);
			NewSubLevelName = NextSubLevelName;
		}
	}
}

void AInWorldStreamLevel::PostChangeInWorldOver()
{
	///<旧的关卡和下一个关卡一样就不用加载下一个关卡和卸载下一个关卡
	if (!OldSubLevelName.Compare(NextSubLevelName) && NextSubLevelName.Compare(TEXT("")))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::PostChangeInWorldOver   OldSubLevelName Compare NextSubLevelName CurSubLevelName=%s NextSubLevelName=%s"), *CurSubLevelName, *NextSubLevelName);

		///<通知已加载完成
		LoadNextSubLevelFinished();
	}
	else
	{
		if (!NextSubLevelName.Compare(TEXT("")))
		{
			SetNextSubLevelName();
		}
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::PostChangeInWorldOver CurSubLevelName=%s NextSubLevelName=%s"), *CurSubLevelName, *NextSubLevelName);
		///<卸载之前的子关卡
		//UnLoadSubLevelByLevelName(FSTRING_TO_FNAME(OldSubLevelName));
		///<加载下一个子关卡
		LoadNextSubLevel();		
	}
}

bool AInWorldStreamLevel::IsCompareLevelManagerSubStreamLevel(FName LevelName)
{
	if (!LevelName.IsNone()&&!UGolbalBPFunctionLibrary::LevelManager()->GetSubStreamLevelName().IsNone())
	{
		return !(LevelName.Compare(UGolbalBPFunctionLibrary::LevelManager()->GetCurrLevelName()));
	}
	return false;
}

void AInWorldStreamLevel::LoadLevelStreamingByLevelName(FName LevelName)
{
	UWorld* InWorld = GetWorld();
	if (InWorld && !LevelName.IsNone())
	{
		IsLoadStreamingLevel = true;
		FString LevelNameString = LevelName.ToString();
		LevelNameString.RemoveFromEnd("01");
		for (ULevelStreaming* LevelStreaming : InWorld->GetStreamingLevels())
		{
			FString FileName = FPaths::GetCleanFilename(LevelStreaming->GetWorldAssetPackageName());
			FString LevelStreamingName;
			if (!InWorld->StreamingLevelsPrefix.IsEmpty())
			{
				FString Left;
				FileName.Split(InWorld->StreamingLevelsPrefix, &Left, &LevelStreamingName);
			}
			else
			{
				LevelStreamingName = FileName;
			}
			if (LevelStreamingName.Contains(LevelNameString))
			{
				LoadSubLevelByLevelName(FName(*LevelStreamingName), false, false, TEXT(""));
			}
		}
	}
}

void AInWorldStreamLevel::UpdateStreamingVolume()
{
	UWorld* InWorld = GetWorld();
	if (InWorld)
	{
		TEnumAsByte<enum EStreamingVolumeUsage> StreamingVolumeUsage = IsCompareLevelManagerSubStreamLevel(FSTRING_TO_FNAME(CurSubLevelName))? (EStreamingVolumeUsage::SVB_LoadingAndVisibility) : (EStreamingVolumeUsage::SVB_LoadingNotVisible);
		
		for (ULevelStreaming* LevelStreaming : InWorld->GetStreamingLevels())
		{
			//<隐藏流送体积的可见性
			for (ALevelStreamingVolume* StreamingVolume : LevelStreaming->EditorStreamingVolumes)
			{
				StreamingVolume->bDisabled = false;
				StreamingVolume->StreamingUsage = StreamingVolumeUsage;
				if (StreamingVolumeUsage == EStreamingVolumeUsage::SVB_LoadingAndVisibility) 
				{				
					TArray<FName> StreamingLevelFileNames = StreamingVolume->StreamingLevelNames;
					for (int32 i = 0; i < StreamingLevelFileNames.Num(); i++)
					{
						TArray<FString> SplitStrings = UGolbalBPFunctionLibrary::SplitString(FNAME_TO_FSTRING(StreamingLevelFileNames[i]), false, "/");
						if (SplitStrings.Num() > 0)
						{
							LoadSubLevelByLevelName(FName(*(SplitStrings.Last())), true, true, TEXT(""));
						}
					}
				}
			}
		}
	}
}

void AInWorldStreamLevel::SetNextSubLevelName()
{
	NextSubLevelName = TEXT("");
	URoleSpaceInterface * RoleSpaceInterface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface")));

	if (RoleSpaceInterface&&RoleSpaceInterface->IsHZMGLevel() && UGolbalBPFunctionLibrary::LevelManager())
	{
		auto newlevelHash = UGolbalBPFunctionLibrary::LevelManager()->GetLevelHashMapData(FSTRING_TO_FNAME((RoleSpaceInterface->GetVideoLoadLevelData()).NextLevel));

		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::SetNextSubLevelName() GetVideoLoadLevelData.NextLevel=%s"), *(RoleSpaceInterface->GetVideoLoadLevelData()).NextLevel);

		if (newlevelHash && !newlevelHash->SubStreamLevelName.IsNone())
		{
			NextSubLevelName = FNAME_TO_FSTRING(newlevelHash->SubStreamLevelName);
		}
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::SetNextSubLevelName() CurSubLevelName=%s NextSubLevelName=%s"), *CurSubLevelName, *NextSubLevelName);

}

void AInWorldStreamLevel::LoadSubLevelByLevelName(const FName LevelName, bool bMakeVisibleAfterLoad, bool bShouldBlockOnLoad, FName ExecutionFunction)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("AInWorldStreamLevel::LoadSubLevelByLevelName LevelName=%s,bMakeVisibleAfterLoad=%d,bShouldBlockOnLoad=%d,ExecutionFunction=%s"), *FNAME_TO_FSTRING(LevelName), bMakeVisibleAfterLoad, bShouldBlockOnLoad, *FNAME_TO_FSTRING(ExecutionFunction));

	if (!LevelName.IsNone())
	{
		FLatentActionInfo LatentInfo;
		LatentInfo.CallbackTarget = this;
		LatentInfo.ExecutionFunction = ExecutionFunction;
		LatentInfo.UUID = UGolbalBPFunctionLibrary::LevelManager()->GetUUID();
		LatentInfo.Linkage = 0;
		UGameplayStatics::LoadStreamLevel(this, LevelName, bMakeVisibleAfterLoad, bShouldBlockOnLoad, LatentInfo);
	}
}

void AInWorldStreamLevel::LoadDefaultSubLevel()
{
	IsLoadSubLevelFinished = true;
	auto newlevelHash = UGolbalBPFunctionLibrary::LevelManager()->GetLevelHashMapData(UGolbalBPFunctionLibrary::LevelManager()->spaceScriptID);

	if (newlevelHash)
	{
		///<获取当前应该切换的子关卡
		if (!UGolbalBPFunctionLibrary::LevelManager()->GetSubStreamLevelName().IsNone())
		{
			CurSubLevelName = UGolbalBPFunctionLibrary::LevelManager()->GetSubStreamLevelName().ToString();
		}
	}

	if (CurSubLevelName.Compare(TEXT("")))
	{
		IsLoadSubLevelFinished = false;
		///<更新流送体积的参数，避免直接进入某个副本出现主场景的岛屿
		UpdateStreamingVolume();
		LoadSubLevelByLevelName(FName(*CurSubLevelName), true, true, TEXT("LoadDefaultSubLevelFinished"));
	}
	else
	{
		////<配置表中没有数据获取第一个子关卡
		UWorld* InWorld = GetWorld();
		if (InWorld && InWorld->GetStreamingLevels().Num() > 0)
		{
			const ULevelStreaming* LevelStreaming = InWorld->GetStreamingLevels()[0];
			if (LevelStreaming)
			{
				FString FileName = FPaths::GetCleanFilename(LevelStreaming->GetWorldAssetPackageName());
				FString LevelName;
				if (!InWorld->StreamingLevelsPrefix.IsEmpty())
				{
					FString Left;
					FileName.Split(InWorld->StreamingLevelsPrefix, &Left, &LevelName);
				}
				else
				{
					LevelName = FileName;
				}
				CurSubLevelName = LevelName;
				IsLoadSubLevelFinished = false;
				///<更新流送体积的参数，避免直接进入某个副本出现主场景的岛屿
				UpdateStreamingVolume();
				LoadSubLevelByLevelName(FName(*CurSubLevelName), true, true, TEXT("LoadDefaultSubLevelFinished"));
			}
		}
	}
	 
	///< 获取下一个子关卡名
	SetNextSubLevelName();
}

void AInWorldStreamLevel::LoadDefaultSubLevelFinished()
{
	UpdateSubLevelVisiblity(FSTRING_TO_FNAME(CurSubLevelName),TEXT(""));

	///<延时1.5s通知关卡切换完成避免穿帮
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayNotifyLoadFinishedHandle, this, &AInWorldStreamLevel::DelayNotifyLoadDefaultSubLevelFinished, 1.5f, false);
}

void AInWorldStreamLevel::DelayNotifyLoadDefaultSubLevelFinished()
{
	///<通知加载完成
	IsLoadSubLevelFinished = true;
	if (IsLoadLevelFinished)
	{
		OnLoadLevelFinished();
	}
}

void AInWorldStreamLevel::LoadNextSubLevel(bool bIsShow/* = false*/)
{
	if (NextSubLevelName.Compare(TEXT("")))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::LoadNextSubLevel() CurSubLevelName=%s NextSubLevelName=%s"), *CurSubLevelName, *NextSubLevelName);

		LoadSubLevelByLevelName(FName(*NextSubLevelName), bIsShow, false, TEXT("LoadNextSubLevelFinished"));
		if (IsCompareLevelManagerSubStreamLevel(FName(*NextSubLevelName)) && !IsLoadStreamingLevel)
		{
			LoadLevelStreamingByLevelName(FName(*NextSubLevelName));
		}
	}
}

void AInWorldStreamLevel::LoadNextSubLevelFinished()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::LoadNextSubLevelFinished() CurSubLevelName=%s NextSubLevelName=%s"), *CurSubLevelName, *NextSubLevelName);

	IsLoadNextSubLevelFinished = true;
	LoadNextSubLevelFinishedDelegate.Broadcast(NextSubLevelName);

	///<通知切换下一个子关卡时，下一个子关卡没有加载完成，现加载完成需要切换关卡
	if (!NewSubLevelName.Compare(NextSubLevelName))
	{
		ChangeToNextSubLevel(FSTRING_TO_FNAME(NewSubLevelName));
	}
}

void AInWorldStreamLevel::UpdateSubLevelVisiblity(FName VisibleLevelName, FName InvisibleLevelName)
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("InWorldStreamLevel::UpdateSubLevelVisiblity VisibleLevelName=%s,InvisibleLevelName=%s"), *FNAME_TO_FSTRING(VisibleLevelName), *FNAME_TO_FSTRING(InvisibleLevelName));
	//显示关卡
	UWorld* InWorld = GetWorld();
	if (InWorld)
	{
		TEnumAsByte<enum EStreamingVolumeUsage> StreamingVolumeUsage = IsCompareLevelManagerSubStreamLevel(VisibleLevelName) ? (EStreamingVolumeUsage::SVB_LoadingAndVisibility) : (EStreamingVolumeUsage::SVB_Loading);

		FString InvisibleLevelNameString = InvisibleLevelName.ToString();
		InvisibleLevelNameString.RemoveFromEnd("01");
		FString VisibleLevelNameString = VisibleLevelName.ToString();
		VisibleLevelNameString.RemoveFromEnd("01");
		
		ALevelStreamingVolume* TempStreamingVolume = nullptr;
		TArray<AActor*> FindActors;
		UGameplayStatics::GetAllActorsOfClass(InWorld, ALevelStreamingVolume::StaticClass(), FindActors);
		if (FindActors.Num() > 0)
		{
			for (AActor* actor : FindActors)
			{  ///<设置流送体积的类型和当前显示的是主关卡获取到上次玩家进入的子岛屿 TempStreamingVolume
				ALevelStreamingVolume* StreamingVolume = Cast<ALevelStreamingVolume>(actor);
				if (IsValid(StreamingVolume))
				{
					if (StreamingVolumeUsage == EStreamingVolumeUsage::SVB_LoadingAndVisibility&&LastEntitypostion != FVector::ZeroVector)
					{
						TempStreamingVolume = (TempStreamingVolume == nullptr) ? StreamingVolume : ((FVector::Distance(TempStreamingVolume->GetActorLocation(), LastEntitypostion) > FVector::Distance(StreamingVolume->GetActorLocation(), LastEntitypostion)) ? StreamingVolume : TempStreamingVolume);
					}
					if (StreamingVolume->StreamingUsage == EStreamingVolumeUsage::SVB_LoadingNotVisible&&StreamingVolumeUsage == EStreamingVolumeUsage::SVB_Loading)
					{
						continue;
					}
					StreamingVolume->StreamingUsage = StreamingVolumeUsage;
				}
			}
		}
		TArray<FString> StreamingLevelNames;
		if (IsValid(TempStreamingVolume))
		{
			TArray<FName> StreamingLevelFileNames = TempStreamingVolume->StreamingLevelNames;
			
			for (int32 i = 0; i < StreamingLevelFileNames.Num(); i++)
			{
				TArray<FString> SplitStrings = UGolbalBPFunctionLibrary::SplitString(FNAME_TO_FSTRING(StreamingLevelFileNames[i]), false, "/");
				if (SplitStrings.Num() > 0)
				{
					StreamingLevelNames.Add(SplitStrings.Last());
				}
			}			
		}
		ULevelStreaming* VisibleStreamingLevel = nullptr;
		ULevelStreaming* VisibleStreamingLevelByEntityPosition = nullptr;
		for (ULevelStreaming* LevelStreaming : InWorld->GetStreamingLevels())
		{
			if (!IsValid(LevelStreaming))
			{
				continue;
			}
			FString FileName = FPaths::GetCleanFilename(LevelStreaming->GetWorldAssetPackageName());
			FString LevelName;
			if (!InWorld->StreamingLevelsPrefix.IsEmpty())
			{
				FString Left;
				FileName.Split(InWorld->StreamingLevelsPrefix, &Left, &LevelName);
			}
			else
			{
				LevelName = FileName;
			}
			if (StreamingLevelNames.Num() > 0 && !(StreamingLevelNames[0].Compare(LevelName)))
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::VisibleLevelNameByEntityPosition=%s "), *LevelName);
				VisibleStreamingLevelByEntityPosition = LevelStreaming;
			}			

			if (VisibleLevelName.Compare(TEXT("")) && !LevelName.Compare(VisibleLevelName.ToString()))
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::VisibleLevelName=%s "), *LevelName);
				VisibleStreamingLevel = LevelStreaming;		
			}
			else if (InvisibleLevelName.Compare(TEXT("")) && FileName.Contains(InvisibleLevelNameString) && LevelStreaming->IsLevelVisible())
			{
				InvisibleStreamingLevels.Add(LevelStreaming);
			}			
		}	
		///<优先显示上次玩家位置的子关卡
		if(IsValid(VisibleStreamingLevelByEntityPosition) && 
			(!VisibleStreamingLevelByEntityPosition->IsLevelVisible())&&
			VisibleStreamingLevelByEntityPosition != VisibleStreamingLevel
			)
		{
			VisibleStreamingLevelByEntityPosition->SetShouldBeVisible(true);
		}

		float FinishedTime = 2.0f;
		if (IsValid(VisibleStreamingLevel) && (!VisibleStreamingLevel->IsLevelVisible()))
		{	///<当前这样处理主要是避免子关卡没有加载好物理碰撞没有导致角色掉到地下
			VisibleStreamingLevel->SetShouldBeVisible(true);			
			//LoadSubLevelByLevelName(VisibleLevelName, true, false, TEXT("UpdateSubLevelVisiblityFinished"));//该方法在已加载完成的情况下没有回调 导致一直会卡住进度条
			//UpdateSubLevelVisiblityFinished(4.2f);
			FinishedTime = 4.2f;
		}

		if (InvisibleStreamingLevels.Num() > 0)
		{	
			///<旧的关卡需要卸载
			if (!(!OldSubLevelName.Compare(NextSubLevelName) && NextSubLevelName.Compare(TEXT("")))&&(InvisibleStreamingLevels.Num()==1))
			{
				//FinishedTime += 2.0f;
				UnLoadSubLevelByLevelName(InvisibleLevelName);
			}
			else
			{
				DelaySetInvisibleStreamingLevels();
				UpdateSubLevelVisiblityFinished(FinishedTime);
			}			
		}
		else 
		{
			UpdateSubLevelVisiblityFinished(FinishedTime);
		}
		

		KBEngine::Entity *entity = UUECS3GameInstance::pKBEApp->Player();
		if (entity)
		{
			LastEntitypostion = entity->Position();
		}
	}
}

void AInWorldStreamLevel::UpdateSubLevelVisiblityFinished(float FinishedTime/* = 2.0f*/)
{
	///<延时2s通知关卡切换完成避免穿帮
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayNotifyLoadFinishedHandle, this, &AInWorldStreamLevel::OnLoadLevelFinished, FinishedTime, false);
}

void AInWorldStreamLevel::DelaySetInvisibleStreamingLevels()
{
	UWorld* World = UUECS3GameInstance::Instance->GetWorld();
	if (World)
	{
		TWeakObjectPtr<AInWorldStreamLevel> DelayThisPtr(this);
		World->GetTimerManager().SetTimerForNextTick(FTimerDelegate::CreateLambda([DelayThisPtr]()
		{
			if (DelayThisPtr.IsValid())
			{
				AInWorldStreamLevel* InWorldStreamLevel = DelayThisPtr.Get();
				if (InWorldStreamLevel->InvisibleStreamingLevels.Num() > 0)
				{
					if (IsValid((InWorldStreamLevel->InvisibleStreamingLevels[0])))
					{
						(InWorldStreamLevel->InvisibleStreamingLevels[0])->SetShouldBeVisible(false);
					}
					InWorldStreamLevel->InvisibleStreamingLevels.RemoveAt(0);
					if (InWorldStreamLevel->InvisibleStreamingLevels.Num() > 0)
					{
						InWorldStreamLevel->DelaySetInvisibleStreamingLevels();
					}
				}
			}
		}));
	}
}

void AInWorldStreamLevel::UnLoadSubLevelByLevelName(FName LevelName)
{
	if (!LevelName.IsNone())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::UnLoadSubLevelByLevelName() LevelName=%s"), *FNAME_TO_FSTRING(LevelName));

		FLatentActionInfo LatentInfo;
		LatentInfo.CallbackTarget = this;
		LatentInfo.ExecutionFunction = FName(TEXT("UnLoadSubLevelFinished"));
		LatentInfo.UUID = UGolbalBPFunctionLibrary::LevelManager()->GetUUID();
		LatentInfo.Linkage = 0;
		UGameplayStatics::UnloadStreamLevel(this, LevelName, LatentInfo, false);
	}
}

void AInWorldStreamLevel::UnLoadSubLevelFinished()
{
	UpdateSubLevelVisiblityFinished(0.1f);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AInWorldStreamLevel::UnLoadSubLevelFinished()"));
}

CONTROL_COMPILE_OPTIMIZE_END
