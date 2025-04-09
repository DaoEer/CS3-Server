// Fill out your copyright notice in the Description page of Project Settings.


#include "StoryManager.h"
#include "ResourceManager.h"
#include "Entity.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Role/RolePerformanceInterface.h"
#include "Interface/Role/RoleQuestInterface.h"
#include "Interface/Role/RoleStoryInterface.h"
#include "Actor/Scene/SceneCharacter.h"
#include "Interface/Role/RolePetInterface.h"
#include "GameStatus.h"
#include "Component/Role/RideCarrierComponent.h"
#include "AudioManager.h"
#include "LevelSequence.h"
#include "LocalDataSaveManager.h"
#include "QuestManager.h"
#include "VisibleManager.h"
#include "SpaceDynamicEffectManager.h"
#include "AtkStateMar.h"
#include "Operation/RoleCtrl/RoleCtrlStateMgr.h"
#include "CustomTimerManager.h"
#include "Util/ConvertUtil.h"
#include "Actor/ServerCharacter.h"
#include "Level/InWorldStreamLevel.h"
#include"Chuangshi.h"
#include "CS3Base/UIManager.h"
#include "Interface/Role/RoleSpaceContentInterface.h"
#include "Kismet/GameplayStatics.h"
#include "GameData/StoryLoadModelData.h"
#include "Actor/Player/CS3CineCameraActor.h"
#include "CS3Base/GameObject.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("PlaySequence"), STAT_PlaySequence, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("StopSequence"), STAT_StopSequence, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("IsShowModel"), STAT_IsShowModel, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("EndCameraAnim"), STAT_EndCameraAnim, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("CheckPreLoadStory"), STAT_CheckPreLoadStory, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("SwitchStoryMode"), STAT_SwitchStoryMode, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("StoryHideEntities"), STAT_StoryHideEntities, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("PrePlaySequence"), STAT_PrePlaySequence, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("StartPlaySequence"), STAT_StartPlaySequence, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("PreLoadStoryAsset"), STAT_PreLoadStoryAsset, STATGROUP_UGStoryManager);
DECLARE_CYCLE_STAT(TEXT("GetPreCameraData"), STAT_GetPreCameraData, STATGROUP_UGStoryManager);

ACS3LevelSequenceActor::ACS3LevelSequenceActor(const FObjectInitializer& Init)
	: Super(Init)
{
}

void ACS3LevelSequenceActor::BeginDestroy()
{

	Super::BeginDestroy();
}

void ACS3LevelSequenceActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (SequencePlayer && SequencePlayer->OnStop.IsBound())
	{
		SequencePlayer->OnStop.Broadcast();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("CS3ALevelSequenceActor::BeginDestroy -> OnStop Broadcast~"));
	}
	Super::EndPlay(EndPlayReason);
}

UGStoryManager::UGStoryManager()
{

}

UGStoryManager::~UGStoryManager()
{
	HideEntitiesList.Empty();
}

UGStoryManager* UGStoryManager::GetInstance()
{
	cs3_checkNoReentry();

	return (UGStoryManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_GStoryManager")));
}

void UGStoryManager::BeginDestroy()
{
	if (IsValid(this))
	{
		ClearDelayDestroyCameraTimer();
	}
	Super::BeginDestroy();
}

void UGStoryManager::ResetStoryData()
{
	bIsJumpToOpenDoorFinished = false;
	JumpToFrameCount = 0;
	bIsPreCamera = false;
	bIsPlayingToUI = false;
	CurrPlayId = TEXT("");
	CurrOrderIndex = -1;
	if (CurrVoiceIndex >= 0)
	{
		CurrVoiceIndex = -1;
	}
	CurrAnimIndex = -1;
	CurrTextIndex = -1;
	HideEntitiesList.Empty();
	bIsEndCamera = false;
}

void UGStoryManager::PlaySequence(const FString& SequenceId, int32 NumLoops /*= 1*/)
{
	if (!CurrPlayId.IsEmpty())
	{			
		StopSequence();
		if (DelayHandle.IsValid() && bIsEndCamera)
		{
			UGolbalBPFunctionLibrary::GetCS3PlayerController()->SetViewTargetWithBlend(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayHandle);
			OnDelayStoppingStoryOperate();
		}
		PlaySequence(SequenceId, NumLoops);
	}
	else 
	{
		SCOPE_CYCLE_COUNTER(STAT_PlaySequence);
		CS3_Warning(TEXT("~~~~~~~UGStoryManager::PlaySequence: SequenceId=%s!"), *SequenceId);
		if (!SequenceId.Compare("") || 0 == NumLoops)return;

		// 播放限定,需InWord才能播放
		UGameStatus* GameState = UUECS3GameInstance::Instance->GameStatus;
		if (!IsValid(GameState) || !(GameState->IsCurrStatus(EGameStatus::InWorld)|| GameState->IsCurrStatus(EGameStatus::Teleport)))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::PlaySequence : GameState && InWorld!"));
			return;
		}
		if (!(LevelSequenceActor && IsValid(LevelSequenceActor)))
		{
			//无效ALevelSequenceActor的话，就重新创建一个
			LevelSequenceActor = UGolbalBPFunctionLibrary::SpawnActor<ACS3LevelSequenceActor>(ACS3LevelSequenceActor::StaticClass());
		}

		//播放资源
		const FSTORY_DATA* StoryData = GetStoryData(SequenceId);

		int32 AssetAccount = 0;
		if (!StoryData || (StoryData->Assets.Num() <= 0))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::PlaySequence : StoryData!"));
			return;
		}

		AssetAccount = StoryData->Assets.Num();
		if (1 == AssetAccount)
		{
			if (StoryData->Assets[0].ToSoftObjectPath().IsValid())
			{
				RelPlaySequence(StoryData->Assets[0], NumLoops, SequenceId);
			}
		}
		else
		{
			int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
			int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
			int32 Gender = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "gender");
			int32 PlayId = Profession - 1;
			if (Gender == 2)
			{
				if (4 != AssetAccount)
				{
					PlayId = Profession + 3;
					if (2 == AssetAccount || 5 == AssetAccount)
					{
						PlayId = AssetAccount - 1;
					}
				}
			}
			else if (2 == AssetAccount)
			{
				PlayId = 0;
			}
		
			if ((PlayId >= 0) && (PlayId < AssetAccount))
			{
				if (StoryData->Assets[PlayId].ToSoftObjectPath().IsValid())
				{
					RelPlaySequence(StoryData->Assets[PlayId], NumLoops, SequenceId);
				}
				else
				{
					CS3_Display(CS3DebugType::CL_Undefined, TEXT("GetStoryAsset -> SequenceId[%s],PlayId[%d] asset is not found~"), *SequenceId, PlayId);
				}
			}
		}
	}	
}

void UGStoryManager::PauseSequence()
{
	if (LevelSequenceActor && LevelSequenceActor->SequencePlayer)
	{
		LevelSequenceActor->SequencePlayer->Pause();
	}
}

void UGStoryManager::StopSequence()
{
	SCOPE_CYCLE_COUNTER(STAT_StopSequence);
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UGStoryManager::StopSequence SequenceId[%s]~"), *CurrPlayId);
	if (LevelSequenceActor && LevelSequenceActor->SequencePlayer)
	{
		if (LevelSequenceActor->bAutoPlay_DEPRECATED)
		{
			LevelSequenceActor->bAutoPlay_DEPRECATED = false;
		}
		LevelSequenceActor->SequencePlayer->Stop();

		if (CurrPlayId.Compare(TEXT("")) && !LevelSequenceActor->SequencePlayer->OnStop.IsBound())
		{
			OnStoryStop();
		}
	}
}


void UGStoryManager::JumpToFrameSequence(int32 NewPosition)
{
	FFrameTime NewPositionTime = FFrameTime(NewPosition, 1.0f / 30.0f);
	if (IsValid(LevelSequenceActor) && IsValid(LevelSequenceActor->SequencePlayer)&&CheckCanJumpToFrame(NewPositionTime))
	{		
		JumpToFrameCount++;
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UGStoryManager::JumpToFrameSequence JumpToFrameCount=%d  NewPosition =%d~"), JumpToFrameCount, NewPosition);
		LevelSequenceActor->SequencePlayer->JumpToFrame(NewPositionTime);
	}
}

bool UGStoryManager::CheckCanJumpToFrame(FFrameTime NewPosition)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UGStoryManager::CheckCanJumpToFrame  NewPosition =%d~"), NewPosition.FrameNumber.Value);
	if (const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId))
	{
		if (!bIsJumpToOpenDoorFinished && StoryData->IsHZMGOpenDoorStory)
		{
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UGStoryManager::CheckCanJumpToFrame  StoryData->IsHZMGOpenDoorStory =true"));
			AInWorldStreamLevel* LevelScriptActor = Cast<AInWorldStreamLevel>(UGolbalBPFunctionLibrary::GetMainLevelActor());

			if (LevelScriptActor && LevelScriptActor->GetIsNextSubLevelFinished())
			{
				JumpToFrameCount = 0;
				bIsJumpToOpenDoorFinished = true;
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("UGStoryManager::CheckCanJumpToFrame PlayToFrameSequence  NewPosition =%d~"), NewPosition.FrameNumber.Value);
				PlayToFrameSequence(GetPlayToFrameData());
				return false;
			}
		}
		if (bIsJumpToOpenDoorFinished && StoryData->IsStopInWorldOver)
		{
			CheckStopInWorldOver();
			return false;
		}
	}	
	if (IsValid(LevelSequenceActor) && IsValid(LevelSequenceActor->SequencePlayer)
		&& LevelSequenceActor->SequencePlayer->GetCurrentTime().Time== NewPosition)
	{
		return false;
	}
	return true;
}

void UGStoryManager::PlayToFrameSequence(FFrameTime NewPosition)
{
	if (IsValid(LevelSequenceActor) && IsValid(LevelSequenceActor->SequencePlayer) && CheckCanPlayToFrame(NewPosition))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UGStoryManager::PlayToFrameSequence start NewPosition =%d~"), NewPosition.FrameNumber.Value);
		LevelSequenceActor->SequencePlayer->PlayToFrame(NewPosition);
	}
}

bool UGStoryManager::CheckCanPlayToFrame(FFrameTime NewPosition)
{
	return true;
}

FFrameTime UGStoryManager:: GetPlayToFrameData()
{
	if (const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId))
	{
		FFrameTime NewPosition = FFrameTime(StoryData->PlayToFrameData, 1.0f / 30.0f);
		return NewPosition;
	}
	return FFrameTime(0, 0.0f);
}

void UGStoryManager::onNotifyAddEffectList()
{
	FSTORY_DATA* StoryData = const_cast<FSTORY_DATA*>(GetStoryData(CurrPlayId));
	if (!StoryData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::onNotifyAddEffectList : StoryData!"));
		return;
	}
	URoleStoryInterface * RoleStoryInterface = Cast<URoleStoryInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStoryInterface"), 0));
	if (IsValid(RoleStoryInterface) && StoryData->EffectList.Num() > 0)
	{
		RoleStoryInterface->onNotifyAddEffectList(CurrPlayId, StoryData->EffectList);
	}
}

void UGStoryManager::onNotifyRemoveEffectList()
{	
	if (CurrPlayId.IsEmpty() || !CurrPlayId.Compare(""))
		return;

	URoleStoryInterface * RoleStoryInterface = Cast<URoleStoryInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStoryInterface"), 0));
	if (IsValid(RoleStoryInterface))
	{
		RoleStoryInterface->onNotifyRemoveEffectList(CurrPlayId);
	}
}



FString UGStoryManager::GetCurrPlayId()
{
	return CurrPlayId;
}

bool UGStoryManager::IsPlaying()
{
	if (IsValid(LevelSequenceActor) && IsValid(LevelSequenceActor->SequencePlayer))
	{
		return (LevelSequenceActor->SequencePlayer->IsPlaying()||(!CurrPlayId.IsEmpty()&&CurrPlayId.Compare(TEXT(""))));
	}
	return false;
}

bool UGStoryManager::IsLevelSequencePlaying()
{
	if (IsValid(LevelSequenceActor) && IsValid(LevelSequenceActor->SequencePlayer))
	{
		return (LevelSequenceActor->SequencePlayer->IsPlaying()|| bIsPreCamera);
	}
	return false;
}

void UGStoryManager::StoryEventByParams(CSTORY_EVENT_PARAM_TYPE_ENUM EventName, const FString& Param1, const FString& Param2, const FString& Param3, const FString& Param4)
{
	if (EventName != CSTORY_EVENT_PARAM_TYPE_ENUM::CNONE)
	{
		switch (EventName)
		{
		case CSTORY_EVENT_PARAM_TYPE_ENUM::CNOTIFY_SERVER:
			NotifyServerEvent();
			break;
		case CSTORY_EVENT_PARAM_TYPE_ENUM::CPLAY_VOICE:
			PlayVoiceWordsByParam(Param1);
			break;
		case CSTORY_EVENT_PARAM_TYPE_ENUM::CPLAY_REDRAW_VIEWPORTS:
			PlayRedrawViewports();
			break;
		case CSTORY_EVENT_PARAM_TYPE_ENUM::CPLAY_ANIM:
			if (Param2.IsEmpty() ||FSTRING_TO_FLOAT(Param2)<0|| FMath::IsNearlyZero(FSTRING_TO_FLOAT(Param2)))
			{
				PlayAnimEventByParam(Param1);
			}
			else if (Param3.IsEmpty())
			{
				PlayAnimEventByParam(Param1, FSTRING_TO_FLOAT(Param2));
			}
			else 
			{
				PlayAnimEventByParam(Param1, FSTRING_TO_FLOAT(Param2), (FSTRING_TO_INT(Param3) == 0 || FSTRING_TO_INT(Param3) < 0) ? false : true);
			}
			
			break;
		case CSTORY_EVENT_PARAM_TYPE_ENUM::CSTOP_ANIM:
			StopAnimEvent();
			break;
		default:
			break;
		}
	}
}

void UGStoryManager::NotifyServerEvent()
{
	// TODO:通知服务器;CurrId:当前剧情Id;CurrOrderIndex:第几个通知索引
	++CurrOrderIndex;
	if (CurrPlayId.IsEmpty() || !CurrPlayId.Compare(""))
		return;

	URoleStoryInterface * RoleStoryInterface = Cast<URoleStoryInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStoryInterface"), 0));
	if (RoleStoryInterface)
	{
		RoleStoryInterface->onNotifyDoStoryEvent(CurrPlayId, CurrOrderIndex);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::NotifyServerEvent -> CurrPlayId[%s], CurrOrderIndex[%d]~"), *CurrPlayId, CurrOrderIndex);
	}	
}

void UGStoryManager::PlayVoiceWords()
{
	UGolbalBPFunctionLibrary::AudioManager()->AAudioManager::StopVoice();
	if (UGolbalBPFunctionLibrary::AudioManager() && IsValid(UGolbalBPFunctionLibrary::AudioManager()))
	{
		if (const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId))
		{
			int32 MaxNum = StoryData->VoiceWords.Num();
			if (MaxNum && (++CurrVoiceIndex < MaxNum))
			{
				PlayVoiceWordsByParam(StoryData->VoiceWords[CurrVoiceIndex]);
			}
		}
	}
}

void UGStoryManager::PlayTextEvent_Implementation()
{
	CurrTextIndex++;
}

void UGStoryManager::PlayVoiceWordsByParam(const FString& VoiceWords)
{
	CS3_Warning(TEXT("~~~~~~~UGStoryManager::PlayVoiceWordsByParam: VoiceWords=%s!"), *VoiceWords);
	TArray<FString> ProfessionVoices = UGolbalBPFunctionLibrary::SplitString(VoiceWords);
	FString VoiceID = "";
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	int32 Gender = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "gender");
	int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
	int32 PlayId = Profession - 1;
	TArray<FString> GenderVoiceIndex;
	if (ProfessionVoices.Num() ==1)
	{
		 GenderVoiceIndex = UGolbalBPFunctionLibrary::SplitString(ProfessionVoices[0], false, ";");
	}
	else if (ProfessionVoices.Num() > 1)
	{
		if ((PlayId >= 0) && (PlayId < ProfessionVoices.Num()))
		{
			 GenderVoiceIndex = UGolbalBPFunctionLibrary::SplitString(ProfessionVoices[PlayId], false, ";");
		}
	}
	if (1 == GenderVoiceIndex.Num())
	{
		VoiceID = GenderVoiceIndex[0];
	}
	else if (GenderVoiceIndex.Num() > 1)
	{
		if (Gender >= 1 && ((Gender - 1) < GenderVoiceIndex.Num()))
		{
			VoiceID = GenderVoiceIndex[Gender - 1];
		}
	}
	if (VoiceID.Compare(""))
	{
		UGolbalBPFunctionLibrary::AudioManager()->AddStoryAudio(VoiceID);
		UGolbalBPFunctionLibrary::AudioManager()->AnalysisVoiceData(VoiceID);
	}
	else 
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("GetStoryAsset -> VoiceWords CurrVoiceIndex[%d],PlayId[%d] asset is not found~"), CurrVoiceIndex, PlayId);
	}
}

void UGStoryManager::PlayRedrawViewports()
{
	CS3_Warning(TEXT("UGStoryManager::PlayRedrawViewports: VoiceWords=%s!"), *CurrPlayId);
	const FSTORY_EVENT_DATA* StoryEventData = GetStoryEventData(CurrPlayId);

	if (StoryEventData)
	{
		if (StoryEventData->StoryEventList.Num() > 0)
		{
			for (auto& data: StoryEventData->StoryEventList)
			{
				if (data.Index == CurrOrderIndex)
				{
					for (auto& StoryEvent : data.StoryEvents)
					{
						bool bIsTeleport = false;
						const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
						FString LeveName = "";
						if (StoryEvent.script == "SETeleportPlayer")
						{
							bIsTeleport = true;
							LeveName = StoryEvent.param1;
						}
						else if (StoryEvent.script == "SETeleportPlayerByClass")
						{
							bIsTeleport = true;
							TArray<FString> LevelNames = UGolbalBPFunctionLibrary::SplitString(StoryEvent.param1);
							int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), "profession");
							int32 LevelId = Profession - 1;
							if ((LevelId >= 0) && (LevelId < LevelNames.Num()))
							{
								LeveName = LevelNames[LevelId];
							}
						}
						if (bIsTeleport && LeveName.Compare(SpaceScriptID))
						{
							if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
							{
								return;
							}
							PauseSequence();
							GEngine->RedrawViewports(false);
							CS3_Display(CS3DebugType::CL_Undefined, TEXT("PlayRedrawViewports -> GEngine->RedrawViewports~"));
							return;
						}						
					}
					break;
				}
			}
			
		}
	}
}

void UGStoryManager::PlayAnimEvent()
{
	CS3_Warning(TEXT("UGStoryManager::PlayAnimEvent: VoiceWords=%s!"), *CurrPlayId);
	if (const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId))
	{
		int32 MaxNum = StoryData->AnimName.Num();
		if (MaxNum && (++CurrAnimIndex < MaxNum))
		{
			TArray<FString> AnimIndex = UGolbalBPFunctionLibrary::SplitString(StoryData->AnimName[CurrAnimIndex], true);
			if (AnimIndex.Num() == 1)
			{
				PlayAnimEventByParam(AnimIndex[0]);
			}
			else if (AnimIndex.Num() == 2)
			{
				PlayAnimEventByParam(AnimIndex[0], FSTRING_TO_FLOAT(AnimIndex[1]));
			}
			else if (AnimIndex.Num() == 3)
			{
				PlayAnimEventByParam(AnimIndex[0], FSTRING_TO_FLOAT(AnimIndex[1]), (FSTRING_TO_INT(AnimIndex[2]) == 0 || FSTRING_TO_INT(AnimIndex[2]) < 0) ? false : true);
			}
		}
	}
}

void UGStoryManager::PlayAnimByIndexEvent(int32 Index)
{
	CS3_Warning(TEXT("UGStoryManager::PlayAnimByIndexEvent: Index=%d!"), Index);
	if (const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId))
	{
		CurrAnimIndex = Index;
		int32 MaxNum = StoryData->AnimName.Num();
		if (MaxNum && (CurrAnimIndex < MaxNum))
		{
			TArray<FString> AnimIndex = UGolbalBPFunctionLibrary::SplitString(StoryData->AnimName[Index], true);
			if (AnimIndex.Num() == 1)
			{
				PlayAnimEventByParam(AnimIndex[0]);
			}
			else if (AnimIndex.Num() == 2)
			{
				PlayAnimEventByParam(AnimIndex[0], FSTRING_TO_FLOAT(AnimIndex[1]));
			}
			else if (AnimIndex.Num() == 3)
			{
				PlayAnimEventByParam(AnimIndex[0], FSTRING_TO_FLOAT(AnimIndex[1]), (FSTRING_TO_INT(AnimIndex[2]) == 0 || FSTRING_TO_INT(AnimIndex[2]) < 0) ? false : true);
			}
		}
	}
}

void UGStoryManager::PlayAnimEventByParam(const FString& AnimName, float PlayRate/*=1.0f*/,bool bLoop/*=true*/)
{
	const FSTORY_ANIM_EVENT* StoryAnimEventData = GetStoryAnimEventData(AnimName);
	CS3_Warning(TEXT("UGStoryManager::PlayAnimEventByParam: AnimName=%s PlayRate=%f bLoop=%d!"), *AnimName, PlayRate, bLoop == true ? 1 : 0);
	if (StoryAnimEventData)
	{
		int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
		int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
		int32 Gender = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "gender");
		int32 PlayId = Profession - 1;
		if (Gender == 2)
		{
			PlayId = Profession + 3;
		}

		if ((PlayId >= 0) && (PlayId < StoryAnimEventData->AnimPath.Num()))
		{
			if (!StoryAnimEventData->AnimPath[PlayId].IsNull())
			{
				UObject* AnimObj = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(StoryAnimEventData->AnimPath[PlayId].ToSoftObjectPath());
				if (IsValid(AnimObj))
				{
					UAnimSequenceBase* AnimSeq = Cast<UAnimSequenceBase>(AnimObj);
					if (IsValid(AnimSeq))
					{
						if (OnPlayAnimEventDelegate.IsBound())
						{
							OnPlayAnimEventDelegate.Broadcast(AnimSeq, PlayRate, bLoop);
						}
					}
				}
			}

		}
	}
}

void UGStoryManager::StopAnimEvent()
{
	CS3_Warning(TEXT("-->GStoryManager::StopAnimEvent!"));
	if (OnStopAnimEventDelegate.IsBound())
	{
		OnStopAnimEventDelegate.Broadcast();
	}
}

bool UGStoryManager::IsShowModel(AActor* Actor, int32 EntityId)
{
	SCOPE_CYCLE_COUNTER(STAT_IsShowModel);
	// 是否在播放剧情
	if (IsLevelSequencePlaying())
	{
		auto Func_HideEntity = [this, Actor, EntityId]()
		{
			if (EntityId != 0)
			{
				HideEntitiesList.AddUnique(EntityId);
			}			
			return false;
		};
		// StoryConfig是否有参数隐藏
		const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
		if (!StoryData)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::IsShowModel : StoryData!"));
			return true;
		}
		FHIDEENTITY_DATA HideEntities = StoryData->HideEntity;
		TArray<FString> HideTypes = UGolbalBPFunctionLibrary::SplitString(HideEntities.HideType, true);
		if (EntityId != 0)
		{
			// 是否包含在隐藏列表
			if (HideEntitiesList.Contains(EntityId)) return Func_HideEntity();			

			if (AServerCharacter* Character = Cast<AServerCharacter>(Actor))
			{
				if (KBEngine::Entity* Entity = Character->GetSelfEntity())
				{
					if (!Entity->ClassName().Compare(FString("Role")))
					{
						if (HideTypes.Contains(TEXT("1")) && !StoryData->IsHZMGOpenDoorStory)
						{
							return Func_HideEntity();
						}
					}
					else if (Entity->ClassName().Compare(FString("VehiclePet")))
					{
						FString EntityScriptId = Entity->GetDefinedProperty(TEXT("scriptID")).GetValue<FString>();

						if (HideTypes.Contains(TEXT("4")))
						{
							TArray<FString> ShowByScriptIds = UGolbalBPFunctionLibrary::SplitString(HideEntities.Param2, true);
							TArray<FString> ShowByClassNames = UGolbalBPFunctionLibrary::SplitString(HideEntities.Param3, true);

							/** 显示ClassName的Entity */
							if (UGolbalBPFunctionLibrary::IsContainStr(Entity->ClassName(), ShowByClassNames)) return true;
							/** 显示ScriptId的Entity */
							if (UGolbalBPFunctionLibrary::IsContainStr(EntityScriptId, ShowByScriptIds)) return true;
							return Func_HideEntity();
						}
						else
						{
							/** 只隐藏ScriptId的Entity */
							TArray<FString> HideByScriptIds = UGolbalBPFunctionLibrary::SplitString(StoryData->HideEntity.Param1, true);
							if (UGolbalBPFunctionLibrary::IsContainStr(EntityScriptId, HideByScriptIds)) return Func_HideEntity();
						}
					}
					else
					{
						if (APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
						{
							if (PlayerActor->PetEntityId != EntityId)
							{
								if (HideTypes.Contains(TEXT("2")))
								{
									return Func_HideEntity();
								}
							}
							else
							{
								if (HideTypes.Contains(TEXT("3")))
								{
									return Func_HideEntity();
								}
							}
						}
					}
				}
			}
		}
		else 
		{
			if (ASceneCharacter* Character = Cast<ASceneCharacter>(Actor))
			{
				if (HideTypes.Contains(TEXT("5")))
				{
					TArray<FString> ShowByUIds = UGolbalBPFunctionLibrary::SplitString(HideEntities.Param4, true);
					
					if (IsValid(Character))
					{
						if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SpaceDynamicEffectManager))
						{
							int  entityUId = UUECS3GameInstance::Instance->SpaceDynamicEffectManager->GetSceneCharacterUID(Character);
							if (entityUId != 0 && UGolbalBPFunctionLibrary::IsContainStr(INT_TO_FSTRING(entityUId), ShowByUIds))
							{
								return true;
							}
						}
					}					
					return false;
				}
			}
		}
		// 隐藏剧情中新生成对象(StoryConfig)
		if (StoryData->HideNewEntity) return Func_HideEntity();
	}

	return true;
}

float UGStoryManager::PreCameraTime()
{
	FCAMERA_SETTINGS_DATA PreCameraSettings;
	GetPreCameraData(PreCameraSettings);
	return (PreCameraSettings.CameraPosInfo.Time <= 0.0f || PreCameraSettings.CameraPosInfo.Point.Equals(FVector::ZeroVector) || PreCameraSettings.CameraPosInfo.Rotator.Equals(FRotator::ZeroRotator)) ? 0.0f : PreCameraSettings.CameraPosInfo.Time;
}

float UGStoryManager::EndCameraAnim()
{
	SCOPE_CYCLE_COUNTER(STAT_EndCameraAnim);
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);

	if (nullptr == StoryData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::EndCameraAnim: StoryData!"));
		return 0;
	}
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
	int32 PlayId = Profession - 1;
	FENDCAMERA_SETTINGS_DATA EndCameraSettings;
	if (1 == StoryData->EndCameraSettings.Num())
	{
		EndCameraSettings = StoryData->EndCameraSettings[0];
	}
	else
	{
		if ((PlayId >= 0) && (PlayId < StoryData->EndCameraSettings.Num()))
		{
			EndCameraSettings = StoryData->EndCameraSettings[PlayId];
		}
	}
	int EndType = EndCameraSettings.CameraType;	
	FCAMERA_DATA CameraData = EndCameraSettings.CameraSettingInfo.CameraPosInfo;

	switch (EndType)
	{
	case -1:
	{
		if (!CameraData.Rotator.IsZero())
		{
			SetPlayerCamera(CameraData.Rotator);
		}
		else
		{
			return 0;
		}
		break;
	}
	case 0:
		AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();		
		if (IsValid(PlayerActor))
		{
			AController* Controller = PlayerActor->GetController();			
			//玩家默认设置
			if (IsValid(Controller))
			{
				FRotator Rotation = PlayerActor->GetActorRotation();
				SetPlayerCamera(Rotation - FRotator(17.0f, 0.0f, 0.0f));
				Rotation = PlayerActor->GetController()->GetControlRotation();
			}			
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::EndCameraAnim ->End Rotater Rotation->Yaw=%f, Rotation->Pitch=%f, Rotation->Roll=%f"), Rotation.Yaw, Rotation.Pitch, Rotation.Roll);
		}
		break;
	}

	if (CameraData.Time <= 0.0f || (CameraData.Point.IsZero() && CameraData.Rotator.IsZero()))
	{
		CS3_Warning(TEXT("AStoryManager::EndCameraAnim ->End Rotater Is Zero or time is Zero~"));
		if (!EndType)
		{
			ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			if (IsValid(PlayerController) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
			{
				PlayerController->SetViewTargetWithBlend(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			}
		}
		return 0;
	}
	if (AServerCharacter* PlayerActor =UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())
	{
		ClearDelayDestroyCameraTimer();
		UClass* CameraClass = EndCameraSettings.CameraSettingInfo.bCineCamera? UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("CineCamera")):UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("GameCamera"));
		AActor* camera = UGolbalBPFunctionLibrary::SpawnActor<AActor>(CameraClass, CameraData.Point, CameraData.Rotator);
	
		if (IsValid(camera))
		{
			if (EndCameraSettings.CameraSettingInfo.bCineCamera)
			{
				Cast<ACS3CineCameraActor>(camera)->UpdateCineCameraFocusSettings(EndCameraSettings.CameraSettingInfo.ManualFocusDistance, EndCameraSettings.CameraSettingInfo.CurrentFocalLength, EndCameraSettings.CameraSettingInfo.CurrentAperture);
			}
			ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			if (IsValid(PlayerController))
			{
				PlayerController->SetViewTargetWithBlend(camera);

				if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
				{
					PlayerController->SetViewTargetWithBlend(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter(), CameraData.Time);
					bIsEndCamera = true;
					TWeakObjectPtr<UGStoryManager> DelayThisPtr(this);
					TWeakObjectPtr<AActor> DelayCameraPtr(camera);
					UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayDestroyCameraHandle,
						FTimerDelegate::CreateLambda([DelayThisPtr, DelayCameraPtr]() {
						if (DelayCameraPtr.IsValid())
						{
							AActor* CameraPtr = DelayCameraPtr.Get();
							CameraPtr->Destroy();
						}
						if (DelayThisPtr.IsValid())
						{
							UGStoryManager* ThisPtr = DelayThisPtr.Get();
							ThisPtr->ClearDelayDestroyCameraTimer();
						}
					}), CameraData.Time, false);

					return CameraData.Time;
				}
				else
				{
					camera->Destroy();
				}					
			}
			else
			{
				camera->Destroy();
			}
		}
	}
	return 0;
}

void UGStoryManager::CheckPreLoadStory(FString SpaceID, bool& bCanExec, FString& StoryID)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckPreLoadStory);
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager)) return;

	const UConfigTable* StroyConfigTabl =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PRELOADSTORY);

	bCanExec = false;
	StoryID = "";
	TArray<FPRELOADSTORY_DATA*> Rows;
	StroyConfigTabl->GetAllRows(Rows);
	UQuestManager* QuestManager = UUECS3GameInstance::Instance->QuestManager;
	if (IsValid(QuestManager))
	{
		for (FPRELOADSTORY_DATA* Row : Rows)
		{
			bool ExecQuest = false;
			bool ExecTask = false;
			bool Repeat = false;
			bool ExecSpacePreLoad = false;
			if (!FNAME_TO_FSTRING(Row->MapName).Compare(SpaceID))
			{
				if (!Row->QuestId.IsEmpty())
				{
					if (Row->QuestState.IsEmpty())
					{
						ExecQuest = QuestManager->IsQuestStatus(FSTRING_TO_INT(Row->QuestId), 2) || QuestManager->IsQuestStatus(FSTRING_TO_INT(Row->QuestId), 3);
					}
					else
					{
						ExecQuest = QuestManager->IsQuestStatus(FSTRING_TO_INT(Row->QuestId), FSTRING_TO_INT(Row->QuestState));
					}

					if (ExecQuest)
					{
						if (QuestManager->IsQuestStatus(FSTRING_TO_INT(Row->QuestId), 2))
						{
							ExecTask = true;
						}
						else if (QuestManager->IsQuestStatus(FSTRING_TO_INT(Row->QuestId), 3))
						{
							if (!Row->TasksState.IsEmpty())
							{
								TArray<FString> tasks = UGolbalBPFunctionLibrary::SplitString(Row->TasksState, false, TEXT(";"));
								ExecTask = true;
								for (int i = 0; i < tasks.Num(); i++)
								{
									TArray<FString> taskInfo = UGolbalBPFunctionLibrary::SplitString(tasks[i], false, TEXT(":"));
									if (taskInfo.Num() > 1)
									{
										if (!QuestManager->IsTaskStatus(FSTRING_TO_INT(Row->QuestId), FSTRING_TO_INT(taskInfo[0]), FSTRING_TO_INT(taskInfo[1])))
										{
											ExecTask = false;
											break;
										}
									}
								}
							}
							else
							{
								ExecTask = true;
							}
						}
					}
				}
				else
				{
					ExecQuest = true;
					ExecTask = true;
				}

				if (Row->bSpacePreLoad)
				{
					URoleSpaceContentInterface * RoleSpaceContentInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
					if (IsValid(RoleSpaceContentInterface) && RoleSpaceContentInterface->bIsFirstEnterCopy)
					{
						ExecSpacePreLoad = true;
					}
				}
				///<副本需要判断
				if ((ExecQuest && ExecTask) || ExecSpacePreLoad)
				{
					if (Row->PlayPos.Compare(""))
					{
						TArray<FString> PosList = UGolbalBPFunctionLibrary::SplitString(Row->PlayPos, false, "|");
						for (int32 i = 0; i < PosList.Num(); i++)
						{
							TArray<FString> pos = UGolbalBPFunctionLibrary::SplitString(PosList[i], false, " ");
							if (pos.Num() < 3)
							{
								Repeat = true;
								break;
							}
							else
							{
								GameObject* entity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
								if (entity)
								{
									float dis = FVector::Distance(entity->Position(), FVector(FSTRING_TO_INT(pos[0]), FSTRING_TO_INT(pos[1]), FSTRING_TO_INT(pos[2])));
									if (dis <= 500)
									{
										Repeat = true;
										break;
									}
								}
							}
						}
					}
					else
					{
						Repeat = true;
					}
				}

				if (Repeat)
				{
					///<判断副本是否已重置				
					if (Row->Repeat)
					{
						if (!ExecSpacePreLoad && Row->bSpacePreLoad)
							return;
						bCanExec = true;
						StoryID = Row->StoryId;
						return;
					}
					else
					{
						if (!ExecSpacePreLoad && Row->bSpacePreLoad)
							return;

						FString key = (UGolbalBPFunctionLibrary::GetFStringPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("playerName")).Append(TEXT("_"))).Append(Row->QuestId);
						if (!UGolbalBPFunctionLibrary::LocalDataSaveManager()->LocalData->GetPreLoadStoryLocalData(key, Row->StoryId))
						{
							bCanExec = true;
							StoryID = Row->StoryId;
							return;
						}
					}
				}
			}
		}
	}
}

const FSTORY_DATA* UGStoryManager::GetStoryData(const FString& SequenceId)
{
	if ((!IsValid(UUECS3GameInstance::Instance))|| (!IsValid(UUECS3GameInstance::Instance->CfgManager))||SequenceId.IsEmpty())return nullptr;

	const FSTORY_DATA* StroyData =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_STORY)->GetRow<FSTORY_DATA>(SequenceId);
	if (!StroyData) CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::GetStoryData : StroyData!"));

	return StroyData;
}

const FSTORY_EVENT_DATA* UGStoryManager::GetStoryEventData(const FString& SequenceId)
{
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::GetStoryEventData : Instance && Instance->CfgManager!"));
		return nullptr;
	}
	const FSTORY_EVENT_DATA* StroyEventData =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STORY_EVENT)->GetRow<FSTORY_EVENT_DATA>(SequenceId);
	if (!StroyEventData) CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::GetStoryEventData : StroyEventData!"));

	return StroyEventData;
}

const FSTORY_ANIM_EVENT* UGStoryManager::GetStoryAnimEventData(const FString& AnimName)
{
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager)) return nullptr;

	const FSTORY_ANIM_EVENT* StroyAnimEventData =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STORY_ANIM_EVENT)->GetRow<FSTORY_ANIM_EVENT>(AnimName);
	if (!StroyAnimEventData) CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::GetStoryAnimEventData : StroyAnimEventData!"));

	return StroyAnimEventData;
}

void UGStoryManager::SwitchStoryMode(bool IsPlay)
{
	SCOPE_CYCLE_COUNTER(STAT_SwitchStoryMode);
	APlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (PlayerController && PlayerActor)
	{
		// 设置玩家控制(设置剧情模式)
		PlayerController->SetCinematicMode(IsPlay, false, true, true, true);
		// 鼠标显示与隐藏
		PlayerController->bShowMouseCursor = !IsPlay;
	}
	// 设置剧情控制状态
	if (ACS3PlayerController* GamePC = Cast<ACS3PlayerController>(PlayerController))
	{
		if (IsPlay)
		{
			UAtkStateMar* AtkState = GamePC->GetAtkStateMar();

			if (IsValid(AtkState))
			{
				if (AtkState->IsHaveState(EATTACT_STATE::AUTO_ATT))
				{
					AtkState->SwitchAutoFight(false, EBreakAutomaticType::NoneBreakType);
				}
			}
			int32 Index = 0;
			if (IsControlledByPlayer())
			{
				Index = 1;
				// 设置玩家控制(设置剧情模式)
				PlayerController->SetCinematicMode(false, false, false, true, true);
				// 鼠标显示与隐藏
				PlayerController->bShowMouseCursor = true;
			}

			GamePC->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_STORY, true, Index);
			
			if (IsValid(GamePC->GetAtkStateMar()))
			{
				GamePC->GetAtkStateMar()->SwitchFightInStoryAtt(true);
			}
		}
		else
		{
			GamePC->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_STORY, false);
			if (FadeTimer > 0.0f)
			{
				SetManualCameraFade();
			}
			if (IsValid(GamePC->GetAtkStateMar()))
			{
				GamePC->GetAtkStateMar()->SwitchFightInStoryAtt(false);
			}
		}
	}
}

void UGStoryManager::PausedVoice(bool bPause, const FString HideVoiceType)
{
	/** 0.暂停语音类型  1.暂停战斗音乐
	2.暂停背景音乐		3.纯客户端语音
	4.3D语音			例0|1|2|4 */
	TArray<FString> PauseTypes;
	PauseTypes = UGolbalBPFunctionLibrary::SplitString(GetPausedVoiceType(), true);
	if (!bPause)
	{		
		TArray<FString> tempHide = UGolbalBPFunctionLibrary::SplitString(GetPausedVoiceType(true), true);
		for (auto data: tempHide)
		{
			PauseTypes.AddUnique(data);
		}		
	}

	TArray<FString> HideVoiceTypes= UGolbalBPFunctionLibrary::SplitString(HideVoiceType, true);

	if (PauseTypes.Num()>0&&UGolbalBPFunctionLibrary::AudioManager()&& IsValid(UGolbalBPFunctionLibrary::AudioManager()))
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetPausedVoice(PauseTypes, HideVoiceTypes, bPause);
	}
}

FString UGStoryManager::GetPausedVoiceType(bool bIsHideNewVioce)
{
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	FString HideVoiceType = TEXT("");

	if (nullptr == StoryData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::GetPausedVoiceType: StoryData!"));
		return HideVoiceType;
	}
	TArray<FString> HideVoiceTypes=StoryData->HideVoiceType;
	if (bIsHideNewVioce)
	{
		HideVoiceTypes = StoryData->HideNewVoice;
	}
	
	if (1 == HideVoiceTypes.Num())
	{
		HideVoiceType = HideVoiceTypes[0];
	}
	else
	{
		int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
		int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
		int32 PlayId = Profession - 1;
		if ((PlayId >= 0) && (PlayId < HideVoiceTypes.Num()))
		{
			HideVoiceType = HideVoiceTypes[PlayId];
		}
		else
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("GetStoryAsset -> HideVoiceType PlayId[%d] asset is not found~"), PlayId);
			return HideVoiceType;
		}
	}
	return  HideVoiceType;	
}

void UGStoryManager::HidePlayer()
{
	if (APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
	{
		PlayerActor->StopAction();
		PlayerActor->StopPlayerMove();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::HidePlayer -> EntityID[%d]~"), PlayerActor->EntityId);
		HideEntitiesList.AddUnique(PlayerActor->EntityId);
		UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	}
}

void UGStoryManager::HideOtherPlayer()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::HideOtherPlayer~"));
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	if (KbeApp == nullptr || KbeApp->Entities() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::HideOtherPlayer : KbeApp||KbeApp->Entities()!"));
		return;
	}

	TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity && !Entity->IsPlayer() && !Entity->ClassName().Compare(FString("Role")))
		{
			if (AActor* Actor = Entity->Actor())
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::HideOtherPlayer -> EntityID[%d]~"), Entity->ID());
				HideEntitiesList.AddUnique(Entity->ID());
				UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor);
			}
		}
	}
}

void UGStoryManager::HideOtherPlayerPet()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::HideOtherPlayerPet~"));
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	if (KbeApp == nullptr || KbeApp->Entities() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::HideOtherPlayerPet : KbeApp||KbeApp->Entities()!"));
		return;
	}
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	int32 PlayerPetId = 0;
	if (PlayerActor)
	{
		PlayerPetId = PlayerActor->PetEntityId;
	}
	
	TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity && !Entity->IsPlayer() && !Entity->ClassName().Compare(FString("VehiclePet")))
		{
			if (PlayerPetId == Entity->ID())continue;///<玩家幻兽
			if (AActor* Actor = Entity->Actor())
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::HideOtherPlayerPet -> EntityID[%d]~"), Entity->ID());
				HideEntitiesList.AddUnique(Entity->ID());
				UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor);
			}
		}
	}
}

void UGStoryManager::HidePlayerPet()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::HidePlayerPet~"));
	if (APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
	{
		if (PlayerActor->PetEntityId != 0)
		{
			KBEngine::Entity* Entity = UGolbalBPFunctionLibrary::FindEntity(PlayerActor->PetEntityId);
			if (Entity && !Entity->ClassName().Compare(FString("VehiclePet")))
			{
				if (AActor* Actor = Entity->Actor())
				{
					CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::HidePlayerPet -> EntityID[%d]~"), PlayerActor->PetEntityId);
					HideEntitiesList.AddUnique(PlayerActor->PetEntityId);
					UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor);
				}
			}
		}
	}
}

void UGStoryManager::HideNonPlayerEntity()
{
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	if (!StoryData || KbeApp==nullptr || KbeApp->Entities() == nullptr)	
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::HideNonPlayerEntity : StoryData||KbeApp||KbeApp->Entities()!"));
		return;
	}

	FHIDEENTITY_DATA HideEntity = StoryData->HideEntity;
	TArray<FString> ShowByScriptIds = UGolbalBPFunctionLibrary::SplitString(HideEntity.Param2, true);
	TArray<FString> ShowByClassNames = UGolbalBPFunctionLibrary::SplitString(HideEntity.Param3, true);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::HideNonPlayerEntity -> FHIDEENTITY_DATA:ShowByScriptIds[%s], ShowByClassNames[%s]~"), *HideEntity.Param2, *HideEntity.Param3);

	TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity && Entity->ClassName().Compare(FString("Role"))&& Entity->ClassName().Compare(FString("VehiclePet")))
		{
			/** 显示ClassName的Entity */
			if (UGolbalBPFunctionLibrary::IsContainStr(Entity->ClassName(), ShowByClassNames)) continue;
			/** 显示ScriptId的Entity */
			FString EntityScriptId = Entity->GetDefinedProperty(TEXT("scriptID")).GetValue<FString>();
			if (UGolbalBPFunctionLibrary::IsContainStr(EntityScriptId, ShowByScriptIds)) continue;
			// 隐藏的Entity
			if (AActor* Actor = Entity->Actor())
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::HideNonPlayerEntity -> EntityID[%d]~"), Entity->ID());
				HideEntitiesList.AddUnique(Entity->ID());
				UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor);
			}
		}
	}
}

void UGStoryManager::StoryHideEntities(bool bIsHide)
{
	SCOPE_CYCLE_COUNTER(STAT_StoryHideEntities);
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	if (!StoryData || KbeApp == nullptr || KbeApp->Entities() == nullptr)	
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::StoryHideEntities : StoryData||KbeApp||KbeApp->Entities()!"));
		return;
	}
	TArray<FString> HideTypes = UGolbalBPFunctionLibrary::SplitString(StoryData->HideEntity.HideType, true);
	///<纯客户端Actor显示模型的UID
	TArray<FString> IgnoreUIDs = UGolbalBPFunctionLibrary::SplitString(StoryData->HideEntity.Param4, true);
	if (bIsHide)
	{
		/** 0.隐藏其他玩家类型		1.只隐藏玩家自己
		2.只隐藏其他玩家宠物	3.只隐藏自己宠物
		4.隐藏周围战斗实体随机组合 例0|1|2|4 */
		
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::StoryHideEntities -> FHIDEENTITY_DATA.HideType[%s]~"), *StoryData->HideEntity.HideType);
		for (auto& Elem : HideTypes)
		{
			int32 HideNum = FCString::Atoi(*Elem);
			switch (HideNum)
			{
			case 0: HideOtherPlayer(); break;
			case 1: HidePlayer(); break;
			case 2: HideOtherPlayerPet(); break;
			case 3: HidePlayerPet(); break;
			case 4: HideNonPlayerEntity(); break;
			case 5: HideSceneCharacter(IgnoreUIDs); break;
			default: CS3_Warning(TEXT("AStoryManager::StoryHideEntities -> FHIDEENTITY_DATA->Param1 HideNum[%s] is not found~"), *Elem); break;
			}
		}
		/** 只隐藏ScriptId的Entity */
		if (!HideTypes.Contains(FString("4")))
		{
			TArray<FString> HideByScriptIds = UGolbalBPFunctionLibrary::SplitString(StoryData->HideEntity.Param1, true);
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::StoryHideEntities -> FHIDEENTITY_DATA:HideByScriptIds[%s]~"), *StoryData->HideEntity.Param1);

			TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
			for (auto& Elem : EntitiesMap)
			{
				KBEngine::Entity* Entity = Elem.Value;
				if (Entity && Entity->ClassName().Compare(FString("Role")))
				{
					FString EntityScriptId = Entity->GetDefinedProperty(TEXT("scriptID")).GetValue<FString>();
					if (!UGolbalBPFunctionLibrary::IsContainStr(EntityScriptId, HideByScriptIds)) continue;
					// 隐藏的Entity
					if (AActor* Actor = Entity->Actor())
					{
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::StoryHideEntities -> EntityID[%d]~"), Entity->ID());
						HideEntitiesList.AddUnique(Entity->ID());
						UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor);
					}
				}
			}
		}
	}
	else
	{
		TArray<int32> EntitiesList = HideEntitiesList;
		// 显示隐藏的Entity
		if (EntitiesList.Num() > 0)
		{
			for (int32 Id : EntitiesList)
			{
				if (UUECS3GameInstance::pKBEApp == nullptr)
				{
					return;
				}
				KBEngine::Entity* Entity = UUECS3GameInstance::pKBEApp->FindEntity(Id);
				if (Entity)
				{
					UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Entity->Actor());
				}
			}
		}		
		HideSceneCharacter(IgnoreUIDs);
	}
}

void UGStoryManager::HideSceneCharacter(TArray<FString> IgnoreUIDs)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SpaceDynamicEffectManager))
	{
		UUECS3GameInstance::Instance->SpaceDynamicEffectManager->UpdateModelVisible(IgnoreUIDs);
	}
}

void UGStoryManager::DisRideOnCarrier()
{
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	if (StoryData)
	{
		if (StoryData->DisRide)
		{
			AServerCharacter* Player =UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
			if (IsValid(Player))
			{
				APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(Player);
				if (IsValid(PlayerCharacter) && PlayerCharacter->IsRidePetState())
				{
					URolePetInterface * Interface = Cast<URolePetInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePetInterface"), 0));

					if (IsValid(Interface))
					{
						Interface->RequestTransformPetFC();
					}
				}				
			}
		}
	}
}

void UGStoryManager::IsOpenMediaUI(bool IsOpen)
{
	//CS3_Warning(TEXT("~~~~~~~UGStoryManager::IsOpenMediaUI: SequenceId=%s!"), *CurrPlayId);
	UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::CreateRole, TEXT("CreateCG"));
	UBaseWindow* CGWidget = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("CreateCG"));
	if (!IsValid(CGWidget))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::IsOpenMediaUI : CGWidget!"));
		return;
	}
	if (IsValid(CGWidget) && !IsOpen)
	{
		CGWidget->Destroy();
	}
}

void UGStoryManager::ResetHZMGStoryOperate()
{
	if (LevelSequenceActor && IsValid(LevelSequenceActor))
	{
		if (ACS3PlayerController* GamePC = Cast<ACS3PlayerController>(UGolbalBPFunctionLibrary::GetCS3PlayerController()))
		{
			UAtkStateMar* AtkState = GamePC->GetAtkStateMar();

			if (IsValid(AtkState))
			{
				if (IsValid(GamePC->GetAtkStateMar()))
				{
					AtkState->SwitchFightInStoryAtt(false);
				}
			}
			GamePC->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_STORY, false);
		}
		HideEntitiesList.Reset();
	}
}


void UGStoryManager::LoadNextSubLevelFinished(FString NextSubLevelName)
{
	if (!CurrPlayId.Compare(TEXT("")) || JumpToFrameCount == 0)return;
	CheckIsStopLoop();
}

void UGStoryManager::CheckIsStopLoop()
{
	AInWorldStreamLevel* LevelScriptActor = Cast<AInWorldStreamLevel>(UGolbalBPFunctionLibrary::GetMainLevelActor());

	if (LevelScriptActor && LevelScriptActor->GetIsNextSubLevelFinished())
	{
		PlayToFrameSequence(GetPlayToFrameData());
	}
}

void UGStoryManager::InWorldLoadingOverEvent()
{
	if (!CurrPlayId.Compare(TEXT("")) || DelayStopInWorldOverHandle.IsValid())return;
	if (JumpToFrameCount > 1 && bIsJumpToOpenDoorFinished)
	{
		CheckStopInWorldOver();
	}
}

void UGStoryManager::CheckStopInWorldOver()
{
	if (UUECS3GameInstance::Instance&&UUECS3GameInstance::Instance->GameStatus &&
		UUECS3GameInstance::Instance->GameStatus->GetIsInWorldLoadingOver())
	{
		StopSequence();
		///回调服务器
		URoleSpaceContentInterface * RoleSpaceContentInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), 0));
		if (RoleSpaceContentInterface)
		{
			RoleSpaceContentInterface->RPC_CELL_OnPlaySpaceIntroduceVoice();
		}
	}	
}

bool UGStoryManager::IsStopLoadingLevel()
{
	if (FSTORY_DATA* StoryData = const_cast<FSTORY_DATA*>(GetStoryData(CurrPlayId)))
	{
		return StoryData->IsStopLoadingLevel;
	}
	return  true;
}

void UGStoryManager::ClientSetAoi()
{
	if (const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId))
	{
		FString Radius = StoryData->Aoi;
		if (!Radius.IsEmpty())
		{
			APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			if (IsValid(PlayerCharacter))
			{
				PlayerCharacter->ClientSetAoi(Radius);
			}
		}
	}
}

void UGStoryManager::ClientResetAoi() 
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->ClientResetAoi();
	}
}

void UGStoryManager::SetPlayerCamera(FRotator Rotater)
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(PlayerActor) && IsValid(PlayerActor->GetController()))
	{
		PlayerActor->GetController()->SetControlRotation(Rotater);
	}
}

void UGStoryManager::OnDelayStoppingStoryOperate()
{
	bIsEndCamera = false;
	PausedVoice(false, "");
	bIsPlayingToUI = false;
	if (IsValid(LevelSequenceActor))
	{
		StoryTriggerUI(false);
	}
	onNotifyRemoveEffectList();
	///回调服务器
	URoleStoryInterface * RoleStoryInterface = Cast<URoleStoryInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStoryInterface"), 0));
	if (RoleStoryInterface)
	{
		RoleStoryInterface->RPC_onStopPlayStory(CurrPlayId);
	}

	if (StopSequenceDelegate.IsBound())
	{
		StopSequenceDelegate.Broadcast(CurrPlayId);
	}

	// 重置剧情数据
	ResetStoryData();
	SwitchStoryMode(false);

	if (UGolbalBPFunctionLibrary::AudioManager() && IsValid(UGolbalBPFunctionLibrary::AudioManager()))
	{
		UGolbalBPFunctionLibrary::AudioManager()->ResetStoryAudio();
	}
	URolePerformanceInterface * Interface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
	if (Interface)
	{
		Interface->OnStoryPlayEnd();
	}
}

void UGStoryManager::SetManualCameraFade()
{
	APlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->PlayerCameraManager->StartCameraFade(1.0f, 1.0f, FadeTimer, FLinearColor(.0f, .0f, .0f, 1.f), false);
	}
}

void UGStoryManager::StopAllCameraShakes()
{
	UWorld* GameWorld = UUECS3GameInstance::Instance->GetWorld();
	// 设置镜头抖动相关
	if (GameWorld && IsValid(GameWorld))
	{
		APlayerCameraManager* PlayerCameraManager = UGameplayStatics::GetPlayerCameraManager(GameWorld, 0);
		if (PlayerCameraManager&&IsValid(PlayerCameraManager))
		{
			PlayerCameraManager->StopAllCameraShakes();
		}
	}
}

void UGStoryManager::RelPlaySequence(TSoftObjectPtr<ULevelSequence> StroyAss, int32 NumLoops, const FString& SequenceId)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UGStoryManager::RelPlaySequence~"));
	if (LevelSequenceActor && LevelSequenceActor->SequencePlayer && LevelSequenceActor->SequencePlayer->IsPlaying())
	{
		LevelSequenceActor->SequencePlayer->Stop();
	}

	ULevelSequence**StoryAssValue = StoryAssList.Find(SequenceId);
	if (StoryAssValue != nullptr && IsValid(*StoryAssValue))
	{
		PrePlaySequence(*StoryAssValue, NumLoops, SequenceId);
		return;
	}

	//镜头语音半身像模型资源
	TArray<FStringAssetReference> LoadPartArray;
	const FSTROY_LOAD_MODEL_DATA* LoadModelData = GetPreLoadStoryVoiceModelAsset(SequenceId);
	if (LoadModelData)
	{
		for (auto val : LoadModelData->LoadModelList)
		{
			LoadPartArray.Add(val.ToSoftObjectPath());
		}
	}

	//镜头资源已存在直接用
	if (IsValid(StroyAss.Get()))
	{
		if (LoadPartArray.Num() == 0)
		{
			//没有需要加载的语音半身像模型资源，直接播镜头
			PrePlaySequence(StroyAss.Get(), NumLoops, SequenceId);
			return;
		}
	}
	else
	{
		if (StroyAss.ToSoftObjectPath().IsValid())
		{			
			LoadPartArray.Add(StroyAss.ToSoftObjectPath());
		}
		else
		{
			CS3_Warning(TEXT("UGStoryManager::RelPlaySequence StroyAss.ToSoftObjectPath() is Null~,StoryID = %s"), *SequenceId);
		}
	}

	if (LoadPartArray.Num() > 0)
	{
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, LoadPartArray,
			FStreamableDelegate::CreateLambda([this, StroyAss, NumLoops, SequenceId, LoadModelData]()
		{
			if (LoadModelData && LoadModelData->HeadModelID.Num() > 0)
			{
				LoadStroyModel(LoadModelData->HeadModelID);
			}
			if (IsValid(StroyAss.Get()))
			{
				PrePlaySequence(StroyAss.Get(), NumLoops, SequenceId);
			}
		}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_STORY);
	}
}

void UGStoryManager::PrePlaySequence(ULevelSequence* StroyAss, int32 NumLoops, const FString& SequenceId)
{
	SCOPE_CYCLE_COUNTER(STAT_PrePlaySequence);

	if (!IsValid(LevelSequenceActor))return;
	CSV_EVENT_GLOBAL(TEXT("PrePlaySequence %s"), *StroyAss->GetName());
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->CS3ConSoleMgr))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->CS3ConSoleMgr->DisplayStoryLog(SequenceId,true);
	}
	ResetStoryData();		// 确保每次数据为初始值
	CurrPlayId = SequenceId;
	bIsPlayingToUI = true;
	StroyAss->PrecompiledEvaluationTemplate = FMovieSceneEvaluationTemplate();
	LevelSequenceActor->SetSequence(StroyAss);
	// 中断所有语音
	if (UGolbalBPFunctionLibrary::AudioManager() && IsValid(UGolbalBPFunctionLibrary::AudioManager()))
	{
		UGolbalBPFunctionLibrary::AudioManager()->StopVoice();
	}

	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	if (nullptr == StoryData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::PrePlaySequence: StoryData!"));
		return;
	}
	FString HideVoiceType = GetPausedVoiceType(true);
	PausedVoice(true, HideVoiceType);
	StoryTriggerUI(true);
	onNotifyAddEffectList();
	float delayTime = PreCameraTime();
	if (delayTime > 0.0f)
	{
		bIsPreCamera = true;
		if (StoryData->HideInputByPreCamera)
		{
			SwitchStoryMode(true);
		}
		if (StoryData->PreCameraOperation)
		{
			OnStoryOperation();
		}
		PlayPreCamera(NumLoops);
		return;
	}
	OnDelayPlayStoryOperate(NumLoops);
}

void UGStoryManager::StartPlaySequence(int32 NumLoops/* = 1*/)
{
	SCOPE_CYCLE_COUNTER(STAT_StartPlaySequence);

	FSTORY_DATA* StoryData =const_cast<FSTORY_DATA*>(GetStoryData(CurrPlayId));
	if (StoryData == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::OnDelayPlayStoryOperate : StoryData||KbeApp||KbeApp->Entities()!"));
		return;
	}

	if (!(LevelSequenceActor && LevelSequenceActor->SequencePlayer))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::StartPlaySequence : (LevelSequenceActor && LevelSequenceActor->SequencePlayer)!"));
		return;
	}
	if (StartSequenceDelegate.IsBound())
	{
		StartSequenceDelegate.Broadcast(CurrPlayId);
	}

	if (StoryData->IsHZMGOpenDoorStory)
	{
		AInWorldStreamLevel* LevelScriptActor = Cast<AInWorldStreamLevel>(UGolbalBPFunctionLibrary::GetMainLevelActor());
		if (LevelScriptActor)
		{
			if (LevelScriptActor->GetIsNextSubLevelFinished())
			{
				NumLoops = 1;
			}
			else 
			{
				LevelScriptActor->LoadNextSubLevelFinishedDelegate.AddUObject(this, &UGStoryManager::LoadNextSubLevelFinished);
			}
		}
	}

	if (StoryData->IsStopInWorldOver)
	{
		if (UUECS3GameInstance::Instance&&UUECS3GameInstance::Instance->GameStatus)
		{
			UUECS3GameInstance::Instance->GameStatus->InWorldLoadingOver.AddDynamic(this, &UGStoryManager::InWorldLoadingOverEvent);
		}
	}

	LevelSequenceActor->SequencePlayer->PlayToFrame(LevelSequenceActor->SequencePlayer->GetStartTime().Time);
	if (1 != NumLoops)
	{
		LevelSequenceActor->SequencePlayer->PlayLooping(NumLoops);
	}
	else
	{
		LevelSequenceActor->SequencePlayer->Play();
	}
	// 绑定完成回调

	if (!LevelSequenceActor->SequencePlayer->OnStop.IsBound())
	{
		LevelSequenceActor->SequencePlayer->OnStop.AddDynamic(this, &UGStoryManager::OnStoryStop);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::PlaySequence -> Bind OnStop~"));
	}
}

void UGStoryManager::OnDelayPlayStoryOperate(int32 NumLoops /*= 1*/)
{
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	if (StoryData == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::OnDelayPlayStoryOperate : StoryData||KbeApp||KbeApp->Entities()!"));
		return;
	}
	if (bIsPreCamera)
	{
		bIsPreCamera = false;
		StartPlaySequence(NumLoops);
		if (!StoryData->HideInputByPreCamera)
		{
			SwitchStoryMode(true);
		}
		if (!StoryData->PreCameraOperation)
		{
			OnStoryOperation();
		}
		return;
	}
	StartPlaySequence(NumLoops);
	SwitchStoryMode(true);
	OnStoryOperation();
}

void UGStoryManager::ClearDelayDestroyCameraTimer()
{
	if (DelayDestroyCameraHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayDestroyCameraHandle);
	}
}

void UGStoryManager::LoadStoryAssetEnd(TSoftObjectPtr<ULevelSequence> stroyAss/*==nullptr*/)
{
	TArray<TSoftObjectPtr<ULevelSequence>> ValueArray;
	StoryAss.GenerateValueArray(ValueArray);
	if (ValueArray.Contains(stroyAss))
	{
		Count++;
		if (LoadStoryOverDelegate.IsBound())
		{
			LoadStoryOverDelegate.Broadcast();
		}
	}
}

void UGStoryManager::OnStoryStop()
{
	CS3_Warning(TEXT("~~~~~~~UGStoryManager::OnStoryStop: SequenceId=%s!"), *CurrPlayId);
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->CS3ConSoleMgr))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->CS3ConSoleMgr->DisplayStoryLog(CurrPlayId, false);
	}
	BP_OnStoryStop();
	float time = 0.0f;
	if (IsValid(LevelSequenceActor) && IsValid(LevelSequenceActor->SequencePlayer))
	{
		LevelSequenceActor->SequencePlayer->OnStop.Clear();
		time = EndCameraAnim();
	}

	StopAllCameraShakes();

	// 设置默认AOI
	ClientResetAoi();
	if (CheckOneTimeHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CheckOneTimeHandle);
	}
	if (DelayStopInWorldOverHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayStopInWorldOverHandle);
	}
	///<CST-7240
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	if (StoryData != nullptr)
	{
		if (StoryData->IsMedia)
		{
			IsOpenMediaUI(false);
		}

		if (StoryData->IsHZMGOpenDoorStory)
		{
			AInWorldStreamLevel* LevelScriptActor = Cast<AInWorldStreamLevel>(UGolbalBPFunctionLibrary::GetMainLevelActor());
			if (LevelScriptActor&&LevelScriptActor->LoadNextSubLevelFinishedDelegate.IsBoundToObject(this))
			{
				LevelScriptActor->LoadNextSubLevelFinishedDelegate.RemoveAll(this);
			}
		}
		if (StoryData->IsStopInWorldOver)
		{
			if (UUECS3GameInstance::Instance&&UUECS3GameInstance::Instance->GameStatus)
			{
				UUECS3GameInstance::Instance->GameStatus->InWorldLoadingOver.RemoveAll(this);
			}
		}
	}
	StoryHideEntities(false);
	if (time > 0)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, this, &UGStoryManager::OnDelayStoppingStoryOperate, time, false);
	}
	else
	{
		OnDelayStoppingStoryOperate();
	}
}

void UGStoryManager::OnStoryOperation()
{
	StoryHideEntities(true);	
	// 设置玩家AOI
	ClientSetAoi();
	DisRideOnCarrier();
}

void UGStoryManager::PreLoadStory(const FName& SpaceId)
{
	UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	if (IsValid(GameInstance) && IsValid(GameInstance->GameStatus))
	{
		if (GameInstance->GameStatus->IsCurrStatus(EGameStatus::InWorld))
		{
			FString StoryID;
			bool bCanExec;
			CheckPreLoadStory(FNAME_TO_FSTRING(SpaceId), bCanExec, StoryID);
			if (bCanExec)
			{
				PlaySequence(StoryID);
				return;
			}
		}
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Exec Pre Load Story Fail~"));
}

int UGStoryManager::PreLoadStoryAsset(const FLoadStoryOverDelegate& InLoadStoryOverDelegate /*= FLoadStoryOverDelegate()*/)
{
	SCOPE_CYCLE_COUNTER(STAT_PreLoadStoryAsset);
	StoryAss.Reset();
	AllStoryAss.Reset();
	StoryAssList.Reset();
	Count = 0;
	LoadStoryOverDelegate = InLoadStoryOverDelegate;
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager)) 
	{
		LoadStoryAssetEnd();
		return StoryAss.Num();
	}

	const UConfigTable* StroyConfigTabl =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_STORY);
	if (!IsValid(StroyConfigTabl))
	{
		LoadStoryAssetEnd();
		return StoryAss.Num();
	}
	TArray<FSTORY_DATA*> Rows;
	StroyConfigTabl->GetAllRows(Rows);
	TArray<FName> RowNames = StroyConfigTabl->GetRowNames();
	
	if (0 == Rows.Num()) 
	{
		LoadStoryAssetEnd();
		return StoryAss.Num();
	}
	const FString SpaceId = UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID"));

	for (FName RowName : RowNames)
	{
		const FSTORY_DATA* STORY_DATA = (FSTORY_DATA*)StroyConfigTabl->GetRow(RowName);
		if (!STORY_DATA || (STORY_DATA->Assets.Num() <= 0))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::PreLoadStoryAsset : STORY_DATA!"));
			continue;
		}
		bool bIsQuestAsset = false;
		TArray<FString> QuestIDs = UGolbalBPFunctionLibrary::SplitString(STORY_DATA->QuestID);

		if (QuestIDs.Num() > 0)
		{
			if (QuestIDs.Contains(TEXT("-1")))
			{
				bIsQuestAsset = true;
			}
			else
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
		}	

		TArray<FString> SpaceName = UGolbalBPFunctionLibrary::SplitString(STORY_DATA->Space);
		if (SpaceName.Contains(SpaceId))
		{
			int32 AssetAccount = STORY_DATA->Assets.Num();
			if (1 == AssetAccount)
			{
				if (STORY_DATA->Assets[0].ToSoftObjectPath() == nullptr)
				{
					break;
				}
				AllStoryAss.Add(FNAME_TO_FSTRING(RowName), STORY_DATA->Assets[0]);
				if (bIsQuestAsset)
				{
					StoryAss.Add(FNAME_TO_FSTRING(RowName), STORY_DATA->Assets[0]);
				}
			}
			else
			{
				int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
				int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
				int32 Gender = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "gender");
				int32 PlayId = Profession - 1;
				if (Gender == 2)
				{
					if (4 != AssetAccount)
					{
						PlayId = Profession + 3;
						if (2 == AssetAccount || 5 == AssetAccount)
						{
							PlayId = AssetAccount - 1;
						}
					}
				}
				else if (2 == AssetAccount)
				{
					PlayId = 0;
				}

				if ((PlayId >= 0) && (PlayId < AssetAccount))
				{
					if (STORY_DATA->Assets[PlayId].ToSoftObjectPath() == nullptr)
					{
						break;
					}
					AllStoryAss.Add(FNAME_TO_FSTRING(RowName), STORY_DATA->Assets[PlayId]);
					if (bIsQuestAsset)
					{
						StoryAss.Add(FNAME_TO_FSTRING(RowName), STORY_DATA->Assets[PlayId]);
					}
				}
			}
		}
	}
	
	if (0 == AllStoryAss.Num())
	{
		LoadStoryAssetEnd();
		return 0;
	}
	
	for (auto& data : StoryAss)
	{
		LoadStoryAsset(data.Key, data.Value);
	}
	return StoryAss.Num();
}

void UGStoryManager::PreLoadAllStoryAsset()
{
	TWeakObjectPtr<UGStoryManager> DelayThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayLoadAllStoryHandle,
		FTimerDelegate::CreateLambda([DelayThisPtr]() {
		if (DelayThisPtr.IsValid())
		{
			UGStoryManager* ThisPtr = DelayThisPtr.Get();
			for (auto& data : ThisPtr->AllStoryAss)
			{
				if (!ThisPtr->StoryAss.Contains(data.Key))
				{
					ThisPtr->LoadStoryAsset(data.Key, data.Value);
				}
			}
		}
	}), 0.2f, false);
}

const FSTROY_LOAD_MODEL_DATA* UGStoryManager::GetPreLoadStoryVoiceModelAsset(FString SequenceId)
{
	TArray<FStringAssetReference> LoadPartArray;

	auto StroyModelData = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STROY_LOAD_MODEL_DATA);
	const FSTROY_LOAD_MODEL_DATA* LoadModelData = StroyModelData->GetRow<FSTROY_LOAD_MODEL_DATA>(SequenceId);
	return LoadModelData;
}

void UGStoryManager::LoadStoryAsset(FString storyID, TSoftObjectPtr<ULevelSequence> stroyAss)
{
	TArray<FStringAssetReference> LoadPartArray;
	const FSTROY_LOAD_MODEL_DATA* LoadModelData = GetPreLoadStoryVoiceModelAsset(storyID);
	if (LoadModelData)
	{
		for (auto val : LoadModelData->LoadModelList)
		{
			LoadPartArray.Add(val.ToSoftObjectPath());
		}
	}

	//已存在直接用
	if (IsValid(stroyAss.Get()))
	{
		if (LoadPartArray.Num() == 0) //没有需要加载的语音半身像模型资源
		{
			LoadStoryAssetEnd(stroyAss);
			StoryAssList.Add(storyID, stroyAss.Get());
			return;
		}
	}
	else
	{
		if (stroyAss.ToSoftObjectPath() == nullptr)
		{
			CS3_Warning(TEXT("UGStoryManager::LoadStoryAsset StroyAss.ToSoftObjectPath() is Null~,StoryID = %s"), *storyID);
			if (LoadPartArray.Num() == 0) //没有需要加载的语音半身像模型资源
			{
				LoadStoryAssetEnd(stroyAss);
				StoryAssList.Add(storyID, stroyAss.Get());
				return;
			}
		}
		if (stroyAss.ToSoftObjectPath().IsValid())
		{
			LoadPartArray.Add(stroyAss.ToSoftObjectPath());
		}
	}

	if (LoadPartArray.Num() > 0)
	{
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, LoadPartArray,
			FStreamableDelegate::CreateLambda([this, stroyAss, storyID, LoadModelData]()
		{
			if (LoadModelData && LoadModelData->HeadModelID.Num() > 0)
			{
				LoadStroyModel(LoadModelData->HeadModelID);
			}
			LoadStoryAssetEnd(stroyAss);
			StoryAssList.Add(storyID, stroyAss.Get());
		}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_STORY);
	}
}

bool UGStoryManager::CanSkip(bool& IsMedia)
{
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	if (nullptr == StoryData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::CanSkip: StoryData!"));
		return true;
	}
	IsMedia = StoryData->IsMedia;
	return (IsMedia || StoryData->Skip < 0.0f) ? false : true;
}

float UGStoryManager::GetSkipTimeData(float& EndTime, float& CurTime, float& StartTime)
{
	//开始时间 
	StartTime = (LevelSequenceActor->SequencePlayer->GetStartTime()).AsSeconds();
	EndTime = (LevelSequenceActor->SequencePlayer->GetEndTime()).AsSeconds();
	CurTime = (LevelSequenceActor->SequencePlayer->GetCurrentTime()).AsSeconds();
	float Length = FMath::Max(EndTime - StartTime, 0.0f);
	CurTime = FMath::Max(CurTime - StartTime, 0.0f);
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	if (nullptr == StoryData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::GetSkipTimeData: StoryData!"));
		return 0.0f;
	}

	if (StoryData->Skip > Length || StoryData->Skip < 0.0f)
	{
		return  FMath::Max(Length - CurTime, 0.0f);
	}

	return FMath::Max(StoryData->Skip - CurTime, 0.0f);
}

bool UGStoryManager::IsControlledByPlayer()
{
	//根据配置表的数据来判断  对剧情状态控制进行处理
	FCAMERA_DATA CameraData;
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);

	if (nullptr == StoryData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::IsControlledByPlayer: StoryData!"));
		return false;
	}
	if (StoryData->IsControlledByPlayer)
	{
		TArray<FString> HideTypes = UGolbalBPFunctionLibrary::SplitString(StoryData->HideEntity.HideType, true);
		///是否隐藏玩家
		if (!HideTypes.Contains(TEXT("1")))
		{
			return true;
		}
	}

	return false;
}

void UGStoryManager::ClearStoryAsset()
{
	StoryAssList.Empty();
	StoryAss.Empty();
}

void UGStoryManager::BP_GetStoryData(const FString& SequenceId, FSTORY_DATA& StoryData)
{
	const FSTORY_DATA* StoryDataPoint = GetStoryData(CurrPlayId);
	if (StoryDataPoint ==nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::BP_GetStoryData : StoryDataPoint!"));
		return;
	}
	StoryData = *StoryDataPoint;
}

bool UGStoryManager::IsNeedHideUI()
{
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);
	if (StoryData==nullptr)
	{
		return false;
	}
	if (StoryData->HideUI && bIsPlayingToUI)
	{
		return true;
	}
	return false;
}

void UGStoryManager::SetPlayRate(float rate)
{
	if (IsValid(LevelSequenceActor)&& IsValid(LevelSequenceActor->SequencePlayer))
	{
		LevelSequenceActor->SequencePlayer->SetPlayRate(rate);
	}	
}

void UGStoryManager::OnSkipEvent()
{
	//中断语音
	if (UGolbalBPFunctionLibrary::AudioManager() && IsValid(UGolbalBPFunctionLibrary::AudioManager()))
	{
		UGolbalBPFunctionLibrary::AudioManager()->StopVoice();
	}

	//播放镜头中事件
	const FSTORY_EVENT_DATA* StoryEventData = GetStoryEventData(CurrPlayId);

	if (StoryEventData)
	{
		if (StoryEventData->StoryEventList.Num() > 0)
		{

			TArray<FSTORY_EVENT_LIST> StoryEventList = StoryEventData->StoryEventList;
			StoryEventList.Sort([](const FSTORY_EVENT_LIST& A, const FSTORY_EVENT_LIST& B) {
				return A.Index < B.Index;
			});

			for (auto& data : StoryEventList)
			{
				if (data.Index >CurrOrderIndex)
				{
					NotifyServerEvent();
				}
			}

			PauseSequence();
			TWeakObjectPtr<UGStoryManager> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayDestroyCameraHandle,
				FTimerDelegate::CreateLambda([DelayThisPtr]() {
				if (DelayThisPtr.IsValid())
				{
					UGStoryManager* ThisPtr = DelayThisPtr.Get();
					ThisPtr->PlayRedrawViewports();
					ThisPtr->StopSequence();
				}
			}), 0.5f, false);
			return;
		}
	}
	StopSequence();
}

void UGStoryManager::GetPreCameraData(FCAMERA_SETTINGS_DATA& PreCameraSettings)
{
	SCOPE_CYCLE_COUNTER(STAT_GetPreCameraData);
	FCAMERA_DATA CameraData;
	const FSTORY_DATA* StoryData = GetStoryData(CurrPlayId);

	if (nullptr == StoryData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGStoryManager::GetPreCameraData: StoryData!"));
		return ;
	}
	int32 PlayerId = UGolbalBPFunctionLibrary::GetPlayerID();
	int32 Profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(PlayerId, "profession");
	int32 PlayId = Profession - 1;
	if (1 == StoryData->PreCameraSettings.Num())
	{
		PreCameraSettings = StoryData->PreCameraSettings[0];
	}
	else
	{		
		if ((PlayId >= 0) && (PlayId < StoryData->PreCameraSettings.Num()))
		{
			PreCameraSettings = StoryData->PreCameraSettings[PlayId];
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END


