#pragma once

#include "Actor/NPCBaseCharacter.h"
#include "MultiAreaSpellBoxCharacter.generated.h"

/*
* 文件名称：MultiAreaSpellBoxCharacter.h
* 功能说明：多区域触发Character
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-10-22
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSHAPE_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	//区域编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 Index;

	//区域名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString Name;

	//区域形状
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 Shape;

	//区域尺寸
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FVector Bounds;

	//区域偏移
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FTransform Transform;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMULTI_AREA_SPELLBOX_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Uname;

	//模型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ModelNumer;

	//模型倍率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float ModelScale;

	//区域数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSHAPE_DATA> ShapeData;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool UnamejResult = !Uname.IsEmpty();
		bool ModelNumerResult = !ModelNumer.IsEmpty();
		if (!UnamejResult) ResultInfo.CheckLog += FString::Printf(TEXT("Uname cannot be empty!  "));
		if (!ModelNumerResult) ResultInfo.CheckLog += FString::Printf(TEXT("ModelNumer cannot be empty!  "));
		bool ShapeDataResult = true;
		if (ShapeData.Num() == 0)
		{
			ShapeDataResult = false;
			ResultInfo.CheckLog += FString::Printf(TEXT("ShapeData cannot be empty!  "));
		}
		else
		{
			int index = 0;
			for (auto data : ShapeData)
			{
				if (data.Name.IsEmpty())
				{
					ShapeDataResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("ShapeData: index(%d): Name cannot be empty!  "), index);
				}
				index++;
			}
		}
		if (UnamejResult && ModelNumerResult && ShapeDataResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};


/*
* 场景物件多区域触发Character类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AMultiAreaSpellBoxCharacter :public ANPCBaseCharacter
{
	GENERATED_BODY()
public:
	AMultiAreaSpellBoxCharacter();///<构造函数

	UFUNCTION(BlueprintImplementableEvent, Category = "SpellBox")
		void OnSwitchArea(int32 Index);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestRefreshAreaStatus();

protected:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent
	virtual FString GetEntityUName() override;///<重写GetEntityUName
};	