#pragma once

#include "CoreMinimal.h"
//UE4
#include "Components/ActorComponent.h"
#include "Color.h"
//CS3数据
#include "GameData/CharacterData.h"
#include "Entity/Alias.h"
#include "GameData/ModelPartData.h"
#include "GameData/CharacterData.h"
#include "AppearanceComponent.generated.h"
 
/*
* 文件名称：AppearanceComponent.h
* 功能说明：外观组件
* 文件作者：shenbing
* 目前维护：ranyuan
* 创建时间：2017-05-12
*/

class ARiderCharacter;
class AStoryCharacter;
class ASpawnBase;
class GameObject;

DECLARE_DELEGATE(FChangeAnimComplete);///换姿势(动作表)完毕代理通知

DECLARE_STATS_GROUP(TEXT("UAppearanceComponent"), STATGROUP_UAppearanceComponent, STATCAT_Advanced);

/*
* 普通外观组件类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAppearanceComponent : public UActorComponent
{
	GENERATED_BODY() 
public:
	friend class ARiderCharacter;
	friend class ASpawnBase;
	friend class AStoryCharacter;

	UAppearanceComponent();
	/*----------------事件触发（回调）-----------------------*/
	virtual void CreateModelOver();
	void OnChangePartOver();

	/*----------------功能执行-------------------------------*/
	/**
	*创建角色外观，使用默认的配置装备
	*@param InModelNumber 模型ID
	*
	*@return 无
	*/
	virtual void CreateAppearance(FString InModelNumber);
	
	/**
	*创建骑乘角色外观[骑马或载具时调用]
	*@param CreateAppData 创建模型的结构体
	*
	*@return 无
	*/
	virtual void CreateRideAppearance(FCREATE_APPEARANCE_DATA CreateAppData) {}
	
	/**
	*创建角色外观 [传入的部件数据]组合[通过模型表中取到的动画蓝图及动作表等]
	*
	*@param InModelNumber 组合编号,决定动画蓝图及动作表(FString)
	*@param AModelInfo	组合模型部件数据，决定部件长外(FAModelInfo)
	*
	*@return 无
	*/
	virtual void CreateAppearanceByModelInfo(const FString& InModelNumber, const FAModelInfo& AModelInfo);

	/**
	*BlueprintCallable 复制目标Actor客户端的当前外观
	*
	*@param CopyCharacter 目标Actor(AGameCharacter*) 
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AppearanceComponent")
		void CopyCharacterFromClientAppearance(ACharacter* CopyCharacter);

	/**
	*BlueprintCallable 复制目标Actor的服务器数据外观[比如变身后，还是需要显示变身前的外观时]
	*
	*@param CopyCharacter 目标Actor(AGameCharacter*)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "AppearanceComponent")
		void CopyCharacterFromServerAppearance(ACharacter* CopyCharacter);

	/**
	*更换模型部件
	*
	*@param pos		模型部位(MODEL_PART_TYPE)
	*@param PartID	部件ID(FString)
	*
	*@return 无
	*/
	virtual void ChangePart(MODEL_PART_TYPE InPos, FString PartID) {};

	/**
	*更换动作表(换姿势)
	*
	*@param InAnimationPath	动画蓝图
	*@param InActionConfigPath	动作表
	*@param ChangeAnimComplete	更换完毕回调
	*
	*@return 无
	*/
	virtual void ChangeAnimAction(TSoftClassPtr<UAnimInstance> InAnimationPath,
		TSoftObjectPtr<UDataTable> InActionConfigPath,
		FChangeAnimComplete ChangeAnimComplete = nullptr);

	/**
	*设置此模型mesh上的所有材质颜色
	*
	*@param LinearColor 
	*
	*@return 无
	*/
	void SetMaterialColor(FLinearColor &LinearColor);

	/**
	*设置部件的相对位置、偏移、旋转
	*
	*@param PartType 部件类型
	*@param MeshComponent  部件组件
	*@param Transfrom  变形数据
	*
	*@return 无
	*/
	void SetPartCptTransform(MODEL_PART_TYPE PartType, UMeshComponent* MeshComponent, const FPART_TRANSFORM& Transfrom);

	/**
	*重置玩家标准武器
	*
	*@param IsFightShow 是否为战斗表现
	*@param InProfession 职业
	*
	*@return 无
	*/
	void ResetWeapon(bool IsFightShow, int32 InProfession);
	void ClearWeapon();//清理手上所有武器

	/**
	*更新武器的显示
	*
	*@param IsFightShow 是否为战斗表现
	*@param InProfession 职业
	*
	*@return 无
	*/
	void UpdateWeaponLocation(bool IsFightShow, int32 InProfession);

	/**
	*更新武器从右手到左手的显示
	*
	*@param IsRightToLeft 是否从右到左
	*@param InProfession 职业
	*
	*@return 无
	*/
	void UpdateWeaponRightToLeft(bool IsRightToLeft, int32 InProfession);

	/**
	*更换武器---玩家变成黑衣人后四职业对应的武器（夜袭凤栖镇）
	*
	*@param Type 武器枚举类型
	*
	*@return 无
	*/
	void UpdateWeapontYXFXZ(YXFXZ_COPY_WEAPON_ENUM Type);

	/**
	*更换武器---玩家远程吃鸡武器（勇闯绝命岛）
	*
	*@param Type 武器枚举类型
	*
	*@return 无
	*/
	void UpdateWeapontYCJMD(YCJMD_COPY_WEAPON_ENUM Type, const FString& SockeName, const FString& PartId);

	/*----------------属性（状态）获取---------------------------*/
	///<获取模型数据
	TSharedPtr<FMODEL_DATA> GetModelData();

	///<获取部件数据列表
	TMap<MODEL_PART_TYPE, FString>& GetPartMap();

	///<获取模型ID
	FString GetModelId();

	///<获取客户端本地的部件数据列表,通过模型ID
	TMap<MODEL_PART_TYPE, FString> GetPartDataMapByModelNumber(FString InModelNumber);

	///<获取服务器存储的部件数据列表,通过模型数据
	TMap<MODEL_PART_TYPE, FString> GetPartDataMapByModelInfo(const FAModelInfo& AModelInfo);

	/*----------------属性（状态）设置---------------------------*/
protected:
	/*-------------------模型相关-------------------------------------*/
	///<预先加载模型总资源路径
	void LoadModelTotalAssetPath(TFunction<void()>&& Callback);

	///<加载并应用所有部件、动作、动画蓝图等资源
	void ApplayModelByPartsMap(TMap<MODEL_PART_TYPE, FString> NewPartMap);

	///<通过entity获取部件列表并设置相应数据	
	void CreatePartMapByServer(TMap<MODEL_PART_TYPE, FString>& InPartDataMap);
	///<根据模型ID创建模型
	bool CreateModel(FString InModelNumber, TMap<MODEL_PART_TYPE, FString> &InPartMap);
	
	///<设置模型数据
	void SetModelData(TSharedPtr<FMODEL_DATA> ModelData);

	///<设置动画蓝图及动作表数据
	void SetAnimData(TSoftClassPtr<UAnimInstance> AnimationPath, TSoftObjectPtr<UDataTable> ActionConfigPath);
	///<设置动作表对应的资源列表
	void UpdateActionAnimAssetList(); 
	///<设置单个动作对应的资源
	void SetActionAnimAsset(FACTION_DATA& ActionData);

	///<获取单个部件数据,通过部件ID
	const FMODEL_PART_DATA* GetPartDataFromCfg(FString PartID);

	///<获取单个模型数据,通过模型ID
	const FMODEL_DATA* GetModelDataFromCfg(FString InModelNumber);
	/*-------------------模型相关-------------------------------------*/

	/*-------------------部件相关-------------------------------------*/
	///<添加对应部位部件
	void AddActorPart(MODEL_PART_TYPE PartType, FMODEL_PART_DATA PartData);

	///< 替换模型部件的材质实例（用于模型变色）
	void ChangeModelPartMaterial(UMeshComponent* MeshComp, const FString& ColorScheme);

	///<清除相应部位部件
	void CancelActorPart(MODEL_PART_TYPE PartType);

	///<检查这个部位是不是这个装备（主要是异步加载资源后，可能变了，所以要检查）
	bool CheckIsVaildPart(MODEL_PART_TYPE PartType, const FString& partID);

	///<设置模型中的静态Mesh部位
	void SetMeshComponent(UMeshComponent* MeshCpt, FName CptName, FName SockName, UObject* MeshObject);
	/*-------------------部件相关-------------------------------------*/
	
	///<模型未加载完毕时，服务器有许多涉及表现的状态属性已经全部同步过来了，需要在模型加载完毕的时候同步刷新状态表现
	void UpdateStateEffect();
private:
	///<填充需加载的动作数据资源
	void FillActionAssertToLoad(TArray<FStringAssetReference> &OutLoadArray, 
		TMap<ACTION_POSE_ENUM, FACTION_DATA> &OutTemActionDatas);
	///<填充需加载的模型数据资源
	void FillModelAssertToLoad(TArray<FStringAssetReference> &AllLoadArray,
		TMap<MODEL_PART_TYPE, FMODEL_PART_DATA> &OutPartDataArray, const TMap<MODEL_PART_TYPE, FString>& PartMap);
	///<外部填充添加部件数据（剧情里面专用）
	void UpdatePartMap(MODEL_PART_TYPE ModelPartType, FString PartId);

	///<绑定静态mesh组件
	void AttachStaticMeshComponent(UStaticMeshComponent* staticMeshComponent, FName sockName, UObject* mesh);
	///<绑定骨架mesh组件
	void AttachSkeletalMeshComponent(USkeletalMeshComponent* skeletalMeshComponent, FName sockName, UObject* mesh);
	
	///<创建静态mesh组件
	UStaticMeshComponent* CreateStaticMeshComponent(FName ComponentName);
	///<创建骨架mesh组件
	USkeletalMeshComponent* CreateSkeletalMeshComponent(FName ComponentName);

	///<批量设置模型所有部位对应资源
	void ApplayPartsModel(const TMap<MODEL_PART_TYPE, FMODEL_PART_DATA> &InPartDataArray);
	///<批量清除模型所有部位对应资源
	void RemoveAllParts();
	///<设置部件对应资源
	void SetActorPart(MODEL_PART_TYPE partPos, UObject* partMesh);

	///<播放出生光效
	void PlayerBornEffect();
protected:
	bool bHasCacheModelNumber = false;			///是否有缓存的模型编号,创建中又来了新的模型需要创建
	FCREATE_APPEARANCE_DATA CurCreateAppData;
	FCREATE_APPEARANCE_DATA CachaeCreateAppData;	///缓存创建外观的数据
	TSharedPtr<FMODEL_DATA> CurModelData;		///当前模型数据
	UPROPERTY()
		TMap<MODEL_PART_TYPE, FString> CurPartMap;	///当前部件Map
	FString DefaultNumber;						///模型缺失的默认模型编号
	bool isInModelCreating;						///模型是否在创建中

private:
	TMap<MODEL_PART_TYPE, TArray<UMaterialInterface*>> MaterialInterfaceMap;///原有材质Map(各部件对应的材质列表)
	UPROPERTY()
		TArray<int32> ModelEffectUID;///<模型附带光效
};

/*
* 玩家外观组件类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API URoleAppearanceComponent : public UAppearanceComponent
{
	GENERATED_BODY()
public:
	URoleAppearanceComponent();

	virtual void CreateRideAppearance(FCREATE_APPEARANCE_DATA CreateAppData) override;
	virtual void ChangePart(MODEL_PART_TYPE InPos, FString InPartID) override;

	///<获取骑乘表数据
	FRIDER_MODEL_ANIM_DATA* GetRideModelAnimDataFromCfg(RIDE_POSTURE_ENUM InPetProfession,
		ROLE_PROFESSION_ENUM InRoleProfession, ROLE_GENDER_ENUM InRoleGender);

protected:
	virtual void CreateModelOver() override;

private:
	///<创建普通模式下的人物
	bool CreateRoleModel(FString RoleModelId); 
	///<创建骑乘模式下的人物和骑宠
	bool CreateRiderAndPetForRideModel();

	///<改变载具部件资源加载完毕
	void OnChangeActorPartLoadCompleted(MODEL_PART_TYPE PartType, const FMODEL_PART_DATA* pPartData);

	///<获取模型数据
	TSharedPtr<FMODEL_DATA> GetRoleModelData(FString InRoleModelNumber);
	///<获取模型数据，通过角色创建配置表
	const FMODEL_DATA* GetModelDataByRoleCreateUiCfg();

public:

protected:

private:
};