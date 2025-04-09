// Fill out your copyright notice in the Description page of Project Settings.

#include "ModifyBoneAnimInstance.h"



TArray<FBoneStruct>& UModifyBoneAnimInstance::GetArrayByType(EBodyPartType type)
{
	if (type == EBodyPartType::Part_Face)
	{
		return FaceBoneArray;
	}
	else
	{
		return BodyBoneArray;
	}
}



void UModifyBoneAnimInstance::InitBoneArray(TArray<FBoneStruct> boneArray, EBodyPartType faceOrBody)
{
	TArray<FBoneStruct>& BoneArray = GetArrayByType(faceOrBody);
	for (auto& bone : boneArray)
	{
		bone.boneIndex = GetSkelMeshComponent()->GetBoneIndex(bone.boneName);
		if (bone.boneIndex > 0)
		{
			BoneArray.Add(bone);
		}
	}
}

