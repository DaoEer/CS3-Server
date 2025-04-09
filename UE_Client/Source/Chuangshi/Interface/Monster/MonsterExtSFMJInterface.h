#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtSFMJInterface.generated.h"

/*
* 文件名称：MonsterExtSFMJInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-08-06
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtSFMJInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtSFMJInterface();
	~UMonsterExtSFMJInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtSFMJInterface'"); } //获取蓝图对象路径

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterExtSFMJInterface")
		void AddInitiativeRange();

	void OnPlayerBeginOverlap();

	void OnPlayerEndOverlap();

	virtual void InitBlueCB() override;

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterExtSFMJInterface")
		void RPC_InteractionResults();

private:
	float Radius = 5.0f;
	UBaseShape* pInitiativeShape = nullptr;
};