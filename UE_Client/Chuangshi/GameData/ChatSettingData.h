#pragma once
#include "CoreMinimal.h"
#include "ChatType.h"
#include "CsvTableRowBase.h"
#include "ChatSettingData.generated.h"

/**
* 文件名称：ChatSettingData.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-04-20
*/

UENUM(BlueprintType)
enum class FChatTypeSwitchingCondition : uint8
{
	CHAT_NONE,
	CHAT_HAS_GROUP,
	CHAT_HAS_TEAM,
	CHAT_HAS_COLLECTIVE,
	CHAT_HAS_GANG,
	CHAT_IS_ONBATTLESPACE,
	CHAT_WHISPER_NAME,
	CHAT_FORBID,///<禁止
};

///频道设置配置数据（配置表）
USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatChannelCfg : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FChatChannelCfg() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ChatType ChannelType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Shorthand;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FColor Color;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsCanModify;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ShortcutKey;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FChatTypeSwitchingCondition> SwitchingConditions;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 OpenLevel;
};

///频道设置数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatChannelSettingData
{
	GENERATED_USTRUCT_BODY()
		FChatChannelSettingData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ChatType ChannelType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Shorthand;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FColor Color;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsCanModify;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ShortcutKey;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FChatTypeSwitchingCondition> SwitchingConditions;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 OpenLevel;
};

///聊天基础设置数据（配置表）
USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatBaseSettingData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FChatBaseSettingData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsShowTime;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool isHideAuto;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Transparency;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FColor BGColor;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 WinWidth;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 WinHigh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 WinPosX;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 WinPosY;
};

///聊天设置保存数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatSettingData
{
	GENERATED_USTRUCT_BODY()
		FChatSettingData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FChatBaseSettingData BaseSettingData;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FChatChannelCfg> ChannelSettingData;
};

///聊天设置标签页贴图配置数据（配置表）
USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatSettingTabTexture : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FChatSettingTabTexture() {};
public:
	///普通状态贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> Normal;

	///高亮状态贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> Hovered;

	///按下状态贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> Pressed;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		TArray<TSoftObjectPtr<UTexture2D>> TextureData;
		TArray<FString> TextureParams;
		TextureData.Add(Normal);
		TextureData.Add(Hovered);
		TextureData.Add(Pressed);
		TextureParams.Add("Normal");
		TextureParams.Add("Hovered");
		TextureParams.Add("Pressed");

		for (int i = 0; i < TextureData.Num(); i++)
		{
			TSoftObjectPtr<UTexture2D> Texture = TextureData[i];
			if (Texture.ToSoftObjectPath().IsValid())
			{
				if (CheckIsScriptPackage(Texture.ToString()))
				{
					if (!CheckScriptSoftPtrIsValid(Texture))
					{
						ResultInfo.Result = Error;
						ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" resource does not exist"), *TextureParams[i]);
					}
				}
				else if (!CheckResourceFileIsExist(Texture.ToString()))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" resource does not exist"), *TextureParams[i]);
				}
			}
			else
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" config is None"), *TextureParams[i]);
			}
		}
		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

///聊天频道贴图配置数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatChannelBGTexture : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FChatChannelBGTexture() {};
public:
	///普通状态贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> Normal;

	///高亮状态贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> Hovered;

	///按下状态贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> Pressed;

	///消息BG贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> MsgBG;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		TArray<TSoftObjectPtr<UTexture2D>> TextureData;
		TArray<FString> TextureParams;
		TextureData.Add(Normal);
		TextureData.Add(Hovered);
		TextureData.Add(Pressed);
		TextureData.Add(MsgBG);
		TextureParams.Add("Normal");
		TextureParams.Add("Hovered");
		TextureParams.Add("Pressed");
		TextureParams.Add("MsgBG");

		for (int i = 0; i < TextureData.Num(); i++)
		{
			TSoftObjectPtr<UTexture2D> Texture = TextureData[i];
			if (Texture.ToSoftObjectPath().IsValid())
			{
				if (CheckIsScriptPackage(Texture.ToString()))
				{
					if (!CheckScriptSoftPtrIsValid(Texture))
					{
						ResultInfo.Result = Error;
						ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" resource does not exist"), *TextureParams[i]);
					}
				}
				else if (!CheckResourceFileIsExist(Texture.ToString()))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" resource does not exist"), *TextureParams[i]);
				}
			}
			else
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" config is None"), *TextureParams[i]);
			}
		}
		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};