// Fill out your copyright notice in the Description page of Project Settings.

#include "CanvasRenderSeparateTriangles.h"
#include <vector>
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/Area.h"
using namespace std;

struct Vector2
{
	float x;
	float y;
	Vector2(){}
	Vector2(float fx, float fy)
	{
		x = fx;
		y = fy;
	}
};

Vector2 operator-(const Vector2& i, const Vector2& i2)
{
	return Vector2{ i.x - i2.x, i.y - i2.y };
}

//计算叉乘
float multiplicationCross(const Vector2& v2, const Vector2& v) { return v2.x*v.y - v2.y*v.x; }

//看两条直线是否相交（大概
bool isLineCross(const Vector2& v1s, const Vector2& v1e, const Vector2& v2s, const Vector2& v2e) {
	if (
		multiplicationCross((v1s - v2s), (v1e - v2s))* multiplicationCross((v1s - v2e), (v1e - v2e)) <= 0.0 &&
		multiplicationCross((v2s - v1s), (v2e - v1s))* multiplicationCross((v2s - v1e), (v2e - v1e)) <= 0.0
		)  return true;
	return false;
}



struct dataPoint {
	size_t backPoint;
	size_t Point;
	size_t frontPoint;
	float swing;
	dataPoint() :backPoint(0), Point(0), frontPoint(0), swing(0.0f) {}
	dataPoint(const std::vector<Vector2>& data, size_t back, size_t poi, size_t front) :backPoint(back), Point(poi), frontPoint(front) {
		calculateSwing(data);
	}
	dataPoint(const dataPoint& dp) :backPoint(dp.backPoint), Point(dp.Point), frontPoint(dp.frontPoint), swing(dp.swing) {}

	//计算凹凸点
	void calculateSwing(const std::vector<Vector2>& data) {
		swing = multiplicationCross((data[Point] - data[backPoint]), (data[frontPoint] - data[Point]));
	}
	void reverse() { std::swap(backPoint, frontPoint); swing = -swing; }

	bool isInAreaB(const std::vector<Vector2>& data, size_t index) const { //只有在该点为凹点时才正确
		Vector2 t1(data[Point] - data[backPoint]);
		Vector2 t2(data[index] - data[Point]);
		Vector2 t3(data[Point] - data[frontPoint]);
		return multiplicationCross(t1, t2) >= 0.0 && multiplicationCross(t2, t3) >= 0.0;
	}

	bool isInAreaA(const std::vector<Vector2>& data, size_t index) const { //只有在该点为凹点时才正确
		Vector2 t1(data[backPoint] - data[Point]);
		Vector2 t2(data[index] - data[Point]);
		Vector2 t3(data[Point] - data[frontPoint]);
		return multiplicationCross(t3, t2) >= 0.0 && multiplicationCross(t2, t1) >= 0.0;
	}

	bool isInAreaC(const std::vector<Vector2>& data, size_t index) const { //只有在该点为凹点时才正确
		Vector2 t1(data[Point] - data[backPoint]);
		Vector2 t2(data[index] - data[Point]);
		Vector2 t3(data[frontPoint] - data[Point]);
		return multiplicationCross(t3, t2) >= 0.0 && multiplicationCross(t2, t1) >= 0.0;
	}
};

//三角形拆分
void speratePolygon(const std::vector<Vector2>& data, const std::vector<dataPoint>& input, size_t po1, size_t po2, std::vector<dataPoint>& op1, std::vector<dataPoint>& op2) {
	if (input.size() < 4) return;
	if (po1 == po2) {
		op1.insert(op1.end(), input.begin(), input.end());
		return;
	}
	else if (po1 > po2) {
		size_t tem = po1;
		po1 = po2;
		po2 = tem;
	}
	dataPoint dp(*(input.begin() + po1));
	dataPoint dp2(*(input.begin() + po2));
	dp.frontPoint = dp2.Point;
	dp.calculateSwing(data);
	dp2.backPoint = dp.Point;
	dp2.calculateSwing(data);
	op1.insert(op1.end(), input.begin(), input.begin() + po1);
	op1.push_back(dp);
	op1.push_back(dp2);
	op1.insert(op1.end(), input.begin() + po2 + 1, input.end());

	dataPoint dp22(*(input.begin() + po1));
	dataPoint dp222(*(input.begin() + po2));
	dp22.backPoint = dp222.Point;
	dp22.calculateSwing(data);
	dp222.frontPoint = dp22.Point;
	dp222.calculateSwing(data);

	op2.push_back(dp22);
	op2.insert(op2.end(), input.begin() + po1 + 1, input.begin() + po2);
	op2.push_back(dp222);
}


bool adjectPointData(const std::vector<Vector2>& data, std::vector<dataPoint>& dp) {
	size_t size = data.size();
	dp.push_back(dataPoint(data, size - 1, 0, 1));
	for (size_t i = 1; i + 1 < size; ++i) {
		dp.push_back(dataPoint(data, i - 1, i, i + 1));
	}
	dp.push_back(dataPoint(data, size - 2, size - 1, 0));

	size_t minx = 0;
	for (size_t i = 1; i < dp.size(); ++i) {
		if (data[dp[i].Point].x < data[dp[minx].Point].x)
			minx = i;
	}

	if (dp[minx].swing < 0.0f) {
		std::reverse(dp.begin(), dp.end());
		for (size_t i = 0; i < dp.size(); ++i) {
			dp[i].reverse();
		}
	}
	return true;
}

//挑选看两个点是否能连线
bool isTwoPointAbleToConnect(const std::vector<Vector2>& data, const std::vector<dataPoint>& dt, size_t c, size_t e) {
	if (dt[c].isInAreaB(data, dt[e].Point)) {
		for (size_t k = 0; k < dt.size(); ++k) {
			const dataPoint& t1 = dt[k];
			const dataPoint& t2 = dt[c];
			const dataPoint& t3 = dt[e];
			if (
				t1.Point == t2.Point ||
				t1.Point == t3.Point ||
				t1.backPoint == t2.Point ||
				t1.backPoint == t3.Point
				) continue;
			if (isLineCross(data[dt[c].Point], data[dt[e].Point], data[dt[k].Point], data[dt[k].backPoint]))
				return false;
		}
		return true;
	}
	return false;
}

//拆分三角形
void sperateConvexPolygon(const std::vector<Vector2>& data, const std::vector<dataPoint>& dt, std::vector<size_t>& order) {
	if (dt.size() < 3) return;
	for (size_t i = 0; i < dt.size(); ++i) {
		if (dt[i].swing < 0.0f) {
			size_t first = i;
			for (size_t k = i + 2; k < dt.size(); ++k) {
				if (isTwoPointAbleToConnect(data, dt, i, k)) {
					if (dt[k].swing < 0.0f) {
						std::vector<dataPoint> dapo1, dapo2;
						speratePolygon(data, dt, i, k, dapo1, dapo2);
						sperateConvexPolygon(data, dapo1, order);
						sperateConvexPolygon(data, dapo2, order);
						return;
					}
					else if (first == i) {
						first = k;
					}
				}
			}
			if (first == i && i != 0) {
				for (size_t k = 0; k < i - 1; ++k) {
					if (isTwoPointAbleToConnect(data, dt, i, k)) {
						first = k;
						break;
					}
				}
			}
			if (first != i) {
				std::vector<dataPoint> dapo1, dapo2;
				speratePolygon(data, dt, i, first, dapo1, dapo2);
				sperateConvexPolygon(data, dapo1, order);
				sperateConvexPolygon(data, dapo2, order);
				return;
			}
			else {
				for (size_t k = 0; k < dt.size(); ++k) {
					if (dt[k].Point == dt[i].Point ||
						dt[k].frontPoint == dt[i].Point) continue;
					if (dt[i].isInAreaA(data, dt[k].Point)) {
						bool isCross = false;
						for (size_t p = 0; p < dt.size(); ++p) {
							if (p == k) continue;
							const dataPoint& t1(dt[p]);
							const dataPoint& t2(dt[k]);
							const dataPoint& t3(dt[i]);
							if (
								t1.Point != t2.Point &&
								t1.Point != t3.Point &&
								t1.frontPoint != t2.Point &&
								t1.frontPoint != t3.Point &&
								isLineCross(data[t1.Point], data[t1.frontPoint], data[t2.Point], data[t3.Point])
								) {
								isCross = true;
								break;
							}
						}
						if (!isCross) {
							std::vector<dataPoint> datap1, datap2;
							speratePolygon(data, dt, i, k, datap1, datap2);
							sperateConvexPolygon(data, datap1, order);
							sperateConvexPolygon(data, datap2, order);
							return;
						}
					}
				}
			}
			return;
		}
	}
	for (size_t i = 1; i + 1 < dt.size(); ++i) {
		order.push_back(dt[0].Point);
		order.push_back(dt[i].Point);
		order.push_back(dt[i + 1].Point);
	}
}

//缩放至[0, 1.0]
bool adjectVector2InOneTexture(Vector2& shift, Vector2& scale, std::vector<Vector2>& p) 
{
	if (p.size() < 3) return false;
	Vector2 RX{ p[0].x, p[0].x };
	Vector2 RY{ p[0].y, p[0].y };
	for (size_t i = 0; i < p.size(); ++i) {
		float X = p[i].x, Y = p[i].y;
		if (X > RX.x) RX.x = X; if (X < RX.y) RX.y = X;
		if (Y > RY.x) RY.x = Y; if (Y < RY.y) RY.y = Y;
	}
	scale = Vector2{ (RX.x - RX.y) / 0.9f, (RY.x - RY.y) / 0.9f };
	shift = Vector2{ RX.y - scale.x * 0.05f, RY.x + scale.y * 0.05f };

	for (size_t i = 0; i < p.size(); ++i) {
		p[i].x = (p[i].x - shift.x) / scale.x;
		p[i].y = (shift.y - p[i].y) / scale.y;
	}
	return true;
}

// 按照世界地图的比例将顶点数据归一化
bool CoordinateWorldToTexture(FVector2D LevelSize, FVector2D LevelOrign, std::vector<Vector2>& p)
{
	for (size_t i = 0; i < p.size(); ++i) 
	{
		p[i].x = (p[i].x - LevelOrign.X) / LevelSize.X;
		p[i].y = (p[i].y - LevelOrign.Y) / LevelSize.Y;
	}
	return true;
}


struct planeData {
	string area;
	string areaname;
	string data;
};

std::vector<planeData> pd;
//////////////////////////////////////////////////////////////////////////

UCanvasRenderSeparateTriangles::UCanvasRenderSeparateTriangles(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)		    
{
}


TArray<FCanvasUVTri> UCanvasRenderSeparateTriangles::TableDataToSeparateTriangles(FVector2D LevelSize, FVector2D LevelOrign, FVector2D MiniMapSize, const TArray<FVector2D>& VertexData, FLinearColor Color)
{
	TArray<FCanvasUVTri> Triangles;
	Triangles.Empty();
	if (VertexData.Num() <= 2)
		return Triangles;

	vector<Vector2> MyVertexData;
	for (int i = 0; i < VertexData.Num(); i++)
	{
		MyVertexData.push_back(Vector2(VertexData[i].X, VertexData[i].Y));
	}

	std::vector<size_t> TrianglesVertex;
	std::vector<dataPoint> dp;
	adjectPointData(MyVertexData, dp); //将顶点数据先计算凹凸点，并转换成逆时针还是顺时针来着。
	sperateConvexPolygon(MyVertexData, dp, TrianglesVertex); //三角化

	CoordinateWorldToTexture(LevelSize, LevelOrign, MyVertexData); //将坐标归一化
	 

	if (TrianglesVertex.size() >= 3)
	{
		for (int i = 0; i < TrianglesVertex.size(); )
		{
			if (i > TrianglesVertex.size() - 2)
				break;

			FCanvasUVTri Tri;
			Tri.V0_Pos.X = MyVertexData[TrianglesVertex[i]].x * MiniMapSize.X;
			Tri.V0_Pos.Y = MyVertexData[TrianglesVertex[i++]].y * MiniMapSize.Y;
			Tri.V1_Pos.X = MyVertexData[TrianglesVertex[i]].x * MiniMapSize.X;
			Tri.V1_Pos.Y = MyVertexData[TrianglesVertex[i++]].y * MiniMapSize.Y;
			Tri.V2_Pos.X = MyVertexData[TrianglesVertex[i]].x * MiniMapSize.X;
			Tri.V2_Pos.Y = MyVertexData[TrianglesVertex[i++]].y * MiniMapSize.Y;
			Tri.V0_Color = Color;
			Tri.V1_Color = Color;
			Tri.V2_Color = Color;
			Triangles.Add(Tri);
		}
	}
	return Triangles;
}

FPolygonData UCanvasRenderSeparateTriangles::ReadTableDataTest(const FString& RowName)
{
	FPolygonData Polygon;
	Polygon.clear();
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AREA_DATA);
	if (ConfigTable)
	{
		const FAREA_DATA* AreaRow = (FAREA_DATA*)ConfigTable->GetRow(RowName);
		if (AreaRow)
		{
			Polygon.MapScriptID = AreaRow->MapScriptID;
			Polygon.Vertex.Append(AreaRow->Polygon);
		}
	}
	return Polygon;
}
