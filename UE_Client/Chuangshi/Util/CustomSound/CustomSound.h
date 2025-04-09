// Fill out your copyright notice in the Description page of Project Settings.
#pragma once

#include "GameFramework/Actor.h"
#include "Component/CS3AudioComponent.h"
#include "CustomSound.generated.h"

/*
* 文件名称：CustomSound.h
* 功能说明：自定义音效
* 文件作者：YangHan
* 目前维护：wuxiaoou
* 创建时间：2017-10-18
*/

class ACustomSound;
class USoundBase;

DECLARE_MULTICAST_DELEGATE_OneParam(FCustomSoundFinished, ACustomSound*);

UCLASS(BlueprintType)
class CHUANGSHI_API ACustomSound : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	ACustomSound();

public:
	/**
	*初始化自动战斗
	*
	*@param Sound 音效资源
	*@param VolumeMultiplier 音量因子
	*@param PitchMultiplier 音高因子
	*@param StartTime 开始的时间
	*
	*@return 无
	*/
	void InitCustomSound(class USoundBase* Sound,float VolumeMultiplier, float PitchMultiplier, float StartTime, FCustomSoundFinished Finished = FCustomSoundFinished());
	
	/**
	*停止音效
	*
	*
	*@return 无
	*/
	void Stop();

	///<音效播完回调
	void OnAudioFinished(UAudioComponent* curAudio);
	
public:
	///<音效组件
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	UCS3AudioComponent* m_AudioComponent;

private:
	///<音效开始的时间
	float m_StartTime;

	///<音效结束回调
	FCustomSoundFinished OnSoundFinished;
};
