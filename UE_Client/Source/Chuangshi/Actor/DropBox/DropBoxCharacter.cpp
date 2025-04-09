// Fill out your copyright notice in the Description page of Project Settings.

#include "DropBoxCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/Role/RoleDropBoxInterface.h"
#include "Manager/ParticleManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/VisibleManager.h"
#include "Manager/ShapeManager.h"
#include "Util/CS3Debug.h"
#include "Component/AppearanceComponent.h"
#include "Components/CapsuleComponent.h"
#include "../Particle/EffectEmitter.h"

ADropBoxCharacter::ADropBoxCharacter()
{
	CharacterClassName = TEXT("DropBoxCharacter");
	PrimaryActorTick.bCanEverTick = true;
	InitBaseComponent();
}

void ADropBoxCharacter::OnUnBindActorCallBack()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(this);
	clearAllStayEffect();
}

void ADropBoxCharacter::GossipWith()
{
	///玩家转向DropBox
	FVector StartLoction = GetActorLocation();
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:ASpellBoxCharacter::GossipWith : PlayerActor!"));
		return;
	}

	FVector TargetLoction = PlayerActor->GetActorLocation();
	FRotator PlayerRotation = UGolbalBPFunctionLibrary::GetLookAtRotator(TargetLoction, StartLoction);
	PlayerActor->SetActorRotation(PlayerRotation);
	PlayerActor->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_TALKTODROPBOX;
	RequestPickUpAllItemsOrOpenBox();
}

void ADropBoxCharacter::OnCreateApperanceOver()
{
	Super::OnCreateApperanceOver();
	pDropBoxShape = CreateSphereShape();
}

UBaseShape* ADropBoxCharacter::CreateSphereShape()
{
	float radius = m_SphereRadius;
	FVector shapeVector = FVector(radius, radius, radius);
	return UUECS3GameInstance::Instance->ShapeManager->CreateShape(this, this, SHAPE_TYPE::SHPERE, shapeVector, &ADropBoxCharacter::OnPlayerBeginOverlap, &ADropBoxCharacter::OnPlayerEndOverlap);
}

void ADropBoxCharacter::OnPlayerBeginOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->AddToInteractivityList(this);
}

void ADropBoxCharacter::OnPlayerEndOverlap_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor)) return;
	PlayerActor->RemoveFromInteractivityList(this);
}

void ADropBoxCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));

	PlayAction("Idle_Free");
}

int32 ADropBoxCharacter::ConfirmQuality()
{
	int CurQuality = 0;
	for (auto& DropBoxItem : GetBoxItemList())
	{
		if (CurQuality < DropBoxItem->Quality)
		{
			CurQuality = DropBoxItem->Quality;
		}
	}
	return CurQuality;
}

void ADropBoxCharacter::CurveMoveAndZoom(const FString& DragActionID, const FString& levitateActionID, const FVector& InStartPosition, const FVector& InEndPosition, float XMoveSpeed, float Scale /*= 1.0f*/, float Gravity /*= 980.0f*/)
{
	//播动作
	if (!DragActionID.IsEmpty())
	{
		PlayAction(FName(*DragActionID));
	}

	// 重置数据
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CurveMoveHandle);
	}
	CurveMoveDeltaTime = 0.0;
	CurveMovePercent = 0.0;
	// 屏蔽位置同步
	SetEnableSyncServerPos(false);

	float Angle = 0.75f;//对应正弦函数X轴上的度数，根据表现可以定义不同的值
	FVector StartPosition = FVector(InStartPosition.X, InStartPosition.Y, GetActorLocation().Z);
	FVector EndPosition = InEndPosition;
	if (!IsMoveFlying())
	{
		EndPosition.Z = InEndPosition.Z + GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() * Scale;
	}
	FVector Dir = EndPosition - StartPosition;
	FVector XDir = FVector(Dir.X, Dir.Y, 0.0f);
	if (Dir.Size() < 10) return;

	float UpTime = 0.0f;//向上的时间
	float NeedTime = 0.0f;//整个过程需要的时间
	float Max_RisingDistance = 0.0f;//正弦函数的系数A y=Asin(ωx+φ)+k
	if (XDir.Size() < 100)//水平距离太短
	{
		NeedTime = FMath::Sqrt(2 * abs(Dir.Z) / Gravity);
		UpTime = NeedTime;
		XMoveSpeed = XDir.Size() / NeedTime;
		Angle = 0.5;
		Max_RisingDistance = Dir.Z / FMath::Sin(Angle* PI);
	}
	else
	{
		NeedTime = XDir.Size() / XMoveSpeed;
		if (abs(Dir.Z) < 100)//垂直距离太短
		{
			UpTime = NeedTime / 2;
			Angle = 1.0f;
			Max_RisingDistance = 0.5 * Gravity * UpTime * UpTime;
		}
		else
		{
			UpTime = (NeedTime / (Angle*PI)) * (0.5*PI);
			Max_RisingDistance = Dir.Z / FMath::Sin(Angle* PI);
		}
	}

	FRotator LookRotation = FRotationMatrix::MakeFromX(Dir).Rotator();
	SetActorRotation(FRotator(GetActorRotation().Pitch, LookRotation.Yaw, GetActorRotation().Roll));

	TWeakObjectPtr<ADropBoxCharacter> ThisPtr(this);
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(
			this, CurveMoveHandle, FTimerDelegate::CreateLambda([ThisPtr, Angle, Dir, XDir,
				XMoveSpeed, StartPosition, EndPosition, UpTime, NeedTime, Max_RisingDistance, Gravity, Scale, levitateActionID]()
		{
			if (ThisPtr.IsValid())
			{
				ADropBoxCharacter* DropBox = ThisPtr.Get();
				float DstDistanceZ = 0.0f;
				FVector2D XPercent = FVector2D(0, 0);
				if (IsValid(DropBox))
				{
					DropBox->CurveMoveDeltaTime += DropBox->GetWorld()->GetDeltaSeconds();
					if (Dir.Z >= 0.0f || abs(Dir.Z) < 100)
					{
						//从低处往高处跳 或者同一水平面跳跃
						DropBox->CurveMovePercent = DropBox->CurveMoveDeltaTime / (2 * UpTime);
						// 大于Angel的时候清空
						if (DropBox->CurveMovePercent >= Angle || DropBox->CurveMoveDeltaTime >= NeedTime)
						{
							DropBox->StopCurveMoveAndZoom(Scale, EndPosition, levitateActionID);
							return;
						}
						else
						{
							DstDistanceZ = StartPosition.Z + FMath::Sin(DropBox->CurveMovePercent * PI) * Max_RisingDistance;
							XPercent = FVector2D(StartPosition + (XMoveSpeed * DropBox->CurveMoveDeltaTime)* XDir.GetSafeNormal());
							DropBox->SetActorLocation(FVector(XPercent.X, XPercent.Y, DstDistanceZ));
						}
					}
					else
					{
						DstDistanceZ = StartPosition.Z - 0.5f * Gravity * (DropBox->CurveMoveDeltaTime * DropBox->CurveMoveDeltaTime);
						//从高处往低处跳
						if (DstDistanceZ <= EndPosition.Z || DropBox->CurveMoveDeltaTime >= NeedTime)
						{
							DropBox->StopCurveMoveAndZoom(Scale, EndPosition, levitateActionID);
							return;
						}
						else
						{
							XPercent = FVector2D(StartPosition + (XMoveSpeed * DropBox->CurveMoveDeltaTime)* XDir.GetSafeNormal());
							DropBox->SetActorLocation(FVector(XPercent.X, XPercent.Y, DstDistanceZ));
						}
					}
					//设置Actor缩放
					float tempScale = (DropBox->CurveMoveDeltaTime / NeedTime) * Scale;
					DropBox->SetActorScale3D(FVector(tempScale, tempScale, tempScale));
				}
			}
		}), GetWorld()->GetDeltaSeconds(), true, 0.5);
	}
}

void ADropBoxCharacter::OpenDropEffectEvent(FString EffectID1 /*= TEXT("103088")*/, FString EffectID2 /*= TEXT("103088_3")*/)
{
	StayEffectID = EffectID2;
	TWeakObjectPtr<ADropBoxCharacter> DelayThisPtr(this);
	int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID1, 0.0f, this, this, FEffectCreate::CreateLambda([DelayThisPtr, EffectID2](int32 UID)
	{
		//光效到达的时候播第二个在空中持续的光效
		AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
		ADropBoxCharacter* ThisPtr = DelayThisPtr.Get();
		if (IsValid(ThisPtr) && IsValid(Effect))
		{
			AEffectEmitter* tempEffect = Cast<AEffectEmitter>(Effect);
			if (IsValid(tempEffect))
			{
				tempEffect->OnEffectArrived.AddDynamic(ThisPtr, &ADropBoxCharacter::OpenDropStayEffectEvent);
			}
		}
	}));
}

void ADropBoxCharacter::OpenDropStayEffectEvent()
{
	if (DeletedCount>0)
	{
		DeletedCount--;
	}
	else
	{
		int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(StayEffectID, 0.0f, this, this);
		StayEffectUIDList.Emplace(EffectUID);
	}
}

void ADropBoxCharacter::FlyTargetEffectEvent(int32 TargetID, FString EffectID)
{
	AActor* sourceActor = nullptr;
	if (StayEffectUIDList.Num()>0)
	{
		sourceActor = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(StayEffectUIDList[0]);
	}
	if (!IsValid(sourceActor))
	{
		sourceActor = this;
	}
	AActor* targer = UGolbalBPFunctionLibrary::GetActorByID(TargetID);
	if (IsValid(sourceActor) && IsValid(targer))
	{
		TWeakObjectPtr<ADropBoxCharacter> DelayThisPtr(this);
		int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, sourceActor, targer, FEffectCreate::CreateLambda([DelayThisPtr](int32 UID)
		{
			DelayThisPtr->FlyTargerOverEvent();
		}));

	}
	DeletedCount++;///用来计数需要删除的粒子数量（因为创建是个异步的过程，而且是等飞行粒子创建完了才创建停留粒子，快速操作的话服务器可能发过来结束了，客户端还没创建停留的粒子）
	if (StayEffectUIDList.Num() > 0)
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(StayEffectUIDList.Pop());
		DeletedCount--;
	}
}

void ADropBoxCharacter::FlyTargerOverEvent()
{

}

void ADropBoxCharacter::StopCurveMoveAndZoom(float Scale, const FVector& InEndPosition, const FString& levitateActionID)
{
	//播动作
	if (!levitateActionID.IsEmpty())
	{
		PlayAction(FName(*levitateActionID));
	}

	SetActorScale3D(FVector(Scale, Scale, Scale));
	FVector EndPosition;
	if (IsMoveFlying())
	{
		EndPosition = InEndPosition;
	}
	else
	{
		EndPosition = FloorTrace(InEndPosition, true);
	}
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CurveMoveHandle);
	}
	
	SetActorLocation(EndPosition);
	SetEnableSyncServerPos(true);
}

void ADropBoxCharacter::clearAllStayEffect()
{
	if (StayEffectUIDList.Num() > 0)
	{
		for (auto StayEffectUID : StayEffectUIDList)
		{
			UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(StayEffectUID);
		}
		StayEffectUIDList.Empty();
	}
	DeletedCount = 0;
}

bool ADropBoxCharacter::isVisible(const UINT64 &PlayerDBID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------- check DropBox is visible by playerDBID:[%u] "), PlayerDBID);
	KBEngine::Entity* DropBox = GetSelfEntity();

	if (DropBox != nullptr)
	{
		FVariant Propvalue = DropBox->GetDefinedProperty(TEXT("ownershipIDs"));
		TArray<FVariant> array = Propvalue.GetValue<TArray<FVariant>>();
		for (int i = 0; i < array.Num(); i++)
		{

			UINT64 Value = UINT64(array[i].GetValue<UINT64>());
			if (PlayerDBID == Value)
			{
				return true;
			}
		}
		return false;
	}

	return false;
}

void ADropBoxCharacter::TraceDropBox(float range)
{
	RealTraceDropBox(range);
}

void ADropBoxCharacter::updateDropBoxModelVisible()
{
	UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(this);
}

void ADropBoxCharacter::CloseBox()
{

	//检测当前动作是否为关闭的动作，如果是则不执行
	if (GetBaseAnimInstance() && "Show_01" == GetBaseAnimInstance()->GetCurPlayActionData().Id)
	{
		return;
	}
	PlayAction("Show_01");
}

void ADropBoxCharacter::OpenBox()
{
	//检测当前动作是否为开启的动作，如果是则不执行
	if (GetBaseAnimInstance() && "Show_02" == GetBaseAnimInstance()->GetCurPlayActionData().Id)
	{
		return;
	}

	PlayAction("Show_02");
}

void ADropBoxCharacter::PlayEffect(FString EffectID)
{
	UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;

	//判断当前粒子是否为将要播放的粒子，如果是就不执行
	if (ParticleManager->FindEffectIDByUID(CurEmitterUID) == EffectID)
	{
		return;
	}

	//如果要切换粒子就先删除旧粒子
	ParticleManager->StopEffectByUID(CurEmitterUID);

	if (UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->BaseSettingData.IsDropTipsEffect)
	{
		//添加并获取到粒子
		CurEmitterUID = ParticleManager->PlayParticle(EffectID, 0.0f, this, this);
	}
}

void ADropBoxCharacter::StopEffect()
{
	UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(CurEmitterUID);
}

TArray<UItemBase*> ADropBoxCharacter::GetBoxItemList()
{
	return DropBox_ItemList;
}

bool ADropBoxCharacter::IsBoxEmpty()
{
	if (GetBoxItemList().Num() > 0)
	{
		return false;
	}
	return true;
}

void ADropBoxCharacter::SetBoxEffect()
{
	if (UUECS3GameInstance::Instance && 
		UUECS3GameInstance::Instance->LocalDataSaveManager &&
		UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData &&
		UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->BaseSettingData.IsDropTipsEffect)
	{
		int32 Quality = ConfirmQuality();
		switch (Quality)
		{
		case 1:
			PlayEffect(TEXT("DropBoxWhite"));
			break;
		case 2:
			PlayEffect(TEXT("DropBoxBule"));
			break;
		case 3:
			PlayEffect(TEXT("DropBoxGolden"));
			break;
		case 4:
			PlayEffect(TEXT("DropBoxPink"));
			break;
		case 5:
		case 6:
		case 7:
			PlayEffect(TEXT("DropBoxGreen"));
			break;
		default:
			break;
		}
	}
	else
	{
		StopEffect();
	}
}

void ADropBoxCharacter::RealTraceDropBox(float range, FDropBoxDelegate Delegate /*= nullptr*/)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		TWeakObjectPtr<ADropBoxCharacter> DelayThisPtr(this);
		PlayerController->TraceTargetActor(this, range, FTraceCallback::CreateLambda([DelayThisPtr, Delegate](bool IsSuccess)
		{
			if (DelayThisPtr.IsValid() && IsSuccess)
			{
				ADropBoxCharacter* ThisPtr = DelayThisPtr.Get();
				UCS3EntityInterface* TempInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleDropBoxInterface"), 0);
				if (IsValid(TempInterface))
				{
					URoleDropBoxInterface* RoleDropBoxInterface = Cast<URoleDropBoxInterface>(TempInterface);
					if (IsValid(RoleDropBoxInterface))
					{
						RoleDropBoxInterface->ReqSendItemInfoListToClient(ThisPtr->EntityId);
					}
				}
			}
		
			Delegate.ExecuteIfBound(IsSuccess);
		}));
	}
}

void ADropBoxCharacter::SetAlreadyRequest(bool IsRequest)
{
	IsAlreadyRequest = IsRequest;
}

bool ADropBoxCharacter::HasUIdInDropBoxItemList(const FString& UId)
{
	for (auto item : GetBoxItemList())
	{
		if (UId == item->UID)
		{
			return true;
		}
	}
	return false;
}

void ADropBoxCharacter::UpdateDropBoxItemList(const FString& UId, int32 LeftAmount)
{
	for (auto item : GetBoxItemList())
	{
		if (UId == item->UID)
		{
			if (LeftAmount == 0)
			{
				GetBoxItemList().Remove(item);
			}
			else if (item->Amount != LeftAmount)
			{
				item->Amount = LeftAmount;
			}
			break;
		}
	}
}

void ADropBoxCharacter::DropBoxInteractiveFinshed()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		///<交互完成后状态的刷新，设置玩家的交互状态
		if (IsValid(PlayerActor->CurInteractiveTarget) && IsValid(this) && PlayerActor->CurInteractiveTarget == this)
		{
			PlayerActor->EPlayerInteractiveState = APLAYER_INTERACTIVE_ENUM::APLAYER_INTERACTIVE_NODE;
		}
	}
}

void ADropBoxCharacter::RequestPickUpAllItemsOrOpenBox_Implementation()
{

}