// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "ModelInterface.generated.h"

/*
* 文件名称：ModelInterface.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-10-18
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UModelInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UModelInterface();
	~UModelInterface();
	static FString GetName() { return TEXT("ModelInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.ModelInterface'"); } //获取蓝图对象路径

public:
	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_headModel();			///<更换头部模型

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_cloakModel();			///<更换披风

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_bodyModel();			///<更换上身

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_hairModel();			///<更换头发

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_adornModel(); 		///<更换头饰

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_hatModel();				///<更换帽子

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_coatModel();			///<更换上衣

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_wristModel();			///<更换护腕

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_handModel();			///<更换手套

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_waistModel();				///<更换腰带

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_pantsModel();			///<更换裤子

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_shoesModel();			///<更换鞋子

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_necklaceModel();			///<更换项链

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_lringModel();			///<更换左手戒指

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_rringModel();			///<更换右手戒指

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_weaponModel();		///<更换武器

	UFUNCTION(BlueprintCallable, Category = "MonsterExtXinMo")
		void OnRep_suitsModel();		///更换套装

protected:

	/**
	*更换装备位置的s模型
	*
	*@param equipPos 装备位置
	*@param partID 需要更换部分的ID
	*
	*@return 无
	*/
	void ChangePart(int equipPos, FString partID);
};
