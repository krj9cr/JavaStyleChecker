
#include <stdio.h>
#include <mpi.h>

main(int argc, char **argv) 
{
	int ierr;

	ierr = MPI_Init(&argc, &argv);

	// Get the processor number of the current node
	int rank;
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	// Get the total number of nodes
	int numNodes;
	MPI_Comm_size(MPI_COMM_WORLD, &numNodes);

	// have rank 0 get the directory listing
	// pass the name of directory[i] to each respective rank i
	if (rank == 0) {
		DIR *d;
		struct dirent *dir;
		int count = 0;
		int index = 0;

		d = opendir("Data");
		if (d) {
			while ((dir = readdir(d)) != NULL) {
				printf("%s\n", dir->d_name);
				strcpy(name[count],dir->d_name);
				count++;
			}
			closedir(d);
		}

		while( count > 0 ) {
			printf("The directory list is %s\r\n",name[index]);
			index++;
			count--;
		}	
	}

	// have rank i execute checkstyle on its directory

	// either save the results to out.i.txt
	// or pass back to rank 0 and have rank 0 glom it together

	int total_projects = 10;

	int my_proj = rank;

	printf("Hello world\n"); 
	 
	ierr = MPI_Finalize();
}