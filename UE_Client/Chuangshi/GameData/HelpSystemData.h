#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "HelpSystemData.generated.h"

/**
* 文件名称：HelpSystemData.h
* 功能说明：帮助系统数据定义
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-9-25
*/

///@struct FHelpGrowExperDetailData 成长帮助具体信息
USTRUCT(BlueprintType)
struct CHUANGSHI_API FHelpGrowExperDetailData
{
	GENERATED_USTRUCT_BODY()
public:
	///节点名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "GrowExperDetailData")
		FString NodeName;
	///节点详细内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "GrowExperDetailData")
		FString NodeContent;
};

///@struct FHelpGrowExperData 成长帮助配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FHelpGrowExperData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FHelpGrowExperData() {};
public:
	///等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "GrowExperData")
		int32 Level = 0;
	///节点数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "GrowExperData")
		TArray<FHelpGrowExperDetailData> Nodes;
};

///@struct FHelpQAData 问答帮助配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FHelpQAData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///问题
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "HelpQAData")
		FString Question;
	///回答
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "HelpQAData")
		FString Answer;
};

///@struct FTreeViewData 树节点配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTreeViewData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///索引
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TreeViewData")
		int32 Index;
	///节点ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TreeViewData")
		int32 ID;
	///父节点ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TreeViewData")
		int32 ParentID;
	///节点层级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TreeViewData")
		int32 Layer;
	///节点名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TreeViewData")
		FString Title;
	///点击节点显示的内容，配置ID指向另一张内容表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TreeViewData")
		int32 ContentID = 0;
};

///@struct FHelpOperateGuideData 操作指引帮助配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FHelpOperateGuideData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///索引
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "HelpOperateGuideData")
		int32 Index;
	///问答内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "HelpOperateGuideData")
		TArray<FHelpQAData> QADatas;
};