// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameFramework/Actor.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Camera/CameraComponent.h"
#include "Engine/StreamableManager.h"
#include "StoryCameraActor.generated.h"

UCLASS()
class CHUANGSHI_API AStoryCameraActor : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AStoryCameraActor();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

   //If true, actor is ticked even if TickType == LEVELTICK_ViewportsOnly
	virtual bool ShouldTickIfViewportsOnly() const override;

	//摄像机边缘光设置
	void OutLineEffectToCamera();

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

	///镜头摄像机组件 在蓝图构建函数初始化 因为当前有两个镜头摄像机的原因所以吧创建放在蓝图构造中 
	UPROPERTY(BlueprintReadWrite, Category = "StoryCameraActor")
		UCameraComponent* StoryCameraComponent;
	UPROPERTY()
		USceneCaptureComponent2D* SceneCapture;///<场景捕捉组件
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		FLinearColor OutLineColor = FLinearColor(0, 1, 1, 0);///边缘光颜色
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		float OutlineWidth = 5.0f;///边缘光厚度
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		bool OpenOutLine = false;///开启边缘光效果
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		TArray<AActor*> ActorRef;///边缘光Actor
	UPROPERTY( BlueprintReadWrite)
		TSoftObjectPtr<UMaterialInterface> PostMaterial;

	int32 DepthTexSize = 512;///贴图大小
	FLinearColor InLineColor = FLinearColor(0, 1, 1, 0);

private:

	UPROPERTY(Category = CameraActor, VisibleAnywhere, BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
		class USceneComponent* SceneComponent;

	FStreamableManager StreamManager;///<资源流管理器

	void SetDynamicMaterial(UMaterialInstanceDynamic* material);

};
