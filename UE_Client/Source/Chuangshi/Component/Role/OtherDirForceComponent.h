// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Component/Role/ForceComponent.h"
#include "OtherDirForceComponent.generated.h"

/*
* 文件名称：OtherDirForceComponent.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：wuxiaoou
* 创建时间：2017-12-07
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UOtherDirForceComponent : public UForceComponent
{
	GENERATED_BODY()
public:
	UOtherDirForceComponent():OtherCharacter(nullptr){}

	//设置其他的目标
	void SetOtherCharacter(ACharacter* OtherActor);

protected:
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
private:
	UPROPERTY()
	class ACharacter* OtherCharacter;
	
	
};
