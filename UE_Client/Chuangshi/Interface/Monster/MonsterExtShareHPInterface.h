#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtShareHPInterface.generated.h"

/*
* 文件名称：MonsterExtShareHPInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-09-13
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtShareHPInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtShareHPInterface();
	~UMonsterExtShareHPInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtShareHPInterface'"); } //获取蓝图对象路径

};