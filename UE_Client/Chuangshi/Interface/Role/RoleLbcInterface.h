// Fill out your copyright notice in the Description page of Project Settings.

#pragma once


#include "CS3Base/CS3EntityInterface.h"
#include "GameData/LbcData.h"
#include "RoleLbcInterface.generated.h"


/*
* 文件名称：RoleLbcInterface.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2020-08-20
*/

/**
 * 玩家练兵场接口类
 */

UCLASS(BlueprintType)
class CHUANGSHI_API URoleLbcInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleLbcInterface();

	static FString GetName() { return TEXT("RoleLbcInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleLbcInterface.BP_RoleLbcInterface_C'"); } //获取蓝图对象路径
	virtual void InitBlueCB() override;

	///初始化数据
	void InitData();

	///请求打开练兵场地图界面
	UFUNCTION(BlueprintCallable, Category = "RoleLbcInterface")
		void ReqOpenLbcMapUI();
	///打开练兵场地图界面
	void OpenLbcMapUI(const FVariant& occupyInfo, const FVariant& declareInfo, const FVariantArray& statusList);

	///请求前往练兵场
	UFUNCTION(BlueprintCallable, Category = "RoleLbcInterface")
	void ReqGotoLbc(uint8 line, int32 index);
	
	///获取某个分线的数据
	UFUNCTION(BlueprintCallable, Category = "RoleLbcInterface")
	TMap<int32, FRoleLbcData> GetLineDatas(uint8 line);

	///消耗指定等级指定数量的士兵
	void LbcOccupyCost(const int32& level, const int32& amount, const int32& money, const FVariantArray& scriptIDList);

	///提交选择交付的士兵
	UFUNCTION(BlueprintCallable, Category = "RoleLbcInterface")
		void ReqSubmitOccupyCost(FString soldierScriptID);
	
	///撤销宣战
	UFUNCTION(BlueprintCallable, Category = "RoleLbcInterface")
		void ReqCancelDeclareLbc();

	//更新占领信息
	void UpdateOccupyInfo(const FVariant& occupyInfo);
	//更新宣战信息
	void UpdateDeclareInfo(const FVariant& declareInfo);
	//更新被宣战信息
	void UpdateBeDeclaredInfo(const FVariant& declareInfo);
	//单个练兵场的状态信息 
	void UpdateLbcStatusInfo(const FVariant& statusInfo);
	//通知宣战者进战场
	void NotifyDeclarerFight(const int32& countDown, const uint8& line, const int32& index, const FVariant& declareInfo);
	//通知占领者进战场
	void NotifyOccupierFight(const int32& countDown, const uint8& line, const int32& index, const FVariant& declareInfo);
	//宣战者放弃争夺
	UFUNCTION(BlueprintCallable, Category = "RoleLbcInterface")
	void DeclarerGiveUpFight(uint8 line, int32 index);
	//占领者放弃争夺
	UFUNCTION(BlueprintCallable, Category = "RoleLbcInterface")
	void OccupierGiveUpFight(uint8 line, int32 index);

public:
	///最大分线数量
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		uint8 MaxLineNum;

	TMap<uint8, TMap<int32, FRoleLbcData>> roleLbcData; //练兵场数据 <line，<index,data>> 

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FLBC_OCCUPY_INFO OccupyInfo; //我占领的练兵场

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FLBC_DECLARE_INFO DeclareInfo; //我宣战的练兵场
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FLBC_DECLARE_INFO BeDeclaredInfo; //我被别人宣战的练兵场
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		TArray<FString> ScriptIDs;	//满足条件的兵种
};