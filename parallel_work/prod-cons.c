// prod-cons.c

// Code structure used from: 
// http://www.hpc.cam.ac.uk/using-clusters/compiling-and-development/parallel-programming-mpi-example

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

main(int argc, char *argv[]) {
	MPI_Init(&argc, &argv);
	// Make sure everyone got here
	MPI_Barrier(MPI_COMM_WORLD);

	// Get current time
	elapsed_time = - MPI_Wtime();

	MPI_Comm_rank(MPI_COMM_WORLD, &myrank); /* process rank, 0 thru N-1 */
	
	if (myrank == 0) {
		master();
	} else {
		worker();
	}

	MPI_Finalize(); /* cleanup MPI */
}

void master() {
	int rank, work;
	char message[BUFF_SIZE];
	double       result;
	MPI_Status     status;
	MPI_Comm_size(MPI_COMM_WORLD, &ntasks); /* #processes in application */

/*
* Set up the queue
*/
	DIR *dp;
	struct dirent *ep;
	dp = opendir ("localtmp/java_projects/");
	int num_dirs = 1015;
	int dir_count = 0;
	char projects[num_dirs][BUFF_SIZE];

	// init?
	int i,j;
	for (i = 0; i < num_dirs; i++) {
		for (j = 0; j < BUFF_SIZE; j++) {
			projects[i][j] = "\0";
		}
	}

	printf("Initialized projects[][]\n");

	if (dp != NULL) {
		while (ep = readdir (dp)) {
			if (strcmp(ep->d_name,".") == 0 || strcmp(ep->d_name,"..") == 0) {
				continue;
			}
			else {
				//puts (ep->d_name);
				strcpy(projects[dir_count],ep->d_name);
				//projects[dir_count] = (ep->d_name);
				//printf("%s\n",projects[dir_count]);
				dir_count++;
			}
		}

		(void) closedir (dp);
	}
	else {
		perror ("Couldn't open the directory");
	}

	printf("Got project names\n");

/*
* Seed the workers.
*/
	dir_count = 0;

	for (rank = 1; rank < ntasks; ++rank) {
		//work = 0/* get_next_work_request */;
		strcpy(message,projects[dir_count]);

		//printf("Next message: %s\n",message);

		//message = &projects[dir_count];
		MPI_Send(&message,         /* message buffer */
		BUFF_SIZE,              /* one data item */
		MPI_CHAR,        /* data item is an integer */
		rank,           /* destination process rank */
		WORKTAG,        /* user chosen message tag */
		MPI_COMM_WORLD);/* always use this */

		//printf("Sent work to %d\n",rank);

		dir_count++;
	}

	printf("Seeded workers\n");

/*
* Receive a result from any worker and dispatch a new work
* request work requests have been exhausted.
*/
	int tmp_num_dirs = 100;
	//while (dir_count < num_dirs) {
	while (dir_count < tmp_num_dirs) {
		strcpy(message,projects[dir_count]);

		//printf("Next message: %s\n",message);

		MPI_Recv(&result,       /* message buffer */
		1,              /* one data item */
		MPI_DOUBLE,     /* of type double real */
		MPI_ANY_SOURCE, /* receive from any sender */
		MPI_ANY_TAG,    /* any type of message */
		MPI_COMM_WORLD, /* always use this */
		&status);       /* received message info */

		//printf("Received request from %d\n",status.MPI_SOURCE);

		MPI_Send(&message, BUFF_SIZE, MPI_CHAR, status.MPI_SOURCE,
		WORKTAG, MPI_COMM_WORLD);

		//printf("Sent work to %d\n",status.MPI_SOURCE);

		dir_count++;
	}

	printf("Telling workers to exit\n");
/*
* Receive results for outstanding work requests.
*/
	for (rank = 1; rank < ntasks; ++rank) {
		MPI_Recv(&result, 1, MPI_DOUBLE, MPI_ANY_SOURCE,
		MPI_ANY_TAG, MPI_COMM_WORLD, &status);

		printf("Received final request from %d\n",status.MPI_SOURCE);
	}
/*
* Tell all the workers to exit.
*/
	for (rank = 1; rank < ntasks; ++rank) {
		MPI_Send(0, 0, MPI_INT, rank, DIETAG, MPI_COMM_WORLD);

		printf("Sent dietag to %d\n",rank);
	}

	printf("Done\n");
	// Get elapsed time
	// Only need to do it for process 0, because it does the final output
	elapsed_time += MPI_Wtime();
	printf("RESULT: %f\n",elapsed_time);
	fflush(stdout);
}

void worker() {
	//printf("Hi I'm rank %d\n",myrank);

	double 		result = 0.0;
	int 		work;
	char 		message[BUFF_SIZE];
	//int java_len = 79;
	int java_len  = 61;
	int path_len  = 28;
	int style_len = 20;
	char java[]  = "java -jar checkstyle-6.15-all.jar -c mediawiki.xml -o jar/";
	char path[]  = ".txt localtmp/java_projects/";
	char style[] = "python style.py jar/";

	char *java_ptr    = malloc(sizeof(char) * java_len);
	char *path_ptr    = malloc(sizeof(char) * path_len);
	char *style_ptr   = malloc(sizeof(char) * style_len);
	char *message_ptr = malloc(sizeof(char) * BUFF_SIZE);
	

	MPI_Status	status;
	
	for (;;) {
		MPI_Recv(&message, BUFF_SIZE, MPI_CHAR, 0, MPI_ANY_TAG,
		MPI_COMM_WORLD, &status);
/*
* Check the tag of the received message.
*/
		if (status.MPI_TAG == DIETAG) {
			return;
		}

		printf("Rank %d recieved %s\n",myrank,message);

		// DO WORK
		//char command[2048] = strcat(strcat(strcat(strcat("java -jar checkstyle-6.15-all.jar -c google-style.xml ", &message), " > out/"), &message), ".txt");
		
		strcpy(java_ptr,java);
		strcpy(path_ptr,path);
		strcpy(style_ptr,style);
		strcpy(message_ptr,message);

		java_ptr = strcat(java_ptr, message_ptr);
		java_ptr = strcat(java_ptr, path_ptr);
		java_ptr = strcat(java_ptr, message_ptr);

		style_ptr = strcat(style_ptr,message_ptr);
		style_ptr = strcat(style_ptr,".txt");

		//printf("Rank %d cmd: %s\n",myrank,java_ptr);

		// execute jar
		
		int ret;
		//if( !(ret = system(java_ptr)) ) {
			system(java_ptr);
		    //printf("Command executed normally\n");
		    // execute python parser
			system(style_ptr);
		//}


		//printf("Rank %d freed\n",myrank);
		
		// Send a request for more work
		MPI_Send(&result, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);

		printf("Rank %d requesting more work\n",myrank);
	}
	fflush(stdout);
}
