// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleStoryInterface.h"
#include "Util/CS3Debug.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/StoryManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleStoryInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(StartBuffPlayStory, &URoleStoryInterface::StartBuffPlayStory,const FString&, const int32&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(StopBuffStory, &URoleStoryInterface::StopBuffStory, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(StartPlayStory, &URoleStoryInterface::StartPlayStory, const FString&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(StopStory, &URoleStoryInterface::StopStory)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleStoryInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleStoryInterface::URoleStoryInterface()
{
}

URoleStoryInterface::~URoleStoryInterface()
{
}

void URoleStoryInterface::onNotifyDoStoryEvent(FString CurrPlayId, int32 CurrOrderIndex)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStoryInterface::onNotifyDoStoryEvent : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(CurrPlayId);
	Args.Add(CurrOrderIndex);
	entity->CellCall(TEXT("onNotifyDoStoryEvent"), Args);
}

void URoleStoryInterface::RPC_onStopPlayStory(FString CurrPlayId)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStoryInterface::RPC_onStopPlayStory : entity!"));
		return;
	};
	int32 BuffID = 0;

	if (StoryBuffDatas.Num() > 0)
	{
		int32 Index = StoryBuffDatas.Num() - 1;
		BuffID = StoryBuffDatas[Index].BuffUID;
		StoryBuffDatas.RemoveAt(Index);
	}
	KBEngine::FVariantArray Args;
	if (BuffID == 0)
	{
		Args.Add(CurrPlayId);
	}
	else
	{
		Args.Add(BuffID);
		Args.Add(CurrPlayId);
	}

	entity->CellCall(TEXT("onStopPlayStory"), Args);
}

void URoleStoryInterface::onNotifyAddEffectList(FString SequenceId, TArray<int32> EffectList)
{
	KBEngine::FVariantArray Args;
	Args.Add(SequenceId);
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(EffectList));
	CellCall(TEXT("onNotifyAddEffectList"), Args);
}

void URoleStoryInterface::onNotifyRemoveEffectList(FString SequenceId)
{
	KBEngine::FVariantArray Args;
	Args.Add(SequenceId);
	CellCall(TEXT("onNotifyRemoveEffectList"), Args);
}

void URoleStoryInterface::StartBuffPlayStory(const FString& SequenceId, const int32& LoopNum, const int32& BuffUID)
{
	APlayerCharacter* Character = Cast<APlayerCharacter>(GetActor());
	if (IsValid(Character) && Character->ActorIsPlayer() && IsValid(UGolbalBPFunctionLibrary::GStoryManager()))
	{
		if (!UGolbalBPFunctionLibrary::GStoryManager()->IsPlaying() && StoryBuffDatas.Num() > 0)
		{
			StoryBuffDatas.RemoveAt(StoryBuffDatas.Num() - 1);
		}
		FStoryBuffData NewData(BuffUID, STORYSTATE::STARTPLAY, SequenceId, LoopNum);
		StoryBuffDatas.Add(NewData);

		Character->StartPlayStory(SequenceId, LoopNum);
	}
}

void URoleStoryInterface::StopBuffStory(const int32& BuffUID)
{
	if (IsValid(UGolbalBPFunctionLibrary::GStoryManager()))
	{
		if (BuffUID !=0 )
		{
			for (int32 i=0;i< StoryBuffDatas.Num();i++)
			{
				if (StoryBuffDatas[i].BuffUID == BuffUID)
				{
					StoryBuffDatas[i].StoryState = STORYSTATE::SERVERSTOP;
					UGolbalBPFunctionLibrary::GStoryManager()->StopSequence();
					break;
				}
			}
		}
		else
		{
			UGolbalBPFunctionLibrary::GStoryManager()->StopSequence();
		}		
	}	
}

void URoleStoryInterface::StartPlayStory(const FString & SequenceId, const int32& LoopNum)
{
	APlayerCharacter* Character = Cast<APlayerCharacter>(GetActor());
	if (IsValid(Character) && Character->ActorIsPlayer() && IsValid(UGolbalBPFunctionLibrary::GStoryManager()))
	{
		FStoryBuffData NewData(0, STORYSTATE::STARTPLAY, SequenceId, LoopNum);
		StoryBuffDatas.Add(NewData);
		Character->StartPlayStory(SequenceId, LoopNum);
	}
}

void URoleStoryInterface::StopStory()
{
	UGolbalBPFunctionLibrary::GStoryManager()->StopSequence();
}
