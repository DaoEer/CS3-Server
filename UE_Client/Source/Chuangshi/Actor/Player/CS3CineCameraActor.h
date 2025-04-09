// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CineCameraComponent.h"
#include "CineCameraActor.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Engine/StreamableManager.h"
#include "CS3CineCameraActor.generated.h"
/**
 * 
 */
UCLASS()
class CHUANGSHI_API ACS3CineCameraActor : public ACineCameraActor
{
	GENERATED_BODY()

public:
	ACS3CineCameraActor(const FObjectInitializer& ObjectInitializer);
	virtual void BeginPlay()override;
	// Called every frame
	virtual void Tick(float DeltaTime) override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	//摄像机边缘光设置
	void OutLineEffectToCamera();

	void UpdateCineCameraFocusMethod();
	void UpdateCineCameraFocusSettings(float ManualFocusDistance, float FocalLength, float Aperture);
	void SetActorRefData(AActor* actor);
public:
	UPROPERTY()
		USceneCaptureComponent2D* SceneCapture;///<场景捕捉组件

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		FLinearColor OutLineColor = FLinearColor(0, 1, 1, 0);///边缘光颜色
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		float OutlineWidth = 5.0f;///边缘光厚度
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		bool OpenOutLine = false;///开启边缘光效果
	UPROPERTY(EditAnywhere, BlueprintReadOnly,Interp)
		AActor* ActorRef;///边缘光Actor
	UPROPERTY(EditDefaultsOnly)
		UMaterialInterface* PostMaterial; // 这个资源在构造时就会加载所以直接硬引用

	int32 DepthTexSize = 1024;///贴图大小
	FLinearColor InLineColor = FLinearColor(0, 1, 1, 0);

	UPROPERTY(Interp, EditAnywhere, BlueprintReadWrite)
		ECameraFocusMethod FocusMethod;
	UPROPERTY(Interp, EditAnywhere, BlueprintReadWrite)
		bool bIsChangeFocusMethod = false;

private:
	FStreamableManager StreamManager;///<资源流管理器
	UMaterialInstanceDynamic* DynamicMaterial;
	UFUNCTION(BlueprintCallable, Category = "CineCameraActor")
	void SetMaterialInstanceDynamic();

private:
	void SetDynamicMaterial(UMaterialInstanceDynamic* material);


};
