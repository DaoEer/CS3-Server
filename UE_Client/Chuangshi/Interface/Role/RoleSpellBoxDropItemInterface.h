// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Item/ItemBase.h"
#include "RoleSpellBoxDropItemInterface.generated.h"

/*
* 文件名称：RoleSpellBoxDropItemInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-10-24
*/

/**
 * 玩家SpellBox拾取物品接口
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleSpellBoxDropItemInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleSpellBoxDropItemInterface();
	~URoleSpellBoxDropItemInterface();

	static FString GetName() { return TEXT("RoleSpellBoxDropItemInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleSpellBoxDropItemInterface.BP_RoleSpellBoxDropItemInterface_C'"); } //获取蓝图对象路径


	/**
	* Define method
	* 跟SpellBox宝箱交互服务器回调给客户端拾取物品信息列表
	*
	* @return 无
	*/
	void SendSpellBoxPickItems(const int32& spellBoxEntityID, const FVariant& Var);

	TArray<UItemBase*> AnalyzeSpellBoxPickItems(const FVariant& Var);

	///<点击宝箱Actor打开宝箱回调通知蓝图显示拾取界面
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleSpellBoxDropItemInterface")
	void OnShowSpellBoxPickItems(const int32& spellBoxEntityID);

	/**
	* BlueprintCallable，通知SpellBoxPickItem 交互完毕
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleSpellBoxDropItemInterface")
	void NotifySpellBoxInteractiveOver(const int32& spellBoxEntityID);

	/**
	* BlueprintCallable，拾取场景物件的物品
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleSpellBoxDropItemInterface")
	void PickUpSpellBoxItem(const int32& spellBoxEntityID, const TArray<FString>& ItemUidList);

	/**
	* BlueprintCallable，关闭界面后 清除宝箱数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleSpellBoxDropItemInterface")
		void ClearPickUpSpellBoxItemData();

	/**
	* Define method
	* BlueprintNativeEvent，拾取完物品的回调
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpellBoxDropItemInterface")
	void OnPickUpSpellBoxItem(const int32& spellBoxEntityID,const FString& ItemUid);


	/**
	* Define method
	* 服务器通知客户端拾取物品给成员
	*
	* @return 无
	*/
	void OnPickUpSpellBoxToMember(const int32& SpellBoxEntityID, const FString& UId, const FVariant& Members);

	UFUNCTION(BlueprintNativeEvent, Category = "RoleSpellBoxDropItemInterface")
		void OnPickUpSpellBoxToMember_BP(int32 SpellBoxEntityID,const FString& UId, const TMap<int32, FString>& MemberInfos); //
	/**
	* 客户端通知服务器拾取物品给成员
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleSpellBoxDropItemInterface")
		void PickUpSpellBoxToMember(int32 SpellBoxEntityID, const FString ItemUId, const int32 DstEntityID);

	void OnSpellBoxPickItemDestroyed(const int32& spellBoxEntityID);

	///< 宝箱销毁回调（通知蓝图关闭拾取界面）
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleSpellBoxDropItemInterface")
	void BP_OnSpellBoxPickItemDestroyed(const int32& spellBoxEntityID);

	virtual void onLeaveWorld() override;
	virtual void InitBlueCB() override;
public:
	///<宝箱的物品列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RoleSpellBoxDropItemInterface")
	TArray<UItemBase*> SpellBox_ItemList;
};