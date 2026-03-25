
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

string str="STO_output_"
string name
GetString("Please enter the sample name",str, name)
number count
getnumber("Please enter the number of img",32.0,count)

number x1,y1,r
getnumber("x1",18,x1)
getnumber("y1",14,y1)
getnumber("r",4,r)


for (number i=1;i<=count;i++)
{
string imgname
imgname=name+ Format(i,"%02d")+"_sl_032_map"
image img

getnamedimage(img,imgname)
ImageSetDimensionCalibration(img,1,0,0.008690,"nm",0)

imageDisplay disp = img.ImageGetImageDisplay( 0 ) 
string strname=getname(img)
component newoval=newovalannotation(y1-r, x1-r, y1+r,x1+r)
disp.componentaddchildatend(newoval)

result(i+": "+GetROISum(img,newoval)+"\n")

}

