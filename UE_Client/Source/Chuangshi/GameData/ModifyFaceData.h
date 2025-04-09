#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "ModifyFaceData.generated.h"
/**
* 文件名称：ModifyFaceData.h
* 功能说明：脸部数据表格
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2019-02-19
*/

USTRUCT(BlueprintType)
struct FMODIFY_FACE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	// 骨骼的名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace")
	FName BoneName;

	// 对应的颜色通道编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace")
		int32 Index = -1;

	// 对应骨骼名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace")
		FName SymName;

	// 骨骼的Transform
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace")
		FTransform BoneTrans;

	// 骨骼的下标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace")
		int32 BoneIndex;

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMATERIAL_FACE_HIT_RESULT
{
	GENERATED_USTRUCT_BODY()
public:

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace|MaterialHit")
		int MaterialIndex;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ModifyFace|MaterialHit")
		FVector2D UVCoordinates;

	FMATERIAL_FACE_HIT_RESULT()
	{
		MaterialIndex = -1;
		UVCoordinates = FVector2D::ZeroVector;
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBONE_FACE_LIMIT : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	// 骨骼名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PinchFace")
		FName BoneName;

	// 是否可调整位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PinchFace")
		bool doTranslation = true;

	// 是否可调整旋转
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PinchFace")
		bool doRotation = true;

	// 是否可调整缩放
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PinchFace")
		bool doScaling = true;

	// 最小偏移矩阵
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PinchFace")
		FTransform MinTransform = FTransform(FRotator(-30.0f, -30.0f, -30.0f), FVector(-1.0f, -1.0f, -1.0f), FVector(0.8f, 0.8f, 0.8f));

	// 最大偏移矩阵
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PinchFace")
		FTransform MaxTransform = FTransform(FRotator(30.0f, 30.0f, 30.0f), FVector(1.0f, 1.0f, 1.0f), FVector(1.5f, 1.5f, 1.5f));

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCameraConfig
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Variable)
		float	Dis;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Variable)
		FVector Loc;
};


UENUM(BlueprintType)
enum class EMODIFY_TYPE : uint8
{
	Part_Face UMETA(DisplayName = "Face"),
	Part_Body UMETA(DisplayName = "Body"),
	Part_Pose UMETA(DisplayName = "Pose"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FFACE_STYLE_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		int32 ChunZhuangIndex = 0;//嘴唇口红样式

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		float ChunZhuangShape = 0;//口红颜色深度

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		int32 HuXuIndex = 0;//胡须样式

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		int32 LianWenIndex = 0;//脸部纹身样式

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		int32 MeiMaoIndex = 0;//眉毛样式

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		float MeiMaoShape = 0;//眉毛浓度

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		int32 YanXianIndex = 0;//眼线样式

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		int32 SaiHongIndex = 0;//腮红样式

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		float SaiHongShape = 0;//腮红范围

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		int32 YanYingIndex = 0;//眼影样式

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		float YanYingShape = 0;//眼影范围大小

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		float Brighjtness = 1.5f;//眼睛亮度

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		float ColorDepth = 0.5f;//瞳孔颜色深度

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		int32 EyeIndex = 0;//瞳孔样式

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = FaceStyle)
		float EyeScale = 1.2f; //眼睛大小
};