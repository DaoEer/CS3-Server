#include "CS3Base/CS3EntityInterface.h"
#include "RoleMilitaryRankInterface.generated.h"
/*
* 文件名称：RoleMilitaryRankInterface.h
* 功能说明：
* 文件作者：lintongbin
* 目前维护：lintongbin
* 创建时间：2020-02-29
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleMilitaryRankInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleMilitaryRankInterface();
	~URoleMilitaryRankInterface();
	
	static FString GetName() { return TEXT("RoleMilitaryRankInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleMilitaryRankInterface.BP_RoleMilitaryRankInterface_C'"); } //获取蓝图对象路径

	virtual void InitBlueCB() override;
	/**
	*玩家军功值
	*
	*@return int32, 军功值
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleMilitaryRankInterface")
		int32 GetExploit();
	/**
	*玩家军衔等级
	*
	*@return int32, 军衔值
	*/
	UFUNCTION(BlueprintCallable, Category = "cs3|RoleMilitaryRankInterface")
		int32 GetMilitaryRank();

	void onUpdataExploit(const int32& exploit, const int32& militaryRank);

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|RoleMilitaryRankInterface")
		void onBPUpdataExploit(const int32& exploit, const int32& militaryRank);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_updataExploit();
};