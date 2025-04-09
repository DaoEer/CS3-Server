// Fill out your copyright notice in the Description page of Project Settings.

#include "ModifyBone.h"
#include "ModifyBoneAnimInstance.h"
#include "Animation/AnimNodeBase.h"
#include "Animation/AnimInstanceProxy.h"
#include "AnimGraphRuntime/Public/BoneControllers/AnimNode_SkeletalControlBase.h"
#include "AnimationRuntime.h"
#include "Chuangshi.h"
#include "GameData/ModifyFaceData.h"
#include "Manager/ModifyFaceManager.h"
#include "BoneContainer.h"
#include "BonePose.h"



FModifyBone::FModifyBone()
	: TranslationSpace(BCS_ComponentSpace)
	, RotationSpace(BCS_ComponentSpace)
	, ScaleSpace(BCS_ComponentSpace)
{

}

void FModifyBone::Initialize_AnyThread(const FAnimationInitializeContext& Context)
{
	ComponentPose.Initialize(Context);
}

void FModifyBone::CacheBones_AnyThread(const FAnimationCacheBonesContext& Context)
{

	InitializeBoneReferences(Context.AnimInstanceProxy->GetRequiredBones());
	ComponentPose.CacheBones(Context);
}

void FModifyBone::EvaluateSkeletalControl_AnyThread(FComponentSpacePoseContext& Output, TArray<FBoneTransform>& OutBoneTransforms)
{
	check(OutBoneTransforms.Num() == 0);
	if (!Output.Pose.GetPose().IsValid())return;
	const FBoneContainer& BoneContainer = Output.Pose.GetPose().GetBoneContainer();
	if (!BoneContainer.IsValid()) return;
	AGameCharacter* GameCharacter =  Cast<AGameCharacter>(Output.AnimInstanceProxy->GetSkelMeshComponent()->GetOwner()) ;
	if (!GameCharacter->IsValidLowLevel())return;
	TArray<FMODIFY_FACE_DATA>& Bones = GameCharacter->ModifyFaceDatas;
	if (!IsValid(UGolbalBPFunctionLibrary::ModifyFaceManager())&& Bones.Num()<0) return;
	if (GameCharacter->bIsGetBone)
	{
		for (int32 i = 0; i < Bones.Num(); ++i)
		{
			FBoneReference BoneRef;
			BoneRef.BoneName = Bones[i].BoneName;
			if (BoneRef.BoneName.IsNone())continue;
			BoneRef.BoneIndex = Output.AnimInstanceProxy->GetSkelMeshComponent()->GetBoneIndex(BoneRef.BoneName);
			if (BoneRef.BoneIndex < 0)
				continue;
			if (!BoneContainer.IsValid())
				continue;
			BoneRef.Initialize(BoneContainer);
			FCompactPoseBoneIndex CompactPoseBoneToModify = BoneRef.GetCompactPoseIndex(BoneContainer);

			FTransform NewBoneTM = Output.Pose.GetComponentSpaceTransform(CompactPoseBoneToModify);
			FTransform ComponentTransform = Output.AnimInstanceProxy->GetComponentTransform();
			// Convert to Bone Space.
			FAnimationRuntime::ConvertCSTransformToBoneSpace(ComponentTransform, Output.Pose, NewBoneTM, CompactPoseBoneToModify, ScaleSpace);
			NewBoneTM.SetScale3D(NewBoneTM.GetScale3D() * Bones[i].BoneTrans.GetScale3D());
			// Convert back to Component Space.
			FAnimationRuntime::ConvertBoneSpaceTransformToCS(ComponentTransform, Output.Pose, NewBoneTM, CompactPoseBoneToModify, ScaleSpace);

			FAnimationRuntime::ConvertCSTransformToBoneSpace(ComponentTransform, Output.Pose, NewBoneTM, CompactPoseBoneToModify, RotationSpace);
			const FQuat BoneQuat(Bones[i].BoneTrans.GetRotation());
			NewBoneTM.SetRotation(BoneQuat * NewBoneTM.GetRotation());
			// Convert back to Component Space.
			FAnimationRuntime::ConvertBoneSpaceTransformToCS(ComponentTransform, Output.Pose, NewBoneTM, CompactPoseBoneToModify, RotationSpace);

			// Convert to Bone Space.
			FAnimationRuntime::ConvertCSTransformToBoneSpace(ComponentTransform, Output.Pose, NewBoneTM, CompactPoseBoneToModify, TranslationSpace);
			NewBoneTM.AddToTranslation(Bones[i].BoneTrans.GetTranslation());
			// Convert back to Component Space.
			FAnimationRuntime::ConvertBoneSpaceTransformToCS(ComponentTransform, Output.Pose, NewBoneTM, CompactPoseBoneToModify, TranslationSpace);

			if (BoneContainer.IsValid()&&BoneRef.IsValidToEvaluate() && BoneRef.HasValidSetup() && BoneRef.GetCompactPoseIndex(BoneContainer) != INDEX_NONE )
			{
				OutBoneTransforms.Add(FBoneTransform(BoneRef.GetCompactPoseIndex(BoneContainer), NewBoneTM));
			}
		}
		OutBoneTransforms.Sort([](const FBoneTransform& TaskA,const FBoneTransform& TaskB) { return TaskA.BoneIndex < TaskB.BoneIndex; });
	}
}


bool FModifyBone::IsValidToEvaluate(const USkeleton* Skeleton, const FBoneContainer& RequiredBones)
{
	return true;
}