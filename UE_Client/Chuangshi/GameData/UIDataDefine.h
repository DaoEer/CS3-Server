#pragma once
#include "CoreMinimal.h"

/**
* 文件名称：UIDataDefine.h
* 功能说明：UI界面
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2016-11-10
*/


/**
*	UI水平停靠方式
*/
UENUM(Blueprintable)
enum class EUIHDOCKSTYLE : uint8
{
	///水平靠左（像素）
	LEFT = 0,
	///水平居中（像素）
	CENTER,
	///水平靠右（像素）
	RIGHT,
	///水平靠左（缩放）
	S_LEFT,
	///水平居中（缩放）
	S_CENTER,
	///水平靠右（缩放）
	S_RIGHT,
	///水平全屏
	HFILL
};

/**
*	UI垂直停靠方式
*/
UENUM(Blueprintable)
enum class EUIVDOCKSTYLE : uint8
{
	///垂直靠左（像素）
	TOP = 0,
	///垂直居中（像素）
	MIDDLE,
	///垂直靠右（像素）
	BOTTOM,
	///垂直靠左（缩放）
	S_TOP,
	///垂直居中（缩放）
	S_MIDDLE,
	///垂直靠右（缩放）
	S_BOTTOM,
	///垂直全屏
	VFILL,
};

/**
 *	道具、技能拖拽来源枚举
 */
UENUM(Blueprintable)
enum class EDRAGSOURCE : uint8
{
	NODRAGSOURCE			= 0 UMETA(DisplayName = "NoDragSource"),				///< 未知的来源
	FROMKITBAG				= 1 UMETA(DisplayName = "FromKitBag"),					///< 来自背包物品框
	FROMNPCSHOP				= 2 UMETA(DisplayName = "FromNpcShop"),					///< 来自NPC商店商品框
	FROMQUICKBAR			= 3 UMETA(DisplayName = "FromQuickBar"),				///< 来自快捷栏
	FROMEQUIP				= 4 UMETA(DisplayName = "FromEquip"),					///< 来自角色属性装备框
	FROMSKILLTREE			= 5 UMETA(DisplayName = "FromSkillTree"),				///< 来自技能树
	FROMPLAYERTRADE			= 6 UMETA(DisplayName = "FromPlayerTrade"),				///< 来自玩家交易物品框
	FROMSTORE				= 7 UMETA(DisplayName = "FromStore"),					///< 来自仓库
	FROMPETSKILL			= 8 UMETA(DisplayName = "FromPetSKill"),				///< 来自于幻兽出战技能框
	FROMPETDRUG				= 9 UMETA(DisplayName = "FromPetDrug"),					///< 来自于幻兽出战药品框
	FROMPETINITIATIVESKILL	= 10 UMETA(DisplayName = "FromPetInitiativeSkill"),		///< 来自于幻兽主动技能
	FROMPETCONSUME			= 11 UMETA(DisplayName = "FromPetConsume"),				///< 来自于幻兽消耗物品格（比如：幻兽升级技能书）
	FROMAUTOFIGHTBAR		= 12 UMETA(DisplayName = "FromAutoFightBar"),			///< 来自自动战斗
	FROMADDDRUGTUTORIAL		= 13 UMETA(DisplayName = "FromAddDrugTutorial"),		///< 来自新手指引
	FROMSPACECOPYBAG		= 14 UMETA(DisplayName = "FromSpaceCopyBag"),			///< 来自副本背包
	FROMINTENSIFYEQUIP		= 15 UMETA(DisplayName = "FromIntensifyEquip"),			///< 来自装备强化
	FROMYCJMDQUICKBAR		= 16 UMETA(DisplayName = "FromYCJMDQuickBar"),			///< 来自勇闯绝命岛快捷栏
	FROMYCJMDQUICKBARCENTER	= 17 UMETA(DisplayName = "FromYCJMDQuickBarCenter"),	///< 来自勇闯绝命岛快捷栏第十个格子，即中间那个
	FROMWORKSHOPSTORAGE		= 18 UMETA(DisplayName = "FromWorkShopStorage"),		///< 来自轮回秘境工坊和乾坤鼎储物柜
	FROMWORKSHOPSMELT		= 19 UMETA(DisplayName = "FromWorkShopSmelt"),			///< 来自轮回秘境工坊熔炼
	FROMTONGSTORE			= 20 UMETA(DisplayName = "FromTongStore"),				///< 来自帮会仓库
	FROMSHENTONGSKILL		= 21 UMETA(DisplayName = "FromShenTongSkill"),			///< 来自神通技能
	FROMCHUANCHENGSKILL		= 22 UMETA(DisplayName = "FromChuanChengSkill"),		///< 来自传承技能
	FROMPASSIVESKILL		= 23 UMETA(DisplayName = "FromPassiveSkill"),			///< 来自被动技能
	FROMPETSHENTONGSKILL	= 24 UMETA(DisplayName = "FromPetShenTongSkill"),		///< 来自幻兽神通技能
};