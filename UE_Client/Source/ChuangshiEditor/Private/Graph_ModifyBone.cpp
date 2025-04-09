// Fill out your copyright notice in the Description page of Project Settings.
#include "Graph_ModifyBone.h"
#include "ChuangshiEditor.h"
#include "CoreMinimal.h"
#include "Editor/AnimGraph/Public/AnimGraphDefinitions.h"
#include "Kismet2/BlueprintEditorUtils.h"
#include "UnrealEd.h"
#include "CompilerResultsLog.h"


#define LOCTEXT_NAMESPACE "ModifyBone"

UGraph_ModifyBone::UGraph_ModifyBone(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	CurWidgetMode = (int32)FWidget::WM_Rotate;
}

FText UGraph_ModifyBone::GetControllerDescription() const
{
	//return LOCTEXT("TransformModifyBone", "Transform (Modify) Bone");
	return LOCTEXT("ModifyBone", "ModifyBone");
}

FText UGraph_ModifyBone::GetTooltipText() const
{
	return LOCTEXT("AnimGraphNode_ModifyBone_Tooltip", "The Transform Bone node alters the transform - i.e. Translation, Rotation, or Scale - of the bone");
}

FText UGraph_ModifyBone::GetNodeTitle(ENodeTitleType::Type TitleType) const
{
	//if ((TitleType == ENodeTitleType::ListView || TitleType == ENodeTitleType::MenuTitle) && (Node.BoneToModify.BoneName == NAME_None))
	if ((TitleType == ENodeTitleType::ListView || TitleType == ENodeTitleType::MenuTitle))
	{
		return GetControllerDescription();
	}
	// @TODO: the bone can be altered in the property editor, so we have to 
	//        choose to mark this dirty when that happens for this to properly work
	else //if (!CachedNodeTitles.IsTitleCached(TitleType, this))
	{
		FFormatNamedArguments Args;
		Args.Add(TEXT("ControllerDescription"), GetControllerDescription());
		//Args.Add(TEXT("BoneName"), FText::FromName(Node.BoneToModify.BoneName));
		Args.Add(TEXT("BoneName"), FText::FromName(FName("CustomedBone")));
		// FText::Format() is slow, so we cache this to save on performance
		if (TitleType == ENodeTitleType::ListView || TitleType == ENodeTitleType::MenuTitle)
		{
			CachedNodeTitles.SetCachedTitle(TitleType, FText::Format(LOCTEXT("AnimGraphNode_ModifyBone_ListTitle", "{ControllerDescription} - Bone: {BoneName}"), Args), this);
		}
		else
		{
			CachedNodeTitles.SetCachedTitle(TitleType, FText::Format(LOCTEXT("AnimGraphNode_ModifyBone_Title", "{ControllerDescription}\nBone: {BoneName}"), Args), this);
		}
	}
	return CachedNodeTitles[TitleType];

}
#undef LOCTEXT_NAMESPACE

