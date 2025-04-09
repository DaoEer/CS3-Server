// Fill out your copyright notice in the Description page of Project Settings.

#include "CollisionComponent.h"
// UE4
#include "Components/CapsuleComponent.h"
#include "Components/PrimitiveComponent.h"
#include "Component/SpringArmComponentEX.h"
// 数据类型
#include "GameData/CollideData.h"
#include "GameData/GameDefault.h"
#include "GameData/CharacterData.h"
#include "GameData/GameDefine.h"
// CS3类型
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/ServerCharacter.h"
#include "Actor/NPCBaseCharacter.h"
#include "Actor/Pet/RiderCharacter.h"
#include "Actor/Action/BaseAnimInstance.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CfgManager.h"
#include "Actor/Scene/MovingPlatformCharacter.h"


CONTROL_COMPILE_OPTIMIZE_START

void UCollisionComponent::UpdateModelCollision()
{
	// 先根据标志位更新碰撞
	if (UpdateModelCollisionByFlag())
	{
		return;
	}
		
	// 不是玩家走一下状态更新
	AServerCharacter* Owner = Cast<AServerCharacter>(GetOwner());
	AServerCharacter* Player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!Player || Player == Owner)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCollisionComponent::UpdateModelCollision : Player!"));
		return;
	}
		
	if (UpdateModelCollisionByState())
	{
		return;
	}

	UpdateModelCollisionByChannel();
}

bool UCollisionComponent::UpdateModelCollisionByFlag()
{	
	// 根据标志位刷新模型的碰撞
	// 12：开启胶囊体碰撞	23：关闭胶囊体碰撞	24：开始骨骼和默认静态网格碰撞	28：开启摄像机碰撞 	31：开启光线碰撞通道-地面
	// 当12和24同时存在时，只有24生效。
	// 当12和13同时存在时，只有13生效。

	// 7号通道：啥都碰		12号标志位
	// 8号通道：啥都不碰	23号标志位

	AServerCharacter* owner = Cast<AServerCharacter>(GetOwner());

	if (!owner)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCollisionComponent::UpdateModelCollisionByFlag : owner!"));
		return false;
	}

	KBEngine::Entity* Entity = owner->GetSelfEntity();

	if (!Entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCollisionComponent::UpdateModelCollisionByFlag : Entity!"));
		return false;
	}

	ENTITY_TYPE EntityType = (ENTITY_TYPE)Entity->GetDefinedProperty(TEXT("entityFlag")).GetValue<uint8>();
	if (!(EntityType == ENTITY_TYPE::ENTITY_FLAG_MONSTER ||
		EntityType == ENTITY_TYPE::ENTITY_FLAG_NPC ||
		EntityType == ENTITY_TYPE::ENTITY_FLAG_SPELL ||
		EntityType == ENTITY_TYPE::ENTITY_FLAG_TRAP ||
		EntityType == ENTITY_TYPE::ENTITY_FLAG_PLATFORM))

		return false;

	bool bCollisionChange = false;
	int64 Bit = 0x01;

	// 获取当前对象的所有标志位
	int64 CurrentFlags = Entity->GetDefinedProperty(TEXT("flags")).GetValue<int64>();
	
	// 12号标志位有变化
	if ((FlagCache & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_COLLISION)) ^ (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_COLLISION)))
	{
		// 没有24号和23号，23和24优先级比12高
		if (!(CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_CLOSE_COLLISION)) && !(CurrentFlags & (0x1 << (uint8)ENTITY_FLAG::FLAG_MESH_COLLISION)))
		{
			if (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_COLLISION))
			{
				SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel7);
			}

			bCollisionChange = true;
		}
	}

	// 23号标志位有变化
	if ((FlagCache & (Bit << (uint8)ENTITY_FLAG::FLAG_CLOSE_COLLISION)) ^ (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_CLOSE_COLLISION)))
	{
		if (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_CLOSE_COLLISION))
		{
			SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel8);
		}
		else
		{
			// 没有24号
			if ((CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_COLLISION)) && !(CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_MESH_COLLISION)))
			{
				SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel7);
			}
		}

		bCollisionChange = true;
	}

	// 24号标志位有变化
	if ((FlagCache & (Bit << (uint8)ENTITY_FLAG::FLAG_MESH_COLLISION)) ^ (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_MESH_COLLISION)))
	{
		UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		if (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_MESH_COLLISION))
		{
			// 开启真实碰撞的时候其实是不用改变碰撞的类型的，Mesh的类型已经有头发控制，STMesh_DefaultStatic默认是StaticMesh类型
			SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel7, DefaultStaticMeshCpt);
			owner->GetMesh()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
			SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel7, owner->GetMesh());
			DefaultStaticMeshCpt->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
			// 没有13号
			if ((CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_COLLISION)) && !(CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_CLOSE_COLLISION)))
			{
				SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel8);
			}
		}
		else
		{
			SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel8, DefaultStaticMeshCpt);
			SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel8, owner->GetMesh());

			// 没有13号
			if ((CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_COLLISION)) && !(CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_CLOSE_COLLISION)))
			{
				SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel7);
			}
		}

		bCollisionChange = true;
	}
	
	// 28号标志位有变化
	if ((FlagCache & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_CAMERA_COLLISION)) ^ (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_CAMERA_COLLISION)))
	{
		UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		if (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_CAMERA_COLLISION))
		{
			owner->GetMesh()->SetCollisionResponseToChannel(ECollisionChannel::ECC_Camera, ECollisionResponse::ECR_Block);
			DefaultStaticMeshCpt->SetCollisionResponseToChannel(ECollisionChannel::ECC_Camera, ECollisionResponse::ECR_Block);
			
		}
		else
		{
			owner->GetMesh()->SetCollisionResponseToChannel(ECollisionChannel::ECC_Camera, ECollisionResponse::ECR_Ignore);
			DefaultStaticMeshCpt->SetCollisionResponseToChannel(ECollisionChannel::ECC_Camera, ECollisionResponse::ECR_Ignore);
		}

		// 为什么这个地方的 bCollisionChange = true 没写？
		// 摄像机碰撞和骨骼的碰撞没有直接的联系，下面还会继续刷新
	}

	// 31号标志位有变化
	if ((FlagCache & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_GROUND_TRACE_COLLISION_CHANNEL)) ^ (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_GROUND_TRACE_COLLISION_CHANNEL)))
	{
		UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(owner->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		if (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_GROUND_TRACE_COLLISION_CHANNEL))
		{
			owner->GetMesh()->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel10, ECollisionResponse::ECR_Block);
			DefaultStaticMeshCpt->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel10, ECollisionResponse::ECR_Block);

		}
		else
		{
			owner->GetMesh()->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel10, ECollisionResponse::ECR_Ignore);
			DefaultStaticMeshCpt->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel10, ECollisionResponse::ECR_Ignore);
		}
	}
	
	FlagCache = CurrentFlags;

	// 当有12或者23号标志位时，算标志位碰撞更新
	if (!bCollisionChange && ((CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_OPEN_COLLISION)) || (CurrentFlags & (Bit << (uint8)ENTITY_FLAG::FLAG_CLOSE_COLLISION))))
	{
		bCollisionChange = true;
	}

	return bCollisionChange;
}

bool UCollisionComponent::UpdateModelCollisionByState()
{
	AServerCharacter* owner = Cast<AServerCharacter>(GetOwner());

	if (!owner)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCollisionComponent::UpdateModelCollisionByState : Player!"));
		return false;
	}

	KBEngine::Entity* Entity = owner->GetSelfEntity();

	if (!Entity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCollisionComponent::UpdateModelCollisionByState : Entity!"));
		return false;
	}

	ENTITY_TYPE EntityType = (ENTITY_TYPE)Entity->GetDefinedProperty(TEXT("entityFlag")).GetValue<uint8>();

	if (!(EntityType == ENTITY_TYPE::ENTITY_FLAG_ROLE || EntityType == ENTITY_TYPE::ENTITY_FLAG_MONSTER || EntityType == ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		return false;
	}

	ENTITY_STATE EntityState = (ENTITY_STATE)Entity->GetDefinedProperty(TEXT("state")).GetValue<int32>();
	
	if (EntityState == ENTITY_STATE::EntityStatePead || 
		EntityState == ENTITY_STATE::EntityStateDead || 
		EntityState == ENTITY_STATE::EntityStateReset ||
		EntityState == ENTITY_STATE::EntityStateShow || 
		EntityState == ENTITY_STATE::EntityStateStall)
	{
		SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel8);			// 啥都不碰
		return true;
	}

	return false;
}

bool UCollisionComponent::UpdateModelCollisionByChannel()
{
	AServerCharacter* Owner = Cast<AServerCharacter>(GetOwner());
	AServerCharacter* Player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!Player || Player == Owner)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCollisionComponent::UpdateModelCollisionByChannel : Player!"));
		return false;
	}

	switch (Player->QueryRelation(Owner))
	{
		case COMBAT_RELATION::COMBAT_RELATION_ENEMY:
		{
			SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel6);
		}
			break;
		default:
		{
			SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel5);
		}
			break;
	};

	return true;
}

void UCollisionComponent::SetPlayerCollisionByNormal()
{
	AServerCharacter* Player = Cast<AServerCharacter>(GetOwner());
	if (Player && Player->ActorIsPlayer())
	{
		SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel3);		///玩家
	}
}

void UCollisionComponent::SetPlayerCollisionByCast()
{
	AServerCharacter* Player = Cast<AServerCharacter>(GetOwner());
	if (Player && Player->ActorIsPlayer())
	{
		SetPlayerCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel4);			///施法玩家
	}
}

void UCollisionComponent::SetPlayerCollisionResponseToChannel(ECollisionChannel Channel, UPrimitiveComponent* Comp /*= nullptr*/)
{
	AServerCharacter* owner = Cast<AServerCharacter>(GetOwner());
	if (!Comp)
	{
		Comp = owner->GetCapsuleComponent();
	}

	Comp->SetCollisionObjectType(Channel);
	UCfgManager* cfbMgr = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* table = cfbMgr->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_COLLIDE_DATA);

	TArray<FCOLLIDE_DATA*> CollideDatas;
	table->GetAllRows(CollideDatas);
	for (FCOLLIDE_DATA* collideData : CollideDatas)
	{
		if (collideData->Channel == Channel)
		{
			for (auto iChannel : collideData->IgnoreChannel)
			{
				Comp->SetCollisionResponseToChannel(iChannel, ECollisionResponse::ECR_Ignore);
			}
			for (auto oChannel : collideData->OverlapChannel)
			{
				Comp->SetCollisionResponseToChannel(oChannel, ECollisionResponse::ECR_Overlap);
			}
			for (auto bChannel : collideData->BlockChannel)
			{
				Comp->SetCollisionResponseToChannel(bChannel, ECollisionResponse::ECR_Block);
			}
			return;
		}
	}
}

void UCollisionComponent::InitCollision()
{
	AGameCharacter* GameCharacter = Cast<AGameCharacter>(GetOwner());
	if (!IsValid(GameCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCollisionComponent::InitCollision : GameCharacter!"));
		return;
	}

	// 这个GhostReceiverCharacter是施法空盒子，不需要碰撞
	if (GameCharacter->CharacterClassName == "GhostReceiverCharacter")
	{
		DisableAllCollision();
		return;
	}

	TSet<UMeshComponent*> MeshComponentArray;
	for (auto Component : GameCharacter->GetComponents())
	{
		UMeshComponent* MeshComponent = Cast<UMeshComponent>(Component);
		if (IsValid(MeshComponent))
		{
			MeshComponentArray.Add(MeshComponent);
		}
	}

	UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(GameCharacter->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
	MeshComponentArray.Remove(GameCharacter->GetMesh());
	MeshComponentArray.Remove(DefaultStaticMeshCpt);

	for (auto Component : MeshComponentArray)
	{

		if (Cast<USkeletalMeshComponent>(Component))
		{
			Component->SetCollisionObjectType(ECollisionChannel::ECC_PhysicsBody);
		}
		else
		{
			Component->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
		}

		Component->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		Component->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Ignore);
	}

	GameCharacter->GetMesh()->SetCollisionObjectType(ECollisionChannel::ECC_WorldDynamic);
	GameCharacter->GetMesh()->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Ignore);
	GameCharacter->GetMesh()->SetCollisionResponseToChannel(ECollisionChannel::ECC_Visibility, ECollisionResponse::ECR_Block);
	GameCharacter->GetMesh()->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel13, ECollisionResponse::ECR_Overlap);

	DefaultStaticMeshCpt->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	DefaultStaticMeshCpt->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Ignore);
	DefaultStaticMeshCpt->SetCollisionObjectType(ECollisionChannel::ECC_WorldStatic);
	DefaultStaticMeshCpt->SetCollisionResponseToChannel(ECollisionChannel::ECC_Visibility, ECollisionResponse::ECR_Block);
	DefaultStaticMeshCpt->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel13, ECollisionResponse::ECR_Overlap);

	GameCharacter->GetCapsuleComponent()->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Ignore);
	GameCharacter->GetCapsuleComponent()->SetCollisionObjectType(ECollisionChannel::ECC_WorldDynamic);
	GameCharacter->GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_Visibility, ECollisionResponse::ECR_Block);
	GameCharacter->GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_WorldStatic, ECollisionResponse::ECR_Block);
	GameCharacter->GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_WorldDynamic, ECollisionResponse::ECR_Overlap);
	GameCharacter->GetCapsuleComponent()->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel13, ECollisionResponse::ECR_Overlap);
	
	/*if (Cast<APlayerCharacter>(GetOwner()) && Cast<APlayerCharacter>(GetOwner())->ActorIsPlayer())
	{
		for (int8 i = 24; i < 32; i++)
		{
			GameCharacter->GetCapsuleComponent()->SetCollisionResponseToChannel((ECollisionChannel)i, ECollisionResponse::ECR_Block);
		}
	}*/
	if (Cast<AMovingPlatformCharacter>(GetOwner()))
	{
		// 移动平台算是地面
		AMovingPlatformCharacter* MovingPlatform = Cast<AMovingPlatformCharacter>(GetOwner());
		UStaticMeshComponent* MovingPlatformDefaultStaticMeshCpt = Cast<UStaticMeshComponent>(MovingPlatform->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		MovingPlatformDefaultStaticMeshCpt->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel10, ECollisionResponse::ECR_Block);
	}
	else if (Cast<AMonsterCharacter>(GetOwner()))
	{
		// 目前怪物不使用Mesh上的碰撞
		GameCharacter->GetMesh()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		// 目前怪物胶囊体没有物理模拟需求
		GameCharacter->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	}
	else
	{
		GameCharacter->GetMesh()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
		GameCharacter->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	}
}

void UCollisionComponent::DisableAllCollision()
{
	AGameCharacter* GameCharacter = Cast<AGameCharacter>(GetOwner());
	if (IsValid(GameCharacter))
	{
		UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(GameCharacter->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		GameCharacter->GetMesh()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		DefaultStaticMeshCpt->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		GameCharacter->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
}

void UCollisionComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);

	DisableAllCollision();
}

void UCollisionComponent::SetWaterCollision(UPrimitiveComponent* Component, WATER_TYPE_ENUM WaterType)
{
	if (!Component)
	{
		return;
	}
	// 设置所有的为无碰撞
	Component->SetCollisionResponseToAllChannels(ECollisionResponse::ECR_Ignore);
	// 所有射线可检测
	Component->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel10, ECollisionResponse::ECR_Block);
	Component->SetCollisionResponseToChannel(ECollisionChannel::ECC_Camera, ECollisionResponse::ECR_Block);
	Component->SetCollisionResponseToChannel(ECollisionChannel::ECC_Visibility, ECollisionResponse::ECR_Block);
	// 7号全部都碰撞阻塞
	Component->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel7, ECollisionResponse::ECR_Block);

	switch (WaterType)
	{
	case WATER_TYPE_ENUM::WATER_CAN_STEPON:
		Component->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
		Component->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel2, ECollisionResponse::ECR_Block);	//player
		Component->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel3, ECollisionResponse::ECR_Block);	//正常玩家
		Component->SetCollisionResponseToChannel(ECollisionChannel::ECC_GameTraceChannel4, ECollisionResponse::ECR_Block);	//施法玩家
		break;
	case WATER_TYPE_ENUM::WATER_NOT_STEPON:
		Component->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
		Component->SetCollisionResponseToChannel(ECollisionChannel::ECC_Visibility, ECollisionResponse::ECR_Ignore);
		break;
	default:
		break;
	}
}

CONTROL_COMPILE_OPTIMIZE_END	
