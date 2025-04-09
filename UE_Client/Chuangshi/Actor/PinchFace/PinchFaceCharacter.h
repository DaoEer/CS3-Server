// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "BoneStruct.h"
#include "PinchFaceAnimInstance.h"
#include "Actor/GameCharacter.h"
#include "GameData/RoleInfo.h"
#include "PinchFaceCharacter.generated.h"


/*
* 文件名称：PinchFaceCharacter.h
* 功能说明：可捏脸角色基类
* 文件作者：luocheng
* 目前维护：wuxiaoou
* 创建时间：2016-08-31
*/


/**
* @struct FMaterialHitResult
* @brief	射线检测材质数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMaterialHitResult
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Translation)
		int MaterialIndex = -1; ///< 材质索引

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Material)
		FVector2D UVCoordinates = FVector2D::ZeroVector;	///< 材质uv
};

/**
 * 捏脸对象类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API APinchFaceCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:

	/**
	 * @fn	APinchFaceCharacter();
	 *
	 * @brief	Default constructor.
	 *
	 * @date	2017/3/27
	 */

	APinchFaceCharacter();

	/**
	 * @fn	void Tick(float DeltaSeconds) override;
	 *
	 * @brief	Ticks.
	 *
	 * @date	2017/3/27
	 *
	 * @param	DeltaSeconds	两帧之间的时间差
	 */

	void Tick(float DeltaSeconds) override;

	/**
	* @fn	void Init(FROLEINFO roleInfo);
	*
	* @brief	初始化给定的玩家信息
	*
	* @date	2017/3/27
	*
	* @param	roleInfo	玩家信息
	*/

	UFUNCTION(BlueprintCallable,Category = "PinchFace")
	void Init(FROLEINFO roleInfo);

	/**
	* @fn	void OnInitlizeFinish();
	*
	* @brief	初始化完成回调
	*
	* @date	2017/3/27
	*/

	UFUNCTION(BlueprintNativeEvent, Category = "PinchFace")
	void OnInitlizeFinish();

	/**
	* @fn	bool LineTrace(struct FHitResult& OutHit, const FVector& Start, const FVector& End, ECollisionChannel TraceChannel);
	*
	* @brief	射线检测
	*
	* @date	2017/3/27
	*
	* @param	OutHit			输出碰撞信息
	* @param 	Start			开始位置
	* @param 	End				结束位置
	* @param 	TraceChannel	碰撞通道
	*
	* @return	True if it succeeds, false if it fails.
	*/
	UFUNCTION(BlueprintCallable, Category = "PinchFace")
	bool LineTrace(struct FHitResult& OutHit, const FVector& Start, const FVector& End, ECollisionChannel TraceChannel);

	/**
	* @fn	bool GetUVFromFaceIndex(struct FMaterialHitResult& OutMaterial, const FHitResult& OutHit, USkeletalMeshComponent* skMesh);
	*
	* @brief	通过碰撞数据获取碰撞点的uv数据
	*
	* @date	2017/3/27
	*
	* @param	OutMaterial	碰撞的材质数据
	* @param  	OutHit	   	碰撞结果
	* @param	skMesh	   	检测的骨骼
	*
	* @return	True if it succeeds, false if it fails.
	*/

	UFUNCTION(BlueprintCallable, Category = "PinchFace")
	bool GetUVFromFaceIndex(struct FMaterialHitResult& OutMaterial, const FHitResult& OutHit, USkeletalMeshComponent* skMesh);

	/**
	* @fn	FColor GetColorFromUV(UTexture2D* txt, FVector2D UVCoordinates);
	*
	* @brief	通过uv获取遮罩颜色,分量(R)
	*
	* @date	2017/3/27
	*
	* @param	txt			 	遮罩图
	* @param  	UVCoordinates	uv坐标
	*
	* @return	返回遮罩颜色
	*/
	UFUNCTION(BlueprintCallable, Category = "PinchFace")
	FColor GetColorFromUV(UTexture2D* txt, FVector2D UVCoordinates);

	/**
	* @fn	FVector MoveCameraArm(USpringArmComponent* arm, float wheelValue, float delta);
	*
	* @brief	摄像机位置控制
	*
	* @date	2017/3/27
	*
	* @param	arm		  	摄像机摇臂
	* @param   	wheelValue	鼠标滚轮偏移
	* @param 	delta	  	时间差值
	*
	* @return	A FVector，摄像机摇臂的位置
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
	FVector MoveCameraArm(USpringArmComponent* arm, float wheelValue, float delta);


	/**
	* @fn	void RotateCamera(float deltaAngle, USpringArmComponent* arm);
	*
	* @brief	摄像机旋转控制
	*
	* @date	2017/3/27
	*
	* @param 	deltaAngle	角度差值
	* @param	arm		  	摄像机摇臂
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
	void RotateCamera(float deltaAngle, USpringArmComponent* arm);

	/**
	* @fn	void ForceMovingCamera(int animState, USpringArmComponent* arm);
	*
	* @brief	摄像机位置状态控制
	*
	* @date	2017/3/27
	*
	* @param 	animState	动作状态
	* @param	arm		 	摄像机摇臂
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
	void ForceMovingCamera(int animState, USpringArmComponent* arm);

	/**
	* @fn	FRotator LookAtCamera(USkeletalMeshComponent* skMesh, UCameraComponent* camera, FVector start, FRotator curRotate, float delta);
	*
	* @brief	看向摄像机
	*
	* @date	2017/3/27
	*
	* @param	skMesh   	操作的骨架网格对象
	* @param	camera   	摄像机组件
	* @param 	start	 	开始位置
	* @param 	curRotate	旋转
	* @param 	delta	 	时间差值
	*
	* @return	A FRotator，rotation信息
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
	FRotator LookAtCamera(USkeletalMeshComponent* skMesh, UCameraComponent* camera, FVector start, FRotator curRotate, float delta);

	/**
	* @fn	FRotator RotateHead(USkeletalMeshComponent* skMesh, UCameraComponent* camera, FRotator curRotate, float delta);
	*
	* @brief	旋转头部
	*
	* @date	2017/3/27
	*
	* @param [in,out]	skMesh   	操作的骨架网格对象
	* @param [in,out]	camera   	摄像机
	* @param 		  	curRotate	旋转
	* @param 		  	delta	 	时间差值
	*
	* @return	A FRotator，rotation信息
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
	FRotator RotateHead(USkeletalMeshComponent* skMesh, UCameraComponent* camera, FRotator curRotate, float delta);

	///坐标转换
	UFUNCTION(BlueprintCallable, Category = PinchFace)

	/**
	 * @fn	FTransform APinchFaceCharacter::ConverTransform(FVector offset, int btnType, int mode);
	 *
	 * @brief	坐标转换
	 *
	 * @date	2017/3/27
	 *
	 * @param	offset 	The offset.
	 * @param	btnType	按钮类型，0代表位移，1代表旋转，2代表缩放
	 * @param	mode   	模式，0代表只改变缩放，1代表改变缩放，同时改变Z轴位置
	 *
	 * @return	A FTransform.
	 */

	FTransform ConverTransform(FVector offset, int btnType, int mode);

	/**
	* @fn	TArray<FString> GetBonesName(USkeletalMeshComponent* skMesh);
	*
	* @brief	获取骨骼名称
	*
	* @date	2017/3/27
	*
	* @param	skMesh	骨骼网格
	*
	* @return	骨骼名称数组
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
	TArray<FString> GetBonesName(USkeletalMeshComponent* skMesh);

	/**
	* @fn	void InitLimitBones(const TArray<FBoneLimit> limitArray, EBodyPartType boneType);
	*
	* @brief	初始化骨骼限制数据
	*
	* @date	2017/3/27
	*
	* @param	limitArray	骨骼限制数据
	* @param	boneType  	骨骼类型，脸部或者身体
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
	void InitLimitBones(const TArray<FBoneLimit> limitArray, EBodyPartType boneType);

	/**
	* @fn	void RegisterMotifyBones(const TArray<FBONE_ATTR> boneArray, EBodyPartType boneType);
	*
	* @brief	注册骨骼变换数据
	*
	* @date	2017/3/27
	*
	* @param	boneArray	骨骼变换数据
	* @param	boneType 	骨骼类型，脸部或者身体
	*/

	UFUNCTION(BlueprintCallable, Category = PinchFace)
	void RegisterMotifyBones(const TArray<FBONE_ATTR> boneArray, EBodyPartType boneType);

	///初始化骨骼变换数据
	UFUNCTION(BlueprintCallable, Category = "PinchFace")
	void InitBones(TArray<FBoneStruct> faceBoneArray, TArray<FBoneStruct> bodyBoneArray);

private:

	/**
	 * @fn	FRotator APinchFaceCharacter::RotateToAngle(FRotator anim, FRotator cur, float delta);
	 *
	 * @brief	旋转角度.
	 *
	 * @date	2017/3/27
	 *
	 * @param	anim 	The animation.
	 * @param	cur  	The current.
	 * @param	delta	The delta.
	 *
	 * @return	A FRotator.
	 */

	FRotator RotateToAngle(FRotator anim, FRotator cur, float delta);

	/**
	 * @fn	int APinchFaceCharacter::GetArmState(USpringArmComponent* arm);
	 *
	 * @brief	获取摄像机的分段状态
	 *
	 * @date	2017/3/27
	 *
	 * @param [in,out]	arm	摄像机摇臂.
	 *
	 * @return	摄像机摇臂状态
	 */

	int GetArmState(USpringArmComponent* arm);

public:
	UPROPERTY(BlueprintReadOnly)
		FROLEINFO RoleInfo; ///< 玩家信息

	UPROPERTY(BlueprintReadWrite)
	FBONE_ATTR SelectBone;  ///< 选中的骨骼节点

	UPROPERTY(BlueprintReadWrite)
	FBONE_ATTR TouchBone;   ///< 触摸到的骨骼节点

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = PinchFace)
		TArray<FFloatVectorStruct> CameraPosArray;  ///< 摄像机分段状态数据

	bool bInintlize = false;

private:
	bool camerAutoMove = false;
	bool forceMoving = false;
	int AnimState = 0;
	FVector curLoc = FVector(0, 0, 0);
	float curLength = 0;
};
