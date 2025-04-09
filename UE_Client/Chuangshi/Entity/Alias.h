#pragma once

#include <vector>
#include <string>
#include "CoreMinimal.h"
#include "KBEngine.h"
#include "GameData/ChatType.h"
#include "GameData/ChatPageType.h"
#include "GameData/ChatData.h"
#include "GameData/ChatPageData.h"
#include "GameData/ChatChannelData.h"
#include "GameData/SpaceEventCondition/SEConditionBase.h"
#include "GameData/SpaceEventCondition/SEConditionFactory.h"
#include "GameData/StallItemData.h"
#include "GameData/BuyShopMallItemData.h"

/*
* 文件名称：Alias.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/


struct FDICT_INT_INT_ITEM
{
public:
	int32 key1;
	int32 value2;

	FDICT_INT_INT_ITEM();

	FDICT_INT_INT_ITEM(const FVariant& variant);

	FVariant ToVariant();
};

struct FDICT_INT_INT
{
public:
	TMap<int32, int32> dictData1;

	FDICT_INT_INT();

	FDICT_INT_INT(const FVariant& variant);

	FVariant ToVariant();
};

/**
*Account模型部位数据
*/
struct FAModelInfo
{
public:
	FString BodyModel;
	FString HeadModel;
	FString SuitsModel;
	FString HairModel;
	FString AdornModel;
	FString HeadAdornModel;
	FString FaceAdornModel;
	FString BackAdornModel;
	FString WaistAdornModel;
	FString HatModel;
	FString CoatModel;
	FString WristModel;
	FString GlovesModel;
	FString WaistModel;
	FString PantsModel;
	FString ShoesModel;
	FString NecklaceModel;
	FString LringModel;
	FString RringModel;
	FString WeaponModel;
	FString CloakModel;
	FString FaBaoModel;
	FString SkeletalWeaponModel;
	FString bodyLightEffect;
};

/**
*角色脸部骨骼数据
*/
struct FaceInfo
{

public:
	FString boneName;
	FString boneData;


	void ToFVariantMap(KBEngine::FVariantMap &out);

	static void CreateFromVariant(const FVariant& val, FaceInfo& out);

};

/**
*角色脸部骨骼数据列表
*/
struct FaceInfoList
{
public:

	TArray<FaceInfo> infolist;

	void ToFVariantMap(KBEngine::FVariantMap &out);

	static void CreateFromVariant(const FVariant& val, FaceInfoList& out);

};

/**
*角色脸部样式数据
*/
struct FaceStyle 
{
	int32 ChunzhuangIndex;
	FString ChunzhuangShape;
	int32 HuXuIndex;
	int32 LianWenIndex;
	int32 MeiMaoIndex;
	FString MeiMaoShape;
	int32 YanXianIndex;
	int32 SaiHongIndex;
	FString SaiHongShape;
	int32 YanYingIndex;
	FString YanYingShape;
	FString Brightness;
	FString ColorDepth;
	int32 EyeIndex;
	FString EyeScale;

	void ToFVariantMap(KBEngine::FVariantMap &out);

	static void CreateFromVariant(const FVariant& val, FaceStyle& out);
};

/**
*玩家身上模型编号
*/
struct Model {

public:
	FString modelName;
	FString modelNumber;

	void ToFVariantMap(KBEngine::FVariantMap &out);

	static void CreateFromVariant(const FVariant& val, Model& out);
};

/**
*玩家自定义模型编号列表
*/
struct ModelList {

public:
	TArray<Model> modelList;

	void ToFVariantMap(KBEngine::FVariantMap &out);

	static void CreateFromVariant(const FVariant& val, ModelList& out);
};

/**
*玩家信息转换类
*/
struct AliasAccountInfo
{
	/**
	*根据Variant创建玩家信息
	*
	*@param val FVariant的引用
	*@param out 输出AliasRoleInfo
	*
	*@return 
	*/
	static void CreateFromVariant(const FVariant& val, AliasAccountInfo& out);


	int32 GameTimeBalance;///<账号付费剩余时长
	FString  LastLoginTime;///<上一次登录时间
	FString  LoginTime;///<本次登录时间
};

/**
*账号信息转换类
*/
struct AliasRoleInfo
{
	/**
	*变量String转换
	*
	*@return FString，将本类的一些变量转化为FString并输出
	*/
	FString ToString();

	/**
	*将信息加入到FVariantMAP容器中
	*
	*@param out 要出入的FVariantMap
	*
	*@return 无
	*/
	void ToFVariantMap(KBEngine::FVariantMap &out);

	/**
	*根据Variant创建玩家信息
	*
	*@param val FVariant的引用
	*@param out 输出AliasRoleInfo
	*
	*@return
	*/
	static void CreateFromVariant(const FVariant& val, AliasRoleInfo& out);

	bool operator == (const AliasRoleInfo &other)
	{
		return this->DBid == other.DBid;
	}

	uint64 DBid;///<DBID
	FString PlayerName;///<玩家名字
	int16 Level;///<玩家等级
	int32 Profession;///<玩家职业
	int32 Camp;///<玩家阵营
	int32 Gender;///<玩家性别
	FString ModelNumber;///<模型编号
	FAModelInfo AModelInfo;///<模型部件数据
	FString LoginLevel;///<角色登录用的关卡
	uint64 OfflineTime;///<上次离线时间
	FaceInfoList faceModel;///玩家捏脸骨骼数据
	FaceStyle faceStyle;//玩家脸部样式数据
};


/**
*玩家信息转换Tmap类
*/
struct AliasRoleInfoTmap
{

	/**
	*变量String转换
	*
	*@return FString，将本类的一些变量转化为FString并输出
	*/
	FString ToString();

	/**
	*根据Variant创建玩家信息Tmap
	*
	*@param val FVariant的引用
	*@param out 输出AliasRoleInfoTmap
	*
	*@return 
	*/
	static void CreateFromVariant(const FVariant& val, AliasRoleInfoTmap& out);

	TArray<AliasRoleInfo> infos;///<玩家转换信息数组
};


/**
*聊天数据转换类
*/
class AliasChatData
{
public:
	/**
	*根据Variant，将数据转换为FChatData聊天数据
	*
	*@param val FVariant的引用
	*
	*@return FChatData*
	*/
	static void CreateFromVariant(const FVariant& val, FChatData& out);

	/**
	*根据FString，将数据转换为FChatData聊天数据
	*
	*@param val FString的引用
	*
	*@return FChatData*
	*/
	static void CreateFromString(const FString& val, FChatData& out);

	/**
	*根据聊天数据，创建分页数组
	*
	*@param val FVariant的引用
	*
	*@return TArray<FChatPageData>*，聊天页面数据数组
	*/
	static void CreateFromVariantToPage(const FVariant& variant, TArray<FChatPageData>& out);

	/**
	*根据聊天数据，创建分页
	*
	*@param val FVariant的引用
	*
	*@return FChatPageData*，聊天页面数据
	*/
	static void CreateFromVariantToPageData(const FVariant& variant, FChatPageData& out);

	/**
	*根据聊天数据，创建频道数组
	*
	*@param val FString的引用
	*
	*@return TArray<FChatChannelData>*，聊天频道数据
	*/
	static void CreateFromStringToChannel(const FString& val, TArray<FChatChannelData>& out);
};

/**
*conInfoStr格式转换类
*/
class AliasSpaceEventConditions
{
public:
	~AliasSpaceEventConditions();

	///conInfoStr 格式 {"ROOT": [{"param2": "1", "param4": "1", "id": 1, "param3": "1", "param1": ""}, {"param2": "2", "param4": "2", "id": 1, "param3": "2", "param1": ""}]}
	/**
	*通过TYPE，ID，将ConInfoStr按标准转换
	*
	*@param EventType 事件种类（int32）
	*@param EventID 事件ID（int32）
	*@param ConInfoStr 事件数据（Fstring引用）
	*
	*@return AliasSpaceEventConditions*
	*/
	static void CreateFromString(const FString& SpaceScriptID, const INT32 EventType, const INT32 EventID, const FString & ConInfoStr, AliasSpaceEventConditions& out);

private:
	/**
	*将CreateFromString处理过的数据，转换成可以使用的格式
	*
	*@param EventType 事件种类（int32）
	*@param EventID 事件ID（int32）
	*@param ConInfoStr 事件数据（Fstring引用）
	*
	*@return USEConditionBase*
	*/
	static USEConditionBase* CreateConFromString(const FString& SpaceScriptID, const INT32 EventType, const INT32 EventID, const FString& SrcStr);
	
public:
	UPROPERTY()
	TArray<USEConditionBase*> Infos;///<使用条件数组（指针类型）
};

/**
*NPC商店标题类
*/
class AliasNpcShopItemList
{
public:
	/**
	*创建NPC的标题
	*
	*@param val 标题数据（Fstring引用）
	*
	*@return TMap<FString, TMap<FString, float>>*
	*/
	static void CreateFromString(const FString& val, TMap<FString, TMap<FString, float>>& out);
};

/**
*Buff数据种类类
*/
class  BuffDataType
{
public:
	/**
	*根据FVariant获取Buff种类
	*
	*@param val 标题数据（FVariant引用）
	*
	*@return BuffDataType*
	*/
	static void CreateFromVariant(const FVariant& val, BuffDataType& out);

public:
	int32 index;///<下标
	int32 buffID;///<BuffID
	float holdTime;///<持续时间
	uint64 endTime;///<Buff时间
	int32 timerID;///< 定时器ID
	int32 casterID;///<CasterID
	int32 casterIsSelf;///<是否给自己
	int32 layer;///<buff层数
	FString className; //脚本名
};

/**
*测试标题
*/
class TESTITEM
{
public:
	~TESTITEM();

	/**
	*将信息加入到FVariantMAP容器中
	*
	*@param out 要出入的FVariantMap
	*
	*@return 无
	*/
	void ToFVariantMap(KBEngine::FVariantMap& out);

public:
	uint64 uid;///<uid
	int32 id;///<id
	int32 amount;///<数量
	TArray<FString> flag;///<标志
	FString misc;///<misc
};

/**
*测试标题
*/
class TESTITEMS
{
public:
	~TESTITEMS();

	/**
	*将信息加入到FVariantMAP容器中
	*
	*@param out 要出入的FVariantMap
	*
	*@return 无
	*/
	void ToFVariantMap(KBEngine::FVariantMap& out);

public:
	int32 id;///<ID
	TArray<TESTITEM> itemList;///< 标题容器
};

/**
*货摊标题
*/
class STALLITEMS
{
public:
	~STALLITEMS();

	/**
	*将信息加入到FVariantMAP容器中
	*
	*@param out 要出入的FVariantMap
	*
	*@return 无
	*/
	void ToFVariantMap(KBEngine::FVariantArray& out);

public:
	TArray<FStallItemData> stallItemList;///<货摊标题数组
};

class AliasShopMallItemList
{
public:
	static void CreateFromString(const FString& val, TMap<FString, TMap<FString, int32>>& out);
};

class BuyShopMallItems
{
public:
	TArray<FBuyShopMallItemData> buyShopMallItemList;
	~BuyShopMallItems()
	{
		buyShopMallItemList.Empty();
	}
	void ToFVariantMap(KBEngine::FVariantArray& out);
};

struct FLEVEL_RANK
{
public:
	uint64 playerDBID1;
	FString playerName2;
	uint8 camp3;
	int32 profession4;
	int32 combatPower5;
	int32 level6;
	int32 ascend7;

	FLEVEL_RANK();

	FLEVEL_RANK(const FVariant& variant);

	FVariant ToVariant();
};

struct FLEVEL_RANK_DICT
{
public:
	TArray<FLEVEL_RANK> datas1;

	FLEVEL_RANK_DICT();

	FLEVEL_RANK_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FCOMBAT_RANK_DICT
{
public:
	TArray<FLEVEL_RANK> datas1;

	FCOMBAT_RANK_DICT();

	FCOMBAT_RANK_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FMONEY_RANK
{
public:
	uint64 playerDBID1;
	FString playerName2;
	uint8 camp3;
	int32 profession4;
	int64 money5;
	int32 level6;
	int32 ascend7;

	FMONEY_RANK();

	FMONEY_RANK(const FVariant& variant);

	FVariant ToVariant();
};

struct FMONEY_RANK_DICT
{
public:
	TArray<FMONEY_RANK> datas1;

	FMONEY_RANK_DICT();

	FMONEY_RANK_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FWEAPON_COMBAT_RANK
{
public:
	uint64 playerDBID1;
	FString playerName2;
	uint8 camp3;
	uint64 weaponUID4;
	int32 weaponID5;
	int32 quality6;
	int32 combatPower7;
	FString attackProperties8;
	FString attachProperties9;
	FString intensifyProperties10;
	int32 ascend11;

	FWEAPON_COMBAT_RANK();

	FWEAPON_COMBAT_RANK(const FVariant& variant);

	FVariant ToVariant();
};

struct FWEAPON_COMBAT_DICT
{
public:
	TArray<FWEAPON_COMBAT_RANK> datas1;

	FWEAPON_COMBAT_DICT();

	FWEAPON_COMBAT_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FGUARD_SOUL_DATA
{
public:
	FString scriptID1;
	int32 level2;
	uint8 buyTime3;

	FGUARD_SOUL_DATA();

	FGUARD_SOUL_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FPAGODA_SOUL_DATA
{
public:
	TArray<FString> allPagoda1;
	TArray<FString> deadPagoda2;
	int32 wayType3;

	FPAGODA_SOUL_DATA();

	FPAGODA_SOUL_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FBIGMAP_SHOW_INFO
{
public:
	int32 objectID1;
	FVector position2;
	FString name3;

	FBIGMAP_SHOW_INFO();

	FBIGMAP_SHOW_INFO(const FVariant& variant);

	FVariant ToVariant();
};

struct FBIGMAP_SHOW_INFOS
{
public:
	TArray<FBIGMAP_SHOW_INFO> infos1;

	FBIGMAP_SHOW_INFOS();

	FBIGMAP_SHOW_INFOS(const FVariant& variant);

	FVariant ToVariant();
};

struct FEQUIP_INFO
{
public:
	uint32 itemID1;
	uint32 combatPower2;
	int32 hardiness3;
	FString attackPropertiesStr4;
	FString attachPropertiesStr5;
	FString intensifyDataStr6;

	FEQUIP_INFO();

	FEQUIP_INFO(const FVariant& variant);

	FVariant ToVariant();
};

struct FEQUIP_INFO_DICT
{
public:
	TArray<FEQUIP_INFO> Datas1;

	FEQUIP_INFO_DICT();

	FEQUIP_INFO_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FROLE_PROPERTY_INFO
{
public:
	FString name;
	int8 camp1;
	int8 gender2;
	uint8 profession3;
	uint8 level4;
	uint32 xiuwei5;
	uint8 jingjieLevel6;
	uint16 killingValue7;
	uint32 potential8;
	uint16 combatPower9;
	uint32 strength10;
	uint32 dexterity11;
	uint32 intellect12;
	uint32 corporeity13;
	uint32 discern14;
	uint16 speed15;
	uint32 HP16;
	uint32 HP_Max17;
	uint32 MP18;
	uint32 MP_Max19;
	uint32 gangQiValue20;
	uint32 gangQiValue_Max21;
	uint32 damage22;
	uint32 magic_damage23;
	uint32 armor24;
	uint32 magic_armor25;
	uint32 gangQi_damagePoint26;
	uint32 gangQi_armorPoint27;
	uint16 criticalstrike28;
	uint16 parry29;
	uint16 hitrate30;
	uint16 dodgerate31;
	uint16 healingrate32;
	uint32 cure33;
	uint32 ice_damage34;
	uint32 fire_damage35;
	uint32 thunder_damage36;
	uint32 xuan_damage37;
	uint32 ice_armor38;
	uint32 fire_armor39;
	uint32 thunder_armor40;
	uint32 xuan_armor41;
	uint32 damage_ignore42;
	uint32 magic_damage_ignore43;
	uint32 armor_ignore44;
	uint32 magic_armor_ignore45;
	uint32 criticalstrike_ignore46;
	uint32 parry_ignore47;
	uint32 hitrate_ignore48;
	uint32 dodgerate_ignore49;
	uint32 ice_damage_ignore50;
	uint32 fire_damage_ignore51;
	uint32 thunder_damage_ignore52;
	uint32 xuan_damage_ignore53;
	uint32 ice_armor_ignore54;
	uint32 fire_armor_ignore55;
	uint32 thunder_armor_ignore56;
	uint32 xuan_armor_ignore57;
	uint32 depress_resist58;
	uint32 hitback_resist59;
	uint32 control_resist60;
	uint32 insane_resist61;
	uint32 feats62;

	FROLE_PROPERTY_INFO();

	FROLE_PROPERTY_INFO(const FVariant& variant);

	FVariant ToVariant();
};

struct FEQUIP_INTENSIFY_SAVE
{
public:
	int32 index1;
	uint64 EquipUID2;
	int32 EquipID3;
	FString intensifyDataStr4;

	FEQUIP_INTENSIFY_SAVE();

	FEQUIP_INTENSIFY_SAVE(const FVariant& variant);

	FVariant ToVariant();
};

struct FEQUIP_INTENSIFY_SAVES
{
public:
	TArray<FEQUIP_INTENSIFY_SAVE> datas1;

	FEQUIP_INTENSIFY_SAVES();

	FEQUIP_INTENSIFY_SAVES(const FVariant& variant);

	FVariant ToVariant();
};

struct FNPCSHOP_ITEM
{
public:
	FString id1;
	int32 amount2;
	double startTime3;

	FNPCSHOP_ITEM();

	FNPCSHOP_ITEM(const FVariant& variant);

	FVariant ToVariant();
};

struct FNPCSHOP_ITEM_LIST
{
public:
	TArray<FNPCSHOP_ITEM> items1;

	FNPCSHOP_ITEM_LIST();

	FNPCSHOP_ITEM_LIST(const FVariant& variant);

	FVariant ToVariant();
};

struct FSHOPMALL_ITEM
{
public:
	FString id;
	int32 amount;
	int32 itemID;

	FSHOPMALL_ITEM();

	FSHOPMALL_ITEM(const FVariant& variant);

	FVariant ToVariant();
};

struct FSHOPMALL_ITEM_LIST
{
public:
	TArray<FSHOPMALL_ITEM> items;

	FSHOPMALL_ITEM_LIST();

	FSHOPMALL_ITEM_LIST(const FVariant& variant);

	FVariant ToVariant();
};

struct FDRUP_SOUL_DATA
{
public:
	int32 id1;
	int32 sellPrice2;
	int32 buyPrice3;

	FDRUP_SOUL_DATA();

	FDRUP_SOUL_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTOREGOODS
{
public:
	int32 ID1;
	int32 GoodsType2;
	int32 GoodsState3;
	int32 ItemType4;
	int32 ItemID5;
	int32 Price6;
	FString LimitTime7;
	int32 LimitAmount8;
	int32 ServeLimitAmount9;
	FString DiscountTime10;
	int32 DiscountPrice11;
	int32 RefreshType12;
	FString Description13;
	int32 ThirdLable14;
	float RebateRate15;

	FSTOREGOODS();

	FSTOREGOODS(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTOREGOODS_DICT
{
public:
	TArray<FSTOREGOODS> Datas1;

	FSTOREGOODS_DICT();

	FSTOREGOODS_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FLIMIT_GOODS
{
public:
	int32 id1;
	int32 amount2;
	double startTime3;

	FLIMIT_GOODS();

	FLIMIT_GOODS(const FVariant& variant);

	FVariant ToVariant();
};

struct FSERVERLIMIT_GOODS_LIST
{
public:
	TArray<FLIMIT_GOODS> items1;

	FSERVERLIMIT_GOODS_LIST();

	FSERVERLIMIT_GOODS_LIST(const FVariant& variant);

	FVariant ToVariant();
};

struct FPLAYERLIMIT_GOODS
{
public:
	uint64 playerDbid1;
	TArray<FLIMIT_GOODS> limitGoods2;

	FPLAYERLIMIT_GOODS();

	FPLAYERLIMIT_GOODS(const FVariant& variant);

	FVariant ToVariant();
};

struct FPLAYERLIMIT_GOODS_LIST
{
public:
	TArray<FPLAYERLIMIT_GOODS> items1;

	FPLAYERLIMIT_GOODS_LIST();

	FPLAYERLIMIT_GOODS_LIST(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTORE_BUY_RECORD
{
public:
	int32 goodsID1;
	int32 amount2;
	FString buyTime3;
	FString uid4;
	int32 price5;
	int32 goodsType6;
	int32 itemID7;

	FSTORE_BUY_RECORD();

	FSTORE_BUY_RECORD(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTORE_BUY_RECORD_DICT
{
public:
	TArray<FSTORE_BUY_RECORD> Datas1;

	FSTORE_BUY_RECORD_DICT();

	FSTORE_BUY_RECORD_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTORE_PRESENT_RECORD
{
public:
	int32 goodsID1;
	int32 amount2;
	FString buyTime3;
	FString sender4;
	FString receiver5;
	FString uid6;
	int32 price7;
	FString receiverDBID8;
	FString senderDBID9;
	int32 itemID10;

	FSTORE_PRESENT_RECORD();

	FSTORE_PRESENT_RECORD(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTORE_PRESENT_RECORD_DICT
{
public:
	TArray<FSTORE_PRESENT_RECORD> Datas1;

	FSTORE_PRESENT_RECORD_DICT();

	FSTORE_PRESENT_RECORD_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTORE_GIFT_BOX_DATA
{
public:
	int32 goodsID1;
	int32 amount2;
	FString receiverName3;
	FString receiverDBID4;
	FString senderName5;
	FString senderDBID6;
	FString endTime7;
	int32 giftState8;
	FString message9;
	FString uid10;
	FString overtime11;
	int32 price12;
	int32 itemID13;

	FSTORE_GIFT_BOX_DATA();

	FSTORE_GIFT_BOX_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTORE_GIFT_BOX_DATA_DICT
{
public:
	TArray<FSTORE_GIFT_BOX_DATA> Datas1;

	FSTORE_GIFT_BOX_DATA_DICT();

	FSTORE_GIFT_BOX_DATA_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTORE_CART_DATA
{
public:
	int32 goodsType1;
	int32 goodsID2;
	int32 amount3;

	FSTORE_CART_DATA();

	FSTORE_CART_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FSTORE_CART_DATA_DICT
{
public:
	TArray<FSTORE_CART_DATA> Datas1;

	FSTORE_CART_DATA_DICT();

	FSTORE_CART_DATA_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FPASSIVE_SKILL_BAR_DATA
{
public:
	int32 id;		//栏位ID(从1开始)
	uint8 isLock;	//是否已开启(0:已开启 1：未开启（至于是否可开启，客户端根据开启条件来进行判断就好，然后界面做显示)）
	int32 skillID;	//被动技能栏内技能ID（没有则为0）

	FPASSIVE_SKILL_BAR_DATA();
	FPASSIVE_SKILL_BAR_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FPASSIVE_SKILL_BAR_DATAS
{
public:
	TArray<FPASSIVE_SKILL_BAR_DATA> datas;

	FPASSIVE_SKILL_BAR_DATAS();
	FPASSIVE_SKILL_BAR_DATAS(const FVariant& variant);

	FVariant ToVariant();
};

struct REMIND_CROND_DATA
{
public:
	FString scriptID;			//活动ID
	uint8 remindType;		//提醒类型

	REMIND_CROND_DATA();
	REMIND_CROND_DATA(const FVariant& variant);
};

struct REMIND_CROND_DATAS
{
public:
	TArray<REMIND_CROND_DATA> datas;

	REMIND_CROND_DATAS();
	REMIND_CROND_DATAS(const FVariant& variant);
};

struct TEMP_ITEM_DATA
{
public:
	FString id;
	int32 itemID;
	int32 amount;
	int32 price;
	TEMP_ITEM_DATA();
	TEMP_ITEM_DATA(const FVariant& variant);

	static void CreateFromVariant(const FVariant& val, TEMP_ITEM_DATA& out);
};

struct BUY_ITEM_RECORD_DATA
{
public:
	FString stallName;
	FString itemName;
	int32 amount;
	int32 totalPrice;
	static void CreateFromVariant(const FVariant& val, BUY_ITEM_RECORD_DATA& out);
};

struct TEMP_SELL_RECORD_DATA
{
public:
	FString itemName;
	FString playerName;
	int32 amount;
	int32 tax;
	int32 totalPrice;
	FString time;
	static void CreateFromVariant(const FVariant& val, TEMP_SELL_RECORD_DATA& out);
};
struct SELL_ITEM_DATA
{
public:
	int32 itemID;
	FString id;
	int32 amount;
	int32 price;
	int32 combatPower;
	FString attackPropertiesStr;
	FString attachPropertiesStr;
	FString intensifyDataStr;
	int32 hardiness;
	SELL_ITEM_DATA();
	SELL_ITEM_DATA(const FVariant& variant);
};
struct BUY_AND_SELL_DATAS
{
public:
	TArray<TEMP_ITEM_DATA> stallCollectionItemList;
	TArray<SELL_ITEM_DATA> stallSellItemList;
	
	BUY_AND_SELL_DATAS();
	BUY_AND_SELL_DATAS(const FVariant& variant);
};

struct ON_REQUEST_STALL_ITEMS_DATAS
{
public:
	TArray<TEMP_ITEM_DATA> stallCollectionItemList;
	TArray<TEMP_ITEM_DATA> stallSellItemList;

	ON_REQUEST_STALL_ITEMS_DATAS();

	ON_REQUEST_STALL_ITEMS_DATAS(const FVariant& variant);
};

struct PET_PERSISTENT_DATA
{
public:
	uint64 uid;
	FString scriptID;
	FString name;
	FString uname;
	uint16 camp;
	uint16 level;
	uint16 takeLevel;
	uint16 ability;
	uint16 ability_Max;
	uint8 step;
	int32 exp;
	uint8 quality;
	TArray<int32> attrSkillBox;
	TArray<int32> passiveSkillBox;
	TArray<int32> noLearnedSkillBox;
	uint64 sleepTime;
	uint32 corporeity;
	uint32 strength;
	uint32 intellect;
	uint32 discern;
	uint32 dexterity;
	uint32 HP;
	uint32 MP;
	uint32 HP_Max;
	uint32 MP_Max;
	uint32 damage;
	uint32 magic_damage;
	uint32 armor;
	uint32 magic_armor;
	uint32 criticalstrike;
	uint32 parry;
	uint32 speed;
	uint32 hitrate;
	uint32 dodgerate;
	uint32 gangQiValue;
	uint32 gangQiValue_Max;
	uint32 gangQiState;
	uint32 gangQi_damagePoint;
	uint32 gangQi_armorPoint;
	uint32 gangQi_qiJieRevive;
	uint32 gangQi_qiYingRevive;
	uint32 combatPower;
	int32 cure;

	uint32 ice_damage;
	uint32 fire_damage;
	uint32 thunder_damage;
	uint32 xuan_damage;
	uint32 ice_armor;
	uint32 fire_armor;
	uint32 thunder_armor;
	uint32 xuan_armor;

	uint32 damage_ignore;
	uint32 magic_damage_ignore;
	uint32 armor_ignore;
	uint32 magic_armor_ignore;
	uint32 criticalstrike_ignore;
	uint32 parry_ignore;
	uint32 hitrate_ignore;
	uint32 dodgerate_ignore;

	uint32 ice_damage_ignore;
	uint32 fire_damage_ignore;
	uint32 thunder_damage_ignore;
	uint32 xuan_damage_ignore;
	uint32 ice_armor_ignore;
	uint32 fire_armor_ignore;
	uint32 thunder_armor_ignore;
	uint32 xuan_armor_ignore;

	uint32 depress_resist;
	uint32 hitback_resist;
	uint32 control_resist;
	uint32 insane_resist;
	TArray<FDICT_INT_INT_ITEM> petShenTongSKill;

	PET_PERSISTENT_DATA();
	PET_PERSISTENT_DATA(const FVariant& variant);
};

struct BUY_BACK_ITEM_DATA
{
public:
	int32 id;
	FString uid;
	int32 amount;
	int32 bindType;
	int32 combatPower;
	FString attackPropertiesStr;
	FString attachPropertiesStr;
	FString intensifyDataStr;
	int32 hardiness;
	BUY_BACK_ITEM_DATA();
	BUY_BACK_ITEM_DATA(const FVariant& variant);
};

struct BUY_BACK_ITEM_DATAS
{
public:
	TArray<BUY_BACK_ITEM_DATA> buyBackItemDataList;

	BUY_BACK_ITEM_DATAS();
	BUY_BACK_ITEM_DATAS(const FVariant& variant);
};

struct SIMPLE_ITEM_DICT
{
public:
	int32 id;
	uint64 uid;
	int32 amount;
	int32 bindType;
	FString dynamicData;
	SIMPLE_ITEM_DICT();
	SIMPLE_ITEM_DICT(const FVariant& variant);
};

struct CATALOG_DATA
{
public:
	int32 relationIndex;
	FString catalogName;
	TArray<uint64> catalogList;
	CATALOG_DATA();
	CATALOG_DATA(const FVariant& variant);
};

struct RELATION_CATALOG_DATA
{
public:
	TArray<CATALOG_DATA> RelationCatalogDatas;
	RELATION_CATALOG_DATA();
	RELATION_CATALOG_DATA(const FVariant& variant);
};

struct FSIGN_DATA
{
public:
	int32 yearMonth;
	TArray<int32> dayList;
	FSIGN_DATA();
	FSIGN_DATA(const FVariant& variant);
};

struct FSIGN_DATAS
{
public:
	TArray<FSIGN_DATA> signDatas;
	FSIGN_DATAS();
	FSIGN_DATAS(const FVariant& variant);
};

struct FPICK_UP_ITEM_DATA
{
public:
	int32 id;
	FString uid;
	int32 amount;
	int32 bindType;
	int32 quality;
	FString dynamicData;
	FPICK_UP_ITEM_DATA();
	FPICK_UP_ITEM_DATA(const FVariant& variant);
};

struct FPICK_UP_ITEM_DATAS
{
public:
	TArray<FPICK_UP_ITEM_DATA> pickUpItemList;
	FPICK_UP_ITEM_DATAS();
	FPICK_UP_ITEM_DATAS(const FVariant& variant);
};

struct MAIL_DATA
{
public:
	uint64 id;
	FString title;
	FString content;
	int64 money;
	FString senderName;
	FString receiverName;
	int32 senderType;
	uint64	receiveTime;
	int32 remainTime;
	int32 isTaken;
	int32 isRead;
	int32 isUpper;  
	int32 lingshi;
	int32 xianshi;
	int64 bindMoney;
	TArray<SIMPLE_ITEM_DICT> itemList;
	MAIL_DATA();
	MAIL_DATA(const FVariant& variant);
};

struct FCHAT_PAGESETTINGS
{
public:
	int8 pageType;
	int8 isDeletable;
	int8 isDraggable;
	FString pageName;
	TArray<int32> channelList;
	FCHAT_PAGESETTINGS();
	FCHAT_PAGESETTINGS(const FVariant& variant);
};

struct FCHAT_PAGESETTINGS_DATAS
{
public:
	TArray<FCHAT_PAGESETTINGS> datas;
	FCHAT_PAGESETTINGS_DATAS();
	FCHAT_PAGESETTINGS_DATAS(const FVariant& variant);
};
struct FCHAT_PARMS_DATA
{
public:
	FString key;
	int32 value;
	FCHAT_PARMS_DATA();
	FCHAT_PARMS_DATA(const FVariant& variant);
};

struct FCHAT_DATA
{
public:
	uint64 playerDBID;
	FString name;
	int8 type;
	int8 entityType;
	FString message;
	TArray<FString> richText;
	TArray<FCHAT_PARMS_DATA> parms;
	FCHAT_DATA();
	FCHAT_DATA(const FVariant& variant);
};

struct FCOUPON_ITEM
{
public:
	FString couponId;
	uint64 uid;
	double createTime;
	FCOUPON_ITEM();
	FCOUPON_ITEM(const FVariant& variant);
};

struct FCOUPON_ITEM_LIST
{
public:
	TArray<FCOUPON_ITEM> couponItems;
	FCOUPON_ITEM_LIST();
	FCOUPON_ITEM_LIST(const FVariant& variant);
};

struct FGIFT_GOODS_DATA
{
public:
	FString uid;
	int32 itemID;
	int32 amount;
	FString itemName;
	FString playerName;
	int32 state;
	FString time;
	FGIFT_GOODS_DATA();
	FGIFT_GOODS_DATA(const FVariant& variant);
};

struct RECALL_GIFT_DATA
{
public:
	FString uid;
	int32 state;
	FString changeTime;
	RECALL_GIFT_DATA();
	RECALL_GIFT_DATA(const FVariant& variant);
};

struct RECALL_GIFT_DATAS
{
public:
	TArray<RECALL_GIFT_DATA> dealGivingGoodsData;
	RECALL_GIFT_DATAS();
	RECALL_GIFT_DATAS(const FVariant& variant);
};

struct FCLINE_RESEARCH_SKILL
{
public:
	int32 skillID;
	int32 progress;
	FCLINE_RESEARCH_SKILL();
	FCLINE_RESEARCH_SKILL( const FVariant& variant);
};

struct FTONG_SKILL_DATA
{
public:
	FCLINE_RESEARCH_SKILL ResearchSkill;
	TArray<FCLINE_RESEARCH_SKILL> PauseSkill;
	TArray<int32> SkillList;
	TArray<int32> SkillLevelList;
	FTONG_SKILL_DATA();
	FTONG_SKILL_DATA( const FVariant& variant);
};

struct FCLINE_TONG_DATAS
{
public:
	FString TongDBID;
	FString TongLeader;
	FString TongName;
	int32 level;
	FString TongMoney;
	FString TongAffiche;
	int32 TongActivity;
	int32 TongGrow;
	int32 TotalNum;
	FString League;
	FString City;
	int32 ShenShou;
	int32 Sign;
	int32 signTime;
	int32 donateMoney;
	int32 Salary;
	FString TongRecruitAffiche;
	TArray<FString> TitleNames;
	TArray<int32> TongGrades;
	TArray<int32> TongBuild;
	int32 UpGradeActivity;
	int32 MinActivity;
	uint8 Allocation;
	uint8 BHLDAllocation;
	FTONG_SKILL_DATA TongSkill;
	FCLINE_TONG_DATAS();
	FCLINE_TONG_DATAS(const FVariant& variant);
};

struct JOIN_TONG_DATA
{
public:
	FString TongDBID;
	FString Name;
	int32 Level;
	int32 Activity;
	int32 TongNum;
	int32 TotalNum;
	FString LeaderName;
	FString Money;
	FString Recruit;
	FString League;
	FString City;
	int32 ShenShou;
	FString PersonTitle; //like 1|2|3|4|...
	JOIN_TONG_DATA();
	JOIN_TONG_DATA(const FVariant& variant);
};

struct JOIN_TONG_DATAS
{
public:
	TArray<JOIN_TONG_DATA> tongDatas;

	JOIN_TONG_DATAS();
	JOIN_TONG_DATAS(const FVariant& variant);
};

struct CLENT_TONG_MEMBER_DATA
{
public:
	FString name;
	FString DBID;
	int32 id;
	int32 level;
	int32 profession;
	int32 title;
	int32 exp;
	int32 weekContribution;
	int32 contribution;
	int32 totalContribution;
	FString localSpace;
	FString offLineTime;
	int32 isGag;
	int32 soldierAmount;
	int32 militaryRank;
	TArray<FString> tongBlocklist;
	CLENT_TONG_MEMBER_DATA();
	CLENT_TONG_MEMBER_DATA(const FVariant& variant);
};

struct TONG_EVENT_DATA
{
public:
	FString time;
	int32	type;
	TArray<FString> param;
	TONG_EVENT_DATA();
	TONG_EVENT_DATA(const FVariant& variant);
};

struct TONG_EVENT_DATAS
{
public:
	TArray<TONG_EVENT_DATA> eventDatas;
	TONG_EVENT_DATAS();
	TONG_EVENT_DATAS(const FVariant& variant);
};

struct FORDER_DATA
{
public:
	FString uid;
	int32 amount;
	int32 price;
	FString remainTime;
	int32 tradeType;
	int32 earnMoney;
	FORDER_DATA();
	FORDER_DATA(const FVariant& variant);
};

struct FORDER_DATAS                    
{
	TArray<FORDER_DATA> orderData;
	FORDER_DATAS();
	FORDER_DATAS(const FVariant& variant);
};

struct FALL_ORDER_DATAS
{
	TArray<FORDER_DATA> lingShiTradeOrder;
	TArray<FORDER_DATA> allLingShiTradeSellOrder;
	TArray<FORDER_DATA> allLingShiTradeCollectOrder;
	int32 tax;
	FALL_ORDER_DATAS();
	FALL_ORDER_DATAS(const FVariant& variant);
};

struct FALL_TRADE_DATA
{
	FString uid;
	int32 amount;
	FString remainTime;
	int32 tradeType;
	FALL_TRADE_DATA();
	FALL_TRADE_DATA(const FVariant& variant);
};

struct FLINGSHITRADE_SUCCESS_DATA
{
	FString uid;
	int32 amount;
	int32 price;
	int32 isSend;
	int32 tradeType;
	FLINGSHITRADE_SUCCESS_DATA();
	FLINGSHITRADE_SUCCESS_DATA(const FVariant& variant);
};

struct FUPDATA_ORDER_DATA
{
	FALL_TRADE_DATA allTradeData;
	FLINGSHITRADE_SUCCESS_DATA allTradeSuccess;
	FUPDATA_ORDER_DATA();
	FUPDATA_ORDER_DATA(const FVariant& variant);
};

struct TONG_QUEST_TREE_DATA
{
public:
	int32 questID;
	FString questTitle;
	int32 layer;
	TArray<int32> route;
	int32 genre;
	TONG_QUEST_TREE_DATA();
	TONG_QUEST_TREE_DATA(const FVariant& variant);
};

struct TONG_QUEST_TREE_DATAS
{
public:
	TArray<TONG_QUEST_TREE_DATA> data;
	TONG_QUEST_TREE_DATAS();
	TONG_QUEST_TREE_DATAS(const FVariant& variant);
};

struct FSOLDIER_SPECIAL_SKILL_DATA
{
public:
	int32 skillID;
	int32 exp;
	int32 maxExp;
	FSOLDIER_SPECIAL_SKILL_DATA();
	FSOLDIER_SPECIAL_SKILL_DATA(const FVariant& variant);
};

struct FBARRACKSSOLDIERDATA
{
public:
	int32 id;
	FString scriptID;
	int32 soldierType;
	int32 level;
	int32 exp;
	int32 isInArmy;
	int32 maxExp;
	TArray<FSOLDIER_SPECIAL_SKILL_DATA> skillIDDatas;
	bool isActive;
	FBARRACKSSOLDIERDATA();
	FBARRACKSSOLDIERDATA(const FVariant& variant);
	
};

struct FARMYDATA
{
public:
	int32 id;
	int32 controlArmyID;
	FString firstGuardScriptID;
	FString secondGuardScriptID;
	FString soldierScriptID;
	TArray<int32> soldierIDs;
	FARMYDATA();
	FARMYDATA(const FVariant& variant);
	/**
	*将信息加入到FVariantMAP容器中
	*
	*@param out 要出入的FVariantMap
	*
	*@return 无
	*/
	void ToFVariantMap(KBEngine::FVariantMap& out);
};

struct FORIGIN_PET_DATA
{
public:
	uint64 uid1;
	FString scriptID2;
	FString name3;
	FString uname4;
	uint16 camp5;
	int32 exp6;
	uint8 bEvolution;
	uint16 level7;
	uint16 takeLevel8;
	uint16 ability9;
	uint16 ability_Max10;
	uint8 step11;
	uint8 quality12;
	TArray<int32> attrSkillBox13;
	TArray<int32> passiveSkillBox14;
	TArray<int32> noLearnedSkillBox15;
	uint64 sleepTime16;
	uint8 wildness17;
	uint32 corporeity22;
	uint32 strength23;
	uint32 intellect24;
	uint32 discern25;
	uint32 dexterity26;
	uint32 HP27;
	uint32 MP28;
	uint32 HP_Max29;
	uint32 MP_Max30;
	uint32 damage31;
	uint32 magic_damage32;
	uint32 armor33;
	uint32 magic_armor34;
	uint32 criticalstrike35;
	uint32 parry36;
	uint32 speed37;
	uint32 hitrate38;
	uint32 dodgerate39;
	uint32 gangQiValue40;
	uint32 gangQiValue_Max41;
	uint32 gangQiState42;
	uint32 gangQi_damagePoint43;
	uint32 gangQi_armorPoint44;
	uint32 gangQi_qiJieRevive45;
	uint32 gangQi_qiYingRevive46;
	uint32 combatPower47;
	int32 cure48;

	uint32 ice_damage;
	uint32 fire_damage;
	uint32 thunder_damage;
	uint32 xuan_damage;
	uint32 ice_armor;
	uint32 fire_armor;
	uint32 thunder_armor;
	uint32 xuan_armor;

	uint32 damage_ignore;
	uint32 magic_damage_ignore;
	uint32 armor_ignore;
	uint32 magic_armor_ignore;
	uint32 criticalstrike_ignore;
	uint32 parry_ignore;
	uint32 hitrate_ignore;
	uint32 dodgerate_ignore;

	uint32 ice_damage_ignore;
	uint32 fire_damage_ignore;
	uint32 thunder_damage_ignore;
	uint32 xuan_damage_ignore;
	uint32 ice_armor_ignore;
	uint32 fire_armor_ignore;
	uint32 thunder_armor_ignore;
	uint32 xuan_armor_ignore;

	uint32 depress_resist;
	uint32 hitback_resist;
	uint32 control_resist;
	uint32 insane_resist;

	FORIGIN_PET_DATA();

	FORIGIN_PET_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FPET_FENCE_DATAS
{
public:
	TArray<FORIGIN_PET_DATA> pets1;

	FPET_FENCE_DATAS();

	FPET_FENCE_DATAS(const FVariant& variant);

	FVariant ToVariant();
};

struct FSGMZ_BOSS_DATA
{
public:
	FString name;
	FString scriptID;
	int32 time;
	int32 exp;
	float PerHP;
	int32 level;
	int32 stage;
	FSGMZ_BOSS_DATA();
	FSGMZ_BOSS_DATA(const FVariant& variant);
};

struct SGMZ_TEAM_DATA
{
public:
	uint8 teamCamp;
	TArray<FSGMZ_BOSS_DATA> bossDatas;
	int32 isKillBoss;
	int32 isWin;
	int32 extraExp;
	int32 score;
	int32 feats;
	FString BossKiller;
	SGMZ_TEAM_DATA();
	SGMZ_TEAM_DATA(const FVariant& variant);
};

struct SGMZ_TEAM_DATAS
{
public:
	TArray<SGMZ_TEAM_DATA> datas;
	SGMZ_TEAM_DATAS();
	SGMZ_TEAM_DATAS(const FVariant& variant);
};

struct FDICT_INT_INT32_LIST_ITEM
{
public:
	int32 key1;
	TArray<int32> value2;

	FDICT_INT_INT32_LIST_ITEM();

	FDICT_INT_INT32_LIST_ITEM(const FVariant& variant);

	FVariant ToVariant();
};

struct FDICT_INT_INT32_LIST
{
public:
	TMap<int32,TArray<int32>> dictData1;

	FDICT_INT_INT32_LIST();

	FDICT_INT_INT32_LIST(const FVariant& variant);

	FVariant ToVariant();
};

struct FDICT_INT_INTDICT_ITEM
{
public:
	int32 key1;
	FDICT_INT_INT value2;

	FDICT_INT_INTDICT_ITEM();

	FDICT_INT_INTDICT_ITEM(const FVariant& variant);

	FVariant ToVariant();
};

struct FDICT_INT_INTDICT
{
public:
	TMap<int32, FDICT_INT_INT> dictData1;

	FDICT_INT_INTDICT();

	FDICT_INT_INTDICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FBHZB_SIGN_MEMBER_DATA
{
public:
	int32 signID;
	int32 groupID;
	FString captainDBID;
	TArray<FString> memberDBIDs;
	uint8 isActive;
	int32 pointIndex;
	FBHZB_SIGN_MEMBER_DATA();
	FBHZB_SIGN_MEMBER_DATA(const FVariant& variant);
	/**
	*将信息加入到FVariantMAP容器中
	*
	*@param out 要出入的FVariantMap
	*
	*@return 无
	*/
	void ToFVariantMap(KBEngine::FVariantMap& out);
};


struct FDICT_STR_INT_ITEM
{
public:
	FString key;
	int32 value;

	FDICT_STR_INT_ITEM();

	FDICT_STR_INT_ITEM(const FVariant& variant);

	FVariant ToVariant();
};

struct FDICT_STR_INT
{
public:
	TMap<FString, int32> dictDataList;

	FDICT_STR_INT();

	FDICT_STR_INT(const FVariant& variant);

	FVariant ToVariant();
};

struct FTRAIN_SOLDIER_QUEST_DICT
{
public:
	FString title1;
	int32 questID2;
	FString taskTitle3;
	uint16 reward4;
	FString soldierScriptID5;

	FTRAIN_SOLDIER_QUEST_DICT();

	FTRAIN_SOLDIER_QUEST_DICT(const FVariant& variant);

	FVariant ToVariant();
};

struct FITEM_FOR_CLIENT
{
public:
	int32 id;
	FString uid;
	int32 amount;
	int32 bindType;
	int32 itemOrder;
	FString itemEndTime;
	FString dynamicData;

	FITEM_FOR_CLIENT(const FVariant& variant);
};

struct FCROND_DATA_DICT
{
public:
	uint8 status;
	FString timeTxt;
	int32 nextStartTime;

	FCROND_DATA_DICT(const FVariant& variant);
};

struct FACTIVITY_DATA_DICT
{
public:
	FString scriptID;
	TArray<FCROND_DATA_DICT> crondList;

	FACTIVITY_DATA_DICT(const FVariant& variant);
};

struct FACTIVITIES_DATA_DICT
{
public:
	FString month;
	FString day;
	FString wday;
	TArray<FACTIVITY_DATA_DICT> table;

	FACTIVITIES_DATA_DICT(const FVariant& variant);
};

struct FBHZB_TONG_INTEGRALDATA
{
public:
	uint64 tongDBID;
	FString tongName;
	int32 tongLevel;
	int32 occupyPointAmount;
	int32 integral;
	int32 camp;
	FBHZB_TONG_INTEGRALDATA(const FVariant& variant);
};

struct CLIENT_DONGFUDATA
{
public:
	int8 dongFuType;
	int16 group;
	int32 batteleID;
	int8 level;
	FString playerName;
	int8 challengeState;
	CLIENT_DONGFUDATA();
	CLIENT_DONGFUDATA(const FVariant& variant);
};

struct CLIENT_DONGFUDATA_ARR
{
public:
	TArray<CLIENT_DONGFUDATA> datas;
	CLIENT_DONGFUDATA_ARR();
	CLIENT_DONGFUDATA_ARR(const FVariant& variant);
};

struct LINGTIAN_DATA
{
public:
	FString scriptID;
	int32 seedNum;
	int8 growthStage;
	uint32 growTime;
	LINGTIAN_DATA();
	LINGTIAN_DATA(const FVariant& variant);
};

struct LINGTIAN_DATA_ARR
{
public:
	TArray<LINGTIAN_DATA> datas;
	LINGTIAN_DATA_ARR();
	LINGTIAN_DATA_ARR(const FVariant& variant);
};

struct BHZB_TONG_SIGNUP_RANK_DATA
{
public:
	uint64 tongDBID;
	FString tongName;
	int32 tongLevel;
	uint32 activity;
	int32 tongMemNum;
	int32 camp;
	BHZB_TONG_SIGNUP_RANK_DATA(const FVariant& variant);
};

struct BHZB_POINT_DATA
{
public:
	int32 index;
	uint64 occupyPlayerDBID;
	FString occupyPlayerName;
	uint64 occupyTongDBID;
	FString occupyTongName;
	uint8 pointType;
	uint8 declareWarState;
	TArray<uint64> joinAttackPlayerDBIDs;
	TArray<uint64> joinProtectPlayerDBIDs;
	FString fightEndTime;
	FString restEndTime;
	FString readyEndTime;
	int32 attackGroupTeamID;
	int32 joinProtectGroupTeamID;
	uint64 declareTongDBID;
	BHZB_POINT_DATA(const FVariant& variant);
};

struct FDICT_STRING_POS_ITEM
{
public:
	FString key1;
	FVector value2;

	FDICT_STRING_POS_ITEM();

	FDICT_STRING_POS_ITEM(const FVariant& variant);

	FVariant ToVariant();
};

struct FBATTACK_DATA
{
public:
	int8 belongSide1;
	TArray<FDICT_STRING_POS_ITEM> datas2;

	FBATTACK_DATA();

	FBATTACK_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FBATTACK_MAP
{
public:
	TArray<FBATTACK_DATA> dictDatas1;

	FBATTACK_MAP();

	FBATTACK_MAP(const FVariant& variant);

	FVariant ToVariant();
};

struct FBATTERY_INFOS
{
public:
	int32 entityID1;
	FString scriptID1;
	int8 state2;
	FVector pos3;

	FBATTERY_INFOS();

	FBATTERY_INFOS(const FVariant& variant);

	FVariant ToVariant();
};

struct FBATTERY_MAP
{
public:
	TArray<FBATTERY_INFOS> dictDatas1;

	FBATTERY_MAP();

	FBATTERY_MAP(const FVariant& variant);

	FVariant ToVariant();
};

struct BHZB_MAP_HOMEBARRACKSDATA
{
public:
	uint64 belongTongDBID;
	FVector position;
	FString name;
	int32 index;

	BHZB_MAP_HOMEBARRACKSDATA(const FVariant& variant);
};

struct BHZB_MAP_MEMBERPOSDATA
{
public:
	int32 groupID;
	FVector position;
	BHZB_MAP_MEMBERPOSDATA(const FVariant& variant);
};

struct FMYSTERIOUSSHOPDATA_MAP
{
public:
	int32 id;		//商品ID
	int32 slotID;	
	int32 amount;

	FMYSTERIOUSSHOPDATA_MAP(const FVariant& variant);
};

struct ORIGIN_PET_CLIENT_SIMPLE_DATA
{
public:
	uint64 uid;
	int8 index;
	FString scriptID;
	uint8 bEvolution;

	ORIGIN_PET_CLIENT_SIMPLE_DATA();

	ORIGIN_PET_CLIENT_SIMPLE_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct ORIGIN_PET_CLIENT_SIMPLE_DATA_LIST
{
public:
	TArray<ORIGIN_PET_CLIENT_SIMPLE_DATA> dictDatas1;

	ORIGIN_PET_CLIENT_SIMPLE_DATA_LIST();

	ORIGIN_PET_CLIENT_SIMPLE_DATA_LIST(const FVariant& variant);

	FVariant ToVariant();
};

struct FCHUANCHENG_SKILL_BAR_DATA
{
public:
	int32 id;		//栏位ID(从1开始)
	uint8 isLock;	//是否已开启(0:已开启 1：未开启（至于是否可开启，客户端根据开启条件来进行判断就好，然后界面做显示)）
	int32 skillID;	//传承技能栏内技能ID（没有则为0）

	FCHUANCHENG_SKILL_BAR_DATA();
	FCHUANCHENG_SKILL_BAR_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FCHUANCHENG_SKILL_BAR_DATAS
{
public:
	TArray<FCHUANCHENG_SKILL_BAR_DATA> datas;

	FCHUANCHENG_SKILL_BAR_DATAS();
	FCHUANCHENG_SKILL_BAR_DATAS(const FVariant& variant);

	FVariant ToVariant();
};

struct FCITY_MEMBER_DATA
{
public:
	uint64 ID = 0;
	FString Name;
	int32 BelongSide = 0;
	int32 KillEnemy = 0;
	int32 Dead = 0;
	int32 Assists = 0;
	int32 KillSoldier = 0;
	int32 TotalExploit = 0;
	int32 OwnerSoldierDeadNum = 0;

	FCITY_MEMBER_DATA(const FVariant& variant);

};

struct FATT_CITY_MEMBER_DATA
{
public:
	FString AttackName;
	FString ProtectName;
	TArray<FCITY_MEMBER_DATA> Members;

	FATT_CITY_MEMBER_DATA(const FVariant& variant);

};

struct BHZB_TONG_MSG_DATA
{
public:
	int32 statusID;
	FString statusArgs;

	BHZB_TONG_MSG_DATA(const FVariant& variant);
};

struct BHZB_TONG_OCCUPY_POINT_DATA
{
public:
	int32 pointNumber;
	int32 pointState;
	FString pointName;

	BHZB_TONG_OCCUPY_POINT_DATA(const FVariant& variant);
};

struct BHZB_TONG_TEAM_DATA
{
public:
	int32 teamNumber;
	int32 pointNumber;
	int32 pointState;
	FString pointName;

	BHZB_TONG_TEAM_DATA(const FVariant& variant);
};

struct BHZB_TONG_WAR_DETAIL
{
public:
	uint64 tongDBID;
	int32 integral;
	int32 rank;
	int32 occupyPointAmount;
	TArray<BHZB_TONG_TEAM_DATA> teamDatas;
	TArray<BHZB_TONG_OCCUPY_POINT_DATA> occupyPointDatas;
	TArray<BHZB_TONG_MSG_DATA> warMsgDatas;

	BHZB_TONG_WAR_DETAIL(const FVariant& variant);
};

struct FALLBHZB_TONG_INTEGRALDATA
{
public:
	uint64 tongDBID;
	FString tongName;
	int32 tongLevel;
	FString startTime;
	int32 integral;
	int32 totalIntegral;
	int32 camp;
	FALLBHZB_TONG_INTEGRALDATA(const FVariant& variant);
};

struct FDICT_STR_STR_ITEM
{
public:
	FString key;
	FString value;

	FDICT_STR_STR_ITEM();

	FDICT_STR_STR_ITEM(const FVariant& variant);

	FVariant ToVariant();
};

struct FDICT_STR_STR
{
public:
	TMap<FString, FString> dictDataList;

	FDICT_STR_STR();

	FDICT_STR_STR(const FVariant& variant);

	FVariant ToVariant();
};

struct FROLLDOM_DATA
{
public:
	FString uid;
	FString ownerDBID;
	uint8 isPickUp;
	FString maxRollDBID;
	int8 maxRoll;
	int8 selfRoll;

	FROLLDOM_DATA();
	FROLLDOM_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FAUCTION_DATA
{
public:
	FString uid;
	FString ownerDBID;
	uint8 isPickUp;
	FString maxAuctionDBID;
	int32 selfMoney;
	uint8 round;
	FString lastAuctionDBID;
	uint8 curAuctionRoleAmount;
	int32 maxAuctionMoney;

	FAUCTION_DATA();
	FAUCTION_DATA(const FVariant& variant);

	FVariant ToVariant();
};

struct FAUCTION_HISTORY_DATA
{
public:
	FString id;
	FString roleName;
	int8 result;
	int32 money;

	FAUCTION_HISTORY_DATA();
	FAUCTION_HISTORY_DATA(const FVariant& variant);

	FVariant ToVariant();
};

//阵营竞技奖励
struct FZYJJ_REWARD_DATA
{
public:
	uint32 exp;
	uint32 feats;
	uint32 exploit;
	uint32 contribution;

	FZYJJ_REWARD_DATA();
	FZYJJ_REWARD_DATA(const FVariant& variant);

	FVariant ToVariant();
};