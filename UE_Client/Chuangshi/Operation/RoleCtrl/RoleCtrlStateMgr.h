#pragma once
#include "RoleCtrlState.h"
#include "GameData/ShortcutKey.h"
#include "RoleCtrlStateMgr.generated.h"
/*
* 文件名称：RoleCtrlStateMgr.h
* 功能说明：
* 文件作者：wuxiaoou
* 目前维护：huting
* 创建时间：2018-04-28
*/
class URoleCtrlBase;

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API URoleCtrlStateMgr : public UActorComponent
{
	GENERATED_BODY()
		URoleCtrlStateMgr();
		~URoleCtrlStateMgr();

	//friend class ACS3PlayerController;

public:
	/** 进入某个状态 */
	virtual void OnEnterState(EROLE_CTRL_STATE State,int32 Index=0);
	/** 离开某个状态 */
	virtual void OnLeaveState(EROLE_CTRL_STATE State);

	/** 重置到普通状态 */
	void ResetToCommomState();

	/** 获取控制状态链表 */
	UFUNCTION(BlueprintPure, Category = "RoleCtrlStateMgr|Get")
		const TArray<URoleCtrlBase*>& GetCtrlStateList() const {
		return CtrlStateList;
	}

	/** 是否有当前状态 */
	UFUNCTION(BlueprintPure, Category = "RoleCtrlStateMgr|Get")
		bool IsHaveState(EROLE_CTRL_STATE State);

	void UpdateStortcutKeyData(bool bGetPlayerData = false);

	TArray<FSHORTCUTKEY> GetAllShortcutKeyData();
	///<保存类型为Type的新快捷键数据到本地客户端
	void SaveShortcutKeyDataByTypeToFile(SHORTCUTKEY_TYPE_ENUM Type, TArray<FSHORTCUTKEY> NewKeys, TArray<FSHORTCUTKEY>& OldKeys);
	
	///<保存NewKeys到本地客户端
	void SaveShortcutKeyDataToFile(TArray<FSHORTCUTKEY> NewKeys);

	//取消快捷键设置数据
	void CancelShortcutKeyData(SHORTCUTKEY_TYPE_ENUM Type);

	///<获取Type默认快捷键数据
	TArray<FSHORTCUTKEY> GetDefaultShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type);

	FSHORTCUTKEY GetDefaultShortcutKeyDataByActName(FName ActName);

	///<获取Type快捷键数据
	TArray<FSHORTCUTKEY> GetShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type);
	
	//获取修改后未保存的快捷键
	TArray<FSHORTCUTKEY> GetChangedShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type);

	///<快捷键是否存在在所有快捷键数据中 bIsChangedKeys=ture时只检测临时修改后的数据
	ESHORTCUT_EXISTING_TYPE CheckShortcutKeyExisting(FGROUPKEY_DATA Keys, FName ActName, FSHORTCUTKEY& OldShortcutKey);

	///<快捷键是否存在在所有快捷键数据中 bIsChangedKeys=ture时只检测临时修改后的数据
	ESHORTCUT_EXISTING_TYPE CheckShortcutKeyExistingInChanged(FGROUPKEY_DATA Keys, FName ActName, FSHORTCUTKEY& OldShortcutKey);

	///<改变快捷键数据时如果找到本地已保存快捷键，弹出消息框,确定：修改临时快捷键数据对应ActName的快键键为Keys的数据为NONE 该函数判断临时快捷键数据对应Keys是否为NONE了
	bool CheckChangedShortcutDataReseted(FSHORTCUTKEY OldShortcutKey, TArray<FKey>Keys);
	
	///<根据ActName获取ShortcutData
	void GetShortcutDataByActName(SHORTCUTKEY_TYPE_ENUM KeyType,FName ActName, FSHORTCUTKEY& ShortcutData,bool bIsChangedKeys=false);

	void AddShortcutDataToChangedKeys(FSHORTCUTKEY ShortcutData);

	void RemoveShortcutDataFromChangedKeys(FSHORTCUTKEY ShortcutData);

	bool ChangedShortcutKeysIsEmpty();
	void InitShortcutKeyDataBySaveData();
	
	bool CheckKeyCanChangeGroupKey(FSHORTCUTKEY ShortcutKey, FGROUPKEY_DATA Keys);///<检查Key键是否能改为

	FString GetKeyNameByActName(FName ActName, FGROUPKEY_DATA& KeyValue);///<根据ActName 获取对应的按键信息

	///<获取所有包含复合键（Shift、Ctrl、Alt、Cmd）有关的键； Key为复合键
	TArray<FSHORTCUTKEY> GetShortcutDataByGroupKey(FKey Key);
protected:
	/** 保存快捷键数据 */
	void SaveShortcutKeyDatas() {}

	// Begin UActorComp Interface
	virtual void BeginPlay() override;
	virtual void BeginDestroy() override;
	// ~End UActorComp Interface

	///<快捷键是否存在在param2中 
	bool CheckShortcutKeyExistingInTarray(FGROUPKEY_DATA GroupKey, TArray<FInputKeyEvent>InputKeyEventDatas);

	const UDataTable*  GetShortcutKeyDataConfig();
private:
	/** 当前状态(可为多个) */
	UPROPERTY(VisibleAnywhere)
		TArray<URoleCtrlBase*> CtrlStateList;

	/** 快捷键本地数据, 可以直接保存和修改 */
	UPROPERTY(VisibleAnywhere)
		TArray<FSHORTCUTKEY> ChangedKeys;

	/** 快捷键保存链表 */
	UPROPERTY(VisibleAnywhere)
		TArray<FSHORTCUTKEY> AllKeys;

	/** 修改后没有保存的快捷键 */
	UPROPERTY(VisibleAnywhere)
		TArray<FSHORTCUTKEY> TempChangedKeys;

};
