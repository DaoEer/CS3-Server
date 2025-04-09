// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Core.h"

/*
* 文件名称：AutoTestDebug.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/


//DECLARE_LOG_CATEGORY_EXTERN(KBELog, Log, All);
DEFINE_LOG_CATEGORY_STATIC(AutoTest, Log, All);

//FDateTime::UtcNow().ToString(TEXT("[%Y-%m-%d %H:%M:%S %N]")));

// see also: Engine\Source\Runtime\Core\Public\Logging\LogVerbosity.h
#define AT_DEBUG(msg, ...)   UE_LOG(AutoTest, Log, msg, __VA_ARGS__);
#define AT_INFO(msg, ...)    UE_LOG(AutoTest, Display, msg, __VA_ARGS__);
#define AT_WARNING(msg, ...) UE_LOG(AutoTest, Warning, msg, __VA_ARGS__);
#define AT_ERROR(msg, ...)   UE_LOG(AutoTest, Error, msg, __VA_ARGS__);
#define AT_FATAL(msg, ...)   UE_LOG(AutoTest, Fatal, msg, __VA_ARGS__);
#define AT_DISPLAY(msg, ...) UE_LOG(AutoTest, Display, msg, __VA_ARGS__);
#define AT_VERBOSE(msg, ...) UE_LOG(AutoTest, Verbose, msg, __VA_ARGS__);