#pragma once

/**
* 文件名称：AreaWallData.h
* 功能说明：光墙数据的UClass
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2017-08-21
*/

/**
*备注：此类获取参数的结构体经常变动，故整合为一个UClass
*/

#include "CS3Object.h"
#include "GameDeFine.h"
#include "AreaWallData.generated.h"

UCLASS(BlueprintType)
class CHUANGSHI_API UAreaWallData : public UCS3Object
{
	GENERATED_BODY()

public:
	static UAreaWallData* GetInstance();

	UFUNCTION(BlueprintCallable, Category = "AreaWall")
	bool SetAreaWallData(const FString RowNumber, AREA_LIGHT_WALL_TYPE_ENUM WallType);

public:
	///区域的坐标数组
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	TArray<FVector> WorldLocation;

	///Z坐标是否有效
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	bool IsValidPosZ;

	///光墙的类型
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	AREA_LIGHT_WALL_TYPE_ENUM WallType;

	///有效落差高度
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	float ValidHeight;

	///等分距离
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	float EqualLength;

	///忽略的对象
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	TArray<FString> Object;

	///射线向上检测的距离
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	float UpLength;

	///射线向下检测的距离
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	float DownLength;

	///光墙高度修正
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	float HeightCorrection;

	///光墙是否闭合
	UPROPERTY(BlueprintReadOnly, Category = "AreaWall")
	bool bIsClose;

/**
private:
	static UAreaWallData* Instance;*/
};