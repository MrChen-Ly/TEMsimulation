// Atom Colouriser. A script to create (and fit) a lattice to an atomic resolution image.
// The atomic positions can then be selected and colourised to highlight defects etc.



// Press the ? button to print instructions in the Output window.

// Updated in v1.1 to fix minor formatting issues in GMS 3.x



// The default settings

number defaultoriginposition=5
if(!getpersistentnumbernote("Atom Colouriser:Settings:Origin Inset (%)", defaultoriginposition))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Origin Inset (%)", defaultoriginposition)
	}


// The default number of ovals along the x axis

number defaultgridxsize=10
if(!getpersistentnumbernote("Atom Colouriser:Settings:Grid Size X", defaultgridxsize))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Grid Size X", defaultgridxsize)
	}


// The default number of ovals along the y axis

number defaultgridysize=10
if(!getpersistentnumbernote("Atom Colouriser:Settings:Grid Size Y", defaultgridysize))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Grid Size Y", defaultgridysize)
	}


// The default spacing of the grid in X (in nm)

number defaultgridxspacing=0.5
if(!getpersistentnumbernote("Atom Colouriser:Settings:Grid X Spacing (nm)", defaultgridxspacing))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Grid X Spacing (nm)", defaultgridxspacing)
	}


// The default spacing of the grid in Y (in nm)

number defaultgridyspacing=0.5
if(!getpersistentnumbernote("Atom Colouriser:Settings:Grid Y Spacing (nm)", defaultgridyspacing))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Grid Y Spacing (nm)", defaultgridyspacing)
	}


// The default column angle - in some projections the lattice columns and rows are not at right angles
// This value specifies the angle of the columns from vertical. ie vertical is zero. It is assumed that rows
// are always horizontal, so a column angle of zero means that columns and row define a 90deg angle. 

number defaultcolumnangle=0
if(!getpersistentnumbernote("Atom Colouriser:Settings:Column Angle (degs", defaultcolumnangle))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Column Angle (degs", defaultcolumnangle)
	}


// The default oval radius in pixels

number defaultovalradius=16
if(!getpersistentnumbernote("Atom Colouriser:Settings:Oval Radius (pxl)", defaultovalradius))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Oval Radius (pxl)", defaultovalradius)
	}

	
// The default setting for the line or fill radio

number defaultlineorfillradio=0
if(!getpersistentnumbernote("Atom Colouriser:Settings:Line or Fill Radio (0-1)", defaultlineorfillradio))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Line or Fill Radio (0-1)", defaultlineorfillradio)
	}


// These values do not appear in the dialog. Clicking on the Tools button in the dialog will bring up a dialog
// which allows them to be changed.


// The default number of centre of gravity iterations

number defaultcogiterations=5
if(!getpersistentnumbernote("Atom Colouriser:Settings:Centre of Gravity Iterations", defaultcogiterations))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Centre of Gravity Iterations", defaultcogiterations)
	}


// The default pixel width at which the images get displayed

number defaultdisplaywidth=400
if(!getpersistentnumbernote("Atom Colouriser:Settings:Image Display Width (pxls)", defaultdisplaywidth))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Image Display Width (pxls)", defaultdisplaywidth)
	}


// The default RGB values for  Button 1

number defaultbutton1colourR=255
if(!getpersistentnumbernote("Atom Colouriser:Settings:Button 1 Colour (Red)", defaultbutton1colourR))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Button 1 Colour (Red)", defaultbutton1colourR)
	}

number defaultbutton1colourG=0
if(!getpersistentnumbernote("Atom Colouriser:Settings:Button 1 Colour (Green)", defaultbutton1colourG))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Button 1 Colour (Green)", defaultbutton1colourG)
	}
	
number defaultbutton1colourB=0
if(!getpersistentnumbernote("Atom Colouriser:Settings:Button 1 Colour (Blue)", defaultbutton1colourB))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Button 1 Colour (Blue)", defaultbutton1colourB)
	}

// The default RGB values for  Button 2

number defaultbutton2colourR=255
if(!getpersistentnumbernote("Atom Colouriser:Settings:Button 2 Colour (Red)", defaultbutton2colourR))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Button 2 Colour (Red)", defaultbutton2colourR)
	}

number defaultbutton2colourG=255
if(!getpersistentnumbernote("Atom Colouriser:Settings:Button 2 Colour (Green)", defaultbutton2colourG))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Button 2 Colour (Green)", defaultbutton2colourG)
	}
	
number defaultbutton2colourB=0
if(!getpersistentnumbernote("Atom Colouriser:Settings:Button 2 Colour (Blue)", defaultbutton2colourB))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Button 2 Colour (Blue)", defaultbutton2colourB)
	}


// The default RGB values for  Button 3

number defaultbutton3colourR=0
if(!getpersistentnumbernote("Atom Colouriser:Settings:Button 3 Colour (Red)", defaultbutton3colourR))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Button 3 Colour (Red)", defaultbutton3colourR)
	}

number defaultbutton3colourG=255
if(!getpersistentnumbernote("Atom Colouriser:Settings:Button 3 Colour (Green)", defaultbutton3colourG))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Button 3 Colour (Green)", defaultbutton3colourG)
	}
	
number defaultbutton3colourB=255
if(!getpersistentnumbernote("Atom Colouriser:Settings:Button 3 Colour (Blue)", defaultbutton3colourB))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Button 3 Colour (Blue)", defaultbutton3colourB)
	}


// The default setting for the colour radio which selects the colour to use

number colourradio=0
if(!getpersistentnumbernote("Atom Colouriser:Settings:Colour Radio (0-2)", colourradio))
	{
		setpersistentnumbernote("Atom Colouriser:Settings:Colour Radio (0-2)", colourradio)
	}



// Three objects are used here: a main dialog to display the main dialog
// a sub-dialog to choose the colours and a redrawer object which recreates the
// dialog to force an update of the coloured buttons

object SubDialogObject, RedrawDialogObject, maindialogobject



// The class creates the sub-dialog and responds to any changed therein
// The sub-dialog is the colour picker to choose the colour colour buttons

Class SubDialogClass:uiframe
	{
		// responds when the Cancel button is pressed by closing the sub-dialog

		void cancelpushed(object self)
			{
				self.close()
			}


	// responds when the Save button is pushed by saving the colour to the global info
	// and updating the button

	void savecolourpushed(object self)
		{
			// Source the atomic number (string) from the label in the subdialog
			// and convert it to a number. Updating is done by calling the RedrawDialogObject
			// this is a suicide object which uses its destructor to close the dialog and 
			// then redraw it. This rather radical approach was used to update the dialog
			// as I have been unable to find a way to force the colour graphics used in
			// the dual state bevel buttons to update 

			// Source the element name from the sub-dialog title and
			// then use it to get the element's atomic number
			
			string colourlabel=dlggettitle(self.lookupelement("colourlabel"))
			string buttonnumber=right(colourlabel, 1)		
			
			// Source the colour value and save it to tags
			
			number red, green, blue
			red=dlggetvalue(self.lookupelement("rfield"))
			green=dlggetvalue(self.lookupelement("gfield"))
			blue=dlggetvalue(self.lookupelement("bfield"))

			setpersistentnumbernote("Atom Colouriser:Settings:Button "+buttonnumber+" Colour (Red)", red)
			setpersistentnumbernote("Atom Colouriser:Settings:Button "+buttonnumber+" Colour (Green)", green)
			setpersistentnumbernote("Atom Colouriser:Settings:Button "+buttonnumber+" Colour (Blue)", blue)
			self.close()
			
			
			// Invoke the RedrawDialogObject to close the periodic table and redraw it

			RedrawDialogObject.ScriptObjectClone().init(self.ScriptObjectgetID()).StartThread("Go")
		}
		
		
		// Responds when the Reset button is pressed by setting the colour of 
		// the RGB fields and the swatch to the defaultcolour
		
		void resetpushed(object self)
			{
				rgbnumber defaultcolour
				getpersistentrgbnumbernote("CSV Importer:Settings:Default Button Colour", defaultcolour)
				
				number red, green, blue
				red=red(defaultcolour)
				green=green(defaultcolour)
				blue=blue(defaultcolour)
				
				dlgvalue(self.lookupelement("rfield"), red)
				dlgvalue(self.lookupelement("gfield"), green)
				dlgvalue(self.lookupelement("bfield"), blue)
			}


	// Responds when the colour picker (eye dropper) button is pressed
	// by displaying a colour selection dialog and setting the RGB field 
	// values according to the choice

	void pickerpushed(object self)
		{
			rgbnumber default=rgb(255,255,255)
			rgbnumber choice
			if(!GetRGBColorDialog( "Choose a colour", default, choice ) ) exit(0)
			
			number red=red(choice)
			dlgvalue(self.lookupelement("rfield"), red)
			
			number green=green(choice)
			dlgvalue(self.lookupelement("gfield"), green)
			
			number blue=blue(choice)
			dlgvalue(self.lookupelement("bfield"), blue)
			
			rgbnumber colourvalue=rgb(red, green, blue)
		}


	// Responds when the RGB values in the subdialog fields are changed
	// by updating the colour of swatch

	void rgbchanged(object self, taggroup tg)
			{
				number red, green, blue
				
				red=dlggetvalue(self.lookupelement("rfield"))
				if(red<0) red=0
				if(red>255) red=255
				dlgvalue(self.lookupelement("rfield"), red)
				
				green=dlggetvalue(self.lookupelement("gfield"))
				if(green<0) green=0
				if(green>255) green=255
				dlgvalue(self.lookupelement("gfield"), green)

				blue=dlggetvalue(self.lookupelement("bfield"))
				if(blue<0) blue=0
				if(blue>255) blue=255
				dlgvalue(self.lookupelement("bfield"), blue)
				
				taggroup swatch=self.lookupelement("swatch")
				taggroup bitmaptags=swatch.dlggetelement(0)
				rgbimage graphic=dlggetbitmapdata(bitmaptags)
				graphic=rgb(red, green, blue)
				bitmaptags.dlgbitmapdata(graphic)
			}


	// Creates the sub-dialog
	
	TagGroup CreateSubDialog(object self) 
		{

		// Graphic for the eyedropper button
		
		rgbimage rgbthumbnail:=[23,23]:
			{
				{rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(212,208,200)},
				{rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(255,255,255),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(192,192,192),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(255,255,255),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(255,255,255),rgb(255,255,255),rgb(128,128,128),rgb(0,0,0),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(255,255,255),rgb(255,255,255),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(255,255,255),rgb(255,255,255),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(255,255,255),rgb(255,255,255),rgb(0,191,191),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(212,208,200),rgb(255,255,255),rgb(0,191,191),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(0,191,191),rgb(0,0,0),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(0,191,191),rgb(0,0,0),rgb(0,191,191),rgb(0,191,191),rgb(0,0,0),rgb(0,191,191),rgb(0,191,191),rgb(0,191,191),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(0,191,191),rgb(0,191,191),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,191,191),rgb(0,191,191),rgb(0,191,191),rgb(0,191,191),rgb(0,191,191),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(0,191,191),rgb(0,191,191),rgb(0,191,191),rgb(0,191,191),rgb(0,191,191),rgb(0,191,191),rgb(0,191,191),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(255,255,255),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(128,128,128),rgb(0,0,0),rgb(212,208,200)},
				{rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(0,0,0),rgb(212,208,200)},
				{rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200),rgb(212,208,200)}
			}
			
			rgbimage pickeronbutton:=dlgmakeraised(rgbthumbnail)
			rgbimage pickeroffbutton=dlgmakelowered(rgbthumbnail)
			
			number defaultfieldvalue=42
			number fieldwidth=5
			TagGroup SubDialog=DLGCreateDialog("Sub-dialog")
			TagGroup box_items
			Taggroup Box=DLGCreateBox("Colour Selection", box_items).dlgexternalpadding(3,3).dlginternalpadding(22,10)

			taggroup atnolabel=dlgcreatelabel("Color :     ").dlgidentifier("colourlabel")
			
			taggroup swatch=dlgcreategraphic(40,40).dlgidentifier("swatch")
			image colourgraphic=rgbimage("",4,40,40)
			number red=192
			number green=192
			number blue=192
			
			colourgraphic=rgb(red, green, blue)
			
			taggroup imagetemp=dlgcreatebitmap(colourgraphic).dlgidentifier("colourswatch")
			dlgaddbitmap(swatch, imagetemp)
			
			taggroup label=dlgcreatelabel("R")
			taggroup rfield=dlgcreateintegerfield(red, 6).dlgidentifier("rfield").dlgchangedmethod("rgbchanged")
			taggroup rgroup=dlggroupitems(label, rfield).dlgtablelayout(2,1,0)
			
			label=dlgcreatelabel("G")
			taggroup gfield=dlgcreateintegerfield(green, 6).dlgidentifier("gfield").dlgchangedmethod("rgbchanged")
			taggroup ggroup=dlggroupitems(label, gfield).dlgtablelayout(2,1,0)

			label=dlgcreatelabel("B")
			taggroup bfield=dlgcreateintegerfield(blue, 6).dlgidentifier("bfield").dlgchangedmethod("rgbchanged")
			taggroup bgroup=dlggroupitems(label, bfield).dlgtablelayout(2,1,0)
			
			taggroup rgbgroup=dlggroupitems(rgroup, ggroup, bgroup).dlgtablelayout(1,3,0).dlgexternalpadding(5,0)
			taggroup swatchgroup=dlggroupitems(swatch, rgbgroup).dlgtablelayout(2,1,0)
			
			taggroup resetbutton=dlgcreatepushbutton("Reset", "resetpushed").dlginternalpadding(2,0)
			taggroup pickerbutton=dlgcreatebevelbutton(pickeroffbutton, pickeronbutton, "pickerpushed")
			taggroup savebutton=dlgcreatepushbutton("Save", "savecolourpushed").dlginternalpadding(4,0)
			taggroup cancelbutton=dlgcreatepushbutton("Cancel", "cancelpushed")
			taggroup spacer1=dlgcreatelabel("").dlgexternalpadding(6,0)
			taggroup spacer2=dlgcreatelabel("").dlgexternalpadding(0,0)

			taggroup topbuttongroup=dlggroupitems(resetbutton, spacer1, pickerbutton).dlgtablelayout(3,1,0).dlganchor("West")
			taggroup bottombuttongroup=dlggroupitems(savebutton, spacer2,cancelbutton).dlgtablelayout(3,1,0).dlganchor("West")
			taggroup allbuttonsgroup=dlggroupitems(topbuttongroup, bottombuttongroup).dlgtablelayout(1,2,0)

			taggroup allelementsgroup=dlggroupitems(atnolabel, swatchgroup, allbuttonsgroup).dlgtablelayout(1,4,0)
			
			box_items.DLGAddElement(allelementsgroup)
			subdialog.dlgaddelement(box)
			return SubDialog
		}
	
	
	// Constructor - this creates the subdialog, but does not display it yet
	
	SubDialogClass(object self)
		{ 
			self.init(self.CreateSubDialog())
		}
		
		
	// Destructor - does nothing
		
	~SubDialogClass(object self) 
		{
			// Note the sub-dialog does not go out of scope when closed. Since it was created with the Main Dialog object
			// It only goes out of scope when the main dialog is destructed.
		}
	}


// Main Dialog class

class AtomColouriserDialog : uiframe
	{
		// Function to zoom an image to the specified width

		void zoomtosize(object self, image img, number newxsize)
			{
				// If the passed in size is <128 do nothing. 

				if(newxsize<128) return


				// Get some info on the image and show it

				number xsize, ysize
				getsize(img, xsize, ysize)
				number newysize=ysize*(newxsize/xsize)
				showimage(img)


				// Source the displays, documents and windows and set the new 
				// content area of the image to the desired value

				imagedisplay imgdisp=img.imagegetimagedisplay(0)
				imagedocument imgdoc=getfrontimagedocument()
				documentwindow docwin=getdocumentwindow(0)
				docwin.windowsetcontentsize(newxsize, newysize)


				// Compute the transform from image to display and maximise the image to fit the new window

				number i2voffx, i2voffy, i2vscalex, i2vscaley, vtop, vleft, vbottom, vright
				imgdisp.ComponentGetChildToviewTransform(i2voffx, i2voffy, i2vscalex, i2vscaley)
				objecttransformtransformrect(i2voffx, i2voffy, i2vscalex, i2vscaley, 0, 0, ysize, xsize,vtop, vleft, vbottom, vright)
				ImageDocumentMaximizeRectInView( imgDoc, vtop, vleft, vbottom, vright ) 
			}


		// Function to return the image ID of an image which has been labelled with a string note. The tag is described by the pathstring
		// which in this case is "My Tag:Image ID" and the string tag which describes the image - in this 

		number findimagebyIDstring(object self, string pathstring, string idstring)
			{
				// If either of the strings are empty - return zero
			
				if(idstring=="" || pathstring=="") return 0


				// Count the number of images open - if zero return zero

				image sourceimg
				number nodocs=countimagedocuments()
					
				if(nodocs==0) 
					{
						return 0
					}
					
					
				// Loop through open images looking for one with the relevant tag
					
				number counter=0, i
				
				for(i=0; i<nodocs; i++)
					{
						imagedocument tempimgdoc=getimagedocument(i)
						image tempimg:=imagedocumentgetimage(tempimgdoc,0)
				

						// Get the tag - if it matches the target end
						
						string tempstring=getstringnote(tempimg, pathstring)
								
						if(tempstring==idstring)
							{
								// set a counter to indicate the target has been found
								
								counter=counter+1
								sourceimg:=tempimg
								break
							}
					}


				// If the counter is zero then no suitably tagged image was found - bail out
				
				if(counter==0) return 0


				// Return the image ID of the located image
				
				number sourceid=imagegetid(sourceimg)
				return sourceid
			}


	// Responds when the Source Image button is pressed

	void sourceimageresponse(object self)
		{
			// Ensure at least one image is displayed
			
			number nodocs=countdocumentwindowsoftype(5)
			if(nodocs<1)
				{
					showalert("Ensure an image is displayed.",2)
					return
				}


			// Source the front-most image and check that it is 2D
			
			image sourceimg:=getfrontimage()
			number xsize, ysize
			getsize(sourceimg, xsize, ysize)
			if(ysize<2)
				{
					showalert("This works on 2D images only.",2)
					return
				}


			// Source the image calibration - images must be calibrated

			number imagexscale=sourceimg.imagegetdimensionscale(0)
			number imageyscale=sourceimg.imagegetdimensionscale(1)
			if(imagexscale==1 || imageyscale==1)
				{
					showalert("This will not work on uncalibrated images.",2)
					exit(0)
				}
				
				
			// Enable/disable the dialog elements

			self.setelementisenabled("sourceimagebutton",0)
			self.setelementisenabled("distortboxgroup",0)
			self.setelementisenabled("gridboxgroup",1)
			self.setelementisenabled("allcolourboxgroup",0)
			self.setelementisenabled("maskbutton",0)

			

			// Label the image with a tag - so that other routines can find it.
			
			setstringnote(sourceimg, "Atom Colouriser:Image ID", "Source Image")


			// position and scale the image
			
			number displaywidth
			getpersistentnumbernote("Atom Colouriser:Settings:Image Display Width (pxls)", displaywidth)
			if(displaywidth<64) displaywidth=64
			
			self.zoomtosize(sourceimg, displaywidth)
			showimage(sourceimg)
			documentwindow sourcewin=getdocumentwindow(0)
			sourcewin.windowsetframeposition(0,0)


			// Source the position (%) of the origin
			
			number origininset
			getpersistentnumbernote("Atom Colouriser:Settings:Origin Inset (%)", origininset)
			if(origininset>50) origininset=50
			
			number originx=xsize*(origininset/100)
			if(originx<10) originx=0
			
			number currentoriginx
			dlggetvalue(self.lookupelement("originxfield"), currentoriginx)
			
			
			// Update the field with the default, but only if it is zero
			
			if(currentoriginx==0)dlgvalue(self.lookupelement("originxfield"), originx)
			
			
			// Origin y field 
			
			number originy=ysize*(origininset/100)
			if(originy<10) originy=0
			number currentoriginy
			dlggetvalue(self.lookupelement("originyfield"), currentoriginy)
			
					
			// Update the field with the default, but only if it is zero

			if(currentoriginy==0) dlgvalue(self.lookupelement("originyfield"), originy)
			
			
			// Remove any ovals from the image
			
			number noovals
			imagedisplay disp=sourceimg.imagegetimagedisplay(0)
			noovals=disp.componentcountchildrenoftype(6)
			number i
			
			for(i=noovals-1; i>-1; i--)
				{
					component thisoval=disp.componentgetnthchildoftype(6,i)
					thisoval.componentremovefromparent()
				}


			// source the gridx and y from the dialog

			number gridxspacing, gridyspacing, gridxovals, gridyovals, ovalradius
			dlggetvalue(self.lookupelement("gridxspacingfield"), gridxspacing)
			dlggetvalue(self.lookupelement("gridyspacingfield"), gridyspacing)
			
			dlggetvalue(self.lookupelement("gridxfield"), gridxovals)
			dlggetvalue(self.lookupelement("gridyfield"), gridyovals)
			
			dlggetvalue(self.lookupelement("originxfield"), originx)
			dlggetvalue(self.lookupelement("originyfield"), originy)
			
			dlggetvalue(self.lookupelement("ovalradiusfield"), ovalradius)

			number xpixelstep=gridxspacing/imagexscale
			number ypixelstep=gridyspacing/imageyscale
			
			
			// Source the column angle value from the Col. Angle field
			
			number columnangle
			dlggetvalue(self.lookupelement("columnanglefield"), columnangle)
			

			// now add the grid of ovals
			
			number thisposx=originx
			number thisposy=originy
			number top, left, bottom, right
			number x, y, counter
			noovals=gridxovals*gridyovals
			
			string atomvalue
			dlggetvalue(self.lookupelement("atomfield"),atomvalue)		
			deletenote(sourceimg, "Atom Colouriser:Points:"+atomvalue)
			setnumbernote(sourceimg, "Atom Colouriser:Points:"+atomvalue+":Number of Points", noovals)
		
		
			// calculate the lateral shift due to the column angle per row
							
			number xshift=tan(columnangle/(180/pi()))*ypixelstep

			for(y=0; y<gridyovals; y++)
				{

					for(x=0; x<gridxovals; x++)
						{		
							top=thisposy-ovalradius
							left=thisposx-ovalradius
							bottom=thisposy+ovalradius
							right=thisposx+ovalradius
							
							
							// Save the coordinates on the image
							
							setnumbernote(sourceimg,  "Atom Colouriser:Points:"+atomvalue+":Oval "+counter+":x", thisposx)
							setnumbernote(sourceimg,  "Atom Colouriser:Points:"+atomvalue+":Oval "+counter+":y", thisposy)
							
							
							// Add the oval
							
							component newoval=newovalannotation(top, left, bottom,right)
							if(x==0 && y==0) newoval.componentsetforegroundcolor(1,0,0) // origin oval is red
							else newoval.componentsetforegroundcolor(1,1,0) // other ovals are yellow
							disp.componentaddchildatend(newoval)
							thisposx=thisposx+xpixelstep
							counter=counter+1
						}
						
					thisposy=thisposy+ypixelstep
					thisposx=originx+(xshift*(y+1))
				}
			showimage(sourceimg)
		}
		
	
	// Responds when the origin x field + button is pressed

	void originxplusresponse(object self)
		{
			number originxval
			dlggetvalue(self.lookupelement("originxfield"), originxval)

			number stepsize=1
			if(shiftdown()) stepsize=5
			if(controldown()) stepsize=25
			if(optiondown()) stepsize=50

			originxval=originxval+stepsize
			dlgvalue(self.lookupelement("originxfield"), originxval)
		}


	// Responds when the origin x field _ button is pressed

	void originxminusresponse(object self)
		{
			number originxval
			dlggetvalue(self.lookupelement("originxfield"), originxval)

			number stepsize=-1
			if(shiftdown()) stepsize=-5
			if(controldown()) stepsize=-25
			if(optiondown()) stepsize=-50

			originxval=originxval+stepsize
			if(originxval<0) originxval=0
			dlgvalue(self.lookupelement("originxfield"), originxval)
		}


	// Responds when the origin y field + button is pressed

	void originyplusresponse(object self)
		{
			number originyval
			dlggetvalue(self.lookupelement("originyfield"), originyval)

			number stepsize=1
			if(shiftdown()) stepsize=5
			if(controldown()) stepsize=25
			if(optiondown()) stepsize=50

			originyval=originyval+stepsize
			dlgvalue(self.lookupelement("originyfield"), originyval)
		}


	// Responds when the origin x field _ button is pressed

	void originyminusresponse(object self)
		{
			number originyval
			dlggetvalue(self.lookupelement("originyfield"), originyval)

			number stepsize=-1
			if(shiftdown()) stepsize=-5
			if(controldown()) stepsize=-25
			if(optiondown()) stepsize=-50

			originyval=originyval+stepsize
			if(originyval<0) originyval=0
			dlgvalue(self.lookupelement("originyfield"), originyval)
		}

		
	// Applies the distortion methods when Skew or Rotation are applied

	void applydistortion(object self, taggroup tg)
		{
			number skewx
			dlggetvalue(self.lookupelement("skewxfield"), skewx)
			number skewy
			dlggetvalue(self.lookupelement("skewyfield"), skewy)
			
			number rotation
			dlggetvalue(self.lookupelement("rotationfield"), rotation)
			number ovalradius
			dlggetvalue(self.lookupelement("ovalradiusfield"), ovalradius)


			// Find the source image
			
			string pathstring="Atom Colouriser:Image ID"
			string idstring="Source Image"	
			number imageid=self.findimagebyIDstring(pathstring,  idstring)

			if(imageid==0) 
				{
					showalert("The original Source Image may have been closed. Please start again.",2)
					return 
				}

			image sourceimg:=getimagefromid(imageid)
			showimage(sourceimg)
			
			
			// Count the numbe of ovals and place their coordinates in a matrix.
			
			imagedisplay sourcedisp=sourceimg.imagegetimagedisplay(0)
			number noovals=sourcedisp.componentcountchildrenoftype(6)
			
			if(noovals==0)
				{
					showalert("There are no markers on the image. Please start again.",2)
					return
				}
			
			number i, originx, originy, top, left, bottom, right, centrex, centrey
			
			
			// Create a matrix to store the oval coordinates. The first two rows are the x and y
			// coordinates. 

			// Creaete a second matrix in which to these coordinates shifted so that the origin
			// coordinate is (0,0). This ensures this coordinate is the origin point and is not moved
			// by transformations. After transformation, the points are shifted back to put the origin
			// in its original position
			
			image ovalcoords=realimage("", 4, noovals, 2)
			image normovalcoords=realimage("", 4, noovals, 2)
			number redovalfound=0, originposition
			

			// Find the ovals, store their locations in a matrix
			
			for(i=0; i<noovals; i++)
				{
					component thisoval=sourcedisp.componentgetnthchildoftype(6,i)
					number red, green, blue
					thisoval.componentgetforegroundcolor(red, green, blue)
					thisoval.componentgetrect(top, left, bottom, right)
					centrex=((right-left)/2)+left
					centrey=((bottom-top)/2)+top
					
			
					// Identify the origin by it being red, other ovals are yellow
					
					if(red==1 && green==0 && blue==0)
						{
							originx=centrex
							originy=centrey
							redovalfound=1
							originposition=i
						}

					setpixel(ovalcoords, i,0, centrex)
					setpixel(ovalcoords, i, 1, centrey)	
				}


			// Fill in lower two rows of the oval coordinates, by normalising them to centrex and centrey
			
			normovalcoords[0,0,1,noovals]=ovalcoords[0,0,1,noovals]-originx
			normovalcoords[1,0,2,noovals]=ovalcoords[1,0,2,noovals]-originy


			// If the origin oval (red) is not found, bail out
			
			if(redovalfound==0)
				{
					showalert("The red (origin) oval was not found. Please start again.",2)
					return
				}
			
			
			// Now apply the skew x and y distortion via appropriate matrix manipulatiom

			// The matrix is a 2 x 2 array, with top left being 1
			// and the bottom right being 1 and the top right being the x shear factor
			// and bottom left being the y shear factor

			number shearxfactor=skewx/100
			number shearyfactor=skewy/100
			
			image shearmatrix=realimage("", 4, 2,2)
			setpixel(shearmatrix, 0,0, 1)// Diagonal - top left - bottom right
			setpixel(shearmatrix, 1,1,1)
			setpixel(shearmatrix, 1,0,shearxfactor)
			setpixel(shearmatrix, 0,1,shearyfactor)


			// Do the matrix multiplication and then shift the points back to their original origin
			
			image shearedcoords=matrixmultiply(shearmatrix,normovalcoords)
			shearedcoords[0,0,1,noovals]=shearedcoords[0,0,1,noovals]+originx
			shearedcoords[1,0,2,noovals]=shearedcoords[1,0,2,noovals]+originy
			
			
			// Now apply the rotation

			// Rotate by an angle theta

			// We will use an angle of 5 degs

			number angleindegs
			dlggetvalue(self.lookupelement("rotationfield"), angleindegs)
			number theta=angleindegs/(180/pi())


			// shift the points to an origin of zero - rotate - then shift back.
			// this ensures that the origin point does not move during rotation
			
			image prerotatecoords=imageclone(shearedcoords)
			prerotatecoords[0,0,1,noovals]=prerotatecoords[0,0,1,noovals]-originx
			prerotatecoords[1,0,2,noovals]=prerotatecoords[1,0,2,noovals]-originy
			
			
			// The matrix is a 2 x 2 array, the the following values

			image rotatematrix=realimage("", 4, 2,2)
			setpixel(rotatematrix, 0,0, cos(theta))
			setpixel(rotatematrix, 1,0, -sin(theta))
			setpixel(rotatematrix, 0,1,sin(theta))
			setpixel(rotatematrix, 1,1,cos(theta))

			image rotatecoords=matrixmultiply(rotatematrix, prerotatecoords)
			
			
			// now shift everything back to the original origin
			
			rotatecoords[0,0,1,noovals]=rotatecoords[0,0,1,noovals]+originx
			rotatecoords[1,0,2,noovals]=rotatecoords[1,0,2,noovals]+originy


			// Remove all the ovals
			
			for(i=noovals-1; i>-1; i--)
				{
					component thisoval=sourcedisp.componentgetnthchildoftype(6, i)
					thisoval.componentremovefromparent()
				}
			
			string atomvalue
			dlggetvalue(self.lookupelement("atomfield"),atomvalue)	
			// Remove the previously stored oval coordinates
			
			deletenote(sourceimg,  "Atom Colouriser:Points:"+atomvalue)
			setnumbernote(sourceimg,  "Atom Colouriser:Points:"+atomvalue+":Number of Points", noovals)

			
			// Now add the sheared/rotated ovals
			
			for(i=0; i<noovals; i++)
				{
					number ovalx=getpixel(rotatecoords, i, 0)
					number ovaly=getpixel(rotatecoords, i,1)
					
					
					// Save the coordinates into tags on the sourceimg
					
					setnumbernote(sourceimg,  "Atom Colouriser:Points:"+atomvalue+":Oval "+i+":x", ovalx)
					setnumbernote(sourceimg,  "Atom Colouriser:Points:"+atomvalue+":Oval "+i+":y", ovaly)


					// Create the new oval 

					number top=ovaly-ovalradius
					number left=ovalx-ovalradius
					number bottom=ovaly+ovalradius
					number right=ovalx+ovalradius
					component thisoval=newovalannotation(top, left, bottom, right)
					
					
					// Set the origin oval to red - all others to yellow
					
					if(i==originposition) thisoval.componentsetforegroundcolor(1,0,0)
					else thisoval.componentsetforegroundcolor(1,1,0)
					sourcedisp.componentaddchildatend(thisoval)
				}
	}


	// Reponds when the rotation plus button is pressed

	void rotationplusresponse(object self)
		{
			dlgvalue(self.lookupelement("skewxfield"), 0)
			dlgvalue(self.lookupelement("skewyfield"), 0)

			number stepsize=0.1
			if(shiftdown()) stepsize=1
			if(controldown()) stepsize=5
			if(optiondown()) stepsize=10

			dlgvalue(self.lookupelement("rotationfield"), stepsize)
									
					
			// Call the apply distortion function to apply the rotation
			
			taggroup tg
			self.applydistortion(tg)
		}
			
		
	// Reponds when the rotation minus button is pressed

	void rotationminusresponse(object self)
		{
			dlgvalue(self.lookupelement("skewxfield"), 0)
			dlgvalue(self.lookupelement("skewyfield"), 0)


			number stepsize=-0.1
			if(shiftdown()) stepsize=-1
			if(controldown()) stepsize=-5
			if(optiondown()) stepsize=-10

			dlgvalue(self.lookupelement("rotationfield"), stepsize)
									
					
			// Call the apply distortion function to apply the rotation
			
			taggroup tg
			self.applydistortion(tg)
		}


	// Reponds when the grid x spacing plus button is pressed

	void gridxplusresponse(object self)
		{
			number gridsizeval
			dlggetvalue(self.lookupelement("gridxspacingfield"), gridsizeval)

			number stepsize=0.001
			if(shiftdown()) stepsize=0.01
			if(controldown()) stepsize=0.05
			if(optiondown()) stepsize=0.1

			gridsizeval=gridsizeval+stepsize
			if(gridsizeval<0.1) gridsizeval=0.1
			dlgvalue(self.lookupelement("gridxspacingfield"), gridsizeval)
		}
			
		
	// Reponds when the grid x spacing minus button is pressed

	void gridxminusresponse(object self)
		{
			number gridsizeval
			dlggetvalue(self.lookupelement("gridxspacingfield"), gridsizeval)

			number stepsize=-0.001
			if(shiftdown()) stepsize=-0.01
			if(controldown()) stepsize=-0.05
			if(optiondown()) stepsize=-0.1

			gridsizeval=gridsizeval+stepsize
			if(gridsizeval<0.1) gridsizeval=0.1
			dlgvalue(self.lookupelement("gridxspacingfield"), gridsizeval)
		}


	// Reponds when the grid x spacing plus button is pressed

	void gridyplusresponse(object self)
		{
			number gridsizeval
			dlggetvalue(self.lookupelement("gridyspacingfield"), gridsizeval)

			number stepsize=0.001
			if(shiftdown()) stepsize=0.01
			if(controldown()) stepsize=0.05
			if(optiondown()) stepsize=0.1

			gridsizeval=gridsizeval+stepsize
			if(gridsizeval<0.1) gridsizeval=0.1
			dlgvalue(self.lookupelement("gridyspacingfield"), gridsizeval)
		}
		
		
	// Reponds when the grid x spacing minus button is pressed

	void gridyminusresponse(object self)
		{
			number gridsizeval
			dlggetvalue(self.lookupelement("gridyspacingfield"), gridsizeval)

			number stepsize=-0.001
			if(shiftdown()) stepsize=-0.01
			if(controldown()) stepsize=-0.05
			if(optiondown()) stepsize=-0.1

			gridsizeval=gridsizeval+stepsize
			if(gridsizeval<0.1) gridsizeval=0.1
			dlgvalue(self.lookupelement("gridyspacingfield"), gridsizeval)
		}


	// Reponds when the grid plus button is pressed

	void skewxplusresponse(object self)
		{
			dlgvalue(self.lookupelement("skewyfield"), 0)
			dlgvalue(self.lookupelement("rotationfield"), 0)
			
			number stepsize=0.05
			if(shiftdown()) stepsize=0.5
			if(controldown()) stepsize=2.5
			if(optiondown()) stepsize=5
			dlgvalue(self.lookupelement("skewxfield"), stepsize)
								
					
			// Call the apply distortion function to apply the rotation
			
			taggroup tg
			self.applydistortion(tg)
		}
			
		
	// Reponds when the grid minus button is pressed

	void skewxminusresponse(object self)
		{
			dlgvalue(self.lookupelement("skewyfield"), 0)
			dlgvalue(self.lookupelement("rotationfield"), 0)
			
			number stepsize=-0.05
			if(shiftdown()) stepsize=-0.5
			if(controldown()) stepsize=-2.5
			if(optiondown()) stepsize=-5

			dlgvalue(self.lookupelement("skewxfield"), stepsize)
							
					
			// Call the apply distortion function to apply the rotation
			
			taggroup tg
			self.applydistortion(tg)
		}


// Reponds when the Skew Y Plus button is pressed

	void skewyplusresponse(object self)
		{
			dlgvalue(self.lookupelement("skewxfield"), 0)
			dlgvalue(self.lookupelement("rotationfield"), 0)
			
			number stepsize=0.05
			if(shiftdown()) stepsize=0.5
			if(controldown()) stepsize=2.5
			if(optiondown()) stepsize=5

			dlgvalue(self.lookupelement("skewyfield"), stepsize)
									
					
			// Call the apply distortion function to apply the rotation
			
			taggroup tg
			self.applydistortion(tg)
		}
		

	// Reponds when the Skew Y minus button is pressed

	void skewyminusresponse(object self)
		{
			dlgvalue(self.lookupelement("skewxfield"), 0)
			dlgvalue(self.lookupelement("rotationfield"), 0)
			
			number stepsize=-0.05
			if(shiftdown()) stepsize=-0.5
			if(controldown()) stepsize=-2.5
			if(optiondown()) stepsize=-5

			dlgvalue(self.lookupelement("skewyfield"), stepsize)
							
					
			// Call the apply distortion function to apply the rotation
			
			taggroup tg
			self.applydistortion(tg)			
		}

	
	// Responds when the originx or originy fields are changed
	
	void originxfieldchanged(object self, taggroup tg)
		{
			number originxval=tg.dlggetvalue()
			if(originxval<1)
				{
					originxval=1
					tg.dlgvalue(originxval)
				}
			
			self.sourceimageresponse()
		}
		
		
	// Responds when the originx or originy fields are changed
	
	void originyfieldchanged(object self, taggroup tg)
		{
			number originyval=tg.dlggetvalue()
			if(originyval<1)
				{
					originyval=1
					tg.dlgvalue(originyval)
				}
			
			self.sourceimageresponse()
		}


	// Responds when the grid X spacing is changed.

	void gridxsizechanged(object self, taggroup tg)
		{
			number gridspacing
			tg.dlggetvalue(gridspacing)
			if(gridspacing<0.1)
				{
					gridspacing=0.1
					tg.dlgvalue(gridspacing)
				}
			setpersistentnumbernote("Atom Colouriser:Settings:Grid X Spacing (nm)", gridspacing)
			self.sourceimageresponse()
		}


	// Responds when the grid Y spacing is changed.

	void gridysizechanged(object self, taggroup tg)
		{
			number gridspacing
			tg.dlggetvalue(gridspacing)
			if(gridspacing<0.1)
				{
					gridspacing=0.1
					tg.dlgvalue(gridspacing)
				}
			setpersistentnumbernote("Atom Colouriser:Settings:Grid Y Spacing (nm)", gridspacing)
			self.sourceimageresponse()
		}


	// Responds whenn the Radius field is changed

	void ovalradiusfieldchanged(object self, taggroup tg)
		{
			number radius=tg.dlggetvalue()
			if(radius<4)
				{
					radius=4
					tg.dlgvalue(radius)
				}
			setpersistentnumbernote("Atom Colouriser:Settings:Oval Radius (pxl)", radius)
			self.sourceimageresponse()
		}


	// Reponds when the rotation field is changed

	void rotationchanged(object self, taggroup tg)
		{
			// does nothing
		}


	// Reponds when the skewx field is changed

	void skewxchanged(object self, taggroup tg)
		{
			// does nothing
		}


	// Reponds when the skewy field is changed

	void skewychanged(object self, taggroup tg)
		{
			// does nothing
		}


	// Responds when the Grid X field is changed - the number of ovals in X

	void gridxfieldchanged(object self, taggroup tg)
		{
			number gridxval=tg.dlggetvalue()
			if(gridxval<4) 
				{
					gridxval=4
					tg.dlgvalue(gridxval)
				}
				
			setpersistentnumbernote("Atom Colouriser:Settings:Grid Size X", gridxval)
			self.sourceimageresponse()
		}
	// Responds when the Atom  field is changed - the label of Atom 

	void atomfieldchanged(object self, taggroup tg)
		{
			string atomval=tg.dlggetstringvalue()
			if(atomval=="") 
				{
					atomval="_"
					tg.dlgvalue(atomval)
				}
				
			setpersistentstringnote("Atom Colouriser:Settings:Atom", atomval)
			self.sourceimageresponse()
		}


	// Responds when the Grid Y field is changed - the number of ovals in y

	void gridyfieldchanged(object self, taggroup tg)
		{
			number gridyval=tg.dlggetvalue()

			if(gridyval<4) 
				{
					gridyval=4
					tg.dlgvalue(gridyval)
				}

			setpersistentnumbernote("Atom Colouriser:Settings:Grid Size Y", gridyval)
			self.sourceimageresponse()
		}


		// Responds when the Distort button is pressed - unlocks the Distort dialog and invokes the distortion methods

		void distortionbuttonpressed(object self)
			{
				self.setelementisenabled("gridboxgroup", 0)
				self.setelementisenabled("distortboxgroup", 1)
				self.setelementisenabled("lockbutton", 1)

				taggroup tg // dummy taggroup
				self.applydistortion(tg)
			}


//Function to find the integeral intensity of single atom colum 
void dointensity(object self,image selectedroi,image &intensityimage ,number i)
{
// Find the source image
		
		string pathstring="Atom Colouriser:Image ID"
		string idstring="Source Image"	
		number imageid=self.findimagebyIDstring(pathstring,  idstring)

		if(imageid==0) 
			{
				showalert("The original Source Image may have been closed. Please start again.",2)
				return 
			}

		image sourceimg:=getimagefromid(imageid)
		number xsize,ysize,radius,intensity,xgrid,col,row
		getsize(selectedroi,xsize,ysize)
		dlggetvalue(self.lookupelement("gridxfield"), xgrid)
		string atomvalue
		dlggetvalue(self.lookupelement("atomfield"),atomvalue)	
		getnumbernote(sourceimg, "Atom Colouriser:Points:"+atomvalue+":Radius :", radius)
		xsize=xsize/2
		ysize=ysize/2
		image mask:=selectedroi*0
		mask=tert((icol-xsize)**2+(irow-ysize)**2<=radius**2,1,0)
		mask*=selectedroi
		intensity=sum(selectedroi)
		setnumbernote(sourceimg,  "Atom Colouriser:Results:"+atomvalue+":Oval "+i+":intensity", intensity)
		col=mod(i,xgrid)
		row=floor(i/xgrid)
		intensityimage[col,row]=intensity
		
}
//responce when intensitybutton is pess 
void intensitybuttonresponse(object self)
{
	// Find the source image
		
		string pathstring="Atom Colouriser:Image ID"
		string idstring="Source Image"	
		number imageid=self.findimagebyIDstring(pathstring,  idstring)

		if(imageid==0) 
			{
				showalert("The original Source Image may have been closed. Please start again.",2)
				return 
			}

		image sourceimg:=getimagefromid(imageid)
		showimage(sourceimg)
		// Count the numbe of ovals and place their coordinates in a matrix.
		
		imagedisplay sourcedisp=sourceimg.imagegetimagedisplay(0)
		number noovals=sourcedisp.componentcountchildrenoftype(6)
		
		if(noovals==0)
			{
				showalert("There are no circles on the image. Please start again.",2)
				return
			}
		
		number i, originx, originy, top, left, bottom, right, centrex, centrey
		number ovalradius
		dlggetvalue(self.lookupelement("ovalradiusfield"), ovalradius)
		
		string atomvalue
		dlggetvalue(self.lookupelement("atomfield"),atomvalue)	
		
		// Create a matrix to store the oval coordinates. The first two rows are the x and y
		// coordinates. 
		
		image ovalcoords=realimage("", 4, noovals, 2)
		number redovalfound=0, originposition
		
		// Store the coordinates of the ovals into an array
	
		number xgrid, ygrid
		dlggetvalue(self.lookupelement("gridxfield"), xgrid)
		dlggetvalue(self.lookupelement("gridyfield"), ygrid)
		image intensityarray=realimage("", 4, xgrid, ygrid) 
		setname(intensityarray,atomvalue)
		number id=imagegetid(intensityarray)
		setnumbernote(sourceimg,"Atom Colouriser:Results:"+atomvalue+":IntensityImageID",id)
		// Find the ovals, store their locations in a matrix
		
		for(i=0; i<noovals; i++)
			{
				component thisoval=sourcedisp.componentgetnthchildoftype(6,i)
				number red, green, blue
				thisoval.componentgetforegroundcolor(red, green, blue)
				thisoval.componentgetrect(top, left, bottom, right)
				centrex=((right-left)/2)+left
				centrey=((bottom-top)/2)+top
				
		
				// Identify the origin by it being red, other ovals are yellow
				
				if(red==1 && green==0 && blue==0)
					{
						originx=centrex
						originy=centrey
						redovalfound=1
						originposition=i
					}

				setpixel(ovalcoords, i,0, centrex)
				setpixel(ovalcoords, i, 1, centrey)	
			}


		// If the origin oval (red) is not found, bail out
		
		if(redovalfound==0)
			{
				showalert("The red (origin) oval was not found. Please start again.",2)
				return
			}
		
		// Now refine the position of the ovals using a centre of gravity approach
		
		number cogiterations

		number j, xsize, ysize
		getsize(sourceimg, xsize, ysize)
		number errorcounter



		
		
		// Now work through the ovals refining their position
		
		for(j=0; j<noovals; j++)
			{
				// Get the jth oval
				
				component thisoval=sourcedisp.componentgetnthchildoftype(6,j)
				number top, left, bottom, right
				thisoval.componentgetrect(top, left, bottom, right)

				number intensity, roit, roil, roir, roib
				roit=top
				roil=left
				roib=bottom
				roir=right
		
		
				// Cog iteration loop
				
						image myroi
						if(roit<0) roit=0
						if(roil<0) roil=0
						if(roib>ysize) roib=ysize
						if(roir>xsize) roir=xsize
						try
							{
								myroi=sourceimg[roit, roil, roib, roir]
								self.dointensity(myroi,intensityarray,j)
							}
						catch
							{
								errorcounter=errorcounter+1
								break
							}
							

	


			showimage(intensityarray)
					

			number thisred, thisgreen, thisblue
			thisoval.componentgetforegroundcolor(thisred, thisgreen, thisblue)
			
			
			// Only change the yellow ones. The red is the origina and must be kept red to id it
			
			if(thisred==1 && thisgreen==1 && thisblue==0) thisoval.componentsetforegroundcolor(0,1,0)
		}

	updateimage(sourceimg) 


	// if errors occur during the refinement of the oval positions.
					
	if(errorcounter>0)
		{
			showalert(errorcounter+" errors were encountered during refinement. Ensure that no ovals lie outside the bounds of the image.",2)
		}



		
		
		
		
		//
		// Check that no ovals have been deleted

	  number expectedovals=xgrid*ygrid
	  if(noovals!=expectedovals)
		{
			showalert(expectedovals+" ovals were expected. "+noovals+" were found. Please start again.",2)
			return
		}

}








	// Function to find the centre of gravity of the passed in image (central roi). The coordinates of the centre are returned
	// via the cogs and cogy variables, which are passed in by reference

	void findcentreofgravity(object self, image centralroi, number &cogx, number &cogy)
		{
			// For information on this calculation see John Russ - Image Processing Handbook, 2nd Ed. p489

				number xpos, ypos, maxval, imgsum, xsize, ysize, i
				image tempimg

				maxval=max(centralroi, xpos, ypos)
				imgsum=sum(centralroi)

				getsize(centralroi, xsize, ysize)

				// Traps for a blank image
				
				if(imgsum==0) // the image is blank so set the CoGs to the centre of the image and return
					{
						cogx=(xsize-1)/2 //minus one since the centre of a 2 x 2 image is 0.5,0.5 - 0,0 is a position
						cogy=(ysize-1)/2 //minus one since the centre of a 2 x 2 image is 0.5,0.5 - 0,0 is a position
						return
					}


				// Collapse the image down onto the x axis

				image xproj=realimage("",4,xsize,1)
				xproj[icol,0]+=centralroi


				// Rotate the passed in image through 90 degs so that rows become columns
				// Then collapse that image down onto the x axis (was the y axis)
				
				tempimg=realimage("", 4, ysize, xsize)
				tempimg=centralroi[irow,icol]
				image yproj=realimage("",4,ysize, 1)
				yproj[icol,0]+=tempimg 

				yproj=yproj*(icol+1) // NB the +1 ensures that for the left column and top row, where
				xproj=xproj*(icol+1) // icol=0 are included in the weighting. 1 must be subtracted from
									// the final position to compensate for this shift
				cogx=sum(xproj)
				cogy=sum(yproj)
				cogx=(cogx/imgsum)-1 // compensation for the above +1 to deal with icol=0
				cogy=(cogy/imgsum)-1
	}

// Responds when Refine button is pressed. 

void refineresponse(object self)
	{
		// Find the source image
		
		string pathstring="Atom Colouriser:Image ID"
		string idstring="Source Image"	
		number imageid=self.findimagebyIDstring(pathstring,  idstring)
		
		if(imageid==0) 
			{
				showalert("The original Source Image may have been closed. Please start again.",2)
				return 
			}

		image sourceimg:=getimagefromid(imageid)
		showimage(sourceimg)
		string atomvalue
		dlggetvalue(self.lookupelement("atomfield"),atomvalue)
		
		// Count the numbe of ovals and place their coordinates in a matrix.
		
		imagedisplay sourcedisp=sourceimg.imagegetimagedisplay(0)
		number noovals=sourcedisp.componentcountchildrenoftype(6)
		
		if(noovals==0)
			{
				showalert("There are no circles on the image. Please start again.",2)
				return
			}
		
		number i, originx, originy, top, left, bottom, right, centrex, centrey
		number ovalradius
		dlggetvalue(self.lookupelement("ovalradiusfield"), ovalradius)
		
		
		// Create a matrix to store the oval coordinates. The first two rows are the x and y
		// coordinates. 
		
		image ovalcoords=realimage("", 4, noovals, 2)
		number redovalfound=0, originposition
		

		// Find the ovals, store their locations in a matrix
		
		for(i=0; i<noovals; i++)
			{
				component thisoval=sourcedisp.componentgetnthchildoftype(6,i)
				number red, green, blue
				thisoval.componentgetforegroundcolor(red, green, blue)
				thisoval.componentgetrect(top, left, bottom, right)
				centrex=((right-left)/2)+left
				centrey=((bottom-top)/2)+top
				
		
				// Identify the origin by it being red, other ovals are yellow
				
				if(red==1 && green==0 && blue==0)
					{
						originx=centrex
						originy=centrey
						redovalfound=1
						originposition=i
					}

				setpixel(ovalcoords, i,0, centrex)
				setpixel(ovalcoords, i, 1, centrey)	
			}


		// If the origin oval (red) is not found, bail out
		
		if(redovalfound==0)
			{
				showalert("The red (origin) oval was not found. Please start again.",2)
				return
			}
		

		// Now refine the position of the ovals using a centre of gravity approach
		
		number cogiterations
		getpersistentnumbernote("Atom Colouriser:Settings:Centre of Gravity Iterations", cogiterations)
		number j, xsize, ysize
		getsize(sourceimg, xsize, ysize)
		number errorcounter


		// Delete the previous oval positions
		
		deletenote(sourceimg,    "Atom Colouriser:Results:"+atomvalue)
		setnumbernote(sourceimg, "Atom Colouriser:Results:"+atomvalue+":Number of Points", noovals)
		
		
		// Now work through the ovals refining their position
		
		for(j=0; j<noovals; j++)
			{
				// Get the jth oval
				
				component thisoval=sourcedisp.componentgetnthchildoftype(6,j)
				number top, left, bottom, right
				thisoval.componentgetrect(top, left, bottom, right)

				number cogx, cogy, roit, roil, roir, roib
				roit=top
				roil=left
				roib=bottom
				roir=right
		
		
				// Cog iteration loop
				
				for(i=0; i<cogiterations; i++)
					{
						image myroi
						if(roit<0) roit=0
						if(roil<0) roil=0
						if(roib>ysize) roib=ysize
						if(roir>xsize) roir=xsize

						try
							{
								myroi=sourceimg[roit, roil, roib, roir]
								self.findcentreofgravity(myroi, cogx, cogy)
							}
						catch
							{
								errorcounter=errorcounter+1
								break
							}
							
						cogy=cogy+roit
						cogx=cogx+roil
						
						
						// Save the refined position in tags on the image
						
						setnumbernote(sourceimg, "Atom Colouriser:Results:"+atomvalue+":Oval "+j+":x", cogx)
						setnumbernote(sourceimg, "Atom Colouriser:Results:"+atomvalue+":Oval "+j+":y", cogy)

 
						// Keep the ovals within the bounds of the image
						
						roit=cogy-ovalradius
						roil=cogx-ovalradius
						roib=cogy+ovalradius
						roir=cogx+ovalradius
						
						if(roit<0) roit=0
						if(roil<0) roil=0
						if(roib>ysize) roib=ysize
						if(roir>xsize) roir=xsize
					}
					
					
			// Update the colour of yellow ovals to green when they are refined
			
			thisoval.componentsetrect(cogy-ovalradius, cogx-ovalradius, cogy+ovalradius, cogx+ovalradius)
			number thisred, thisgreen, thisblue
			thisoval.componentgetforegroundcolor(thisred, thisgreen, thisblue)
			
			
			// Only change the yellow ones. The red is the origina and must be kept red to id it
			
			if(thisred==1 && thisgreen==1 && thisblue==0) thisoval.componentsetforegroundcolor(0,1,0)
		}
	setnumbernote(sourceimg, "Atom Colouriser:Points:"+atomvalue+":Radius",ovalradius)
	updateimage(sourceimg) 


	// if errors occur during the refinement of the oval positions.
					
	if(errorcounter>0)
		{
			showalert(errorcounter+" errors were encountered during refinement. Ensure that no ovals lie outside the bounds of the image.",2)
		}


	// Store the coordinates of the ovals into an array
	
	number xgrid, ygrid
	dlggetvalue(self.lookupelement("gridxfield"), xgrid)
	dlggetvalue(self.lookupelement("gridyfield"), ygrid)
	image polynomialarray=realimage("", 4, xgrid*2, ygrid) // note x 2 because x and y coordinates are saved as pairs.
	
	
	// Check that no ovals have been deleted
	/*
	number expectedovals=xgrid*ygrid
	if(noovals!=expectedovals)
		{
			showalert(expectedovals+" ovals were expected. "+noovals+" were found. Please start again.",2)
			return
		}
	*/
	}
	
	
// Responds when the Col. Angle field value is changed




void columnanglefieldchanged(object self, taggroup tg)
	{
		number columnangle=tg.dlggetvalue()
		if(columnangle<-45) columnangle=-45
		if(columnangle>45) columnangle=45
		tg.dlgvalue(columnangle)
		setpersistentnumbernote("Atom Colouriser:Settings:Column Angle (degs", columnangle)
		self.sourceimageresponse()
	}
		

// Responds when the Clear button is pressed. Restores the original image by removing ovals and tags.
// If ALT is held down all images created by this script are deleted without warning.

void clearresponse(object self)
	{
		// Reset the dialog
		
		self.setelementisenabled("gridboxgroup",0)
		self.setelementisenabled("distortboxgroup",0)
		self.setelementisenabled("allcolourgroup",0)
		self.setelementisenabled("maskbutton", 0)	
		self.setelementisenabled("sourceimagebutton", 1)
		
		
		// Record if the ALT key is held down
		
		number Altdown
		if(optiondown()) altdown=1
	
	
		// Find the source image
		
		string pathstring="Atom Colouriser:Image ID"
		string idstring="Source Image"	
		number imageid=self.findimagebyIDstring(pathstring,  idstring)
		
		
		// If the image exists
		
		if(imageid!=0)
			{
				try
					{
						// Find the source image and remove any ovals
						
						image sourceimg:=getimagefromid(imageid)
						showimage(sourceimg)
						
						imagedisplay sourcedisp=sourceimg.imagegetimagedisplay(0)
						number noovals=sourcedisp.componentcountchildrenoftype(6)
						number i
						
						for(i=noovals-1; i>-1; i--)
							{
								component thisoval=sourcedisp.componentgetnthchildoftype(6,i)
								thisoval.componentremovefromparent()
							}
						deletenote(sourceimg, "Atom Colouriser")		
					}
				catch break
		}
		
		
		// Set the Skew X and Y fields to zero
		
		dlgvalue(self.lookupelement("skewxfield"), 0)
		dlgvalue(self.lookupelement("skewyfield"), 0)
		
		
		// If ALT is not held down end here.
		
		if(altdown==0) return

		
		// If ALT is held down - delete the Undistort, Magnitude and Vector images
				
				
		// Find the Mask image
		
		pathstring="Atom Colouriser:Image ID"
		idstring="Mask Image"	
		try
			{
				imageid=self.findimagebyIDstring(pathstring,  idstring)
				image undistortimg:=getimagefromid(imageid)
				if(imageid!=0) deleteimage(undistortimg)
			}
		catch
			{
				break
			}

	}


	// Responds when the Lock button is pressed by  locking the position of any circles on the image

	void lockbuttonresponse(object self)
		{
			// Find the Source image
			
			self.setelementisenabled("lockbutton", 0)
			string pathstring="Atom Colouriser:Image ID"
			string idstring="Source Image"	

			number imageid
			try
				{
					imageid=self.findimagebyIDstring(pathstring,  idstring)
					
					
					// If the image is not found and the lock was turned on, turn it off
					
					if(imageid==0)
						{
							self.setelementisenabled("lockbutton", 1)
							return
						}
				}
			catch
				{
					self.setelementisenabled("lockbutton", 1)
					break
				}


			// Count the number of oval annotations and set them to be either locked or unlocked
							
			image sourceimg:=getimagefromid(imageid)
			imagedisplay sourcedisp=sourceimg.imagegetimagedisplay(0)
			
			number noovals=sourcedisp.componentcountchildrenoftype(6)
			number i, setmovable
			
			for(i=noovals-1; i>-1; i--)
				{
					component thisoval=sourcedisp.componentgetnthchildoftype(6,i)
					setmovable=0
					thisoval.componentsetmovable(setmovable)
				}
			self.setelementisenabled("allcolourgroup",1)
			self.setelementisenabled("maskbutton",1)
			self.setelementisenabled("distortboxgroup", 0)
		}




// Responds when the ? button is pressed - puts instructions in the Output window

void helpbuttonpressed(object self)
	{
		result("\n\nAtom Colouriser:")
		result("\n\nThe purpose of this script is to create an array of coloured circles to delineate atomic sites in")
		result("\nan experimental high resolution HAADF image. This may be to highlight an interface or some kind of defect.")
		result("\nThe script works by creating a geometric array of circles which roughly matches the experimental lattice.")
		result("\nThat array is then stretched, skewed and rotated so that it comes into reasonably close registry with the")		
		result("\nthe experimental lattice. A centre of gravity routine is used to centre each circle on its atomic column")
		result("\nprecisely. Finally, this array of circles is then locked and by selecting circles they can be individually")
		result("\ncoloured - either in outline or fill. The coloured overlay on the experimental image may be used as is.")
		result("\nAlternatively, it can be extracted as a seperate mask image on a black background.")
		result("\n\n1. Have a high resolution HAADF image front-most. The image must be spatially calibrated.")
		result("\n2. Select the image with the Get Image button. An array of circles is drawn on the image")
		result("\n	according to the parameters specified in the Define Ideal Lattice dialog section.")
		result("\n	Grid X and Y specify the number of columns and rows of circles.")
		result("\n	Radius specifies the radius of each circle. This should be large enough to fully encompass the atomic")
		result("\n	column, but not so large that it overlaps with other circles or atomic columns.")
		result("\n	X and Y Space specifies the spacing between the circles. These should be adjusted to get a good match")
		result("\n	with the experimental lattice.")
		result("\n	Origin X and Y specifies the position of the Origin of the lattice of circles. This is shown as a red circle.")
		result("\n	This origin circle would normally be fitted to an atomic column near the top left corner of the image.")
		result("\n	Col. Angle. This is the angle the columns of atoms make with respect to vertical.")
		result("\n	Hold down Control or Shift or Alt when clicking on the + or - buttons in this script to change the step size.") 
		result("\n3. Adjust the above parameters so that your lattice of circles approximately matches your experimental lattice.")
		result("\n	Avoid fitting atomic colum which are partially off the edge of the image - the fitting routine will not")
		result("\n	fit these accurately.")
		result("\n4. Fitting button: Press the Fitting button. This unlocks the Fit Experimental Lattice section.")
		result("\n	This section allows your geometric lattice to be skewed in X and Y and rotated, to improve the fit")
		result("\n	of the two lattices. Adjust the parameters so that a good fit is obtained. It does not have to be perfect.")
		result("\n	Provided that more than about half of the atomic column is inside the circle, the fitting routine should do the rest.")
		result("\n5. Refine button: This will do an iterative centre of gravity fit of each circle on its respective atomic column.")
		result("\n	Refined circles turn from yellow to green (except the Origin circle). You can press the Refine button several")
		result("\n	times to further improve the fit (if necessary).")
		
		result("\n6. Manually positioning/adding circles: You can individually select and delete any circles by clicking on one")
		result("\n	(green handles appear) and selecting Delete.")
		result("\n	You may manually copy a circle (Control + C) and paste it (Control + V) to manually add")
		result("\n	and position circles onto atomic columns which lie outside your regular array.")
		result("\n	You can manually reposition refined circles by clicking on a circle to highlight then pressing")
		result("\n	any of the keyboard arrow keys to move it Pressing Refine will refine the positions the newly added circles.")
		
		result("\n7. Lock button: Once you are satisfied with the position of all the circles press the Lock button.")
		result("\n	This will lock the position of all the circles to prevent them from being accidentally moved while selecting them.")
		result("\n	It also unlocks the Colourise section.")
		
		result("\n8. Select the colours you wish to use by clicking on the square coloured buttons - a colour picker opens.")
		result("\n9. There are three preset colours - select which is to be used by selecting the 1, 2, 3 Radio button next to its respective colour.")
		result("\n10. Select whether you wish to colour the circle as an outline (Line) or filled (Fill).")
		result("\n11 Select the circles to be coloured. If you wish to colour them all the same, click on the image to have it front-most.")
		result("\n	Then hit Control + a to select all the circles.")
		result("\n	Then hit the Colourise button to colour them.")
		result("\n	To select individual circles, click on them to select them (green corner handles appear) then press the Colourise button.")
		result("\n	To select multiple circles keep SHIFT held down while clicking on circles.")
		result("\n	To select a contigous block of circles click and drag across them. All circles fully encompassed the rectangle")
		result("\n	you describe will be selected.")
		result("\n12. To save the image in a colour format suitable for a publication, choose File/Save Display As . .  and ensure")
		result("\n	that the 'Save as Greyscale' option is not selected. TIFF is the best format.")
		result("\n13. Extract Mask: Press this button to create a Mask image which is the same size as your annotated image but")
		result("\n	contains a black bacground along with the array of coloured circles. You may decide to use this juxtaposed")
		result("\n 	with your high resolution image, instead of having the mask of circles overlaid on the experimental image.")
		
		result("\nTools button: This shows the default settings for the script. Nearly all of these are set/changed directly via the script")
		result("\n	However, three parameters can only be changed via the Tools dialog : Centre of Gravity Iterations")
		result("\n	- how many times the Refine routine iterates; Image Display Width - the default size at which the script")
		result("\n	displays images (in pixels); and Origin Inset - how far inset from the top left corner of the image (as a %)")
		result("\n	does the origin appear initially.")
		result("\nClear button: Pressing Clear will remove all annotations from the experimental image. If the ALT key is held down")
		result("\n	when Clear is pressed any images which this script has created (ie Mask images) will be deleted also.")

				
		showalert("        Instructions have been printed in the Output window.\n\n(To display the Output window: Window/Show Output Window).",2)
	}


// Responds when the Zero Position radio is changed - saves the settings to a tag

void zeropositionradiochanged(object self, taggroup tg)
	{
		number radioval=tg.dlggetvalue()
		setpersistentnumbernote("Atom Colouriser:Settings:Origin Radio Setting (0-1)", radioval)
	}


// Reponds when the tools button is pressed - shows the global info

void toolsbuttonpressed(object self)
	{
		taggroup ptags=getpersistenttaggroup()
		taggroup distorttags
		ptags.taggroupgettagastaggroup("Atom Colouriser:Settings", distorttags)
		distorttags.taggroupopenbrowserwindow(0)
	}


// Save the dialog position to the global tags

void abouttoclosedocument(object self)
	{
		documentwindow dialogwin=self.getframewindow()
		number wintop, winleft
		dialogwin.windowgetframeposition(winleft, wintop)
		setpersistentnumbernote("Atom Colouriser:Settings:Dialog Top", wintop)
		setpersistentnumbernote("Atom Colouriser:Settings:Dialog Left", winleft)
	}



	// When any colour button is pressed, this identifies which button is pressed.
	// The use of dual state buttons means that when they are pressed they
	// latch on. This finds the latched one, identifies it and resets it

	void colourbuttonresponse(object self)
		{
			number i
			number buttonnumber
			taggroup tg
			
			// Go through all the colour buttons until the one which is on is found - reset it.
			
			for(i=1; i<4; i++)
				{
					try
						{
							tg=self.lookupelement("colourbutton"+i)
							if(tg.dlggetvalue()) // found the button that is on - so reset it
								{
									tg.dlgbevelbuttonOn(0)
									buttonnumber=i	
									break
								}
						}
					catch break
					
					
				}


			// Set the subdialog title and at no field and then source the saved colour 
			// avoiding the use of black RGB(0,0,0) as this would prevent the background
			// of the button being coloured as the letters are black and the background
			// is set on the basis of it not being black
		
			SubDialogObject.display("Colour "+i).WindowSetFramePosition(600, 100 )
			dlgtitle(subdialogObject.lookupelement("colourlabel"), "Colour : "+i)
			
			
			// Look up the colour value saved for the element in the global info
			// If none is set, then set it to defaultgrey - a global variable at
			// the start of the script
			
			rgbnumber colourvalue, defaultcolour
			number red, green, blue

			getpersistentnumbernote("Atom Colouriser:Settings:Button "+i+" Colour (Red)", red)
			getpersistentnumbernote("Atom Colouriser:Settings:Button "+i+" Colour (Green)", green)
			getpersistentnumbernote("Atom Colouriser:Settings:Button "+i+" Colour (Blue)", blue)

							
			dlgvalue(subdialogobject.lookupelement("rfield"), red)
			dlgvalue(subdialogobject.lookupelement("gfield"), green)
			dlgvalue(subdialogobject.lookupelement("bfield"), blue)
		}
		
		
// Responds when the Colourise button is pressed
	
void colouriseresponse(object self)
	{
		// Find the Source image
		
		string pathstring="Atom Colouriser:Image ID"
		string idstring="Source Image"	


		// Source the front-most image
		
		number imageid=self.findimagebyIDstring(pathstring,  idstring)
		if(imageid==0) return
				

		// Get the radio identifying which colour to use
		
		number colourradioval
		dlggetvalue(self.lookupelement("colourradio"), colourradioval)
		colourradioval=colourradioval+1
		
		
		// Source the corresponding colour
		
		number red, green, blue
		getpersistentnumbernote("Atom Colouriser:Settings:Button "+colourradioval+" Colour (Red)", red)
		getpersistentnumbernote("Atom Colouriser:Settings:Button "+colourradioval+" Colour (Green)", green)
		getpersistentnumbernote("Atom Colouriser:Settings:Button "+colourradioval+" Colour (Blue)", blue)

		
		// Get the radio to decide whether to fill or outline the ovals
		
		number lineorfill
		dlggetvalue(self.lookupelement("lineorfillradio"), lineorfill)
		
		
		// Work through the ovals setting the selected ones to the colour and fill specified
								
		image sourceimg:=getimagefromid(imageid)
		imagedisplay sourcedisp=sourceimg.imagegetimagedisplay(0)
				
		number noovals=sourcedisp.componentcountchildrenoftype(6)
		number i, setmovable, numberselected=0
				
		for(i=noovals-1; i>-1; i--)
			{
				component thisoval=sourcedisp.componentgetnthchildoftype(6,i)
						
				if(thisoval.componentisselected())
					{
						numberselected=numberselected+1
						if(lineorfill==1) thisoval.componentsetfillmode(1)
						else thisoval.componentsetfillmode(2)
						thisoval.componentsetforegroundcolor(red/255, green/255, blue/255)
					}
			}
			
		if(numberselected==0) showalert("Ensure one or more circles are selected for colouring.",2)
	}
		
		
// Responds when the Extract Mask button is pressed.

void maskbuttonresponse(object self)
	{
		// Find the Source image
		
		string pathstring="Atom Colouriser:Image ID"
		string idstring="Source Image"	


		// Source the front-most image
		
		number imageid=self.findimagebyIDstring(pathstring,  idstring)
		if(imageid==0) return
		image sourceimg:=getimagefromid(imageid)
		
		
		// Get the image coordinates to display the mask to its right
		
		number top, left, bottom, right
		showimage(sourceimg)
		documentwindow sourcewin=getdocumentwindow(0)
		sourcewin.windowgetframebounds(top, left, bottom, right)
		string sourcename=getname(sourceimg)
		
		
		// If the image is close to the right hand edge, display the image just
		// offset fromt he top left corner
		
		number screenwidth, screenheight, imagewidth=right-left
		getscreensize(screenwidth, screenheight)
		if(right>(0.8*screenwidth)) 
			{
				right=left+30
				top=top+30
			}
		
		
		// Get the ovals and copy them to a mask image
		
		imagedisplay sourcedisp=sourceimg.imagegetimagedisplay(0)
		number noovals=sourcedisp.componentcountchildrenoftype(6)
		if(noovals==0) return
		
		image mask=imageclone(sourceimg)*0
		showimage(mask)
		documentwindow maskwin=getdocumentwindow(0)
		maskwin.windowsetframebounds(top, right, bottom, right+imagewidth)
		setname(mask, "Mask of "+sourcename)
		setstringnote(mask, "Atom Colouriser:Image ID", "Mask Image")
		imagedisplay maskdisp=mask.imagegetimagedisplay(0)
		
		number i
		taggroup ovaltags=newtaggroup()
		component thisoval
		
		for(i=noovals-1; i>-1; i--)
			{
				thisoval=sourcedisp.componentgetnthchildoftype(6,i)
				thisoval.componentexternalizeproperties(ovaltags)
				component newoval=newovalannotation(0,0,1,1)
				newoval.componentinternalizeproperties(ovaltags)
				maskdisp.componentaddchildatend(newoval)
			}
	}


// Responds when the colour radio is changed - writes the value to tags

void colourradiochanged(object self, taggroup tg)
	{
		number colourradioval=tg.dlggetvalue()
		setpersistentnumbernote("Atom Colouriser:Settings:Colour Radio (0-2)", colourradioval)
	}
	

// Responds when the Line or Fill radio is changed - writes the value to tags

void lineorfillradiochanged(object self, taggroup tg)
	{
		number lineorfillradioval=tg.dlggetvalue()
		setpersistentnumbernote("Atom Colouriser:Settings:Line or Fill Radio (0-1)", lineorfillradioval)
	}
		
		

// this function creates a taggroup containing the dialog elements:
// a box within which a simple button is present.

void MakeDialog(object self)
	{

		TagGroup dialog_items;	
		TagGroup dialog = DLGCreateDialog("Distortion Correction", dialog_items)


		// Creates a box in the dialog which surrounds the button

		taggroup box_items
		taggroup box=dlgcreatebox("  Image  ", box_items)
		box.dlgexternalpadding(3,3)
		box.dlginternalpadding(18,10)


		// Creates the various dialog elements

		TagGroup SourceImageButton = DLGCreatePushButton("Get Image", "sourceimageresponse").dlgidentifier("sourceimagebutton")
		SourceImageButton.dlgexternalpadding(5,0)
		taggroup ClearButton=dlgcreatepushbutton("Clear*", "clearresponse").dlgidentifier("clearbutton").dlgexternalpadding(5,0)
		
		number gridxvalue
		getpersistentnumbernote("Atom Colouriser:Settings:Grid Size X", gridxvalue)

		taggroup label=dlgcreatelabel("Grid_X")
		taggroup gridxfield=dlgcreateintegerfield(gridxvalue,4).dlgidentifier("gridxfield").dlgchangedmethod("gridxfieldchanged")
		taggroup gridxgroup=dlggroupitems(label, gridxfield).dlgtablelayout(1,2,0)
		
		
		number gridyvalue
		getpersistentnumbernote("Atom Colouriser:Settings:Grid Size Y", gridyvalue)

		label=dlgcreatelabel("Grid_Y")
		taggroup gridyfield=dlgcreateintegerfield(gridyvalue,4).dlgidentifier("gridyfield").dlgchangedmethod("gridyfieldchanged")
		taggroup gridygroup=dlggroupitems(label, gridyfield).dlgtablelayout(1,2,0)
		
		string atomvalue
		getpersistentstringnote("Atom Colouriser:Settings:Atom", atomvalue)

		label=dlgcreatelabel("Atom")
		taggroup atomfield=dlgcreatestringfield(atomvalue,4).dlgidentifier("atomfield").dlgchangedmethod("atomfieldchanged")
		taggroup atomgroup=dlggroupitems(label, atomfield).dlgtablelayout(1,2,0)
		
		number ovalradius
		getpersistentnumbernote("Atom Colouriser:Settings:Oval Radius (pxl)", ovalradius)
		label=dlgcreatelabel("Radius/pxl")
		taggroup radiusfield=dlgcreateintegerfield(ovalradius, 4).dlgidentifier("ovalradiusfield").dlgchangedmethod("ovalradiusfieldchanged")

		taggroup radiusgroup=dlggroupitems(label, radiusfield).dlgtablelayout(1,2,0)
		taggroup gridsizeandradiusgroup=dlggroupitems(gridxgroup, gridygroup, radiusgroup,atomgroup).dlgtablelayout(2,2,0)

		taggroup distortionbutton=dlgcreatepushbutton("Fitting", "distortionbuttonpressed").dlgidentifier("distortionbutton").dlgexternalpadding(0,5)
	
		taggroup originxfield=dlgcreateintegerfield(0,6).dlgidentifier("originxfield").dlgchangedmethod("originxfieldchanged")
		
		taggroup originyfield=dlgcreateintegerfield(0,6).dlgidentifier("originyfield").dlgchangedmethod("originyfieldchanged")

		taggroup originxplusbutton=dlgcreatepushbutton("+","originxplusresponse").dlgidentifier("originxplusbutton")
		taggroup originxminusbutton=dlgcreatepushbutton("-","originxminusresponse").dlgidentifier("originxminusbutton").dlginternalpadding(3,0)
		taggroup originyplusbutton=dlgcreatepushbutton("+","originyplusresponse").dlgidentifier("originyplusbutton")
		taggroup originyminusbutton=dlgcreatepushbutton("-","originyminusresponse").dlgidentifier("originyminusbutton").dlginternalpadding(3,0)
		
		taggroup originxbuttongroup=dlggroupitems(originxplusbutton, originxminusbutton).dlgtablelayout(2,1,0)
		taggroup originybuttongroup=dlggroupitems(originyplusbutton, originyminusbutton).dlgtablelayout(2,1,0)
		
		label=dlgcreatelabel("Origin_X / pxl")
		taggroup originxgroup=dlggroupitems(label, originxfield, originxbuttongroup).dlgtablelayout(1,3,0)
				
		label=dlgcreatelabel("Origin_Y / pxl")
		taggroup originygroup=dlggroupitems(label, originyfield, originybuttongroup).dlgtablelayout(1,3,0)
		taggroup originfieldsgroup=dlggroupitems(originxgroup, originygroup).dlgtablelayout(2,1,0)
		
		label=dlgcreatelabel("Col._Angle/deg")
		number columnangle
		getpersistentnumbernote("Atom Colouriser:Settings:Column Angle (degs", columnangle)
		taggroup columnanglefield=dlgcreaterealfield(columnangle, 8, 4).dlgidentifier("columnanglefield").dlgchangedmethod("columnanglefieldchanged")
		taggroup columnanglegroup=dlggroupitems(label, columnanglefield).dlgtablelayout(1,2,0)

		label=dlgcreatelabel("X_Space/nm")
		number gridxspacing
		getpersistentnumbernote("Atom Colouriser:Settings:Grid X Spacing (nm)", gridxspacing)

		taggroup gridxsizefield=dlgcreaterealfield(gridxspacing, 8, 4,"gridxsizechanged").dlgidentifier("gridxspacingfield")
		taggroup gridxfieldgroup=dlggroupitems(label, gridxsizefield).dlgtablelayout(1,2,0)
		taggroup gridxplusbutton=dlgcreatepushbutton("+","gridxplusresponse").dlgidentifier("gridxplusbutton")
		taggroup gridxminusbutton=dlgcreatepushbutton("-","gridxminusresponse").dlgidentifier("gridxminusbutton").dlginternalpadding(3,0)
		
		taggroup gridxbuttongroup=dlggroupitems(gridxplusbutton, gridxminusbutton).dlgtablelayout(2,1,0)
		taggroup gridxspacinggroup=dlggroupitems(gridxfieldgroup, gridxbuttongroup).dlgtablelayout(1,2,0)
	
		label=dlgcreatelabel("Y_Space/nm")
		number gridyspacing
		getpersistentnumbernote("Atom Colouriser:Settings:Grid Y Spacing (nm)", gridyspacing)

		taggroup gridysizefield=dlgcreaterealfield(gridyspacing, 8, 4,"gridysizechanged").dlgidentifier("gridyspacingfield")
		taggroup gridyfieldgroup=dlggroupitems(label, gridysizefield).dlgtablelayout(1,2,0)
		taggroup gridyplusbutton=dlgcreatepushbutton("+","gridyplusresponse").dlgidentifier("gridyplusbutton")
		taggroup gridyminusbutton=dlgcreatepushbutton("-","gridyminusresponse").dlgidentifier("gridminusbutton").dlginternalpadding(3,0)
		
		taggroup gridybuttongroup=dlggroupitems(gridyplusbutton, gridyminusbutton).dlgtablelayout(2,1,0)
		taggroup gridyspacinggroup=dlggroupitems(gridyfieldgroup, gridybuttongroup).dlgtablelayout(1,2,0)

		
		label=dlgcreatelabel("Rotation/deg")
		taggroup rotationfield=dlgcreaterealfield(0, 8, 2,"rotationchanged").dlgidentifier("rotationfield").dlgenabled(0)
		taggroup rotationfieldgroup=dlggroupitems(label, rotationfield).dlgtablelayout(1,2,0)
		taggroup rotationplusbutton=dlgcreatepushbutton("+","rotationplusresponse").dlgidentifier("rotationplusbutton")
		taggroup rotationminusbutton=dlgcreatepushbutton("-","rotationminusresponse").dlgidentifier("rotationminusbutton").dlginternalpadding(3,0)
		
		taggroup rotationbuttongroup=dlggroupitems(rotationplusbutton, rotationminusbutton).dlgtablelayout(2,1,0)
		taggroup rotationgroup=dlggroupitems(rotationfieldgroup, rotationbuttongroup).dlgtablelayout(1,2,0)
		
		taggroup refinebutton=dlgcreatepushbutton("Refine", "refineresponse").dlgidentifier("refinebutton").dlgexternalpadding(0,0)
		
		taggroup intensitybutton=dlgcreatepushbutton("Intensity", "intensitybuttonresponse").dlgidentifier("intensitybutton").dlgexternalpadding(0,0)
		
		taggroup lockatomsbutton=dlgcreatepushbutton("Lock", "lockbuttonresponse").dlgidentifier("lockbutton").dlginternalpadding(5,0)
		taggroup refineandlockgroup=dlggroupitems(refinebutton, lockatomsbutton,intensitybutton).dlgtablelayout(1,3,0).dlgexternalpadding(0,10)

		taggroup rotationandrefinelockgroup=dlggroupitems(rotationgroup, refineandlockgroup).dlgtablelayout(2,1,0)
		taggroup gridspacinggroup=dlggroupitems(gridxspacinggroup, gridyspacinggroup).dlgtablelayout(2,1,0)
		
		label=dlgcreatelabel("Skew_X/%")
		taggroup skewxfield=dlgcreaterealfield(0, 8, 4,"skewxchanged").dlgidentifier("skewxfield").dlgenabled(0)
		taggroup skewxfieldgroup=dlggroupitems(label, skewxfield).dlgtablelayout(1,2,0)
		taggroup skewxplusbutton=dlgcreatepushbutton("+","skewxplusresponse").dlgidentifier("skewxplusbutton")
		taggroup skewxminusbutton=dlgcreatepushbutton("-","skewxminusresponse").dlgidentifier("skewxminusbutton").dlginternalpadding(3,0)
		
		taggroup skewxbuttongroup=dlggroupitems(skewxplusbutton, skewxminusbutton).dlgtablelayout(2,1,0)
		taggroup skewxgroup=dlggroupitems(skewxfieldgroup, skewxbuttongroup).dlgtablelayout(1,2,0)
		
		label=dlgcreatelabel("Skew_Y/%")
		taggroup skewyfield=dlgcreaterealfield(0, 8, 4,"skewychanged").dlgidentifier("skewyfield").dlgenabled(0)
		taggroup skewyfieldgroup=dlggroupitems(label, skewyfield).dlgtablelayout(1,2,0)
		taggroup skewyplusbutton=dlgcreatepushbutton("+","skewyplusresponse").dlgidentifier("skewyplusbutton")
		taggroup skewyminusbutton=dlgcreatepushbutton("-","skewyminusresponse").dlgidentifier("skewyminusbutton").dlginternalpadding(3,0)
		
		taggroup skewybuttongroup=dlggroupitems(skewyplusbutton, skewyminusbutton).dlgtablelayout(2,1,0)
		taggroup skewygroup=dlggroupitems(skewyfieldgroup, skewybuttongroup).dlgtablelayout(1,2,0)

		taggroup skewxandygroup=dlggroupitems(skewxgroup, skewygroup).dlgtablelayout(2,1,0)
		
				
		// Create a button for sourcing the image

		taggroup imagebuttongroup=dlggroupitems(sourceimagebutton, clearbutton).dlgtablelayout(2,1,0)
		box_items.dlgaddelement(imagebuttongroup)
		dialog_items.dlgaddelement(box)
		
		
		// Creates a box in the dialog which surrounds Grid part of the dialog

		taggroup gridbox_items
		taggroup gridbox=dlgcreatebox(" Define Ideal Lattice  ", gridbox_items)
		gridbox.dlgexternalpadding(3,0)
		gridbox.dlginternalpadding(20,3)

		taggroup colangleanddistortiongroup=dlggroupitems(columnanglegroup, distortionbutton).dlgtablelayout(2,1,0)
		taggroup gridboxgroup=dlggroupitems(gridsizeandradiusgroup, gridspacinggroup, originfieldsgroup, colangleanddistortiongroup).dlgtablelayout(1,4,0).dlgidentifier("gridboxgroup").dlgenabled(0)
		gridbox_items.dlgaddelement(gridboxgroup)
		dialog_items.dlgaddelement(gridbox)


		// Create a box for distorting the grid
		
		taggroup distortbox_items
		taggroup distortbox=dlgcreatebox(" Fit Experimental Lattice ", distortbox_items)
		distortbox.dlgexternalpadding(3,0)
		distortbox.dlginternalpadding(27,3)

		taggroup distortboxgroup=dlggroupitems(skewxandygroup, rotationandrefinelockgroup).dlgtablelayout(1,3,0).dlgidentifier("distortboxgroup").dlgenabled(0)
		distortbox_items.dlgaddelement(distortboxgroup)
		dialog_items.dlgaddelement(distortbox)


		// Create a box for optimising the gird and undistorting the image
		
		taggroup colourbox_items
		taggroup colourbox=dlgcreatebox("  Colourise  ", colourbox_items)
		colourbox.dlgexternalpadding(3,0).dlginternalpadding(12,10)


		// The radio to select which colour to use

		number colourradioval
		getpersistentnumbernote("Atom Colouriser:Settings:Colour Radio (0-2)", colourradioval)

		taggroup colourisebutton=dlgcreatepushbutton("Colourise","colouriseresponse")
		taggroup colourradioitems
		taggroup colourradio=dlgcreateradiolist(colourradioitems, colourradioval).dlgidentifier("colourradio").dlgchangedmethod("colourradiochanged")
		colourradioitems.dlgaddradioitem("1", 0)
		colourradioitems.dlgaddradioitem("2", 1).dlginternalpadding(0,2)
		colourradioitems.dlgaddradioitem("3", 2)


		// The radio to select line or fill

		number lineorfillradioval
		getpersistentnumbernote("Atom Colouriser:Settings:Line or Fill Radio (0-1)", lineorfillradioval)

		taggroup lineorfillradioitems
		taggroup lineorfillradio=dlgcreateradiolist(lineorfillradioitems, lineorfillradioval).dlgidentifier("lineorfillradio").dlgchangedmethod("lineorfillradiochanged")
		lineorfillradioitems.dlgaddradioitem("Line", 0)
		lineorfillradioitems.dlgaddradioitem("Fill", 1)

		image colourgraphic=rgbimage("",4,16,16)
		number red, green, blue
		getpersistentnumbernote("Atom Colouriser:Settings:Button 1 Colour (Red)", red)
		getpersistentnumbernote("Atom Colouriser:Settings:Button 1 Colour (Green)", green)
		getpersistentnumbernote("Atom Colouriser:Settings:Button 1 Colour (Blue)", blue)
		colourgraphic=rgb(red, green, blue)
		taggroup colourbutton1=dlgcreatedualstatebevelbutton("colourbutton1", colourgraphic, colourgraphic, "colourbuttonresponse")

		getpersistentnumbernote("Atom Colouriser:Settings:Button 2 Colour (Red)", red)
		getpersistentnumbernote("Atom Colouriser:Settings:Button 2 Colour (Green)", green)
		getpersistentnumbernote("Atom Colouriser:Settings:Button 2 Colour (Blue)", blue)
		colourgraphic=rgb(red, green, blue)
		taggroup colourbutton2=dlgcreatedualstatebevelbutton("colourbutton2", colourgraphic, colourgraphic, "colourbuttonresponse")

		getpersistentnumbernote("Atom Colouriser:Settings:Button 3 Colour (Red)", red)
		getpersistentnumbernote("Atom Colouriser:Settings:Button 3 Colour (Green)", green)
		getpersistentnumbernote("Atom Colouriser:Settings:Button 3 Colour (Blue)", blue)
		colourgraphic=rgb(red, green, blue)
		taggroup colourbutton3=dlgcreatedualstatebevelbutton("colourbutton3", colourgraphic, colourgraphic, "colourbuttonresponse")

		taggroup maskbutton=dlgcreatepushbutton("Extract Mask", "maskbuttonresponse").dlgidentifier("maskbutton").dlgenabled(0)

		taggroup colourbuttongroup=dlggroupitems(colourbutton1, colourbutton2, colourbutton3).dlgtablelayout(1,3,0)
		taggroup colourbuttonandradiogroup=dlggroupitems(colourradio, colourbuttongroup).dlgtablelayout(2,1,0).dlgexternalpadding(8,0)
		taggroup colouriseandlineorfillgroup=dlggroupitems(colourisebutton, lineorfillradio).dlgtablelayout(1,2,0).dlgexternalpadding(8,0)

		taggroup allcolourgroup=dlggroupitems(colourbuttonandradiogroup, colouriseandlineorfillgroup).dlgtablelayout(2,1,0).dlgenabled(0).dlgidentifier("allcolourgroup")

		
		// Define the tools icons for the tools button
				
		realimage toolsicon:=[21,20]:
			{
				{204,204,205,204,205,204,204,204,204,205,205,204,205,205,204,204,204,204,205,204,204},
				{204,204,204,205,205,204,204,204,204,205,204,204,204,205,204,204,204,204,205,204,204},
				{204,205,205,205,204,204,204,205,204,204,204,205,204,204,204,204,205,204,205,204,205},
				{205,204,204,205,205,204,205,204,205,204,0,0,0,0,204,204,204,205,204,205,204},
				{205,204,204,205,204,204,204,204,204,0,0,106,105,0,0,0,204,204,204,204,204},
				{205,205,204,205,204,0,0,0,204,204,204,0,0,105,105,105,0,204,204,204,204},
				{204,204,204,204,204,204,0,0,205,204,205,205,0,105,105,105,0,205,204,204,204},
				{205,205,204,0,205,205,0,0,205,204,205,204,0,0,106,105,0,0,205,205,205},
				{205,205,205,0,0,0,0,0,205,205,205,0,45,0,0,0,105,105,204,204,204},
				{205,204,204,0,0,0,0,205,0,204,0,45,0,204,204,0,105,0,204,204,204},
				{205,204,205,205,204,204,205,0,204,0,45,0,204,204,204,204,0,204,205,205,204},
				{205,204,204,204,205,204,204,205,0,204,0,204,204,204,204,204,204,204,205,205,204},
				{205,204,204,204,205,205,204,0,44,0,205,0,204,204,205,205,205,204,205,204,204},
				{204,205,204,204,204,204,0,44,0,204,0,204,0,204,205,205,204,205,204,204,205},
				{204,204,204,204,204,0,44,0,204,204,205,0,205,0,204,205,205,205,204,204,204},
				{204,204,205,205,0,44,0,204,204,204,205,204,0,205,0,204,205,204,205,204,204},
				{204,204,205,205,0,0,204,205,204,204,204,205,205,0,0,205,204,204,205,204,204},
				{204,204,205,204,204,205,204,204,204,204,204,205,204,204,204,205,205,204,204,204,204},
				{204,204,205,204,205,204,204,204,204,204,204,204,204,204,205,204,205,205,205,204,205},
				{204,205,205,205,205,205,204,204,204,204,205,205,204,205,205,204,204,205,205,205,204}
			}
					
		image toolsbuttonicon=toolsicon.dlgmakeraised()
		taggroup toolsbutton=dlgcreatebevelbutton(toolsicon,toolsbuttonicon, "toolsbuttonpressed").dlgidentifier("toolsbutton")
		taggroup padding=dlgcreatelabel("").dlgexternalpadding(4,0)
		taggroup toolsgroup=dlggroupitems(toolsbutton, padding).dlgtablelayout(2,1,0).dlganchor("East")

		taggroup  helpbutton=dlgcreatepushbutton("?", "helpbuttonpressed").dlgidentifier("helpbutton").dlginternalpadding(2,0)
		taggroup buttongroup=dlggroupitems(maskbutton, toolsbutton, helpbutton).dlgtablelayout(3,1,0)		
		
		taggroup colourboxgroup=dlggroupitems(allcolourgroup, buttongroup).dlgtablelayout(1,2,0)
		colourbox.dlgaddelement(colourboxgroup)

		dialog_items.dlgaddelement(colourbox)
		taggroup footer=dlgcreatelabel(" v1.1 Oct. 2022")
		dialog_items.dlgaddelement(footer)

		number screenwidth, screenheight
		getscreensize(screenwidth, screenheight)
		number dialogtop, dialogleft
		getpersistentnumbernote("Atom Colouriser:Settings:Dialog Top", dialogtop)
		getpersistentnumbernote("Atom Colouriser:Settings:Dialog Left", dialogleft)

		if(dialogleft<0) dialogleft=0
		if(dialogleft>(0.85*screenwidth)) dialogleft=0.85*screenwidth
		if(dialogtop<0) dialogtop=0
		if(dialogtop>(0.85*screenheight)) dialogtop=0.85*screenheight
		
		self.init(dialog)
		display(self, "Atom Colouriser")
		documentwindow dialogwin=self.getframewindow()
		dialogwin.windowsetframeposition(dialogleft, dialogtop)
	}


// The constructor this calls the makedialog() function and displays it

AtomColouriserDialog(object self)
	{
		self.makeDialog()
		
		// Allocate the RedrawDialog object for use by the subdialog later

		RedrawDialogObject=alloc(RedrawDialogClass)
	}


// The destructor is called when the object (the dialog) is closed

~AtomColouriserDialog(object self)
	{
	}
}


// This is called when the Save button in the sub-dialog is called
// it closes the main periodic table. It contains a dummy thread called Go
// This does nothing and so end immediately, and as it is going out of scope
// its destructor is called. The destructor redraws the Periodic Table dialog
// with an updated colour button

class RedrawDialogClass:object
{
number DialogID

object init(object self,number DialogIDP)
	{
		DialogID = DialogIDP
		return self
	}
	
	//dummy thread - which does nothing except end. As it is going out of scope
	// its destructor is called. This closes the periodic table dialog and then 
	// redraws it. This object is in effect a suicide object, the death of which
	// is used to trigger the redrawing of the dialog
	
void Go(object self) 
	{
		// Thread which does nothing except end and invoke the destructor
	}	


// The destructor is called when the thread ends. It closes the Periodic Table
// dialog and then redraws it

~RedrawDialogClass(object self) 
	{
	
	// Check that the main dialog is still displayed and valid
	
	if(MainDialogObject.ScriptObjectIsValid())
		{
			// close it then recreate it
			
			if(MainDialogObject.GetFrameWindow().WindowIsValid()) MainDialogObject.GetFrameWindow().WindowClose(0)	
			maindialogobject.MakeDialog()
			
			
			// Set the enabled status to the same as when the colour button was pressed
			
			maindialogobject.setelementisenabled("gridboxgroup",0)
			maindialogobject.setelementisenabled("distortboxgroup",0)
			maindialogobject.setelementisenabled("allcolourgroup",1)
			maindialogobject.setelementisenabled("maskbutton",1)
		}
	}
}


// Main script starts here

void main()
	{
		// this calls the constructor for the Periodic Table dialog
		
		maindialogobject=alloc(AtomColouriserDialog)
		
		// The sub-dialog is created within the main dialog object in order
		// to ensure the two objects can communicate. However, it is not displayed
		// until called when an element button is pressed
		
		subdialogobject=alloc(SubDialogClass)
	}

main()

// allocates the above function which puts it all together
