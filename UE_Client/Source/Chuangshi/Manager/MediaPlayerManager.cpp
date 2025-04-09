// Fill out your copyright notice in the Description page of Project Settings.

#include "MediaPlayerManager.h"
#include "ResourceManager.h"
#include "CS3Base/UIManager.h"
#include "AudioManager.h"
#include "GameStatus.h"
#include"Chuangshi.h"
#include "GameStatus.h"
#include "QuestManager.h"
#include "GameDevelop/CS3PlayerController.h"
#include "AtkStateMar.h"
#include "CustomTimerManager.h"
#include "Operation/RoleCtrl/RoleCtrlStateMgr.h"
#include "CS3Base/BaseWindow.h"
#include "Actor/ServerCharacter.h" 
#include "Interface/Role/RoleInterface.h" 


UMediaPlayerManager* UMediaPlayerManager::GetInstance()
{
	cs3_checkNoReentry();
	UMediaPlayerManager * MediaPlayerManager = (UMediaPlayerManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MediaPlayerManager")));
	
	if (IsValid(MediaPlayerManager))
	{
		return MediaPlayerManager;
	}
	return nullptr;
}

void UMediaPlayerManager::OnInitMediaPlayer_Implementation()
{

}

void UMediaPlayerManager::Close(bool bIsForcedClose/* = false*/)
{
	if (IsValid(MediaPlayer) &&(( bIsStopByLoadingOver &&bIsCanStopByMinimumTime)|| bIsForcedClose))
	{
		MediaPlayer->Close();
	}
}

bool UMediaPlayerManager::OpenSource(UMediaSource* MediaSource)
{	
	if (!IsValid(MediaPlayer))
	{
		OnInitMediaPlayer();
	}
	MediaPlayer->OnMediaOpened.AddDynamic(this, &UMediaPlayerManager::OnMediaOpened);
	MediaPlayer->OnMediaOpenFailed.AddDynamic(this, &UMediaPlayerManager::OnMediaOpenFailed);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayerManager::OpenSource~"));
	return MediaPlayer->OpenSource(MediaSource);
}

bool UMediaPlayerManager::Pause()
{
	if (IsValid(MediaPlayer)&& MediaPlayer->CanPause())
	{
		return MediaPlayer->Pause();
	}
	return false;
}

bool UMediaPlayerManager::Play()
{
	/*if (IsValid(MediaPlayer))
	{
		return MediaPlayer->Play();
	}*/
	return false;
}

bool UMediaPlayerManager::Rewind()
{
	if (IsValid(MediaPlayer))
	{
		return MediaPlayer->Rewind();
	}
	return false;
}

bool UMediaPlayerManager::SetRate(float Rate)
{
	if (IsValid(MediaPlayer))
	{
		return MediaPlayer->SetRate(Rate);
	}
	return false;
}

void UMediaPlayerManager::PlayMedia(FString MediaPlayerId)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayerManager::PlayMedia -> MediaId[%s]~"), *MediaPlayerId);
	if (!IsValid(MediaPlayer))
	{
		OnInitMediaPlayer();
	}
	if (MediaPlayer->IsPlaying()|| MediaPlayer->IsPaused())
	{
		ClearMediaEvent();
		Close();
	}

	//播放资源
	const FMEDIA_PLAYER_DATA* MediaPlayerData = GetMediaPlayerData(MediaPlayerId);
	if (MediaPlayerData == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMediaPlayerManager::PlayMedia : MediaPlayerData!"));
		return;
	}

	int AssetAccount = MediaPlayerData->MediaSources.Num();

	if (1 == AssetAccount)
	{
		if (MediaPlayerData->MediaSources[0].ToSoftObjectPath().IsValid())
		{
			GetMediaSource(MediaPlayerData->MediaSources[0], MediaPlayerId);
		}
	}
	else
	{
		int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
		int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
		int32 PlayId = Profession - 1;
		if ((PlayId >= 0) && (PlayId < AssetAccount))
		{
			if (MediaPlayerData->MediaSources[PlayId].ToSoftObjectPath().IsValid())
			{
				GetMediaSource(MediaPlayerData->MediaSources[PlayId], MediaPlayerId);
			}
		}
	}
}

void UMediaPlayerManager::StartPlayMedia(TSoftObjectPtr<UMediaSource> TempMediaAss, const FString& MediaId)
{
	if (IsValid(TempMediaAss.Get()))
	{
		if (OpenSource(TempMediaAss.Get()))
		{
			CurMediaPlayerId = MediaId;
		}
	}
}

void UMediaPlayerManager::GetMediaSource(TSoftObjectPtr<UMediaSource> TempMediaAss, const FString& MediaId)
{
	UMediaSource** MediaAssValue = MediaAssList.Find(MediaId);
	if (MediaAssValue != nullptr && IsValid((*MediaAssValue)))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayerManager::GetMediaSource MediaAssList-> MediaId[%s] ~"), *MediaId);
		StartPlayMedia(*MediaAssValue, MediaId);
		return;
	}
	//已存在直接用
	if (IsValid(TempMediaAss.Get()))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayerManager::GetMediaSource MediaAss.Get()-> MediaId[%s] ~"), *MediaId);
		StartPlayMedia(TempMediaAss.Get(), MediaId);
	}
	else
	{
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, TempMediaAss.ToSoftObjectPath(),
			FStreamableDelegate::CreateLambda([this, TempMediaAss, MediaId]()
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayerManager::GetMediaSource -> MediaId[%s] ~"), *MediaId);
			StartPlayMedia(TempMediaAss.Get(), MediaId);
		}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_MEDIA);
	}
}

void UMediaPlayerManager::OnEndReached()
{
	const FMEDIA_PLAYER_DATA* MediaPlayerData = GetMediaPlayerData(CurMediaPlayerId);
	if (MediaPlayerData &&MediaPlayerData->Loop)		
		return;

	OnMediaStoped();
}

void UMediaPlayerManager::OnMediaClosed()
{
	OnMediaStoped();
}

void UMediaPlayerManager::OnMediaOpened(FString OpenedUrl)
{
	if (OnMediaOpenedDelegate.IsBound())
	{
		OnMediaOpenedDelegate.Broadcast();
	}	

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayerManager::OnMediaOpened -> MediaId[%s]~"), *CurMediaPlayerId);
	if (!MediaPlayer->OnEndReached.IsAlreadyBound(this, &UMediaPlayerManager::OnEndReached))
	{
		MediaPlayer->OnEndReached.AddDynamic(this, &UMediaPlayerManager::OnEndReached);
	}
	if (!MediaPlayer->OnMediaClosed.IsAlreadyBound(this, &UMediaPlayerManager::OnMediaClosed))
	{
		MediaPlayer->OnMediaClosed.AddDynamic(this, &UMediaPlayerManager::OnMediaClosed);
	}
	// 中断所有语音
	if (UGolbalBPFunctionLibrary::AudioManager() && IsValid(UGolbalBPFunctionLibrary::AudioManager()))
	{
		UGolbalBPFunctionLibrary::AudioManager()->StopVoice();
		TArray<FString> HideTypes = { "1","2","3","4","5" };
		UGolbalBPFunctionLibrary::AudioManager()->SetPausedVoice(HideTypes, HideTypes, true);
	}
	OnEnableInput(false);
	
	//播放资源
	const FMEDIA_PLAYER_DATA* MediaPlayerData = GetMediaPlayerData(CurMediaPlayerId);
	if (MediaPlayerData == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMediaPlayerManager::OnMediaOpened : MediaPlayerData!"));
		return;
	}

	if (MediaPlayerData->IsStopInWorldOver)
	{
		if (UUECS3GameInstance::Instance&&UUECS3GameInstance::Instance->GameStatus)
		{
			bIsStopByLoadingOver = false;
			//UUECS3GameInstance::Instance->GameStatus->InWorldLoadingOver.AddDynamic(this, &UMediaPlayerManager::InWorldLoadingOverEvent);
			UUECS3GameInstance::Instance->GameStatus->LoginLoadingOver.AddDynamic(this, &UMediaPlayerManager::InWorldLoadingOverEvent);
		}
	}
	/*UGUIManager* GUIManager = UUECS3GameInstance::Instance->GUIManager;
	if (IsValid(GUIManager) && MediaPlayerData->HideUI)
	{
		GUIManager->HideOrShowVSWindows(true);
	}*/
	
	//FString tempMediaPlayerId = CurMediaPlayerId;
	//CurMediaPlayerId = TEXT("");
	//创建播放CG的界面，由界面处理播放CG
	UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::CreateRole, TEXT("CreateCG")); 
	//UBaseWindow* CGWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("CreateCG"));
	//if (!IsValid(CGWidget))
	//{
	//	CS3_Warning(TEXT("-->Null Pointer error:UMediaPlayerManager::OnMediaOpened : CGWidget!"));
	//	return;
	//}
	//CurMediaPlayerId = tempMediaPlayerId;

	//FTimerHandle DelayHandle;
	//TWeakObjectPtr<UMediaPlayerManager> DelayThisPtr(this);
	//UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([DelayThisPtr, MediaPlayerData]()
	//{
	//	if (DelayThisPtr.IsValid() && MediaPlayerData)
	//	{
	//		UMediaPlayerManager* ThisPtr = DelayThisPtr.Get();
	//		ThisPtr->MediaPlayer->SetRate(MediaPlayerData->Rate);
	//		ThisPtr->MediaPlayer->SetLooping(MediaPlayerData->Loop);
	//		ThisPtr->MediaPlayer->Play();
	//	}
	//}), 0.001f, false);
	MediaPlayer->SetRate(MediaPlayerData->Rate);
	MediaPlayer->SetLooping(MediaPlayerData->Loop);
	MediaPlayer->Play();
	if (MediaPlayerData->Loop&&MediaPlayerData->MinimumTime>0.0f)
	{
		bIsCanStopByMinimumTime = false;
		TWeakObjectPtr<UMediaPlayerManager> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, MinimumTimeHandle, FTimerDelegate::CreateLambda([DelayThisPtr, MediaPlayerData]()
		{
			if (DelayThisPtr.IsValid() && MediaPlayerData)
			{
				UMediaPlayerManager* ThisPtr = DelayThisPtr.Get();
				ThisPtr->bIsCanStopByMinimumTime = true;
				ThisPtr->Close();
			}
		}), MediaPlayerData->MinimumTime, false);
	}
	onNotifyServerEvent(MediaPlayerData->OnMediaOpenedEvent);
}

void UMediaPlayerManager::OnMediaOpenFailed(FString FailedUrl)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayerManager::OnMediaOpenFailed -> MediaId[%s]~"), *CurMediaPlayerId);
	ResetMediaData();
}

bool UMediaPlayerManager::IsStopLoadingLevel()
{
	const FMEDIA_PLAYER_DATA* MediaPlayerData = GetMediaPlayerData(CurMediaPlayerId);
	if (MediaPlayerData)
	{
		return MediaPlayerData->IsStopLoadingLevel;
	}
	return  true;
}

bool UMediaPlayerManager::IsStopInWorldOver()
{
	const FMEDIA_PLAYER_DATA* MediaPlayerData = GetMediaPlayerData(CurMediaPlayerId);
	if (MediaPlayerData)
	{
		return MediaPlayerData->IsStopInWorldOver;
	}
	return  false;
}

bool UMediaPlayerManager::IsPlaying()
{
	if (!CurMediaPlayerId.IsEmpty()&& CurMediaPlayerId.Compare(TEXT("")))
	{
		return true;
	}
	return false;
}

void UMediaPlayerManager::DelayRemoveCGWindow()
{
	UBaseWindow* CGWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("CreateCG"));
	if (IsValid(CGWidget))
	{
		CGWidget->Destroy();
	}
}

const FMEDIA_PLAYER_DATA* UMediaPlayerManager::GetMediaPlayerData(const FString& MediaPlayerId)
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (!IsValid(UUECS3GameInstance::Instance->CfgManager)) || MediaPlayerId.IsEmpty())return nullptr;

	const FMEDIA_PLAYER_DATA* MediaPlayerData =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_MEDIA_PLAYER_DATA)->GetRow<FMEDIA_PLAYER_DATA>(MediaPlayerId);
	if (!MediaPlayerData) CS3_Warning(TEXT("-->Null Pointer error:UMediaPlayerManager::GetMediaPlayerData : MediaPlayerData!"));

	return MediaPlayerData;
}

void UMediaPlayerManager::OnEnableInput(bool bIsEnable)
{
	APlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	// 设置剧情控制状态
	if (ACS3PlayerController* GamePC = Cast<ACS3PlayerController>(PlayerController))
	{
		// 鼠标显示与隐藏
		GamePC->bShowMouseCursor = bIsEnable;
		if (IsValid(PlayerActor))
		{
			if (!bIsEnable)
			{
				UAtkStateMar* AtkState = GamePC->GetAtkStateMar();

				if (IsValid(AtkState))
				{
					if (AtkState->IsHaveState(EATTACT_STATE::AUTO_ATT))
					{
						AtkState->SwitchAutoFight(false, EBreakAutomaticType::NoneBreakType);
					}
				}
				GamePC->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_STORY, true,0);
			}
			else
			{
				GamePC->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_STORY, false);
			}
		}
	}
}

void UMediaPlayerManager::OnMediaStoped()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayerManager::OnMediaStoped -> MediaId[%s]~"), *CurMediaPlayerId);
	ClearMediaEvent();
	const FMEDIA_PLAYER_DATA* MediaPlayerData = GetMediaPlayerData(CurMediaPlayerId);
	if (MediaPlayerData)
	{
		onNotifyServerEvent(MediaPlayerData->OnMediaStopedEvent);
	}
	
	ResetMediaData();
	OnEnableInput(true);

	if (OnMediaEndReachedDelegate.IsBound())
	{
		OnMediaEndReachedDelegate.Broadcast();
	}
	
	if (MediaPlayerData->IsStopInWorldOver)
	{
		if (UUECS3GameInstance::Instance&&UUECS3GameInstance::Instance->GameStatus)
		{
			//UUECS3GameInstance::Instance->GameStatus->InWorldLoadingOver.Remove(this, TEXT("InWorldLoadingOverEvent"));
			UUECS3GameInstance::Instance->GameStatus->LoginLoadingOver.Remove(this, TEXT("InWorldLoadingOverEvent"));
		}
	}
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(MinimumTimeHandle);
	
	if ((UUECS3GameInstance::Instance->GameStatus && !UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::InWorld)))
	{
		FTimerHandle DelayHandle;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this, &UMediaPlayerManager::DelayRemoveCGWindow, 0.5f, false);
	}
	else
	{
		DelayRemoveCGWindow();
		UGUIManager* GUIManager = UUECS3GameInstance::Instance->GUIManager;
		if (IsValid(GUIManager))
		{
		//	GUIManager->HideOrShowVSWindows(false);
		}
		// 恢复所有语音
		if (UGolbalBPFunctionLibrary::AudioManager() && IsValid(UGolbalBPFunctionLibrary::AudioManager()))
		{
			TArray<FString> PauseTypes = { "1","2","3","4","5" };
			TArray<FString>HideTypes;
			UGolbalBPFunctionLibrary::AudioManager()->SetPausedVoice(PauseTypes, HideTypes, false);
		}
	}
}

int UMediaPlayerManager::PreLoadMediaAsset(const FLoadMediaOverDelegate& InLoadMediaOverDelegate /*= FLoadMediaOverDelegate()*/)
{
	MediaAssList.Reset();
	MediaAss.Reset();
	AllMediaAss.Reset();
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager))
	{
		LoadMediaAssetEnd();
		return MediaAss.Num();
	}

	const UConfigTable* MediaConfigTab =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_MEDIA_PLAYER_DATA);
	if (!IsValid(MediaConfigTab))
	{
		LoadMediaAssetEnd();
		return MediaAss.Num();
	}

	TArray<FName> RowNames = MediaConfigTab->GetRowNames();

	const FString SpaceId = UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID"));

	for (FName RowName : RowNames)
	{
		const FMEDIA_PLAYER_DATA* MediaData = (FMEDIA_PLAYER_DATA*)MediaConfigTab->GetRow(RowName);
		if (!MediaData || (MediaData->MediaSources.Num() <= 0))
		{
			break;
		}
		bool bIsQuestAsset = false;
		TArray<FString> QuestIDs = UGolbalBPFunctionLibrary::SplitString(MediaData->QuestID);

		if (QuestIDs.Num() > 0)
		{
			UQuestManager* QuestManager = UUECS3GameInstance::Instance->QuestManager;
			if (IsValid(QuestManager))
			{
				TArray<int32> QuestTable;
				QuestManager->GetPlayerQuestIDs(QuestTable);
				for (auto& QuestID : QuestIDs)
				{
					if (QuestTable.Contains(FSTRING_TO_INT(QuestID)))
					{
						bIsQuestAsset = true;
						break;
					}
				}
			}
		}

		TArray<FString> SpaceName = UGolbalBPFunctionLibrary::SplitString(MediaData->Space);
		if (SpaceName.Contains(SpaceId))
		{
			int32 AssetAccount = MediaData->MediaSources.Num();
			if (1 == AssetAccount)
			{
				if (MediaData->MediaSources[0].ToSoftObjectPath() == nullptr)
				{
					break;
				}
				AllMediaAss.Add(FNAME_TO_FSTRING(RowName), MediaData->MediaSources[0]);
				if (bIsQuestAsset)
				{
					MediaAss.Add(FNAME_TO_FSTRING(RowName), MediaData->MediaSources[0]);
				}
			}
			else
			{
				int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
				int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
				int32 PlayId = Profession - 1;
				if ((PlayId >= 0) && (PlayId < AssetAccount))
				{
					if (MediaData->MediaSources[PlayId].ToSoftObjectPath() == nullptr)
					{
						break;
					}
					AllMediaAss.Add(FNAME_TO_FSTRING(RowName), MediaData->MediaSources[PlayId]);
					if (bIsQuestAsset)
					{
						MediaAss.Add(FNAME_TO_FSTRING(RowName), MediaData->MediaSources[PlayId]);
					}
				}
			}
		}
	}

	if (0 == AllMediaAss.Num())
	{
		LoadMediaAssetEnd();
		return 0;
	}

	for (auto& data : MediaAss)
	{
		LoadMediaAsset(data.Key, data.Value);
	}
	return MediaAss.Num();
}

void UMediaPlayerManager::LoadMediaAssetEnd(TSoftObjectPtr<UMediaSource> stroyAss /*= nullptr*/)
{
	TArray<TSoftObjectPtr<UMediaSource>> ValueArray;
	MediaAss.GenerateValueArray(ValueArray);
	if (ValueArray.Contains(stroyAss))
	{
		if (LoadMediaOverDelegate.IsBound())
		{
			LoadMediaOverDelegate.Broadcast();
		}
	}
}

void UMediaPlayerManager::LoadMediaAsset(FString MediaID, TSoftObjectPtr<UMediaSource> TempMediaAss)
{
	if (TempMediaAss.ToSoftObjectPath() == nullptr)
	{
		LoadMediaAssetEnd(TempMediaAss);
		return;
	}

	UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, TempMediaAss.ToSoftObjectPath(),
		FStreamableDelegate::CreateLambda([this, TempMediaAss, MediaID]()
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayerManager::LoadMediaAsset -> MediaId[%s]~"), *MediaID);
		LoadMediaAssetEnd(TempMediaAss);
		MediaAssList.Add(MediaID, TempMediaAss.Get());
	}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_MEDIA);
}

void UMediaPlayerManager::ClearMediaEvent()
{
	if (MediaPlayer->OnEndReached.IsAlreadyBound(this, &UMediaPlayerManager::OnEndReached))
	{
		MediaPlayer->OnEndReached.RemoveDynamic(this, &UMediaPlayerManager::OnEndReached);
	}
	if (MediaPlayer->OnMediaClosed.IsAlreadyBound(this, &UMediaPlayerManager::OnMediaClosed))
	{
		MediaPlayer->OnMediaClosed.RemoveDynamic(this, &UMediaPlayerManager::OnMediaClosed);
	}
	if (MediaPlayer->OnMediaOpened.IsAlreadyBound(this, &UMediaPlayerManager::OnMediaOpened))
	{
		MediaPlayer->OnMediaOpened.RemoveDynamic(this, &UMediaPlayerManager::OnMediaOpened);
	}
	if (MediaPlayer->OnMediaOpenFailed.IsAlreadyBound(this, &UMediaPlayerManager::OnMediaOpenFailed))
	{
		MediaPlayer->OnMediaOpenFailed.RemoveDynamic(this, &UMediaPlayerManager::OnMediaOpenFailed);
	}
}

void UMediaPlayerManager::ResetMediaData()
{
	CurMediaPlayerId = TEXT("");
}

void UMediaPlayerManager::InWorldLoadingOverEvent()
{
	if (UUECS3GameInstance::Instance&&UUECS3GameInstance::Instance->GameStatus &&
		UUECS3GameInstance::Instance->GameStatus->GetIsInWorldLoadingOver())
	{
		bIsStopByLoadingOver = true;
		Close();
	}
}

void UMediaPlayerManager::onNotifyServerEvent(FString Params)
{	
	///回调服务器
	TArray<FString> ParamsList = UGolbalBPFunctionLibrary::SplitString(Params, true);
	if (ParamsList.Num() > 0)
	{
		URoleInterface * RoleInterface = Cast<URoleInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.GameObjectInterface : nullptr);
		if (RoleInterface)
		{
			FString MethodName = ParamsList[0];
			ParamsList.RemoveAt(0);
			RoleInterface->CellCallWithBp(MethodName, ParamsList);
		}
	}
}

void UMediaPlayerManager::PreLoadAllMediaAsset()
{
	TWeakObjectPtr<UMediaPlayerManager> DelayThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayLoadAllMediaHandle,
		FTimerDelegate::CreateLambda([DelayThisPtr]() {
		if (DelayThisPtr.IsValid())
		{
			UMediaPlayerManager* ThisPtr = DelayThisPtr.Get();
			for (auto& data : ThisPtr->AllMediaAss)
			{
				if (!ThisPtr->MediaAss.Contains(data.Key))
				{
					ThisPtr->LoadMediaAsset(data.Key, data.Value);
				}
			}
		}
	}), 0.2f, false);
}

void UMediaPlayerManager::PreLoadMediaAssetByGameStatus()
{
	MediaAssList.Reset();
	MediaAss.Reset();
	AllMediaAss.Reset();
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMediaPlayerManager::PreLoadMediaAssetByGameStatus : （Instance &&Instance->CfgManager）!"));
		return;
	}

	const UConfigTable* MediaConfigTab =UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_MEDIA_PLAYER_DATA);
	if (!IsValid(MediaConfigTab))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMediaPlayerManager::PreLoadMediaAssetByGameStatus: MediaConfigTab!"));
		return;
	}
	TArray<FName> RowNames = MediaConfigTab->GetRowNames();
	
	for (FName RowName : RowNames)
	{
		const FMEDIA_PLAYER_DATA* MediaData = (FMEDIA_PLAYER_DATA*)MediaConfigTab->GetRow(RowName);
		if (!MediaData || (MediaData->MediaSources.Num() <= 0))
		{
			break;
		}
		bool bIsQuestAsset = false;

		EGameStatus CurrStatus= UUECS3GameInstance::Instance->GameStatus->GetCurrStatus();
		if (MediaData->GameStatus.Contains(CurrStatus))
		{
			int32 AssetAccount = MediaData->MediaSources.Num();
			if (1 == AssetAccount)
			{
				if (MediaData->MediaSources[0].ToSoftObjectPath() == nullptr)
				{
					break;
				}
				AllMediaAss.Add(FNAME_TO_FSTRING(RowName), MediaData->MediaSources[0]);
			}
			else
			{
				int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
				if (PlayerId<1)
				{
					break;
				}
				int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
				int32 PlayId = Profession - 1;
				if ((PlayId >= 0) && (PlayId < AssetAccount))
				{
					if (MediaData->MediaSources[PlayId].ToSoftObjectPath() == nullptr)
					{
						break;
					}
					AllMediaAss.Add(FNAME_TO_FSTRING(RowName), MediaData->MediaSources[PlayId]);
				}
			}
		}
	}

	if (0 == AllMediaAss.Num())
	{		
		return ;
	}

	PreLoadAllMediaAsset();	
}

void UMediaPlayerManager::ClearMediaAsset()
{
	MediaAssList.Empty();
	MediaAss.Empty();
	AllMediaAss.Empty();
}

bool UMediaPlayerManager::IsNeedHideUI()
{
	/*if (!CurMediaPlayerId.IsEmpty()&& CurMediaPlayerId.Compare(TEXT("")))
	{
		return true;
	}*/
	return false;
}

void UMediaPlayerManager::GetSkipTimeData(float& HoldTime, float& CurTime, float& SkipTime, bool& bIsCanSkip, bool& bIsShowUI)
{
	bIsShowUI = false;
	bIsCanSkip = false;
	//播放资源
	const FMEDIA_PLAYER_DATA* MediaPlayerData = GetMediaPlayerData(CurMediaPlayerId);
	if (MediaPlayerData == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMediaPlayerManager::GetSkipTimeData : MediaPlayerData!"));
		return;
	}
	if (IsValid(MediaPlayer))
	{
		bIsShowUI = MediaPlayerData->SkipData.bIsShowSkipUI;
		HoldTime = MediaPlayer->GetDuration().GetTotalSeconds();		
		CurTime = MediaPlayer->GetTime().GetTotalSeconds();			
		if (MediaPlayerData->SkipData.Skip > HoldTime || MediaPlayerData->SkipData.Skip < 0.0f)
		{
			SkipTime=  FMath::Max(HoldTime, 0.0f);
		}
		else
		{
			SkipTime = FMath::Max(MediaPlayerData->SkipData.Skip - CurTime, 0.0f);
		}	
		if (MediaPlayerData->SkipData.Skip >= 0.0f)
		{
			bIsCanSkip = true;
		}
	}
}
