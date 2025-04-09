// Fill out your copyright notice in the Description page of Project Settings.


#include "SpellBoxInterface.h"
#include "Actor/SpellBox/SpellBoxCharacter.h"
#include "Manager/ParticleManager.h"
#include "Manager/VisibleManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Kismet/KismetMathLibrary.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(USpellBoxInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(USpellBoxInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

USpellBoxInterface::USpellBoxInterface()
{
	BoxStatus = -1;
	CurEffectUID = -1;
}

USpellBoxInterface::~USpellBoxInterface()
{

}

void USpellBoxInterface::OnRep_minGossipDis()
{

}

void USpellBoxInterface::OnRep_maxGossipDis()
{

}

void USpellBoxInterface::OnRep_listenEvents()
{

}

bool USpellBoxInterface::HasListenEvent(int32 eventType)
{
	if (GetEntity() == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::HasListenEvent : GetEntity()!"));
		return false;
	}

	int64 _ListenEvents = GetEntity()->GetDefinedProperty(TEXT("listenEvents")).GetValue<int64>();
	int64 _EventType = int64(1) << int64(eventType);
	return (_ListenEvents & _EventType) == _EventType;
}

void USpellBoxInterface::CLIENT_RefreshBoxStatus_Implementation()
{
	AServerCharacter* Player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Player) || GetEntity() == nullptr || Player->GetSelfEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::CLIENT_RefreshBoxStatus_Implementation : Player||GetEntity()||Player->GetSelfEntity()!"));
		return;
	}

	KBEngine::FVariantArray Args;
	Args.Add(GetEntity()->ID());
	Player->GetSelfEntity()->CellCall(TEXT("requestRefreshBoxStatus"), Args);
}

void USpellBoxInterface::CLIENT_SetBoxStatus_Implementation(int32 boxStatus,const FString& spellBoxEffectID, float effectModelScale, const FString& slotName)
{
	if (!IsValid(GetActor()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::CLIENT_SetBoxStatus_Implementation : GetActor()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("SpellBox::CLIENT_SetBoxStatus [%i]~effectID [%s]"), boxStatus, *spellBoxEffectID);
	if (BoxStatus != boxStatus)
	{
		BoxStatus = boxStatus;
		
		if (IsValid(GetActor()))
		{
			UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(GetActor());///隐藏或显示模型：VisibleManager会根据BoxStatus设置可见性		
			ASpellBoxCharacter* SpellBoxActor = Cast<ASpellBoxCharacter>(GetActor());
			SpellBoxActor->OnSetBoxStatus(boxStatus);
		}

		UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;
		if (BoxStatus == 0)
		{
			///隐藏光效、设置为不可选
			ParticleManager->StopEffectByUID(CurEffectUID);

		}
		else if (BoxStatus == 1)
		{
			///隐藏光效、设置为不可选
			ParticleManager->StopEffectByUID(CurEffectUID);
		}
		else
		{
			///显示光效、设置为可选
			//显示光效
			Cast<AServerCharacter>(GetActor())->SetEffectDynamicData(slotName, effectModelScale,FVector(0.0f,0.0f,0.0f));
			//添加并获取到粒子
			CurEffectUID = ParticleManager->PlayParticle(spellBoxEffectID, 0.0f, GetActor(), GetActor());
		}
	}
}

void USpellBoxInterface::CLIENT_SpellBoxInterrupted_Implementation()
{
	if (IsValid(GetActor()))
	{
		ASpellBoxCharacter* SpellBoxActor = Cast<ASpellBoxCharacter>(GetActor());
		if (IsValid(SpellBoxActor))
		{
			SpellBoxActor->SpellBoxInteractiveInterrupted();
		}
	}
}

void USpellBoxInterface::OnDelayStopAction(float delayStop)
{
	ASpellBoxCharacter* SpellBoxActor = Cast<ASpellBoxCharacter>(GetActor());
	SpellBoxActor->FinshPlayAction(delayStop);
}

void USpellBoxInterface::CLIENT_OnHoldRadiusFog_Implementation(const FString& Albedo, const float& StarHoldRadius, const float& EndHoldRadius, const float& Extinction, const float& time)
{
	ASpellBoxCharacter* SpellBoxActor = Cast<ASpellBoxCharacter>(GetActor());
	TArray<FString> ColorList = UGolbalBPFunctionLibrary::SplitString(Albedo);
	FVector DissolveDirectionVector = FVector(FSTRING_TO_FLOAT(ColorList[0]), FSTRING_TO_FLOAT(ColorList[1]), FSTRING_TO_FLOAT(ColorList[2]));
	UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(SpellBoxActor->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
	UGolbalBPFunctionLibrary::CS3SetVectorParameterOnMaterials(DefaultStaticMeshCpt, "Albedo", DissolveDirectionVector);
	UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(DefaultStaticMeshCpt, "Extinction", Extinction);
	HoldRadiusTime = 0.0f;
	TWeakObjectPtr<USpellBoxInterface> DelayThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, HoldRadiusHandle, FTimerDelegate::CreateLambda(
		[SpellBoxActor, DelayThisPtr, time, StarHoldRadius, EndHoldRadius]()
	{
			if (!DelayThisPtr.IsValid())
			{
				CS3_Warning(TEXT("AppCmpt.Error::CreateModel:LoadAssetPathCallBack *this is error!"));
				return;
			}
			USpellBoxInterface* ThisPtr = DelayThisPtr.Get();
			UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(SpellBoxActor->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
			
			if (ThisPtr->HoldRadiusTime < 1)
			{
				ThisPtr->HoldRadiusTime += 0.01f / time;
				float CurDegree = UKismetMathLibrary::Ease(StarHoldRadius, EndHoldRadius, ThisPtr->HoldRadiusTime, EEasingFunc::Linear);
				UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(DefaultStaticMeshCpt, TEXT("HoleRadius"), CurDegree);
			}
			else
			{
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->HoldRadiusHandle);
			}
	}), 0.01f, true);
}

void USpellBoxInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_RefreshBoxStatus");
	ArrBlueFunc.Add("CLIENT_SetBoxStatus");
	ArrBlueFunc.Add("CLIENT_SpellBoxInterrupted");
	ArrBlueFunc.Add("CLIENT_OnHoldRadiusFog");
	Supper::InitBlueCB();
}
CONTROL_COMPILE_OPTIMIZE_END
