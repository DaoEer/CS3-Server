#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "EnumCsvDefine.h"
#include "LevelHashMap.generated.h"

/**
* 文件名称：LevelHashMap.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2016-12-02
*/

///加载方式的枚举，策划在同地图传送时需要判断是否出现Loading界面，目前集合石必须要出现
///注意，添加枚举时请在下表IsNeedLoad属性上备注清楚类型
UENUM(BlueprintType)
enum class LOADING_MODE_ENUM : uint8
{
	LOADING_MODE_NULL = 0 UMETA(DisplayName = "LOADING_MODE_NULL"),//默认方式
	LOADING_MODE_JIHESHI = 1 UMETA(DisplayName = "LOADING_MODE_JIHESHI"),//集合石
	LOADING_MODE_FORCE =2 UMETA(DisplayName = "LOADING_MODE_FORCE"),//强制
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FLEVEL_HASHMAP : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:

	//资源关卡名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName LevelName;

	//资源子关卡名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName SubStreamLevelName = TEXT("");
	/*是否需要加载进度条，TMap不支持在表格显示，故此用TArray实现
	* 数组第0个值为默认值
	* 数组第1个值集合石
	* 后续有待扩展
	*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<bool> IsNeedLoad;
	//逻辑关卡名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FName LogicLevelName;
	//关卡描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Description;
};

enum class EGAMELEVELTYPE : uint8
{
	GAME_LEVEL_TYPE_NONE = 0 UMETA(DisplayName = "GAME_LEVEL_TYPE_NONE"),
	GAME_LEVEL_TYPE_LOGIN = 1 UMETA(DisplayName = "GAME_LEVEL_TYPE_LOGIN"),
	GAME_LEVEL_TYPE__ROLE_SELECE = 2 UMETA(DisplayName = "GAME_LEVEL_TYPE__ROLE_SELECE"),
	GAME_LEVEL_TYPE__ROLE_CREATE = 3 UMETA(DisplayName = "GAME_LEVEL_TYPE__ROLE_CREATE"),
	GAME_LEVEL_TYPE__CAMP_SELECT = 4 UMETA(DisplayName = "GAME_LEVEL_TYPE__CAMP_SELECT"),
	GAME_LEVEL_TYPE__WORLD_NORMAL = 5 UMETA(DisplayName = "GAME_LEVEL_TYPE__WORLD_NORMAL"),
	GAME_LEVEL_TYPE__WORLD_PLANE = 6 UMETA(DisplayName = "GAME_LEVEL_TYPE__WORLD_PLANE"),
	GAME_LEVEL_TYPE__WORLD_STREAM = 7 UMETA(DisplayName = "GAME_LEVEL_TYPE__WORLD_STREAM"),
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FRESULT_MAP_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:

	//头卡原点坐标(单位:厘米)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector2D LevelWorldOrign = FVector2D(0.0f,0.0f);

	//地图实际缩放比例
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Rate = 0.0f;

	//地图实际图片的纹理尺寸（单位：像素）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector2D MapUISize = FVector2D(0.0f, 0.0f);;

	//是否小地图表读取
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool HasMiniMapCfg = false;
};