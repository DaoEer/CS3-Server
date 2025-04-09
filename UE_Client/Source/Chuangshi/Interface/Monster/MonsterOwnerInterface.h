// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
//#include "Delegate.h"
#include "MonsterOwnerInterface.generated.h"

/*
* 文件名称：MonsterOwnerInterface.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-1-30
*/


DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSetBootyOwnerAssist, int32, SelfEntityID);

/*
* 怪物所有权数据结构体
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBootOwnerData
{
	GENERATED_BODY()
public:
	int32 type;
	int32 ownerID;
};


UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterOwnerInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterOwnerInterface();
	~UMonsterOwnerInterface();
	static FString GetName() { return TEXT("MonsterOwnerInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterOwnerInterface'"); } //获取蓝图对象路径

public:

	//当前玩家是否为拥有者
	UFUNCTION(BlueprintCallable, Category = "MonsterOwnerInterface")
		bool PlayerIsOwner();

	/**
	* Define method
	* BlueprintCallable，所有权通知
	*
	* @param data ，所有者信息
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "MonsterOwnerInterface")
		void CLIENT_OnSetBootyOwner(const FString& data);

	//判断此ID所对应的是否是所有者
	UFUNCTION(BlueprintCallable, Category = "MonsterOwnerInterface")
		bool CheckOwner(int32 type, int32 id);

	UPROPERTY(BlueprintAssignable, Category = "MonsterOwnerInterface")
		FOnSetBootyOwnerAssist OnSetBootyOwnerAssist;

	//判断此ID所对应的是否有所有者
	UFUNCTION(BlueprintCallable, Category = "MonsterOwnerInterface")
		bool hasOwner();


	virtual void InitBlueCB() override;

private:
	TArray<FBootOwnerData> bootOwnerList;	///<怪物所有权信息列表
	TArray<int32> bootOwnerIDList;
};
