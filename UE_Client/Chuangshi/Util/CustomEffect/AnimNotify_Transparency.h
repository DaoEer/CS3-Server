// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3AnimNotify.h"
#include "AnimNotify_Transparency.generated.h"

/*
* 文件名称：AnimNotify_CustomSkeletalAnim.h
* 功能说明：半透明通知
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2019-01-09
*/

UENUM(BlueprintType)
enum class Transparency_Type : uint8
{
	ADDTRANS = 0,			//添加半透明
	REMOVETRANS = 1			//移除半透明
};

UCLASS(meta = (DisplayName = "CS3AnimNotify_Transparency"))
class CHUANGSHI_API UAnimNotify_Transparency : public UCS3AnimNotify
{
	GENERATED_BODY()
	
	// Begin UAnimNotify interface
	virtual FString GetNotifyName_Implementation() const override;

	virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
	// End UAnimNotify interface

	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;

	// 类型
	UPROPERTY(EditAnywhere, Category = "TransparencyAnimNotify")
	Transparency_Type TransType = Transparency_Type::ADDTRANS;

	// 透明度
	UPROPERTY(EditAnywhere, Category = "TransparencyAnimNotify", meta = (ClampMin = "0.0", ClampMax = "1.0"))
	float Alpha = 1.0f;
};
