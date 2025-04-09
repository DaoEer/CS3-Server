#pragma once
#include "SlateBasics.h"

/*
* 文件名称：CS3Styles.h
* 功能说明：
* 文件作者：huangshanquan
* 目前维护：huangshanquan
* 创建时间：2017-12-05
*/

/** 
 * 初始化创世画刷样式资源并且注册和注销资源
 */
class FCS3Styles
{
public:
	/**
	* 初始化和注册组件.
	**/
	static void Initialize();
	/**
	* 注销类型设置CS3StyleInstance未空指针.
	**/
	static void Shutdown();
	/**
	*  获取Slate Style 指针.
	**/
	static const class ISlateStyle& Get();
	/**
	* 获取Style Set名称.
	**/
	static FName GetStyleSetName();

private:
	/**
	* 创建Style Set实例.
	**/
	static TSharedRef<class FSlateStyleSet> Create(); 

	/**
	* 单间实例
	**/
	static TSharedPtr<class FSlateStyleSet> CS3StyleInstance;
};

