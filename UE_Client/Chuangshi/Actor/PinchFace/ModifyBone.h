// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "BoneStruct.h"
#include "AnimGraphRuntime/Public/BoneControllers/AnimNode_SkeletalControlBase.h"
#include "GameData/ModifyFaceData.h"
#include "ModifyBone.generated.h"

/*
* 文件名称：ModifyBone.h
* 功能说明：修改动画骨骼位置偏移
* 文件作者：luocheng
* 目前维护：wuxiaoou
* 创建时间：2016-08-31
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FModifyBone :public FAnimNode_SkeletalControlBase
{
	GENERATED_BODY()

public:

	//UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Links)
	//FComponentSpacePoseLink ComponentPose; 

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Translation)
		TEnumAsByte<enum EBoneControlSpace> TranslationSpace;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Rotation)
		TEnumAsByte<enum EBoneControlSpace> RotationSpace;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Scale)
		TEnumAsByte<enum EBoneControlSpace> ScaleSpace;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Variable)
		EMODIFY_TYPE ModifyType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Variable)
		FTransform ModifyTransform;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Variable)
		FName BoneName;

	FModifyBone();


	virtual void Initialize_AnyThread(const FAnimationInitializeContext& Context) override;
	virtual void CacheBones_AnyThread(const FAnimationCacheBonesContext& Context)  override;
	virtual bool IsValidToEvaluate(const USkeleton* Skeleton, const FBoneContainer& RequiredBones);
	virtual void EvaluateSkeletalControl_AnyThread(FComponentSpacePoseContext& Output, TArray<FBoneTransform>& OutBoneTransforms) override;
};
