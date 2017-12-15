var cytoscape = require("cytoscape");

var fs = require('fs');


var json = JSON.parse('{{json_data}}')
var output = '{{output_file}}'

var CytoscapeObj;

var cose_layout = {
  name: 'cose',

  // Called on `layoutready`
  ready: function(){},

  // Called on `layoutstop`
  stop: function(){},

  // Whether to animate while running the layout
  // true : Animate continuously as the layout is running
  // false : Just show the end result
  // 'end' : Animate with the end result, from the initial positions to the end positions
  animate: false,

  // Easing of the animation for animate:'end'
  animationEasing: undefined,

  // The duration of the animation for animate:'end'
  animationDuration: undefined,

  // A function that determines whether the node should be animated
  // All nodes animated by default on animate enabled
  // Non-animated nodes are positioned immediately when the layout starts
  animateFilter: function ( node, i ){ return false; },

  // Whether to fit the network view after when done
  fit: false,

  // Padding on fit
  padding: 30,

  // Constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
  boundingBox: undefined,

  // Excludes the label when calculating node bounding boxes for the layout algorithm
  nodeDimensionsIncludeLabels: false,

  // Randomize the initial positions of the nodes (true) or use existing positions (false)
  randomize: true,

  // Extra spacing between components in non-compound graphs
  componentSpacing: 40,

  // Node repulsion (non overlapping) multiplier
  nodeRepulsion: function( node ){ return 2048; },

  // Node repulsion (overlapping) multiplier
  nodeOverlap: 4,

  // Ideal edge (non nested) length
  idealEdgeLength: function( edge ){ return 32; },

  // Divisor to compute edge forces
  edgeElasticity: function( edge ){ return 32; },

  // Nesting factor (multiplier) to compute ideal edge length for nested edges
  nestingFactor: 1.2,

  // Gravity force (constant)
  gravity: 1,

  // Maximum number of iterations to perform
  numIter: 1000,

  // Initial temperature (maximum node displacement)
  initialTemp: 1000,

  // Cooling factor (how the temperature is reduced between consecutive iterations
  coolingFactor: 0.99,

  // Lower temperature threshold (below this point the layout will end)
  minTemp: 1.0,

  // Pass a reference to weaver to use threads for calculations
  weaver: false,

  zoom:0.3
};

var circle_layout = {name:'circle',fit:false,zoom:0.3}

var concentric_layout = {
  name: 'concentric',

  fit: true, // whether to fit the viewport to the graph
  padding: 30, // the padding on fit
  startAngle: 3 / 2 * Math.PI, // where nodes start in radians
  sweep: undefined, // how many radians should be between the first and last node (defaults to full circle)
  clockwise: true, // whether the layout should go clockwise (true) or counterclockwise/anticlockwise (false)
  equidistant: false, // whether levels have an equal radial distance betwen them, may cause bounding box overflow
  minNodeSpacing: 10, // min spacing between outside of nodes (used for radius adjustment)
  boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
  avoidOverlap: true, // prevents node overlap, may overflow boundingBox if not enough space
  nodeDimensionsIncludeLabels: false, // Excludes the label when calculating node bounding boxes for the layout algorithm
  height: undefined, // height of layout area (overrides container height)
  width: undefined, // width of layout area (overrides container width)
  spacingFactor: undefined, // Applies a multiplicative factor (>0) to expand or compress the overall area that the nodes take up
  concentric: function( node ){ // returns numeric value for each node, placing higher nodes in levels towards the centre
  return node.degree();
  },
  levelWidth: function( nodes ){ // the letiation of concentric values in each level
  return nodes.maxDegree() / 4;
  },
  animate: false, // whether to transition the node positions
  animationDuration: 500, // duration of animation in ms if enabled
  animationEasing: undefined, // easing of animation if enabled
  animateFilter: function ( node, i ){ return true; }, // a function that determines whether the node should be animated.  All nodes animated by default on animate enabled.  Non-animated nodes are positioned immediately when the layout starts
  ready: undefined, // callback on layoutready
  stop: undefined, // callback on layoutstop
  transform: function (node, position ){ return position; } // transform a given node position. Useful for changing flow direction in discrete layouts
};

buildCytoscape(json,enlargeNetwork);




//--------------------------------------------------------------------------------------------------

function buildCytoscape(json,enlargeNetwork){
	CytoscapeObj = cytoscape({
		layout: {name:'preset',fit:false,zoom:0.3},
		elements: json
	});


	if(CytoscapeObj.nodes()[0].position().x == 0 && CytoscapeObj.nodes()[0].position().y == 0){
	   var layout = null;

	   if(CytoscapeObj.nodes().length > 400){
            layout = CytoscapeObj.layout(circle_layout);
	   }else if(CytoscapeObj.nodes().length > 200){
            layout = CytoscapeObj.layout(concentric_layout);
	   }else{
            layout = CytoscapeObj.layout(cose_layout);
	   }

	    layout.promiseOn('layoutstop').then(function( event ){
            enlargeNetwork(0.5, CytoscapeObj);
            printNetworkPosition(CytoscapeObj);
        });
	    layout.run();
	}
}

//--------------------------------------------------------------------------------------------------

function printNetworkPosition(obj){
    var toWrite = "Node\tPosX\tPosY\n";

    allnodes = obj.nodes()

    for(var i = 0; i < obj.nodes().length; i++){
        nodedata = obj.nodes()[i].data();
        nodepos = obj.nodes()[i].position();
        toWrite = toWrite + nodedata["id"]+"\t"+nodepos["x"]+"\t"+nodepos["y"]+"\n";
    }
    fs.writeFile(output, toWrite);
}

//--------------------------------------------------------------------------------------------------

function enlargeNetwork(factor,CytoscapeObj){
	//get corner of the network
	min_x = 999999999
	max_x = -999999999
	min_y = 999999999
	max_y = -999999999

	CytoscapeObj.nodes().forEach(function(s){
		if(s.position()["x"]>max_x){
			max_x = s.position()["x"]
		}
		if(s.position()["x"]<min_x){
			min_x = s.position()["x"]
		}
		if(s.position()["y"]>max_y){
			max_y = s.position()["y"]
		}
		if(s.position()["y"]<min_y){
			min_y = s.position()["y"]
		}
	});

	length = max_x-min_x;
	height = max_y-min_y;

	center_x = min_x+length/2;
	center_y = min_y+height/2;

	new_min_x = center_x-length;
	new_max_x = center_x+length;

	new_min_y = center_x-height;
	new_max_y = center_x+height;

	CytoscapeObj.nodes().forEach(function(s){
		s.position()["x"] = s.position()["x"]+((1+factor)*(s.position()["x"]-center_x));
		s.position()["y"] = s.position()["y"]+((1+factor)*(s.position()["y"]-center_y));
	});
	return CytoscapeObj;
}