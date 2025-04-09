#pragma once
#include "CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "SpaceDynamicEffectData.generated.h"

/**
* 文件名称：SpaceDynamicEffectData.h
* 功能说明：副本效果数据
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-08-08
*/

class UBaseEffect;

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSPACEDYNAMICEFFECT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	/**ClassType：Class'/Script/CS3.CreateEntityEffect'
	*	Param1：entity模型ID|模型大小|模型碰撞类型(模型碰撞类型三类：COLLISION_DEFAULT(如桥)、COLLISION_NONE、COLLISION_ENEMY)
			   |是否可以寻路(默认为0不可寻路 ，1：可寻路)|是否与摄像机发生碰撞|是否与可见的对象发生碰撞
	*	Param2：生成entity的UID
	*	Param3：entity位置朝向(位置和朝向直接用“|”分隔 位置之间XYZ用“；”分隔)
	*	Param4：播放动作和时间间隔(动作|时间间隔|是否随机直接用“|”分隔 动作之间用“；”分隔)
	*	Param5：播放光效和时间间隔(光效|时间间隔|是否随机直接用“|”分隔 光效之间用“；”分隔)
	*ClassType：Class'/Script/CS3.ChangeEntityEffect'
	*	Param1：改变entity的UID
	*	Param2：动作|时间间隔|是否随机直接用“|”分隔 动作之间用“；”分隔
	*	Param3：播放光效和时间间隔(光效|时间间隔|是否随机直接用“|”分隔 光效之间用“；”分隔)
	*	Param4~5：无
	*ClassType：Class'/Script/CS3.DestroyEntityEffect'
	*	Param1：entity的UID之间用“|”分隔
	*	Param2：销毁时间“|”分隔
	*	Param3：销毁时动作“|”分隔
	*	Param4：销毁时光效“|”分隔
	*	Param5：无
	*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftClassPtr<UBaseEffect> ClassType;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param4;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param5;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "备注")
		FString Remarks;

public:
	void CheckCreateEntityEffectData(RowCheckResultInfo& ResultInfo, bool& bHasError)
	{
		TArray<FString> Param1Data = UGolbalBPFunctionLibrary::SplitString(Param1);
		if (Param1Data.Num() >= 2 && FSTRING_TO_FLOAT(Param1Data[1]) == 0)
		{
			bHasError = true;
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param1\" Index(%d) config error"), 2);
		}
		if (Param1Data.Num() >= 5)
		{
			FString TempParam3 = Param1Data[3].TrimStartAndEnd();
			FString TempParam4 = Param1Data[4].TrimStartAndEnd();
			if ((TempParam3 != "1" && TempParam3 != "0") || (TempParam4 != "1" && TempParam4 != "0"))
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param1\" Index(%d) or Index(%d) config error"), 4, 5);
			}
		}
		if (Param2.TrimStartAndEnd() != "0" && FSTRING_TO_INT(Param2) == 0)
		{
			bHasError = true;
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param2\" config error"));
		}

		TArray<FString> Param3Data = UGolbalBPFunctionLibrary::SplitString(Param3);
		if (Param3Data.Num() > 1)
		{
			bool bParam3Error = false;
			TArray<FString> PosParam = UGolbalBPFunctionLibrary::SplitString(Param3Data[0], false, ";");
			if (PosParam.Num() > 2)
			{
				FString TempPos1 = PosParam[0].TrimStartAndEnd();
				FString TempPos2 = PosParam[1].TrimStartAndEnd();
				FString TempPos3 = PosParam[2].TrimStartAndEnd();
				if (((TempPos1 != "0" && TempPos1 != "0.0") && FSTRING_TO_FLOAT(TempPos1) == 0)
					|| ((TempPos2 != "0" && TempPos2 != "0.0") && FSTRING_TO_FLOAT(TempPos2) == 0)
					|| ((TempPos3 != "0" && TempPos3 != "0.0") && FSTRING_TO_FLOAT(TempPos3) == 0))
				{
					bParam3Error = true;
				}

			}
			TArray<FString> DirParam = UGolbalBPFunctionLibrary::SplitString(Param3Data[1], false, ";");
			if (DirParam.Num() > 2)
			{
				FString TempDir1 = DirParam[0].TrimStartAndEnd();
				FString TempDir2 = DirParam[1].TrimStartAndEnd();
				FString TempDir3 = DirParam[2].TrimStartAndEnd();
				if (((TempDir1 != "0" && TempDir1 != "0.0") && FSTRING_TO_FLOAT(TempDir1) == 0)
					|| ((TempDir2 != "0" && TempDir2 != "0.0") && FSTRING_TO_FLOAT(TempDir2) == 0)
					|| ((TempDir3 != "0" && TempDir3 != "0.0") && FSTRING_TO_FLOAT(TempDir3) == 0))
				{
					bParam3Error = true;
				}
			}
			if (bParam3Error)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param3\" config error"));
			}
		}

		TArray<FString> Param4Data = UGolbalBPFunctionLibrary::SplitString(Param4);
		if (Param4Data.Num() > 1)
		{
			bool bParam4Error = false;
			TArray<FString> TempData = UGolbalBPFunctionLibrary::SplitString(Param4Data[1], false, ";");
			for (auto& Data : TempData)
			{
				if (Data.TrimStartAndEnd() != "0" && Data.TrimStartAndEnd() != "0.0" && FSTRING_TO_FLOAT(Data) == 0)
				{
					bParam4Error = true;
					break;
				}
			}
			if (Param4Data.Num() > 2)
			{
				if (Param4Data[2].TrimStartAndEnd() != "0" && Param4Data[2].TrimStartAndEnd() != "0.0" && FSTRING_TO_INT(Param4Data[2]) == 0)
				{
					bParam4Error = true;
				}
			}
			if (bParam4Error)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param4\" config error"));
			}
		}
		TArray<FString> Param5Data = UGolbalBPFunctionLibrary::SplitString(Param5);
		if (Param5Data.Num() > 1)
		{
			bool bParam4Error = false;
			TArray<FString> TempData = UGolbalBPFunctionLibrary::SplitString(Param5Data[1], false, ";");
			for (auto& Data : TempData)
			{
				if (Data.TrimStartAndEnd() != "0" && Data.TrimStartAndEnd() != "0.0" && FSTRING_TO_FLOAT(Data) == 0)
				{
					bParam4Error = true;
					break;
				}
			}
			if (Param5Data.Num() > 2)
			{
				if (Param5Data[2].TrimStartAndEnd() != "0" && FSTRING_TO_INT(Param5Data[2]) == 0)
				{
					bParam4Error = true;
				}
			}
			if (bParam4Error)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param5\" config error"));
			}
		}
	}

	void CheckSkyEffectData(RowCheckResultInfo& ResultInfo, bool& bHasError)
	{
		FString TempParam3 = Param3.TrimStartAndEnd();
		if (TempParam3 != "" && TempParam3 != "0" && TempParam3 != "0.0")
		{
			if (FSTRING_TO_FLOAT(TempParam3) == 0)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param3\" config error"));
			}
		}
	}

	void CheckChangeEntityEffectData(RowCheckResultInfo& ResultInfo, bool& bHasError)
	{
		if (Param1.TrimStartAndEnd() != "0" && FSTRING_TO_INT(Param1) == 0)
		{
			bHasError = true;
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param1\" config error"));
		}
		TArray<FString> Param2Data = UGolbalBPFunctionLibrary::SplitString(Param2);
		if (Param2Data.Num() > 1)
		{
			bool bParam2Error = false;
			TArray<FString> TempData = UGolbalBPFunctionLibrary::SplitString(Param2Data[1], false, ";");
			for (auto& Data : TempData)
			{
				if (Data.TrimStartAndEnd() != "0" && Data.TrimStartAndEnd() != "0.0" && FSTRING_TO_FLOAT(Data) == 0)
				{
					bParam2Error = true;
					break;
				}
			}
			if (Param2Data.Num() > 2)
			{
				if (Param2Data[2].TrimStartAndEnd() != "0" && FSTRING_TO_INT(Param2Data[2]) == 0)
				{
					bParam2Error = true;
				}
			}
			if (bParam2Error)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param2\" config error"));
			}
		}

		TArray<FString> Param3Data = UGolbalBPFunctionLibrary::SplitString(Param3);
		if (Param3Data.Num() > 1)
		{
			bool bParam3Error = false;
			TArray<FString> TempData = UGolbalBPFunctionLibrary::SplitString(Param3Data[1], false, ";");
			for (auto& Data : TempData)
			{
				if (Data.TrimStartAndEnd() != "0" && Data.TrimStartAndEnd() != "0.0" && FSTRING_TO_FLOAT(Data) == 0)
				{
					bParam3Error = true;
					break;
				}
			}
			if (Param3Data.Num() > 2)
			{
				if (Param3Data[2].TrimStartAndEnd() != "0" && FSTRING_TO_INT(Param3Data[2]) == 0)
				{
					bParam3Error = true;
				}
			}
			if (bParam3Error)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param3\" config error"));
			}
		}
	}

	void CheckDestroyEntityEffectData(RowCheckResultInfo& ResultInfo, bool& bHasError)
	{
		TArray<FString> Param1Data = UGolbalBPFunctionLibrary::SplitString(Param1);
		TArray<FString> Param2Data = UGolbalBPFunctionLibrary::SplitString(Param2);
		for (auto& Data: Param1Data)
		{
			if (Data.TrimStartAndEnd() != "0" && FSTRING_TO_INT(Data) == 0)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param1\" config error"));
				break;
			}
		}
		for (auto& Data : Param2Data)
		{
			if (Data.TrimStartAndEnd() != "0" && Data.TrimStartAndEnd() != "0.0" && FSTRING_TO_FLOAT(Data) == 0)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param2\" config error"));
				break;
			}
		}
	}

	void CheckCreateEffectByScriptData(RowCheckResultInfo& ResultInfo, bool& bHasError)
	{
		TArray<FString> Param2Data = UGolbalBPFunctionLibrary::SplitString(Param2);
		FVector Pos;
		FRotator Direction;
		if (Param2Data.Num() > 1)
		{
			bool bParam2Error = false;
			TArray<FString> PosParam = UGolbalBPFunctionLibrary::SplitString(Param2Data[0], false, ";");
			if (PosParam.Num() > 2)
			{
				FString Pos0 = PosParam[0].TrimStartAndEnd();
				FString Pos1 = PosParam[1].TrimStartAndEnd();
				FString Pos2 = PosParam[2].TrimStartAndEnd();
				if ((Pos0 != "0" && Pos0 != "0.0" && FSTRING_TO_FLOAT(Pos0) == 0)
					|| (Pos1 != "0" && Pos1 != "0.0" && FSTRING_TO_FLOAT(Pos1) == 0)
					|| (Pos2 != "0" && Pos2 != "0.0" && FSTRING_TO_FLOAT(Pos2) == 0)
					)
				{
					bParam2Error = true;
				}
			}
			TArray<FString> DirParam = UGolbalBPFunctionLibrary::SplitString(Param2Data[1], false, ";");
			if (DirParam.Num() > 2)
			{
				FString Dir0 = DirParam[0].TrimStartAndEnd();
				FString Dir1 = DirParam[1].TrimStartAndEnd();
				FString Dir2 = DirParam[2].TrimStartAndEnd();
				if ((Dir0 != "0" && Dir0 != "0.0" && FSTRING_TO_FLOAT(Dir0) == 0)
					|| (Dir1 != "0" && Dir1 != "0.0" && FSTRING_TO_FLOAT(Dir1) == 0)
					|| (Dir2 != "0" && Dir2 != "0.0" && FSTRING_TO_FLOAT(Dir2) == 0)
					)
				{
					bParam2Error = true;
				}
			}
			if (bParam2Error)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"Param2\" config error"));
			}
		}
	}

	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		bool bHasError = false;

		FString TypeName = ClassType.GetAssetName();
		if (TypeName == "CreateEntityEffect")
		{
			CheckCreateEntityEffectData(ResultInfo, bHasError);
		}
		else if (TypeName == "SkyEffect")
		{
			CheckSkyEffectData(ResultInfo, bHasError);
		}
		else if (TypeName == "ChangeEntityEffect")
		{
			CheckChangeEntityEffectData(ResultInfo, bHasError);
		}
		else if (TypeName == "DestroyEntityEffect")
		{
		}
		else if (TypeName == "CreateEffectByScript")
		{
			CheckCreateEffectByScriptData(ResultInfo, bHasError);
		}
		if (bHasError)
		{
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: ")) + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

///创建entity的数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCREATE_ENTITY_EFFECT_DATA
{
	GENERATED_USTRUCT_BODY()

	FString ModelNumber;///<模型ID
	float ModelScale = 1.0f;///<缩放
	FString CollisionType ;///<碰撞		
	bool bAffectNavigation = false;///<是否影响寻路
	bool bCameraCollision = false;///<是否与摄像机发生碰撞
	bool bVisibilityCollision = false;///<是否与可见的对象发生碰撞
	FVector Pos;///<生成的位置
	FRotator Direction;///<生成朝向
	bool bIsRandomAction = false;///<动作是否随机
	TArray<FString> ActionNames;///<动作名
	TArray<float> ActionIntervals;///<动作间隔
	bool bIsRandomEffect = false; ///<光效是否随机
	TArray<FString> EffectIDs;///<光效ID
	TArray<float> EffectIntervals;///<光效间隔时间
};

///天气效果
UENUM()
enum class ESKYEFFECTENUM :uint8
{
	None,
	Environment,
	SkyMaterial,
};
