// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/ModelPartData.h"
#include "GameData/ModifyFaceData.h"
#include "RoleModelInterface.generated.h"

/*
* 文件名称：RoleModelInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

 ///变身模型
class CHUANGSHI_API ReplaceModel
{
	void changeRoleModel() {};
};

///组合模型
class CHUANGSHI_API ComposeModel: public ReplaceModel
{
	void changeRoleModel() {};
};

/**
*玩家模型接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleModelInterface: public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleModelInterface();
	~URoleModelInterface();
	static FString GetName() { return TEXT("RoleModelInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleModelInterface.BP_RoleModelInterface_C'"); } //获取蓝图对象路径


public:
	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
	void OnRep_headModel();			///<更换头部模型

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
	void OnRep_cloakModel();			///<更换披风

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
	void OnRep_bodyModel();			///<更换上身

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
	void OnRep_hairModel();			///<更换头发

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
	void OnRep_adornModel(); 		///<更换头饰

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_hatModel();				///<更换帽子

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_coatModel();			///<更换上衣

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_wristModel();			///<更换护腕

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_handModel();			///<更换手套

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_waistModel();				///<更换腰带

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_pantsModel();			///<更换裤子

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_shoesModel();			///<更换鞋子

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_necklaceModel();			///<更换项链

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_lringModel();			///<更换左手戒指

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_rringModel();			///<更换右手戒指

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_weaponModel();		///<更换武器

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_suitsModel();		///更换套装
	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void OnRep_fabaoModel();		///更换法宝

	///更换头饰
	void Set_headAdornModel(const FString& newVal, const FString& oldVal);
	///更换面饰
	void Set_faceAdornModel(const FString& newVal, const FString& oldVal);
	///更换背饰
	void Set_backAdornModel(const FString& newVal, const FString& oldVal);
	///更换腰饰
	void Set_waistAdornModel(const FString& newVal, const FString& oldVal);
	///更换环身光效
	void Set_bodyLightEffect(const FString& newVal, const FString& oldVal);
	///背包变形偏移数据
	void Set_backAdornParam(const FString& newVal, const FString& oldVal);
	void StartSetBackAdornParam();

	// 模型变色
	void Set_colorScheme(const uint8& newValu, const uint8& oldVal);

	UFUNCTION(BlueprintCallable, Category = "RoleModelInterface")
		void ReqFaceModelData();///获取角色脸部模型数据

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleModelInterface")
		void OnReqFaceModelData(const TArray<FString>& BoneName, const TArray<FString>& BoneDatas , FFACE_STYLE_DATA faceStyleData);///将脸部数据传入蓝图中

	virtual void InitBlueCB() override;

	void CLIENT_OnReqFaceData(const FVariant& FaceModelData, const FVariant& FaceStyleData);///接收服务器发过来的脸部数据

protected:
	/**
	*更换装备位置的s模型
	*
	*@param equipPos 装备位置
	*@param partID 需要更换部分的ID
	*
	*@return 无
	*/
	void ChangePart(MODEL_PART_TYPE PartType, FString partID);

private:
	void StartChangePart(MODEL_PART_TYPE PartType, FString partID);

private:
	UPROPERTY()
		TMap<MODEL_PART_TYPE, FString> CachePartChangeData; 
	FDelegateHandle Handle;
	FDelegateHandle ChangePartHandle;
};
