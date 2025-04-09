#pragma once
#include "CoreMinimal.h"
#include "ModifyBoneAnimInstance.h"
#include "BoneStruct.h"
#include "Runtime/Engine/Public/BonePose.h"
#include "PinchFaceAnimInstance.generated.h"

/**
* 文件名称：PinchFaceAnimInstance.h
* 功能说明：支持捏脸功能的动画类基类
* 目前维护：wuxiaoou
* 文件作者：luocheng
* 创建时间：2016-08-31
*/

/**
* @enum	EBoneTransType
*
* @brief	骨骼变换类型
*/
UENUM(Blueprintable)
enum class EBoneTransType : uint8
{	
	POS_X			UMETA(DisplayName = "POS_X"),
	POS_Y 			UMETA(DisplayName = "POS_Y"),
	POS_Z 			UMETA(DisplayName = "POS_Z"),
	ROT_X			UMETA(DisplayName = "ROT_X"),
	ROT_Y 			UMETA(DisplayName = "ROT_Y"),
	ROT_Z 			UMETA(DisplayName = "ROT_Z"),
	SCALC_X			UMETA(DisplayName = "SCALC_X"),
	SCALC_Y			UMETA(DisplayName = "SCALC_Y"),
	SCALC_Z 		UMETA(DisplayName = "SCALC_Z"),
};


/**
* @class	UPinchFaceAnimInstance
*
* @brief	捏脸动画模块
*
* @date	2017/3/25
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UPinchFaceAnimInstance : public UModifyBoneAnimInstance
{
	GENERATED_BODY()
public:

	/**
	 * @fn	TArray<FBoneLimit>& GetLimitArrayByType(EBodyPartType type);
	 *
	 * @brief	根据类型获取限制列表.
	 *
	 * @date	2017/3/25
	 */

	UFUNCTION()
		TArray<FBoneLimit>& GetLimitArrayByType(EBodyPartType type);

	/**
	* @fn	virtual void InitBoneArray(TArray<FBoneStruct> boneArray, EBodyPartType faceOrBody) override;
	*
	* @brief	初始化骨骼数组
	*
	* @date	2017/3/25
	*
	* @param	boneArray 	骨骼数组
	* @param	faceOrBody	枚举类型，表示是脸部还是身体
	*/

	//UFUNCTION(BlueprintCallable, Category = PinchFace)
	virtual void InitBoneArray(TArray<FBoneStruct> boneArray, EBodyPartType faceOrBody) override;

	/**
	 * @fn	void SetBoneTransform(FTransform trans, FName boneName, EBodyPartType faceOrBody);
	 *
	 * @brief	设置骨骼数据
	 *
	 * @date	2017/3/25
	 *
	 * @param	trans	偏移
	 * @param	boneName	骨骼名称
	 * @param	faceOrBody	骨骼类型
	 */

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		void SetBoneTransform(FTransform trans, FName boneName, EBodyPartType faceOrBody);

	/**
	 * @fn	UPinchFaceAnimInstance::UFUNCTION(BlueprintCallable, Category = PinchFace) void ResetAllBones(EBodyPartType faceOrBody);
	 *
	 * @brief	重置所有骨骼
	 *
	 * @date	2017/3/25
	 *
	 * @param	faceOrBody	重置骨骼类型
	 */

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		void ResetAllBones(EBodyPartType faceOrBody);

	/**
	 * @fn	void ResetBone(FName boneName, EBodyPartType faceOrBody);
	 *
	 * @brief	重置骨骼
	 *
	 * @date	2017/3/25
	 *
	 * @param	boneName	重置骨骼名称
	 * @param	faceOrBody	重置骨骼类型
	 */

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		void ResetBone(FName boneName, EBodyPartType faceOrBody);

	/**
	 * @fn	FTransform GetSynBoneTrans(FTransform inTrans, EBodyPartType faceOrBody);
	 *
	 * @brief	获取同步变换骨骼变换矩阵.
	 *
	 * @date	2017/3/25
	 *
	 * @return	返回对应同步变换的矩阵.
	 *
	 * @param	inTrans	输入的矩阵.
	 * @param	faceOrBody	骨骼类型.
	 */

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		FTransform GetSynBoneTrans(FTransform inTrans, EBodyPartType faceOrBody);

	/**
	 * @fn	void GetBoneTransformInfo(EBodyPartType faceOrBody, FName boneName, bool& doLocal, FBoneOffsetStruct3& Local, bool& doRot, FBoneOffsetStruct3& Rot, bool& doScalc, FBoneOffsetStruct3& Scalc);
	 *
	 * @brief	根据骨骼名获取位置.
	 *
	 * @date	2017/3/25
	 *
	 * @param	faceOrBody	部位类型，脸部或者身体
	 * @param	boneName	骨骼名称
	 * @param	doLocal	位置是否可调整
	 * @param	local		位置.
	 * @param	doRot	旋转是否可调整
	 * @param	rot	旋转.
	 * @param	doScalc	缩放是否可调整
	 * @param	sclac	缩放.
	 */

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		void GetBoneTransformInfo(EBodyPartType faceOrBody, FName boneName, bool& doLocal, FBoneOffsetStruct3& Local, bool& doRot, FBoneOffsetStruct3& Rot, bool& doScalc, FBoneOffsetStruct3& Scalc);


	/**
	* @fn	void LimitBone(FBoneStruct& bone, EBodyPartType type);
	*
	* @brief	骨骼变换限制
	*
	* @date	2017/3/25
	*
	* @param	bone	骨骼数据列表
	* @param 	type	骨骼类型
	*/

	UFUNCTION()
		void LimitBone(FBoneStruct& bone, EBodyPartType type);


	/**
	* @fn	void SavePinchFaceData();
	*
	* @brief	保存骨骼数据
	*
	* @date	2017/3/25
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		void SavePinchFaceData();

	/**
	* @fn	void SetBonePresentValue(FName boneName, EBodyPartType faceOrBody, EBoneTransType transType, float value);
	*
	* @brief	Sets bone present value.
	*
	* @date	2017/3/25
	*
	* @param	boneName  	骨骼名称
	* @param	faceOrBody	骨骼类型，是脸部还是身体
	* @param	transType 	骨骼变换类型
	* @param	value	  	线性插值的Alpha的范围
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		void SetBonePresentValue(FName boneName, EBodyPartType faceOrBody, EBoneTransType transType, float value);

	/**
	* @fn	void SetLimitBoneArray(TArray<FBoneLimit> limitArray, EBodyPartType faceOrBody);
	*
	* @brief	设置骨骼限制数组
	*
	* @date	2017/3/25
	*
	* @param	limitArray	骨骼限制数组
	* @param	faceOrBody	骨骼类型，是脸部还是身体
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		void SetLimitBoneArray(TArray<FBoneLimit> limitArray, EBodyPartType faceOrBody);

	/**
	* @fn	void AddModifyBone(FName boneName, EBodyPartType faceOrBody);
	*
	* @brief	Adds a modify bone to 'faceOrBody'.
	*
	* @date	2017/3/25
	*
	* @param	boneName  	骨骼名称
	* @param	faceOrBody	骨骼类型，是脸部还是身体
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
		void AddModifyBone(FName boneName, EBodyPartType faceOrBody);

public:

	// 骨骼变换范围
	const float minLoc = -2.0f; ///< 最小的位置
	const float maxLoc = 2.0f;  ///< 最大的位置
	const float minRot = -30.0f;	///< 最小的旋转
	const float maxRot = 30.0f; ///< 最大的旋转
	const float minScl = 0.8f;  ///< 最小的3D缩放
	const float maxScl = 1.5f;  ///< 最大的3D缩放

	UPROPERTY()
	TArray<FBoneLimit> FaceBoneLimitArray;  ///< Array of face bone limits，脸部骨骼限制数组

	UPROPERTY()
	TArray<FBoneLimit> BodyBoneLimitArray;  ///< Array of body bone limits，身体骨骼限制数组


};
