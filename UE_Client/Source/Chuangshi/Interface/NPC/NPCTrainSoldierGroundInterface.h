#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "NPCTrainSoldierGroundInterface.generated.h"

/*
* 文件名称：NPCTrainSoldierGroundInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-04-16
*/
/**
*练兵场NPC接口类
*/

UENUM(BlueprintType)
enum class  NPCTRAINSOLDIERGROUND_STATE: uint8
{
	///不可被宣战
	NPCTRAINSOLDIERGROUND_STATE_CAN_NOT_BE_DECLARE = 0 UMETA(DisplayName = "NPCTRAINSOLDIERGROUND_STATE_CAN_NOT_BE_DECLARE"),
	///可被宣战
	NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE = 1 UMETA(DisplayName = "NPCTRAINSOLDIERGROUND_STATE_CAN_BE_DECLARE"),
	///争夺中
	NPCTRAINSOLDIERGROUND_STATE_FIGHT = 2 UMETA(DisplayName = "NPCTRAINSOLDIERGROUND_STATE_FIGHT"),
};

UENUM(BlueprintType)
enum class  NPCTRAINSOLDIERGROUND_TYPE : uint8
{
	/// 练兵场
	NPCTRAINSOLDIERGROUND_TYPE_NONE = 0 UMETA(DisplayName = "NPCTRAINSOLDIERGROUND_TYPE_NONE"),
	/// 初级练兵场
	NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL = 1 UMETA(DisplayName = "NPCTRAINSOLDIERGROUND_TYPE_LOW_LEVEL"),
	/// 中级练兵场
	NPCTRAINSOLDIERGROUND_TYPE_MIDDLE_LEVEL = 2 UMETA(DisplayName = "NPCTRAINSOLDIERGROUND_TYPE_MIDDLE_LEVEL"),
	/// 高级练兵场
	NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL = 3 UMETA(DisplayName = "NPCTRAINSOLDIERGROUND_TYPE_HIGH_LEVEL"),
};

UCLASS(BlueprintType)
class CHUANGSHI_API UNPCTrainSoldierGroundInterface : public UNPCInterface
{
	GENERATED_BODY()
		typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCTrainSoldierGroundInterface();
	~UNPCTrainSoldierGroundInterface();
	static FString GetName() { return TEXT("NPCTrainSoldierGroundInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.NPCTrainSoldierGroundInterface'"); } //获取蓝图对象路径

	void Set_lineNumber(const int32& newVal, const int32& oldVal);
	void Set_index(const int32& newVal, const int32& oldVal);
	void Set_occupyPlayerName(const FString& newVal, const FString& oldVal);;
	void Set_declareWarState(const uint8& newVal, const uint8& oldVal);
	void Set_fightEndTime(const FString& newVal, const FString& oldVal);
	void Set_trainGroundType(const uint8& newVal, const uint8& oldVal);
	void Set_occupyPlayerDBID(const uint64& newVal, const uint64& oldVal);

	void CLIENT_CreateTrainSoldierGroundArea(const FString& InScriptID, uint8 IsOwnSide);

	UFUNCTION(BlueprintCallable, Category = "NPCTrainSoldierGroundInterface")
		int32 GetTrainSoldierGroundLineNumber();

	UFUNCTION(BlueprintCallable, Category = "NPCTrainSoldierGroundInterface")
		int32 GetTrainSoldierGroundIndex();

	UFUNCTION(BlueprintCallable, Category = "NPCTrainSoldierGroundInterface")
		FString GetTrainSoldierGroundOccupyPlayerName();

	UFUNCTION(BlueprintCallable, Category = "NPCTrainSoldierGroundInterface")
		NPCTRAINSOLDIERGROUND_STATE GetTrainSoldierGroundState();

	UFUNCTION(BlueprintCallable, Category = "NPCTrainSoldierGroundInterface")
		FString GetTrainSoldierGroundFightEndTime();

	UFUNCTION(BlueprintCallable, Category = "NPCTrainSoldierGroundInterface")
		NPCTRAINSOLDIERGROUND_TYPE GetTrainGroundType();

private:
	int32 lineNumber; ///< 练兵场所在分线
	int32 index; ///< 练兵场编号
	NPCTRAINSOLDIERGROUND_TYPE TrainGroundType;
	FString occupyPlayerName; ///< 占领玩家名称
	NPCTRAINSOLDIERGROUND_STATE declareWarState; ///< 练兵场状态
	FString fightEndTime; ///< 战斗结束时间
};