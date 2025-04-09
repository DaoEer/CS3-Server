// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Util/CustomEffect/CS3AnimNotify.h"
#include "NotifySkillDecal.generated.h"

/*
* 文件名称：NotifySkillDecal.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：zhangfudong
* 创建时间：2017-07-18
*/

UCLASS(abstract, meta = (DisplayName = "CS3SkillDecalAnimNotify"))
class CHUANGSHI_API UNotifySkillDecal : public UCS3AnimNotify
{
	GENERATED_BODY()
	
public:
	UNotifySkillDecal();

	virtual void BeginDestroy() override;

	virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation);
protected:
	void SpawnMat(USkeletalMeshComponent* MeshComp);///<创建贴花材质

public:
	///光效资源
	UPROPERTY(EditAnywhere, meta = (DisplayName = "Particle System"))
		UParticleSystem* PSTemplate;
	
	///贴花位置偏移 X指左方，Y指前方，Z指上方，单位厘米
	UPROPERTY(EditAnywhere)
		FVector DecalLocation;
	///贴花大小比例
	UPROPERTY(EditAnywhere)
		float DecalScale;
	///贴花作用高度，此项所填值为高度一半，无其他需求不要改变默认值（单位CM）
	UPROPERTY(EditAnywhere)
		float DecalHight;
	///贴花旋转（沿Z轴旋转，从上往下看顺时针方向，单位角度）
	UPROPERTY(EditAnywhere)
		float DecalRoater;
	///是否绑定
	UPROPERTY(EditAnywhere)
		bool bIsBind;
	///当留空或填错，贴花将绑定到对象的世界坐标（一般的表现为胶囊体的中间）
	UPROPERTY(EditAnywhere)
		FName SocketName;
	///显示时长
	UPROPERTY(EditAnywhere)
		float LifeTime;
};
