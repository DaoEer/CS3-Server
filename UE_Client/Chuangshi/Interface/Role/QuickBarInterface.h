// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/CsvTableRowBase.h"
#include "GameData/Skill/QuickSkillData.h"
#include "QuickBarInterface.generated.h"

/*
* 文件名称：QuickBarInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：chendongyong
* 创建时间：2017-07-29
*/

/**
* 各职业心法技能数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILLPOSTUREDATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	//技能心法:0（无心法）101、102（战士）201、202（剑客）301、302（射手）401、402（法师）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SkillPosture;
	//1级的心法技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SkillID;
	//普通状态按钮图片路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> NormalBtnTexture;
	//高亮状态按钮图片路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> HighlightBtnTexture;
	//图片尺寸
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector2D ImageSize;
	bool operator ==(const FSKILLPOSTUREDATA& other)
	{
		return other.SkillPosture == SkillPosture;
	}

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		ResultInfo.Result = Ok;

		if (NormalBtnTexture.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(NormalBtnTexture.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("; \"NormalBtnTexture\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("; \"NormalBtnTexture\" config is None"));
		}
		if (HighlightBtnTexture.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(HighlightBtnTexture.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"HighlightBtnTexture\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("; \"HighlightBtnTexture\" config is None"));
		}
		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}


	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/**
* 快捷栏接口
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UQuickBarInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UQuickBarInterface();
	~UQuickBarInterface();
	static FString GetName() { return TEXT("QuickBarInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleQuickBarInterface.BP_RoleQuickBarInterface_C'"); } //获取蓝图对象路径

	virtual void onLeaveWorld() override;

	/**
	* BlueprintCallable，更新快捷栏Item
	*
	* @param Index 快捷栏位置
	* @param QbType 快捷栏类型
	* @param Id 快捷栏ID
	* @param BindType 快捷栏绑定类型
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarInterface")
	void UpdateQBItem(int32 Index, int32 QbType, int32 Id, int32 BindType, int32 QuickID, FString petUid );

	/**
	* BlueprintCallable，交换快捷栏Item
	*
	* @param SrcIndex 快捷栏源位置
	* @param DstIndex 快捷栏目标位置
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarInterface")
	void ExchangeQBItem(int32 SrcIndex, int32 DstIndex);

	/**
	* BlueprintCallable，移除快捷栏Index位置的Item
	*
	* @param Index 快捷栏位置
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarInterface")
	void RemoveQBItem(int32 Index);

	/**
	* Define method
	* BlueprintCallable，服务器回调更新快捷栏Item，修改QbItemList数据
	*
	* @param Index 快捷栏位置
	* @param QbType 快捷栏类型
	* @param Id 快捷栏ID
	* @param BindType 快捷栏绑定类型
	* @param Page 快捷栏页（区分心法的，不是翻页）
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "QuickBarInterface")
		void CLIENT_OnUpdateQBItem(int32 Index, int32 QbType, int32 Id, int32 BindType, int32 QuickID, int32 Page,const FString& petUid);
	/**
	* Define method
	* BlueprintCallable，服务器回调移除快捷栏Index位置的Item，删除QbItemList数据
	*
	* @param Index 快捷栏位置
	* @param Page 快捷栏页（区分心法的，不是翻页）
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "QuickBarInterface")
		void CLIENT_OnRemoveQBItem(int32 Page, int32 Index);

	UFUNCTION(BlueprintCallable, Category = "QuickBarInterface")
		int32 GetSkillPosture();

	virtual void InitBlueCB() override;

private:
	
	void RPC_BASE_qb_updateItem(int32 Index, int32 QbType, int32 Id, int32 BindType, int32 QuickID, int32 Page, FString petUid);

	void RPC_BASE_qb_exchangeItem(int32 SrcIndex, int32 DstIndex, int32 Page);

	void RPC_BASE_qb_removeItem(int32 DstIndex, int32 Page);

};
