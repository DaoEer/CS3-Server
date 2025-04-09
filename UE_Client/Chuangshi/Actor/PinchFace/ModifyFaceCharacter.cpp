// Fill out your copyright notice in the Description page of Project Settings.

#include "ModifyFaceCharacter.h"
#include "SkeletalMeshRenderData.h"
#include "SkeletalMeshLODRenderData.h"
#include "SkeletalRenderPublic.h"
#include "Components/InputComponent.h"
#include "GameFramework/InputSettings.h"
#include "GameFramework/PlayerInput.h"
#include "GameFramework/SpringArmComponent.h"
#include "Util/CS3Debug.h"
#include "RawIndexBuffer.h"
#include "Component/AppearanceComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Role/RoleStoreInterface.h"
#include "../../Interface/Role/RoleSpaceInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

AModifyFaceCharacter::AModifyFaceCharacter()
{
	CreateRoleMesh();
	InitBaseComponent();
}

void AModifyFaceCharacter::InitBaseComponent()
{
	AppearanceComponent = CreateDefaultSubobject<URoleAppearanceComponent>(TEXT("RoleAppearanceComponent"));
}

void AModifyFaceCharacter::BeginPlay()
{
	Super::BeginPlay();
	//初始化光照功能
	CS3LightComponent = NewObject<UCS3LightComponent>(this, TEXT("CS3LightComponent"));
	CS3LightComponent->RegisterComponent();
	CS3LightComponent->CreateLight();
	CS3LightComponent->SetComponentTickEnabled(false);
	CS3LightComponent->SceneLight->SetVisibility(true);
}

void AModifyFaceCharacter::CreateModel(FString ModelId)
{
	GetAppearanceComponent()->CreateAppearance(ModelId);
}

void AModifyFaceCharacter::CreateStoreRoleModel()
{
	GameObject* RoleEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (RoleEntity)
	{
		FString ModelId = "SK_ShopPerformerPC_M_None";
		int32 Gender = (int32)RoleEntity->GetDefinedProperty(TEXT("gender"));
		if (Gender == 2)///女性
		{
			ModelId = "SK_ShopPerformerPC_F_None";
		}

		FAModelInfo ModelInfo = RoleEntity->GetModelInfo();
		AddShopPreviewPart(ModelInfo);
		GetAppearanceComponent()->CreateAppearanceByModelInfo(ModelId, ModelInfo);
	}
}

void AModifyFaceCharacter::ResetStoreModelPart(MODEL_PART_TYPE PartType)
{
	GameObject* RoleEnfity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
	if (nullptr != RoleEnfity && IsValid(GetAppearanceComponent()))
	{
		FString PartId = RoleEnfity->GetPartIdByType(PartType);
		if (PartType == MODEL_PART_TYPE::MODEL_PART_BODYS_LIGHT)
		{
			ChangeBodyLightEffect(PartId);
		}
		else
		{
			GetAppearanceComponent()->ChangePart(PartType, PartId);
		}
	}
}

void AModifyFaceCharacter::SetupPlayerInputComponent(class UInputComponent* InputCpt)
{
	Super::SetupPlayerInputComponent(InputCpt);
	const UInputSettings* InputSettings = GetDefault<UInputSettings>();
	const FInputAxisKeyMapping turnaxismappingUp(TEXT("MouseScrollUp"), EKeys::MouseScrollUp, 1.0f);
	const FInputAxisKeyMapping turnaxismappingDown(TEXT("MouseScrollDown"), EKeys::MouseScrollDown, -1.0f);
	((UInputSettings*)InputSettings)->AddAxisMapping(turnaxismappingUp);
	((UInputSettings*)InputSettings)->AddAxisMapping(turnaxismappingDown);
	((UInputSettings*)InputSettings)->SaveKeyMappings(); 
	/** BIND Axis */
	InputCpt->BindAxis("MouseScrollUp", this, &AModifyFaceCharacter::MouseScrolMoveCameraArm);
	InputCpt->BindAxis("MouseScrollDown", this, &AModifyFaceCharacter::MouseScrolMoveCameraArm);
}

void AModifyFaceCharacter::OnCreateModelOver()
{
	Super::OnCreateModelOver();
	if (IsValid(GetBaseAnimInstance()))
	{
		CheckPartHideByAction(GetBaseAnimInstance()->GetCurPlayActionData());
	}
}

int AModifyFaceCharacter::MouseLineTrace(struct FHitResult& OutHit, const FVector& Start, const FVector& End, ECollisionChannel TraceChannel)
{
	UWorld* World = GetWorld();
	FCollisionQueryParams Params = FCollisionQueryParams::DefaultQueryParam;
	Params.bReturnFaceIndex = true;
	Params.bTraceComplex = true;
	//Params.bTraceAsyncScene = true;

	World->LineTraceSingleByChannel(OutHit, Start, End, TraceChannel, Params);
	return OutHit.FaceIndex;
}

bool AModifyFaceCharacter::GetUVFromFaceIndex(struct FMATERIAL_FACE_HIT_RESULT& OutMaterial, const FHitResult& OutHit, USkeletalMeshComponent* SK_Mesh)
{
	FSkeletalMeshRenderData& SkelMeshRenderData = SK_Mesh->MeshObject->GetSkeletalMeshRenderData();
	const FSkeletalMeshLODRenderData& LODData = SkelMeshRenderData.LODRenderData[0];
	const FMultiSizeIndexContainer& IndexBufferContainer = LODData.MultiSizeIndexContainer;
	const FRawStaticIndexBuffer16or32Interface& ModelIndexBuffer = *LODData.MultiSizeIndexContainer.GetIndexBuffer();
	if (ModelIndexBuffer.Num() <= 0 && OutHit.FaceIndex > -1)
	{
		return false;
	}
	int32 OutFaceIndex = OutHit.FaceIndex;

	int32 VerIndex0 = ModelIndexBuffer.Get(OutFaceIndex * 3);
	int32 VerIndex1 = ModelIndexBuffer.Get(OutFaceIndex * 3 + 1);
	int32 VerIndex2 = ModelIndexBuffer.Get(OutFaceIndex * 3 + 2);

	FVector2D Vert0UV = SK_Mesh->GetVertexUV(VerIndex0, 0);
	FVector2D Vert1UV = SK_Mesh->GetVertexUV(VerIndex1, 0);
	FVector2D Vert2UV = SK_Mesh->GetVertexUV(VerIndex2, 0);

	OutMaterial.UVCoordinates = (Vert0UV + Vert1UV + Vert2UV) / 3.0;
	int32 VertexIndex;
	int32 Section;
	bool bOutHasExtraBoneInfluences = false;
	LODData.GetSectionFromVertexIndex(OutHit.FaceIndex, Section, VertexIndex);
	OutMaterial.MaterialIndex = LODData.RenderSections[Section].MaterialIndex;
	if (OutMaterial.MaterialIndex == -1)
	{
		return false;
	}
	return true;
}

FColor AModifyFaceCharacter::GetColorFromUV(UTexture2D* Texture, FVector2D UVCoordinates)
{
	FTexture2DMipMap* MipMap = &Texture->PlatformData->Mips[0];
	FByteBulkData* RawImageData = &MipMap->BulkData;
	FColor* FormatedImageData = static_cast<FColor*>(RawImageData->Lock(LOCK_READ_ONLY));

	uint32 Width = MipMap->SizeX;
	uint32 Height = MipMap->SizeY;


	uint32 CoordX = (uint32)((UVCoordinates.X - FMath::FloorToFloat(UVCoordinates.X)) * Width);
	uint32 CoordY = (uint32)((UVCoordinates.Y - FMath::FloorToFloat(UVCoordinates.Y)) * Height);

	FColor PixelColor;

	if (CoordX < Width && CoordY < Height)
	{
		PixelColor = FormatedImageData[CoordY * Width + CoordX];
	}

	RawImageData->Unlock();
	return PixelColor;
}

FVector AModifyFaceCharacter::MoveCameraArm(USpringArmComponent* Arm, float WheelValue, float Delta)
{
	float Length = Arm->TargetArmLength;
	FVector Loc = Arm->RelativeLocation;

	int State = GetArmState(Arm);

	if (State == -1)
	{
		CameraAutoMove = true;
	}
	else
	{
		CameraAutoMove = false;
	}

	if (!CameraAutoMove && !ForceMoving)
	{
		Arm->TargetArmLength = Length + WheelValue;
		AnimState = State;

		if (Arm->TargetArmLength < CameraPosArray[State].Dis)
			AnimState = State - 1;
		if (Arm->TargetArmLength > CameraPosArray[State].Dis + 25)
			AnimState = State + 1;

		AnimState = FMath::Clamp(AnimState, 0, 1);
		CurLoc = Loc;
		CurLength = Length;
	}
	else
	{
		FVector AnimLoc = CameraPosArray[AnimState].Loc;
		float AnimLength = CameraPosArray[AnimState].Dis + 5;
		
		Loc = (AnimLoc - CurLoc) * Delta + Loc;
		Arm->TargetArmLength = (AnimLength - CurLength) * Delta + Length;

		if (FMath::Abs(AnimLoc.Z - Loc.Z) < 10.0f || FMath::Abs(AnimLength - Length) < 5.f)
		{
			CurLoc = Loc;
			CurLength = Length;
			ForceMoving = false;
		}
	}
	return Loc;
}

void AModifyFaceCharacter::RotateCamera(float DeltaAngle, USpringArmComponent* Arm)
{
	FRotator Rot = FRotator(DeltaAngle, 0, 0);
	if ((Arm->GetComponentRotation().Pitch > 20 && DeltaAngle > 0) || (Arm->GetComponentRotation().Pitch < -40 && DeltaAngle < 0))
		return;
	Arm->AddLocalRotation(Rot);
}

FTransform AModifyFaceCharacter::ConverTransform(FVector Offset, int BtnType, int Mode)
{
	FTransform Res = FTransform();
	switch (BtnType)
	{
	case 0:
	{
		Res.SetLocation(Offset * 0.01f);
		break;
	}
	case 1:
	{
		FRotator Rot = FRotator(-Offset.X * 0.1f, Offset.Y * 0.1f, -Offset.Z * 0.3f);
		Res.SetRotation(FQuat(Rot));
		break;
	}
	case 2:
	{
		if (Mode == 0)
		{
			FVector Scl = FVector(1 + Offset.X*0.005, 1 + Offset.Z*0.005, 1 + Offset.Y*0.005);
			//FVector scl = FVector(1 , 1 + offset.Z*0.005, 1);
			Res.SetScale3D(Scl);
		}
		else
		{
			FVector Loc = FVector(0, 0, Offset.Z*0.02);
			FVector Scl = FVector(1, 1 + Offset.X*0.005, 1 + Offset.X*0.005);
			Res.SetLocation(Loc);
			Res.SetScale3D(Scl);
		}
		break;
	}
	}
	return Res;
}

void AModifyFaceCharacter::ModifyFaceChangePart(MODEL_PART_TYPE InPos, FString PartID)
{
	ChangeModelPart(InPos, PartID);
}

void AModifyFaceCharacter::PlayAction_BP(FName ActionName)
{
	PlayAction(ActionName);
}

void AModifyFaceCharacter::SetBackAdornLoaction(FVector deviation)
{
	UMeshComponent* backadorn = GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_BACK_ADORN);
	if (backadorn)
	{
		backadorn->SetRelativeLocation(deviation);
	}
}

void AModifyFaceCharacter::OnBackWorldLevel()
{
	int32 EntityID = UGolbalBPFunctionLibrary::GetPlayerID();
	URoleSpaceInterface* RoleSpaceInterface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface"), EntityID));
	if (RoleSpaceInterface)
	{
		KBEngine::Entity* entity = RoleSpaceInterface->GetEntity();
		if (entity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::RPC_RequestGoToSpace : entity!"));
			return;
		}
		FVector entityDirection = entity->LocalDirection(); 
		FVector entityLocation = entity->LocalPosition();
		FString ReviveSpace = UGolbalBPFunctionLibrary::GetSpaceData("SPACE_SCRIPT_ID");
		RoleSpaceInterface->RPC_RequestGoToSpace(ReviveSpace, entityLocation, entityDirection);
	}
}

int AModifyFaceCharacter::GetActorGender()
{
	int32 EntityID = UGolbalBPFunctionLibrary::GetPlayerID();
	URoleSpaceInterface* RoleSpaceInterface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface"), EntityID));
	if (RoleSpaceInterface)
	{
		KBEngine::Entity* entity = RoleSpaceInterface->GetEntity();
		return entity->GetDefinedProperty("gender");
	}
	return 0;
}

int32 AModifyFaceCharacter::GetArmState(USpringArmComponent* Arm)
{
	float Length = Arm->TargetArmLength;
	for (int i = 0; i < CameraPosArray.Num(); i++)
	{
		if (Length < CameraPosArray[i].Dis + 25 && Length > CameraPosArray[i].Dis)
			return i;
	}
	return -1;
}

void AModifyFaceCharacter::AddShopPreviewPart(FAModelInfo& ModelInfo)
{
	TMap<MODEL_PART_TYPE, FString> PartMap;
	URoleStoreInterface * RoleStoreInterface = Cast<URoleStoreInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStoreInterface"), 0));
	if (IsValid(RoleStoreInterface))
	{
		PartMap = RoleStoreInterface->GetStoreTryAppearancePart();
	}
	for (TPair<MODEL_PART_TYPE, FString> Part : PartMap)
	{
		if (Part.Value.IsEmpty())
		{
			continue;
		}
		MODEL_PART_TYPE PartType = Part.Key;
		if (PartType == MODEL_PART_TYPE::MODEL_PART_COATS)
		{
			ModelInfo.CoatModel = Part.Value;
		}
		else if (PartType == MODEL_PART_TYPE::MODEL_PART_HAIRS)
		{
			ModelInfo.HairModel = Part.Value;
		}
		else if (PartType == MODEL_PART_TYPE::MODEL_PART_ADORN)
		{
			ModelInfo.AdornModel = Part.Value;
		}
		else if (PartType == MODEL_PART_TYPE::MODEL_PART_HEAD_ADORN)
		{
			ModelInfo.HeadAdornModel = Part.Value;
		}
		else if (PartType == MODEL_PART_TYPE::MODEL_PART_FACE_ADORN)
		{
			ModelInfo.FaceAdornModel = Part.Value;
		}
		else if (PartType == MODEL_PART_TYPE::MODEL_PART_BACK_ADORN)
		{
			ModelInfo.BackAdornModel = Part.Value;
		}
		else if (PartType == MODEL_PART_TYPE::MODEL_PART_WAIST_ADORN)
		{
			ModelInfo.WaistAdornModel = Part.Value;
		}
		else if (PartType == MODEL_PART_TYPE::MODEL_PART_CLOAK)
		{
			ModelInfo.CloakModel = Part.Value;
		}
	}
}


CONTROL_COMPILE_OPTIMIZE_END