import win32com.client.dynamic				# Module for COM-Client
import sys, os  					# Module for File-Handling
import win32gui						# Module for MessageBox
import numpy as np 					# Module for numerical computing

CATIA = win32com.client.Dispatch("CATIA.Application")	# Binding python session into CATIA
documents1 = CATIA.Documents				# CATIA object for managing documents
partDocument1 = documents1.Add("Part")			# Starting new part
part1 = partDocument1.Part				# part1 
ShFactory = part1.HybridShapeFactory			# Shape factory provides generating of shapes
bodies1 = part1.HybridBodies				# Starting new body (geometrical set) in part1
body1 = bodies1.Add()					# Adding new body to part1
body1.Name="Airfoil"					# Naming new body as "wireframe"

body2 = bodies1.Add()					# Adding new body in part1
body2.Name="Surfaces"					# Naming new body as "Surfaces"

body3 = bodies1.Add()					# Adding new body in part1
body3.Name="Skeleton"					# Naming new body as "Skeleton"

fp1=open("geomExtract.dat",'r')
a=[]
a=fp1.readline().split()
k=int(a[0])
l=int(a[2])

Guide1 = ShFactory.AddNewSpline()
Guide1.SetSplineType(0)
Guide1.SetClosing(0)
Guide2 = ShFactory.AddNewSpline()
Guide2.SetSplineType(0)
Guide2.SetClosing(0)
Guide3 = ShFactory.AddNewSpline()
Guide3.SetSplineType(0)
Guide3.SetClosing(0)
Guide4 = ShFactory.AddNewSpline()
Guide4.SetSplineType(0)
Guide4.SetClosing(0)

kk=0
ll=int(k/2)+1
#print ll
for i in range (0,l):
    st="spline"+str(kk)+"Up = ShFactory.AddNewSpline()"
    exec st
    st="spline"+str(kk)+"Up.SetSplineType(0)"
    exec st
    exec st
    st="spline"+str(kk)+"Up.SetClosing(0)"
    exec st
    for j in range (0,ll):
        a=fp1.readline().split()
        x=a[0]
        y=a[1]
        z=a[2]
        if j==0:
            x0=x
            y0=y
            z0=z
        if j==ll-1:
            x1=x
            y1=y
            z1=z
        point=ShFactory.AddNewPointCoord(x,y,z)
        st="spline"+str(kk)+"Up.AddPoint(point)"
        exec st
    st="ShFactory.GSMVisibility(spline"+str(kk)+"Up,0)"
    exec st
    st="body1.AppendHybridShape(spline"+str(kk)+"Up)"
    exec st
    part1.Update()
    st="spline"+str(kk)+"Down = ShFactory.AddNewSpline()"
    exec st
    st="spline"+str(kk)+"Down.SetSplineType(0)"
    exec st
    exec st
    st="spline"+str(kk)+"Down.SetClosing(0)"
    exec st
    point=ShFactory.AddNewPointCoord(x1,y1,z1)
    st="spline"+str(kk)+"Down.AddPoint(point)"
    exec st
    if (i>=0 and i<l-1):
        Guide2.AddPoint(point)
        point1=ShFactory.AddNewPointCoord(x0,y0,z0)
        Guide1.AddPoint(point1)
    if (i>=l-2 and i<l):
        Guide4.AddPoint(point)
        point1=ShFactory.AddNewPointCoord(x0,y0,z0)
        Guide3.AddPoint(point1)
    if (i==31):
        pt1=ShFactory.AddNewPointCoord(x0,y0,z0)
        body3.AppendHybridShape(pt1)
        ShFactory.GSMVisibility(pt1,0)
        yp1=y0
    elif (i==67):
        pt2=ShFactory.AddNewPointCoord(x0,y0,z0)
        body3.AppendHybridShape(pt2)
        ShFactory.GSMVisibility(pt2,0)
        yp2=y0
    elif (i==29):
        pt3=ShFactory.AddNewPointCoord(x0,y0,z0)
        body3.AppendHybridShape(pt3)
        ShFactory.GSMVisibility(pt3,0)
        yp3=y0
    elif (i==0):
        pt4=ShFactory.AddNewPointCoord(x0,y0,z0)
        body3.AppendHybridShape(pt4)
        ShFactory.GSMVisibility(pt4,0)
        yp4=y0
    for j in range (ll,k):
        a=fp1.readline().split()
        x=a[0]
        y=a[1]
        z=a[2]
        point=ShFactory.AddNewPointCoord(x,y,z)
        st="spline"+str(kk)+"Down.AddPoint(point)"
        exec st
    st="ShFactory.GSMVisibility(spline"+str(kk)+"Down,0)"
    exec st
    st="body1.AppendHybridShape(spline"+str(kk)+"Down)"
    exec st
    kk+=1
    st="spline"+str(i)+"Up.Name=\"Spline"+str(i)+"Down\""
    exec st
    st="spline"+str(i)+"Down.Name=\"Spline"+str(i)+"Up\""
    exec st
body1.AppendHybridShape(Guide1)
ShFactory.GSMVisibility(Guide1,0)
Guide1.Name="Guide1"
body1.AppendHybridShape(Guide2)
ShFactory.GSMVisibility(Guide2,0)
Guide2.Name="Guide2"
body1.AppendHybridShape(Guide3)
ShFactory.GSMVisibility(Guide3,0)
Guide3.Name="Guide3"
body1.AppendHybridShape(Guide4)
ShFactory.GSMVisibility(Guide4,0)
Guide4.Name="Guide4"
part1.Update()

loftup = ShFactory.AddNewLoft()
loftup.SectionCoupling = 1
loftup.Relimitation = 1
loftup.CanonicalDetection = 2
#Add Guide to the loft
reference1 = part1.CreateReferenceFromObject(Guide1)
loftup.AddGuide(reference1)
reference1 = part1.CreateReferenceFromObject(Guide2)
loftup.AddGuide(reference1)

loftdown = ShFactory.AddNewLoft()
loftdown.SectionCoupling = 1
loftdown.Relimitation = 1
loftdown.CanonicalDetection = 2
#Add Guide to the loft
reference1 = part1.CreateReferenceFromObject(Guide1)
loftdown.AddGuide(reference1)
reference1 = part1.CreateReferenceFromObject(Guide2)
loftdown.AddGuide(reference1)
for i in range (0,l-1):
    sti="spline"+str(i)+"Up"
    st="ref1 = part1.CreateReferenceFromObject("+sti+")"
    exec st
    ref2 = None
    loftup.AddSectionToLoft(ref1, 1, ref2)
    sti="spline"+str(i)+"Down"
    st="ref1 = part1.CreateReferenceFromObject("+sti+")"
    exec st
    ref2 = None
    loftdown.AddSectionToLoft(ref1, 1, ref2)
#Adding loft to Surfaces geometrical set
body2.AppendHybridShape(loftup)
body2.AppendHybridShape(loftdown)
part1.Update()
loftup.Name="MainDown"
loftdown.Name="MainUp"

loftup1 = ShFactory.AddNewLoft()
loftup1.SectionCoupling = 1
loftup1.Relimitation = 1
loftup1.CanonicalDetection = 2
#Add Guide to the loft
reference1 = part1.CreateReferenceFromObject(Guide3)
loftup1.AddGuide(reference1)
reference1 = part1.CreateReferenceFromObject(Guide4)
loftup1.AddGuide(reference1)

loftdown1 = ShFactory.AddNewLoft()
loftdown1.SectionCoupling = 1
loftdown1.Relimitation = 1
loftdown1.CanonicalDetection = 2
#Add Guide to the loft
reference1 = part1.CreateReferenceFromObject(Guide3)
loftdown1.AddGuide(reference1)
reference1 = part1.CreateReferenceFromObject(Guide4)
loftdown1.AddGuide(reference1)
for i in range (l-2,l):
    sti="spline"+str(i)+'Up'
    st="ref1 = part1.CreateReferenceFromObject("+sti+")"
    exec st
    ref2 = None
    loftup1.AddSectionToLoft(ref1, 1, ref2)
    sti="spline"+str(i)+"Down"
    st="ref1 = part1.CreateReferenceFromObject("+sti+")"
    exec st
    ref2 = None
    loftdown1.AddSectionToLoft(ref1, 1, ref2)
body2.AppendHybridShape(loftup1)
body2.AppendHybridShape(loftdown1)
part1.Update()
loftup1.Name="TipUp"
loftdown1.Name="TipDown"


#Creating the Ribs and spars. First lets create the intersecting planes.
Direction2 = ShFactory.AddNewDirectionByCoord(0.000000, 0.000000, 1.000000)
Direction3 = ShFactory.AddNewDirectionByCoord(0.000000, 1.000000, 0.000000)
originElements1 = part1.OriginElements
PlaneExplicit1 = originElements1.PlaneZX
#reference1 = part1.CreateReferenceFromObject(PlaneExplicit1)
Shapes1 = body2.HybridShapes
#LineExplicit1 = Shapes1.Item("Z Axis")
#reference2 = part1.CreateReferenceFromObject(LineExplicit1)

reference1 = part1.CreateReferenceFromObject(pt1)
LinePtDir101 = ShFactory.AddNewLinePtDir(reference1, Direction2, 0.000000, 200.000000, False)
body3.AppendHybridShape(LinePtDir101)
part1.InWorkObject = LinePtDir101
part1.Update()
reference1 = part1.CreateReferenceFromObject(pt1)
PointCoord2 = ShFactory.AddNewPointCoord(-500.000000, 0.000000, 0.000000)
PointCoord2.PtRef = reference1
body3.AppendHybridShape(PointCoord2)
part1.InWorkObject = PointCoord2
part1.Update()
reference2 = part1.CreateReferenceFromObject(PointCoord2)
LinePtPt101 = ShFactory.AddNewLinePtPt(reference1, reference2)
Rotate1 = ShFactory.AddNewEmptyRotate()
reference1 = part1.CreateReferenceFromObject(LinePtPt101)
Rotate1.ElemToRotate = reference1
Rotate1.VolumeResult = False
Rotate1.RotationType = 0
reference2 = part1.CreateReferenceFromObject(LinePtDir101)
Rotate1.Axis = reference2
Rotate1.AngleValue = -19.226000
body3.AppendHybridShape(Rotate1)
part1.InWorkObject = Rotate1
part1.Update()
Translate1 = ShFactory.AddNewEmptyTranslate()
reference1 = part1.CreateReferenceFromObject(Rotate1)
Translate1.ElemToTranslate = reference1
Translate1.VectorType = 0
Translate1.Direction = Direction2
Translate1.DistanceValue = 475.000000
Translate1.VolumeResult = False
body3.AppendHybridShape(Translate1)
part1.InWorkObject = Translate1
part1.Update()
reference2 = part1.CreateReferenceFromObject(Translate1)
Plane2Lines1 = ShFactory.AddNewPlane2Lines(reference1, reference2)
body3.AppendHybridShape(Plane2Lines1)
part1.InWorkObject = Plane2Lines1
part1.Update()

reference1 = part1.CreateReferenceFromObject(pt2)
LinePtDir102 = ShFactory.AddNewLinePtDir(reference1, Direction2, 0.000000, 200.000000, False)
body3.AppendHybridShape(LinePtDir102)
part1.InWorkObject = LinePtDir102
part1.Update()
reference1 = part1.CreateReferenceFromObject(pt2)
PointCoord3 = ShFactory.AddNewPointCoord(-500.000000, 0.000000, 0.000000)
PointCoord3.PtRef = reference1
body3.AppendHybridShape(PointCoord3)
part1.InWorkObject = PointCoord3
part1.Update()
reference2 = part1.CreateReferenceFromObject(PointCoord3)
LinePtPt102 = ShFactory.AddNewLinePtPt(reference1, reference2)
Rotate2 = ShFactory.AddNewEmptyRotate()
reference1 = part1.CreateReferenceFromObject(LinePtPt102)
Rotate2.ElemToRotate = reference1
Rotate2.VolumeResult = False
Rotate2.RotationType = 0
reference2 = part1.CreateReferenceFromObject(LinePtDir102)
Rotate2.Axis = reference2
Rotate2.AngleValue = -19.226000
body3.AppendHybridShape(Rotate2)
part1.InWorkObject = Rotate2
part1.Update()
Translate2 = ShFactory.AddNewEmptyTranslate()
reference1 = part1.CreateReferenceFromObject(Rotate2)
Translate2.ElemToTranslate = reference1
Translate2.VectorType = 0
Translate2.Direction = Direction2
Translate2.DistanceValue = 475.000000
Translate2.VolumeResult = False
body3.AppendHybridShape(Translate2)
part1.InWorkObject = Translate2
part1.Update()
reference2 = part1.CreateReferenceFromObject(Translate2)
Plane2Lines2 = ShFactory.AddNewPlane2Lines(reference1, reference2)
body3.AppendHybridShape(Plane2Lines2)
part1.InWorkObject = Plane2Lines2
part1.Update()

reference1 = part1.CreateReferenceFromObject(pt3)
PointCoord4 = ShFactory.AddNewPointCoord(-500.000000, 0.000000, 0.000000)
PointCoord4.PtRef = reference1
body3.AppendHybridShape(PointCoord4)
part1.InWorkObject = PointCoord4
part1.Update()
reference2 = part1.CreateReferenceFromObject(PointCoord4)
LinePtPt111 = ShFactory.AddNewLinePtPt(reference1, reference2)
Translate3 = ShFactory.AddNewEmptyTranslate()
reference1 = part1.CreateReferenceFromObject(LinePtPt111)
Translate3.ElemToTranslate = reference1
Translate3.VectorType = 0
Translate3.Direction = Direction2
Translate3.DistanceValue = 475.000000
Translate3.VolumeResult = False
body3.AppendHybridShape(Translate3)
part1.InWorkObject = Translate3
part1.Update()
reference2 = part1.CreateReferenceFromObject(Translate3)
Plane2Lines3 = ShFactory.AddNewPlane2Lines(reference1, reference2)
body3.AppendHybridShape(Plane2Lines3)
part1.InWorkObject = Plane2Lines3
part1.Update()

ShFactory.GSMVisibility(LinePtDir102,0)
ShFactory.GSMVisibility(LinePtDir101,0)
ShFactory.GSMVisibility(Translate3,0)
ShFactory.GSMVisibility(Translate2,0)
ShFactory.GSMVisibility(Translate1,0)
ShFactory.GSMVisibility(Rotate2,0)
ShFactory.GSMVisibility(Rotate1,0)
ShFactory.GSMVisibility(PointCoord2,0)
ShFactory.GSMVisibility(PointCoord3,0)
ShFactory.GSMVisibility(PointCoord4,0)
ShFactory.GSMVisibility(LinePtPt102,0)
ShFactory.GSMVisibility(LinePtPt101,0)
ShFactory.GSMVisibility(LinePtPt111,0)
ShFactory.GSMVisibility(Plane2Lines3,0)
ShFactory.GSMVisibility(Plane2Lines2,0)
ShFactory.GSMVisibility(Plane2Lines1,0)

#Planes created. Now lets create the ribs.
#Creating Rib 1
reference1 = part1.CreateReferenceFromObject(loftup)
reference2 = part1.CreateReferenceFromObject(Plane2Lines1)
Intersection1 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection1.PointType = 0
body3.AppendHybridShape(Intersection1)
part1.InWorkObject = Intersection1
part1.Update ()
reference1 = part1.CreateReferenceFromObject(loftdown)
reference2 = part1.CreateReferenceFromObject(Plane2Lines1)
Intersection2 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection2.PointType = 0
body3.AppendHybridShape(Intersection2)
part1.InWorkObject = Intersection2
part1.Update()
Fill2 = ShFactory.AddNewFill()
reference1 = part1.CreateReferenceFromObject(Intersection1)
Fill2.AddBound(reference1)
reference2 = part1.CreateReferenceFromObject(Intersection2)
Fill2.AddBound(reference2)
Fill2.Continuity = 0
body3.AppendHybridShape(Fill2)
part1.InWorkObject = Fill2
part1.Update()
Fill2.Name="Rib1"
ShFactory.GSMVisibility(Intersection1,0)
ShFactory.GSMVisibility(Intersection2,0)

#Creating Rib 2
reference1 = part1.CreateReferenceFromObject(loftup)
reference2 = part1.CreateReferenceFromObject(Plane2Lines2)
Intersection3 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection3.PointType = 0
body3.AppendHybridShape(Intersection3)
part1.InWorkObject = Intersection3
part1.Update ()
reference1 = part1.CreateReferenceFromObject(loftdown)
reference2 = part1.CreateReferenceFromObject(Plane2Lines2)
Intersection4 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection4.PointType = 0
body3.AppendHybridShape(Intersection4)
part1.InWorkObject = Intersection4
part1.Update()
Fill1 = ShFactory.AddNewFill()
reference1 = part1.CreateReferenceFromObject(Intersection4)
Fill1.AddBound(reference1)
reference2 = part1.CreateReferenceFromObject(Intersection3)
Fill1.AddBound(reference2)
Fill1.Continuity = 0
body3.AppendHybridShape(Fill1)
part1.InWorkObject = Fill1
part1.Update()
Fill1.Name="Rib2"
ShFactory.GSMVisibility(Intersection3,0)
ShFactory.GSMVisibility(Intersection4,0)

#Creating line parallel to TE
'''reference1 = part1.CreateReferenceFromObject(Intersection1)
PointOnCurve1 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.000000, False)
body3.AppendHybridShape(PointOnCurve1)
part1.InWorkObject = PointOnCurve1
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection3)
PointOnCurve2 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.000000, False)
body3.AppendHybridShape(PointOnCurve2)
part1.InWorkObject = PointOnCurve2
part1.Update()
reference1 = part1.CreateReferenceFromObject(PointOnCurve2)
reference2 = part1.CreateReferenceFromObject(PointOnCurve1)'''
reference1 = part1.CreateReferenceFromObject(pt1)
reference2 = part1.CreateReferenceFromObject(pt2)
LinePtPt1 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt1)
part1.InWorkObject = LinePtPt1
part1.Update()
#ShFactory.GSMVisibility(PointOnCurve1,0)
#ShFactory.GSMVisibility(PointOnCurve2,0)

#Creating Rib 3
ref1 = part1.CreateReferenceFromObject(Plane2Lines1)
TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
ref2 = part1.CreateReferenceFromObject(Plane2Lines2)
dist = TheMeasurable.GetMinimumDistance(ref2)
x1=-dist/2
PlaneOffset1 = ShFactory.AddNewPlaneOffset(ref1, x1, False)
body3.AppendHybridShape(PlaneOffset1)
part1.Update()
ShFactory.GSMVisibility(PlaneOffset1,0)
reference1 = part1.CreateReferenceFromObject(loftup)
reference2 = part1.CreateReferenceFromObject(PlaneOffset1)
Intersection5 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection5.PointType = 0
body3.AppendHybridShape(Intersection5)
part1.InWorkObject = Intersection5
part1.Update ()
reference1 = part1.CreateReferenceFromObject(loftdown)
reference2 = part1.CreateReferenceFromObject(PlaneOffset1)
Intersection6 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection6.PointType = 0
body3.AppendHybridShape(Intersection6)
part1.InWorkObject = Intersection6
part1.Update()
Fill6 = ShFactory.AddNewFill()
reference1 = part1.CreateReferenceFromObject(Intersection5)
Fill6.AddBound(reference1)
reference2 = part1.CreateReferenceFromObject(Intersection6)
Fill6.AddBound(reference2)
Fill6.Continuity = 0
body3.AppendHybridShape(Fill6)
part1.InWorkObject = Fill6
part1.Update()
Fill6.Name="Rib3"
ShFactory.GSMVisibility(Intersection5,0)
ShFactory.GSMVisibility(Intersection6,0)

#Creating Rib 10
reference1 = part1.CreateReferenceFromObject(loftup)
reference2 = part1.CreateReferenceFromObject(Plane2Lines3)
Intersection110 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection110.PointType = 0
body3.AppendHybridShape(Intersection110)
part1.InWorkObject = Intersection110
part1.Update ()
reference1 = part1.CreateReferenceFromObject(loftdown)
reference2 = part1.CreateReferenceFromObject(Plane2Lines3)
Intersection160 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection160.PointType = 0
body3.AppendHybridShape(Intersection160)
part1.InWorkObject = Intersection160
part1.Update()
Fill110 = ShFactory.AddNewFill()
reference1 = part1.CreateReferenceFromObject(Intersection160)
Fill110.AddBound(reference1)
reference2 = part1.CreateReferenceFromObject(Intersection110)
Fill110.AddBound(reference2)
Fill110.Continuity = 0
body3.AppendHybridShape(Fill110)
part1.InWorkObject = Fill110
part1.Update()
Fill110.Name="Rib10"
ShFactory.GSMVisibility(Intersection110,0)
ShFactory.GSMVisibility(Intersection160,0)

#Creating points for Spar1
reference1 = part1.CreateReferenceFromObject(Intersection5)
PointOnCurve3 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.000000, False)
body3.AppendHybridShape(PointOnCurve3)
part1.InWorkObject = PointOnCurve3
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection5)
PointOnCurve8 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 1.000000, False)
body3.AppendHybridShape(PointOnCurve8)
part1.InWorkObject = PointOnCurve8
part1.Update()
reference1 = part1.CreateReferenceFromObject(PointOnCurve3)
reference2 = part1.CreateReferenceFromObject(PointOnCurve8)
LinePtPt2 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt2)
part1.InWorkObject = LinePtPt2
part1.Update()
reference1 = part1.CreateReferenceFromObject(LinePtPt2)
PointOnCurve9 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.700000, False)
body3.AppendHybridShape(PointOnCurve9)
part1.InWorkObject = PointOnCurve9
part1.Update()
reference2 = part1.CreateReferenceFromObject(PointOnCurve9)
reference1 = part1.CreateReferenceFromObject(LinePtPt1)
Direction1 = ShFactory.AddNewDirection(reference1)
LinePtDir2 = ShFactory.AddNewLinePtDir(reference2, Direction1, (dist/2+1000), -(dist/2+1000), False)
body3.AppendHybridShape(LinePtDir2)
part1.InWorkObject = LinePtDir2
part1.Update()
reference2 = part1.CreateReferenceFromObject(LinePtDir2)
Extrude1 = ShFactory.AddNewExtrude(reference2, 1000.000000, 1000.000000, Direction2)
body3.AppendHybridShape(Extrude1)
part1.InWorkObject = Extrude1
part1.Update()
reference1 = part1.CreateReferenceFromObject(Extrude1)
reference2 = part1.CreateReferenceFromObject(Intersection110)
Intersection7 = ShFactory.AddNewIntersection(reference2, reference1)
Intersection7.PointType = 0
body3.AppendHybridShape(Intersection7)
part1.InWorkObject = Intersection7
part1.Update()
reference2 = part1.CreateReferenceFromObject(Intersection160)
Intersection8 = ShFactory.AddNewIntersection(reference2, reference1)
Intersection8.PointType = 0
body3.AppendHybridShape(Intersection8)
part1.InWorkObject = Intersection8
part1.Update()
reference2 = part1.CreateReferenceFromObject(Intersection3)
Intersection9 = ShFactory.AddNewIntersection(reference2, reference1)
Intersection9.PointType = 0
body3.AppendHybridShape(Intersection9)
part1.InWorkObject = Intersection9
part1.Update()
reference2 = part1.CreateReferenceFromObject(Intersection4)
Intersection10 = ShFactory.AddNewIntersection(reference2, reference1)
Intersection10.PointType = 0
body3.AppendHybridShape(Intersection10)
part1.InWorkObject = Intersection10
part1.Update()

reference1 = part1.CreateReferenceFromObject(Intersection7)
reference2 = part1.CreateReferenceFromObject(Intersection8)
reference3 = part1.CreateReferenceFromObject(Intersection9)
Plane3Points1 = ShFactory.AddNewPlane3Points(reference1, reference2, reference3)
body3.AppendHybridShape(Plane3Points1)
part1.InWorkObject = Plane3Points1
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftup)
reference2 = part1.CreateReferenceFromObject(Plane3Points1)
Intersection11 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection11.PointType = 0
body3.AppendHybridShape(Intersection11)
part1.InWorkObject = Intersection11
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftdown)
Intersection12 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection12.PointType = 0
body3.AppendHybridShape(Intersection12)
part1.InWorkObject = Intersection12
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection11)
reference2 = part1.CreateReferenceFromObject(Fill110)
Split2 = ShFactory.AddNewHybridSplit(reference1, reference2, 1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split2)
part1.InWorkObject = Split2
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split2)
reference2 = part1.CreateReferenceFromObject(Fill1)
Split3 = ShFactory.AddNewHybridSplit(reference1, reference2, -1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split3)
part1.InWorkObject = Split3
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection12)
reference2 = part1.CreateReferenceFromObject(Fill110)
Split4 = ShFactory.AddNewHybridSplit(reference1, reference2, -1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split4)
part1.InWorkObject = Split4
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split4)
reference2 = part1.CreateReferenceFromObject(Fill1)
Split5 = ShFactory.AddNewHybridSplit(reference1, reference2, 1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split5)
part1.InWorkObject = Split5
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection7)
reference2 = part1.CreateReferenceFromObject(Intersection8)
LinePtPt3 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt3)
part1.InWorkObject = LinePtPt3
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection9)
reference2 = part1.CreateReferenceFromObject(Intersection10)
LinePtPt4 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt4)
part1.InWorkObject = LinePtPt4
part1.Update()
Fill3 = ShFactory.AddNewFill()
reference1 = part1.CreateReferenceFromObject(Split3)
Fill3.AddBound(reference1)
reference2 = part1.CreateReferenceFromObject(LinePtPt3)
Fill3.AddBound(reference2)
reference3 = part1.CreateReferenceFromObject(Split5)
Fill3.AddBound(reference3)
reference4 = part1.CreateReferenceFromObject(LinePtPt4)
Fill3.AddBound(reference4)
Fill3.Continuity = 0
body3.AppendHybridShape(Fill3)
part1.InWorkObject = Fill3
part1.Update()
Fill3.Name="Spar1"
ShFactory.GSMVisibility(PointOnCurve3,0)
ShFactory.GSMVisibility(PointOnCurve8,0)
ShFactory.GSMVisibility(PointOnCurve9,0)
ShFactory.GSMVisibility(Intersection9,0)
ShFactory.GSMVisibility(Intersection10,0)
ShFactory.GSMVisibility(Intersection7,0)
ShFactory.GSMVisibility(Intersection8,0)
ShFactory.GSMVisibility(LinePtPt1,0)
ShFactory.GSMVisibility(LinePtPt2,0)
ShFactory.GSMVisibility(LinePtPt3,0)
ShFactory.GSMVisibility(LinePtPt4,0)
ShFactory.GSMVisibility(Extrude1,0)
ShFactory.GSMVisibility(LinePtDir2,0)
ShFactory.GSMVisibility(Plane3Points1,0)
ShFactory.GSMVisibility(Split3,0)
ShFactory.GSMVisibility(Split5,0)

#Creating points for Spar 1.1
reference1 = part1.CreateReferenceFromObject(Intersection7)
Extrude4 = ShFactory.AddNewExtrude(reference1, 0.000000, 500.000000, Direction3)
body3.AppendHybridShape(Extrude4)
part1.InWorkObject = Extrude4
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection8)
Extrude5 = ShFactory.AddNewExtrude(reference1, 0.000000, 500.000000, Direction3)
body3.AppendHybridShape(Extrude5)
part1.InWorkObject = Extrude5
part1.Update()
reference1 = part1.CreateReferenceFromObject(Extrude4)
reference2 = part1.CreateReferenceFromObject(Extrude5)
Plane2Lines5 = ShFactory.AddNewPlane2Lines(reference1, reference2)
body3.AppendHybridShape(Plane2Lines5)
part1.InWorkObject = Plane2Lines5
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftup)
reference2 = part1.CreateReferenceFromObject(Plane2Lines5)
Intersection19 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection19.PointType = 0
body3.AppendHybridShape(Intersection19)
part1.InWorkObject = Intersection19
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftdown)
Intersection20 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection20.PointType = 0
body3.AppendHybridShape(Intersection20)
part1.InWorkObject = Intersection20
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection19)
reference2 = part1.CreateReferenceFromObject(Fill110)
Split16 = ShFactory.AddNewHybridSplit(reference1, reference2, -1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split16)
part1.InWorkObject = Split16
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection20)
reference2 = part1.CreateReferenceFromObject(Fill110)
Split17 = ShFactory.AddNewHybridSplit(reference1, reference2, 1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split17)
part1.InWorkObject = Split17
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split16)
PointOnCurve16 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 1.000000, False)
body3.AppendHybridShape(PointOnCurve16)
part1.InWorkObject = PointOnCurve16
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split17)
PointOnCurve17 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.000000, False)
body3.AppendHybridShape(PointOnCurve17)
part1.InWorkObject = PointOnCurve17
part1.Update()
reference1 = part1.CreateReferenceFromObject(PointOnCurve16)
reference2 = part1.CreateReferenceFromObject(PointOnCurve17)
LinePtPt11 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt11)
part1.InWorkObject = LinePtPt11
part1.Update()
Fill8 = ShFactory.AddNewFill()
reference1 = part1.CreateReferenceFromObject(Split16)
Fill8.AddBound(reference1)
reference2 = part1.CreateReferenceFromObject(LinePtPt3)
Fill8.AddBound(reference2)
reference3 = part1.CreateReferenceFromObject(Split17)
Fill8.AddBound(reference3)
reference4 = part1.CreateReferenceFromObject(LinePtPt11)
Fill8.AddBound(reference4)
Fill8.Continuity = 0
body3.AppendHybridShape(Fill8)
part1.InWorkObject = Fill8
part1.Update()
Fill8.Name="Spar1.1"
ShFactory.GSMVisibility(Plane2Lines5,0)
ShFactory.GSMVisibility(Split16,0)
ShFactory.GSMVisibility(Split17,0)
ShFactory.GSMVisibility(Extrude4,0)
ShFactory.GSMVisibility(Extrude5,0)
ShFactory.GSMVisibility(LinePtPt11,0)
ShFactory.GSMVisibility(PointOnCurve16,0)
ShFactory.GSMVisibility(PointOnCurve17,0)


#Creating Ribs 4-6
for ind in range(4,7):
    ref1 = part1.CreateReferenceFromObject(Plane2Lines1)
    x2=x1/4*(ind-3)
    st="PlaneOffset10"+str(ind)+" = ShFactory.AddNewPlaneOffset(ref1, x2, False)"
    exec st
    st="body3.AppendHybridShape(PlaneOffset10"+str(ind)+")"
    exec st
    part1.Update()
    st="ShFactory.GSMVisibility(PlaneOffset10"+str(ind)+",0)"
    exec st
    reference1 = part1.CreateReferenceFromObject(loftup)
    st="reference2 = part1.CreateReferenceFromObject(PlaneOffset10"+str(ind)+")"
    exec st
    st="Intersection10"+str(ind)+" = ShFactory.AddNewIntersection(reference1, reference2)"
    exec st
    st="Intersection10"+str(ind)+".PointType = 0"
    exec st
    st="body3.AppendHybridShape(Intersection10"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Intersection10"+str(ind)
    exec st
    part1.Update()
    reference1 = part1.CreateReferenceFromObject(loftdown)
    st="Intersection15"+str(ind)+" = ShFactory.AddNewIntersection(reference1, reference2)"
    exec st
    st="Intersection15"+str(ind)+".PointType = 0"
    exec st
    st="body3.AppendHybridShape(Intersection15"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Intersection15"+str(ind)
    exec st
    part1.Update ()
    st="Fill10"+str(ind)+" = ShFactory.AddNewFill()"
    exec st
    st="reference1 = part1.CreateReferenceFromObject(Intersection10"+str(ind)+")"
    exec st
    st="Fill10"+str(ind)+".AddBound(reference1)"
    exec st
    st="reference2 = part1.CreateReferenceFromObject(Intersection15"+str(ind)+")"
    exec st
    st="Fill10"+str(ind)+".AddBound(reference2)"
    exec st
    st="Fill10"+str(ind)+".Continuity = 0"
    exec st
    st="body3.AppendHybridShape(Fill10"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Fill10"+str(ind)
    exec st
    part1.Update()
    st="reference1 = part1.CreateReferenceFromObject(Fill10"+str(ind)+")"
    exec st
    reference2 = part1.CreateReferenceFromObject(Fill3)
    st="Split10"+str(ind)+" = ShFactory.AddNewHybridSplit(reference1, reference2, 1)"
    exec st
    st="ShFactory.GSMVisibility(Fill10"+str(ind)+",0)"
    exec st
    st="body3.AppendHybridShape(Split10"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Split10"+str(ind)
    part1.Update()
    st="Split10"+str(ind)+".Name=\"Rib"+str(ind)+"\""
    exec st
    st="ShFactory.GSMVisibility(Intersection10"+str(ind)+",0)"
    exec st
    st="ShFactory.GSMVisibility(Intersection15"+str(ind)+",0)"
    exec st

#Creating Ribs 7-9
for ind in range(7,10):
    ref1 = part1.CreateReferenceFromObject(PlaneOffset1)
    x2=x1/4*(ind-6)
    st="PlaneOffset10"+str(ind)+" = ShFactory.AddNewPlaneOffset(ref1, x2, False)"
    exec st
    st="body3.AppendHybridShape(PlaneOffset10"+str(ind)+")"
    exec st
    part1.Update()
    st="ShFactory.GSMVisibility(PlaneOffset10"+str(ind)+",0)"
    exec st
    reference1 = part1.CreateReferenceFromObject(loftup)
    st="reference2 = part1.CreateReferenceFromObject(PlaneOffset10"+str(ind)+")"
    exec st
    st="Intersection10"+str(ind)+" = ShFactory.AddNewIntersection(reference1, reference2)"
    exec st
    st="Intersection10"+str(ind)+".PointType = 0"
    exec st
    st="body3.AppendHybridShape(Intersection10"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Intersection10"+str(ind)
    exec st
    part1.Update()
    reference1 = part1.CreateReferenceFromObject(loftdown)
    st="Intersection15"+str(ind)+" = ShFactory.AddNewIntersection(reference1, reference2)"
    exec st
    st="Intersection15"+str(ind)+".PointType = 0"
    exec st
    st="body3.AppendHybridShape(Intersection15"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Intersection15"+str(ind)
    exec st
    part1.Update ()
    st="Fill10"+str(ind)+" = ShFactory.AddNewFill()"
    exec st
    st="reference1 = part1.CreateReferenceFromObject(Intersection10"+str(ind)+")"
    exec st
    st="Fill10"+str(ind)+".AddBound(reference1)"
    exec st
    st="reference2 = part1.CreateReferenceFromObject(Intersection15"+str(ind)+")"
    exec st
    st="Fill10"+str(ind)+".AddBound(reference2)"
    exec st
    st="Fill10"+str(ind)+".Continuity = 0"
    exec st
    st="body3.AppendHybridShape(Fill10"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Fill10"+str(ind)
    exec st
    part1.Update()
    st="reference1 = part1.CreateReferenceFromObject(Fill10"+str(ind)+")"
    exec st
    reference2 = part1.CreateReferenceFromObject(Fill3)
    st="Split10"+str(ind)+" = ShFactory.AddNewHybridSplit(reference1, reference2, 1)"
    exec st
    st="ShFactory.GSMVisibility(Fill10"+str(ind)+",0)"
    exec st
    st="body3.AppendHybridShape(Split10"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Split10"+str(ind)
    part1.Update()
    st="Split10"+str(ind)+".Name=\"Rib"+str(ind)+"\""
    exec st
    st="ShFactory.GSMVisibility(Intersection10"+str(ind)+",0)"
    exec st
    st="ShFactory.GSMVisibility(Intersection15"+str(ind)+",0)"
    exec st

dist=float(yp3)-float(yp4)

#Creating Ribs 11-13
for ind in range(11,14):
    ref1 = part1.CreateReferenceFromObject(Plane2Lines3)
    x2=dist/4*(ind-10)
    st="PlaneOffset1"+str(ind)+" = ShFactory.AddNewPlaneOffset(ref1, x2, False)"
    exec st
    st="body3.AppendHybridShape(PlaneOffset1"+str(ind)+")"
    exec st
    part1.Update()
    st="ShFactory.GSMVisibility(PlaneOffset1"+str(ind)+",0)"
    exec st
    reference1 = part1.CreateReferenceFromObject(loftup)
    st="reference2 = part1.CreateReferenceFromObject(PlaneOffset1"+str(ind)+")"
    exec st
    st="Intersection1"+str(ind)+" = ShFactory.AddNewIntersection(reference1, reference2)"
    exec st
    st="Intersection1"+str(ind)+".PointType = 0"
    exec st
    st="body3.AppendHybridShape(Intersection1"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Intersection1"+str(ind)
    exec st
    part1.Update()
    reference1 = part1.CreateReferenceFromObject(loftdown)
    st="Intersection"+str(150+ind)+" = ShFactory.AddNewIntersection(reference1, reference2)"
    exec st
    st="Intersection"+str(150+ind)+".PointType = 0"
    exec st
    st="body3.AppendHybridShape(Intersection"+str(150+ind)+")"
    exec st
    st="part1.InWorkObject = Intersection"+str(150+ind)
    exec st
    part1.Update ()
    st="Fill1"+str(ind)+" = ShFactory.AddNewFill()"
    exec st
    st="reference1 = part1.CreateReferenceFromObject(Intersection1"+str(ind)+")"
    exec st
    st="Fill1"+str(ind)+".AddBound(reference1)"
    exec st
    st="reference2 = part1.CreateReferenceFromObject(Intersection"+str(150+ind)+")"
    exec st
    st="Fill1"+str(ind)+".AddBound(reference2)"
    exec st
    st="Fill1"+str(ind)+".Continuity = 0"
    exec st
    st="body3.AppendHybridShape(Fill1"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Fill1"+str(ind)
    exec st
    part1.Update()
    st="Fill1"+str(ind)+".Name=\"Rib"+str(ind)+"\""
    exec st
    '''st="reference1 = part1.CreateReferenceFromObject(Fill10"+str(ind)+")"
    exec st
    reference2 = part1.CreateReferenceFromObject(Fill3)
    st="Split10"+str(ind)+" = ShFactory.AddNewHybridSplit(reference1, reference2, -1)"
    exec st
    st="ShFactory.GSMVisibility(Fill10"+str(ind)+",0)"
    exec st
    st="body3.AppendHybridShape(Split10"+str(ind)+")"
    exec st
    st="part1.InWorkObject = Split10"+str(ind)
    part1.Update()
    st="Split10"+str(ind)+".Name=\"Rib"+str(ind)+"\""
    exec st'''
    st="ShFactory.GSMVisibility(Intersection1"+str(ind)+",0)"
    exec st
    st="ShFactory.GSMVisibility(Intersection"+str(150+ind)+",0)"
    exec st


#Creating points for Spar 2
reference1 = part1.CreateReferenceFromObject(Intersection110)
PointOnCurve4 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.500000, False)
body3.AppendHybridShape(PointOnCurve4)
part1.InWorkObject = PointOnCurve4
part1.Update() 
reference1 = part1.CreateReferenceFromObject(Intersection160)
PointOnCurve5 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.500000, False)
body3.AppendHybridShape(PointOnCurve5)
part1.InWorkObject = PointOnCurve5
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection4)
PointOnCurve6 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.666666, False)
body3.AppendHybridShape(PointOnCurve6)
part1.InWorkObject = PointOnCurve6
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection3)
PointOnCurve7 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.333333, False)
body3.AppendHybridShape(PointOnCurve7)
part1.InWorkObject = PointOnCurve7
part1.Update()
ShFactory.GSMVisibility(PointOnCurve4,0)
ShFactory.GSMVisibility(PointOnCurve5,0)
ShFactory.GSMVisibility(PointOnCurve6,0)
ShFactory.GSMVisibility(PointOnCurve7,0)
reference1 = part1.CreateReferenceFromObject(PointOnCurve4)
reference2 = part1.CreateReferenceFromObject(PointOnCurve5)
reference3 = part1.CreateReferenceFromObject(PointOnCurve6)
Plane3Points2 = ShFactory.AddNewPlane3Points(reference1, reference2, reference3)
body3.AppendHybridShape(Plane3Points2)
part1.InWorkObject = Plane3Points2
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftup)
reference2 = part1.CreateReferenceFromObject(Plane3Points2)
Intersection15 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection15.PointType = 0
body3.AppendHybridShape(Intersection15)
part1.InWorkObject = Intersection15
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftdown)
Intersection14 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection14.PointType = 0
body3.AppendHybridShape(Intersection14)
part1.InWorkObject = Intersection14
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection15)
reference2 = part1.CreateReferenceFromObject(Fill110)
Split6 = ShFactory.AddNewHybridSplit(reference1, reference2, 1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split6)
part1.InWorkObject = Split6
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split6)
reference2 = part1.CreateReferenceFromObject(Fill1)
Split7 = ShFactory.AddNewHybridSplit(reference1, reference2, -1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split7)
part1.InWorkObject = Split7
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection14)
reference2 = part1.CreateReferenceFromObject(Fill110)
Split8 = ShFactory.AddNewHybridSplit(reference1, reference2, -1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split8)
part1.InWorkObject = Split8
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split8)
reference2 = part1.CreateReferenceFromObject(Fill1)
Split9 = ShFactory.AddNewHybridSplit(reference1, reference2, 1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split9)
part1.InWorkObject = Split9
part1.Update()
reference1 = part1.CreateReferenceFromObject(PointOnCurve4)
reference2 = part1.CreateReferenceFromObject(PointOnCurve5)
LinePtPt6 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt6)
part1.InWorkObject = LinePtPt6
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split7)
PointOnCurve13 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.000000, False)
body3.AppendHybridShape(PointOnCurve13)
part1.InWorkObject = PointOnCurve13
part1.Update()
reference1 = part1.CreateReferenceFromObject(PointOnCurve13)
reference2 = part1.CreateReferenceFromObject(PointOnCurve6)
LinePtPt7 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt7)
part1.InWorkObject = LinePtPt7
part1.Update()
Fill4 = ShFactory.AddNewFill()
reference1 = part1.CreateReferenceFromObject(Split7)
Fill4.AddBound(reference1)
reference2 = part1.CreateReferenceFromObject(LinePtPt6)
Fill4.AddBound(reference2)
reference3 = part1.CreateReferenceFromObject(Split9)
Fill4.AddBound(reference3)
reference4 = part1.CreateReferenceFromObject(LinePtPt7)
Fill4.AddBound(reference4)
Fill4.Continuity = 0
body3.AppendHybridShape(Fill4)
part1.InWorkObject = Fill4
part1.Update()
Fill4.Name="Spar2"
ShFactory.GSMVisibility(Intersection15,0)
ShFactory.GSMVisibility(Intersection14,0)
ShFactory.GSMVisibility(Plane3Points2,0)
ShFactory.GSMVisibility(Split7,0)
ShFactory.GSMVisibility(Split9,0)
ShFactory.GSMVisibility(LinePtPt6,0)
ShFactory.GSMVisibility(LinePtPt7,0)
ShFactory.GSMVisibility(PointOnCurve13,0)

#Creating points for Spar 2.1
reference1 = part1.CreateReferenceFromObject(PointOnCurve4)
Extrude2 = ShFactory.AddNewExtrude(reference1, 0.000000, 500.000000, Direction3)
body3.AppendHybridShape(Extrude2)
part1.InWorkObject = Extrude2
part1.Update()
reference1 = part1.CreateReferenceFromObject(PointOnCurve5)
Extrude3 = ShFactory.AddNewExtrude(reference1, 0.000000, 500.000000, Direction3)
body3.AppendHybridShape(Extrude3)
part1.InWorkObject = Extrude3
part1.Update()
reference1 = part1.CreateReferenceFromObject(Extrude2)
reference2 = part1.CreateReferenceFromObject(Extrude3)
Plane2Lines4 = ShFactory.AddNewPlane2Lines(reference1, reference2)
body3.AppendHybridShape(Plane2Lines4)
part1.InWorkObject = Plane2Lines4
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftup)
reference2 = part1.CreateReferenceFromObject(Plane2Lines4)
Intersection17 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection17.PointType = 0
body3.AppendHybridShape(Intersection17)
part1.InWorkObject = Intersection17
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftdown)
Intersection18 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection18.PointType = 0
body3.AppendHybridShape(Intersection18)
part1.InWorkObject = Intersection18
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection17)
reference2 = part1.CreateReferenceFromObject(Fill110)
Split14 = ShFactory.AddNewHybridSplit(reference1, reference2, -1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split14)
part1.InWorkObject = Split14
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection18)
reference2 = part1.CreateReferenceFromObject(Fill110)
Split15 = ShFactory.AddNewHybridSplit(reference1, reference2, 1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split15)
part1.InWorkObject = Split15
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split14)
PointOnCurve14 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 1.000000, False)
body3.AppendHybridShape(PointOnCurve14)
part1.InWorkObject = PointOnCurve14
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split15)
PointOnCurve15 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.000000, False)
body3.AppendHybridShape(PointOnCurve15)
part1.InWorkObject = PointOnCurve15
part1.Update()
reference1 = part1.CreateReferenceFromObject(PointOnCurve14)
reference2 = part1.CreateReferenceFromObject(PointOnCurve15)
LinePtPt10 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt10)
part1.InWorkObject = LinePtPt10
part1.Update()
Fill7 = ShFactory.AddNewFill()
reference1 = part1.CreateReferenceFromObject(Split14)
Fill7.AddBound(reference1)
reference2 = part1.CreateReferenceFromObject(LinePtPt6)
Fill7.AddBound(reference2)
reference3 = part1.CreateReferenceFromObject(Split15)
Fill7.AddBound(reference3)
reference4 = part1.CreateReferenceFromObject(LinePtPt10)
Fill7.AddBound(reference4)
Fill7.Continuity = 0
body3.AppendHybridShape(Fill7)
part1.InWorkObject = Fill7
part1.Update()
Fill7.Name="Spar2.1"
ShFactory.GSMVisibility(Plane2Lines4,0)
ShFactory.GSMVisibility(Split14,0)
ShFactory.GSMVisibility(Split15,0)
ShFactory.GSMVisibility(Extrude2,0)
ShFactory.GSMVisibility(Extrude3,0)
ShFactory.GSMVisibility(LinePtPt10,0)
ShFactory.GSMVisibility(PointOnCurve14,0)
ShFactory.GSMVisibility(PointOnCurve15,0)


#Creating points for Spar 3
reference1 = part1.CreateReferenceFromObject(Intersection113)
PointOnCurve8 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.150000, False)
body3.AppendHybridShape(PointOnCurve8)
part1.InWorkObject = PointOnCurve8
part1.Update() 
reference1 = part1.CreateReferenceFromObject(Intersection163)
PointOnCurve9 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.850000, False)
body3.AppendHybridShape(PointOnCurve9)
part1.InWorkObject = PointOnCurve9
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection4)
PointOnCurve10 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.850000, False)
body3.AppendHybridShape(PointOnCurve10)
part1.InWorkObject = PointOnCurve10
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection3)
PointOnCurve11 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.150000, False)
body3.AppendHybridShape(PointOnCurve11)
part1.InWorkObject = PointOnCurve11
part1.Update()
ShFactory.GSMVisibility(PointOnCurve8,0)
ShFactory.GSMVisibility(PointOnCurve9,0)
ShFactory.GSMVisibility(PointOnCurve10,0)
ShFactory.GSMVisibility(PointOnCurve11,0)
reference1 = part1.CreateReferenceFromObject(PointOnCurve8)
reference2 = part1.CreateReferenceFromObject(PointOnCurve9)
reference3 = part1.CreateReferenceFromObject(PointOnCurve10)
Plane3Points3 = ShFactory.AddNewPlane3Points(reference1, reference2, reference3)
body3.AppendHybridShape(Plane3Points3)
part1.InWorkObject = Plane3Points3
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftup)
reference2 = part1.CreateReferenceFromObject(Plane3Points3)
Intersection13 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection13.PointType = 0
body3.AppendHybridShape(Intersection13)
part1.InWorkObject = Intersection13
part1.Update()
reference1 = part1.CreateReferenceFromObject(loftdown)
Intersection16 = ShFactory.AddNewIntersection(reference1, reference2)
Intersection16.PointType = 0
body3.AppendHybridShape(Intersection16)
part1.InWorkObject = Intersection16
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection16)
reference2 = part1.CreateReferenceFromObject(Fill113)
Split10 = ShFactory.AddNewHybridSplit(reference1, reference2, -1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split10)
part1.InWorkObject = Split10
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split10)
reference2 = part1.CreateReferenceFromObject(Fill1)
Split11 = ShFactory.AddNewHybridSplit(reference1, reference2, 1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split11)
part1.InWorkObject = Split11
part1.Update()
reference1 = part1.CreateReferenceFromObject(Intersection13)
reference2 = part1.CreateReferenceFromObject(Fill113)
Split12 = ShFactory.AddNewHybridSplit(reference1, reference2, 1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split12)
part1.InWorkObject = Split12
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split12)
reference2 = part1.CreateReferenceFromObject(Fill1)
Split13 = ShFactory.AddNewHybridSplit(reference1, reference2, -1)
ShFactory.GSMVisibility(reference1,0)
body3.AppendHybridShape(Split13)
part1.InWorkObject = Split13
part1.Update()
reference1 = part1.CreateReferenceFromObject(PointOnCurve8)
reference2 = part1.CreateReferenceFromObject(PointOnCurve9)
LinePtPt8 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt8)
part1.InWorkObject = LinePtPt8
part1.Update()
reference1 = part1.CreateReferenceFromObject(Split13)
PointOnCurve12 = ShFactory.AddNewPointOnCurveFromPercent(reference1, 0.000000, False)
body3.AppendHybridShape(PointOnCurve12)
part1.InWorkObject = PointOnCurve12
part1.Update()
reference1 = part1.CreateReferenceFromObject(PointOnCurve12)
reference2 = part1.CreateReferenceFromObject(PointOnCurve10)
LinePtPt9 = ShFactory.AddNewLinePtPt(reference1, reference2)
body3.AppendHybridShape(LinePtPt9)
part1.InWorkObject = LinePtPt9
part1.Update()
Fill5 = ShFactory.AddNewFill()
reference1 = part1.CreateReferenceFromObject(Split11)
Fill5.AddBound(reference1)
reference2 = part1.CreateReferenceFromObject(LinePtPt8)
Fill5.AddBound(reference2)
reference3 = part1.CreateReferenceFromObject(Split13)
Fill5.AddBound(reference3)
reference4 = part1.CreateReferenceFromObject(LinePtPt9)
Fill5.AddBound(reference4)
Fill5.Continuity = 0
body3.AppendHybridShape(Fill5)
part1.InWorkObject = Fill5
part1.Update()
Fill5.Name="Spar3"
ShFactory.GSMVisibility(Intersection13,0)
ShFactory.GSMVisibility(Intersection16,0)
ShFactory.GSMVisibility(Plane3Points3,0)
ShFactory.GSMVisibility(Split11,0)
ShFactory.GSMVisibility(Split13,0)
ShFactory.GSMVisibility(LinePtPt8,0)
ShFactory.GSMVisibility(LinePtPt9,0)
ShFactory.GSMVisibility(PointOnCurve12,0)

#Writing the areas to an output file
ref1 = part1.CreateReferenceFromObject(Fill2)
TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
area= TheMeasurable.Area
fp=open("Structural.Values.dat","w")
st="Area of Rib1 is "+str(area)+" sq.m.\n"
fp.write(st)
ref1 = part1.CreateReferenceFromObject(Fill1)
TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
area= TheMeasurable.Area
st="Area of Rib2 is "+str(area)+" sq.m.\n"
fp.write(st)
ref1 = part1.CreateReferenceFromObject(Fill6)
TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
area= TheMeasurable.Area
st="Area of Rib3 is "+str(area)+" sq.m.\n"
fp.write(st)
for ind in range (4,10):
    st="ref1 = part1.CreateReferenceFromObject(Split10"+str(ind)+")"
    TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
    TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
    area= TheMeasurable.Area
    st="Area of Rib"+str(ind)+" is "+str(area)+" sq.m.\n"
    fp.write(st)
ref1 = part1.CreateReferenceFromObject(Fill110)
TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
area= TheMeasurable.Area
st="Area of Rib10 is "+str(area)+" sq.m.\n"
for ind in range (11,14):
    st="ref1 = part1.CreateReferenceFromObject(Fill1"+str(ind)+")"
    TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
    TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
    area= TheMeasurable.Area
    st="Area of Rib"+str(ind)+" is "+str(area)+" sq.m.\n"
    fp.write(st)
fp.write(st)
ref1 = part1.CreateReferenceFromObject(Fill3)
TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
area= TheMeasurable.Area
st="Area of Spar1 is "+str(area)+" sq.m.\n"
fp.write(st)
ref1 = part1.CreateReferenceFromObject(Fill4)
TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
area= TheMeasurable.Area
st="Area of Spar2 is "+str(area)+" sq.m.\n"
fp.write(st)
ref1 = part1.CreateReferenceFromObject(Fill5)
TheSPAWorkbench = CATIA.ActiveDocument.GetWorkbench ( "SPAWorkbench" )
TheMeasurable = TheSPAWorkbench.GetMeasurable(ref1)
area= TheMeasurable.Area
st="Area of Spar3 is "+str(area)+" sq.m.\n"
fp.write(st)
fp.close()


