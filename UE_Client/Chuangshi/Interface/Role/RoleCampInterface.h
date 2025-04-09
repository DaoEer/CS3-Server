#pragma once

#include "Util/CS3Debug.h"
#include "CS3Base/CS3EntityInterface.h"
#include "RoleCampInterface.generated.h"

/*
* 文件名称：RoleCampInterface.h
* 功能说明：玩家阵营
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-12-25
*/
/**
 * 玩家阵营接口类
 */

UCLASS(BlueprintType)
class  CHUANGSHI_API URoleCampInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleCampInterface();
	~URoleCampInterface();
	static FString GetName() { return TEXT("RoleCampInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleCampInterface.BP_RoleCampInterface_C'"); } //获取蓝图对象路径


	/**
	*Define Method
	*BlueprintNativeEvent,阵营气运改变回调
	*
	*@param: newCampMorale  新气运
	*@param: oldCampMorale  旧气运
	*@param: otherCampMorale  其他阵营气运
	*@param: buffID  
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void CLIENT_onMoraleChange(const FString& newCampMorale, const FString& oldCampMorale, const FString& otherCampMorale, const int32& buffID);

	/**
	*Define Method
	*BlueprintNativeEvent,查询阵营数据回调
	*
	*@param: taoismMorale  仙道气运
	*@param: demonMorale  魔道气运
	*@param: taoismVenName  仙道尊者名字
	*@param: demonVenName  魔道尊者名字
	*@param: isGetCampReward  是否领取奖励（false：未领取， true：已领取）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void CLIENT_OnQueryCampUIData(const FString& taoismMorale, const FString& demonMorale, const FString& taoismVenName, const FString& demonVenName, uint8 isGetCampReward);

	/**
	*Define Method
	*BlueprintNativeEvent,查询阵营数据回调
	*@param: OpenSwitch  开关
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleQuestInterface")
		void CLIENT_SetClientCampSwitch(uint8 OpenSwitch);

	virtual void InitBlueCB() override;

	/**
	*是否打开阵营开关
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleQuestInterface")
		bool IsOpenCampSwitch();

	/**
	*申请获得阵营气UI数据
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RquestQueryCampUIData();

	/**
	*申请获得阵营气运奖励
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_rquestCampMoraleReward();

private:
	bool IsOpenSwitch = false;
};
