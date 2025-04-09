// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "AnimGraphNode_SkeletalControlBase.h"
#include "Actor/PinchFace/ModifyBone.h"
#include "EdGraph/EdGraphNodeUtils.h"
#include "Graph_ModifyBone.generated.h"
/**
 * 
 */
UCLASS(BlueprintType)
class CHUANGSHIEDITOR_API UGraph_ModifyBone : public UAnimGraphNode_SkeletalControlBase
{
	GENERATED_UCLASS_BODY()
	
	UPROPERTY(EditAnywhere, Category = Settings)
	FModifyBone Node;
public:
	// UEdGraphNode interface
	virtual FText GetNodeTitle(ENodeTitleType::Type TitleType) const;
	virtual FText GetTooltipText() const;
	// End of UEdGraphNode interface

protected:
	virtual FText GetControllerDescription() const;
	virtual const FAnimNode_SkeletalControlBase* GetNode() const override { return &Node; }

private:
	FNodeTitleTextTable CachedNodeTitles;
	int32 CurWidgetMode;
	
	
};
