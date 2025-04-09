#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "FaBaoData.generated.h"

/**
* 文件名称：FaBaoData.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2018-06-05
*/


USTRUCT(BlueprintType)
struct CHUANGSHI_API FFABAOMESH_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///法宝类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 FaBaoType = 0;
	///法宝模型ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString FaBaoModelID;
	///法宝大小
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float FaBaoScale;
	///法宝位置偏移
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector FaBaoLocation;
	///法宝待机动作（如果没有得话可以不填）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString FaBaoStandyID;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSPLINE_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///法宝围绕玩家旋转半径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float SplineScale;
	///法宝围绕玩家旋转速度
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float SplineSpeed;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FFABAOSILL_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///法宝动画ID
	///	根据动画流程顺序配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> FaBaoAimID;
	///法宝特效ID
	///	根据动画流程顺序配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> FaBaoEffectID;
	///法宝动画延迟时间（秒）
	///	根据动画流程顺序配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<float> FaBaoPlayTime;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FFABAO_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///法宝数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "FabaoData")
		FFABAOMESH_DATA FabaoMeshData;

	///Splien线条数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSPLINE_DATA SplineData;
	///绑定点名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName SockeName;
	///技能ID，施法技能效果ID，根绝相应的需求效果填写不同的ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SkillID = 0;

	///技能数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FFABAOSILL_DATA SkillData;

	///备注说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "备注")
		FString Remarks;

};