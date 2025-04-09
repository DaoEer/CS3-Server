// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Util/CustomEffect/CS3AnimNotifyState.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequenceBase.h"
#include "ObjectMacros.h"
#include "AnimNotifyState_AttachMeshPart.generated.h"

/*
* 文件名称：AnimNotifyState_AttchMeshPart.h
* 功能说明：绑定附属部件到主角身上通知状态（通过配置表DT_MeshBindCfg绑定）
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2018-03-07
*/

UCLASS(const, Blueprintable, Abstract, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3AnimNotifyState_AttachMeshPart"))
class CHUANGSHI_API UAnimNotifyState_AttachMeshPart : public UCS3AnimNotifyState
{
	GENERATED_BODY()
public:
	UAnimNotifyState_AttachMeshPart();

#if WITH_EDITOR
	virtual void PreEditChange(UProperty* PropertyAboutToChange) override;
#endif

	virtual void NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration) override;
	virtual void NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime) override;
	virtual void NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation) override;
	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;

public:

	///①同一个"MeshBindID"在不同的通知之间,会互相冲突,需要注意使用(必要时，可以申请两个配置相同的ID以供表现保障)
	///②目前不支持在编辑器中直接查看表现,需要在游戏中观察
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Attch Mesh Part")
		FString NotifyType = "CS3AttchMeshPart";

	///不影响具体功能,仅供配置人员备注使用
	UPROPERTY(EditAnywhere, Category = "Attch Mesh Part", DisplayName = "备注")
		FString HelpDesc;

	///对应配置ID详见部件绑定配置表(MeshBindTable)
	UPROPERTY(EditAnywhere, Category = "Attch Mesh Part")
		FName AttachMeshId;
};
