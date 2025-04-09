// Fill out your copyright notice in the Description page of Project Settings.


#include "GameObjectInterface.h"

#include "Kismet/KismetMathLibrary.h"
#include "kismet/KismetMaterialLibrary.h"

#include "GameData/GameDefault.h"
#include "GameData/Skill/BuffTableData.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Actor/ServerCharacter.h"
#include "Actor/SpellBox/SpellBoxCharacter.h"
#include "CS3Base/GameObject.h"
#include "Manager/AudioManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/ParticleManager.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/ResourceManager.h"
#include "Manager/CfgManager.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Manager/AudioManager.h"
#include "Manager/CfgManager.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Components/AudioComponent.h"
#include "GameFramework/PawnMovementComponent.h"
#include "GameData/CharacterData.h"
#include "GameData/EnumCsvDefine.h"
#include "CoreDelegates.h"
#include "TimerManager.h"

CONTROL_COMPILE_OPTIMIZE_START
	
CS3_BEGIN_INTERFACE_METHOD_MAP(UGameObjectInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UGameObjectInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(prefixName, &UGameObjectInterface::Set_prefixName, FString)
CS3_END_INTERFACE_PROPERTY_MAP()
	

UGameObjectInterface::UGameObjectInterface()
{
	extraModelNumberList.Empty();
}

UGameObjectInterface::~UGameObjectInterface()
{

}


void UGameObjectInterface::CLIENT_ShowInvisible_Implementation()
{
	if (IsValid(GetActor()))
	{
		Cast<AServerCharacter>(GetActor())->ShowInvisible();
	}
}

void UGameObjectInterface::CLIENT_HideInvisible_Implementation()
{
	if (IsValid(GetActor()))
	{
		Cast<AServerCharacter>(GetActor())->HideInvisible();
	}
}


void UGameObjectInterface::CLIENT_OnPlayParticles_Implementation(const int32& TargetID, const FString& EffectID, const FString& SoltName, float EffectScale,FVector Pos)
{
	this->OnPlayParticles_P(TargetID,EffectID,SoltName,EffectScale,Pos);
}

void UGameObjectInterface::OnPlayParticles_P(const int32&  TargetID, const FString& EffectID, const FString& SoltName, float EffectScale, FVector Pos)
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());

	if (IsValid(ServerActor))
	{
		ServerActor->SetEffectDynamicData(SoltName, EffectScale, Pos);
		AServerCharacter* BeAtkActor = nullptr;
		KBEngine::Entity* BeAtkEntity = UGolbalBPFunctionLibrary::FindEntity(TargetID);
		if (nullptr != BeAtkEntity)
		{
			BeAtkActor = Cast<AServerCharacter>(((CS3Entity *)BeAtkEntity)->Actor());
			CurrentUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, GetActor(), BeAtkActor, FEffectCreate::CreateLambda([Pos](int32 UID)
			{
				AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
				if (Effect)
				{
					Effect->AddActorWorldOffset(Pos);
				}
			}));
		}
	}
}


void UGameObjectInterface::CLIENT_OnStopParticles_Implementation()
{
	if (!IsValid(GetActor()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEntitySpaceEventInterface::OnStopParticles_Implementation : GetEntity()!"));
		return;
	}

	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(CurrentUID);
}

void UGameObjectInterface::CLIENT_ShowTopCountDown_Implementation(float LifeTime, float TimerInterval)
{
	if (IsValid(GetActor()))
	{
		ASpellBoxCharacter* SpellBoxCharacter = Cast<ASpellBoxCharacter>(GetActor());
		if (SpellBoxCharacter && this->GetEntity())
		{
			SpellBoxCharacter->OnShowTopCountDownBP(LifeTime, TimerInterval);
		}
	}
}

void UGameObjectInterface::CLIENT_HideTopCountDown_Implementation()
{
	if (IsValid(GetActor()))
	{
		ASpellBoxCharacter* SpellBoxCharacter = Cast<ASpellBoxCharacter>(GetActor());
		if (SpellBoxCharacter && this->GetEntity())
		{
			SpellBoxCharacter->OnHideTopCountDownBP();
		}
	}
}

void UGameObjectInterface::CLIENT_PlayOneByOneAction(const int32 &ContinuousId, TArray<FName>& ActionIds, TArray<FString>& ActionStartTimes)
{
	AServerCharacter* Character = Cast<AServerCharacter>(GetActor());
	if (IsValid(Character))
	{
		TArray<float> TemActionStartTimes;
		for (auto obj : ActionStartTimes)
		{
			TemActionStartTimes.Add(FSTRING_TO_FLOAT(obj));
		}
		Character->PlayContinuousActions(ContinuousId, ActionIds, TemActionStartTimes);
	}
}

void UGameObjectInterface::UpdateRelation()
{
	if (IsValid(GetActor()))
	{
		Cast<AServerCharacter>(GetActor())->UpdateRelation();
	}
}

void UGameObjectInterface::ExecuteTweenModelScale()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEntitySpaceEventInterface::ExecuteTweenModelScale : GetEntity()!"));
		return;
	}
	if (!IsValid(GetActor()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEntitySpaceEventInterface::ExecuteTweenModelScale : GetActor()!"));
		return;
	}
	//暂时不需要坐骑模型从小变大
	SetModelMeshScale(1.f);
	//SetModelMeshScale(0.4f);
	UpdateActorPosition();
	bScaleTweenProcess = true;
	float ToModelScaleValue = GetEntity()->GetDefinedProperty(TEXT("modelScale")).GetValue<float>();
	TWeakObjectPtr<UGameObjectInterface> DelayThisPtr(this);

	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, PetScaleHandle,
			FTimerDelegate::CreateLambda([DelayThisPtr, ToModelScaleValue]()
		{
			if (DelayThisPtr.IsValid())
			{
				UGameObjectInterface* ThisPtr = DelayThisPtr.Get();
				AServerCharacter* Actor_Server = Cast<AServerCharacter>(ThisPtr->GetActor());
				float AddToModelSacelValue = Actor_Server->GetMesh()->RelativeScale3D.Z + 0.007f;
				//CS3_Display(CS3DebugType::CL_Undefined, TEXT("StartScaleRidePet=====%f,   %f,   Z=%f"), AddToModelSacelValue, ToModelScaleValue, Actor_Server->GetMesh()->RelativeScale3D.Z);
				if (AddToModelSacelValue >= ToModelScaleValue)
				{
					ThisPtr->bScaleTweenProcess = false;
					if (IsValid(UUECS3GameInstance::Instance))
					{
						UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->PetScaleHandle);
					}
				}
				else
				{
					ThisPtr->SetModelMeshScale(AddToModelSacelValue);
					ThisPtr->UpdateActorPosition();
				}
			}
		}), 0.01f, true);
	}
}

void UGameObjectInterface::CLIENT_OnPlay3DSound_Implementation(const FString& SoundID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager) && IsValid(GetActor()))
	{
		AudioComponent = UGolbalBPFunctionLibrary::AudioManager()->AsyncPlay3DSound(GetActor(), SoundID);
	}
}

void UGameObjectInterface::CLIENT_OnStop3DSound_Implementation()
{
	//停止播放
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager) && IsValid(AudioComponent))
	{
		UUECS3GameInstance::Instance->AudioManager->Stop3DSound(AudioComponent);
		AudioComponent = nullptr;
	}
}

void UGameObjectInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnPlayAction");
	ArrBlueFunc.Add("CLIENT_StopAction");
	ArrBlueFunc.Add("CLIENT_StopFrontAction");
	ArrBlueFunc.Add("CLIENT_ShowInvisible");
	ArrBlueFunc.Add("CLIENT_HideInvisible");
	ArrBlueFunc.Add("CLIENT_OnPlayParticles");
	ArrBlueFunc.Add("UpdateRelation");
	ArrBlueFunc.Add("CLIENT_ShowTopCountDown");
	ArrBlueFunc.Add("CLIENT_HideTopCountDown ");
	ArrBlueFunc.Add("CLIENT_PlayOneByOneAction");
	ArrBlueFunc.Add("CLIENT_ChangeToDstModelScale");
	ArrBlueFunc.Add("CLIENT_ChangeToNormalModelScale");
	ArrBlueFunc.Add("CLIENT_CastToStone");
	ArrBlueFunc.Add("CLIENT_CastToNormal");
	ArrBlueFunc.Add("CLIENT_BindDisplayObject");
	ArrBlueFunc.Add("CLIENT_UnbindDisplayObject");
	ArrBlueFunc.Add("CLIENT_ChangeShowPosture");
	ArrBlueFunc.Add("CLIENT_ChangeShowAnimAndActionPosture");
	ArrBlueFunc.Add("CLIENT_OnStopParticles");
	ArrBlueFunc.Add("CLIENT_OnPlay3DSound");
	ArrBlueFunc.Add("CLIENT_OnStop3DSound");
	Supper::InitBlueCB();
}

void UGameObjectInterface::Set_prefixName(const FString& newVal, const FString& oldVal)
{
	AServerCharacter* Owner = Cast<AServerCharacter>(GetActor());
	if (IsValid(Owner))
	{
		Owner->onPrefixNameChange(newVal);
	}

}

void UGameObjectInterface::onEnterWorld()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEntitySpaceEventInterface::onEnterWorld : GetEntity()!"));
		return;
	}
	Supper::onEnterWorld();
}

void UGameObjectInterface::onLeaveWorld()
{
	Supper::onLeaveWorld();
}

void UGameObjectInterface::OnRep_modelNumber()
{
	AActor* actor = GetActor();
	if (IsValid(actor) && GetEntity() != nullptr)
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(actor);
		if (IsValid(ServerCharacter) && ServerCharacter->IsInitialized())
		{
			FString newValue = GetEntity()->GetDefinedProperty(TEXT("modelNumber")).GetValue<FString>();
			if (newValue == new_modelNumber)
			{
				return;
			}
			ServerCharacter->CheckCreateDynamicPartCpt(newValue);
			SetModelScale(1.0f);//还原到标准缩放
			new_modelNumber = newValue;
			ServerCharacter->CreateAppearance();
			UpdateActorPosition();
		}
	}
}
void UGameObjectInterface::OnRep_extraModelNumber()
{
	AActor* actor = GetActor();
	if (!actor || !GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGameObjectInterface::OnRep_extraModelNumber : actor || GetEntity()!"));
		return;
	}
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(actor);
	if (!ServerCharacter || !ServerCharacter->IsInitialized())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGameObjectInterface::OnRep_extraModelNumber : MyCharacter || MyCharacter->IsInitialized()!"));
		return;
	}
	if (old_extraModelNumber.Equals(extraModelNumber))return;
	FString newValue = GetEntity()->GetDefinedProperty(TEXT("extraModelNumber")).GetValue<FString>();
	extraModelNumberList.Add(newValue);

	StartChangeModel();				//此处不需要考虑模型是不是正在创建，外观组件会考虑CST-13694
}

void UGameObjectInterface::OnRep_modelScale()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity !=nullptr)
	{
		if (old_modelNumber == new_modelNumber && bUpdateModelScale)
		{
			float newValue = entity->GetDefinedProperty(TEXT("modelScale")).GetValue<float>();
			SetModelScale(newValue);

			//(CST-8737)处理模型加载完毕后，在空中则不要设置位置，会导致直接将玩家拉到地面而没有下落过程
			UpdateActorPosition();
		}
	}
}

void UGameObjectInterface::OnRep_armyModelList()
{
	if (GetEntity() == nullptr || !IsValid(GetActor()))
	{
		return;
	}
	KBEngine::FVariantArray armyModelList = GetEntity()->GetDefinedProperty(TEXT("armyModelList")).GetValue<KBEngine::FVariantArray>();

	AServerCharacter* Character = Cast<AServerCharacter>(GetActor());
	if (IsValid(Character))
	{
		if (armyModelList.Num() > 0)
		{
			Character->OrganizeArmy((TArray<FString>)armyModelList);
		}
		else
		{
			Character->DissolutionArmy();
		}
	}

}

void UGameObjectInterface::OnRep_SyncPosClient()
{
}

bool UGameObjectInterface::isEntityFlag(ENTITY_TYPE entityFlag)
{
	if (GetEntity() != nullptr)
	{
		uint8 selfFlag = GetEntity()->GetDefinedProperty(TEXT("entityFlag")).GetValue<uint8>();
		if (selfFlag == uint8(entityFlag))
		{
			return true;
		}
	}	
	return false;
}

ENTITY_TYPE UGameObjectInterface::getEntityFlag()
{
	if (GetEntity() != nullptr)
	{
		uint8 selfFlag = GetEntity()->GetDefinedProperty(TEXT("entityFlag")).GetValue<uint8>();
		return ENTITY_TYPE(selfFlag);
	}
	return ENTITY_TYPE(0);
}

bool UGameObjectInterface::IsEntityFlagExt(ENTITY_TYPE_EXT entityFlagExt)
{
	if (GetEntity() != nullptr)
	{
		uint8 selfFlag = GetEntity()->GetDefinedProperty(TEXT("entityFlagExt")).GetValue<uint8>();
		if (selfFlag == uint8(entityFlagExt))
		{
			return true;
		}
	}
	return false;
}

ENTITY_TYPE_EXT UGameObjectInterface::GetEntityFlagExt()
{
	if (GetEntity() != nullptr)
	{
		uint8 selfFlag = GetEntity()->GetDefinedProperty(TEXT("entityFlagExt")).GetValue<uint8>();
		return ENTITY_TYPE_EXT(selfFlag);
	}
	return ENTITY_TYPE_EXT(0);
}


void UGameObjectInterface::CLIENT_OnPlayAction_Implementation(const FString& ActionId, float delayStop)
{
	AServerCharacter* Actor = Cast<AServerCharacter>(GetActor());
	if (!IsValid(Actor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEntitySpaceEventInterface::OnPlayAction_Implementation : Actor!"));
		return;
	}
	Actor->PlayAction(FSTRING_TO_FNAME(ActionId));

	//Spellbox石头延迟暂停
	OnDelayStopAction(delayStop);
}

void UGameObjectInterface::CLIENT_StopAction_Implementation()
{
	AServerCharacter* character = Cast<AServerCharacter>(GetActor());
	if (IsValid(character))
	{
		character->StopAction();
	}
}


void UGameObjectInterface::CLIENT_StopFrontAction_Implementation()
{
	AServerCharacter* character = Cast<AServerCharacter>(GetActor());
	if (IsValid(character))
	{
		character->StopFrontAction();
	}
}

void UGameObjectInterface::SetModelScale(const float &newValue)
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if(IsValid(Actor_Server))
	{
		FVector Scale3D = Actor_Server->GetActorScale3D();
		if (FMath::IsNearlyEqual(Scale3D.Z, newValue))
		{
			return;
		}
		//FVector ActorLocation = Actor_Server->GetActorLocation();
		//float LastScaleHeight = Actor_Server->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
		Actor_Server->SetActorScale3D(FVector(newValue, newValue, newValue));

		//头发缩放后会揉成一团，需要对头发作以下设置
		UMeshComponent *MeshPartCom = Actor_Server->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_HAIRS);
		if (MeshPartCom)
		{
			MeshPartCom->RecreatePhysicsState();
		}
		//float LastScaleHeight_New = Actor_Server->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
		//float DisHight = LastScaleHeight_New - LastScaleHeight;
		//ActorLocation.Z += DisHight;
		
		/*
		这部分改收统一更新位置,因不光缩放时、还有胶囊体变化时等,以免重复设置位置:UpdateActorPosition()
		GameObject* entity = (GameObject*)GetEntity();
		if (entity != nullptr )
		{
			FVector Pos ;
			//这里不采用entity->Position()的原因是此时服务器的坐标可能已经发生改变，而高度是不靠谱的，所以不用
			Pos = entity->GetOnGroundPos(false, Actor_Server->GetActorLocation());
			//Pos = Actor_Server->OnGroundPos(entity->Position());
			//CS3_Warning(TEXT("------------------2-----UGameObjectInterface::SetModelScale[id:%d--------GetActorLocation:%f,POS:%f,position: %f]"), GetEntity()->ID(), Actor_Server->GetActorLocation().Z,Pos.Z, entity->Position().Z);
			Actor_Server->SetActorLocation(Pos);
		}*/
		Actor_Server->RemoveOnActorCreaterFinishBind();
		Actor_Server->OnBpSetModelScale(newValue);
	}
}


void UGameObjectInterface::SetModelMeshScale(const float &newValue)
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if (IsValid(Actor_Server))
	{
		FVector Scale3D = Actor_Server->GetMesh()->RelativeScale3D;
		if (FMath::IsNearlyEqual(Scale3D.Z, newValue))
		{
			return;
		}
		Actor_Server->GetMesh()->SetRelativeScale3D(FVector(newValue, newValue, newValue));
		Actor_Server->RemoveOnActorCreaterFinishBind();
		Actor_Server->OnBpSetModelScale(newValue);
	}
}

bool UGameObjectInterface::IsInFlags(ENTITY_FLAG EntityFlag, int64 Flags)
{
	int64 Flag = int64(1) << int64(EntityFlag);
	return (Flags & Flag) == Flag;
}

void UGameObjectInterface::CLIENT_ChangeToDstModelScale_Implementation(const float& ChangeTime, const float& ChangeModelScaleX, const float& ChangeModelScaleY, const float& ChangeModelScaleZ, const float& NormalModelScale)
{

	DtsScaleVector.X = ChangeModelScaleX * NormalModelScale;
	DtsScaleVector.Y = ChangeModelScaleY * NormalModelScale;
	DtsScaleVector.Z = ChangeModelScaleZ * NormalModelScale;

	CurScaleVector.X = NormalModelScale;
	CurScaleVector.Y = NormalModelScale;
	CurScaleVector.Z = NormalModelScale;
	if (FMath::IsNearlyZero(ChangeTime))
	{
		SetActorScale(DtsScaleVector);
	}
	else
	{
		TimeValue = 0.0f;
		ChangeSpeed = ChangeTime;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(ChangeScaleHandle, this, &UGameObjectInterface::TickChangeToDstModelScale, ChangeScaleTick, true);
	}
}
void UGameObjectInterface::TickChangeToDstModelScale()
{
	if (CurScaleVector == DtsScaleVector)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ChangeScaleHandle);
		return;
	}
	TimeValue += ChangeScaleTick / ChangeSpeed;
	if (TimeValue<1)
	{
		SetActorScale(UKismetMathLibrary::VEase(CurScaleVector, DtsScaleVector, TimeValue, EEasingFunc::Linear));
	}
	else
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ChangeScaleHandle);
	}
}

void UGameObjectInterface::CLIENT_ChangeToNormalModelScale_Implementation(const float& NormalTime, const float& NormalModelScale)
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if (!Actor_Server)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGameObjectInterface::ChangeToNormalModelScale_Implementation : Actor_Server!"));
		return;
	}
	CurScaleVector = Actor_Server->GetActorScale3D();
	DtsScaleVector.X = NormalModelScale;
	DtsScaleVector.Y = NormalModelScale;
	DtsScaleVector.Z = NormalModelScale;

	if (FMath::IsNearlyZero(NormalTime))
	{
		SetActorScale(DtsScaleVector);
	}
	else
	{
		TimeValue = 0.0f;	
		ChangeSpeed = NormalTime;
		TWeakObjectPtr<UGameObjectInterface> ThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, ChangeScaleHandle, FTimerDelegate::CreateLambda([ThisPtr]()
		{
			if (ThisPtr.IsValid())
			{
				ThisPtr.Get()->TickChangeToNormalModelScale();
			}
		}), ChangeScaleTick, true);
	}
}
void UGameObjectInterface::TickChangeToNormalModelScale()
{
	if (CurScaleVector == DtsScaleVector)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ChangeScaleHandle);
		//bUpdateModelScale = true; /*CST-3928*/
		return;
	}
	TimeValue += ChangeScaleTick / ChangeSpeed;
	if (TimeValue < 1)
	{
		SetActorScale(UKismetMathLibrary::VEase(CurScaleVector, DtsScaleVector, TimeValue, EEasingFunc::Linear));
	}
	else
	{
		KBEngine::Entity* entity = GetEntity();
		if (entity)
		{
			float newValue = entity->GetDefinedProperty(TEXT("modelScale")).GetValue<float>();
			if (!FMath::IsNearlyEqual(newValue, DtsScaleVector.GetMin()))
			{
				SetActorScale(FVector(newValue, newValue, newValue));
			}
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ChangeScaleHandle);
		}
	}
}

void UGameObjectInterface::SetActorScale(FVector ModelScale)
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if (!Actor_Server)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGameObjectInterface::SetActorScale : Actor_Server!"));
		return;
	}
	Actor_Server->SetActorScale3D(ModelScale);
	
	//头发缩放后会揉成一团，需要对头发作以下设置
	UMeshComponent *MeshPartCom = Actor_Server->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_HAIRS);
	if (MeshPartCom)
	{
		MeshPartCom->RecreatePhysicsState();
	}

	UpdateActorPosition();
}

void UGameObjectInterface::OnsetActorScale()
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if (!Actor_Server)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGameObjectInterface::OnsetActorScale : Actor_Server!"));
		return;
	}
	GetActor()->SetActorLocation(Actor_Server->FloorTrace(Actor_Server->GetActorLocation()));
}


void UGameObjectInterface::CLIENT_CastToStone_Implementation(float StoneSpeed, int32 effectType)
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if (!IsValid(Actor_Server)) return;
	TWeakObjectPtr<AServerCharacter> ActorPtr(Actor_Server);
	TWeakObjectPtr<UGameObjectInterface> ThisPtr(this);
	if (Actor_Server->bIsChangeAppearanceling || (!Actor_Server->GetApperanceLoadingOver()) || !IsValid(Actor_Server->GetMesh()) || !IsValid(Actor_Server->GetMesh()->SkeletalMesh))
	{
		if (StoneDelegateHandle.IsValid())
		{
			Actor_Server->OnModelChangeAppearanceOverDelegate.Remove(StoneDelegateHandle);
			StoneDelegateHandle.Reset();
		}
		StoneDelegateHandle = Actor_Server->OnModelChangeAppearanceOverDelegate.AddLambda([
			ThisPtr, StoneSpeed, effectType]()
		{
			UGameObjectInterface* ThisInterface = ThisPtr.Get();
			if (IsValid(ThisInterface))
			{
				AServerCharacter* ServerActor = Cast<AServerCharacter>(ThisInterface->GetActor());
				if (IsValid(ServerActor) && IsValid(ServerActor->GetMesh()) && IsValid(ServerActor->GetMesh()->SkeletalMesh))
				{
					ThisInterface->CastToStone(StoneSpeed, effectType);
					ServerActor->OnModelChangeAppearanceOverDelegate.Remove(ThisInterface->StoneDelegateHandle);
				}
			}
		});
		return;
	}
	CastToStone(StoneSpeed, effectType);
}

void UGameObjectInterface::DelayCastToStone(float StoneSpeed, int32 effectType)
{
	//FCoreDelegates::OnBeginFrame.AddUObject(this, &UGameObjectInterface::CastToStone, StoneSpeed, effectType);
	if (!IsValid(UUECS3GameInstance::Instance)) return;
	UCustomTimerManager* TimerManager = UUECS3GameInstance::Instance->CustomTimerManager;
	if (IsValid(TimerManager))
	{
		FTimerHandle Handle;
		FTimerDelegate Delegate = FTimerDelegate::CreateUObject(this, &UGameObjectInterface::CastToStone, StoneSpeed, effectType);
		TimerManager->SetTimer(this, Handle, Delegate, UUECS3GameInstance::Instance->GetWorld()->GetDeltaSeconds(), false);
	}
	else
	{
		CastToStone(StoneSpeed, effectType);
	}
}

void UGameObjectInterface::CastToStone(float StoneSpeed, int32 effectType)
{
	const UConfigTable* Table = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BUFF_CLIENT_EFFECT);
	const FBUFF_CLIENT_EFFECT_DATA* Data = Table->GetRow<FBUFF_CLIENT_EFFECT_DATA>(INT_TO_FSTRING(effectType));
	if (!Data)
	{
		return;
	}
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if (!IsValid(Actor_Server)) return;
	TWeakObjectPtr<AServerCharacter> ActorPtr(Actor_Server);
	TWeakObjectPtr<UGameObjectInterface> ThisPtr(this);

	// 设置混合的最大值
	BlendMaxValue = Data->StonePetrifiedAlpha;

	TArray<FStringAssetReference> LoadList;
	LoadList.Add(Data->StoneDetailNormal.ToSoftObjectPath());
	LoadList.Add(Data->StoneTexture_D.ToSoftObjectPath());
	LoadList.Add(Data->StoneTexture_N.ToSoftObjectPath());

	// 加载资源
	UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, LoadList,
		FStreamableDelegate::CreateLambda([StoneSpeed, effectType, ActorPtr, Data, ThisPtr]()
	{
		if (!ActorPtr.IsValid() || !ThisPtr.IsValid())
		{
			return;
		}
		UGameObjectInterface* ThisInterface = ThisPtr.Get();
		AServerCharacter* ServerActor = ActorPtr.Get();
		if (!IsValid(ServerActor) || !IsValid(ThisInterface))
		{
			return;
		}
		TArray<UMaterialInterface*> MaterialsList = ServerActor->GetMesh()->GetMaterials();
		for (int32 i = 0; i < MaterialsList.Num(); i++)
		{
			// 替换效果材质
			UMaterialInstanceDynamic* DynamicMaterial = Cast<UMaterialInstanceDynamic>(MaterialsList[i]);
			if (DynamicMaterial)
			{
				DynamicMaterial->SetTextureParameterValue("StoneDetailNormal", Data->StoneDetailNormal.Get());
				DynamicMaterial->SetTextureParameterValue("StoneTexture_D", Data->StoneTexture_D.Get());
				DynamicMaterial->SetTextureParameterValue("StoneTexture_N", Data->StoneTexture_N.Get());
				DynamicMaterial->SetScalarParameterValue("StoneNormalIntensity", Data->StoneNormalIntensity);
				DynamicMaterial->SetScalarParameterValue("StoneRoughnessB", Data->StoneRoughnessB);
				DynamicMaterial->SetScalarParameterValue("StoneRoughnessH", Data->StoneRoughnessH);
				DynamicMaterial->SetScalarParameterValue("StoneSpecular", Data->StoneSpecular);
			}
			else
			{
				// 没有动态材质的时候，创建动态材质
				DynamicMaterial = UKismetMaterialLibrary::CreateDynamicMaterialInstance(ServerActor->GetWorld(), MaterialsList[i]);
				DynamicMaterial->SetTextureParameterValue("StoneDetailNormal", Data->StoneDetailNormal.Get());
				DynamicMaterial->SetTextureParameterValue("StoneTexture_D", Data->StoneTexture_D.Get());
				DynamicMaterial->SetTextureParameterValue("StoneTexture_N", Data->StoneTexture_N.Get());
				DynamicMaterial->SetScalarParameterValue("StoneNormalIntensity", Data->StoneNormalIntensity);
				DynamicMaterial->SetScalarParameterValue("StoneRoughnessB", Data->StoneRoughnessB);
				DynamicMaterial->SetScalarParameterValue("StoneRoughnessH", Data->StoneRoughnessH);
				DynamicMaterial->SetScalarParameterValue("StoneSpecular", Data->StoneSpecular);
				ServerActor->GetMesh()->SetMaterial(i, DynamicMaterial);
			}
		}

		// 开始效果，并设置状态
		ThisInterface->EffectType = effectType;
		if (FMath::IsNearlyZero(StoneSpeed))
		{
			ThisInterface->BlendValue = Data->StonePetrifiedAlpha;
			ThisInterface->SetActorStone(ThisInterface->BlendValue);
		}
		else
		{
			ThisInterface->BlendSpeed = 1.0 / StoneSpeed;
			ThisInterface->BlendValue = 0.0;
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(ThisInterface->StoneHandle, ThisInterface, &UGameObjectInterface::TickCastToStone, ThisInterface->StoneTick, true);
		}
		// 开始效果的回调
		ThisInterface->OnCastActorStone(true);

	}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_EFFECT);
}

void UGameObjectInterface::TickCastToStone()
{
	if (BlendValue < BlendMaxValue)
	{
		BlendValue += BlendSpeed *StoneTick;
		BlendValue = BlendValue > BlendMaxValue ? BlendMaxValue : BlendValue;
		SetActorStone(BlendValue);		
	}
	else 
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(StoneHandle);
	}
}


void UGameObjectInterface::CLIENT_CastToNormal_Implementation(const float& NormalSpeed, const int32& effectType)
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if (!IsValid(Actor_Server)) return;
	if (Actor_Server->bIsChangeAppearanceling || (!Actor_Server->GetApperanceLoadingOver()) || !IsValid(Actor_Server->GetMesh()) || !IsValid(Actor_Server->GetMesh()->SkeletalMesh))
	{
		Actor_Server->OnModelChangeAppearanceOverDelegate.Remove(StoneDelegateHandle);
		return;
	}
	if (FMath::IsNearlyZero(NormalSpeed))
	{
		BlendValue = 0.0;
		SetActorStone(BlendValue);
	}
	else
	{
		BlendSpeed = 1.0 / NormalSpeed;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(StoneHandle, this, &UGameObjectInterface::TicCastToNormal, StoneTick, true);
	}
}


void UGameObjectInterface::TicCastToNormal()
{
	if (BlendValue > 0.0)
	{
		BlendValue -= BlendSpeed *StoneTick;
		BlendValue = BlendValue < 0.0f ? 0.0f : BlendValue;
		SetActorStone(BlendValue);
	}
	else 
	{
		// 结束效果的回调
		OnCastActorStone(false);
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(StoneHandle);
	}
}

void UGameObjectInterface::SetActorStone(float Value)
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());

	if (Actor_Server && Actor_Server->GetMesh()->SkeletalMesh)
	{
		UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(Actor_Server->GetMesh(), "StonePetrifiedAlpha", Value);
		//Actor_Server->GetMesh()->SetScalarParameterValueOnMaterials("StonePetrifiedAlpha", Value);
	}
}

void UGameObjectInterface::OnCastActorStone(bool bBegin)
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());

	if (!ServerActor)
	{
		// 重置状态
		EffectType = -1;
		return;
	}

	if (bBegin)
	{
		//switch (EffectType)
		//{
		//	// 冰冻效果，暂停动画
		//	case 1:
		//	{
		//		ServerActor->GetMesh()->bPauseAnims = true;
		//	}
		//	break;
		//}
	}
	else
	{
		// 重置状态
		//switch (EffectType)
		//{
		//	// 冰冻效果，播放动画
		//	case 1:
		//	{
		//		ServerActor->GetMesh()->bPauseAnims = false;
		//	}
		//	break;
		//}
		EffectType = -1;
	}
}


void UGameObjectInterface::CLIENT_BindDisplayObject_Implementation(const FString& AttachMeshID)
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if (Actor_Server)
	{
		Actor_Server->BindMesh(FSTRING_TO_FNAME(AttachMeshID));
	}
}


void UGameObjectInterface::CLIENT_UnbindDisplayObject_Implementation(const FString& AttachMeshID)
{
	AServerCharacter* Actor_Server = Cast<AServerCharacter>(GetActor());
	if (Actor_Server)
	{
		Actor_Server->UnBindMesh(FSTRING_TO_FNAME(AttachMeshID));
	}
}

void UGameObjectInterface::CLIENT_ChangeShowAnimAndActionPosture_Implementation(const FString& NewModelId, const FString& InActionId, const FString& OutActionId)
{
	CheckChangePosAnim(1, NewModelId, InActionId, OutActionId);
}

void UGameObjectInterface::CLIENT_ChangeShowPosture_Implementation(const FString& NewModelId, const FString& InActionId, const FString& OutActionId)
{
	CheckChangePosAnim(2, NewModelId, InActionId, OutActionId);
}

void UGameObjectInterface::StartChangeModel()
{
	AServerCharacter* MyCharacter = Cast<AServerCharacter>(GetActor());
	if (!IsValid(MyCharacter) || !MyCharacter->IsInitialized())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGameObjectInterface::StartChangeModel : MyCharacter || MyCharacter->IsInitialized()!"));
		return;
	}
	if (IsValid(this) && GetEntity() != nullptr)
	{
		if (extraModelNumberList.Num() > 0)
		{
			MyCharacter->CheckCreateDynamicPartCpt(extraModelNumberList[0]);
			extraModelNumberList.Empty();
			SetModelScale(1.0f);
			UpdateActorPosition();
			MyCharacter->CreateAppearance();
		}
	}
}

void UGameObjectInterface::CheckChangePosAnim(int32 ChangeType, const FString& NewModelId, const FString& InActionId, const FString& OutActionId)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEntitySpaceEventInterface::ChangeShowPosture_Implementation : GetEntity()!"));
		return;
	}
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(GetActor());
	if (!ServerCharacter)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGameObjectInterface::ChangeShowPosture_Implementation : Character!"));
		return;
	}

	CachePosChangeType = ChangeType;
	CachePosNewModelId = NewModelId;
	CachePosInActionId = InActionId.IsEmpty() ? "None" : FSTRING_TO_FNAME(InActionId);
	CachePosOutActionId = OutActionId.IsEmpty() ? "None" : FSTRING_TO_FNAME(OutActionId);

	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("[ChangeShowPosture]bIsChangeModeling=%d,  id=%d"), MyCharacter->bIsChangeAppearanceling ? 1 : 0, GetEntity()->ID());
	if (ServerCharacter->bIsChangeAppearanceling)
	{
		TWeakObjectPtr<UGameObjectInterface> DelayThisPtr(this);
		TWeakObjectPtr<AServerCharacter> DelayServerCharacterPtr(ServerCharacter);
		if (PosAnimHandle.IsValid())
		{
			ServerCharacter->OnModelChangeAppearanceOverDelegate.Remove(PosAnimHandle);
			PosAnimHandle.Reset();
		}
		PosAnimHandle = ServerCharacter->OnModelChangeAppearanceOverDelegate.AddLambda([DelayThisPtr, DelayServerCharacterPtr]()
			{
				if (DelayThisPtr.IsValid() && DelayServerCharacterPtr.IsValid())
				{
					UGameObjectInterface* ThisPtr = DelayThisPtr.Get();
					AServerCharacter* ServerCharacter = DelayServerCharacterPtr.Get();
					if (IsValid(ThisPtr) && IsValid(ServerCharacter))
					{
						ThisPtr->StartChangePosAnim();
						ServerCharacter->OnModelChangeAppearanceOverDelegate.Remove(ThisPtr->PosAnimHandle);
					}
				}
			});
	}
	else
	{
		StartChangePosAnim();
	}
}

void UGameObjectInterface::StartChangePosAnim()
{
	AServerCharacter* Character = Cast<AServerCharacter>(GetActor());
	if (!Character)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGameObjectInterface::StartChangePosAnim : Character!"));
		return;
	}
	if (!CachePosNewModelId.IsEmpty())
	{
		auto ModelTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_MODEL);
		const FMODEL_DATA* pModelData = ModelTable->GetRow<FMODEL_DATA>(CachePosNewModelId);
		if (!pModelData)
		{
			FString DefaultModelNumber_M = UUECS3GameInstance::Instance->GameDefault->DefaultModelNumber_M;
			pModelData = ModelTable->GetRow<FMODEL_DATA>(DefaultModelNumber_M);
		}

		TSoftClassPtr<UAnimInstance> AnimationPath;
		if (CachePosChangeType == 1)
		{
			AnimationPath = pModelData->AnimationPath;
		}
		Character->ChangeAnimAction(AnimationPath, pModelData->ActionConfigPath, CachePosOutActionId, CachePosInActionId);

		CachePosChangeType = 0;
		CachePosNewModelId = "";
		CachePosInActionId = "";
		CachePosOutActionId = "";
	}
}

void UGameObjectInterface::UpdateActorPosition()
{
	GameObject* entity = (GameObject*)GetEntity();
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(GetActor());
	if (entity != nullptr && IsValid(ServerCharacter))
	{
		ServerCharacter->UpdateActorPositionToGround();
	}
}

void UGameObjectInterface::OnRep_moveSpeed()
{
	if (IsValid(GetActor()) && GetEntity() != nullptr)
	{
		float newValue = GetEntity()->GetDefinedProperty(TEXT("moveSpeed")).GetValue<float>();
		Cast<AServerCharacter>(GetActor())->SetMaxWalkSpeed(newValue * 100.f);
	}
}

CONTROL_COMPILE_OPTIMIZE_END
