// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "JsonObject.h"
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/PetEpitome.h"
#include "GameData/PetData.h"
#include "GameData/Item/ToolCost.h"
#include "Entity/Alias.h"
#include "RolePetInterface.generated.h"

/*
* 文件名称：RolePetInterface.h
* 功能说明：幻兽接口类
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-07-06
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URolePetInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URolePetInterface();
	~URolePetInterface();
	static FString GetName() { return TEXT("RolePetInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RolePetInterface.BP_RolePetInterface_C'"); } //获取蓝图对象路径

public:
#pragma region	原兽功能
	// 打开兽栏界面
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
		void CLIENT_openOriginPetUI(const int32& EntityID_);
	// 占领轮回秘境spaceType改变
	void OnOccypySpaceTypeChange(const enum LHMJ_SPACE_TYPE & _spaceType);

	// 出战幻兽入栏
	UFUNCTION(BlueprintCallable)
		void ActivePetEnterFence();
	// 出战幻兽入栏回调
	void CLIENT_OnActivePetEnterFence(const FString& petUID);

	// 原兽初始化接口
	void CLIENT_addOriginPet(const FVariant& ORIGIN_PET_DATA_1);
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
		void OnAddOriginPetBP(const int32& Index, const FString& UID);

	// 在洞府中，显示原兽模型
	void CLIENT_showOriginPetModel(const FVariant& _OriginPetDatas);
	// 添加原兽模型显示
	void CLIENT_OnAddOriginPetModel(const FVariant& _OriginPetData);
	// 移除原兽模型显示
	void CLIENT_OnRemoveOriginPetModel(const int8& Index, const uint8& DirectDel);
	// 交换原兽模型显示
	void CLIENT_OnExChangeOriginPetModel(const FVariant& _OriginPetData, const int8& Index);

	// 放生原兽 
	UFUNCTION(BlueprintCallable)
		void FreePetFromFence(const FString& UID);
	UFUNCTION(BlueprintNativeEvent, Category = "RolePetInterface")
		void CLIENT_OnFreePetFromFence(const FString& UID);

	// 获取原兽蛋物品UID
	UFUNCTION(BlueprintCallable)
		void GetOriginPetEgg(TArray<FString>& UIds);

	// 获取同类型食材（通用、素食、肉食）
	UFUNCTION(BlueprintCallable)
		void GetPetFoodByType(const FString& UID, TArray<FString>& UIds);
	// 喂养食材
	UFUNCTION(BlueprintCallable)
		void FeedPetItemFood(const FString& UID, const int32& ItemID, const int32& Num);
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
		void OnFeedPetStartBP(const FString& UID, const FString& cdTimer, const int32& step);

	//原兽入栏
	UFUNCTION(BlueprintCallable)
		void GenerateOriginPet(const int32& ItemID);
	
	/**
	*BlueprintNativeEvent,喂养原兽，降低野性
	*
	*@param UID  原兽的UID
	*@param CurWildness 原兽当前野性值
	*@param CDEndTime CD结束时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RolePetInterface")
		void CLIENT_OnFeedPetWildness(const FString& UID, const int32& CurWildness, const FString& CDEndTime);

	/**
	*BlueprintNativeEvent,喂养原兽，增加经验
	*
	*@param UID  原兽的UID
	*@param CurExp  原兽当前经验值
	*@param CDEndTime CD结束时间
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RolePetInterface")
		void CLIENT_OnFeedPetExp(const FString& UID, const int32& Step, const int32& CurExp, const FString& CDEndTime);

	/**
	*BlueprintNativeEvent,移除幻兽喂养CD
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void CLIENT_clearPetCDTime();
	// 幻兽进化
	UFUNCTION(BlueprintCallable)
		void EvolutionOriginPet(const FString& UID);
	/**
	*BlueprintNativeEvent,进化幻兽回调
	*
	*@param UID  原兽的UID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RolePetInterface")
		void CLIENT_onEvolutionPet(const FString& UID);

	// 幻兽出栏
	UFUNCTION(BlueprintCallable)
		void PetOutsideFromFence(const FString& UID);
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_OnPetOutsideFromFence(const FString& UID);
	// 兽栏 与 出战位置交换位置
	void CLIENT_OnExChangePetFromFence(const FString& EnterUID, const FString& LeaveUID);

	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		UOriginPetEpitome* GetOriginPetByUId(const FString& UID);

	// 长期未喂食（饥饿）
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		bool IsHunger(const FString& UID);

	///更换当前载具模型编号
	void Set_carrierId(const FString& newVal, const FString& oldVal);

protected:
	void _CreateOriginPet(FORIGIN_PET_DATA data);
	void _CreateOriginPetByPetUID(const FString& UID);

public:
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, UOriginPetEpitome*> OriginPetDatas;

	UPROPERTY(BlueprintReadOnly)
		TMap<int32, class AOriginPetCharacter*> OriginPetCharacters;

private:
	LHMJ_SPACE_TYPE spaceType;

#pragma endregion
public:
	/**
	*BlueprintImplementableEvent,幻兽骑乘状态改变通知
	*
	*@param State   0：没有坐骑，1：有坐骑
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
	void OnPetRiderStateChangedBP(const int32& State);
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
	void OnRep_petCageMax();/// 幻兽格子
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
	void OnPetCageMaxChangedBP(const int32& petCageMax);/// 幻兽格子改变通知蓝图

	/// 添加幻兽数据（玩家上线初始化数据调用）
	/// UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
	void PetAddData(const FVariant& var);

	/**
	*BlueprintImplementableEvent,增加幻兽通知蓝图回调
	*
	*@param index 幻兽索引
	*@param pet 幻兽数据
	*@param isGenerate 是否为孵化幻兽蛋(true：孵化幻兽蛋增加幻兽，false：玩家上线初始化数据增加幻兽)
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
	void OnAddPetBP(const int32& index , const UPetEpitome* pet, bool isGenerate);

	/// 删除幻兽数据
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
	void PetRemoveData(const FString& UID);
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
	void OnRemovePetBP(const FString& UID);


	// 设置出战幻兽经验
	UFUNCTION(BlueprintNativeEvent)
		void CLIENT_OnSetActivePetExp(const int32& CurExp);
	/**
	* Define method
	* BlueprintNativeEvent，孵化幻兽蛋服务器回调
	*
	* @param JsonStr JSON打包的幻兽数据
	*
	* @return 无
	*/
	
	/// UFUNCTION(BlueprintNativeEvent, Category = "RolePetInterface")
	void OnGeneratePet(const FVariant& var);

	/// 将幻兽JSON打包的数据解析成幻兽数据UPetEpitome
	///UFUNCTION(BlueprintPure, Category = "RolePetInterface")
	UPetEpitome* AnalyzePetJsonStr(const FVariant& Variantdata);

	/// 更新幻兽数据
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void updatePetEpitomeDatas(FString& UID, FString& attrName, FString& value);
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
	void OnUpdatePetDatasBP(const FString& UID, const FString& attrName, const FString& value);

	void updateOriginPetEpitomeDatas(FString & UID, FString & attrName, FString & value);

	/// 获取幻兽数据
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		UPetEpitome* GetPetByUID(const FString& UID);

	/// 通过幻兽UID获取图标
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		UTexture2D* GetIconByPetUID(const FString& UID);
	/// 通过幻兽Icon获取图标
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		UTexture2D* GetPetIconTexture(const FString& Icon);

	/// 召唤幻兽回调
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
	void onConjurePetResult(const FString& UID, const int32& PetEntityID);
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
	void OnConjurePetResultBP(const FString& UID, const int32& PetEntityID);

	/// 回收幻兽回调
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
	void onWithdrawPetResult();
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
	void OnWithdrawPetResultBP();

	/// 获取幻兽种族
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		PET_PROFESSION_ENUM GetPetProfessionByVehicleModelNum(const FString& VehicleModelNum);

	/// 获取幻兽种族
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		PET_PROFESSION_ENUM GetPetProfessionByScriptID(const FString& ScriptID);

	/// 获取幻兽模型ID
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		FString GetPetModelByScriptID(const FString& ScriptID);

	/// 获取幻兽模型偏移数据
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		FPET_MODEL_DATA GetPetModelTransformByModelID(const FString& ModelID);

	/// 判断是否已获得这个类型的幻兽
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		bool CheckIsOwn(FString ScriptID);

	/**
	*BlueprintPure,幻兽排序
	*
	*@return 幻兽UID列表
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
	void SortPetUId(const FString& ActivePetUId, const TArray<FString>& UIds);

	/**
	*BlueprintCallable,服务器通知客户端幻兽重命名失败
	*
	*@param UID 幻兽UID
	*@param MessageID 消息ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void OnPetReNameFail(const FString& UID,const int32 MessageID);

	/**
	*BlueprintImplementableEvent,客户端通知蓝图事件：幻兽重命名失败
	*
	*@param UID 幻兽UID
	*@param Name 幻兽名字
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
		void OnPetReNameFailBP(const FString& UID, const FString& Name);

	/**
	*BlueprintCallable,客户端请求服务器更改幻兽模式
	*
	*@param State 模式状态（1 防御;2 主动;3 被动）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestPetAIChangeStateFC(const int32 State);

	/**
	*BlueprintCallable,客户端请求服务器更改幻兽命令
	*
	*@param State 模式状态（1 跟随;2 停留 ）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestPetAIChangeCommandFC(const int32 State);

	/**
	*BlueprintCallable,客户端请求服务器更改幻兽攻击目标
	*
	*@param SkillID 幻兽第一个已学习的主动技能，没有则传0
	*@param TargetID 目标EntityID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestPetAIAttackTargetFC(const int32 SkillID, const int32 TargetID);

	/**
	*BlueprintCallable,客户端请求服务器消耗仙石合成幻兽
	*
	*@param IsCompose 是不是合成
	*
	*@param MainPetUId 主幻兽UId
	*
	*@param VicePetUId 副幻兽UId
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestOnComposePetBygold(const uint8 IsCompose, const FString MainPetUId, const FString VicePetUId);

	/**
	*BlueprintCallable,请求服务器升级幻兽主动技能
	*
	*@param UId 幻兽UId
	*
	*@param SkillId 升级的技能ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestUpgradePetSkill(const FString UId, const int32 SkillId);

	/**
	*BlueprintCallable,请求服务器升级幻兽被动技能
	*
	*@param UId 幻兽UId
	*
	*@param SkillId 升级的技能ID
	*
	*@param SkillBookId 技能书ID
	*
	*@param ItemId 附加材料物品ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestUpgradePetPassiveSkill(const FString UId, const int32 SkillId, const int32 SkillBookId = 0, const int32 ItemId = 0);

	/**
	*BlueprintCallable,请求服务器替换级幻兽主动技能
	*
	*@param UId 幻兽UId
	*
	*@param SkillId 被替换的技能 ID
	*
	*@param SkillBookId 技能书ID
	*
	*@param ItemId 启化丹物品ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestReplacePetSkill(const FString UId, const int32 SkillId, const int32 SkillBookId, const int32 ItemId = 0);

	/**
	*BlueprintCallable,请求服务器替换级幻兽被动技能
	*
	*@param UId 幻兽UId
	*
	*@param SkillId 被替换的技能 ID
	*
	*@param SkillBookId 技能书ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestReplacePetPassiveSkill(const FString UId, const int32 SkillId, const int32 SkillBookId);

	/**
	*BlueprintCallable,请求骑上宠物
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestTransformPetFC();

	/**
	*BlueprintCallable,骑上宠物是否成功的回调
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void OnIsmountSuccess(bool IsMount);

	/**
	*BlueprintPure，根据UId计算幻兽成长度区间
	*
	@param UId1 主幻兽UId
	*
	@param UId2 副幻兽UId
	*
	*@return FString 幻兽成长度区间
	*/
	UFUNCTION(BlueprintPure, Category = "RolePetInterface")
		FString GetPetRangeAbility(const FString& UId1, const FString& UId2);

	/**
	*BlueprintImplementableEvent,幻兽命令改变通知蓝图
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
		void VehiclePetStopAICommand();

	/**
	*BlueprintCallable,设置幻兽攻击的最大距离
	*@param Distance 距离
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RolePetInterface")
		void RequestSetPetDistaceFC(const float Distance);

	/**
	*BlueprintImplementableEvent,幻兽命令改变通知蓝图
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "RolePetInterface")
		void VehiclePetSetAttackState(const int32 State);

	// 幻兽神通技能，改变AI行为树
	void OnChangePetAI(FString AIIndex);
	// 幻兽神通技能结束
	void OnFinishChangePetAI();

	void onLeaveWorld() override;            ///< 当Entity离开世界（被销毁时）时，此方法被调用
	virtual void OnLeaveScenes()override;

	/**
	*BlueprintPure，更新幻兽血槽的血量值
	@param curHP 改变后的血量
	@param oldHP 改变前的血量
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RolePetInterface")
		void CLIENT_OnPetExtraHPChanged(const int32 curHP, const int32 oldHP);
	/**
	*BlueprintPure，更新幻兽蓝槽的蓝量值
	@param curMP 改变后的蓝量
	@param oldMP 改变前的蓝量
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RolePetInterface")
		void CLIENT_OnPetExtraMPChanged(const int32 curMP, const int32 oldMP);

	/**
	*BlueprintCallable,请求服务器激活/关闭血槽
	*@param IsActiveHP 是否激活 （是为True/否为False）
	*@param percent 百分比
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_onActiveHPSlot(const bool& IsActiveHP, const int32& percentHP);

	/**
	*BlueprintCallable,请求服务器激活/关闭蓝槽
	*@param IsActiveMP 是否激活 （是为True/否为False）
	*@param percent 百分比
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_onActiveMPSlot(const bool& IsActiveMP, const int32& percentMP);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_conjurePet(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_withdrawPet();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_freePet(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_addPetStep(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_activateCage();

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_sealPet(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_GetSealPetEggAttr(const FString& STRING_1);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_composePet(const FString& STRING_1, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_BASE_reName(const FString& STRING_1, const FString& UNICODE_1);

	void RPC_CELL_requestAttackTarget(int32 skillID, int32 targetID);

	void OnSetOwnerPetID(const int32 entityID) { petEntityID = entityID; };

	virtual void InitBlueCB() override;

	UFUNCTION(BlueprintNativeEvent, Category = "RolePetInterface")
		void OnGetSealPetEggAttrTo(const FClientSealPetData & Pet);

	void OnGetSealPetEggAttr(const FVariant& var);


	FClientSealPetData VarToClientSealPetData(const FVariant& Variantdata);
public:
	// 玩家召唤出的幻兽id
	UPROPERTY(BlueprintReadOnly, Category = "RolePetInterface")
		int32 petEntityID;
	UPROPERTY(BlueprintReadOnly)
		FString ActivityPetUID;
private:
	UPROPERTY()
	TMap<FString, UPetEpitome*> Pets;
	
};
