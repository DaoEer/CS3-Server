// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "GameData/ModifyFaceData.h"
#include "Components/InputComponent.h"
#include "Engine/EngineTypes.h"
#include "GameFramework/SpringArmComponent.h"
#include "Component/CS3LightComponent.h"
#include "Entity/Alias.h"
#include "ModifyFaceCharacter.generated.h"

/*
* 文件名称：AModifyFaceCharacter.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2019-08-08
*/

UCLASS()
class CHUANGSHI_API AModifyFaceCharacter : public AGameCharacter
{
	GENERATED_BODY()
		
public: 
	AModifyFaceCharacter();
	virtual void BeginPlay();
	virtual void SetupPlayerInputComponent(class UInputComponent* InputCpt) override;
	virtual void OnCreateModelOver()override;

	//创建捏脸关卡的模型
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		void CreateModel(FString ModelId);
	//云裳阁:创建云裳阁关卡的模型
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		void CreateStoreRoleModel();

	//云裳阁:重置云裳阁模型外观的部件(恢复成服务器玩家默认的部件）
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		void ResetStoreModelPart(MODEL_PART_TYPE PartType);

	// 射线检测
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		int MouseLineTrace(struct FHitResult& OutHit, const FVector& Start, const FVector& End, ECollisionChannel TraceChannel);

	// 获取 UV
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		bool GetUVFromFaceIndex(struct FMATERIAL_FACE_HIT_RESULT& OutMaterial, const FHitResult& OutHit, USkeletalMeshComponent* SK_Mesh);

	// 获取 UV 对应的颜色
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		FColor GetColorFromUV(UTexture2D* Texture, FVector2D UVCoordinates);

	// 移动摄像机
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		FVector MoveCameraArm(USpringArmComponent* Arm, float WheelValue, float Delta);

	// 旋转摄像机
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		void RotateCamera(float DeltaAngle, USpringArmComponent* Arm);

	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		FTransform ConverTransform(FVector Offset, int BtnType, int Mode);

	//鼠标中键滚轮方法
	UFUNCTION(BlueprintImplementableEvent, Category = "ModifyFace|ModifyFunction")
		void MouseScrolMoveCameraArm(float Aixs);

	//鼠标中键滚轮方法
	UFUNCTION(BlueprintCallable, Category = "ModifyFace|ModifyFunction")
		void ModifyFaceChangePart(MODEL_PART_TYPE InPos, FString PartID);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace|ModifyVariable")
		TArray<FCameraConfig> CameraPosArray;

	//播放动画
	UFUNCTION(BlueprintCallable, Category = "LoginCharacter")
		void PlayAction_BP(FName ActionName);

	//修改背饰偏移
	UFUNCTION(BlueprintCallable, Category = "LoginCharacter")
		void SetBackAdornLoaction(FVector deviation);

		UFUNCTION(BlueprintCallable, Category = "LoginCharacter")
	void OnBackWorldLevel();

	/**
	*Define method
	*通知登录排队信息
	*
	*@param rank,排名队列中每次
	*@param time,平均登陆时间
	*@param count,排队总人数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "LoginCharacter")
		void OnReceiveWattingInfo(const int32& rank, const float& time, const int32& count);

	/**
	*通知取消登录排队
	*
	*@param isInQueue,是否还在排队队列中(如果还在，意味着取消失败)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "LoginCharacter")
		void OnCancelLoginQueue(const int32& isInQueue);

	//获取Actor性别
	UFUNCTION(BlueprintCallable, Category = "ClothesCharacter")
	int GetActorGender();

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent

private:
	UCS3LightComponent* CS3LightComponent;
	int32 GetArmState(USpringArmComponent* Arm);

	void AddShopPreviewPart(FAModelInfo& ModelInfo);///<附加了预览的关卡商城中部件资源

public:

protected:

private:
	bool CameraAutoMove = false;
	bool ForceMoving = false;
	int AnimState = 0;
	FVector CurLoc;
	float CurLength;
};
