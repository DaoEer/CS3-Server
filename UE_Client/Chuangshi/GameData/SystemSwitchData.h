#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "GameData/CsvTableRowBase.h"
#include "GameData/UIDataDefine.h"
#include "Util/ConvertUtil.h"
#include "SystemSwitchData.generated.h"

/**
* 文件名称：SystemSwitchData.h
* 功能说明：功能开启
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-03-16
*/

///开启条件基类
UCLASS()
class CHUANGSHI_API USystemOpenCNDBase : public UCS3Object
{
	GENERATED_BODY()
};

///关闭条件基类
UCLASS()
class CHUANGSHI_API USystemCloseCNDBase : public UCS3Object
{
	GENERATED_BODY()
};

///表现基类
UCLASS()
class CHUANGSHI_API USystemSwitchACTBase : public UCS3Object
{
	GENERATED_BODY()
};

///开关条件参数
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSystemOpenCNDParam
{
	GENERATED_USTRUCT_BODY()
public:
	///系统索引，程序自动赋值，仅程序用
		FName SystemIndex;
	/*用来指定使用哪个类来处理；
	*SystemOpenLevelCND 类型：Param1（等级）
	*SystemOpenQuestCND 类型：Param1（任务ID）, Param2（任务状态）
	*SystemOpenQuestTaskCND 类型：Param1（任务ID）, Param2（子任务ID），Param3（子任务状态）
	*SystemOpenSpaceCND 类型：Param1（SpaceScriptID，格式：地图1|地图2|地图3）
	*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Script;
	///参数一
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	///参数二
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	///参数三
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
};

///关闭条件参数
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSystemCloseCNDParam
{
	GENERATED_USTRUCT_BODY()
public:
	///系统索引，程序自动赋值，仅程序用
		FName SystemIndex;
	/*用来指定使用哪个类来处理；
	*SystemCloseLevelCND 类型：Param1（等级）
	*SystemCloseQuestCND 类型：Param1（任务ID）, Param2（任务状态）
	*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Script;
	///参数一
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	///参数二
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	///参数三
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
};

///表现参数
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSystemSwitchACTParam
{
	GENERATED_USTRUCT_BODY()
public:
	///系统索引，程序自动赋值，仅程序用
		FName SystemIndex;
	///用来指定使用哪个类来处理；SystemSwitchLightACT、SystemSwitchEffectACT
	/*用来指定使用哪个类来处理；
	*SystemSwitchLightACT 类型：按钮变亮表现（主界面系统、子功能）
	*SystemSwitchEffectACT 类型：光效表现（活动）
	*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Script;
	///系统按钮UI的类型，1 有面板路径UI 2 动态取UI(面板+子节点名字)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 UIType = 0;
	///系统按钮UI的路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString UILinkTarget;
	///系统按钮标记，程序自动赋值，仅程序用
		FName BtnTag;
};

#pragma region	/** 系统开启条件相关 */
///开启条件
UCLASS()
class CHUANGSHI_API USystemOpenBaseCND : public USystemOpenCNDBase
{
	GENERATED_BODY()
public:
	virtual bool CheckOpenCondition(const FSystemOpenCNDParam& CndParams) { return false; }
};

///等级
UCLASS(BlueprintType)
class CHUANGSHI_API USystemOpenLevelCND : public USystemOpenBaseCND
{
	GENERATED_BODY()
public:
	/**
	*CndParams参数一是等级
	*/
	virtual bool CheckOpenCondition(const FSystemOpenCNDParam& CndParams) override;
};

///任务
UCLASS(BlueprintType)
class CHUANGSHI_API USystemOpenQuestCND : public USystemOpenBaseCND
{
	GENERATED_BODY()
public:
	/**
	*CndParams参数一是任务ID, 参数二是任务状态
	*/
	virtual bool CheckOpenCondition(const FSystemOpenCNDParam& CndParams) override;
};

///子任务
UCLASS(BlueprintType)
class CHUANGSHI_API USystemOpenQuestTaskCND : public USystemOpenBaseCND
{
	GENERATED_BODY()
public:
	/**
	*CndParams参数一是任务ID, 参数二是子任务ID，参数三子任务状态
	*/
	virtual bool CheckOpenCondition(const FSystemOpenCNDParam& CndParams) override;
};

/**地图（某些系统只有在某些地图能显示）
*Param1配置 SpaceScriptID，格式：地图1|地图2|地图3
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USystemOpenSpaceCND : public USystemOpenBaseCND
{
	GENERATED_BODY()
public:
	virtual bool CheckOpenCondition(const FSystemOpenCNDParam& CndParams) override;
};

#pragma endregion

#pragma region	/** 关闭条件相关 */

///关闭条件
UCLASS()
class CHUANGSHI_API USystemCloseBaseCND : public USystemCloseCNDBase
{
	GENERATED_BODY()
public:
	virtual bool CheckCloseCondition(const FSystemCloseCNDParam& CndParams) { return false; }
};

///等级
UCLASS(BlueprintType)
class CHUANGSHI_API USystemCloseLevelCND : public USystemCloseBaseCND
{
	GENERATED_BODY()
public:
	virtual bool CheckCloseCondition(const FSystemCloseCNDParam& CndParams) override;
};

///任务
UCLASS(BlueprintType)
class CHUANGSHI_API USystemCloseQuestCND : public USystemCloseBaseCND
{
	GENERATED_BODY()
public:
	virtual bool CheckCloseCondition(const FSystemCloseCNDParam& CndParams) override;
};

#pragma endregion

#pragma region	/** 开启表现相关 */
///开启、关闭表现
UCLASS()
class CHUANGSHI_API USystemSwitchBaseACT : public USystemSwitchACTBase
{
	GENERATED_BODY()
public:
	virtual void DoOpenAction(const FSystemSwitchACTParam& ActParams) {  }
	virtual void DoCloseAction(const FSystemSwitchACTParam& ActParams) {  }
};

///按钮变亮表现（主界面系统、子功能）
UCLASS(BlueprintType)
class CHUANGSHI_API USystemSwitchLightACT : public USystemSwitchBaseACT
{
	GENERATED_BODY()
public:
	virtual void DoOpenAction(const FSystemSwitchACTParam& ActParams) override;
	virtual void DoCloseAction(const FSystemSwitchACTParam& ActParams) override;
};

///光效表现（活动）
UCLASS(BlueprintType)
class CHUANGSHI_API USystemSwitchEffectACT : public USystemSwitchBaseACT
{
	GENERATED_BODY()
public:
	virtual void DoOpenAction(const FSystemSwitchACTParam& ActParams) override;
	virtual void DoCloseAction(const FSystemSwitchACTParam& ActParams) override;
};

#pragma endregion

///开启条件
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSystemOpenCondition
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSystemOpenCNDParam CndParams;
	//UPROPERTY(EditAnywhere, BlueprintReadWrite)
	USystemOpenBaseCND* CndObj;

	virtual ~FSystemOpenCondition() {}

	virtual bool CheckOpenCondition();
};

///关闭条件
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSystemCloseCondition
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSystemCloseCNDParam CndParams;
	//UPROPERTY(EditAnywhere, BlueprintReadWrite)
	USystemCloseBaseCND* CndObj;

	virtual ~FSystemCloseCondition() {}

	virtual bool CheckCloseCondition();
};

///系统开启、关闭表现
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSystemSwitchAction
{
	GENERATED_USTRUCT_BODY()
public:
	///表现参数配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSystemSwitchACTParam ActParams;
	//UPROPERTY(EditAnywhere, BlueprintReadWrite)
	USystemSwitchBaseACT* ActObj;
	///开启表现
	void DoOpenAction();
	///关闭表现
	void DoCloseAction();
};

///@struct SystemSwitchData 系统功能开启配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSystemSwitchData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///系统索引（唯一）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName SystemIndex;
	///按钮所在的界面类型，表示这个按钮在哪个界面上（类型值在DT_UI）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString WindowID;
	///按钮打开的系统界面类型，打开的不是新窗口不要配（类型值在DT_UI）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SystemWindowID;
	///系统名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SystemName;
	///开启条件配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSystemOpenCondition> OpenCnds;
	///关闭条件配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSystemCloseCondition> CloseCnds;
	///开启表现配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSystemSwitchAction> OpenAction;
	///系统按钮标记（唯一）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName BtnTag;
	///tipsID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SystemTipsID;
	///备注说明
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Comment;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool SystemIndexResult = !this->SystemIndex.IsNone() && FNAME_TO_FSTRING(this->SystemIndex).IsNumeric();
		bool SystemNameResult = !this->SystemName.IsEmpty();
		bool BtnTagResult = !this->BtnTag.IsNone();
		bool SystemTipsIDResult = !this->SystemTipsID.IsEmpty() && this->SystemTipsID.IsNumeric();
		if (!SystemIndexResult) ResultInfo.CheckLog += FString::Printf(TEXT("SystemIndex: %s is config error!  "), *FNAME_TO_FSTRING(this->SystemIndex));
		if (!SystemNameResult) ResultInfo.CheckLog += FString::Printf(TEXT("SystemName: %s is config error!  "), *this->SystemName);
		bool OpenCndsResult = true;
		if (this->OpenCnds.Num() == 0)
		{
			OpenCndsResult = false;
			ResultInfo.CheckLog += FString::Printf(TEXT("OpenCnds is empty!  "));
		}
		else
		{
			int index = 0;
			for (auto cnd : this->OpenCnds)
			{
				if (cnd.CndParams.Script.IsEmpty() || (cnd.CndParams.Param1.IsEmpty() || !cnd.CndParams.Param1.IsNumeric()))
				{
					OpenCndsResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("OpenCnds: Index(%d) "), index);
					if (cnd.CndParams.Script.IsEmpty()) ResultInfo.CheckLog += FString::Printf(TEXT("Script is empty!  "));
					if (cnd.CndParams.Param1.IsEmpty() || !cnd.CndParams.Param1.IsNumeric()) ResultInfo.CheckLog += FString::Printf(TEXT("Param1: %s is config error!  "), *cnd.CndParams.Param1);
				}
				index++;
			}
		}

		bool OpenActionResult = true;
		if (this->OpenAction.Num() == 0)
		{
			OpenActionResult = false;
			ResultInfo.CheckLog += FString::Printf(TEXT("OpenAction is empty!  "));
		}
		else
		{
			int index = 0;
			for (auto action : this->OpenAction)
			{
				if (action.ActParams.Script.IsEmpty())
				{
					OpenActionResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("OpenAction: Index(%d) Script is empty!  "), index);
				}
				index++;
			}
		}

		bool resutl = SystemIndexResult && SystemNameResult && BtnTagResult && SystemTipsIDResult && OpenCndsResult && OpenActionResult;
		if (resutl)
		{
			ResultInfo.Result = Ok;
			return;
		}
		else
		{
			ResultInfo.Result = Error;
		}
		if (!BtnTagResult) ResultInfo.CheckLog += FString::Printf(TEXT("BtnTag: %s is config error!  "), *FNAME_TO_FSTRING(this->BtnTag));
		if (!SystemTipsIDResult) ResultInfo.CheckLog += FString::Printf(TEXT("SystemTipsID: %s is config error!  "), *this->SystemTipsID);
		if (!resutl) ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};

	FORCEINLINE bool operator==(const FSystemSwitchData& Other) const
	{
		if (this->SystemIndex == Other.SystemIndex)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
	///开启条件检测
	bool CheckOpenCondition()
	{
		if (OpenCnds.Num() <= 0)
		{
			return true;
		}
		else
		{
			for (FSystemOpenCondition& OpenCnd : OpenCnds)
			{
				if (!OpenCnd.CheckOpenCondition())
				{
					return false;
				}
			}
			return true;
		}
	}
	///关闭条件检测
	bool CheckCloseCondition()
	{
		if (CloseCnds.Num() <= 0)
		{
			return false;
		}
		else
		{
			for (FSystemCloseCondition& CloseCnd : CloseCnds)
			{
				//有一个条件符合就关闭
				if (CloseCnd.CheckCloseCondition())
				{
					return true;
				}
			}
			return false;
		}
	}
	///表现
	void DoAction();
};