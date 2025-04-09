#pragma once

#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "InputData.h"
#include "ShortcutKey.generated.h"

/**
* 文件名称：ShortcutKey.h
* 功能说明：快捷键数据
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-06-1
*/

UENUM(Blueprintable)
enum class SHORTCUTKEY_TYPE_ENUM : uint8
{
	ROLEACTION,				//角色动作
	UISHOW,					//界面开关
	CAMERA,					//镜头设置
	SELECTTARGET,			//目标选择
	FLYOPERATION,			//轻功操作
	NORMALMAINQUICKBAR,		//普通模式主快捷栏
	ACTMAINQUICKBAR,		//ACT模式主快捷栏
	SECONDQUICKBAR,			//副快捷栏
	MAGICPET,				//幻兽快捷栏
	SPELL,					//符咒快捷栏
	OTHER,					//其他类型快捷栏
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSHORTCUTKEY : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///分类
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ShortcutKey")
		SHORTCUTKEY_TYPE_ENUM KeyType;
	///行为
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ShortcutKey")
		FName ActName;
	///键值，数组中包括主键和副键
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ShortcutKey")
		TArray<FInputKeyEvent> MainKey;
	///不可以改变为以下Key列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray <FKey> CannotChangeKeys;
	///是否允许修改
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ShortcutKey")
		bool CanChange;
	///是否可以组合
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ShortcutKey")
		bool CanGroup=true;
	///是否可以双击
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ShortcutKey")
		bool CanDoubleClick = true;
	///是否跳过检测快键键存在
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ShortcutKey")
		bool CanSkipChecking = false;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ShortcutKey")
		FString Remarks;

	bool Compara(const FSHORTCUTKEY &B)
	{
		if (KeyType == B.KeyType && ActName == B.ActName && CanChange == B.CanChange && CanGroup == B.CanGroup &&
			CanDoubleClick == B.CanDoubleClick && Remarks == B.Remarks&&CanSkipChecking == B.CanSkipChecking)
		{
			if (CannotChangeKeys.Num() != B.CannotChangeKeys.Num())
			{
				return false;
			}
			else
			{
				for (int i = 0; i < CannotChangeKeys.Num(); i++)
				{
					if (CannotChangeKeys[i] != B.CannotChangeKeys[i])
					{
						return false;
					}
				}
			}

			if (MainKey.Num() == B.MainKey.Num())
			{
				if (MainKey.Num()==0)
				{
					return true;
				}
				int count = 0;
				for (int i = 0; i < MainKey.Num(); i++)
				{
					if (MainKey[i].KeyDatas.Num() == B.MainKey[i].KeyDatas.Num() && MainKey[i].Key == B.MainKey[i].Key)
					{
						for (int j = 0; j < MainKey[i].KeyDatas.Num(); j++)
						{
							if (MainKey[i].KeyDatas[j].Type == B.MainKey[i].KeyDatas[j].Type&&
								FMath::IsNearlyEqual(MainKey[i].KeyDatas[j].Scale, B.MainKey[i].KeyDatas[j].Scale) &&
								MainKey[i].KeyDatas[j].Shift == B.MainKey[i].KeyDatas[j].Shift&&
								MainKey[i].KeyDatas[j].Ctrl == B.MainKey[i].KeyDatas[j].Ctrl&&
								MainKey[i].KeyDatas[j].Alt == B.MainKey[i].KeyDatas[j].Alt&&
								MainKey[i].KeyDatas[j].Cmd == B.MainKey[i].KeyDatas[j].Cmd&&
								MainKey[i].KeyDatas[j].IE == B.MainKey[i].KeyDatas[j].IE&&
								MainKey[i].KeyDatas[j].FuncName == B.MainKey[i].KeyDatas[j].FuncName)
							{
								count++;
								break;
							}
						}
					}
					if (count > 0 && count == MainKey.Num())
					{
						return true;
					}
				}
			}
		}
		return false;
	}
};