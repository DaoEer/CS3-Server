// Fill out your copyright notice in the Description page of Project Settings.

#include "PinchFaceCharacter.h"
#include "CoreMinimal.h"
#include "SkeletalMeshTypes.h"
#include "Kismet/KismetMathLibrary.h"
#include "Component/SpringArmComponentEX.h"
#include "Components/SkeletalMeshComponent.h"
#include "Camera/CameraComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"

APinchFaceCharacter::APinchFaceCharacter()
{
	CharacterClassName = TEXT("PinchFaceCharacter");
	PrimaryActorTick.bCanEverTick = true;
}


void APinchFaceCharacter::Tick(float DeltaSeconds)
{
	if (bInintlize)
	{
		Super::Tick(DeltaSeconds);
	}
}


void APinchFaceCharacter::Init(FROLEINFO roleInfo)
{
	RoleInfo = roleInfo;
	
	OnInitlizeFinish();
}

void APinchFaceCharacter::OnInitlizeFinish_Implementation()
{
	//标记初始化完成
	bInintlize = true;
}


#pragma region Line Trace


bool APinchFaceCharacter::LineTrace(struct FHitResult& OutHit, const FVector& Start, const FVector& End, ECollisionChannel TraceChannel)
{
	UWorld* world = GetWorld();
	FCollisionQueryParams Params = FCollisionQueryParams::DefaultQueryParam;
	Params.bReturnFaceIndex = true;
	Params.bTraceComplex = true;
	//Params.bTraceAsyncScene = true;

	return world->LineTraceSingleByChannel(OutHit, Start, End, TraceChannel, Params);
}

TArray<FString> APinchFaceCharacter::GetBonesName(USkeletalMeshComponent* skMesh)
{
	TArray<FString> NameList;
	//TODO:等煜鹏修复
	/*
	FSkeletalMeshResource* skeletalResource = skMesh->GetSkeletalMeshResource();
	for (int i = 0, len = skMesh->GetNumBones(); i < len; ++i)
	{
		NameList.Add(skMesh->GetBoneName(i).ToString());
	}
	*/
	return NameList;
}

//根据射线检测结果获取碰撞材质（uv坐标、材质索引）
bool APinchFaceCharacter::GetUVFromFaceIndex(struct FMaterialHitResult& OutMaterial, const FHitResult& OutHit, USkeletalMeshComponent* skMesh)
{
	//TODO:等煜鹏修复
	/*
	FSkeletalMeshResource* skeletalResource = skMesh->GetSkeletalMeshResource();
	if (!skeletalResource || skeletalResource->LODModels.Num() <= 0)
		return false;
	
	const FStaticLODModel& LODModel = skeletalResource->LODModels[0];

	const FRawStaticIndexBuffer16or32Interface* modelIndexBuffer = LODModel.MultiSizeIndexContainer.GetIndexBuffer();
	uint32 VerIndex0 = modelIndexBuffer->Get((uint32)OutHit.FaceIndex * 3);
	uint32 VerIndex1 = modelIndexBuffer->Get((uint32)OutHit.FaceIndex * 3 + 1);
	uint32 VerIndex2 = modelIndexBuffer->Get((uint32)OutHit.FaceIndex * 3 + 2);

	FVector Vert0Pos = LODModel.VertexBufferGPUSkin.GetVertexPositionSlow(VerIndex0);
	FVector Vert1Pos = LODModel.VertexBufferGPUSkin.GetVertexPositionSlow(VerIndex1);
	FVector Vert2Pos = LODModel.VertexBufferGPUSkin.GetVertexPositionSlow(VerIndex2);

	FVector2D Vert0UV = LODModel.VertexBufferGPUSkin.GetVertexUV(VerIndex0, 0);
	FVector2D Vert1UV = LODModel.VertexBufferGPUSkin.GetVertexUV(VerIndex1, 0);
	FVector2D Vert2UV = LODModel.VertexBufferGPUSkin.GetVertexUV(VerIndex2, 0);

	FVector ComponentLocation = skMesh->GetComponentLocation();
	FRotator ComponentRotation = skMesh->GetComponentRotation();
	FVector ComponentScale = skMesh->GetComponentScale();

	FVector LocalImpactPoint = ComponentRotation.UnrotateVector(OutHit.ImpactPoint - ComponentLocation) / ComponentScale;

	// Determine the barycentric coordinates
	FVector u = Vert1Pos - Vert0Pos;
	FVector v = Vert2Pos - Vert0Pos;
	FVector w = LocalImpactPoint - Vert0Pos;


	FVector vCrossW = FVector::CrossProduct(v, w);
	FVector vCrossU = FVector::CrossProduct(v, u);

	if (FVector::DotProduct(vCrossW, vCrossU) < 0.0f)
	{
		//return false;
	}

	FVector uCrossW = FVector::CrossProduct(u, w);
	FVector uCrossV = FVector::CrossProduct(u, v);

	if (FVector::DotProduct(uCrossW, uCrossV) < 0.0f)
	{
		//return false;
	}

	float denom = uCrossV.Size();
	float b1 = vCrossW.Size() / denom;
	float b2 = uCrossW.Size() / denom;
	float b0 = 1.0f - b1 - b2;

	// Determine the hit UV.
	float hitU = b0 * Vert0UV.X + b1 * Vert1UV.X + b2 * Vert2UV.X;
	float hitV = b0 * Vert0UV.Y + b1 * Vert1UV.Y + b2 * Vert2UV.Y;

	//OutMaterial.UVCoordinates = FVector2D(hitU, hitV);
	OutMaterial.UVCoordinates = (Vert0UV + Vert1UV + Vert2UV) / 3.0;

	// Loop through the LOD's sections to find the one that contains the face that was hit.
	for (int32 i = 0; i < LODModel.Sections.Num(); i++)
	{
		uint32 MinVertIndex = LODModel.Sections[i].BaseVertexIndex;
		uint32 MaxVertIndex = LODModel.Sections[i].BaseVertexIndex + LODModel.Sections[i].GetNumVertices();

		if (FMath::IsWithinInclusive(VerIndex0, MinVertIndex, MaxVertIndex) &&
			FMath::IsWithinInclusive(VerIndex1, MinVertIndex, MaxVertIndex) &&
			FMath::IsWithinInclusive(VerIndex2, MinVertIndex, MaxVertIndex))
		{
			OutMaterial.MaterialIndex = LODModel.Sections[i].MaterialIndex;
			break;
		}
	}

	if (OutMaterial.MaterialIndex == -1)
	{
		return false;
	}

	return true;
	*/
	return false;
}

void APinchFaceCharacter::InitLimitBones(const TArray<FBoneLimit> limitArray, EBodyPartType boneType)
{
	auto anim = GetMesh()->GetAnimInstance();
	UPinchFaceAnimInstance* pinchAnim = Cast<UPinchFaceAnimInstance>(anim);
	if (IsValid(pinchAnim))
	{
		pinchAnim->SetLimitBoneArray(limitArray, boneType);
	}
}


void APinchFaceCharacter::RegisterMotifyBones(const TArray<FBONE_ATTR> boneArray, EBodyPartType boneType)
{
	auto anim = GetMesh()->GetAnimInstance();
	UPinchFaceAnimInstance* pinchAnim = Cast<UPinchFaceAnimInstance>(anim);
	if (IsValid(pinchAnim))
	{
		for (auto& bone : boneArray)
		{
			pinchAnim->AddModifyBone(bone.BoneName, boneType);
		}
	}
}

void APinchFaceCharacter::InitBones(TArray<FBoneStruct> faceBoneArray, TArray<FBoneStruct> bodyBoneArray)
{
	UModifyBoneAnimInstance* anim = Cast<UModifyBoneAnimInstance>(GetMesh()->GetAnimInstance());
	if (anim)
	{
		//初始化脸部骨骼
		anim->InitBoneArray(faceBoneArray, EBodyPartType::Part_Face);

		//初始化身体骨骼
		anim->InitBoneArray(bodyBoneArray, EBodyPartType::Part_Body);
	}
}

//根据获取的UV坐标获取遮罩图对应的颜色
FColor APinchFaceCharacter::GetColorFromUV(UTexture2D* txt, FVector2D UVCoordinates)
{
	FTexture2DMipMap* MyMipMap = &txt->PlatformData->Mips[0];
	FByteBulkData* RawImageData = &MyMipMap->BulkData;
	FColor* FormatedImageData = static_cast<FColor*>(RawImageData->Lock(LOCK_READ_ONLY));

	uint32 width = MyMipMap->SizeX, height = MyMipMap->SizeY;

	uint32 coordx = (uint32)((UVCoordinates.X - FMath::FloorToFloat(UVCoordinates.X)) * width);
	uint32 coordy = (uint32)((UVCoordinates.Y - FMath::FloorToFloat(UVCoordinates.Y)) * height);

	FColor PixelColor;

	if (coordx < width && coordy < height)
	{
		PixelColor = FormatedImageData[coordy * width + coordx];
	}

	RawImageData->Unlock();

	return PixelColor;
}
#pragma endregion


#pragma region Camera

FVector APinchFaceCharacter::MoveCameraArm(USpringArmComponent* arm, float wheelValue, float delta)
{
	float length = arm->TargetArmLength;
	FVector loc = arm->RelativeLocation;

	int state = GetArmState(arm);

	if (state == -1)
	{
		camerAutoMove = true;
	}
	else
	{
		camerAutoMove = false;
	}

	if (!camerAutoMove && !forceMoving)
	{
		UGolbalBPFunctionLibrary::SetCameraTargetArmLength(arm, length + wheelValue);
		this->AnimState = state;

		if (arm->TargetArmLength < CameraPosArray[state].dis)
		{
			this->AnimState = state - 1;
		}

		if (arm->TargetArmLength > CameraPosArray[state].dis + 200)
		{
			this->AnimState = state + 1;
		}
		this->AnimState = FMath::Clamp(this->AnimState, 0, 2);
		curLoc = loc;
		curLength = length;
	}
	else
	{
		FVector animLoc = CameraPosArray[this->AnimState].loc;
		float animLength = CameraPosArray[this->AnimState].dis + 100;

		loc = (animLoc - curLoc) * delta + loc;
		UGolbalBPFunctionLibrary::SetCameraTargetArmLength(arm,(animLength - curLength) * delta + length);

		if (FMath::Abs(animLoc.Z - loc.Z) < 10.0f || FMath::Abs(animLength - length) < 10.0f)
		{
			curLoc = loc;
			curLength = length;
			forceMoving = false;
		}
	}
	return loc;
}


void APinchFaceCharacter::RotateCamera(float deltaAngle, USpringArmComponent* arm)
{
	FRotator rot = FRotator(deltaAngle, 0, 0);
	if ((arm->GetComponentRotation().Pitch > 20 && deltaAngle > 0) || (arm->GetComponentRotation().Pitch < -40 && deltaAngle < 0))
	{
		return;
	}
	arm->AddLocalRotation(rot);
}

void APinchFaceCharacter::ForceMovingCamera(int animState, USpringArmComponent* arm)
{
	this->AnimState = animState;
	curLoc = arm->RelativeLocation;
	curLength = arm->TargetArmLength;
	forceMoving = true;
}


FRotator APinchFaceCharacter::LookAtCamera(USkeletalMeshComponent* skMesh, UCameraComponent* camera, FVector start, FRotator curRotate, float delta)
{
	FVector end = camera->GetComponentLocation();
	FRotator rot = UKismetMathLibrary::FindLookAtRotation(start, end);
	FRotator anim = FRotator(0, 0, 0);
	anim.Roll = -rot.Pitch;

	float animYaw = -skMesh->GetComponentRotation().Yaw;

	if (FMath::Abs(animYaw) < 120)
	{
		anim.Yaw = animYaw;
	}

	FRotator res = RotateToAngle(anim, curRotate, delta);
	return res;
}


FRotator APinchFaceCharacter::RotateHead(USkeletalMeshComponent* skMesh, UCameraComponent* camera, FRotator curRotate, float delta)
{
	float animPitch = camera->GetComponentRotation().Pitch;
	float animYaw = -skMesh->GetComponentRotation().Yaw;

	FRotator anim = FRotator(0, 0, 0);

	if (FMath::Abs(animPitch) < 120)
	{
		anim.Roll = animPitch;
	}

	if (FMath::Abs(animYaw) < 120)
	{
		anim.Yaw = animYaw;
	}

	return RotateToAngle(anim, curRotate, delta);
}


FTransform APinchFaceCharacter::ConverTransform(FVector offset, int btnType, int mode)
{
	FTransform res;

	switch (btnType)
	{
		case 0://位移
		{
			res.SetLocation(offset * 0.01f);
			break;
		}
		case 1://旋转
		{
			FRotator rot = FRotator(-offset.X*0.1, offset.Y*0.1, -offset.Z*0.3);
			res.SetRotation(FQuat(rot));
			break;
		}
		case 2://缩放
		{
			if (mode == 0)
			{
				FVector scl = FVector(1 + offset.X*0.005, 1 + offset.Z*0.005, 1 + offset.Y*0.005);
				//FVector scl = FVector(1 , 1 + offset.Z*0.005, 1);
				res.SetScale3D(scl);
			}
			else
			{
				FVector loc = FVector(0, 0, offset.Z*0.02);
				FVector scl = FVector(1, 1 + offset.X*0.005, 1 + offset.X*0.005);
				res.SetLocation(loc);
				res.SetScale3D(scl);
			}
			break;
		}
	}
	return res;
}

#pragma endregion

FRotator APinchFaceCharacter::RotateToAngle(FRotator anim, FRotator cur, float delta)
{
	anim.Pitch = FMath::Clamp(anim.Pitch, -60.0f, 60.0f);
	anim.Roll = FMath::Clamp(anim.Roll, -60.0f, 60.0f);
	anim.Yaw = FMath::Clamp(anim.Yaw, -60.0f, 60.0f);

	FRotator res = cur + (anim - cur) * delta;
	return res;
}

int APinchFaceCharacter::GetArmState(USpringArmComponent * arm)
{
	float length = arm->TargetArmLength;

	for (int i = 0; i < CameraPosArray.Num(); i++)
	{
		if (length < CameraPosArray[i].dis + 200 && length > CameraPosArray[i].dis)
		{
			return i;
		}
	}

	return -1;
}

