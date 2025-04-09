#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "NPCBigMapDatas.generated.h"

/**
* 文件名称：NPCBigMapDatas.h
* 功能说明：
* 文件作者：fangpengjun
* 目前维护：zhandgan
* 创建时间：2017-10-27
*/

//大地图NPC类型枚举值
UENUM(BlueprintType)
enum class  NPC_BIGMAP_TYPE_ENUM:uint8
{
	//默认
	Default					= 0 UMETA(DisplayName = "Default"),
	//队友
	Teammate				= 1 UMETA(DisplayName = "Teammate"),
	//任务
	Quest					= 2 UMETA(DisplayName = "Quest"),
	//车夫
	Driver					= 3 UMETA(DisplayName = "Driver"),
	//商人
	Business				= 4 UMETA(DisplayName = "Business"),
	//兑换
	Exchange				= 5 UMETA(DisplayName = "Exchange"),
	//仓库
	Store					= 6 UMETA(DisplayName = "Store"),
	//技能学习
	SkillLearn				= 7 UMETA(DisplayName = "SkillLearn"),
	//副本入口
	CopyEntrance			= 8 UMETA(DisplayName = "CopyEntrance"),
	//传送点
	TeleportPoint			= 9 UMETA(DisplayName = "TeleportPoint"),
	//怪物
	Monster					= 10 UMETA(DisplayName = "Monster"),
	//可交互对象
	SpellBox				= 11 UMETA(DisplayName = "SpellBox"),
	//材料
	Material				= 12 UMETA(DisplayName = "Material"),
	//武器商
	Armsmerchants			= 13 UMETA(DisplayName = "Armsmerchants"),
	//防具商
	ArmourSmith				= 14 UMETA(DisplayName = "ArmourSmith"),
	//幻兽商
	MagicBeast				= 15 UMETA(DisplayName = "MagicBeast"),
	//商人
	Businessman				= 16 UMETA(DisplayName = "Businessman"),
	//玩法
	Play					= 17 UMETA(DisplayName = "Play"),
	//药瓶商
	MedicineBottles			= 18 UMETA(DisplayName = "MedicineBottles"),
	//战场
	Battlefield				= 19 UMETA(DisplayName = "Battlefield"),
};

//大地图NPC类型枚举值
UENUM(BlueprintType)
enum class  NPC_BIGMAP_VISIBLE_FLAG :uint8
{
	//默认可见，可控制
	NPC_MAP_VISIBLE_DEFAULT			= 0	UMETA(DisplayName = "VisibleDefault"),
	//强制可见，不可控
	NPC_MAP_VISIBLE_ENFOCUS		= 1	UMETA(DisplayName = "VisibleFocus"),
	//强制不可见，不可控
	NPC_MAP_INVISIBLE_ENFOCUS	= 2	UMETA(DisplayName = "InvisibleFocus"),
	//大小地图都可见
	NPC_MAP_VISIBLE_ALL					= 3	UMETA(DisplayName = "VisibleInAll"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FNPC_BIGMAP_DATA:public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	//NPC所在关卡名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString LevelName;
	//NPC的ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString NPCScriptID;
	//NPC的阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp = 0;
	//NPC在大地图类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		NPC_BIGMAP_TYPE_ENUM BigMapType;
	//NPC在大地图显示类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		NPC_BIGMAP_VISIBLE_FLAG DisplayOnClient;
	//NPC标记是否动态贴图显示
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool isDynamicDisplay;
	//NPC标记是否与服务器同步
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool SyncWithServer;
};