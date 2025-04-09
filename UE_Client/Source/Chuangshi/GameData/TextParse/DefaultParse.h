#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "Internationalization/Regex.h"

/**
* 文件名称：DefaultParse.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-09-18
*/

struct StructSpecialFormatText
{
	FString SpecialFormatText;
	FString UnformattedText;
};

struct StructColor
{
	uint8 R;
	uint8 G;
	uint8 B;
	uint8 A;
};

/**
*默认的属性解释器，能够解释的规范如下：
*1、该解释器解释以大括号（{）括回来的属性串
*2、属性键与值得关系通过等号来表达
*3、多个属性之间以英文符号分隔
*4、如果属性值带有分号，需要以单引号将串括起来
*如："{ aa = 1222; bb = AADFASDF; cc = 'aasdfasdf'; dd = 23,23,5; ee = ( 3, 4, 5 ) }"
*/
class DefaultParse
{
public:
	DefaultParse();
	~DefaultParse();
	struct StructSpecialFormatText GetFormatText(FString Text);
	struct StructSpecialFormatText GetSpeicalFormatText(FString Text);
	void GetAttrInfos(FString AttrsText, TMap<FString, FString>& AttrInfos, TMap<FString,FString>& KeyReplacementInfos);
	int TransInt(FString StrInt);
	float TransFloat(FString StrFloat);
	FString TransColor(FString StrColor);

private:
	FRegexPattern ScopePattern;///<  \{.*[^\\]\},匹配大括号，其中}前一个字符不能是'\'
	//FRegexPattern SplitPattern;///<	\w+\s*=\s*[^'].*?(?=;)|\w+\s*=\s*'.*?'|\w+\s*=\s*[^'].*|\w+\s*=\s*'.* 匹配几种 xxx = yyy 类型，包括 xxx=yyy xxx='yyy'
	FRegexPattern IntPattern;///<	^[\+\-]{0,1}\d+$	整数匹配包括负整数
	FRegexPattern FloatPattern;///<	^([\+\-]{0,1}\d*)(\.\d*)?$	浮点数匹配模式（包括负数）
	FRegexPattern ColorPattern;///< ^\(((?:\s*?\d+\s*?,){2,3})\s*?\d+\s*?\)$|^\s*?c\d{1,3}\s*$ 颜色格式：c1~c999或者(255,255,255)或者(255,255,255,255)
};