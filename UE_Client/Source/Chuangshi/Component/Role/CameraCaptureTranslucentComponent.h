// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/SceneCaptureComponent2D.h"
#include "CameraCaptureTranslucentComponent.generated.h"

/*
* 文件名称：CameraCaptureTranslucentComponent.h
* 功能说明：模型半透明处理，实现方式与ATransActorCapture基本相同
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020/3/27
*/


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API UCameraCaptureTranslucentComponent : public USceneCaptureComponent2D
{
	GENERATED_BODY()
		
public:	
	UCameraCaptureTranslucentComponent();

	void SetWarnTips(const uint8& BWarn);

	void AddTranslucentComponent(AActor* InActor);
	void RemoveTranslucentComponent(AActor* InActor);
	
protected:
	// Called when the game starts
	virtual void BeginPlay() override;

	void Init();
public:	
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	// 后处理材质实例                                                                                                                                                     
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		class UMaterialInstanceDynamic* M_PTranslucentInst;

		
};
