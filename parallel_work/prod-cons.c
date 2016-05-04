// prod-cons.c

// Code skeleton for master/worker MPI setup orignally from:
// http://www.hpc.cam.ac.uk/using-clusters/compiling-and-development/parallel-programming-mpi-example

/****** OVERALL ALGORITHM ********

	1)	Master gets the list of project names from the specified directory

	2)	Master iterates through the list of projects, passing Workers a project name

	3)	Workers check the tag of the message to see if it's a terminating tag.
		If not terminating, the worker executes the checkstyle.jar on the project folder
		as well as the style.py parser on the .jar's output.

	6)	Terminates when Master finishes going through the list of projects

**********************************/

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>
#include <string.h>
#include <mpi.h>
#define WORKTAG    1
#define DIETAG     2
#define BUFF_SIZE 1024

void master();
void worker();

int myrank, ntasks;
double elapsed_time;
int use_script = 1; 	// zero = false, nonzero = true
int start_dir  = 0; 	// specifies what project in the list to start at
int end_dir    = 1000;	// specifies what project in the list to end at
int num_dirs   = 1007;	// the total number of project directories (yes, there is actually more than 1000)


//*****************************************//
//    				Main 			       //
//*****************************************//
main(int argc, char *argv[]) {
	MPI_Init(&argc, &argv);
	// Make sure everyone got here
	MPI_Barrier(MPI_COMM_WORLD);

	// Get current time
	elapsed_time = - MPI_Wtime();

	// Get process rank
	MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
	
	// Determine if master or worker
	if (myrank == 0) {
		master();
	} else {
		worker();
	}

	// Cleanup
	MPI_Finalize();
}

//*****************************************//
//    Stuff for master (rank 0) to do      //
//*****************************************//
void master() {
	int rank, work;
	char message[BUFF_SIZE];
	double result;
	MPI_Status status;
	MPI_Comm_size(MPI_COMM_WORLD, &ntasks); // get number of tasks

	// Print out whether or not script is being used
	if (use_script != 0) {
		printf("SCRIPT\n");
	}
	else {
		printf("NO SCRIPT\n");
	}

//-----------Get list of projects-----------//
	// directory junk
	DIR *dp;
	struct dirent *ep;

	dp = opendir ("localtmp/java_projects/"); // path to project directories
	int dir_count = 0; // counter
	char projects[num_dirs][BUFF_SIZE]; // list

	// Initialize in case of problems
	int i,j;
	for (i = 0; i < num_dirs; i++) {
		for (j = 0; j < BUFF_SIZE; j++) {
			projects[i][j] = "\0";
		}
	}

	printf("Initialized projects[][]\n");

	// Iterate through the directory and grab project directory names
	if (dp != NULL) {
		while (ep = readdir (dp)) {
			// Make sure we're not out of bounds
			if (dir_count >= num_dirs) {
				break;
			}
			// Make sure we don't consider the "." or ".." directories
			if (strcmp(ep->d_name,".") == 0 || strcmp(ep->d_name,"..") == 0) {
				continue;
			}
			// Add the project to the list of project names
			else {
				strcpy(projects[dir_count],ep->d_name);
				//printf("%s\n",projects[dir_count]); // uncomment this to print out all project names
				dir_count++;
			}
		}

		(void) closedir (dp);
	}
	else {
		perror ("Couldn't open the directory");
	}

	printf("Got project names\n");

//------------Seed workers--------------//
	dir_count = start_dir; // reset counter to be start location

	// Loop through all Workers once
	for (rank = 1; rank < ntasks; ++rank) {
		
		// Get the next work item
		strcpy(message,projects[dir_count]);

		MPI_Send(&message,	/* message buffer */
		BUFF_SIZE,          /* size of buffer */
		MPI_CHAR,        	/* data item is chars */
		rank,           	/* destination process rank */
		WORKTAG,        	/* work tag */
		MPI_COMM_WORLD);

		// Increment counter
		dir_count++;
	}

	printf("Seeded workers\n");

//----Recieve more requests and respond-----//	
	// Continue until we reach the specified end directory
	while (dir_count < end_dir) {

		// Get next item of work
		strcpy(message,projects[dir_count]);

		MPI_Recv(&result,/* dummy result */
		1,              /* one data item */
		MPI_DOUBLE,     /* of type double real */
		MPI_ANY_SOURCE, /* receive from any sender */
		MPI_ANY_TAG,    /* any type of message */
		MPI_COMM_WORLD,
		&status);       /* received message info */

		// Send piece of work
		MPI_Send(&message, BUFF_SIZE, MPI_CHAR, status.MPI_SOURCE,
		WORKTAG, MPI_COMM_WORLD);

		// Increment counter
		dir_count++;
	}

	printf("Telling workers to exit\n");

//--------Receive Final Requests----------//
	for (rank = 1; rank < ntasks; ++rank) {
		MPI_Recv(&result, 1, MPI_DOUBLE, MPI_ANY_SOURCE,
		MPI_ANY_TAG, MPI_COMM_WORLD, &status);

		printf("Received final request from %d\n",status.MPI_SOURCE);
	}

//--------Tell workers to die----------//
	for (rank = 1; rank < ntasks; ++rank) {
		MPI_Send(0, 0, MPI_INT, rank, DIETAG, MPI_COMM_WORLD);

		printf("Sent dietag to %d\n",rank);
	}

//---------DONE----------//
	printf("Done\n");

	// Get elapsed time
	elapsed_time += MPI_Wtime();
	printf("RESULT: %f\n",elapsed_time);
	fflush(stdout);
}


//*****************************************//
//   Stuff for worker (rank != 0) to do    //
//*****************************************//
void worker() {
	double 		result = 0.0; // dummy result
	char 		message[BUFF_SIZE]; // buffer for message
	MPI_Status	status;

	// Set up strings of commands
	int java_len  = 61;
	int path_len  = 28;
	int style_len = 20;
	int script_size = 10;
	char java[]  = "java -jar checkstyle-6.15-all.jar -c sun_checks.xml -o jar/";
	char path[]  = ".txt localtmp/java_projects/";
	char style[] = "python style.py jar/";
	char script[] = "./bash.sh ";

	// Copy to pointers
	char *java_ptr    = malloc(sizeof(char) * java_len);
	char *path_ptr    = malloc(sizeof(char) * path_len);
	char *style_ptr   = malloc(sizeof(char) * style_len);
	char *message_ptr = malloc(sizeof(char) * BUFF_SIZE);
	char *script_ptr  = malloc(sizeof(char) * script_size);
	
//----------Continuously Recv work-----------//
	for (;;) {
		MPI_Recv(&message, BUFF_SIZE, MPI_CHAR, 0, MPI_ANY_TAG,
		MPI_COMM_WORLD, &status);

		// Check for die tag
		if (status.MPI_TAG == DIETAG) {
			return;
		}

		printf("Rank %d recieved %s\n",myrank,message);

//-----------------DO WORK------------------//
		// Execute different commands depending on use of script or not
		if (use_script != 0) {
			// Pass project name to script
			strcpy(message_ptr,message);
			strcpy(script_ptr,script);
			script_ptr = strcat(script_ptr, message_ptr);

			// Execute the script, which executes the jar and python parser
			system(script_ptr);
		}
		else {
			// Piece together project name with commands
			strcpy(java_ptr,java);
			strcpy(path_ptr,path);
			strcpy(style_ptr,style);
			strcpy(message_ptr,message);

			java_ptr = strcat(java_ptr, message_ptr);
			java_ptr = strcat(java_ptr, path_ptr);
			java_ptr = strcat(java_ptr, message_ptr);

			style_ptr = strcat(style_ptr,message_ptr);
			style_ptr = strcat(style_ptr,".txt");

			// Execute jar
			system(java_ptr);
			// Execute python parser
			system(style_ptr);
		}
		
		// Send a request for more work
		MPI_Send(&result, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
	}
	fflush(stdout);
}
