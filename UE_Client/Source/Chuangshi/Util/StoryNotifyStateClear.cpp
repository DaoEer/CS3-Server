// Fill out your copyright notice in the Description page of Project Settings.


#include "StoryNotifyStateClear.h"
#include "Actor/Player/StoryCharacter.h"
#include "Util/CS3Debug.h"



void UStoryNotifyStateClear::NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration)
{
	if (AStoryCharacter* StoryCharacter = Cast<AStoryCharacter>(MeshComp->GetOwner()))
	{
		if (Animation != StoryCharacter->OldAnim)
		{
			ClearNotifyState(MeshComp, StoryCharacter->OldAnim);

			StoryCharacter->OldAnim = Animation;
		}
		
	}

	Received_NotifyBegin(MeshComp, Animation, TotalDuration);
}

void UStoryNotifyStateClear::ClearNotifyState(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation)
{
	if (!Animation)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UStoryNotifyStateClear::ClearNotifyState: Animation!"));
		return;
	}

	auto NotifyArr = Animation->Notifies;

	for (auto NotifyFor : NotifyArr)
	{
		if (NotifyFor.NotifyStateClass)
		{
			NotifyFor.NotifyStateClass->NotifyEnd(MeshComp, Animation);
		}
	}
}
