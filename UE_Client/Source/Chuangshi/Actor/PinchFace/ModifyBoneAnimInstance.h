// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Animation/AnimInstance.h"
#include "BoneStruct.h"
#include "ModifyBoneAnimInstance.generated.h"

/*
* 文件名称：ModifyBoneAnimInstance.h
* 功能说明：
* 文件作者：luocheng
* 目前维护：wuxiaoou
* 创建时间：2016-12-14
*/

/**
* @class	UModifyBoneAnimInstance
*
* @brief	支持表现骨骼修改的动画
*
* @date	2017/3/25
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UModifyBoneAnimInstance : public UAnimInstance
{
	GENERATED_BODY()
public:

	/**
	 * @fn	TArray<FBoneStruct>& GetArrayByType(EBodyPartType type);
	 *
	 * @brief	根据类型获取骨骼数组.
	 *
	 * @date	2017/3/25
	 *
	 * @param	type	: 部位类型.
	 *
	 * @return	对应部位的骨骼数据数据.
	 */

	TArray<FBoneStruct>& GetArrayByType(EBodyPartType type);

	/**
	 * @fn	virtual void InitBoneArray(TArray<FBoneStruct> boneArray, EBodyPartType faceOrBody);
	 *
	 * @brief	初始化骨骼节点 : 用于已有骨骼改变数据，用于初始化表现.
	 *
	 * @date	2017/3/25
	 *
	 * @param	parameter1	骨骼节点数据列表.
	 * @param	parameter2	骨骼类型.
	 */

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		virtual void InitBoneArray(TArray<FBoneStruct> boneArray, EBodyPartType faceOrBody);

protected:
	UPROPERTY()
		TArray<FBoneStruct> FaceBoneArray;  ///< Array of face bones,脸部骨骼数据

	UPROPERTY()
		TArray<FBoneStruct> BodyBoneArray;  ///< Array of body bones,身体骨骼数据



	
};
