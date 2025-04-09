#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "GameData/NPCShopData.h"
#include "Entity/Alias.h"
#include "NPCExtMysteriousShopInterface.generated.h"

/*
* 文件名称：NPCExtMysteriousShopInterface.h
* 功能说明：
* 文件作者：QRN
* 目前维护：QNR
* 创建时间：2020-08-18
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UNPCExtMysteriousShopInterface : public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCExtMysteriousShopInterface();
	~UNPCExtMysteriousShopInterface();
	static FString GetName() { return TEXT("NPCExtMysteriousShopInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_NPCExtMysteriousShopInterface.BP_NPCExtMysteriousShopInterface_C'"); } //获取蓝图对象路径

	//获取神秘商人出售的商品信息
	UFUNCTION(BlueprintCallable, Category = "CS3|MysteriousShopNPC")
		void RequestShopData();

	//请求从神秘商人处购买指定商品
	UFUNCTION(BlueprintCallable, Category = "CS3|MysteriousShopNPC")
		void RequestBuyShopItem(int32 slotID, int32 amount);

	//接收到神秘商人出售的商品信息
	void recvMysteriousShopData(const FVariant& datas);
	UFUNCTION(BlueprintImplementableEvent, Category = "CS3|MysteriousShopNPC")
		void onRecvMysteriousShopData();

	//购买成功
	void onSuccessBuyShopItem(const int32& slotID, const int32& amount);
	UFUNCTION(BlueprintImplementableEvent, Category = "CS3|MysteriousShopNPC")
		void onSuccessBuyShopItemEvent();

	void InitShopDatas();

	UFUNCTION(BlueprintCallable, Category = "CS3|MysteriousShopNPC")
		TMap<int32, FMysteriousShopData> getShopDatas() { return ShopDatas; }

	virtual void InitBlueCB() override;

private:
	TMap<int32, FMYSTERIOUSSHOPDATA_MAP> ShopSVRDatas;			// 记录商品剩余数目{ slotID ： 商品数据 }
	TMap<int32, FMysteriousShopData> ShopDatas;					// 记录商品价格等配置内容{ slotID ： configData }
};
