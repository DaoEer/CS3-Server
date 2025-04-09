#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "StoreGoodsDataTable.generated.h"

/**
* 文件名称：StoreGoodsDataTable.h
* 功能说明：商城商品表数据结构
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-04-22
*/

/** 商城商品表数据结构 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_GOODS_DATA_TABLE : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "ID")
		int32 ID = 0;
	///商品类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "GoodsType")
		int32 GoodsType = 0;
	///商品状态
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "GoodsState")
		int32 GoodsState = 0;
	///物品类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "ItemType")
		int32 ItemType = 0;
	///三级标签
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "ThirdLable")
		int32 ThirdLable = 0;
	///物品ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "ItemID")
		int32 ItemID = 0;
	///价格
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "Price")
		int32 Price = 0;
	///限时购买
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "LimitTime")
		FString LimitTime;
	///限制购买次数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "LimitAmount")
		int32 LimitAmount = -1;
	///全服限制购买次数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "ServeLimitAmount")
		int32 ServeLimitAmount = -1;
	///折扣时间
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "DiscountTime")
		FString DiscountTime;
	//折扣价
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "DiscountPrice")
		int32 DiscountPrice = 0;
	///刷新类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "RefreshType")
		int32 RefreshType = 0;
	///玄石返回倍率
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "RebateRate")
		float RebateRate = 0.0;
	///描述
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "Description")
		FString Description;
	///数量
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_GOODS_DATA_TABLE", DisplayName = "Amount")
		int32 Amount = 1;
};

/** 商城推荐商品数据结构 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_RECOMMENT_GOODS_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 ID;
	///是否推荐到首页
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		bool IsHome;
	///是否推荐到推荐商品
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		bool IsRecomment;
};

/** 商城推送商品数据结构 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_PUSH_GOODS_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 ID;
	///链接路径，格式：一级标签页.二级标签页，如0.2，表示推荐商品的灵丹妙药标签页
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString LinkPath;
	///贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> TexturePath;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (TexturePath.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(TexturePath.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath\" config is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_SUB_PAGE_DATA
{
	GENERATED_BODY()
	
	///二级标签，0：全部，1：衣服，2：发型，3：头饰，4：面饰，5：背饰，6：腰饰，7：披风，8：环身，9：光效，10：秘宝，11：杂货，12：点卡；格式如：1|衣服
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString SecondPageType;
	///三级标签，0：全部，1：男修士，2：女修士；格式如：1|男修士
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		TArray<FString> ThirdPageType;
};

/** 商城标签页配置表数据结构 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_PAGE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///一级标签，0：首页，1：外观，2：坐骑，3：天材地宝，4：玄石专区；格式如：1|外观
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString FirstPageType;
	///二级标签，0：全部，1：衣服，2：发型，3：头饰，4：面饰，5：背饰，6：腰饰，7：披风，8：环身，9：光效，10：秘宝，11：杂货，12：点卡；格式如：1|衣服
	///三级标签，0：全部，1：男修士，2：女修士；格式如：1|男修士
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		TArray<FSTORE_SUB_PAGE_DATA> SubPageType;
};

/** 商城搜索表 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_SEARCH_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:

	///商品名
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString ItemName;
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 GoodsID;
};

/** 商城表情动作配置 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_EMOTEACTION_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///动作ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString ActionID;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString Remarks;
};

/** 商城云裳阁模型调整配置 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_MODEL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///模型位置偏移
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FVector DeltaLocation;
	///模型大小
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FVector Scale3D = FVector(1.0f, 1.0f, 1.0f);
};

/** 商城外观背饰的参数 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_BACK_ADORN_PARAM : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///相对位置
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FVector Location;
	///相对旋转
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FRotator Rotation;
};