#pragma once
#include "Entity/Alias.h"
#include "Interface/NPC/NPCInterface.h"
#include "NPCExtCaveHouseInterface.generated.h"

/*
* 文件名称：NPCExtCaveHouseInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2020-04-17
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UNPCExtCaveHouseInterface : public UNPCInterface
{
	GENERATED_BODY()
		typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCExtCaveHouseInterface();
	~UNPCExtCaveHouseInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.NPCExtCaveHouseInterface'"); } //获取蓝图对象路径
	virtual void InitBlueCB() override;

	// 设置建筑光效
	void Set_lightWallID(const int32& newVal, const int32& oldVal);
	/**
	*Define Method
	*BlueprintNativeEvent,通知打开建造头顶UI
	*@param	endBuildTime  结束时间
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|NPCExtCaveHouseInterface")
		void OnShowBuildUI(const FString& endBuildTime);

	// 建筑设置 种植模型
	void OnShowLingTian(const FVariant& Var);

	LINGTIAN_DATA GetLingTianDataByIndex(const int32& index);

	// 灵田
	UPROPERTY()
		TMap<int32, class APlantCharacter*> PlantCharacterMap;

protected:
	virtual void onEnterWorld() override;     ///< 当Entity进入世界时，此方法被调用
	virtual void onLeaveWorld() override;     ///< 当Entity离开世界（被销毁时）时，此方法被调用

private:
	int32 LightWallUID;				// 建筑光墙光效

	LINGTIAN_DATA_ARR LTDatas;			// 灵田数据
};
