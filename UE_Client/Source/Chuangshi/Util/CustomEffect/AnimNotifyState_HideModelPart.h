// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3AnimNotifyState.h"
#include "AnimNotifyState_HideModelPart.generated.h"

/*
* 文件名称：AnimNotifyState_HideModelPart.h
* 功能说明：隐藏模型部件通知状态（用于动作上通知隐藏某部件）
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2018-01-29
*/

class AGameCharacter;

UCLASS(const, Blueprintable, Abstract, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3AnimNotifyState_HideModelPart"))
class CHUANGSHI_API UAnimNotifyState_HideModelPart : public UCS3AnimNotifyState
{
	GENERATED_BODY()
public:
	UAnimNotifyState_HideModelPart();

	virtual void NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration) override;
	virtual void NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime) override;
	virtual void NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation) override;

private:
	void SetPartHideInGame(AGameCharacter *GameCharacter, bool HideInGame);
public:

	///①通知状态开始时,隐藏部件;通知状态结束时,显示部件
	///②请注意以下冲突情况，谨慎配置
	///②①同个动画中，多个通知之间会互相冲突
	///②②不同动画中，动画混合时，会互相冲突（如：淡入淡出、混合空间、半身融合…）
	///②③与动作表中的“HidePartDatas”参数冲突
	///③请注意以下限制情况，主动回避
	///③①背景动作中禁用（@CST-4078）
	///③②动画时间轴0~0.2秒（@CST-4077）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Part Hide In Game")
		FString NotifyType = "CS3HideModelPart";

	///不影响具体功能,仅供配置人员备注使用
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "备注")
		FString HelpDesc; 
	///默认静态组件
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "STMesh_DefaultStatic")
		bool STMesh_DefaultStatic;
	///骨骼模型
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "Mesh")
		bool SKMesh_Bodys;
	///头部
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Heads")
		bool SKMesh_Heads;
	///套装
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Suits")
		bool SKMesh_Suits;
	///头发
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Hairs")
		bool SKMesh_Hairs;
	///头饰
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Adorn")
		bool SKMesh_Adorn;
	///帽子
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Hat")
		bool SKMesh_Hat;
	///上衣
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Coats")
		bool SKMesh_Coats;
	///护腕
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Wrist")
		bool SKMesh_Wrist;
	///手套
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Gloves")
		bool SKMesh_Gloves;
	///腰带
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Waist")
		bool SKMesh_Waist;
	///裤子
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Pants")
		bool SKMesh_Pants;
	///鞋子
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Shoes")
		bool SKMesh_Shoes;
	///项链
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Necklace")
		bool SKMesh_Necklace;
	///左手戒指
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_L_RING")
		bool SKMesh_L_RING;
	///右手戒指
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_R_RING")
		bool SKMesh_R_RING;
	///双手武器
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_BHweapon")
		bool SKMesh_BHweapon;
	///左手武器
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "STMesh_LHweapon")
		bool STMesh_LHweapon;
	///右手武器
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "STMesh_RHweapon")
		bool STMesh_RHweapon;
	///披风
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_Cloak")
		bool SKMesh_Cloak;
	///法宝
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "SKMesh_FaBao")
		bool SKMesh_FaBao;
	///左手骨架武器[只针对链刃职业]
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "STMesh_LHweapon")
		bool STMesh_S_LHweapon;
	///右手骨架武器[只针对链刃职业]
	UPROPERTY(EditAnywhere, Category = "Part Hide In Game", DisplayName = "STMesh_RHweapon")
		bool STMesh_S_RHweapon;
private:
};
