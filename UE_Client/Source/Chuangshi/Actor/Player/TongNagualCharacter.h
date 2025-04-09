// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/GameCharacter.h"
#include "GameData/TongNagualData.h"
#include "TongNagualCharacter.generated.h"

/*
* 文件名称：TongNagualCharacter.h
* 功能说明：帮会神兽召唤
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2019-09-18
*/


UCLASS()
class CHUANGSHI_API ATongNagualCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	ATongNagualCharacter();

	///通过ModelID更换模型
	UFUNCTION(BlueprintCallable, Category = "TongNagualCharacter")
		void ChangeModelByModelID(FString ModelID);

	///通过ScriptID查找模型信息
	UFUNCTION(BlueprintCallable, Category = "TongNagualCharacter")
		FTONG_NAGUAL_MODEL_DATA GetModelDataByScriptID(FString ScriptID);

	/* 由于第一次创建模型时需要一定的时间，在创建完成前会阻止后续创建模型的请求。如果在创建过程中切换神兽界面，
	最终创建出来的是前一次请求创建的模型，所以需要在创建结束后再判断是否显示到界面 */
	UFUNCTION(BlueprintImplementableEvent, Category = "TongNagualCharacter")
		void OnCreateApperanceOver_BP();

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	virtual void OnCreateApperanceOver() override;

private:
	TMap<FString, FTONG_NAGUAL_MODEL_DATA> ModelDatas;
	///当前请求创建的模型ID
	FString CurrModelID;
};
