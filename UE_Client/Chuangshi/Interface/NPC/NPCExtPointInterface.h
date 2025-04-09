#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "GameData/BHZBData.h"
#include "NPCExtPointInterface.generated.h"

/*
* 文件名称：NPCExtPointInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-05-20
*/
/**
*帮会争霸据点
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UNPCExtPointInterface : public UNPCInterface
{
	GENERATED_BODY()
		typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCExtPointInterface();
	~UNPCExtPointInterface();
	static FString GetName() { return TEXT("NPCExtPointInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.NPCExtPointInterface'"); } //获取蓝图对象路径

	void Set_index(const int32& newVal, const int32& oldVal);
	void Set_occupyPlayerName(const FString& newVal, const FString& oldVal);
	void Set_occupyTongName(const FString& newVal, const FString& oldVal);
	void Set_declareWarState(const uint8& newVal, const uint8& oldVal);
	void Set_fightEndTime(const FString& newVal, const FString& oldVal);
	void Set_restEndTime(const FString& newVal, const FString& oldVal);
	void Set_pointType(const uint8& newVal, const uint8& oldVal);

	UFUNCTION(BlueprintCallable, Category = "NPCExtPointInterface")
		int32 GetNPCEXTPointIndex();

	UFUNCTION(BlueprintCallable, Category = "NPCExtPointInterface")
		FString GetNPCEXTPointOccupyPlayerName();

	UFUNCTION(BlueprintCallable, Category = "NPCExtPointInterface")
		FString GetNPCEXTPointOccupyTongName();

	UFUNCTION(BlueprintCallable, Category = "NPCExtPointInterface")
		NPCEXTPOINT_STATE GetNPCEXTPointState();

	UFUNCTION(BlueprintCallable, Category = "NPCExtPointInterface")
		FString GetNPCEXTPointFightEndTime();

	UFUNCTION(BlueprintCallable, Category = "NPCExtPointInterface")
		FString GetNPCEXTPointRestEndTime();

	UFUNCTION(BlueprintCallable, Category = "NPCExtPointInterface")
		NPCEXTPOINT_TYPE GetNPCEXTPointType();

private:
	int32 index; ///< 据点编号
	FString occupyPlayerName; ///< 占领玩家名称
	FString occupyTongName; ///< 占领帮会名称
	NPCEXTPOINT_STATE declareWarState; ///< 据点状态
	FString fightEndTime; ///< 战斗结束时间
	FString restEndTime; ///< 休整结束时间
	NPCEXTPOINT_TYPE pointType; ///< 据点类型
};