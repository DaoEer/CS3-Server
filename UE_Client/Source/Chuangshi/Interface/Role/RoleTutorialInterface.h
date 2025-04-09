// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Util/CS3Debug.h"
#include "CS3Base/CS3EntityInterface.h"
#include "RoleTutorialInterface.generated.h"

/*
* 文件名称：RoleTutorialInterface.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-11-08
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleTutorialInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	static FString GetName() { return TEXT("RoleTutorialInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleTutorialInterface.BP_RoleTutorialInterface_C'"); } //获取蓝图对象路径


	//拆分RecordTutorialIndexs，用于判定
	UPROPERTY(BlueprintReadOnly)
		TArray<FString> RecordIndexList;

	UPROPERTY(BlueprintReadOnly)
		FString RecordTutorialIndexs;

	UFUNCTION(BlueprintCallable, Category = "RoleTutorialInterface")
		void OnRep_RecordTutorialIndexs();

	//删除那些仅能触发一次的，但是已经触发过的事件
	void ClearDoOnceEvents();


	///是否为仅触发一次的，并且已经触发过
	UFUNCTION(BlueprintCallable, Category = "RoleTutorialInterface")
		bool IsDoneTriggerItem(const FString& Index);

	void FinishTriggerOnceTurtorial(const FName& KeyIndex);

	virtual void onLeaveWorld() override; ///< 当Entity离开世界（被销毁时）时，此方法被调用

};