

#include "MonsterExtJZZYXYInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Interface/Role/RoleSpaceContentInterface.h"
#include "Util/CS3Debug.h"
#include "Kismet/KismetMathLibrary.h"
#include "Kismet/KismetArrayLibrary.h"
#include "Manager/ParticleManager.h"
#include "Actor/Particle/EffectEmitter.h"
#include "ConstructorHelpers.h"
#include "Materials/Material.h"
#include "Manager/ResourceManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtJZZYXYInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtJZZYXYInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtJZZYXYInterface::UMonsterExtJZZYXYInterface()
{

}

UMonsterExtJZZYXYInterface::~UMonsterExtJZZYXYInterface()
{
}

void UMonsterExtJZZYXYInterface::RPC_onTreadZYXY()
{
	KBEngine::Entity* Monster = GetEntity();
	if (Monster == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterExtJZZYXYInterface::RPC_onTreadZYXY : Monster!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Monster->CellCall(TEXT("onTreadZYXY"), Args);
}

void UMonsterExtJZZYXYInterface::RPC_onTreadZYPoint()
{

	KBEngine::Entity* Monster = GetEntity();
	if (Monster == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMonsterExtJZZYXYInterface::RPC_onTreadZYPoint : Monster!"));
		return;
	}
	
	if (mOccupyStatus != 0)
		return;

	KBEngine::FVariantArray Args;
	Monster->CellCall(TEXT("onTreadZYPoint"), Args);
}

void UMonsterExtJZZYXYInterface::onStartOccupy_Implementation()
{
	mIsStartOccupy = true;
}

void UMonsterExtJZZYXYInterface::onEndOccupy_Implementation(bool isPlayerOccupy)
{
	mIsStartOccupy = false;
	mOccupyStatus = 2;

	if (isPlayerOccupy)
	{
		mOccupyStatus = 1;
		BP_StopStepFloor();
		APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		URoleSpaceContentInterface* interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), Player->EntityId));
		if (!IsValid(interface))return;
		for (int32 ectval : EffectUIDs)
		{
			FString MonsterId = INT_TO_FSTRING(EntityID) + "_" + INT_TO_FSTRING(ectval);
			interface->FirePointRecord.Remove(MonsterId);
		}
	}
	else
	{
		BP_StopStepFloor();
		AGameCharacter* MonsterXY = Cast<AGameCharacter>(GetActor());
		UMaterialInterface* MaterialObj =Cast<UMaterialInterface>(UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(
			FSoftObjectPath(TEXT("Material'/Game/Effects/Materials/M_30311_Guang8_Inst.M_30311_Guang8_Inst'"))));
		if (IsValid(MaterialObj) && IsValid(MonsterXY))
		{
			UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(MonsterXY->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
			DefaultStaticMeshCpt->SetMaterial(0, MaterialObj);
			DefaultStaticMeshCpt->SetMaterial(1, MaterialObj);
		}
	}
}

void UMonsterExtJZZYXYInterface::onNotifyExplodeCountdown_Implementation(int time)
{

}

bool UMonsterExtJZZYXYInterface::isCanLight(int32 entityID)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player) || Player->EntityId != entityID) return false;
	URoleSpaceContentInterface* interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), entityID));
	if (interface == nullptr || mOccupyStatus == 2 || !(interface->bIsHasRuDaoBuffFlag))
	{
		return false;
	}
	return true;
}

bool UMonsterExtJZZYXYInterface::BP_isCanLight()
{
	AServerCharacter* Owner = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(Owner))
	{
		return isCanLight(Owner->EntityId);
	}
	return false;
}

void UMonsterExtJZZYXYInterface::BP_StarStepFloor(float Distance , FString effectID)
{
	AGameCharacter* MonsterXY = Cast<AGameCharacter>(GetActor());
	if (!IsStepFloor && IsValid(MonsterXY))
	{
		//第一次进入时初始化数据
		SocketNames.Empty();
		IsStepFloor = true;
		UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(MonsterXY->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		SocketNames = DefaultStaticMeshCpt->GetAllSocketNames();
	}
	///判断当前模型有效性以及服务器数据是否可以开始踩火焰
	if (SocketNames.Num() <= 0 || !BP_isCanLight())
	{
		return ;
	}

	TWeakObjectPtr<UMonsterExtJZZYXYInterface> DelayThisPtr(this);
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;
	URoleSpaceContentInterface* interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), Player->EntityId));
	if (!IsValid(interface))return;

	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, CheckStepFloorventHandle,
		FTimerDelegate::CreateLambda([DelayThisPtr, MonsterXY, Player, effectID, ParticleManager, Distance, interface]()
	{
		if (!DelayThisPtr.IsValid())
		{
			return;
		}
		UMonsterExtJZZYXYInterface* ThisPtr = DelayThisPtr.Get();
		if (ThisPtr->SocketNames.Num() > 0)
		{
			UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(MonsterXY->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
			for (TArray<FName>::TIterator It = ThisPtr->SocketNames.CreateIterator(); It; It++)
			{
				FVector SocketLocation = DefaultStaticMeshCpt->GetSocketLocation(*It);
				float distance = UKismetMathLibrary::Vector_Distance(SocketLocation, Player->GetActorLocation());
				if (distance <= Distance)
				{
					int32 num = ThisPtr->SocketNames.Num();
					int32 EffectUID = ParticleManager->PlayParticle(effectID, 0.0f, MonsterXY, MonsterXY, FEffectCreate::CreateLambda([SocketLocation](int32 UID)
						{
							AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
							if (Effect)
							{
								Effect->SetActorLocation(SocketLocation);
							}
						}));
					ThisPtr->SaveSocketNmaes.Add(*It);
					ThisPtr->EffectUIDs.Add(EffectUID);
					FString MonsterId = INT_TO_FSTRING(ThisPtr->EntityID) + "_" + INT_TO_FSTRING(EffectUID);
					interface->FirePointRecord.Add(MonsterId);
					It.RemoveCurrent();
				}
			}
		}
		if (ThisPtr->SocketNames.Num() < 10)
		{
			ThisPtr->RPC_onTreadZYPoint();
			ThisPtr->IsStepFloor = false;
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->CheckStepFloorventHandle);
		}
	}), 0.1f, true);
}

void UMonsterExtJZZYXYInterface::BP_StopStepFloor()
{
	if (CheckStepFloorventHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CheckStepFloorventHandle);
	}
}

void UMonsterExtJZZYXYInterface::onExtinguishLight_Implementation(int32 num)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	URoleSpaceContentInterface* interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), Player->EntityId));
	if (!IsValid(interface))return;
	UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;
	if (SaveSocketNmaes.Num()>0&& IsStepFloor)
	{ 
		///删除所有生成的光效 
		for (int32 ectval: EffectUIDs)
		{
			if (ParticleManager->FindEmitterByUID(ectval))
			{
				ParticleManager->Stop(Cast<AEffectEmitter>(ParticleManager->FindEmitterByUID(ectval)));
				FString MonsterId = EntityID + "_" + ectval;
				interface->FirePointRecord.Remove(MonsterId);
			}
		}

		SaveSocketNmaes.Empty();
		EffectUIDs.Empty();
		IsStepFloor = false;//数据重置
	}
}

void UMonsterExtJZZYXYInterface::InitBlueCB()
{
	ArrBlueFunc.Add("onStartOccupy");
	ArrBlueFunc.Add("onEndOccupy");
	ArrBlueFunc.Add("onExtinguishLight");
	ArrBlueFunc.Add("onNotifyExplodeCountdown");
	Supper::InitBlueCB();
}
