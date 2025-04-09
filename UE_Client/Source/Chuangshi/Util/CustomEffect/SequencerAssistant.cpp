#include "SequencerAssistant.h"
#include "../CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

UStopDelegateStorageComponent::UStopDelegateStorageComponent()
{
	ParticleNeedStop = true;
}

UStopDelegateStorageComponent* UStopDelegateStorageComponent::CreateAndAttachToComponent(USceneComponent* Input)
{
	auto CurPtr = Get(Input);
	if (CurPtr != nullptr)
		return CurPtr;
	auto Ptr = NewObject<UStopDelegateStorageComponent>(Input, TEXT("StorageComponent"), RF_NoFlags, nullptr, false, nullptr);
	FAttachmentTransformRules Rules{ EAttachmentRule::KeepRelative , false };
	Ptr->AttachToComponent(Input, Rules);
	return Ptr;
}

UStopDelegateStorageComponent* UStopDelegateStorageComponent::Get(USceneComponent* Input)
{
	auto& Attached = Input->GetAttachChildren();
	for (auto Ite : Attached)
	{
		auto Ptr = Cast<UStopDelegateStorageComponent>(Ite);
		if (IsValid(Ptr))
			return Ptr;
	}
	return nullptr;
}

void UStopDelegateStorageComponent::StopAll()
{
	for (auto& ite : StateStorageMapping)
		ite.Value.ExecuteIfBound();
	StateStorageMapping.Empty();
}


CONTROL_COMPILE_OPTIMIZE_END