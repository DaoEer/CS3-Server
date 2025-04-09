// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Interface/SpellBox/SpellBoxInterface.h"
#include "GameData/LingTianPlantData.h"
#include "SpellBoxLingTianInterface.generated.h"

/*
* 文件名称：SpellBoxLingTianInterface.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2020-04-23
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USpellBoxLingTianInterface : public USpellBoxInterface
{
	GENERATED_BODY()
		typedef USpellBoxInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

public:
	USpellBoxLingTianInterface();
	~USpellBoxLingTianInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.SpellBoxLingTianInterface'"); } //获取蓝图对象路径

	void Set_clientSeedNum(const int32& newVal, const int32& oldVal);
	void Set_clientGrowthStage(const int32& newVal, const int32& oldVal);

public:
	///打开种植界面UI
	void ShowLingTianPlantUI(const int32& entityID);

	///打开成长信息界面UI
	void ShowGrowUpMsgUI(const int32& entityID, const FString& endTimeStr);

	///点击种植按钮通知
	UFUNCTION(BlueprintCallable, Category = "SpellBoxLingTianInterface")
	void RPC_onClickPlant(int32 ItemID);

	///获取种子数据
	UFUNCTION(BlueprintCallable)
		void GetLingTianSeedData(FString &seedIcon, FString &seedName);
	
	///获取种子列表
	UFUNCTION(BlueprintCallable, Category = "SpellBoxLingTianInterface")
		TArray<int32> GetSeedIDList();

	// 获取当前种子的生长阶段数据(因为成熟期 ，跟最后一阶段用的模型一样)
	UFUNCTION(BlueprintCallable)
		FGROWTHSTAGEMODELNUMBER GetCurSeedGrowData();

	// 模型创建完成回调
	UFUNCTION(BlueprintCallable)
		void OnCreateModelFinish();
private:
	///初始化种子数据
	void InitLingTianSeedData();

	void BeginCreateMesh();
	void CheckMeshComponent(const TArray<FVector>& PosList);
	void CreateApperaance(const FString& ModelID);

public:
	/// 种子类型
	UPROPERTY(BlueprintReadOnly)
		int32 seedNum;

	///生长阶段
	UPROPERTY(BlueprintReadOnly)
		int32 growthStage;

	//生长时间
	UPROPERTY(BlueprintReadOnly)
		FString endStrTime;

	///种子数据
	TMap<int32, FLING_TIAN_PLANT_DATA*> seedData;

	UPROPERTY(BlueprintReadOnly)
		UStaticMesh* TempMesh;

	bool ModelIsCreate;
private:
	TArray<UStaticMeshComponent*> CropMeshComponents;
	//TArray<UStaticMesh*> MeshArr;
	FTimerHandle DelayCreateHandle;				// 延迟生成，因为需要种子数据 和 阶段数据 决定生成的模型
	int32 CurCreateMeshIndex;

	
};
