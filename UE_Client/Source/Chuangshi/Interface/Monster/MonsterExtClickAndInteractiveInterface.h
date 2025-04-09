#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtClickAndInteractiveInterface.generated.h"

/*
* 文件名称：MonsterExtClickAndInteractiveInterface.h
* 功能说明：
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2020-05-26
*/

class UBaseShape;

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtClickAndInteractiveInterface : public UMonsterInterface
{
	GENERATED_BODY()
		typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	virtual void onLeaveWorld() override;
	void CLIENT_AddInteractiveRange(const float& Radius);
	void OnPlayerBeginOverlap();
	void OnPlayerEndOverlap();

	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtClickAndInteractiveInterface'"); } //获取对象路径

	UFUNCTION(BlueprintCallable)
		void RPC_CELL_RequestInteraction();

private:
	//UPROPERTY()
	UBaseShape* pInitiativeShape = nullptr;//在UShapeManager里面管理了
};