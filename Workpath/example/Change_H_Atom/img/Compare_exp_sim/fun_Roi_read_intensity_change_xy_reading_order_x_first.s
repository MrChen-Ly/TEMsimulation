realnumber remind(number n1,number n2)
{
number n3
n1=round(n1*10**n2)
n3=n1/(10**n2)
return n3
}


void MyAddOvalROIToMask( image img, component ovalROI )
{
    number top, left, bottom, right
    /*number cx,cy,r
    ovalROI.ROIGetcircle( cx, cy,r)
    cx=remind(cx,0)
    cy=remind(cy,0)
    r=remind(r,0)*/
	number Ox,Oy,t,l,b,r,ra
	ovalROI.componentgetrect(t,l,b,r)
	Ox=(r+l)/2
	Oy=(b+t)/2
	
	
	ra=(r-l+b-t)/4
	ra=round(ra)
	//Ox=round(Ox)
	//Oy=round(Oy)

	
    number sx = 2*ra
    number sy = 2*ra
   
    
    // Create mask of just the rect area
    image maskCut := RealImage( "", 4, sx, sy)
    maskCut = ( ((ra-icol)/ra)**2 + ((ra-irow)/ra)**2 <= 1 ) ? 1 : 0
    top=Oy-ra
    left=Ox-ra
    bottom=Oy+ra
    right=Ox+ra
    // Apply mask to image
    img[top, left, bottom, right] = maskCut
    
}

//sum peak integral intensity
      
   number GetROISum( image img1, component theRoi )
{

    
    // Create a binary mask of "img1" size using the ROI's coordinates
    image mask = img1 * 0;   // image of same size as "img1" with 0 values
    number sx, sy	
    img1.GetSize( sx, sy )
    
    MyAddOvalROIToMask( mask, theROI )

    
   // if ( TwoButtonDialog( "Show mask?", "Yes", "No" ) )
       // mask.ShowImage()
    
    // Do meanValue as sums of masked points
    number maskedPoints = sum( mask )
    number maskedSum
    if ( 0 < maskedPoints ) 
        maskedSum = sum( mask * img1 ) 	 	
        //maskedSum = sum( mask * img1 ) / maskedPoints 
    else
        maskedSum = sum( img1 )
    
    return maskedSum 
}
TagGroup DLG, DLGItems ,xnofield,ynofield
DLG = DLGCreateDialog( "Please enter strings", DLGItems ) 
TagGroup popup1tg = DLGCreatePopup( 0 ) 
popup1tg.DLGAddPopupItemEntry( "integral" ) //popup1tg.DLGGetValue()=1
popup1tg.DLGAddPopupItemEntry( "Max" ) //popup1tg.DLGGetValue()=2
popup1tg.DLGAddPopupItemEntry( "mean" ) //popup1tg.DLGGetValue()=3
popup1tg.DLGAddPopupItemEntry( "x,y" )//popup1tg.DLGGetValue()=4
DLGitems.DLGAddElement( DLGCreateLabel( "Please select option (popup):" ) ) 
DLGitems.DLGAddElement( popup1tg ) 

	
	
taggroup varlab1=DLGCreatelabel("x:")
xnofield = DLGCreaterealField(1.0,8, 4)
taggroup noxgroup=dlggroupitems(varlab1, xnofield)
noxgroup.dlgtablelayout(2,1,0)
noxgroup.dlgexternalpadding(5,0)
DLGitems.DLGAddElement(noxgroup) 

taggroup varlab2=DLGCreatelabel("y:")
ynofield = DLGCreaterealField(1.0,8, 4)
taggroup noygroup=dlggroupitems(varlab2, ynofield)
noygroup.dlgtablelayout(2,1,0)
noygroup.dlgexternalpadding(5,0)
DLGitems.DLGAddElement(noygroup) 
taggroup  val1tg
DLGitems.DLGAddElement( DLGCreateStringField( "Getname:", val1tg, "Atom_O_", 20 ) )

TagGroup radio_items
taggroup radioList = DLGCreateRadioList( radio_items, 0, "output X Y" )
radio_items.DLGAddElement( DLGCreateRadioItem( "NONE", 0 ) )
radio_items.DLGAddElement( DLGCreateRadioItem( "XY ", 1 ) )
radiolist.dlgexternalpadding(0,10)
DLGitems.DLGAddElement(radiolist) 
 
TagGroup opt1tg = DLGCreateCheckBox( "unit",0)
DLGitems.DLGAddElement( opt1tg)
    
if ( !Alloc( UIframe ).Init( DLG ).Pose() ) 
Throw( "User abort." ) 
	
try
{
image sourceimg:=getfrontimage()
showimage(sourceimg)
imagedisplay sourcedisp=sourceimg.imagegetimagedisplay(0)
number noovals=sourcedisp.componentcountchildrenoftype(6)
number radius, sizeX, sizeY, scalex, scaley
getsize(sourceimg, sizeX, sizeY)
getscale(sourceimg, scalex, scaley)
number y,x
dlggetvalue(xnofield,x)
dlggetvalue(ynofield,y)
getpersistentnumbernote("Yale recording:Mouse Position:Current radius",radius)
string atomtypevalue,atomtypevaluex,atomtypevaluey,atomtypevalueinten
getpersistentstringnote("Yale recording:Mouse Position:Atomtype",atomtypevalue)
dlggetvalue(val1tg,atomtypevalue)
string label 
popup1tg.DLGGetNthLabel( popup1tg.DLGGetValue()-1, label )
atomtypevaluex=atomtypevalue+"x"
atomtypevaluey=atomtypevalue+"y"


atomtypevalueinten=atomtypevalue+label
image imgx:=realimage(atomtypevaluex,4,x,y)
image imgy:=realimage(atomtypevaluey,4,x,y)
image imgin:=realimage(atomtypevalueinten,4,x,y)

number count
for (number i=0;i<=noovals-2;i++)
{
component thisoval=sourcedisp.componentgetnthchildoftype(6,i)
if(thisoval.ComponentIsSelected())
{
number col,row,intensity
col=mod(count,x)
row=floor(count/x)
number Ocx,Ocy,t,l,b,r
thisoval.componentgetrect(t,l,b,r)


Ocx=(r+l)/2
Ocy=(b+t)/2
if (opt1tg.DLGGetValue()==1)
{
Ocx=Ocx*scalex
Ocy=Ocy*scaley
}
imgx[col,row]=Ocx
imgy[col,row]=Ocy







if (popup1tg.DLGGetValue()==1)//"integral"
{
result("in")
imgin[col,row]=GetROISum(sourceimg,thisoval)

}
else if (popup1tg.DLGGetValue()==2)//"Max"
{
imgin[col,row]=MAX(sourceimg[t,l,b,r])
}
else//"mean"
{
imgin[col,row]=mean(sourceimg[t,l,b,r])
}


count=count+1

}
if(radioList.DLGGetValue()==1)
{
showimage(imgx)
showimage(imgy)
}
showimage(imgin)
//imageDisplay sourcedisp = imgx.ImageGetImageDisplay( 0 ) 
//sourcedisp.ImageDisplayChangeDisplayType( "spreadsheet")
}


}
catch break
