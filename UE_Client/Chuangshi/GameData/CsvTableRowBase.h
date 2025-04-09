#pragma once
#include "Engine/DataTable.h"
#include "PackageName.h"
#include "FileManager.h"
#include "ModuleManager.h"
#include "AssetRegistryModule.h"
#include "AssetData.h"
#include "CsvTableRowBase.generated.h"


/**
* 文件名称：CsvTableRowBase.h
* 功能说明：所有配置表结构体的基类，此类公开了RowName
* 文件作者：ranxuanwen
* 目前维护：wuxiaoou
* 创建时间：2016-09-07
*/
enum CheckResult
{
	//没有重载
	Unrealized,
	//检查正确
	Ok,
	//检查错误
	Error,
};

struct RowCheckResultInfo
{
	FName RowName;
	CheckResult Result;
	FString CheckLog;
};

USTRUCT()
struct FCSV_TABLE_ROW_BASE : public FTableRowBase
{
	GENERATED_BODY()
	friend class UCsvBaseDataManager;
	friend class UResourceManager;
public:
	///配置表默认行名（建议将ID设置为默认值，不需要表头字符）
	FName RowName;

	//检查数据是否正常
	virtual bool Check() const
	{
		return true;
	};
private:
	inline void SetRowName(const FName& NewRowName)
	{
		RowName = NewRowName;
	};

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		ResultInfo.Result = CheckResult::Unrealized;
	};

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};

	virtual bool GetIsBackstageAsyncLoad()
	{
		return true;
	};

	bool CheckResourceFileIsExist(const FString& ResourceFile)
	{
		FString NewResourceFile = ResourceFile;
		int32 NameStartIndex = INDEX_NONE;
		NewResourceFile.FindChar(TCHAR('\''), NameStartIndex);
		if (NameStartIndex != INDEX_NONE)
		{
			int32 NameEndIndex = INDEX_NONE;
			NewResourceFile.FindLastChar(TCHAR('\''), NameEndIndex);
			if (NameEndIndex > NameStartIndex)
			{
				NewResourceFile = NewResourceFile.Mid(NameStartIndex + 1, NameEndIndex - NameStartIndex - 1);
			}
			else
			{
				return false;
			}
		}
		if (!FPackageName::IsValidObjectPath(NewResourceFile))
		{
			return false;
		}
		FString PackageName = FPackageName::ObjectPathToPackageName(NewResourceFile);
		FString FilePath;
		// Try to convert this to a file path
		if (FPackageName::DoesPackageExist(PackageName, 0, &FilePath) == false)
		{
			return false;
		}

		// if that succeeded FilePath will be a relative path to a  file, if not just assume that's what we were given and proceed...
		if (IFileManager::Get().FileExists(*FilePath) == false)
		{
			return false;
		}

		const FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>(TEXT("AssetRegistry"));
		const FAssetData AssetData = AssetRegistryModule.Get().GetAssetByObjectPath(*ResourceFile);

		if (AssetData.IsValid())
		{
			return true;
		}
		return false;
	};

	bool CheckIsScriptPackage(const FString& ResourceFile)
	{
		return FPackageName::IsScriptPackage(ResourceFile);
	};

	bool CheckScriptSoftPtrIsValid(TSoftClassPtr<UObject> SoftClassPtr)
	{
		UClass* targetClass = SoftClassPtr.Get();
		if (!IsValid(targetClass))
		{
			targetClass = SoftClassPtr.LoadSynchronous();
		}
		if (targetClass)
		{
			return true;
		}
		return false;
	};

	bool CheckScriptSoftPtrIsValid(TSoftObjectPtr<UObject> SoftObjPtr)
	{
		UObject* targetObj = SoftObjPtr.Get();
		if (!IsValid(targetObj))
		{
			targetObj = SoftObjPtr.LoadSynchronous();
		}
		if (targetObj)
		{
			return true;
		}
		return false;
	};

	/**
	*FString字符串拆分，此方法和UGolbalBPFunctionLibrary的SplitString功能一样，但是
	*在定义结构体的头文件引用UGolbalBPFunctionLibrary的方法可能会导致报错。
	*
	*@param	InString 需要拆分字符串
	*@param	IsElemUnique 是否保持分割出来数组元素唯一
	*@param	SplitChar 分隔符号
	*
	*@return TArray<FString> 引擎提供类似方法ParseIntoArray
	*/
	TArray<FString> SplitString(const FString& InString, bool IsElemUnique = false, FString SplitChar = "|")
	{
		TArray<FString> SplitArray;
		FString SplitStr(InString);
		FString Left, Right;
		bool Result = true;
		while (!SplitStr.IsEmpty())
		{
			Result = SplitStr.Split(SplitChar, &Left, &Right, ESearchCase::Type::CaseSensitive);
			if (Result)
			{
				SplitStr = Right;
				if (IsElemUnique)
					SplitArray.AddUnique(Left);
				else
					SplitArray.Add(Left);
			}
			else
			{
				if (IsElemUnique)
					SplitArray.AddUnique(SplitStr);
				else
					SplitArray.Add(SplitStr);
				SplitStr = TEXT("");
			}
		}
		return SplitArray;
	}

	bool CheckPosDirCheckData(RowCheckResultInfo& ResultInfo, FString Param, FString ParamName, FString SplitText = " ")
	{
		TArray<FString> ParamSplit = SplitString(Param.TrimStartAndEnd(), false, SplitText);
		if (ParamSplit.Num() == 3)
		{
			FString Data0 = ParamSplit[0].TrimStartAndEnd();
			FString Data1 = ParamSplit[1].TrimStartAndEnd();
			FString Data2 = ParamSplit[2].TrimStartAndEnd();
			if ((Data0 != "0" && Data0 != "0.0" && FCString::Atof(*Data0) == 0)
				|| (Data1 != "0" && Data1 != "0.0" && FCString::Atof(*Data1) == 0)
				|| (Data2 != "0" && Data2 != "0.0" && FCString::Atof(*Data2) == 0))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" config error"), *ParamName);
				return false;
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" config error"), *ParamName);
			return false;
		}
		return true;
	}

	bool CheckParamIntData(RowCheckResultInfo& ResultInfo, FString Param, FString ParamName, bool bNeedSplit = true, FString SplitText = " ")
	{
		TArray<FString> ParamSplit;
		if (bNeedSplit)
		{
			ParamSplit = SplitString(Param.TrimStartAndEnd(), false, SplitText);
		}
		else
		{
			ParamSplit.Add(Param);
		}

		for (auto& Split : ParamSplit)
		{
			if (Split.TrimStartAndEnd() != "0" && FCString::Atoi(*Split) == 0)
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" config error"), *ParamName);
				return false;
			}
		}
		return true;
	}

	bool CheckParamFloatData(RowCheckResultInfo& ResultInfo, FString Param, FString ParamName, bool bNeedSplit = true, FString SplitText = " ")
	{
		TArray<FString> ParamSplit;
		if (bNeedSplit)
		{
			ParamSplit = SplitString(Param.TrimStartAndEnd(), false, SplitText);
		}
		else
		{
			ParamSplit.Add(Param);
		}

		for (auto& Split : ParamSplit)
		{
			if (Split.TrimStartAndEnd() != "0" && Split.TrimStartAndEnd() != "0.0" && FCString::Atof(*Split) == 0)
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"%s\" config error"), *ParamName);
				return false;
			}
		}
		return true;
	}
};