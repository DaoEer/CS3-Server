// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "GameData/UIDataDefine.h"
#include "UIConfigData.generated.h"

/**
* 文件名称：UIManagerData.h
* 功能说明：UI界面管理数据
* 文件作者：zhengdan
* 目前维护：zhangdan
* 创建时间：2016-9-12
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FUIConfigData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FUIConfigData() {};
public:
	///界面类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "WinType")
		FString WinType = TEXT("");
	///备注说明，说明是什么界面，程序不使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "Remarks")
		FString Remarks;
	///加载类型（0：使用时加载；1：预加载）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "LoadType")
		int32 LoadType = 0;
	///离开地图时清理界面处理（0：销毁；1：隐藏；2：不处理），默认销毁
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "DestroyType")
		int32 DestroyType = 0;
	///界面蓝图类路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "Widget")
		TSoftClassPtr<UObject> Widget = nullptr;
	///界面层级，默认1
	///	0:总是在底层，1:普通窗口，2:tip消息等，3:loading界面
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "PosZSegment")
		int32 PosZSegment = 1;
	///界面是否可拖拽
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "IsMoveable")
		bool IsMoveable = true;
	///标示窗口是否可被激活
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "IsActivable")
		bool IsActivable = true;
	///如果为 False，鼠标点击在窗口上时，仍然判断鼠标点击的是屏幕
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "IsHitable")
		bool IsHitable = true;
	///按 esc 键是否会隐藏
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "IsEscHide")
		bool IsEscHide = true;
	///获取/设置相对其父UI的水平停靠方式："LEFT", "CENTER", "RIGHT","HFILL", "S_LEFT", "S_CENTER", "S_RIGHT"
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "H_DockStyle")
		EUIHDOCKSTYLE H_DockStyle = EUIHDOCKSTYLE::CENTER;
	///获取/设置相对其父UI的垂直停靠方式："TOP", "MIDDLE", "BOTTOM","VFILL", "S_TOP", "S_MIDDLE", "S_BOTTOM"
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "V_DockStyle")
		EUIVDOCKSTYLE V_DockStyle = EUIVDOCKSTYLE::MIDDLE;
	///获取/设置左距( 像素坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "Left")
		float Left = 0;	
	///获取/设置顶距( 像素坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "Top")
		float Top = 0;
	///获取/设置水平中距( 像素坐标 ),偏左设置负数，偏右设置正数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "Center")
		float Center = 0;
	///获取/设置垂直中距( 像素坐标 ),偏上设置负数，偏下设置正数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "Middle")
		float Middle = 0;
	///获取/设置右距( 像素坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "Right")
		float Right = 0;
	///获取/设置底距( 像素坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "Bottom")
		float Bottom = 0;
	///获取/设置左距( 相对坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "R_Left")
		float R_Left = 0;
	///获取/设置顶距( 相对坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "R_Top")
		float R_Top = 0;
	///获取/设置水平中距( 相对坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "R_Center")
		float R_Center = 0.5;
	///获取/设置垂直中距( 相对坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "R_Middle")
		float R_Middle = 0.5;
	///获取/设置右距( 相对坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "R_Right")
		float R_Right = 1;
	///获取/设置底距( 相对坐标 )
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "UIConfigData", DisplayName = "R_Bottom")
		float R_Bottom = 1;
};

///@struct FCS3TipsData tips配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCS3TipsData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///tips内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Tips;
	///备注说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Comment;
};

///@struct FSystemBtnData 功能按钮配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFunctionBtnData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///Normal状态贴图
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> NormalTexture;
	///Hovered状态贴图
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> HoveredTexture;
	///Pressed状态贴图
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> PressedTexture;
	///Disable状态贴图
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> DisableTexture;
	///贴图Size
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector2D Size;
	///活动ICON位置（只有活动类型的ICON才需要填），用|隔开，例 1|1 表示第一行第一个
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString BtnPosition;
	///系统界面类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString WindowType;
	///系统快捷键
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ActName;
	///备注说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Comment;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		bool NormalTextureResult = checkTexture(ResultInfo, NormalTexture, FString("NormalTexture"));
		bool HoveredTextureResult = checkTexture(ResultInfo, HoveredTexture, FString("HoveredTexture"));
		bool PressedTextureResult = checkTexture(ResultInfo, PressedTexture, FString("PressedTexture"));
		bool DisableTextureResult = checkTexture(ResultInfo, DisableTexture, FString("DisableTexture"));
		bool SizeResult = Size.X > 0 && Size.Y > 0;
		bool BtnPositionResult = true;
		if (!BtnPosition.TrimStartAndEnd().IsEmpty()) BtnPositionResult = SplitString(BtnPosition)[0].TrimStartAndEnd().IsNumeric() && SplitString(BtnPosition)[1].TrimStartAndEnd().IsNumeric();
		bool WindowTypeResult = !WindowType.TrimStartAndEnd().IsEmpty();
		if (NormalTextureResult && HoveredTextureResult && PressedTextureResult && DisableTextureResult && SizeResult && BtnPositionResult && WindowTypeResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			if (!SizeResult) ResultInfo.CheckLog += FString::Printf(TEXT("Size is config error!  "));
			if (!BtnPositionResult) ResultInfo.CheckLog += FString::Printf(TEXT("BtnPosition is config error!  "));
			if (!WindowTypeResult) ResultInfo.CheckLog += FString::Printf(TEXT("WindowType cannot be empty!  "));
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	};
	bool checkTexture(RowCheckResultInfo& ResultInfo, TSoftObjectPtr<UTexture2D> TexturePath, FString TextureName)
	{
		if (TexturePath.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(TexturePath.ToString()))
			{
				ResultInfo.CheckLog += FString::Printf(TEXT("%s resource does not exist!  "), *TextureName);
				return false;
			}
		}
		else
		{
			ResultInfo.CheckLog += FString::Printf(TEXT("%s config is None!  "), *TextureName);
			return false;
		}
		return true;
	};
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCS3ItemQualityData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//品质名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString QualityName;
	//品质颜色
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FColor QualityColor;
	//品质框贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> QualityTexturePath;
	//tips品质底图贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> TipsTexturePath;
};