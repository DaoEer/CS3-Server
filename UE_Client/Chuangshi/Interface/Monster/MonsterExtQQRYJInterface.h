#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtQQRYJInterface.generated.h"

/*
* 文件名称：MonsterExtQQRYJInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-11-18
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtQQRYJInterface : public UMonsterInterface
{
	GENERATED_BODY()
		typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtQQRYJInterface();
	~UMonsterExtQQRYJInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtQQRYJInterface'"); } //获取蓝图对象路径

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterExtQQRYJInterface")
		void AddAlternatelyRange();

	void OnPlayerBeginOverlap();

	void OnPlayerEndOverlap();

	virtual void InitBlueCB() override;

	UFUNCTION(BlueprintCallable, Category = "cs3|MonsterExtQQRYJInterface")
		void RPC_alternatelyResults();

private:
	float Radius = 6.0f;
	UBaseShape* pInitiativeShape = nullptr;
};