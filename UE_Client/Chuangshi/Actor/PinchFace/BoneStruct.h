// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "BoneStruct.generated.h"

/*
* 文件名称：BoneStruct.h
* 功能说明：
* 文件作者：luocheng
* 目前维护：wuxiaoou
* 创建时间：2016-12-07
*/

/**
* @struct	FBoneStruct
*
* @brief	骨骼变换数据
*
* @date	2017/3/25
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBoneStruct
{
	GENERATED_BODY()

public:

	/**
	 * @fn	friend bool FBoneStruct::operator<(const FBoneStruct& a, const FBoneStruct& b)
	 *
	 * @brief	小于比较运算符.
	 *
	 * @date	2017/3/25
	 *
	 * @param	a	The first instance to compare.
	 * @param	b	The second instance to compare.
	 *
	 * @return	True if the first parameter is less than the second.
	 */

	friend bool operator<(const FBoneStruct& a, const FBoneStruct& b)
	{
		return a.boneIndex < b.boneIndex;
	}

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Name)
		FName boneName; ///< 骨骼名称

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Transform)
		FTransform transform;   ///< 骨骼偏移

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Scale)
		FVector alpha = FVector(1, 1, 1);   ///< 透明度

	int boneIndex = -1; ///< 骨骼索引

	int parentIndex = -1;   ///< 骨骼父节点索引

	FTransform compTrans;   ///< 组件transform

};



/**
* @struct	FBoneLimit
*
* @brief	骨骼限制数据
*
* @date	2017/3/25
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBoneLimit
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Name)
	FName boneName; ///< 骨骼名称

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Translation)
		bool doTranslation = true;  ///< 是否可调整位置

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Rotation)
		bool doRotation = true; ///< 是否可调整旋转

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Scale)
		bool doScaling = true;  ///< 是否可调整缩放

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Scale)
	FTransform MinTransform;	///< 最小偏移矩阵
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Scale)
	FTransform MaxTransform;	///< 最大偏移矩阵

};


/**
* @struct	FBoneOffsetStruct
*
* @brief	骨骼偏移数据
*
* @date	2017/3/25
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBoneOffsetStruct
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly)
		float MinValue = 0; ///< The minimum value

	UPROPERTY(BlueprintReadOnly)
		float MaxValue = 1; ///< The maximum value

	UPROPERTY(BlueprintReadOnly)
		float CurValue = 0; ///< The current value
};

/**
* @struct	FBoneOffsetStruct3
*
* @brief	骨骼偏移数据
*
* @date	2017/3/25
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBoneOffsetStruct3
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly)
	FBoneOffsetStruct X;	

	UPROPERTY(BlueprintReadOnly)
	FBoneOffsetStruct Y;	

	UPROPERTY(BlueprintReadOnly)
	FBoneOffsetStruct Z;	
};


/**
* @struct	FBoneColorStruct
*
* @brief	骨骼颜色数据
*
* @date	2017/3/25
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBoneColorStruct
{
	GENERATED_BODY()

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Name)
		FName boneName; ///< 骨骼名称

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Name)
		float boneColor;	///< 骨骼颜色
};



/**
* @enum	EBodyPartType
*
* @brief	部件类型
*/
UENUM(BlueprintType)
enum class EBodyPartType : uint8
{
	Part_Face UMETA(DisplayName = "face"), ///< 脸
	Part_Body UMETA(DisplayName = "body"),///< 身体
	Part_Pose UMETA(DisplayName = "pose"),///< 姿势
};

/**
* @struct	FFloatVectorStruct
*
* @brief	浮点Vector结构体
*
* @date	2017/3/25
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFloatVectorStruct
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Variable)
		float	dis;	///< The distance，距离

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Variable)
		FVector loc;	///< The location
};


/**
* @struct	FBONE_ATTR
*
* @brief	骨骼配置属性
*
* @date	2017/3/25
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBONE_ATTR
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FName BoneName; ///< 骨骼名称

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int Color = -1; ///< 骨骼对应遮罩颜色

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FName SymBone;  ///< 骨骼同步位置骨骼名称
};