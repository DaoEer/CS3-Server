#pragma once
#include "GameFramework/Actor.h"
#include "Actor/GameCharacter.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "GameData/VoiceData.h"
#include "Actor/Player/PlayerCharacter.h"
#include "HeadManager.generated.h"

/*
* 文件名称：HeadManager.h
* 功能说明：头像（半身像）管理类
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-07-25
*/

UCLASS(BlueprintType)
class CHUANGSHI_API AHeadManager : public AActor
{
	GENERATED_BODY()
		AHeadManager();
	~AHeadManager();

public:
	static AHeadManager* GetInstance();

	virtual void BeginPlay() override;
	
#pragma region	/** 半身像配置工具专用，不要调用 */
public:
	///半身像工具方法，开始配置
	UFUNCTION(BlueprintCallable, CallInEditor, Category = "HeadManager")
		void StartHalfHeadSetting();
	///半身像工具方法，结束配置
	UFUNCTION(BlueprintCallable, CallInEditor, Category = "HeadManager")
		void StopHalfHeadSetting();
	///半身像工具方法，更新位置配置表DT_HeadModelTransformCfg数据
	UFUNCTION(BlueprintCallable, CallInEditor, Category = "HeadManager")
		void UpdateHalfHeadTableData(const FString& HeadID, const FTransform& Transform, const float& FOVAngle);
	///半身像工具方法，更新配置表DT_HeadModelCfg数据
	UFUNCTION(BlueprintCallable, CallInEditor, Category = "HeadManager")
		void UpdateHalfHeadModelTableData(const FString& HeadID, const FString& ModelID
			, const TArray<FHEAD_MODEL_ACTION_DATA>& ModelActionData
			, const TArray<FHEAD_BUST_MODEL_ACTION_DATA>& HeadModelActionData
			, const TArray<FHEAD_MODEL_EFFECT_DATA>& ModelEffectData);
	///半身像工具方法，保存配置表资源
	UFUNCTION(BlueprintCallable, CallInEditor, Category = "HeadManager")
		bool SaveHalfHeadTableData();

	/**
	* 半身像工具方法，设置当前模型ID，用于输入动作ID时搜索模型对应的动作ID
	* ModelID为3D半身像配置表的ModelID
	*/
	UFUNCTION(BlueprintCallable, CallInEditor, Category = "HeadManager")
		void SetCurrModelID(FString ModelID);

private:
	///半身像工具方法，销毁actor
	void DestroyHalfHeadCharacter();

#pragma endregion

public:
	///获取动态半身像配置数据
	UFUNCTION(BlueprintCallable, CallInEditor, Category = "HeadManager")
		FHEAD_MODEL_DATA GetHalfHeadModleDataByHeadID(const FString& HeadID, bool& IsSuccess);
	///获取动态半身像位置配置数据，IsSuccess为False时返回的位置数据为默认数据
	UFUNCTION(BlueprintCallable, CallInEditor, Category = "HeadManager")
		FHEAD_MODEL_TRANSFORM_DATA GetHalfHeadModelTransDataByModelID(const FString& ModelID, bool& IsSuccess);

private:
	void InitHalfHeadTableData();

public:
	UPROPERTY()
		const UDataTable* HalfHeadConfigTable = nullptr;///<半身像配置表

	UPROPERTY()
		const UDataTable* HalfHeadTranConfigTable = nullptr;///<半身像配置表

#pragma region	/** 半身像配置工具专用，不要调用 */
	///半身像工具变量，半身像ProxyActor列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "HeadManager")
		TArray<AGameCharacter*> HalfHeadCharacters;
	///半身像工具变量，半身像材质列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "HeadManager")
		TArray<UMaterialInstanceDynamic*>  HalfHeadMaterialIns;
	///半身像工具变量，是否正在进行配置半身像数据
	bool IsHeadSetting;
	///半身像工具变量，是否修改了半身像配置数据
	bool IsChangeSetting;
	///半身像工具变量，是否修改了半身像位置配置数据
	bool IsChangeTransSetting;
	///半身像工具变量，当前的模型ID，用于输入动作ID时搜索模型对应的动作ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "HeadManager")
		FString CurrModelID;
	///半身像工具变量，当前的玩家模型ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "HeadManager")
		FString CurrPlayerModelID;
#pragma endregion
};