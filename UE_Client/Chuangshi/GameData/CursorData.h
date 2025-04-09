#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "GameData/UIDataDefine.h"
#include "GameData/Barracks/RoleBarracksItemData.h"
#include "CursorData.generated.h"

/**
* 文件名称：CursorData.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：zhangdan
* 创建时间：2017-08-30
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCURSOR_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///鼠标图片
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UObject> CursorTexture;

	///鼠标图片Size
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector2D TextureSize;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		if (CursorTexture.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(CursorTexture.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"CursorTexture\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"CursorTexture\" config is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

///左键抓取、拖拽数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FDragDropOperationData
{
	GENERATED_USTRUCT_BODY()
public:
	///来源
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		EDRAGSOURCE Source;
	///物品UID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString UID;
	///物品绝对位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 AbsOrderID = 0;
	///物品相对位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SlotIndex = 0;
	///快捷栏类型（ConstDataBP.h有定义）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 QbType = 0;
	///快捷栏道具ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 QbID = 0;
	///快捷栏容器ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 QuickID = 0;
	///道具绑定类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BindType = 0;
};

///养兵部队左键抓取、拖拽数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FArmsDragDropOperationData
{
	GENERATED_USTRUCT_BODY()
public:
	///分类
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Category;
	///ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	///士兵类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ENUM_BARRACKS_SOLDIER_TYPE soldierType;
	///部队id
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ArmID = 0;
	///士兵信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FROLEBARRACKSITEMDATA RoleBarrachsItemData;
};