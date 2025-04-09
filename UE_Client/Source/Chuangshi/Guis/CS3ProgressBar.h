// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ProgressBar.h"
#include "CS3ProgressBar.generated.h"

/*
* 文件名称：CS3ProgressBar.h
* 功能说明：封装进度条做平滑过渡处理
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2018-07-31
*/
UCLASS()
class CHUANGSHI_API UCS3ProgressBar : public UProgressBar
{
	GENERATED_UCLASS_BODY()
	
public:
	///<进度条平滑过渡速率（范围1-5）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Progress, meta = (UIMin = "1", UIMax = "5"))
		float Velocity = 2.5;
	///<SetTimer间隔时间（范围0.01-0.1）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Progress, meta = (UIMin = "0.01", UIMax = "1"))
		float IntervalTime = 0.02;
	
	/** Sets the current value of the ProgressBar. */
	UFUNCTION(BlueprintCallable, Category = "CS3Progress")
		void SetProgressPercent(float InPercent);

	virtual void BeginDestroy() override;
private:
	float CurPercent;
	float DstPercent;
	float TotalTime;
	UPROPERTY()
		FTimerHandle CdTimerHandle;///<CD计时器

private:
	void StartCdTime();///<启动CD计时器
	void StopCdTime();///<停止CD计时器
	void ShowClipShader();///<播放平滑过渡裁剪效果
};
