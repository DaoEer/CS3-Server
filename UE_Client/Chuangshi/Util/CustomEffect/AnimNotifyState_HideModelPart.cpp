// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotifyState_HideModelPart.h"
#include "Actor/GameCharacter.h"
#include <time.h>
#include "Util/CS3Debug.h"
#include "GameData/CharacterData.h"
#include "Components/SkeletalMeshComponent.h"



CONTROL_COMPILE_OPTIMIZE_START
UAnimNotifyState_HideModelPart::UAnimNotifyState_HideModelPart()
{
	#if WITH_EDITORONLY_DATA
		NotifyColor = FColor(255, 236, 0, 255);
	#endif // WITH_EDITORONLY_DATA
}

void UAnimNotifyState_HideModelPart::NotifyBegin(class USkeletalMeshComponent * MeshComp, 
	class UAnimSequenceBase * Animation, float TotalDuration)
{
	Super::NotifyBegin(MeshComp, Animation, TotalDuration);

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UAnimNotifyState:  [time=%d,  name=%s,  HideModelPart[begin]]"), clock(), *Animation->GetName());
	AGameCharacter *GameCharacter = Cast<AGameCharacter>(MeshComp->GetOwner());
	if (IsValid(GameCharacter))
	{
		SetPartHideInGame(GameCharacter, true);
	}
}

void UAnimNotifyState_HideModelPart::NotifyTick(class USkeletalMeshComponent * MeshComp, 
	class UAnimSequenceBase * Animation, float FrameDeltaTime)
{
	Super::NotifyTick(MeshComp, Animation, FrameDeltaTime);
}

void UAnimNotifyState_HideModelPart::NotifyEnd(class USkeletalMeshComponent * MeshComp, 
	class UAnimSequenceBase * Animation)
{
	Super::NotifyEnd(MeshComp, Animation);
	
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UAnimNotifyState:  [time=%d,  name=%s,  HideModelPart[end]]"), clock(), *Animation->GetName());
	AGameCharacter *GameCharacter = Cast<AGameCharacter>(MeshComp->GetOwner());
	if (IsValid(GameCharacter))
	{
		SetPartHideInGame(GameCharacter, false);
	}
}

void UAnimNotifyState_HideModelPart::SetPartHideInGame(AGameCharacter *GameCharacter, bool HideInGame)
{
	if (STMesh_DefaultStatic)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_STATIC, HideInGame);
	}
	if (SKMesh_Bodys)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_BODYS, HideInGame);
	}
	if (SKMesh_Heads)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_HEADS, HideInGame);
	}
	if (SKMesh_Suits)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_SUITS, HideInGame);
	}
	if (SKMesh_Hairs)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_HAIRS, HideInGame);
	}
	if (SKMesh_Adorn)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_ADORN, HideInGame);
	}
	if (SKMesh_Hat)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_HAT, HideInGame);
	}
	if (SKMesh_Coats)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_COATS, HideInGame);
	}
	if (SKMesh_Wrist)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_WRIST, HideInGame);
	}
	if (SKMesh_Gloves)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_GLOVES, HideInGame);
	}
	if (SKMesh_Waist)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_WAIST, HideInGame);
	}
	if (SKMesh_Necklace)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_NECKLACE, HideInGame);
	}
	if (SKMesh_L_RING)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_LHAND_RING, HideInGame);
	}
	if (SKMesh_R_RING)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_RHAND_RING, HideInGame);
	}
	if (SKMesh_Pants)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_PANTS, HideInGame);
	}
	if (SKMesh_Shoes)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_SHOES, HideInGame);
	}
	if (SKMesh_Cloak)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_CLOAK, HideInGame);
	}
	if (STMesh_LHweapon)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_LWEAPON, HideInGame);
	}
	if (STMesh_RHweapon)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_RWEAPON, HideInGame);
	}
	if (SKMesh_BHweapon)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_BWEAPON, HideInGame);
	}
	if (SKMesh_FaBao)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_FABAO, HideInGame);
	}
	if (STMesh_S_LHweapon)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_S_LWEAPON, HideInGame);
	}
	if (STMesh_S_RHweapon)
	{
		GameCharacter->SetMeshPartHiddenInGame(MODEL_PART_TYPE::MODEL_PART_S_RWEAPON, HideInGame);
	}
}
CONTROL_COMPILE_OPTIMIZE_END
