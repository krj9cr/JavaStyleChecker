// Karen Johnson (krj9cr)
// Kyle Sullivan (kas2ud)

import java.awt.Point;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

import world.Robot;
import world.World;

public class HW2 extends Robot {
	public PriorityQueue<MyPoint> openList;
	int numRows;
	int numCols;
	int depth = 0;
	double w1 = 0.5;
	double w2 = 2.0;
	double assumptionPercentage;
	private MyPoint[][] map;
	private ArrayList<Point> path = new ArrayList<Point>();
	private Map<MyPoint,MyPoint> came_from = new HashMap<MyPoint,MyPoint>();
	private MyPoint start = new MyPoint(0, 0);
	private MyPoint end = new MyPoint(0, 0);
	public static boolean uncertainty = true; //CHANGE THIS TO AFFECT UNCERTAINTY
	
	//Constructor takes start/end positions and
	//number of rows and columns in the World map
	public HW2(MyPoint startPos, MyPoint endPos, int rows, int cols){
		start = startPos;
		end = endPos;
		numRows = rows;
		numCols = cols;
		map = new MyPoint[numRows][numCols];
		//determines whether or not to assume O or X
		//commented out part bases percentage on World size but doesn't work well lol
		assumptionPercentage = 0.50;//(((double)(100.0-(double)(numRows*numCols)))/100.0);
	}
	
	public void aStar(PriorityQueue<MyPoint> input){
		//set up queue with start node
		input.add(this.start);
		this.start.setVisited(true);
		this.start.setHeurDist(Math.abs(this.start.getX()-end.getX())+Math.abs(this.start.getY()-end.getY()));
		this.start.setDist(0);
		this.start.setPointType("S");
		map[(int) start.getX()][(int) start.getY()] = this.start;
		//while queue is not empty
		while (input.size() != 0){
			MyPoint currNode = input.peek();
			//check if end node
			if (currNode.getX() == end.getX() && currNode.getY() == end.getY()) {
				//reconstruct path
				path = reconstructPath(came_from, end, currNode);
				break; //yes, less pinging
			}
			//remove from queue and mark the map as visited/processed
			input.remove();
			currNode.setVisited(true);
			currNode.setProcessed(true);
			//for each neighbor
			for (int i = (int) (currNode.getX()-1); i <= (int) (currNode.getX()+1); i++){
				for (int j = (int) (currNode.getY()-1); j <= (int) (currNode.getY()+1); j++){
					//make sure index isn't out of bounds
					if (i < 0 || j < 0 || i > this.numRows -1 || j > this.numCols - 1){
						continue;
					}
					//check if already processed
					if (map[i][j].isProcessed()){
						continue;
					}
					MyPoint neighbor = (map[i][j]);
					//see if we already know the point type or not
					if (neighbor.getPointType().equals("")) {
							//ping
							String pointType = super.pingMap(new Point(i,j));
							neighbor.setPointType(pointType);
						
						//check if an obstacle
						if (!neighbor.getPointType().equals("X")) {
							//calculate stuff
							int tentative_g_score = (int) currNode.getDist() + 1;
							if (!neighbor.isVisited() || tentative_g_score < neighbor.getDist()) {
								came_from.put(neighbor, currNode);
								neighbor.setDist(tentative_g_score);
								//manhattan distance vs euclidean distance
								//neighbor.setHeurDist(Math.abs(neighbor.getX()-end.getX())+Math.abs(neighbor.getY()-end.getY()));
								neighbor.setHeurDist(neighbor.distance(end));
								if (!neighbor.isVisited()) {
									input.add(neighbor);
								}
							}
						}
					}

				}
			} //end for loop
		} //end while loop
		//move through path
		for (int i = path.size()-1; i >= 0; i--) {
			Point next = path.get(i);
			this.move(next);
		}
	}
	
	public void aStar2(PriorityQueue<MyPoint> input){
		//set up the queue with the start node
		input.add(this.start);
		this.start.setVisited(true);
		this.start.setHeurDist(Math.abs(this.start.getX()-end.getX())+Math.abs(this.start.getY()-end.getY()));
		this.start.setDist(0);
		this.start.setPointType("S");
		map[(int) start.getX()][(int) start.getY()] = this.start;
		//while queue is not empty
		while (input.size() != 0){
			MyPoint currNode = input.peek();
			//check if end node
			if (currNode.getX() == end.getX() && currNode.getY() == end.getY()) {
				//reconstruct path
				path = reconstructPath(came_from, end, currNode);
				break; //breaking here causes less pinging
			}
			//remove from queue and mark the map as visited/processed
			input.remove();
			currNode.setVisited(true);
			currNode.setProcessed(true);
			//for each neighbor
			for (int i = (int) (currNode.getX()-1); i <= (int) (currNode.getX()+1); i++){
				for (int j = (int) (currNode.getY()-1); j <= (int) (currNode.getY()+1); j++){
					//make sure index isn't out of bounds
					if (i < 0 || j < 0 || i > this.numRows -1 || j > this.numCols - 1){
						continue;
					}
					//check if already processed
					if (map[i][j].isProcessed()){
						continue;
					}
					//grab the neighbor
					MyPoint neighbor = (map[i][j]);
					//see if we already know the point type or not
					if (neighbor.getPointType().equals("")) {
							//ping a bunch of times
							double num_O = 0;
							double num_X = 0;
							String pointType = "";
							for (int p = 0; p < 10; p++) {
								 pointType = super.pingMap(new Point(i,j));
								 if (pointType.equals("X"))
									 num_X++;
								 else if (pointType.equals("O") || pointType.equals("F"))
									 num_O++;
							}
							//test if percentage of O's is above some value
							//commented out stuff moves the robot to validate the point and moves it back
							if (num_O/(num_O+num_X) > assumptionPercentage) {
								//System.out.println(this.move(new Point(i,j)));
								//test if move worked
								//if (this.getPosition().equals( new Point(i,j))) {
									neighbor.setPointType("O");
									//move back to current
									//System.out.println(this.move(new Point((int)currNode.getX(), (int)currNode.getY())));
								//}
							}
							else {
								neighbor.setPointType("X");
							}
						
						//check if an obstacle
						if (!neighbor.getPointType().equals("X")) {
							//calculate stuff
							int tentative_g_score = (int) currNode.getDist() + 1;
							depth = tentative_g_score;
							if (!neighbor.isVisited() || tentative_g_score < neighbor.getDist()) {
								came_from.put(neighbor, currNode);
								neighbor.setDist(tentative_g_score);
								//manhattan distance vs euclidean distance
								//neighbor.setHeurDist(Math.abs(neighbor.getX()-end.getX())+Math.abs(neighbor.getY()-end.getY()));
								neighbor.setHeurDist(neighbor.distance(end));
								if (!neighbor.isVisited()) {
									input.add(neighbor);
								}
							}
						}
					}

				}
			} //end for loop
			//plan ahead 7 nodes and move through them
			if (depth % 7 == 0 && depth != 0) {
				path = reconstructPath(came_from, input.peek(), currNode);
				for (int i = path.size()-1; i >= 0; i--) {
					Point next = path.get(i);
					if (!next.equals(this.getPosition()))
						this.move(next);
				}
			}//end for loops
		} //end while loop
		//move through path
		for (int i = path.size()-1; i >= 0; i--) {
			Point next = path.get(i);
			if (!next.equals(this.getPosition()))
				this.move(next);
		}
	}
	
	
	public ArrayList<Point> reconstructPath(Map<MyPoint,MyPoint> came_from, MyPoint current, MyPoint pos) {
		path.add(new Point((int)current.getX(), (int)current.getY()));
		while (came_from.containsKey(current)) {
			current = came_from.get(current);
			if (current != start)
				path.add(new Point((int)current.getX(), (int)current.getY()));
		}
		return path;
	}
	
	@Override
	public void travelToDestination() {
		//max size of PQ is number of positions minus start and final spots
		int size = (numRows*numCols);
		PriorityQueue<MyPoint> openList = new PriorityQueue<MyPoint>(size, new Comparator<MyPoint>() {
			@Override
			public int compare(MyPoint x, MyPoint y){
				if ((w1*x.getDist() + w2*x.getHeurDist()) < (w1*y.getDist() + w2*y.getHeurDist())){
					return -1;
				}
				if ((w1*x.getDist() + w2*x.getHeurDist()) > (w1*y.getDist() + w2*y.getHeurDist())){
					return 1;
				}
				return 0;
			}
		});
		//initialize map
		for (int i = 0;i<numRows;i++){
			for (int j=0;j<numCols;j++){
				MyPoint input = new MyPoint(i,j);
				//String pointType = super.pingMap(new Point(i,j));
				//input.setPointType(pointType);
				map[i][j] = input;
			}
		}
		//call astar
		if (uncertainty) {
			aStar2(openList);
		}
		else {
			aStar(openList);
		}
	}
	
	public static void main(String[] args) {
		try{
			World myWorld = new World("test3.txt", uncertainty);
			MyPoint initial = new MyPoint(myWorld.getStartPos());
			MyPoint last = new MyPoint(myWorld.getEndPos());
			int numRows = myWorld.numRows();
			int numCols = myWorld.numCols();
			HW2 myRobot = new HW2(initial, last, numRows, numCols);
			myRobot.addToWorld(myWorld);
			myRobot.travelToDestination();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}

}
