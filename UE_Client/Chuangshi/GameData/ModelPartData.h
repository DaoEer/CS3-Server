#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "GameData/CharacterData.h"
#include "Animation/AnimInstance.h"
#include "ModelPartData.generated.h"
/**
 * 文件名称：PartItemModelData.h
 * 功能说明：模型部件配置（能装备的部件）
 * 文件作者：ranxuanwen
 * 目前维护：ranyuan
 * 创建时间：2016-09-08
 */

 /// 黑衣人换武器枚举(夜袭凤栖镇-肖冬)
UENUM(BlueprintType)
enum class YXFXZ_COPY_WEAPON_ENUM : uint8
{
	///无武器
	YXFXZ_COPY_WEAPON_NULL = 0 UMETA(DisplayName = "YXFXZCopyWeaponNull"),
	///匕首
	YXFXZ_COPY_WEAPON_BISHOU = 1 UMETA(DisplayName = "YXFXZCopyWeaponBishou"),
	///刀
	YXFXZ_COPY_WEAPON_DAO = 2 UMETA(DisplayName = "YXFXZCopyWeaponDao"),
	///枪
	YXFXZ_COPY_WEAPON_QIANG = 3 UMETA(DisplayName = "YXFXZCopyWeaponQiang"),
	///弓
	YXFXZ_COPY_WEAPON_GONG = 4 UMETA(DisplayName = "YXFXZCopyWeaponGong"),
	///箭袋
	YXFXZ_COPY_WEAPON_JIAN = 5 UMETA(DisplayName = "YXFXZCopyWeaponJian"),
};

/// 远程吃鸡换武器枚举(叶鑫炎)
UENUM(BlueprintType)
enum class YCJMD_COPY_WEAPON_ENUM : uint8
{
	///无武器
	YCJMD_COPY_WEAPON_NULL = 0 UMETA(DisplayName = "YCJMDCopyWeaponNull"),
	///手弩
	YCJMD_COPY_WEAPON_SHOU_NU = 1 UMETA(DisplayName = "YCJMDCopyWeaponShouNu"),
	///十字弩
	YCJMD_COPY_WEAPON_SHI_ZI_NU = 2 UMETA(DisplayName = "YCJMDCopyWeaponShiZiNu"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMODEL_PART_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:

	///模型部件资源
	///支持：
	///	骨骼网络物体、静态网格物体
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "ModelPartPath")
		TSoftObjectPtr<UObject> ModelPartPath;
	///动画蓝图资源
	///注意：
	///	仅用于独立骨架部件，如，头发
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "PartAnimBpPath")
		TSoftClassPtr<UAnimInstance> PartAnimBpPath;
	///部件变形
	///注意：
	///	暂不支持：MODEL_PART_BODYS、MODEL_PART_FABAO
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "PartTransform")
		FPART_TRANSFORM PartTransform;
	///光效列表（@DT_EffectCfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "EffectIdArray")
		TArray<FString> EffectIdArray;
	///可见性检测是否依赖模型胶囊体
	///	是：使用模型胶囊体判定可见性
	///	否：使用部件自身判定可见性
	///注意：
	///	默认“是”，使用胶囊效率较高
	///	仅当模型表现不正确时，可以选择“否”（@CST-6215）
	///	已知风险：比胶囊体大的模型有时候可能会消失不见，可通过此参数优化，详见（@CST-13300）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "UseAttachParentBound")
		bool UseAttachParentBound = true;
	/// 模型变色功能（替换美术材质）
	/// 变色方案编号（见DT_ModelColorScheme）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "ColorScheme")
		FString ColorScheme;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "备注")
		FString Remarks;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (ModelPartPath.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(ModelPartPath.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ModelPartPath\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ModelPartPath\" is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMODEL_COLOR_SCHEME_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	// 需要替换的材质。key:对应mesh中的第几个材质，value为替换的目标材质
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<int32, TSoftObjectPtr<UMaterialInterface>> RepMaterialMap;

};
