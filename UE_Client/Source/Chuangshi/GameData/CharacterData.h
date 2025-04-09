// Fill out your copyright notice in the Description page of Project Settings.
#pragma once
#include "CoreMinimal.h"
//UE4
#include "Engine/DataTable.h"
#include "Engine/StaticMesh.h"
#include "Animation/AnimationAsset.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/AnimInstance.h"
//CS3数据
#include "GameDeFine.h"
#include "CsvTableRowBase.h"
#include "GameFramework/Character.h"
#include "CharacterData.generated.h"

/**
* 文件名称：CharacterData.h
* 功能说明：人物数据对象相关
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2016-09-02
*/

class UAnimSequenceBase;
class UAnimMontage;
class UBlendSpaceBase;

///职业枚举
UENUM(BlueprintType)
enum class ROLE_PROFESSION_ENUM : uint8
{
	///战士
	ROLE_PROFESSION_TYPE_ZHAN_SHI = 1 UMETA(DisplayName = "RoleProfessionZhanShi"),
	///剑客
	ROLE_PROFESSION_TYPE_JIAN_KE = 2 UMETA(DisplayName = "RoleProfessionJianKe"),
	///射手
	ROLE_PROFESSION_TYPE_SHE_SHOU = 3 UMETA(DisplayName = "RoleProfessionSheShou"),
	///法师
	ROLE_PROFESSION_TYPE_FA_SHI = 4 UMETA(DisplayName = "RoleProfessionFaShi"),
	///枚举计数（此项无效，请勿选择）
	ROLE_PROFESSION_TYPE_NULL = 5 UMETA(DisplayName = "RoleProfessionNull"),
};

///性别枚举
UENUM(BlueprintType)
enum class ROLE_GENDER_ENUM :uint8
{
	///男性
	ROLE_GENDER_TYPE_MALE = 1 UMETA(DisplayName = "RoleGenderMale"),
	///女性
	ROLE_GENDER_TYPE_FEMALE = 2 UMETA(DisplayName = "RoleGenderFemale"),
};

/**
*装备位置类型
*功能：对应装备插槽的枚举，仅用于AGameCharacter中的换装及ModelTable表的配置
*注意：由于其它部件是绑定在Mesh下的，在应用部件时，需对部件排序，以达到先应用身体部件，否则，将会导致崩溃
*	所以，将MODEL_PART_BODYS的枚举值定义为最小，以便排序时排在第一位置
*/
UENUM(BlueprintType)
enum class MODEL_PART_TYPE : uint8
{
	///默认静态组件
	MODEL_PART_STATIC = 0	UMETA(DisplayName = "MODEL_PART_STATIC"),
	///骨骼模型（Mesh）
	MODEL_PART_BODYS = 10	UMETA(DisplayName = "MODEL_PART_BODYS"),
	///头部
	MODEL_PART_HEADS = 11	UMETA(DisplayName = "MODEL_PART_HEADS"),
	///套装
	MODEL_PART_SUITS = 12	UMETA(DisplayName = "MODEL_PART_SUITS"),
	///头发
	MODEL_PART_HAIRS = 13	UMETA(DisplayName = "MODEL_PART_HAIRS"),
	///发饰
	MODEL_PART_ADORN = 14	UMETA(DisplayName = "MODEL_PART_ADORN"),
	///头饰
	MODEL_PART_HEAD_ADORN = 15	UMETA(DisplayName = "MODEL_PART_HEAD_ADORN"),
	///面饰
	MODEL_PART_FACE_ADORN = 16	UMETA(DisplayName = "MODEL_PART_FACE_ADORN"),
	///背饰
	MODEL_PART_BACK_ADORN = 17	UMETA(DisplayName = "MODEL_PART_BACK_ADORN"),
	///腰饰
	MODEL_PART_WAIST_ADORN = 18	UMETA(DisplayName = "MODEL_PART_WAIST_ADORN"),
	///披肩
	MODEL_PART_CAPE = 19	UMETA(DisplayName = "MODEL_PART_CAPE"),
	///帽子
	MODEL_PART_HAT = 20		UMETA(DisplayName = "MODEL_PART_HAT"),
	///上衣
	MODEL_PART_COATS = 21	UMETA(DisplayName = "MODEL_PART_COATS"),
	///护腕
	MODEL_PART_WRIST = 22	UMETA(DisplayName = "MODEL_PART_WRIST"),
	///手套
	MODEL_PART_GLOVES = 23	UMETA(DisplayName = "MODEL_PART_GLOVES"),
	///腰带
	MODEL_PART_WAIST = 24	UMETA(DisplayName = "MODEL_PART_WAIST"),
	///裤子
	MODEL_PART_PANTS = 25	UMETA(DisplayName = "MODEL_PART_PANTS"),
	///鞋子
	MODEL_PART_SHOES = 26	UMETA(DisplayName = "MODEL_PART_SHOES"),
	///项链
	MODEL_PART_NECKLACE = 27	UMETA(DisplayName = "MODEL_PART_NECKLACE"),
	///左手戒指
	MODEL_PART_LHAND_RING = 28	UMETA(DisplayName = "MODEL_PART_LHAND_RING"),
	///右手戒指
	MODEL_PART_RHAND_RING = 29	UMETA(DisplayName = "MODEL_PART_RHAND_RING"),
	///双手静态武器
	MODEL_PART_BWEAPON = 31		UMETA(DisplayName = "MODEL_PART_BWEAPON"),
	///左手静态武器
	MODEL_PART_LWEAPON = 32		UMETA(DisplayName = "MODEL_PART_LWEAPON"),
	///右手静态武器
	MODEL_PART_RWEAPON = 33		UMETA(DisplayName = "MODEL_PART_RWEAPON"),
	///披风
	MODEL_PART_CLOAK = 34	UMETA(DisplayName = "MODEL_PART_CLOAK"),
	///法宝
	MODEL_PART_FABAO = 35	UMETA(DisplayName = "MODEL_PART_FABAO"),
	///左手骨架武器
	MODEL_PART_S_LWEAPON = 36		UMETA(DisplayName = "MODEL_PART_S_LWEAPON"),
	///右手骨架武器
	MODEL_PART_S_RWEAPON = 37		UMETA(DisplayName = "MODEL_PART_S_RWEAPON"),
	///环身
	MODEL_PART_BODYS_LIGHT = 38		UMETA(DisplayName = "MODEL_PART_BODYS_LIGHT"),
	///枚举计数（此项无效，请勿选择）
	MODEL_PART_NUM	= 39	UMETA(DisplayName = "MODEL_PART_NUM"),
};

///骑乘姿态枚举
UENUM(BlueprintType)
enum class RIDE_POSTURE_ENUM : uint8
{
	///无姿态
	RIDE_POSTURE_NULL			= 0 UMETA(DisplayName = "RidePostureNull"),
	///骑马姿态
	RIDE_POSTURE_RIDE			= 1 UMETA(DisplayName = "RidePostureRide"),
	///御剑姿态
	RIDE_POSTURE_FLOAT			= 2 UMETA(DisplayName = "RidePostureFloat"),
	///骑老鹰姿态
	RIDE_POSTURE_RIDE_EAGLE		= 3 UMETA(DisplayName = "RidePostureRideEagle"),
	///移动石头姿态
	RIDE_POSTURE_RIDE_STONE		= 4 UMETA(DisplayName = "RidePostureRideStone"),
	///盘腿姿态
	RIDE_POSTURE_CROSS_LEG = 5 UMETA(DisplayName = "RidePostureCrossLeg"),
	///二指施法姿态
	RIDE_POSTURE_TWO_FINGER = 6 UMETA(DisplayName = "RidePostureTwoFinger"),
	///吃鸡挂着大鸟姿态
	RIDE_POSTURE_HANG = 7 UMETA(DisplayName = "RidePostureHang")
};

///动作分类
UENUM(BlueprintType)
enum class ACTION_TYPE_ENUM : uint8
{
	///随机搞怪动作
	ACTION_TYPE_RANDOM = 1 UMETA(DisplayName = "ActionTypeRandom"),
	///待机动作（普通能切换的站立、poss动作、攻击待机、跳跃待机、死亡待机）
	ACTION_TYPE_STANDBY = 2 UMETA(DisplayName = "ActionTypeStandby"),
	///行走、跑步
	ACTION_TYPE_MOVE = 3 UMETA(DisplayName = "ActionTypeMove"),
	///快速受击动作
	ACTION_TYPE_HIT = 4 UMETA(DisplayName = "ActionTypeHit"),
	///拔刀、收刀动作
	ACTION_TYPE_SHIFT = 5 UMETA(DisplayName = "ActionTypeShift"),
	///跳跃起始
	ACTION_TYPE_JUMP_START = 6 UMETA(DisplayName = "ActionTypeJumpStart"),
	///跳跃空中
	ACTION_TYPE_JUMP_AIR = 7 UMETA(DisplayName = "ActionTypeJumpAir"),
	///跳跃结束
	ACTION_TYPE_JUMP_END = 8 UMETA(DisplayName = "ActionTypeJumpEnd"),
	///跳跃移动结束
	ACTION_TYPE_JUMP_MOVE_END = 9 UMETA(DisplayName = "ActionTypeJumpMoveEnd"),
	///眩晕
	ACTION_TYPE_DIZZY = 10 UMETA(DisplayName = "ActionTypeDizzy"),
	///睡眠
	ACTION_TYPE_SLEEP = 11 UMETA(DisplayName = "ActionTypeSleep"),
	///击退动作
	ACTION_TYPE_HIT_BACK = 12 UMETA(DisplayName = "ActionTypeHitBack"),
	///击退倒地动作
	ACTION_TYPE_HIT_FLY_FLOOR = 13 UMETA(DisplayName = "ActionTypeHitFlyFloor"),
	///击退起身动作
	ACTION_TYPE_HIT_FLY_GET_UP = 14 UMETA(DisplayName = "ActionTypeHitFlyGetUp"),
	///自杀死亡、攻击死亡、摔死
	ACTION_TYPE_DEATH = 15 UMETA(DisplayName = "ActionTypeDeath"),
	///复活
	ACTION_TYPE_REBORN = 16 UMETA(DisplayName = "ActionTypeReborn"),
	///各种技能动作
	ACTION_TYPE_SKILL = 17 UMETA(DisplayName = "ActionTypeSkill"),
	///表演动作
	ACTION_TYPE_SHOW = 18 UMETA(DisplayName = "ActionTypeShow"),
	///上下载具动作
	ACTION_TYPE_CARRIER = 19 UMETA(DisplayName = "ActionTypeCarrier"),
	///脸部表情动作
	ACTION_TYPE_FACE = 20 UMETA(DisplayName = "ActionTypeFace"),
	///同背景过渡动作
	ACTION_TYPE_FILTER = 21 UMETA(DisplayName = "ActionTypeFilter"),
	///绑定播放的前景表演动作
	ACTION_TYPE_FRONT_SHOW = 22 UMETA(DisplayName = "ActionTypeFrontShow"),
	///攀爬梯子动作
	ACTION_TYPE_CLIMB_LADDER = 23 UMETA(DisplayName = "ActionTypeClimbLadder"),
	///瞄准偏移动作
	ACTION_TYPE_AIM_OFFSET = 24 UMETA(DisplayName = "ActionTypeAimOffset"),
};

///动画分类
UENUM(BlueprintType)
enum class ANIM_TYPE_ENUM : uint8
{
	///动画序列（导入的普通动画资源）
	ANIM_TYPE_QEQUENCE = 1 UMETA(DisplayName = "AnimTypeSequence"),
	///动态蒙太奇
	ANIM_TYPE_DYNAMIC_MONTAGE = 2 UMETA(DisplayName = "AnimTypeDynamicMontage"),
	///蒙太奇
	ANIM_TYPE_MONTAGE = 3 UMETA(DisplayName = "AnimTypeMontage"),
	///动画合成
	ANIM_TYPE_COMPOSITE = 4 UMETA(DisplayName = "AnimTypeComposite"),
	///混合空间
	ANIM_TYPE_BLEND_SPACE = 5 UMETA(DisplayName = "AnimTypeBlendSpace"),
	///混合空间1D
	ANIM_TYPE_BLEND_SPACE_1D = 6 UMETA(DisplayName = "AnimTypeBlendSpace1D"),
	///目标偏移
	ANIM_TYPE_OFFSET_BLEND_SAPCE = 7 UMETA(DisplayName = "AnimTypeOffsetBlendSpace"),
	///目标偏移1D
	ANIM_TYPE_OFFSET_BLEND_SAPCE_1D = 8 UMETA(DisplayName = "AnimTypeOffsetBlendSpace1D"),
};

///前景背景动作分类
UENUM(BlueprintType)
enum class ACTION_GROUND_TYPE_ENUM : uint8
{
	ACTION_GROUND_TYPE_NULL = 0 UMETA(DisplayName = "AnimTypeSequence"),
	///背景
	ACTION_GROUND_TYPE_BACK = 1 UMETA(DisplayName = "AnimTypeDynamicMontage"),
	///前景
	ACTION_GROUND_TYPE_FRONT = 2 UMETA(DisplayName = "AnimTypeMontage"),
};

///动作位移设置类型
UENUM(BlueprintType)
enum class ACTION_DISPLACE_TYPE : uint8
{
	///真位移（正常表现）
	ACTION_DISPLACE_TYPE_REALLY = 0 UMETA(DisplayName = "ActionDisplaceTypeReally"),
	///假位移（如落霞剑）
	ACTION_DISPLACE_TYPE_FALSE = 1 UMETA(DisplayName = "ActionDisplaceTypeFalse"),
	///无位移（如镜头中的弱水剑）
	ACTION_DISPLACE_TYPE_NONE = 2 UMETA(DisplayName = "ActionDisplaceTypeNone"),
};

///动作枚举(枚举uint8上限<=255)
UENUM(BlueprintType)
enum class ACTION_POSE_ENUM : uint8
{
	///（待机与状态，规划：#1~15）
	///基本站立
	ACTION_POSE_STAND_1 = 1 UMETA(DisplayName = "ACTION_POSE_STAND_1"),
	///战斗待机
	ACTION_POSE_STAND_2 = 2 UMETA(DisplayName = "ACTION_POSE_STAND_2"),
	///其他
	ACTION_POSE_STAND_3 = 3 UMETA(DisplayName = "ACTION_POSE_STAND_3"),
	ACTION_POSE_STAND_4 = 4 UMETA(DisplayName = "ACTION_POSE_STAND_4"),
	ACTION_POSE_STAND_5 = 5 UMETA(DisplayName = "ACTION_POSE_STAND_5"),
	ACTION_POSE_STAND_6 = 6 UMETA(DisplayName = "ACTION_POSE_STAND_6"),
	ACTION_POSE_STAND_7 = 7 UMETA(DisplayName = "ACTION_POSE_STAND_7"),
	ACTION_POSE_STAND_8 = 8 UMETA(DisplayName = "ACTION_POSE_STAND_8"),
	ACTION_POSE_STAND_9 = 9 UMETA(DisplayName = "ACTION_POSE_STAND_9"),
	ACTION_POSE_STAND_10 = 10 UMETA(DisplayName = "ACTION_POSE_STAND_10"),
	///眩晕
	ACTION_POSE_DIZZY_11 = 11 UMETA(DisplayName = "ACTION_POSE_DIZZY_11"),
	///睡眠
	ACTION_POSE_SLEEP_12 = 12 UMETA(DisplayName = "ACTION_POSE_SLEEP_12"),
	///攀爬梯子
	ACTION_POSE_CLIMB_LADDER_15 = 15 UMETA(DisplayName = "ACTION_POSE_CLIMB_LADDER_15"),
	///（战斗过渡，规划：#16~20）
	///拔刀（自由→战斗）
	ACTION_POSE_SHIFT_16 = 16 UMETA(DisplayName = "ACTION_POSE_SHIFT_16"),
	///收刀（战斗→自由）
	ACTION_POSE_SHIFT_17 = 17 UMETA(DisplayName = "ACTION_POSE_SHIFT_17"),
	ACTION_POSE_SHIFT_18 = 18 UMETA(DisplayName = "ACTION_POSE_SHIFT_18"),
	ACTION_POSE_SHIFT_19 = 19 UMETA(DisplayName = "ACTION_POSE_SHIFT_19"),
	ACTION_POSE_SHIFT_20 = 20 UMETA(DisplayName = "ACTION_POSE_SHIFT_20"),
	///（移动，规划：#21~30）
	ACTION_POSE_MOVE_21 = 21 UMETA(DisplayName = "ACTION_POSE_MOVE_21"),
	ACTION_POSE_MOVE_22 = 22 UMETA(DisplayName = "ACTION_POSE_MOVE_22"),
	ACTION_POSE_MOVE_23 = 23 UMETA(DisplayName = "ACTION_POSE_MOVE_23"),
	ACTION_POSE_MOVE_24 = 24 UMETA(DisplayName = "ACTION_POSE_MOVE_24"),
	ACTION_POSE_MOVE_25 = 25 UMETA(DisplayName = "ACTION_POSE_MOVE_25"),
	///（随机，规划：#31~40）
	ACTION_POSE_RANDOM_31 = 31 UMETA(DisplayName = "ACTION_POSE_RANDOM_31"),
	ACTION_POSE_RANDOM_32 = 32 UMETA(DisplayName = "ACTION_POSE_RANDOM_32"),
	ACTION_POSE_RANDOM_33 = 33 UMETA(DisplayName = "ACTION_POSE_RANDOM_33"),
	ACTION_POSE_RANDOM_34 = 34 UMETA(DisplayName = "ACTION_POSE_RANDOM_34"),
	ACTION_POSE_RANDOM_35 = 35 UMETA(DisplayName = "ACTION_POSE_RANDOM_35"),
	///（跳跃，规划：#41~60）
	ACTION_POSE_JUMP_START_41 = 41 UMETA(DisplayName = "ACTION_POSE_JUMP_START_41"),
	ACTION_POSE_JUMP_START_42 = 42 UMETA(DisplayName = "ACTION_POSE_JUMP_START_42"),
	ACTION_POSE_JUMP_START_43 = 43 UMETA(DisplayName = "ACTION_POSE_JUMP_START_43"),
	ACTION_POSE_JUMP_START_44 = 44 UMETA(DisplayName = "ACTION_POSE_JUMP_START_44"),
	ACTION_POSE_JUMP_START_45 = 45 UMETA(DisplayName = "ACTION_POSE_JUMP_START_45"),
	ACTION_POSE_JUMP_END_46 = 46 UMETA(DisplayName = "ACTION_POSE_JUMP_END_46"),
	ACTION_POSE_JUMP_END_47 = 47 UMETA(DisplayName = "ACTION_POSE_JUMP_END_47"),
	ACTION_POSE_JUMP_END_48 = 48 UMETA(DisplayName = "ACTION_POSE_JUMP_END_48"),
	ACTION_POSE_JUMP_END_49 = 49 UMETA(DisplayName = "ACTION_POSE_JUMP_END_49"),
	ACTION_POSE_JUMP_END_50 = 50 UMETA(DisplayName = "ACTION_POSE_JUMP_END_50"),
	ACTION_POSE_JUMP_AIR_51 = 51 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_51"),
	ACTION_POSE_JUMP_AIR_52 = 52 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_52"),
	ACTION_POSE_JUMP_AIR_53 = 53 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_53"),
	ACTION_POSE_JUMP_AIR_54 = 54 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_54"),
	ACTION_POSE_JUMP_AIR_55 = 55 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_55"),
	ACTION_POSE_JUMP_AIR_56 = 56 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_56"),
	ACTION_POSE_JUMP_AIR_57 = 57 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_57"),
	ACTION_POSE_JUMP_AIR_58 = 58 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_58"),
	ACTION_POSE_JUMP_AIR_59 = 59 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_59"),
	ACTION_POSE_JUMP_AIR_60 = 60 UMETA(DisplayName = "ACTION_POSE_JUMP_AIR_60"),
	///（死亡，规划：#61~70）
	ACTION_POSE_DEATH_61 = 61 UMETA(DisplayName = "ACTION_POSE_DEATH_61"),
	ACTION_POSE_DEATH_62 = 62 UMETA(DisplayName = "ACTION_POSE_DEATH_62"),
	///（骑乘，规划：#71~80）
	ACTION_POSE_CARRIER_71 = 71 UMETA(DisplayName = "ACTION_POSE_CARRIER_71"),
	ACTION_POSE_CARRIER_72 = 72 UMETA(DisplayName = "ACTION_POSE_CARRIER_72"),
	///（技能，规划：#81~110、#231~245）
	ACTION_POSE_SKILL_81 = 81 UMETA(DisplayName = "ACTION_POSE_SKILL_81"),
	ACTION_POSE_SKILL_82 = 82 UMETA(DisplayName = "ACTION_POSE_SKILL_82"),
	ACTION_POSE_SKILL_83 = 83 UMETA(DisplayName = "ACTION_POSE_SKILL_83"),
	ACTION_POSE_SKILL_84 = 84 UMETA(DisplayName = "ACTION_POSE_SKILL_84"),
	ACTION_POSE_SKILL_85 = 85 UMETA(DisplayName = "ACTION_POSE_SKILL_85"),
	ACTION_POSE_SKILL_86 = 86 UMETA(DisplayName = "ACTION_POSE_SKILL_86"),
	ACTION_POSE_SKILL_87 = 87 UMETA(DisplayName = "ACTION_POSE_SKILL_87"),
	ACTION_POSE_SKILL_88 = 88 UMETA(DisplayName = "ACTION_POSE_SKILL_88"),
	ACTION_POSE_SKILL_89 = 89 UMETA(DisplayName = "ACTION_POSE_SKILL_89"),
	ACTION_POSE_SKILL_90 = 90 UMETA(DisplayName = "ACTION_POSE_SKILL_90"),
	ACTION_POSE_SKILL_91 = 91 UMETA(DisplayName = "ACTION_POSE_SKILL_91"),
	ACTION_POSE_SKILL_92 = 92 UMETA(DisplayName = "ACTION_POSE_SKILL_92"),
	ACTION_POSE_SKILL_93 = 93 UMETA(DisplayName = "ACTION_POSE_SKILL_93"),
	ACTION_POSE_SKILL_94 = 94 UMETA(DisplayName = "ACTION_POSE_SKILL_94"),
	ACTION_POSE_SKILL_95 = 95 UMETA(DisplayName = "ACTION_POSE_SKILL_95"),
	ACTION_POSE_SKILL_96 = 96 UMETA(DisplayName = "ACTION_POSE_SKILL_96"),
	ACTION_POSE_SKILL_97 = 97 UMETA(DisplayName = "ACTION_POSE_SKILL_97"),
	ACTION_POSE_SKILL_98 = 98 UMETA(DisplayName = "ACTION_POSE_SKILL_98"),
	ACTION_POSE_SKILL_99 = 99 UMETA(DisplayName = "ACTION_POSE_SKILL_99"),
	ACTION_POSE_SKILL_100 = 100 UMETA(DisplayName = "ACTION_POSE_SKILL_100"),
	///（快速受击，规划：#111~120）
	ACTION_POSE_HIT_111 = 111 UMETA(DisplayName = "ACTION_POSE_HIT_111"),
	ACTION_POSE_HIT_112 = 112 UMETA(DisplayName = "ACTION_POSE_HIT_112"),
	ACTION_POSE_HIT_113 = 113 UMETA(DisplayName = "ACTION_POSE_HIT_113"),
	ACTION_POSE_HIT_114 = 114 UMETA(DisplayName = "ACTION_POSE_HIT_114"),
	ACTION_POSE_HIT_115 = 115 UMETA(DisplayName = "ACTION_POSE_HIT_115"),
	///（脸部表情，规划：#121~130、#161~170）
	ACTION_POSE_FACE_121 = 121 UMETA(DisplayName = "ACTION_POSE_FACE_121"),
	ACTION_POSE_FACE_122 = 122 UMETA(DisplayName = "ACTION_POSE_FACE_122"),
	ACTION_POSE_FACE_123 = 123 UMETA(DisplayName = "ACTION_POSE_FACE_123"),
	ACTION_POSE_FACE_124 = 124 UMETA(DisplayName = "ACTION_POSE_FACE_124"),
	ACTION_POSE_FACE_125 = 125 UMETA(DisplayName = "ACTION_POSE_FACE_125"),
	ACTION_POSE_FACE_126 = 126 UMETA(DisplayName = "ACTION_POSE_FACE_126"),
	ACTION_POSE_FACE_127 = 127 UMETA(DisplayName = "ACTION_POSE_FACE_127"),
	ACTION_POSE_FACE_128 = 128 UMETA(DisplayName = "ACTION_POSE_FACE_128"),
	ACTION_POSE_FACE_129 = 129 UMETA(DisplayName = "ACTION_POSE_FACE_129"),
	ACTION_POSE_FACE_130 = 130 UMETA(DisplayName = "ACTION_POSE_FACE_130"),
	ACTION_POSE_FACE_161 = 161 UMETA(DisplayName = "ACTION_POSE_FACE_161"),
	ACTION_POSE_FACE_162 = 162 UMETA(DisplayName = "ACTION_POSE_FACE_162"),
	ACTION_POSE_FACE_163 = 163 UMETA(DisplayName = "ACTION_POSE_FACE_163"),
	ACTION_POSE_FACE_164 = 164 UMETA(DisplayName = "ACTION_POSE_FACE_164"),
	ACTION_POSE_FACE_165 = 165 UMETA(DisplayName = "ACTION_POSE_FACE_165"),
	ACTION_POSE_FACE_166 = 166 UMETA(DisplayName = "ACTION_POSE_FACE_166"),
	ACTION_POSE_FACE_167 = 167 UMETA(DisplayName = "ACTION_POSE_FACE_167"),
	ACTION_POSE_FACE_168 = 168 UMETA(DisplayName = "ACTION_POSE_FACE_168"),
	ACTION_POSE_FACE_169 = 169 UMETA(DisplayName = "ACTION_POSE_FACE_169"),
	ACTION_POSE_FACE_170 = 170 UMETA(DisplayName = "ACTION_POSE_FACE_170"),
	///（复活，规划：#131~140）
	ACTION_POSE_REBORN_131 = 131 UMETA(DisplayName = "ACTION_POSE_REBORN_131"),
	ACTION_POSE_REBORN_132 = 132 UMETA(DisplayName = "ACTION_POSE_REBORN_132"),
	ACTION_POSE_REBORN_133 = 133 UMETA(DisplayName = "ACTION_POSE_REBORN_133"),
	ACTION_POSE_REBORN_134 = 134 UMETA(DisplayName = "ACTION_POSE_REBORN_134"),
	ACTION_POSE_REBORN_135 = 135 UMETA(DisplayName = "ACTION_POSE_REBORN_135"),
	///（击退，规划：#141~160）
	ACTION_POSE_HIT_BACK_141 = 141 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_141"),
	ACTION_POSE_HIT_BACK_142 = 142 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_142"),
	ACTION_POSE_HIT_BACK_143 = 143 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_143"),
	ACTION_POSE_HIT_BACK_144 = 144 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_144"),
	ACTION_POSE_HIT_BACK_145 = 145 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_145"),
	ACTION_POSE_HIT_BACK_146 = 146 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_146"),
	ACTION_POSE_HIT_BACK_147 = 147 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_147"),
	ACTION_POSE_HIT_BACK_148 = 148 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_148"),
	ACTION_POSE_HIT_BACK_149 = 149 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_149"),
	ACTION_POSE_HIT_BACK_150 = 150 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_150"),
	ACTION_POSE_HIT_BACK_151 = 151 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_151"),
	ACTION_POSE_HIT_BACK_152 = 152 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_152"),
	ACTION_POSE_HIT_BACK_153 = 153 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_153"),
	ACTION_POSE_HIT_BACK_154 = 154 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_154"),
	ACTION_POSE_HIT_BACK_155 = 155 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_155"),
	ACTION_POSE_HIT_BACK_156 = 156 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_156"),
	ACTION_POSE_HIT_BACK_157 = 157 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_157"),
	ACTION_POSE_HIT_BACK_158 = 158 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_158"),
	ACTION_POSE_HIT_BACK_159 = 159 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_159"),
	ACTION_POSE_HIT_BACK_160 = 160 UMETA(DisplayName = "ACTION_POSE_HIT_BACK_160"),
	///（击倒，规划：#171~180）
	ACTION_POSE_HIT_FLY_FLOOR_171 = 171 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_171"),
	ACTION_POSE_HIT_FLY_FLOOR_172 = 172 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_172"),
	ACTION_POSE_HIT_FLY_FLOOR_173 = 173 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_173"),
	ACTION_POSE_HIT_FLY_FLOOR_174 = 174 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_174"),
	ACTION_POSE_HIT_FLY_FLOOR_175 = 175 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_175"),
	ACTION_POSE_HIT_FLY_FLOOR_176 = 176 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_176"),
	ACTION_POSE_HIT_FLY_FLOOR_177 = 177 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_177"),
	ACTION_POSE_HIT_FLY_FLOOR_178 = 178 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_178"),
	ACTION_POSE_HIT_FLY_FLOOR_179 = 179 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_179"),
	ACTION_POSE_HIT_FLY_FLOOR_180 = 180 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_FLOOR_180"),
	///（击倒起身，规划：#181~190）
	ACTION_POSE_HIT_FLY_GET_UP_181 = 181 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_181"),
	ACTION_POSE_HIT_FLY_GET_UP_182 = 182 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_182"),
	ACTION_POSE_HIT_FLY_GET_UP_183 = 183 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_183"),
	ACTION_POSE_HIT_FLY_GET_UP_184 = 184 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_184"),
	ACTION_POSE_HIT_FLY_GET_UP_185 = 185 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_185"),
	ACTION_POSE_HIT_FLY_GET_UP_186 = 186 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_186"),
	ACTION_POSE_HIT_FLY_GET_UP_187 = 187 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_187"),
	ACTION_POSE_HIT_FLY_GET_UP_188 = 188 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_188"),
	ACTION_POSE_HIT_FLY_GET_UP_189 = 189 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_189"),
	ACTION_POSE_HIT_FLY_GET_UP_190 = 190 UMETA(DisplayName = "ACTION_POSE_HIT_FLY_GET_UP_190"),
	///（表演，规划：#201~230）
	ACTION_POSE_SHOW_201 = 201 UMETA(DisplayName = "ACTION_POSE_SHOW_201"),
	ACTION_POSE_SHOW_202 = 202 UMETA(DisplayName = "ACTION_POSE_SHOW_202"),
	ACTION_POSE_SHOW_203 = 203 UMETA(DisplayName = "ACTION_POSE_SHOW_203"),
	ACTION_POSE_SHOW_204 = 204 UMETA(DisplayName = "ACTION_POSE_SHOW_204"),
	ACTION_POSE_SHOW_205 = 205 UMETA(DisplayName = "ACTION_POSE_SHOW_205"),
	ACTION_POSE_SHOW_206 = 206 UMETA(DisplayName = "ACTION_POSE_SHOW_206"),
	ACTION_POSE_SHOW_207 = 207 UMETA(DisplayName = "ACTION_POSE_SHOW_207"),
	ACTION_POSE_SHOW_208 = 208 UMETA(DisplayName = "ACTION_POSE_SHOW_208"),
	ACTION_POSE_SHOW_209 = 209 UMETA(DisplayName = "ACTION_POSE_SHOW_209"),
	ACTION_POSE_SHOW_210 = 210 UMETA(DisplayName = "ACTION_POSE_SHOW_210"),
	ACTION_POSE_SHOW_211 = 211 UMETA(DisplayName = "ACTION_POSE_SHOW_211"),
	ACTION_POSE_SHOW_212 = 212 UMETA(DisplayName = "ACTION_POSE_SHOW_212"),
	ACTION_POSE_SHOW_213 = 213 UMETA(DisplayName = "ACTION_POSE_SHOW_213"),
	ACTION_POSE_SHOW_214 = 214 UMETA(DisplayName = "ACTION_POSE_SHOW_214"),
	ACTION_POSE_SHOW_215 = 215 UMETA(DisplayName = "ACTION_POSE_SHOW_215"),
	ACTION_POSE_SHOW_216 = 216 UMETA(DisplayName = "ACTION_POSE_SHOW_216"),
	ACTION_POSE_SHOW_217 = 217 UMETA(DisplayName = "ACTION_POSE_SHOW_217"),
	ACTION_POSE_SHOW_218 = 218 UMETA(DisplayName = "ACTION_POSE_SHOW_218"),
	ACTION_POSE_SHOW_219 = 219 UMETA(DisplayName = "ACTION_POSE_SHOW_219"),
	ACTION_POSE_SHOW_220 = 220 UMETA(DisplayName = "ACTION_POSE_SHOW_220"),
	ACTION_POSE_SHOW_221 = 221 UMETA(DisplayName = "ACTION_POSE_SHOW_221"),
	ACTION_POSE_SHOW_222 = 222 UMETA(DisplayName = "ACTION_POSE_SHOW_222"),
	ACTION_POSE_SHOW_223 = 223 UMETA(DisplayName = "ACTION_POSE_SHOW_223"),
	ACTION_POSE_SHOW_224 = 224 UMETA(DisplayName = "ACTION_POSE_SHOW_224"),
	ACTION_POSE_SHOW_225 = 225 UMETA(DisplayName = "ACTION_POSE_SHOW_225"),
	ACTION_POSE_SHOW_226 = 226 UMETA(DisplayName = "ACTION_POSE_SHOW_226"),
	ACTION_POSE_SHOW_227 = 227 UMETA(DisplayName = "ACTION_POSE_SHOW_227"),
	ACTION_POSE_SHOW_228 = 228 UMETA(DisplayName = "ACTION_POSE_SHOW_228"),
	ACTION_POSE_SHOW_229 = 229 UMETA(DisplayName = "ACTION_POSE_SHOW_229"),
	ACTION_POSE_SHOW_230 = 230 UMETA(DisplayName = "ACTION_POSE_SHOW_230"),
	///（技能(补充)，规划：#231~245）
	ACTION_POSE_SKILL_231 = 231 UMETA(DisplayName = "ACTION_POSE_SKILL_231"),
	ACTION_POSE_SKILL_232 = 232 UMETA(DisplayName = "ACTION_POSE_SKILL_232"),
	ACTION_POSE_SKILL_233 = 233 UMETA(DisplayName = "ACTION_POSE_SKILL_233"),
	ACTION_POSE_SKILL_234 = 234 UMETA(DisplayName = "ACTION_POSE_SKILL_234"),
	ACTION_POSE_SKILL_235 = 235 UMETA(DisplayName = "ACTION_POSE_SKILL_235"),
	ACTION_POSE_SKILL_236 = 236 UMETA(DisplayName = "ACTION_POSE_SKILL_236"),
	ACTION_POSE_SKILL_237 = 237 UMETA(DisplayName = "ACTION_POSE_SKILL_237"),
	ACTION_POSE_SKILL_238 = 238 UMETA(DisplayName = "ACTION_POSE_SKILL_238"),
	ACTION_POSE_SKILL_239 = 239 UMETA(DisplayName = "ACTION_POSE_SKILL_239"),
	ACTION_POSE_SKILL_240 = 240 UMETA(DisplayName = "ACTION_POSE_SKILL_240"),
	ACTION_POSE_SKILL_241 = 241 UMETA(DisplayName = "ACTION_POSE_SKILL_241"),
	ACTION_POSE_SKILL_242 = 242 UMETA(DisplayName = "ACTION_POSE_SKILL_242"),
	ACTION_POSE_SKILL_243 = 243 UMETA(DisplayName = "ACTION_POSE_SKILL_243"),
	ACTION_POSE_SKILL_244 = 244 UMETA(DisplayName = "ACTION_POSE_SKILL_244"),
	ACTION_POSE_SKILL_245 = 245 UMETA(DisplayName = "ACTION_POSE_SKILL_245"),
	///（绑定前景，规划：#246~250）
	ACTION_POSE_FRONT_SHOW_246 = 246 UMETA(DisplayName = "ACTION_POSE_FRONT_SHOW_246"),
	ACTION_POSE_FRONT_SHOW_247 = 247 UMETA(DisplayName = "ACTION_POSE_FRONT_SHOW_247"),
	ACTION_POSE_FRONT_SHOW_248 = 248 UMETA(DisplayName = "ACTION_POSE_FRONT_SHOW_248"),
	ACTION_POSE_FRONT_SHOW_249 = 249 UMETA(DisplayName = "ACTION_POSE_FRONT_SHOW_249"),
	ACTION_POSE_FRONT_SHOW_250 = 250 UMETA(DisplayName = "ACTION_POSE_FRONT_SHOW_250"),
	///（瞄准偏移动作）
	ACTION_POSE_AIM_OFFSET_254 = 254 UMETA(DisplayName = "ACTION_POSE_AIM_OFFSET_254"),
	///背景动作过渡
	ACTION_POSE_FILTER_255 = 255 UMETA(DisplayName = "ACTION_POSE_FILTER_255"),
};

///自定义移动模型枚举
UENUM(BlueprintType)
enum class CUSTOM_MOVEMENT_MODE_ENUM : uint8
{
	///无
	CUSTOM_MOVEMENT_NONE = 0 UMETA(DisplayName = "None"),
	///根骨骼位移模式
	CUSTOM_MOVEMENT_ROOT_MOTION = 1 UMETA(DisplayName = "RootMotion"),
	///爬梯子模式
	CUSTOM_MOVEMENT_LADDER = 2 UMETA(DisplayName = "Ladder"),
};

///玩家交互状态
UENUM(BlueprintType)
enum class APLAYER_INTERACTIVE_ENUM : uint8
{
	///NPC交谈中
	APLAYER_INTERACTIVE_TALKTONPC UMETA(DisplayName = "APLAYER_INTERACTIVE_TALKTONPC"),
	///SpellBox交互中
	APLAYER_INTERACTIVE_TALKTOSPELLBOX UMETA(DisplayName = "APLAYER_INTERACTIVE_TALKTOSPELLBOX"),
	///DropBox交互中
	APLAYER_INTERACTIVE_TALKTODROPBOX UMETA(DisplayName = "APLAYER_INTERACTIVE_TALKTODROPBOX"),
	///目标追踪中
	APLAYER_INTERACTIVE_TRACETOTARGET UMETA(DisplayName = "APLAYER_INTERACTIVE_TRACETOTARGET"),
	///目标选择中
	APLAYER_INTERACTIVE_SECLECTTARGET UMETA(DisplayName = "APLAYER_INTERACTIVE_SECLECTTARGET"),
	///交互成功
	APLAYER_INTERACTIVE_SUCCESS UMETA(DisplayName = "APLAYER_INTERACTIVE_SUCCESS"),

	///用于判断优先级的状态，直到下一个判断优先级的判断，区间内的状态优先级一样
	APLAYER_TALKTONPC,

	///受击退中
	APLAYER_INTERACTIVE_HITBACK UMETA(DisplayName = "APLAYER_INTERACTIVE_HITBACK"),

	///用于判断优先级的状态，直到下一个判断优先级的判断，区间内的状态优先级一样
	APLAYER_EFFECT,

	///一般状态
	APLAYER_INTERACTIVE_NODE UMETA(DisplayName = "APLAYER_INTERACTIVE_NODE"),
};

/** 动作中断结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FACTION_BREAK_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		FString NameDesc;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 RandomState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 StandByState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 MoveState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 HitState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 ShiftState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 JumpStartState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 JumpAirState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 JumpEndState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 JumpEndMoveState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 DizzyState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 SleepState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 HitBackState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 HitFlyFloorState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 HitFlyFloorGetState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 DeathState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 RebornState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 SkillState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 ShowState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 CarrierState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 FaceState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 FilterState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 FrontShowState = 0;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 ClimbLadderState = 0;
public:
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) {
		FString TempNameDesc = this->NameDesc.TrimStartAndEnd();
		bool IsError = TempNameDesc.IsEmpty();
		if (IsError)
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("NameDesc Format Is Empty!\n"));
		}
		else {
			ResultInfo.Result = Ok;
		}
	}

	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/** 动作结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FACTION_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///备注
	///	没有任何功能，仅供策划记录及查看，说明此行动作的用途
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CharacterData", DisplayName = "备注")
		FString Remarks;
	///动作状态类型（请保持默认）
	///	动作状态类型、动作状态标识、动画资源类型、动作状态混合索引…等，需要配合使用
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		ACTION_TYPE_ENUM ActionType;
	///动作状态标识（请保持默认）
	///	动作状态类型、动作状态标识、动画资源类型、动作状态混合索引…等，需要配合使用
	///注意：
	///	已知风险：不得重复，否则后续内容将失效
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		ACTION_POSE_ENUM ActionPose;
	///动作状态混合索引（请保持默认）
	///	动作状态类型、动作状态标识、动画资源类型、动作状态混合索引…等，需要配合使用
	///注意：
	///	已知风险：在每个“动作状态类型”中，不得重复，否则后续内容将失效
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 BlendIndex = 0;
	///关联背景动作
	///支持：
	///	播放前景动作（动态/蒙太奇）时，额外触发一个背景动作（@CST-1022）
	///注意：
	///	使用方法限定：目前只应用于“前景动作”
	///		如，“击飞”前景动作播放时，同时也切换了“击倒”的背景动作（@DT_M_Sword_PC）
	///		如，“起跳”前景动作播放时，同时也切换了“下落”的背景动作（@DT_M_Sword_PC）
	///	已知风险：可能导致循环触发，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		FName BindBackGroundId;
	///关联前景动作
	///支持：
	///	播放背景动作（移动/待机）时，额外触发/中止一个前景动作（@CST-7447）
	///注意：
	///	使用方法限定：目前只应用于“背景动作”
	///		如，“跑步”时，额外播放“前景表演扛鼎跑步”（@DT_M_Sword_QuanKunPocket_1）
	///		如，“待机”时，额外播放“带有光效通知的举盾表现”（@DT_GW1172_1）
	///	已知风险：可能导致循环触发，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		FName BindFrontGroundId;
	///关联瞄准偏移动作
	///支持：
	///	播放前、背景动作（移动/待机）时，额外融合一个瞄准偏移动作
	///注意：
	///	使用方法限定：目前只应用于远程吃鸡
	///	已知风险：可能导致循环触发，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		FName BindAimOffsetId;
	///是否激活“上半身与下半身”融合（如“上半身拔刀”）
	///注意：
	///	已知风险：此处几种混合，同时只能生效一种，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		bool IsBodyHalfBlend;
	///是否激活“脸部与脖子以下”融合（如“脸部表情”）
	///注意：
	///	已知风险：此处几种混合，同时只能生效一种，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		bool IsFaceHalfBlend;
	///动画资源类型（请保持默认）
	///	动作状态类型、动作状态标识、动画资源类型、动作状态混合索引…等，需要配合使用
	///注意：
	///	已知风险：应当使用正确的资源类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		ANIM_TYPE_ENUM AnimType;
	///动画资源
	///注意：
	///	已知风险：模型的骨骼与动作资源的骨骼不匹配时，将表现异常，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		TSoftObjectPtr<UAnimationAsset> AnimPath;
	///动作播放结束后，是否回到待机
	///	是：结束本动作，衔接对应背景动作（如“技能表现后，回到待机”）
	///	否：停在本动作最后一帧（如“死亡后，趴着不动”）
	///注意：
	///	使用方法限定：只有动作“不循环”时，此参数才生效
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		bool IsReturnStandy;
	///是否动作循环
	///	是：循环播放（不停地）
	///	否：只播放一次，然后结束
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		bool IsLoop;
	
	///是否要设置位移(例：目前剧情技能表现用)
	///UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
	///	bool IsResetDisplaceType = false;
	///重置位移类型(目前剧情技能表演用)
	///UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
	///	ACTION_DISPLACE_TYPE ResetDisplaceType;
	
	///播放起始位置（秒）
	///支持：
	///	可以从动作的任意时刻开始播放，不需要从头开始
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		float PlayStartPosition;
	///动作播放速度（倍）
	///	与动画资源的RateScale属性同时生效，表现为“乘法”
	///注意：
	///	使用方法限定：动画资源类型为“蒙太奇”时，此参数无效（如“拔刀收刀”）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		float PlayRate = 1.0f;
	///动作淡入时间（秒）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		float BlendInTime;
	///动作淡出时间（秒）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		float BlendOutTime;
	
	///从序列结束到触发器混合的时间(未启用)【小于0时,使用BlendOutTime值;大于等于0时,则使用(CurrentSectionLength-PosInSection)/FMath::Abs(PlayRate * Montage->RateScale)】
	///UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
	///	float BlendOutTriggerTime;
	
	///蒙太奇剪辑片段名（默认“Default”）
	///支持：
	///	配合蒙太奇资源的片段名使用
	///	当前项目的资源规范中，蒙太奇资源都要求只有一个片段且命名“Default”，因此，此处无需特别配置
	///注意：
	///	动画资源类型“蒙太奇”专用
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		FName MontageSectionId = "Default";
	///上马动作位移开始时机（百分比）
	///支持：
	///	描述从上马动作的何时开始，进行位置偏移表现（@CST-2693）
	///		如，“0.82”代表从此动作时长的82%开始
	///注意：
	///	上马动作专用
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		float RiderGetOnTimePercent = 1.0f;
	///隐藏部件列表
	///支持：
	///	在播放某动作的过程中，隐藏单位的部件显示（@CST-3477）
	///注意：
	///	已知风险：下拉菜单中，“Bodys部件”（Mesh）不支持隐藏，请避免使用
	///	已知风险：Wrist＝护腕、Waist＝腰带，拼写接近，请注意区分
	///	已知风险：目前隐藏部件表现尚不支持”多个描述同时作用“
	///		①“动作”之间冲突：前景与背景都有配置时，前景动作的隐藏配置生效（前景＞背景）
	///		②“动画通知状态”之间冲突：后续触发会覆盖已有表现（后＞先）
	///		③“动作”与“动画通知状态”冲突：开始时，动作先触发，动画通知状态后触发；结束时，动画通知状态先触发，动作后触发（动作＞动画）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		TArray<MODEL_PART_TYPE> HidePartDatas;

	///（程序用，策划无需在意，请保持默认）
	///当前的对象
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterDataCode")
		ACharacter* Character;
	///（程序用，策划无需在意，请保持默认）
	///动作ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterDataCode")
		FName Id;
	///（程序用，策划无需在意，请保持默认）
	///当前的动画对象[序列、动态蒙太奇、蒙太奇]
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterDataCode")
		UAnimSequenceBase* CurAnimSquenceBase;
	///（程序用，策划无需在意，请保持默认）
	///当前的动画对象[混合空间]
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterDataCode")
		UBlendSpaceBase* CurBlendSpaceBase;
	///（程序用，策划无需在意，请保持默认）
	///动态唯一ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterDataCode")
		int32 DynamicId = 0;
	///（程序用，策划无需在意，请保持默认）
	///动作名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterDataCode")
		FString ActionName;
	///（程序用，策划无需在意，请保持默认）
	///连续动作标识ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterDataCode")
		int32 ContinuousId = 0;
	///（程序用，策划无需在意，请保持默认）
	///动作类型[前景还是背景]
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterDataCode")
		ACTION_GROUND_TYPE_ENUM GroundType;

	///std::function<void(ACharacter *, FString)> PlayEffectCallback;
};

/** 连续动作结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FACTION_CONTINUOUS : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///连续动作标识
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Id")
		int32 Id = 0;
	///动作ID数组
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "continuousActionIds")
		TArray<FName> ActionIds;
	///动作起始帧时间数组
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "continuousActionStartTimes")
		TArray<float> ActionStartTimes;
};

/** 怪物结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMONSTER_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Uname")
		FString Uname;
	///初始化动作
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "InitActionId")
		FString InitActionId;
	///单位脚本类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "EntityScript")
		FString EntityScript;
	///模型编号（@DT_ModelCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "ModelNumber")
		FString ModelNumber;
	///死亡特效配置
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "DeadEffectId")
		FString DeadEffectId;
	///出生前光效（@DT_EffectCfg）
	///支持：
	///	光效刷怪表现（@CST-1631）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "BeforeSpawnEffectId")
		FString BeforeSpawnEffectId;
	///出生前光效时长（秒）
	///支持：
	///	光效刷怪表现（@CST-1631）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "BeforeSpawnPlayEffectTime")
		float BeforeSpawnPlayEffectTime;
	///AI战斗追击距离（米）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "ChaseDistance")
		float ChaseDistance;
	///模型缩放倍率（倍）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "ModelScale")
		float ModelScale = 1.0f;
	///参数1
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "Param1")
		FString Param1;
	///参数2
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "Param2")
		FString Param2;
	///参数3
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "Param3")
		FString Param3;
	///参数4
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "Param4")
		FString Param4;
	///参数5
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "Param5")
		FString Param5;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool EntityScriptResult = !EntityScript.IsEmpty() && (EntityScript[0] >= 'A' && EntityScript[0] <= 'Z');
		bool ModelNumberResult = !ModelNumber.IsEmpty();
		bool BeforeSpawnPlayEffectTimeResult = BeforeSpawnPlayEffectTime >= 0.0f;
		bool result = EntityScriptResult && ModelNumberResult && BeforeSpawnPlayEffectTimeResult;
		if (result)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			if (!EntityScriptResult) ResultInfo.CheckLog += FString::Printf(TEXT("EntityScript: \"%s\" is config error!  "), *EntityScript);
			if (!ModelNumberResult) ResultInfo.CheckLog += FString::Printf(TEXT("Modelnumber cannot be empty!  "));
			if (!BeforeSpawnPlayEffectTimeResult) ResultInfo.CheckLog += FString::Printf(TEXT("BeforeSpawnPlayEffectTime: \"%f\" is config error!  "), BeforeSpawnPlayEffectTime);
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/** NPC结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FNPC_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Uname")
		FString Uname;
	///初始化动作
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "InitActionId")
		FString InitActionId;
	///模型编号（@DT_ModelCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "ModelNumber")
		FString ModelNumber;
	///死亡特效配置
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "DeadEffectId")
		FString DeadEffectId;
	///出生前光效（@DT_EffectCfg）
	///支持：
	///	光效刷怪表现（@CST-1631）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "BeforeSpawnEffectId")
		FString BeforeSpawnEffectId;
	///出生前光效时长（秒）
	///支持：
	///	光效刷怪表现（@CST-1631）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "BeforeSpawnPlayEffectTime")
		float BeforeSpawnPlayEffectTime;
	///模型缩放倍率（倍）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "ModelScale")
		float ModelScale = 1.0f;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool ModelNumberResult = !ModelNumber.IsEmpty();
		bool ModelScaleResult = ModelScale > 0.0f;
		if (ModelNumberResult && ModelScaleResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			if (!ModelNumberResult) ResultInfo.CheckLog += FString::Printf(TEXT("ModelNumber cannot be empty!  "));
			if (!ModelScaleResult) ResultInfo.CheckLog += FString::Printf(TEXT("ModelScale: \"%f\" is config error!  "), ModelScale);
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/** SceneObject结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSCENEOBJECT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Uname")
		FString Uname;
	///模型编号（@DT_ModelCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "ModelNumber")
		FString ModelNumber;
	///模型缩放倍率（倍）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "ModelScale")
		float ModelScale = 1.0f;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool UnameResult = !Uname.IsEmpty();
		bool ModelNumberResult = !ModelNumber.IsEmpty();
		bool ModelScaleResult = ModelScale > 0.0f;
		if (UnameResult && ModelNumberResult && ModelScaleResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			if (!UnameResult) ResultInfo.CheckLog += FString::Printf(TEXT("Uname cannot be empty!  "));
			if (!ModelNumberResult) ResultInfo.CheckLog += FString::Printf(TEXT("ModelNumber cannot be empty!  "));
			if (!ModelScaleResult) ResultInfo.CheckLog += FString::Printf(TEXT("ModelScale: \"%f\" is config error!  "), ModelScale);
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/** SpellBox结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSPELLBOX_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Uname")
		FString Uname;
	///模型编号（@DT_ModelCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "ModelNumber")
		FString ModelNumber;
	///出生前光效（@DT_EffectCfg）
	///支持：
	///	光效刷怪表现（@CST-1631）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "BeforeSpawnEffectId")
		FString BeforeSpawnEffectId;
	///光效大小（倍）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "effectModelScale")
		float effectModelScale = 1.0f;
	///模型缩放倍率（倍）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "ModelScale")
		float ModelScale = 1.0f;
	///是否显示提示
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "IsShowTips")
		bool IsShowTips = false;
	///是否可站立
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "IsStandUp")
		bool IsStandUp = false;
	///AI检测范围形状类型
	///	1：矩形
	///支持：
	///	SpellboxDoor专用配置（@CST-5312）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "Shape")
		int32 Shape = 1;
	///AI检测范围形状参数
	///	对于1矩形：长 | 宽 | 高（米）
	///支持：
	///	SpellboxDoor专用配置（@CST-5312）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "Bounds")
		FVector Bounds;
	///AI检测范围形状偏移
	///	对于1矩形：前 | 左 | 上（米）
	///支持：
	///	SpellboxDoor专用配置（@CST-5312）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "Transform")
		FTransform Transform;
	///参数1
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Param1")
		FString Param1;
	///参数2
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Param2")
		FString Param2;
	///参数3
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Param3")
		FString Param3;
	///参数4
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Param4")
		FString Param4;
	///参数5
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Param5")
		FString Param5;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool ModelScaleResult = ModelScale > 0.0f;
		if (ModelScaleResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			if (!ModelScaleResult) ResultInfo.CheckLog += FString::Printf(TEXT("ModelScale: \"%f\" is config error!\n"), ModelScale);
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/** Trap结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTRAP_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Uname")
		FString Uname;
	///模型编号（@DT_ModelCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "ModelNumber")
		FString ModelNumber;
	///模型缩放倍率（倍）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "ModelScale")
		float ModelScale = 1.0f;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool UnameResult = !Uname.IsEmpty();
		bool ModelNumberResult = !ModelNumber.IsEmpty();
		bool ModelScaleResult = ModelScale > 0.0f;
		if (UnameResult && ModelNumberResult && ModelScaleResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			if (!UnameResult) ResultInfo.CheckLog += FString::Printf(TEXT("Uname cannot be empty!  "));
			if (!ModelNumberResult) ResultInfo.CheckLog += FString::Printf(TEXT("ModelNumber cannot be empty!  "));
			if (!ModelScaleResult) ResultInfo.CheckLog += FString::Printf(TEXT("ModelScale: \"%f\" is config error!  "), ModelScale);
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/** 部件位置、旋转、缩放参数数据结构 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPART_TRANSFORM
{
	GENERATED_BODY()
public:
	///相对位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "RelativeLocation")
		FVector RelativeLocation = FVector(0.f, 0.f, 0.f);
	///相对旋转
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "RelativeRotation")
		FRotator RelativeRotation = FRotator(0.f, 0.f, 0.f);;
	///相对缩放
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelPartData", DisplayName = "RelativeScale3D")
		FVector RelativeScale3D = FVector(1.0f);
};

/** Mesh绑定结构体 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMESH_BIND_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///骨骼模型
	///支持：
	///	额外部件绑定表现（@CST-3326）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "SkeletaMeshPath")
		TSoftObjectPtr<USkeletalMesh> SkeletalMeshPath;
	///绑定时骨骼动画
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "AnimationAssetPath")
		TSoftObjectPtr<UAnimationAsset> AnimationAssetPath;
	///是否开启骨骼模型的碰撞
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "IsCollision")
		bool IsCollision = false;
	///静态模型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "StaticMeshPath")
		TSoftObjectPtr<UStaticMesh> StaticMeshPath;
	///绑定点名称（目标骨骼点或插槽点）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "SocketName")
		FName SocketName;
	///绑定光效
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "EffectID")
		FString EffectID;
	///部件变形
	///注意：
	///	暂不支持：MODEL_PART_BODYS、MODEL_PART_FABAO
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterData", DisplayName = "PartTransform")
		FPART_TRANSFORM PartTransform;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Remarks")
		FString Remarks;

public:
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) {
		bool SkeletalMeshPathResult = this->SkeletalMeshPath.IsNull() ? true : FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->SkeletalMeshPath.ToString());
		bool AnimationAssetPathResult = this->AnimationAssetPath.IsNull() ? true : FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->AnimationAssetPath.ToString());
		bool StaticMeshPathResult = this->StaticMeshPath.IsNull() ? true : FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->StaticMeshPath.ToString());
		bool IsError = !SkeletalMeshPathResult || !AnimationAssetPathResult || !StaticMeshPathResult;
		if (IsError)
		{
			ResultInfo.Result = Error;
		}
		else {
			ResultInfo.Result = Ok;
		}
		if (!SkeletalMeshPathResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("%s is Error, "), *this->SkeletalMeshPath.ToString());
		}
		if (!AnimationAssetPathResult){
			ResultInfo.CheckLog += FString::Printf(TEXT("%s is Error, "), *this->AnimationAssetPath.ToString());
		}
		if (!StaticMeshPathResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("%s is Error, "), *this->StaticMeshPath.ToString());
		}
		if (IsError) {
			ResultInfo.CheckLog += TEXT("\n");
		}
	}

	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

///部件插槽绑定类型
UENUM(BlueprintType)
enum class PART_SLOT_BIND_OBJ_ENUM : uint8
{
	PART_SLOT_BIND_OBJ_ACTOR = 0 UMETA(DisplayName = "PART_SLOT_BIND_OBJ_ACTOR"),//actor对象
	PART_SLOT_BIND_OBJ_PARTICLE = 1 UMETA(DisplayName = "PART_SLOT_BIND_OBJ_PARTICLE"),//粒子
};
/** 部件插槽绑定结构体 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPART_SLOT_BIND_OBJ_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///用于唯一标识
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "WeaponBindObjData", DisplayName = "Id")
		int32 Id = 0;
	///绑定对象的类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "WeaponBindObjData", DisplayName = "WeaponBindObjType")
		PART_SLOT_BIND_OBJ_ENUM BindObjType;
	///插槽名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "WeaponBindObjData", DisplayName = "SoketName")
		FName SoketName;
	///是否绑定
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "WeaponBindObjData", DisplayName = "SoketName")
		bool bBind = false;
	///偏移的相对位置
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "WeaponBindObjData", DisplayName = "Position")
		FVector RelativePosition = FVector(0.0f, 0.0f, 0.0f);
	///偏移的相对方向
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "WeaponBindObjData", DisplayName = "Direction")
		FVector RelativeDirection = FVector(0.0f, 0.0f, 0.0f);;

	///要被绑定的EntityID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "ActorData", DisplayName = "ByBindEntityID")
		int32 ByBindEntityID = 0;
	///自己EntityID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "ActorData", DisplayName = "MainEntityID")
		int32 MainEntityID = 0;

	///粒子ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Particle", DisplayName = "Direction")
		FString ParticleId;
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FCHARACTER_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CharacterData")
		int32 CharacterId = 0;
};

/** 选择角色和创建角色动作表 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSELECT_CREAT_ACTION_DATE : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///动作名称（匹配对应动作表，@如：DT_M_Sword_Performer）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "AnimationName")
		FName AnimationName;

	///动作组动画合成名称（匹配对应动作表，@如：DT_M_Sword_Performer）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "AnimationGroupName")
		FName AnimationGroupName;

	///职业名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "RoleProfessionName")
		FName RoleProfessionName;

	///播放语音ID：≤24小时（@DT_AudioCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "RoleVoiceID")
		TArray<FString> RoleVoiceID;

	///播放语音ID：24~72小时（@DT_AudioCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "RoleVoiceID_1")
		TArray<FString> RoleVoiceID_1;

	///播放语音ID：72~168小时（@DT_AudioCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "RoleVoiceID_2")
		TArray<FString> RoleVoiceID_2;

	///播放语音ID：168~720小时（@DT_AudioCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "RoleVoiceID_3")
		TArray<FString> RoleVoiceID_3;

	///播放语音ID：＞720小时（@DT_AudioCfg）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "RoleVoiceID_4")
		TArray<FString> RoleVoiceID_4;
	
	///说明
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "Description")
		FString Description;

public:
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) {
		bool AnimationNameResult = this->AnimationName.IsNone();
		bool AnimationGroupNameResult = this->AnimationGroupName.IsNone();
		bool RoleProfessionNameResult = this->RoleProfessionName.IsNone();
		bool IsError = AnimationNameResult || AnimationGroupNameResult || RoleProfessionNameResult;
		if (IsError)
		{
			ResultInfo.Result = Error;
		}
		else {
			ResultInfo.Result = Ok;
		}
		if (AnimationNameResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("AnimationName Format Is Empty, "));
		}
		if (AnimationGroupNameResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("AnimationGroupName Format Is Empty, "));
		}
		if (RoleProfessionNameResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("RoleProfessionName Format Is Empty, "));
		}
		if (IsError) {
			ResultInfo.CheckLog += TEXT("\n");
		}
	}

	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/** 角色不同方向移动速度修正 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FDIR_MOVE_SPEED : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///PC移动偏航角（角度）
	///支持：
	///	PC向各个方向移动速度不一致的表现（@CST-1985）
	///		具体配置值方向时，速度修正＝配置修正
	///		在两个配置值之间时，线性混合速度修正
	///注意：
	///	要求配置覆盖范围≥[﹣180°,180°]
	///	要求偏航角的取值升序排列，否则将会计算错误
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "YawAngle")
		float DirAngle;
	///最大速度的百分比（倍，取值范围(0,1]）
	///支持：
	///	PC向各个方向移动速度不一致的表现（@CST-1985）
	///		具体配置值方向时，速度修正＝配置修正
	///		在两个配置值之间时，线性混合速度修正
	///注意：
	///	要求偏航角﹣180°、﹢180°时，取值相同
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData", DisplayName = "CharacterSpeed")
		float CharacterSpeed;
};

/** 载具结构体对象 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCARRIER_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///骑乘姿态
	///	描述骑在此载具上的骑士，应当适应何种姿态
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "RidePosture")
		RIDE_POSTURE_ENUM RidePosture;
	///载具模型（@DT_ModelCfg）
	///	应配置Carrier类型的模型表现支持
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "CarrierModelId")
		FString CarrierModelId;
	///骑者模型位置X修正（厘米）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "RiderOffsetX")
		float RiderOffsetX;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FPET_DATA", DisplayName = "备注")
		FString Remarks;
};

/** 选择职业和性别时判断是否存在 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPROFESSION_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///阵营
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "ROFESSION_DATA", DisplayName = "Camp")
		FString Camp;
	///职业
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "ROFESSION_DATA", DisplayName = "Profession")
		FString Profession;
	///性别
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "ROFESSION_DATA", DisplayName = "Gender")
		FString Gender;
	///当前版本是否有此职业
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "ROFESSION_DATA", DisplayName = "IsAvailableInVersion")
		bool IsAvailableInVersion;
};


/** 状态对应的光效 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FEffectState_Effect_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///效果状态
	///支持：
	///	为指定效果状态配置默认光效表现（@CST-3076）
	///注意：
	///	此配置表中，效果状态应该唯一，若有重复则后面的无效
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "EffectState_Effect")
		EFFECT_STATE EffectStateData;
	///光效ID（@DT_EffectCfg，留空代表“没有表现”）
	///支持：
	///	为指定效果状态配置默认光效表现（@CST-3076）
	///注意：
	///	应当配置，持续时间无限的周期表现
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "EffectState_Effect")
		TArray<FString> EffectIDs;
	///备注
	///	无任何功能，仅供策划记录及查看
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "EffectState_Effect", DisplayName = "备注")
		FString Remarks;
};

/** 部件对应名称与枚举结构 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPartItem
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "EquipPosType")
		MODEL_PART_TYPE posType;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PartID")
		FString PartID;

};

/** 胶囊体参数数据结构 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCAPSULE_SHAPE
{
	GENERATED_BODY()
public:
	///胶囊体半高（厘米）
	///支持：
	///	设定模型对应的胶囊体参数：胶囊半高（@CST-4515）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "CapsuleHalfHeight")
		float CapsuleHalfHeight = 100.0f;
	///胶囊体半径（厘米）
	///支持：
	///	设定模型对应的胶囊体参数：胶囊半径（@CST-4515）
	///注意：
	///	应配置“半径≤半高”，否则将表现为“比预期大的球体形状，半高＝半径”
	///	对于PC单位可用的模型，应配置“胶囊半径应＞0”，否则跳跃状态将不正确
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "CapsuleRadius")
		float CapsuleRadius = 34.0f;
	///Mesh组件的位置Z修正（厘米）
	///支持：
	///	调整模型具体表现细节（@CST-4515）
	///		因胶囊体Root点默认位置在胶囊体中心，而一般表现需要模型Root在胶囊下端
	///		所以一般配置是"负一倍的胶囊半高"
	///注意：
	///	胶囊体Root点默认位置在胶囊体中心
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "MeshRelativeLocationZ")
		float MeshRelativeLocationZ = -100.0f;
};

/** 模型结构 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMODEL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:

	///动画蓝图
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "AnimationPath")
		TSoftClassPtr<UAnimInstance> AnimationPath;

	///动作表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "ActionConfigPath")
		TSoftObjectPtr<UDataTable> ActionConfigPath;

	///部件列表（@DT_ModelPartCfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "PartArray")
		TArray<FPartItem> PartArray;

	///光效列表（@DT_EffectCfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "EffectId")
		TArray<FString> EffectIdArray;

	///胶囊体形状数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "CapsuleShapeData")
		FCAPSULE_SHAPE CapsuleShapeData;

	///是否强制自定义渲染深度（@CST-8276）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "IsRenderCustomDepth")
		bool IsRenderCustomDepth = false;

	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ModelData", DisplayName = "备注")
		FString Remarks;

	///赋值构造
	FMODEL_DATA& operator=(const FMODEL_DATA& src)
	{
		this->AnimationPath = src.AnimationPath;
		this->ActionConfigPath = src.ActionConfigPath;
		for (FPartItem item : src.PartArray)
		{
			FPartItem temp;
			temp.PartID = item.PartID;
			temp.posType = item.posType;
			this->PartArray.Add(temp);
		}

		for (FString effectID : src.EffectIdArray)
		{
			this->EffectIdArray.Add(effectID);
		}
		this->CapsuleShapeData = src.CapsuleShapeData;
		this->Remarks = src.Remarks;
		this->RowName = src.RowName;
		return *this;
	}
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (ActionConfigPath.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(ActionConfigPath.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ActionConfigPath\" resource does not exist"));
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/** 骑士模型动作数据 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FRIDER_MODEL_ANIM_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///骑乘姿态
	///	通过职业、性别、姿态，选择对应的模型表现
	///	骑乘姿态一般由载具决定
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		RIDE_POSTURE_ENUM RidePosture;
	///骑士职业
	///	通过职业、性别、姿态，选择对应的模型表现
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		ROLE_PROFESSION_ENUM RiderProfession;
	///骑士性别
	///	通过职业、性别、姿态，选择对应的模型表现
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		ROLE_GENDER_ENUM RiderGender;
	///骑士动画蓝图
	///	被选择的模型表现
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		TSoftClassPtr<UAnimInstance> AnimationPath;
	///骑士姿态动作表
	///	被选择的模型表现
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		TSoftObjectPtr<UDataTable> ActionConfigPath;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CharacterData", DisplayName = "备注")
		FString Remarks;

public:
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) {
		bool AnimationPathResult = this->AnimationPath.IsNull() ? true : FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->AnimationPath.ToString());
		bool ActionConfigPathResult = this->ActionConfigPath.IsNull() ? true : FCSV_TABLE_ROW_BASE::CheckResourceFileIsExist(this->ActionConfigPath.ToString());
		bool IsError = !AnimationPathResult || !ActionConfigPathResult;
		if (IsError)
		{
			ResultInfo.Result = Error;
		}
		else {
			ResultInfo.Result = Ok;
		}
		if (!AnimationPathResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("%s is Error, "), *this->AnimationPath.ToString());
		}
		if (!ActionConfigPathResult) {
			ResultInfo.CheckLog += FString::Printf(TEXT("%s is Error, "), *this->ActionConfigPath.ToString());
		}
		if (IsError) {
			ResultInfo.CheckLog += TEXT("\n");
		}
	}

	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

/** 动作暂停数据 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FACTION_PAUSE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///动作数据
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		bool IsOpen;
	///动作数据
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		FACTION_DATA ActionData;
	///总秒数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		float TotalSecondsTime;
	///当前秒数
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		float CurSecondsTime;
};

/** 创建外观模型的数据 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCREATE_APPEARANCE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///角色模型ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		FString RoleModelId;
	///骑宠模型ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		FString RidePetModelId;
	///主模型职业
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 RoleProfession;
	///主模型性别
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 RoleGender;
	///主模型阵营
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		int32 RoleCamp;
	///载具姿势[决定骑士在马上的姿势]
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CharacterData")
		RIDE_POSTURE_ENUM RidePosture = RIDE_POSTURE_ENUM::RIDE_POSTURE_NULL;
};