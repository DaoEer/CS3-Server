
#include "NPCExtMysteriousShopInterface.h"
#include "Actor/NPC/NPCCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Manager/CfgManager.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(UNPCExtMysteriousShopInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvMysteriousShopData, &UNPCExtMysteriousShopInterface::recvMysteriousShopData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onSuccessBuyShopItem, &UNPCExtMysteriousShopInterface::onSuccessBuyShopItem, const int32&, const int32&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UNPCExtMysteriousShopInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()


UNPCExtMysteriousShopInterface::UNPCExtMysteriousShopInterface()
{
}


UNPCExtMysteriousShopInterface::~UNPCExtMysteriousShopInterface()
{
}

void UNPCExtMysteriousShopInterface::RequestShopData()
{
	if (this->GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("--UNPCExtMysteriousShopInterface::RequestShopData no this Entity!%d"), EntityID);
		return;
	}
	KBEngine::FVariantArray Args;
	this->GetEntity()->CellCall(TEXT("requestShopData"), Args);
}

void UNPCExtMysteriousShopInterface::RequestBuyShopItem(int32 slotID, int32 amount)
{
	if (this->GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("--UNPCExtMysteriousShopInterface::RequestBuyShopItem no this Entity!%d"), EntityID);
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(slotID);
	Args.Add(amount);
	this->GetEntity()->CellCall(TEXT("requestBuyShopItem"), Args);
}

void UNPCExtMysteriousShopInterface::recvMysteriousShopData(const FVariant& datas)
{
	KBEngine::FVariantArray array_data = datas.GetValue<KBEngine::FVariantArray>();
	for (FVariant& data : array_data)
	{
		FMYSTERIOUSSHOPDATA_MAP element = FMYSTERIOUSSHOPDATA_MAP(data);
		if (ShopSVRDatas.Contains(element.slotID))
			ShopSVRDatas.Remove(element.slotID);
		ShopSVRDatas.Add(element.slotID, element);
	}
	InitShopDatas();
	onRecvMysteriousShopData();
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("MysteryShop"));
	}
}

void UNPCExtMysteriousShopInterface::onSuccessBuyShopItem(const int32& slotID, const int32& amount)
{
	if (ShopSVRDatas.Contains(slotID))
	{
		ShopSVRDatas[slotID].amount -= amount;

		if (ShopSVRDatas[slotID].amount < 0)
			ShopSVRDatas[slotID].amount = 0;
	}
	if (ShopDatas.Contains(slotID))
	{
		ShopDatas[slotID].BuyLimit -= amount;

		if (ShopDatas[slotID].BuyLimit < 0)
			ShopDatas[slotID].BuyLimit = 0;
	}

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnSuccessBuyItemEvent.Broadcast();
	}
}

void UNPCExtMysteriousShopInterface::InitShopDatas()
{
	ShopDatas.Empty();
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	if (CfgManager == nullptr) return;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MYSTERIOUS_SHOP_DATA);
	if (ConfigTable)
	{
		for (TPair<int32, FMYSTERIOUSSHOPDATA_MAP>& data : ShopSVRDatas)
		{
			TArray<FMysteriousShopData*> CombatShops;
			ConfigTable->GetAllRows(CombatShops);
			for (auto CS : CombatShops)
			{
				if (data.Value.id == CS->id)
				{
					//获取配置其他信息一致，只需要修改一下数量
					FMysteriousShopData d(*CS);	
					d.BuyLimit = data.Value.amount;
					ShopDatas.Add(data.Value.slotID, d);
				}
			}
		}
	}
}

void UNPCExtMysteriousShopInterface::InitBlueCB()
{
	Supper::InitBlueCB();
}


CONTROL_COMPILE_OPTIMIZE_END
