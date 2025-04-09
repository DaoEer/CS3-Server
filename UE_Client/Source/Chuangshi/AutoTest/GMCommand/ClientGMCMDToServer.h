#pragma once


#include "ClientGMCMDToServer.generated.h"

/*
* 文件名称：ClientGMCMDToServer.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2017-12-09
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UClientGMCMDToServer: public UObject
{
	GENERATED_BODY()
	typedef void (UClientGMCMDToServer::*pMethod) (int32 playerID, int32 desEntityID, FString methodName, FString args);
public:
	UClientGMCMDToServer();
	~UClientGMCMDToServer();
	static UClientGMCMDToServer* GetInstance();
	void BuildMap();
	UFUNCTION(BlueprintCallable, Category = "UClientGMCMDToServer | CallFunc")
	void CallFunc(int32 playerID, int32 desEntityID, const FString methodName, const FString cmdArgs);

	//传送NPCPointDatasTable中点的位置(CST-3101)
	void gotoPoint(int32 playerID, int32 desEntityID, FString methodName,  FString args);

	//设置table选取全部战斗关系的entity
	void tabAllEntity(int32 playerID, int32 desEntityID, FString methodName, FString args);

	//对目标施放客户端技能
	void spellCSkill(int32 playerID, int32 desEntityID, FString methodName, FString args);

	//目标对自己施放客户端技能
	void spellCSkillSelf(int32 playerID, int32 desEntityID, FString methodName, FString args);

	//添加客户端buff
	void addCBuff(int32 playerID, int32 desEntityID, FString methodName, FString args);

	//目标对自己添加客户端buff
	void addCBuffSelf(int32 playerID, int32 desEntityID, FString methodName, FString args);

public:
	
	//通过字符串调用方法

	TMap<FString, pMethod> MethodNameMap;
	//客户端方法名转为服务器方法名
	//TMap<FString, FString> ClientMethodToServerMap;

};


