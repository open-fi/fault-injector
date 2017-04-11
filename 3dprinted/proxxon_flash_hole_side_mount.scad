$fn=36;
$outer=9;
$inner=6;
$height_base=3;
$height_coupling=10;

union(){
   translate([0,0,0])
	difference(){
		cube([90,60,$height_base],center=true);
	    cylinder(d=14,h=1e3,center=true);	
	   }

	translate([-45.0/2-40,0,$height_base/2+50/2])
	cylinder(d=20,50,center=true);

   translate([-65,0,0])
	cube([40,60,$height_base],center=true);


}