$fn=72;
//$fs=0.1;
// +1 for smaller printing
$outer=11+3;
$inner=9+1.4;
$height=15;
$hole=2;

union(){
    translate([0,0,1])
	difference(){
		cylinder(d=$outer, h=2, center=true);
        cylinder(d=$hole, h=1e3,center=true);
	
	}
	translate([0,0,$height/2+1])		
    difference(){
		cylinder(d=$outer, h=$height, center=true);
        cylinder(d=$inner,h=1e3,center=true);
	}

}