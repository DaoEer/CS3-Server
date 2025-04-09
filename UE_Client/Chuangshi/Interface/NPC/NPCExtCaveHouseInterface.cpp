
#include "NPCExtCaveHouseInterface.h"
#include "Components/TextRenderComponent.h"
#include "Actor/Scene/PlantCharacter.h"
#include "Component/AvatarFilterActorComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ParticleManager.h"
#include "Manager/EventManager.h"
#include "Manager/ResourceManager.h"
#include "GameData/ConstData.h"


CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(UNPCExtCaveHouseInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnShowLingTian, &UNPCExtCaveHouseInterface::OnShowLingTian, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UNPCExtCaveHouseInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(lightWallID, &UNPCExtCaveHouseInterface::Set_lightWallID, int32)
CS3_END_INTERFACE_PROPERTY_MAP()


UNPCExtCaveHouseInterface::UNPCExtCaveHouseInterface()
{
}


UNPCExtCaveHouseInterface::~UNPCExtCaveHouseInterface()
{
}


void UNPCExtCaveHouseInterface::OnShowBuildUI_Implementation(const FString& endBuildTime)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnShowBuildUIEvent.Broadcast(endBuildTime);
		}
	}
}

void UNPCExtCaveHouseInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OnShowBuildUI");
	Supper::InitBlueCB();
}

void UNPCExtCaveHouseInterface::Set_lightWallID(const int32 & newVal, const int32 & oldVal)
{
	UParticleManager* partMgr = UGolbalBPFunctionLibrary::ParticleManager();
	if (IsValid(partMgr))
	{
		if (LightWallUID)
		{
			partMgr->StopEffectByUID(LightWallUID);
		}
		if (newVal)
		{
			AActor* selfActor = GetActor();
			LightWallUID = partMgr->PlayParticle(INT_TO_FSTRING(newVal), 0.0f, selfActor, selfActor);
		}
	}
	
}

void UNPCExtCaveHouseInterface::OnShowLingTian(const FVariant & Var)
{
	UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	if (IsValid(GameInstance))
	{
		LTDatas.datas.Empty();
		LTDatas = LINGTIAN_DATA_ARR(Var);

		UClass* ActorClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("PlantCharacter"));
		if (!ActorClass)return;
		AActor* actor = this->GetActor();
		TWeakObjectPtr<UNPCExtCaveHouseInterface> DelayThis(this);
		if (!IsValid(actor))return;
		for (auto i = 0; i < 4; ++i)
		{
			GameInstance->ResourceManager->RequestAsyncLoad(this, FStringAssetReference(ActorClass),
				FStreamableDelegate::CreateLambda([DelayThis, ActorClass, i]()
			{
				if (!DelayThis.IsValid())return;
				UNPCExtCaveHouseInterface* DelayInterface = DelayThis.Get();
				AActor* actor = DelayInterface->GetActor();
				if (!IsValid(actor))return;
				if (ActorClass)
				{
					FTransform SpawnTransform = FTransform();
					APlantCharacter* RetActor = Cast<APlantCharacter>(UGolbalBPFunctionLibrary::BeginDeferredActorSpawnFromClass(ActorClass, SpawnTransform));
					if (RetActor)
					{
						RetActor->AttachToActor(actor, FAttachmentTransformRules::KeepRelativeTransform);
						RetActor->SetActorRelativeLocation(LHMJ_LING_TIAN_POS[i]);
						RetActor->SetActorScale3D(FVector(0.26f, 0.26f, 0.26f));
						RetActor->OnBroadCreateModelOver.BindUObject(RetActor, &APlantCharacter::InitPlantData, DelayInterface->GetLingTianDataByIndex(i));
						RetActor->CreateAppearance();
						DelayInterface->PlantCharacterMap.Add(i, RetActor);
					}
				}
			}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY, LHMJ_LING_TIAN_POS[i]);
		}
	}
}

LINGTIAN_DATA UNPCExtCaveHouseInterface::GetLingTianDataByIndex(const int32& index)
{
	if (LTDatas.datas.Num() > 0)
	{
		FString scriptID = LHMJ_LT_SCRIPTS[index];
		for (auto LTData : LTDatas.datas)
		{
			if (LTData.scriptID == scriptID)
			{
				return LTData;
			}
		}
	}
	LINGTIAN_DATA temp;
	temp.seedNum = 0;
	temp.growthStage = 0;
	temp.growTime = 0;
	return temp;
}

void UNPCExtCaveHouseInterface::onEnterWorld()
{
	Supper::onEnterWorld();
	
	
}

void UNPCExtCaveHouseInterface::onLeaveWorld()
{
	PlantCharacterMap.Empty();
	Supper::onLeaveWorld();
}

CONTROL_COMPILE_OPTIMIZE_END
