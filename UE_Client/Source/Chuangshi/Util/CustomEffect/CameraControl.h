// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Kismet/KismetMaterialLibrary.h"
#include "Util/CS3Debug.h"
#include "Component/SpringArmComponentEX.h"
#include "Camera/CameraComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Engine/TextureRenderTarget2D.h"
#include "Camera/CameraShake.h"
#include "CameraControl.generated.h"

/*
* 文件名称：CameraControl.h
* 功能说明：
* 文件作者：wangzheng
* 目前维护：wuxiaoou
* 创建时间：2017-03-08
*/


CONTROL_COMPILE_OPTIMIZE_START
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnDistortSceneFinished);

UCLASS(Blueprintable, meta = (DisplayName = "CameraControl"))
class CHUANGSHI_API ACameraControl : public AActor
{
	GENERATED_BODY()

		struct BaseData
	{
		float Intensity;
		FVector Time;
		float Passed;
		bool Enable;
		BaseData()
		{
			Enable = false;
			Passed = 0.0f;
		}
		void Init(float fIntensity, float fFadeInT, float fRemainT, float fFadeOutT)
		{
			Intensity = fIntensity;
			Time = FVector(fFadeInT, fRemainT, fFadeOutT);
			Passed = 0.0f;
			Enable = true;
		}
	};
	struct CommonData
	{
		float Time;
		float Passed;
		bool Enable;
		int32 Priority;
		CommonData()
		{
			Enable = false;
			Passed = 0.0f;
		}
		void Init(float fTime)
		{
			Time = fTime;
			Passed = 0.0f;
			Enable = true;
		}
	};
	struct ShakeData : CommonData
	{
		// 震动
		float Intensity;
		float Rate;
		//震动增量
		FVector ShakeDelta;
		void Init(float fIntensity, float fRate, float fTime, ACameraControl* Contral)
		{
			//上一次动作进程判断
			if (ShakeDelta != FVector(0.0f, 0.0f, 0.0f))
			{
				USpringArmComponent* arm = Cast<USpringArmComponent>(Contral->m_CurrCamera->GetAttachParent());

				//如果有遗留偏移，则清除
				arm->SocketOffset.Set(arm->SocketOffset.X - ShakeDelta.X, arm->SocketOffset.Y - ShakeDelta.Y,
					arm->SocketOffset.Z - ShakeDelta.Z);

			}
			CommonData::Init(fTime);
			Intensity = fIntensity;
			Rate = fRate;

			ShakeDelta = FVector(0.0f, 0.0f, 0.0f);
		}
	};
	struct ApproachData : BaseData
	{
		// 拉近拉远
		float ArmLength;

		void Init(float fDist, float fApproachT, float fRemainT, float fApproachBackT, float fArmLength)
		{
			BaseData::Init(fDist, fApproachT, fRemainT, fApproachBackT);
			ArmLength = 0.0f;
		}
	};
	struct BlurData : BaseData
	{
		//淡入淡出
		UPROPERTY()
			UMaterialInstanceDynamic*  MID;
	};
	struct BlurOffsetX : BlurData
	{
	};
	struct BlurOffsetY : BlurData
	{
	};
	struct UpData : BaseData
	{
		//拉高拉低
		void Init(float fDist, float fApproachT, float fRemainT, float fApproachBackT)
		{
			BaseData::Init(fDist, fApproachT, fRemainT, fApproachBackT);
		}
	};
	struct DistortData : BaseData
	{
		//屏幕扭曲材质
		UPROPERTY()
			UMaterialInstanceDynamic* MID;
		FLinearColor FilterColor;///扭曲颜色
		float DistortArea;///扭曲颜色
		bool bIsEndEffect;///结束效果
		FLinearColor MaskColor;///遮罩颜色MaskColor
		void Init(float fIntensity, FLinearColor fFilterColor, FLinearColor fMaskColor, float fDistortArea, float fRate, float fTime, float fBackTime)
		{
			if (fFilterColor.R < 0 || fFilterColor.G < 0 || fFilterColor.B < 0)
			{
				FilterColor.R = 0;
				FilterColor.G = 0;
				FilterColor.B = 0;
				CS3_Warning(TEXT("DistortScene FilterColor is Error or RGB is less than Zero!!!"));
			}
			else
			{
				FilterColor = fFilterColor;
			}
			if (fMaskColor.R < 0 || fMaskColor.G < 0 || fMaskColor.B < 0 || fMaskColor.A < 0)
			{
				MaskColor.R = 0;
				MaskColor.G = 0;
				MaskColor.B = 0;
				MaskColor.A = 0;
				CS3_Warning(TEXT("DistortScene MaskColor is Error or RGBA is less than Zero!!!"));
			}
			else
			{
				MaskColor = fMaskColor;
			}
			if (fDistortArea < 0)
			{
				DistortArea = 0;
				CS3_Warning(TEXT("DistortScene DistortArea is less than Zero!!!"))
			}
			else
			{
				DistortArea = fDistortArea;
			}

			bIsEndEffect = false;
			BaseData::Init(fIntensity, fRate, fTime, fBackTime);
		}
	};

	struct LXDistorData : BaseData
	{
		//屏幕螺旋扭曲材质
		UPROPERTY()
			UMaterialInstanceDynamic* MID;
		float DitortAngle;///扭曲角度
		float DistortMask;///扭曲遮罩
		float StartTimeDistort;///开始扭曲时间
		float RecoveryTimeDistort;///恢复时间
		bool bIsEndEffect;///结束效果
		bool isEable;
		void Init(float fDitortAngle, float fDistortMask, float fStartTimeDistort, float fRecoveryTimeDistort)
		{
			DitortAngle = fDitortAngle;
			DistortMask = fDistortMask;
			StartTimeDistort = fStartTimeDistort;
			RecoveryTimeDistort = fRecoveryTimeDistort;

			bIsEndEffect = false;
			isEable = true;
			BaseData::Init(fDitortAngle, fDistortMask, fStartTimeDistort, fRecoveryTimeDistort);
		}
	};
	/// 描边效果
	struct OutLineData : BlurData
	{
	};
public:
	// Sets default values for this actor's properties
	ACameraControl();

	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

	// Called every frame
	virtual void Tick(float DeltaSeconds) override;

	//If true, actor is ticked even if TickType == LEVELTICK_ViewportsOnly
	virtual bool ShouldTickIfViewportsOnly() const override;

	UFUNCTION(BlueprintCallable, Category = Camera)
		void Init(UCameraComponent *Camera, UCameraComponent* Camera1);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void CameraShake(float Intensity, float Rate, float Time, int32 Priority);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void StopCameraShake();

	UFUNCTION(BlueprintCallable, Category = Camera)
		//void CameraApproach(float Dist, bool Percentage, float ApproachT, float RemainT, float ApproachBackT, bool ChangeCamera);
		void CameraApproach(float Dist, float ApproachT, float RemainT, float ApproachBackT);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void StopCameraApproach();

	UFUNCTION(BlueprintCallable, Category = Camera)
		void RadialBlur(float Intensity, float FadeInT, float RemainT, float FadeOutT);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void StopRadialBlur();

	UFUNCTION(BlueprintCallable, Category = Camera)
		void RadialOffsetX(float Offset, float FadeInT, float RemainT, float FadeOutT);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void StopRadialOffsetX();

	UFUNCTION(BlueprintCallable, Category = Camera)
		void RadialOffsetY(float Offset, float FadeInT, float RemainT, float FadeOutT);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void StopRadialOffsetY();

	UFUNCTION(BlueprintCallable, Category = Camera)
		void CameraUp(float Height, float FadeInT, float RemainT, float FadeOutT);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void StopCameraUp();

	// 	UFUNCTION(BlueprintCallable, Category = Camera)
	// 		void CameraRotate(float Time);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void DistortScene(float Intensity, FLinearColor FilterColor, FLinearColor MaskColor, float fDistortArea, float FadeInT, float RemainT, float FadeOutT);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void OnEndDistortScene();

	UFUNCTION(BlueprintCallable, Category = Camera)
		void StopDistortScene();

	UFUNCTION(BlueprintCallable, Category = Camera)
		void LXDistortScene(float fDitortAngle, float fDistortMask, float fStartTimeDistort, float fRecoveryTimeDistort);

	UFUNCTION(BlueprintCallable, Category = Camera)
		void OnEndLXDistortScene();

	UFUNCTION(BlueprintCallable, Category = Camera)
		void StopLXDistortScene();

	UFUNCTION(BlueprintCallable, Category = Camera)
		bool BlurisEnable();

	UFUNCTION(BlueprintCallable, Category = Camera)
		void ResetBlur();

	UFUNCTION(BlueprintCallable, Category = "Camera | OutLine")
		void OpenOutLineCalculation();

	UFUNCTION(BlueprintCallable, Category = "Camera | OutLine")
		void CloseOutLineCalculation();

	UFUNCTION(BlueprintCallable, Category = "Camera | OutLine")
		void OpenModelVagueCalculation();

	UFUNCTION(BlueprintCallable, Category = "Camera | OutLine")
		void CloseModelVagueCalculation();

	UFUNCTION(BlueprintCallable, Category = "Camera | OutLine")
		void ChangeOutLineColor(const FVector& Color);

	UFUNCTION(BlueprintCallable, Category = "Camera | OutLine")
		void ChangeOutLineWidth(const float& Width);

	void AddPerspectiveTarget(int32 targetID, float maxDist, float minDist, float maxHeigth);
	void RemovePerspectiveTarget(int32 targetID);
	

private:
	void _UpdateShake(float DeltaTime);
	void _UpdateApproach(float DeltaTime);
	void _UpdateRadialBlur(float DeltaTime);
	void _UpdataRadialOffsetX(float DeltaTime);
	void _UpdataRadialOffsetY(float DeltaTime);
	void _UpdateUp(float DeltaTime);
	//void _UpdateRotate(float DeltaTime);
	void _UpdateDistort(float DeltaTime);
	void _UpdateLXDistort(float DeltaTime);
	FLinearColor GetDistortColor(FLinearColor FilterColor);

	void _UpdatePerspectiveTarget(float DeltaTime);
public:
	UPROPERTY(BlueprintAssignable, Category = "CameraControl")
		FOnDistortSceneFinished OnDistortSceneFinished;

private:

	UPROPERTY(EditAnywhere, AdvancedDisplay)
		UCameraComponent *m_CameraComponent;
	UPROPERTY()
		UCameraComponent *m_CameraComponent1;
	UPROPERTY()
		UCameraComponent *m_CurrCamera;

	// 震动
	ShakeData m_Shake;

	// 拉近
	ApproachData m_Approach;

	// 经向模糊
	BlurData m_Blur;
	BlurOffsetX m_BlurOffsetX;
	BlurOffsetY m_BlurOffsetY;

	// 升高
	UpData m_Up;

	// 旋转
	//CommonData m_Rotate;

	//屏幕扭曲
	DistortData m_Distort;

	// 模型描边
	OutLineData m_OutLines;

	// 模型模糊
	OutLineData m_ModelVague;

	LXDistorData m_DistorSceneData;
	UPROPERTY()
		UMaterial* BlurMaterial;
	UPROPERTY()
		UMaterial* BlurOffsetMaterial;
	UPROPERTY()
		UMaterial* DistortMaterial;
	UPROPERTY()
		UMaterialInstance* DistorSceneMaterial;
	UPROPERTY()
		UMaterial* OutLineMaterial;
	UPROPERTY()
		UMaterial* ModelVagueMaterial;

private:
	int32 OutLineNums;
	TArray<int32> TargetIDArr;
	float MinVisibleDistance;
	float MaxVisibleDistance;
	float MaxVisibleHeigth;

};


UCLASS(Blueprintable, editinlinenew, meta = (DisplayName = "CS3CameraShake"))
class CHUANGSHI_API UCS3CameraShake : public UCameraShake
{
	GENERATED_BODY()
public:
	// Native API
	virtual void UpdateAndApplyCameraShake(float DeltaTime, float Alpha, FMinimalViewInfo& InOutPOV)override;
	virtual void PlayShake(class APlayerCameraManager* Camera, float Scale, ECameraAnimPlaySpace::Type InPlaySpace, FRotator UserPlaySpaceRot = FRotator::ZeroRotator)override;	
	void UpdateShakeData(int8 ShakeType,float Amplitude,float Frequency, uint8 InitialOffset, uint8 Waveform);

};
CONTROL_COMPILE_OPTIMIZE_END
