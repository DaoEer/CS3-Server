// Fill out your copyright notice in the Description page of Project Settings.
#include "InWorldLevel.h"

#include "CoreMinimal.h"

#include "Manager/LoaderManager.h"
#include "Manager/LoginManager.h"
#include "KBEngine.h"
#include "Util/CS3Debug.h"
#include "Entity.h"
#include "CS3Base/CS3Entity.h"
#include "Util/GolbalBPFunctionLibrary.h"

#include "Actor/Player/PlayerCharacter.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/LevelStreaming.h"
#include "Manager/LevelManager.h"
#include "Manager/CustomTimerManager.h"

CONTROL_COMPILE_OPTIMIZE_START


void AInWorldLevel::BeginPlay()
{
	Super::BeginPlay();
	
	//ShowLoadingWidget();
	GEngine->RedrawViewports(true);
	
	KBEngine::Entity* PlayerEntity = nullptr;
	FVector PlayerPos;
	if (UUECS3GameInstance::pKBEApp != nullptr)
	{
		PlayerEntity = UUECS3GameInstance::pKBEApp->Player();
	}
	if (PlayerEntity != nullptr)
	{
		PlayerPos = PlayerEntity->Position();
		ULevelManager* LevelManager = UGolbalBPFunctionLibrary::LevelManager();
		if (IsValid(LevelManager))
		{
			if (LevelManager->GetIsLoadAllOtherLevelAfterSplit())
			{
				AddAllSubLevelsByPosition(PlayerPos);
			}
			else
			{
				PrimaryActorTick.bCanEverTick = false;
			}
			if (LevelManager->GetIsLoadNineSubLevelAfterSplit())
			{
				LoadSubLevelsByPositionInInit(PlayerPos);
			}
			else
			{
				IsBlockLevelFinished = true;
			}
		}
	}


}

bool AInWorldLevel::CheckLoginRun()
{
	if (Super::CheckLoginRun())
	{
		if (UUECS3GameInstance::pKBEApp == nullptr)	return false; 	//直接打开某关卡播放，如果不是登录进来的，就不执行下面内容逻辑
	}
	else
	{
		return false;
	}
	return true;
}
void AInWorldLevel::CreateDynamicRes()
{

}

void AInWorldLevel::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
	
	SetActorTickEnabled(false);
}

void AInWorldLevel::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	KBEngine::Entity* PlayerEntity = nullptr;
	FVector PlayerPos;
	if (UUECS3GameInstance::pKBEApp != nullptr)
	{
		PlayerEntity = UUECS3GameInstance::pKBEApp->Player();
	}
	if (PlayerEntity != nullptr)
	{
		PlayerPos = PlayerEntity->Position();
		UpdateSubLevelsByPosition(PlayerPos);
	}
}

void AInWorldLevel::LoadSubLevelsByPositionInInit(const FVector& Position)
{
	TArray<FString> SubLevels,MoreSubLevels;
	SubLevels = GetNineSubLevelsByPosition(Position);
	CurrentLoadedSubLevels = SubLevels;
	for (auto SubLevel: SubLevels)
	{
		FLatentActionInfo LatentInfo;
		LatentInfo.CallbackTarget = this;
		LatentInfo.ExecutionFunction = FName(TEXT("LoadBlockStreamLevelFinished"));
		LatentInfo.UUID = UGolbalBPFunctionLibrary::LevelManager()->GetUUID();
		LatentInfo.Linkage = 0;
		UGameplayStatics::LoadStreamLevel(this, FName(*SubLevel), true, true, LatentInfo);
		
	}
	if (LoadedBlockNum == AllBlockLoadedSubLevels.Num())
	{
		IsBlockLevelFinished = true;
	}

}

void AInWorldLevel::UpdateSubLevelsByPosition(const FVector& Position)
{
	if (SortedAllSubLevels.Num() == 0)
	{
		return;
	}
	for (int32 i=0; i<4; ++i)
	{
		if (SortedAllSubLevels.Num() == 0)
		{
			break;
		}
		FString SubLevel = SortedAllSubLevels[0];
		SortedAllSubLevels.Remove(SubLevel);
		FLatentActionInfo LatentInfo;
		LatentInfo.CallbackTarget = this;
		LatentInfo.UUID = UGolbalBPFunctionLibrary::LevelManager()->GetUUID();
		LatentInfo.Linkage = 0;
		UGameplayStatics::LoadStreamLevel(this, FName(*SubLevel), true, false, LatentInfo);
		CurrentLoadedSubLevels.AddUnique(SubLevel);
	}
	//TArray<FString> SubLevels;
	//SubLevels = GetSubLevelByPosition(Position, 7);
	//if (SubLevels == CurrentLoadedSubLevels)
	//{
	//	return;
	//}
	//for (auto SubLevel : SubLevels)
	//{
	//	if (!CurrentLoadedSubLevels.Contains(SubLevel))
	//	{
	//		FLatentActionInfo LatentInfo;
	//		LatentInfo.CallbackTarget = this;
	//		LatentInfo.UUID = UGolbalBPFunctionLibrary::LevelManager()->GetUUID();
	//		LatentInfo.Linkage = 0;
	//		UGameplayStatics::LoadStreamLevel(this, FName(*SubLevel), true, false, LatentInfo);
	//	}
	//}
	//for (auto CurrentSubLevel : CurrentLoadedSubLevels)
	//{
	//	if (!SubLevels.Contains(CurrentSubLevel))
	//	{
	//		FLatentActionInfo LatentInfo;
	//		UGameplayStatics::UnloadStreamLevel(this, FName(*CurrentSubLevel), LatentInfo);
	//	}
	//}
	//CurrentLoadedSubLevels = SubLevels;
}

TArray<FString> AInWorldLevel::GetCurrLoadedSubLevels()
{
	return CurrentLoadedSubLevels;
}

FString AInWorldLevel::GetCurrentSubLevelByPosition(const FVector& Position)
{
	FName CurrentLevelName = UGolbalBPFunctionLibrary::LevelManager()->GetCurrLevelName();
	int32 PlayerX = FMath::FloorToInt(Position.X);
	int32 PlayerY = FMath::FloorToInt(Position.Y);
	int32 SplitXNum = PlayerX > 0 ? FMath::DivideAndRoundUp(PlayerX, SplitLength) : FMath::DivideAndRoundDown(PlayerX, SplitLength);
	int32 SplitYNum = PlayerY > 0 ? FMath::DivideAndRoundUp(PlayerY, SplitLength) : FMath::DivideAndRoundDown(PlayerY, SplitLength);
	int32 RightX = (SplitXNum * SplitLength == PlayerX ? SplitXNum + 1 : SplitXNum);
	int32 TopY = (SplitYNum * SplitLength == PlayerY ? SplitYNum + 1 : SplitYNum);
	FString Filename = CurrentLevelName.ToString();
	Filename = Filename + TEXT("_") + (RightX - 1 < 0 ? TEXT("M") + FString::FromInt(FMath::Abs(RightX - 1)) : TEXT("P") + FString::FromInt(FMath::Abs(RightX - 1)));
	Filename = Filename + TEXT("_") + (TopY - 1 < 0 ? TEXT("M") + FString::FromInt(FMath::Abs(TopY - 1)) : TEXT("P") + FString::FromInt(FMath::Abs(TopY - 1)));
	Filename = Filename + TEXT("_") + (RightX < 0 ? TEXT("M") + FString::FromInt(FMath::Abs(RightX)) : TEXT("P") + FString::FromInt(FMath::Abs(RightX)));
	Filename = Filename + TEXT("_") + (TopY < 0 ? TEXT("M") + FString::FromInt(FMath::Abs(TopY)) : TEXT("P") + FString::FromInt(FMath::Abs(TopY)));
	return Filename;
}

TArray<FString> AInWorldLevel::GetNineSubLevelsByPosition(const FVector& Position)
{
	return GetSubLevelByPosition(Position, 3);
}

TArray<FString> AInWorldLevel::GetSubLevelByPosition(const FVector& Position, const int32& length)
{
	TArray<FString> SubLevels;
	int32 DistFromCenter = length / 2;
	if (length % 2 == 0)
	{
		return SubLevels;
	}
	else
	{
		FName CurrentLevelName = UGolbalBPFunctionLibrary::LevelManager()->GetCurrLevelName();
		int32 PlayerX = FMath::FloorToInt(Position.X);
		int32 PlayerY = FMath::FloorToInt(Position.Y);
		int32 SplitXNum = PlayerX > 0 ? FMath::DivideAndRoundUp(PlayerX, SplitLength) : FMath::DivideAndRoundDown(PlayerX, SplitLength);
		int32 SplitYNum = PlayerY > 0 ? FMath::DivideAndRoundUp(PlayerY, SplitLength) : FMath::DivideAndRoundDown(PlayerY, SplitLength);
		int32 RightX = (SplitXNum * SplitLength == PlayerX ? SplitXNum + 1 : SplitXNum);
		int32 TopY = (SplitYNum * SplitLength == PlayerY ? SplitYNum + 1 : SplitYNum);
		int32 CurrentX = RightX - DistFromCenter;
		int32 CurrentY = TopY + DistFromCenter;


		while (CurrentX <= RightX + DistFromCenter && CurrentY >= TopY - DistFromCenter)
		{
			FString CurrentLevel = CurrentLevelName.ToString();
			TArray<FString> CurrentLevelList = UGolbalBPFunctionLibrary::SplitString(CurrentLevel);
			if (CurrentLevelList.Num() > 0)
			{
				for (auto Level: CurrentLevelList)	//这里这样做是为了防止像凤鸣南麓一样可能子关卡有重叠区域，以及不确定切分后的子关卡属于之前哪一个子关卡。
				{
					FString Filename = Level;
					Filename = Filename + TEXT("_") + (CurrentX - 1 < 0 ? TEXT("M") + FString::FromInt(FMath::Abs(CurrentX - 1)) : TEXT("P") + FString::FromInt(FMath::Abs(CurrentX - 1)));
					Filename = Filename + TEXT("_") + (CurrentY - 1 < 0 ? TEXT("M") + FString::FromInt(FMath::Abs(CurrentY - 1)) : TEXT("P") + FString::FromInt(FMath::Abs(CurrentY - 1)));
					Filename = Filename + TEXT("_") + (CurrentX < 0 ? TEXT("M") + FString::FromInt(FMath::Abs(CurrentX)) : TEXT("P") + FString::FromInt(FMath::Abs(CurrentX)));
					Filename = Filename + TEXT("_") + (CurrentY < 0 ? TEXT("M") + FString::FromInt(FMath::Abs(CurrentY)) : TEXT("P") + FString::FromInt(FMath::Abs(CurrentY)));
					if (AllSubLevels.Contains(Filename))
					{
						SubLevels.AddUnique(Filename);
					}
				}
			}
			if (CurrentX == RightX + DistFromCenter)
			{
				CurrentX = RightX - DistFromCenter;
				CurrentY = CurrentY - 1;
			}
			else
			{
				CurrentX = CurrentX + 1;
			}
		}
	}

	return SubLevels;
}

ULevelStreaming* AInWorldLevel::FindSubLevelStreamingObject(FName SubLevel)
{
	if (SubLevel == NAME_None)
	{
		return nullptr;
	}
	UWorld* InWorld = GetWorld();
	FString SearchPackageName;
	// Special case for PIE, the PackageName gets mangled.
	if (!InWorld->StreamingLevelsPrefix.IsEmpty())
	{
		FString PackageName = FPackageName::GetShortName(SubLevel);
		if (!PackageName.StartsWith(InWorld->StreamingLevelsPrefix))
		{
			PackageName = InWorld->StreamingLevelsPrefix + PackageName;
		}

		if (!FPackageName::IsShortPackageName(SubLevel))
		{
			PackageName = FPackageName::GetLongPackagePath(SubLevel.ToString()) + TEXT("/") + PackageName;
		}

		SearchPackageName = PackageName;
	}
	else
	{
		SearchPackageName = SubLevel.ToString();
	}

	if (FPackageName::IsShortPackageName(SearchPackageName))
	{
		// Make sure MyMap1 and Map1 names do not resolve to a same streaming level
		SearchPackageName = TEXT("/") + SearchPackageName;
	}

	for (ULevelStreaming* LevelStreaming : InWorld->GetStreamingLevels())
	{
		// We check only suffix of package name, to handle situations when packages were saved for play into a temporary folder
		// Like Saved/Autosaves/PackageName
		if (LevelStreaming &&
			LevelStreaming->GetWorldAssetPackageName().EndsWith(SearchPackageName, ESearchCase::IgnoreCase))
		{
			return LevelStreaming;
		}
	}

	return nullptr;
}

TArray<FString> AInWorldLevel::GetAllSubStreamingLevels()
{
	UWorld* InWorld = GetWorld();
	TArray<FString> AllSubStreamingLevels;
	TArray<FString> AlwaysLoadedStreamingLevels;
	FName CurrentLevelName = UGolbalBPFunctionLibrary::LevelManager()->GetCurrLevelName();
	FString CurrentLevel = CurrentLevelName.ToString();
	TArray<FString> CurrentLevelList = UGolbalBPFunctionLibrary::SplitString(CurrentLevel);
	for (ULevelStreaming* LevelStreaming : InWorld->GetStreamingLevels())
	{
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

			if (!LevelStreaming->ShouldBeAlwaysLoaded())
			{
				if (!LevelStreaming->HasLoadedLevel() && !LevelName.IsEmpty() && !CurrentLevelList.Contains(LevelName))
				{
					AllSubStreamingLevels.AddUnique(LevelName);
				}
			}
			else
			{
				AlwaysLoadedStreamingLevels.AddUnique(LevelName);
			}
		}
		
	}
	//if (AlwaysLoadedStreamingLevels.Num() > CurrentLevelList.Num())
	//{
	//	CS3_Warning(TEXT("AInWorldLevel::GetAllSubStreamingLevels[ HashMapTable Config Error(num of CurrentLevelList:%d, first item:%s)]"), CurrentLevelList.Num(), *CurrentLevelList[0]);
	//	AllSubStreamingLevels.Empty();
	//	return AllSubStreamingLevels;
	//}
	TArray<FString> TempSubLevels = AllSubStreamingLevels;
	for (auto StreamingLevel: TempSubLevels)
	{
		bool IsStartWithLoadedLevel = false;
		for (auto AlwaysLoadedLevel : AlwaysLoadedStreamingLevels)
		{
			if (StreamingLevel.StartsWith(AlwaysLoadedLevel))
			{
				IsStartWithLoadedLevel = true;
				break;
			}
		}
		if (!IsStartWithLoadedLevel)
		{
			AllSubStreamingLevels.Remove(StreamingLevel);

		}
	}
	
	return AllSubStreamingLevels;
}

void AInWorldLevel::AddAllSubLevelsByPosition(const FVector& Position)
{
	int32 length = 5;
	AllSubLevels = GetAllSubStreamingLevels();
	TArray<FString> AllFoliageSubLevels;
	for (auto SubLevel: AllSubLevels)
	{
		if (SubLevel.EndsWith("_FoliageLevel"))
		{
			AllFoliageSubLevels.AddUnique(SubLevel);
		}
	}
	AllBlockLoadedSubLevels = GetNineSubLevelsByPosition(Position);
	
	while (AllSubLevels.Num() != 0)
	{
		TArray<FString> SubLevels = GetSubLevelByPosition(Position, length);
		TArray<FString> LastSubLevels = GetSubLevelByPosition(Position, length - 2);
		for (auto SubLevel: SubLevels)
		{
			if (!LastSubLevels.Contains(SubLevel) && AllSubLevels.Contains(SubLevel) && !AllFoliageSubLevels.Contains(SubLevel))
			{
				SortedAllSubLevels.AddUnique(SubLevel);
			}
		}
		if (SortedAllSubLevels.Num() + AllBlockLoadedSubLevels.Num() == AllSubLevels.Num() - AllFoliageSubLevels.Num())
		{
			SortedAllSubLevels.Append(AllFoliageSubLevels);
			break;
		}
		length += 2;

	}
}

void AInWorldLevel::LoadBlockStreamLevelFinished()
{
	LoadedBlockNum += 1;
	if (LoadedBlockNum == AllBlockLoadedSubLevels.Num())
	{
		IsBlockLevelFinished = true;
		if (IsLoadLevelFinished)
		{
			UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportNormalLevel();
		}
	}
}

void AInWorldLevel::BeginDestroy()
{
	Super::BeginDestroy();
}


void AInWorldLevel::ShowLoadingWidget()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::ShowLoadingWidget---------------"));
	////显示加载进度条
	FEndLoadCallBack EndCallBack;
	if (UGolbalBPFunctionLibrary::LoginManager()->bIsFirstEnterWorld)
	{
		UGolbalBPFunctionLibrary::GLoaderManager()->LoadWorldSpace(EndCallBack); 
	}
	else
	{
		UGolbalBPFunctionLibrary::GLoaderManager()->LoadTeleportSpace(EndCallBack);
	}
}

void AInWorldLevel::OnLoadLevelFinished()
{
	CS3_Display(CS3DebugType::CL_Level, TEXT("CS3LevelScriptActor::OnLoadLevelFinished---------------"));
	IsLoadLevelFinished = true;
	if (IsBlockLevelFinished)
	{
		UGolbalBPFunctionLibrary::LevelManager()->OnEndTeleportNormalLevel();
	}
	if (DelayLoadFinishedHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayLoadFinishedHandle);
	}
	
}

CONTROL_COMPILE_OPTIMIZE_END
