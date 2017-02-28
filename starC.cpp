#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <vector>
#include <queue>
#include <stack>
#include <set>
#include <map>
#include <list>
#include <utility>

using namespace std;

struct node{
	std::vector<stack <char> > state;
	struct node *parent;
	std::pair<int,int>  action; 
	int gCost, hCost;
};

struct compare{
	bool operator()(node* const& n1, node* const& n2){
		return (n1->gCost + n1->hCost) > (n2->gCost + n2->hCost);
	}
};

int goalA(vector<stack <char> > actual, vector<stack <char> > goal){
	int i, j, res = 1;

	for(i = 0; i < goal.size(); i++){		
		if( goal[i].size() > 0 && goal[i].top() == 'X'){
			goal[i].pop();
			continue;
		}else if(actual[i].size() != goal[i].size()){			
			return 0;				
		}while( goal[i].size() > 0){
			if(actual[i].top() != goal[i].top()){
				return 0;
			}
			actual[i].pop();
			goal[i].pop();
		}
	}
	return res;
}

int heuristic(vector<stack <char> > actual, vector<stack <char> > goal){
	int i, j, dif, s1, s2, res = 0;

	for(i = 0; i < goal.size(); i++){
		while( goal[i].size() > 0 && actual[i].size() > 0){
			if(goal[i].top() != 'X'){		
				dif = actual[i].size() - goal[i].size();
				if( dif > 0 ){
					while(dif > 0){
						actual[i].pop();
						res++;
						dif--;
					}
				}else if( dif < 0 ){
					while(dif < 0){
						goal[i].pop();
						res++;
						dif++;
					}
				}
				if(actual[i].top() != goal[i].top()){
					res++;
				}
				actual[i].pop();
				goal[i].pop();
			}else{
				goal[i].pop();
				do{
					actual[i].pop();
				}while(actual[i].size() > 0);

			}
		}
	}
	return res;
}

int expandNode(struct node **child, struct node *parent, pair<int,int> action, int limit){	
	char aux;
	//Para que solo expanda nodos validos
	if( !(parent->state[action.first].empty()) && (parent->state[action.second].size() < limit)){		
		(*child) = new node;
		(*child)->parent = parent;
		(*child)->state = parent->state;
		(*child)->action = action;

		aux = (*child)->state[action.first].top();
		(*child)->state[action.second].push( aux );

		(*child)->state[action.first].pop();

		(*child)->gCost = parent->gCost + (1 + abs(action.first - action.second));
		return 1;
	}
	return 0;
}

//Main
int main(int arg, char** argv){
	char box;
	int fin = 0, i, j, maxHeight;

	string init,goal;

	stack<char>temp;
	vector<stack <char> > goalState;
	stack<pair <int, int> > solution;
	pair<int,int>  action;

	priority_queue <node *,vector<node *>, compare> frontier;
	map < vector<stack <char> >, int > isInFrontier;
	map < vector<stack <char> >, int >::iterator itFrontier;

	set < vector<stack <char> > > explored;
	set < vector<stack <char> > >::iterator itExplored;
	
	struct node *root = new node;
	struct node *actualNode = new node;
	struct node *childNode = new node;

	cin >> maxHeight; 
	getline(cin,init);
	getline(cin,init);
	getline(cin,goal);

	if(root != NULL){
		for(int k =0;k < init.length(); k++){
			if(init[k]=='('){
				while(!temp.empty())
					temp.pop();
			}else if(init[k]==')'){
				root->state.push_back(temp);
			}else if(init[k]>=65 && init[k]<=90){
				temp.push(init[k]);
			}
		}
		while(!temp.empty()){temp.pop();}

		root->parent = NULL;
		root->gCost = 0;
	}

    //Crates
	for(int k =0;k < goal.length(); k++){
		if(goal[k]=='X'){
			temp.push(goal[k]);
			goalState.push_back(temp);
		}else if(goal[k]=='(' || goal[k]==';'){
			while(!temp.empty()){temp.pop();}
		}else if(goal[k]==')'){
			goalState.push_back(temp);
		}else if(goal[k]>=65 && goal[k]<=90){
			temp.push(goal[k]);
		}
	}
	while(!temp.empty()){temp.pop();}
		

	root->hCost = heuristic(root->state, goalState);

	frontier.push( root );
	isInFrontier.insert( map< vector<stack <char> >, int >::value_type(root->state, root->gCost + root->hCost) );

	explored.clear();

	do{
		if(isInFrontier.empty()){
			cout << "No solution found" << endl;
			return -1;			
		}

		do{
			actualNode = frontier.top();
			frontier.pop();
		}while(isInFrontier.erase(actualNode->state) != 1);  
				
		if(goalA(actualNode->state, goalState) == 1){
			cout << actualNode->gCost << endl;
			while(actualNode->parent != NULL){
				solution.push(actualNode->action);
				actualNode = actualNode->parent;
			}

			while(!(solution.empty()) ){
				cout << "(" << solution.top().first << "," << solution.top().second << ") " << endl;
				solution.pop();
			}
			return 1;
		}
		
		explored.insert(actualNode->state);

		for(i = 0; i < goalState.size(); i++){
			for(j = 0; j < goalState.size(); j++){
				if(i != j){				
					action = make_pair(i, j); 					
					if(expandNode(&childNode, actualNode, action, maxHeight) == 1){
						childNode->hCost = heuristic(childNode->state, goalState);

						itExplored = explored.find(childNode->state);
						itFrontier = isInFrontier.find(childNode->state);
						if(itExplored == explored.end()){					
							frontier.push(childNode);
							isInFrontier.insert( map< vector<stack <char> >, int >::value_type(childNode->state, childNode->gCost + childNode->hCost) );
						}
						if( itFrontier != isInFrontier.end() && itFrontier->second > (childNode->gCost + childNode->hCost)){
							isInFrontier.erase(itFrontier);
							frontier.push(childNode);
							isInFrontier.insert( map< vector<stack <char> >, int >::value_type(childNode->state, childNode->gCost + childNode->hCost) );
					
						}
					}
				}
			}
		}
	}while(frontier.size() > 0);
	cout << "No solution found" << endl;
	return 0;
}