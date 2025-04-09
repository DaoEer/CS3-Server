#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtRHBInterface.generated.h"

/*
* 文件名称：MonsterExtRHBInterface.h
* 功能说明：
* 文件作者：lintongbin
* 目前维护：lintongbin
* 创建时间：2020-01-13
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtRHBInterface : public UMonsterInterface
{
	GENERATED_BODY()
		typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtRHBInterface();
	~UMonsterExtRHBInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtRHBInterface'"); } //获取蓝图对象路径

	virtual void InitBlueCB() override;

	UFUNCTION(BlueprintNativeEvent, Category = "cs3|MonsterExtRHBInterface")
		void startThorwtorch(const FString& effectID, const int32& radius);
};