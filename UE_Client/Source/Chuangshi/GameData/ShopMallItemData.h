// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "Item/ItemBase.h"
#include "JsonReader.h"
#include "JsonSerializer.h"
#include "ShopMallItemData.generated.h"

/**
* 文件名称：ShopMallItemData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-04-07
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FShopMallItemData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FShopMallItemData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Id")
		FString Id;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MallType")
		FString MallType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemID")
		int32 ItemID = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemType")
		int32 ItemType = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SubItemType")
		int32 SubItemType = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Amount")
		int32 Amount = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Price")
		FString Price;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Description")
		FString Description;

	///是否可以使用优惠劵
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsCoupons")
		int32 IsCoupons = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "OpenRule")
		FString OpenRule;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		bool bHasError = false;

		TSharedRef<TJsonReader<TCHAR>> JsonReader = TJsonReaderFactory<TCHAR>::Create(Price);
		TSharedPtr<FJsonObject> JsonParsed;
		bool bDeserialized = FJsonSerializer::Deserialize(JsonReader, JsonParsed);
		if (!bDeserialized)
		{
			bHasError = true;
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Price\" config error"));
		}
		/*else
		{
			TArray<FString> Keys;
			JsonParsed->Values.GetKeys(Keys);
			FJsonObject& JosnObject = *JsonParsed.Get();
			for (auto& Key : Keys)
			{
				FString Value = JosnObject.GetStringField(Key);
			}
		}*/
		JsonReader = TJsonReaderFactory<TCHAR>::Create(OpenRule);
		bDeserialized = FJsonSerializer::Deserialize(JsonReader, JsonParsed);
		if (!bDeserialized)
		{
			if (bHasError)
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"OpenRule\" config error"));
			}
			else
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"OpenRule\" config error"));
			}
		}

	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
USTRUCT(BlueprintType)
struct CHUANGSHI_API FShopMallItem
{
	GENERATED_USTRUCT_BODY()
		FShopMallItem() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Id")
		FString Id;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Item")
		UItemBase* Item = nullptr;
};

/**
*商城首页超链接配置表
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMallHomeLinkData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString GoodsId;

	///链接类型
	///	0：热销商品
	///	1：专题推荐
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 LinkType = 0;

	///推送模板类型
	///	true：是推送模板
	///	false：不是推送模板
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool isTuisong;

	///编号对应贴图路径
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
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath\" is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/**
*商城类型配置表
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMallItemTypeData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///商品类型名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ItemTypeName;

	///商品大类
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ItemCategory = 0;
};

/**
*商城优惠劵
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCouponData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FCouponData() {};
public:
	///优惠劵ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CouponId")
		FString CouponId;
	///优惠劵名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CouponName")
		FString CouponName;
	///折扣
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Discount")
		float Discount = 0.0f;
	///时限
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TimeLimit")
		int32 TimeLimit = 0;
	///适用的商城
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MallType")
		FString MallType;
	///适用的商品类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemType")
		int32 ItemType = 0;
	///适用的商品子类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SubItemType")
		int32 SubItemType = 0;
};

/**
*商城优惠劵
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCouponItemData
{
	GENERATED_USTRUCT_BODY()
		FCouponItemData() {};
public:
	///优惠劵ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CouponId")
		FString CouponId;
	///优惠劵UID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CouponUid")
		FString CouponUid;
	bool operator ==(const FCouponItemData& other)
	{
		if (other.CouponUid == CouponUid)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};