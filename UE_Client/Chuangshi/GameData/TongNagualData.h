#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "TongNagualData.generated.h"

/**
* 文件名称：PetData.h
* 功能说明：帮会神兽相关数据
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2019-09-20
*/

UENUM(BlueprintType)
enum class TONG_NAGUAL_TYPE: uint8
{
	///青龙
	TYPE_QINGLONG = 1,
	///白虎
	TYPE_BAIHU,
	///玄武
	TYPE_XUANWU,
	///朱雀
	TYPE_ZHUQUE
};


/** 帮会神兽召唤3D模型配置 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTONG_NAGUAL_MODEL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///ModelID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "ModelID")
		FString ModelID = TEXT("");
	///神兽名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "UName")
		FString UName = TEXT("");
	///神兽类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "Type")
		TONG_NAGUAL_TYPE Type;
	///神兽等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "Level")
		int32 Level;
	///气血
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "Qixue")
		int32 Qixue;
	///外攻攻击
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "WaiGong")
		int32 WaiGong;
	///内攻攻击
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "NeiGong")
		int32 NeiGong;
	///外攻防御
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "WaiFang")
		int32 WaiFang;
	///内攻防御
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "NeiFang")
		int32 NeiFang;
	///神兽文案判词
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "CopyVerdictDes")
		FString CopyVerdictDes = TEXT("");
	///神兽功能信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "FunctionDes")
		FString FunctionDes = TEXT("");
	///偏移
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "Transform")
		FTransform Transform;
	///摄像机FOV偏移
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FTONG_NAGUAL_MODEL_DATA", DisplayName = "FOVAngle")
		float FOVAngle = 0.0f;
};
